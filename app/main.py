import faust
import os
import logging
import re

from app.config.logging_config import configure_logging


# Set up logging
configure_logging()
logger = logging.getLogger(__name__)


# Define Faust Record class for message structure
class Message(faust.Record):
    user_id: str
    recipient_id: str
    text: str

# Initialize the Faust application
app = faust.App(
    'message_filter_app',
    broker='kafka://kafka-00:9092',
    store='memory://'
)

# Kafka topics
messages_topic = app.topic('messages', value_type=Message)  # Use the Message class here
filtered_messages_topic = app.topic('filtered_messages', value_type=Message)  # Use the Message class here

# Paths to the files containing lists
BLOCKED_USERS_FILE = 'blocked_users.csv'
CENSORED_WORDS_FILE = 'censored_words.csv'

# Lists for blocking and censorship
blocked_users = set()
censored_words = set()

# Compile a regex pattern that matches any of the censored words
def get_censored_pattern():
    if censored_words:
        return re.compile(r'\b(' + '|'.join(map(re.escape, censored_words)) + r')\b')
    return None

# Load the list of blocked users
def load_blocked_users():
    global blocked_users
    if os.path.exists(BLOCKED_USERS_FILE):
        with open(BLOCKED_USERS_FILE, 'r') as f:
            blocked_users = set(f.read().splitlines())

# Load the list of censored words
def load_censored_words():
    global censored_words
    if os.path.exists(CENSORED_WORDS_FILE):
        with open(CENSORED_WORDS_FILE, 'r') as f:
            censored_words = set(f.read().splitlines())

# Function for logging word replacement
def log_replacement(match):
    word = match.group(0)
    if word:  # Ensure the word is not empty
        # Log the word and its replacement
        logger.info(f"Word '{word}' found in message. Replacing with {'*' * len(word)}")
        return '*' * len(word)
    return word


# Filter messages
@app.agent(messages_topic)
async def process_messages(stream):
    global censored_pattern
    async for message in stream:
        load_blocked_users()
        load_censored_words()
        censored_pattern = get_censored_pattern()

        logger.info(f"Message type: {type(message)}")
        logger.info(f"Message object: {message}")

        if isinstance(message, dict):
            message_value = message
        else:
            message_value = message.__dict__

        user_id = message_value.get('user_id')
        text = message_value.get('text', '')

        # Check for blocked users
        if user_id in blocked_users:
            logger.info(f'Skipping message from {user_id} due to blocked_user ban')
            continue

        ## Censoring words in the message text using regex and logging replacements
        if censored_pattern:
            text = censored_pattern.sub(log_replacement, text)
        else:
            logger.info(f'censored_pattern empty')

        # Send the filtered message
        await filtered_messages_topic.send(value={
            'user_id': user_id,
            'recipient_id': message_value.get('recipient_id'),
            'text': text
        })

if __name__ == '__main__':
    app.main()
