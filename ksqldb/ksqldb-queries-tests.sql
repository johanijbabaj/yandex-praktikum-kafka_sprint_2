-- Count the total number of sent messages
SELECT * FROM total_messages;


-- Count unique recipients for all messages
SELECT * FROM total_unique_recipients;


-- Count the top active users by message count
-- FIX IT: I can't find the way to use ORDER BY with LIMIT to get TOP users 
SELECT * FROM users_activity 
EMIT CHANGES 
LIMIT 5;


-- Aggregate user statistics
SELECT * FROM user_statistics;
