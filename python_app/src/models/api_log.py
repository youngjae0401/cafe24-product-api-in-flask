from database import Database
from datetime import datetime

'''
CREATE TABLE `api_logs` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `type` varchar(50) DEFAULT NULL,
    `message` varchar(100) DEFAULT NULL,
    `origin_key` varchar(100) DEFAULT NULL,
    `cafe24_key` varchar(100) DEFAULT NULL,
    `response` longtext,
    `created_at` datetime DEFAULT NULL,
    PRIMARY KEY (`id`)
)
'''

class ApiLog:
    def save(type=None, message=None, origin_key=None, cafe24_key=None, response=None):
        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor()

        try:
            insert_query = '''
                INSERT INTO api_logs (type, message, origin_key, cafe24_key, response, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (
                type,
                message,
                origin_key,
                cafe24_key,
                response,
                datetime.now()
            ))
            connection.commit()
        except Exception as e:
            raise
        finally:
            cursor.close()
