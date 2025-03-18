# InSpectra-Backend-AlgorithmHub

now it still have problem after run docker compose up it need to

docker exec -it inspectra-backend-algorithmhub-mysql-db-1 mysql -uuser -ppassword

and input

CREATE DATABASE IF NOT EXISTS algorithm_db;
USE algorithm_db;
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    job_id VARCHAR(255) UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'queued' NOT NULL
);

to create table