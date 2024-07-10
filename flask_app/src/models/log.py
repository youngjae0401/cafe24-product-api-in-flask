from database import Database
from datetime import datetime

'''
CREATE TABLE `logs` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `level` varchar(10) DEFAULT NULL,
    `message` longtext,
    `created_at` datetime DEFAULT NULL,
    PRIMARY KEY (`id`)
)
'''

class Log:
    def save(level, message):
        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor()

        try:
            insert_query = '''
            INSERT INTO logs (level, message, created_at)
            VALUES (%s, %s, %s)
            '''
            cursor.execute(insert_query, (
                level,
                message,
                datetime.now()
            ))
            connection.commit()
        except Exception as e:
            raise
        finally:
            cursor.close()
