## Task 2: Create database and table

### 建立 website 資料庫

```sql
CREATE DATABASE website;
USE website;
CREATE TABLE member (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    follower_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

```
![task2截圖](image/task_2.png)