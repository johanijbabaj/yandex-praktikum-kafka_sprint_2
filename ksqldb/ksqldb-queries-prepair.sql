-- Create a stream to ingest messages from Kafka
CREATE STREAM IF NOT EXISTS messages_stream (
    user_id STRING,
    recipient_id STRING,
    message STRING,
    timestamp BIGINT
) WITH (
    KAFKA_TOPIC='messages',
    VALUE_FORMAT='JSON'
);

-- Create a table to count the total number of sent messages
CREATE TABLE IF NOT EXISTS total_messages AS
  SELECT 'total' AS key, COUNT(*) AS total
  FROM messages_stream
  GROUP BY 'total'
  EMIT CHANGES;


-- Create a table to count unique recipients for all messages
CREATE TABLE IF NOT EXISTS total_unique_recipients AS
  SELECT 'global' AS dummy_key, COUNT_DISTINCT (recipient_id) AS unique_recipient_count
  FROM messages_stream
  GROUP BY 'global'
  EMIT CHANGES;


-- Create a table to identify the top active users by message count
CREATE TABLE IF NOT EXISTS users_activity AS
    SELECT user_id, COUNT(*) AS message_count
    FROM messages_stream
    GROUP BY user_id
    EMIT CHANGES;


-- Create a table to aggregate user statistics
CREATE TABLE IF NOT EXISTS user_statistics AS
    SELECT 
        user_id,
        COUNT(*) AS message_count,
        COUNT_DISTINCT (recipient_id) AS unique_recipient_count
    FROM messages_stream
    GROUP BY user_id
    EMIT CHANGES;


