# Kafka Streams project sprint 2
# Stream Processing Project: User Blocking and Message Censorship

This project demonstrates a stream processing system that implements user blocking and message censorship using Apache Kafka and Docker Compose. Additionally, it includes an optional ksqlDB-based analytics task for deeper exploration of stream processing.

---

## Features

### Task 1: Stream Processing with User Blocking and Message Censorship
- **User Blocking**:  
  Allows users to block unwanted users and filters messages from blocked users.  
  Block lists are stored locally on disk.
- **Message Censorship**:  
  Implements a censorship mechanism for prohibited words. Messages pass through a censorship component before delivery.  
  Prohibited words can be updated dynamically.

### Task 2: Real-Time Analytics with ksqlDB
- **Real-Time Analytics**:  
  Processes incoming JSON messages and calculates the following metrics in real-time:
  - Total number of messages sent.
  - Number of unique recipients.
  - Top 5 most active users by sent messages.
- **User Statistics Aggregation**:  
  Provides per-user statistics including the total number of messages sent and the number of unique recipients.

---

## Project Structure

### Directories and Files
- `docker-compose.yml`: Configures and deploys the infrastructure for Kafka, ksqlDB, and supporting services.
- `app/`: Contains the code for user blocking and message censorship.
  - `blocked_users.csv`: Contains list of blocked users.
  - `censored_words.csv`: Contains list of censored words.
  - `main.py`: Faust application that implement logic of blocking users and updated messages.
- `ksqldb/`: Contains ksqlDB queries and configurations.
  - `ksqldb-queries.sql`: Queries for creating streams, tables, and performing analytics.
- `utlis/`: Includes code for test messages generation.

---

## Instructions

### Prerequisites
- [Docker](https://www.docker.com/) installed on your system.
- [Docker Compose](https://docs.docker.com/compose/) installed.

### Setup and Deployment
1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/johanijbabaj/yandex-praktikum-kafka_sprint_2.git
   cd yandex-praktikum-kafka_sprint_2
   ```

2. **Start the Environment**:  
   ```bash
   docker-compose up -d
   ```

3. **Prepare Kafka Topics and Streams**:  
  Create the required topics for the project using the Kafka CLI or Kafka UI tool [localhost:8085](http://localhost:8085/ui/clusters/kraft/all-topics?)
    - messages: Incoming messages.
    - filtered_messages: Processed messages.
    - create ksql streams and tables: 
        ```bash
      docker exec -i ksqldb-cli-00 ksql http://ksqldb-server-00:8088 < ksqldb/ksqldb-queries-prepair.sql
      ```

4. **Run Stream Processing**:  
    Execute the stream processing code
    ```bash
    docker exec -it faust-app python utils/kafka_message_producer.py
    ```

5. **Run Stream Processing**:  
    Execute the stream processing code
    ```bash
    docker exec -it faust-app python utils/kafka_message_producer.py
    ```
6. **Check filtered_messages topic with UI:**
    - 20% off the messages fro the *messages* topic from the blocked users shouldn't be sent to the *filtered_messages* topic
    - 20% off the messages should be sent with censorshiped words and changed to the ****** in  *filtered_messages* topic

### Testing ksqlDB Analytics

1. **Send Test Messages**:  
    - **Run script to generate the random messages**: 
      ```bash
      docker exec -it faust-app python utils/kafka_message_producer.py
      ```
2. **Run Queries**:  
   Use the following options verify analytics:

   - **Run all queries from the sql file**:  
     ```bash
     docker exec -i ksqldb-cli-00 ksql http://ksqldb-server-00:8088 < ksqldb/ksqldb-queries-tests.sql 
     ```
   - **Run all with UI from the file**:  
     use queries from the file documentation [ksqldb-queries-tests.sql](ksqlb/ksqldb-queries-tests.sql) 
     
  


