from database import Database

class Product:
    def find_all():
        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            select_query = '''
            SELECT
                id,
                hscode,
                title_en,
                weight,
                box_volume,
                box_width,
                box_length,
                box_height
            FROM
                products
            WHERE
                parent_id IS NULL
            ORDER BY id DESC
            LIMIT 1000
            '''
            cursor.execute(select_query)
            return cursor.fetchall()
        except Exception as e:
            raise
        finally:
            cursor.close()

    def find_by_id(product_no):
        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            select_query = '''
            SELECT
                id,
                hscode,
                title_en,
                weight,
                box_volume,
                box_width,
                box_length,
                box_height
            FROM
                products
            WHERE
                id = %(product_no)s
            AND
                parent_id IS NOT NULL
            '''
            cursor.execute(select_query, {'product_no': product_no})
            return cursor.fetchone()
        except Exception as e:
            raise
        finally:
            cursor.close()
