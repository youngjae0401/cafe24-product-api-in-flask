from database import Database
from datetime import datetime

'''
CREATE TABLE `api_logs` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `api_type` varchar(100) DEFAULT NULL,
    `product_id` bigint DEFAULT NULL,
    `cafe24_product_id` bigint DEFAULT NULL,
    `response` longtext,
    `created_at` datetime DEFAULT NULL,
    PRIMARY KEY (`id`)
)
'''

class ApiLog:
    def save(api_type, product_id, cafe24_product_id, response):
        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor()

        try:
            insert_query = '''
            INSERT INTO api_logs (api_type, product_id, cafe24_product_id, response, created_at)
            VALUES (%s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (
                api_type,
                product_id,
                cafe24_product_id,
                response,
                datetime.now()
            ))
            connection.commit()
        except Exception as e:
            raise
        finally:
            cursor.close()
