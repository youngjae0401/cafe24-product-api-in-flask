from database import Database

class Product:
    def __get_common_select_fields():
        return '''
            p.id,
            p.hscode,
            COALESCE(p.weight, 0) AS box_weight,
            COALESCE(p.box_volume, 0) AS box_volume,
            COALESCE(p.box_width, 0) AS box_width,
            COALESCE(p.box_height, 0) AS box_height,
            COALESCE(p.box_length, 0) AS box_length,
            IF(p.short_description IS NOT NULL AND p.short_description != '', CONCAT(p.short_description, '<br>'), '') AS short_description
            COALESCE(p.description, '') AS description,
            COALESCE(
                (
                    SELECT
                        CONCAT_WS(
                            '/',
                            '/web/product',
                            SUBSTRING(MD5(CONCAT('$', SUBSTRING(m.id, 1, LENGTH(m.id) - 4))), 1, 2),
                            SUBSTRING(MD5(CONCAT('$', SUBSTRING(m.id, 1, LENGTH(m.id) - 4))), 3, 2),
                            SUBSTRING(m.id, 1, LENGTH(m.id) - 4),
                            m.file_name
                        )
                    FROM
                        media m
                    WHERE
                        m.model_id = p.id
                    AND
                        m.model_type = 'product'
                    AND
                        m.collection_name = 'products'
                    AND
                        (m.file_name LIKE '%%.jpg%%' OR m.file_name LIKE '%%.png%%' OR m.file_name LIKE '%%.jpeg%%' OR m.file_name LIKE '%%.gif%%' OR m.file_name LIKE '%%.webp%%')
                    GROUP BY
                        m.collection_name, m.model_id
                    ORDER BY
                        m.order_column
                    LIMIT 1
                ),
                ''
            ) AS thumb,
            COALESCE(
                (
                    SELECT
                        GROUP_CONCAT(
                            CONCAT(
                                '<p style="text-align: center;"><img src="',
                                CONCAT_WS(
                                    '/',
                                    '/web/product',
                                    SUBSTRING(MD5(CONCAT('$', SUBSTRING(m.id, 1, LENGTH(m.id) - 4))), 1, 2),
                                    SUBSTRING(MD5(CONCAT('$', SUBSTRING(m.id, 1, LENGTH(m.id) - 4))), 3, 2),
                                    SUBSTRING(m.id, 1, LENGTH(m.id) - 4),
                                    m.file_name
                                ),
                                '"></p>'
                            )
                        SEPARATOR '') 
                    FROM
                        media m
                    WHERE
                        m.model_id = p.id
                    AND
                        m.model_type = 'product'
                    AND
                        m.collection_name = 'details'
                    GROUP BY
                        m.collection_name, m.model_id
                ),
                ''
            ) AS details
        '''

    def find_all():
        db = Database()
        connection = db.get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            select_query = f'''
                SELECT
                    {Product.__get_common_select_fields()}
                FROM
                    products p
                WHERE
                    p.parent_id IS NULL
                ORDER BY p.id DESC
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
            select_query = f'''
                SELECT
                    {Product.__get_common_select_fields()}
                FROM
                    products p
                WHERE
                    p.id = %(product_no)s
                AND
                    p.parent_id IS NOT NULL
            '''
            cursor.execute(select_query, {'product_no': product_no})
            return cursor.fetchone()
        except Exception as e:
            raise
        finally:
            cursor.close()
