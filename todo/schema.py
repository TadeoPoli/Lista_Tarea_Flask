instructions = [
    """
        CREATE TABLE IF NOT EXISTS user (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE  NOT NULL,
            password VARCHAR(255) NOT NULL    
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    """
        CREATE TABLE IF NOT EXISTS todo (
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_by INT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            description TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT FALSE,
            CONSTRAINT fk_todo_user FOREIGN KEY (created_by) REFERENCES user (id),
            INDEX idx_todo_created_by_created_at (created_by, created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
]
