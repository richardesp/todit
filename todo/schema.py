
# Lista de instrucciones que le iremos mandando secuencialmente a mysql

instructions = [
    "SET FOREIGN_KEY_CHECKS = 0", # Desactivar la validación de claves foráneas para poder borrar
    "DROP TABLE IF EXISTS Task",
    "DROP TABLE IF EXISTS User",
    "SET FOREIGN_KEY_CHECKS = 1", # La vuelvo a activar por seguridad en la integridad y consistencia de la bd
    """
    CREATE TABLE User (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(64) UNIQUE NOT NULL,
        password VARCHAR(256) NOT NULL
    )
    """,
    """
    CREATE TABLE Task (
        id INT PRIMARY KEY AUTO_INCREMENT,
        created_by INT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL,
        FOREIGN KEY (created_by) REFERENCES User (id)
    )
    """
]