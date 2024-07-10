from database import Database

'''
CREATE TABLE `cafe24_authorization` (
    `id` bigint unsigned NOT NULL AUTO_INCREMENT,
    `access_token` varchar(100) NOT NULL,
    `expires_at` datetime NOT NULL,
    `refresh_token` varchar(100) NOT NULL,
    `refresh_token_expires_at` datetime NOT NULL,
    `issued_at` datetime NOT NULL,
    PRIMARY KEY (`id`),
    KEY `cafe24_autorization_access_token_IDX` (`access_token`) USING BTREE,
    KEY `cafe24_autorization_expires_at_IDX` (`expires_at`) USING BTREE
)
'''

class Cafe24Authorization:
    def find_one():
        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            select_query = '''
            SELECT
                access_token,
                expires_at,
                refresh_token,
                refresh_token_expires_at
            FROM
                cafe24_autorization
            ORDER BY id DESC
            LIMIT 1
            '''
            cursor.execute(select_query)
            return cursor.fetchone()
        except Exception as e:
            raise
        finally:
            cursor.close()

    def save(token_dict):
        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor()

        try:
            insert_query = '''
            INSERT INTO cafe24_autorization (access_token, expires_at, refresh_token, refresh_token_expires_at, issued_at)
            VALUES (%s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (
                token_dict['access_token'],
                token_dict['expires_at'],
                token_dict['refresh_token'],
                token_dict['refresh_token_expires_at'],
                token_dict['issued_at']
            ))
        except Exception as e:
            raise
        finally:
            cursor.close()
