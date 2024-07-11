from flask import jsonify
from config import CAFE24_CONFIG
from src.apis.cafe24_api import Cafe24API
from src.models.log import Log
from src.models.api_log import ApiLog
from src.models.product import Product
from src.utils.logger import logger
import json, time, math, string, os

class Cafe24Service:
    def __init__(self):
        self.cafe24_api = Cafe24API()
        self.shop_no = CAFE24_CONFIG['shop_no']

    def find_suppliers_count(self):
        return self.cafe24_api.find_suppliers_count()

    def find_product_count(self):
        return self.cafe24_api.find_product_count()

    def find_product(self, cafe24_product_no):
        return json.loads(self.cafe24_api.find_product(product_no=cafe24_product_no, params={'shop_no': self.shop_no}))

    def find_product_variant(self, cafe24_product_no, cafe24_variant_code):
        return self.cafe24_api.find_product_variant(product_no=cafe24_product_no, variant_code=cafe24_variant_code, params={'shop_no': self.shop_no})

    def find_supplier(self, cafe24_supplier_code):
        return self.cafe24_api.find_supplier(supplier_code=cafe24_supplier_code, params={'shop_no': self.shop_no})

    def find_suppliers_user(self, cafe24_supplier_user_id):
        return self.cafe24_api.find_suppliers_user(user_id=cafe24_supplier_user_id, params={'shop_no': self.shop_no})

    def find_suppliers(self, request):
        params = {
            'shop_no': self.shop_no,
            'user_id': request.get('user_id'),
            'supplier_code': request.get('supplier_code'),
            'supplier_name': request.get('supplier_name'),
            'limit': request.get('limit'),
            'offset': request.get('offset'),
            'fields': request.get('fields')
        }

        return self.cafe24_api.find_suppliers(params=params)

    def find_suppliers_users(self, request):
        params = {
            'shop_no': self.shop_no,
            'supplier_code': request.get('supplier_code'),
            'supplier_name': request.get('supplier_name'),
            'limit': request.get('limit'),
            'offset': request.get('offset'),
            'fields': request.get('fields')
        }

        return self.cafe24_api.find_suppliers_users(params=params)

    def find_products(self, request):
        params = {
            'shop_no': self.shop_no,
            'product_no': request.get('product_no'),
            'since_product_no': request.get('since_product_no'),
            'limit': request.get('limit'),
            'offset': request.get('offset'),
            'fields': request.get('fields')
        }

        return self.cafe24_api.find_products(params=params)

    def find_product_variants(self, cafe24_product_no):
        return self.cafe24_api.find_product_variants(product_no=cafe24_product_no)

    def update_product(self, origin_product_no):
        return self.__update_products(origin_products=[Product.find_by_id(product_no=origin_product_no)])

    def update_products(self):
        return self.__update_products(origin_products=Product.find_all())

    def update_suppliers_users(self, request):
        params = {
            'shop_no': self.shop_no,
            'supplier_code': request.get('supplier_code'),
            'limit': request.get('limit'),
            'offset': request.get('offset'),
            'fields': 'supplier_code'
        }

        # 등록되어 있는 공급사 조회
        cafe24_suppliers = json.loads(self.cafe24_api.find_suppliers(params=params))
    
        return self.__update_suppliers_users(cafe24_suppliers=cafe24_suppliers)

    def delete_product(self, cafe24_product_no):
        return self.delete_product(product_no=cafe24_product_no)

    # API 호출은 초당 2회 제한이 있기 때문에 API이 호출되기 전에 sleep으로 지연이 필요
    def __update_products(self, origin_products=None):
        if not origin_products:
            return jsonify([])

        try:
            result_cafe24_products = []
            for origin_product in origin_products:
                time.sleep(0.3)

                # 무게와 부피 중에 큰 값으로 무게 설정, 소수점 2자리까지 올림 처리하여 표시
                product_weight = int(origin_product['box_weight'])
                product_volume = int(origin_product['box_volume'])
                weight = (product_weight if product_weight > product_volume else product_volume) / 1000
                weight = math.ceil(weight * 100) / 100

                # 자체 서비스 코드로 카페24 API에 조회
                # custom_product_code 필드는 콤마로 구분해서 다중 조회가 가능
                # API 문서에는 100개 미만까지 가능하다고 되어 있지만 실제 호출 시 10개까지만 조회되는 것을 확인
                # 그래서 일단 상품은 단일로 조회
                params = {
                    "shop_no": self.shop_no,
                    "custom_product_code": str(origin_product['id'])
                }
                
                cafe24_products = json.loads(self.cafe24_api.find_products(params=params))
                for cafe24_product in cafe24_products['products']:
                    # 카페24 상품 API에 custom_product_code로 조회 시 LIKE 검색으로 조회되기 때문에 일치하는지 확인이 필요
                    if str(origin_product['id']) == str(cafe24_product['custom_product_code']):
                        time.sleep(0.3)

                        api_log_message = "UPDATE PRODUCT(NOT THUMB)"
                        request_data = {
                            "shop_no": self.shop_no,
                            "hscode": str(origin_product['hscode']),
                            "product_weight": str(weight),
                            "description": str(origin_product['short_description']) + str(origin_product['details']) + str(origin_product['description']),
                            "product_volume": {
                                "use_product_volume": "T",
                                "product_width": origin_product['box_width'],
                                "product_height": origin_product['box_height'],
                                "product_length": origin_product['box_length']
                            }
                        }

                        if origin_product['thumb']:
                            request_data['detail_image'] = str(origin_product['thumb'])
                            request_data['image_upload_type'] = "A" # 대표이미지 등록
                            api_log_message = "UPDATE PRODUCT"

                        # update product
                        cafe24_update_product = self.cafe24_api.update_product(product_no=str(cafe24_product['product_no']), request_data=request_data)
                        ApiLog.save(type='product', message=api_log_message, orgin_key=origin_product['id'], cafe24_key=int(cafe24_product['product_no']), response=cafe24_update_product)
                        result_cafe24_products.append(cafe24_product)

                        time.sleep(0.3)

                        # 카페24 상품 품목 조회
                        cafe24_product_variants = json.loads(self.cafe24_api.find_product_variants(product_no=str(cafe24_product['product_no'])))

                        request_data = []
                        for idx, variants in enumerate(cafe24_product_variants['variants']):
                            # 옵션이 없어도 품목이 조회되는 경우 발생
                            # 품목 옵션이 있는 경우만 데이터 배열에 저장
                            if variants['options']:
                                # 순차적인 알파벳
                                unique_char = self.__generate_alphabet_sequence(idx)
                                request_data.append({
                                    "shop_no": self.shop_no,
                                    "variant_code": variants['variant_code'],
                                    "custom_variant_code": f"{unique_char}{cafe24_product['product_no']}" # [A-Z]+[0-9]+
                                })

                        api_log_message = 'NOT OPTIONS'
                        cafe24_update_product_variants = None
                        if request_data:
                            # update product variants
                            cafe24_update_product_variants = self.cafe24_api.update_product_variants(product_no=str(cafe24_product['product_no']), request_data=request_data)
                            api_log_message = 'UPDATE PRODUCT VARIANTS'

                        ApiLog.save(type='product', message=api_log_message, orgin_key=origin_product['id'], cafe24_key=int(cafe24_product['product_no']), response=cafe24_update_product_variants)
                        result_cafe24_products.append(cafe24_product)

            return jsonify(result_cafe24_products)
        except Exception as e:
            logger.error(f"Failed to update products: {e}")
            Log.save("ERROR", f"Failed to update products: {e}")
            raise

    def __update_suppliers_users(self, cafe24_suppliers=None):
        if not cafe24_suppliers:
            return jsonify([])

        try:
            result_cafe24_suppliers_users = []
            for cafe24_supplier in cafe24_suppliers['suppliers']:
                time.sleep(0.3)

                params = {
                    'supplier_code': str(cafe24_supplier['supplier_code']),
                    'fields': 'user_id'
                }

                cafe24_suppliers_users = json.loads(self.cafe24_api.find_suppliers_users(params=params))
                for cafe24_suppliers_user in cafe24_suppliers_users['users']:
                    # 공급사 수정은 user_id로 해야하는데 없는 경우가 있어서 확인이 필요
                    if cafe24_suppliers_user['user_id']:
                        time.sleep(0.3)

                        request_data = {
                            'permission_shop_no': [2], # 접근 가능 쇼핑몰
                            'permission_category_select': 'F', # 상품 등록 시 분류선택 권한
                            'permission_product_modify': 'T', # 상품 수정 권한
                            'permission_product_display': 'F', # 상품 진열 권한
                            'permission_product_selling': 'F', # 상품 판매 권한
                            'permission_product_delete': 'F', # 등록 상품 삭제 권한
                            'permission_order_menu': 'T', # 주문 메뉴 접근 권한
                            'permission_amount_inquiry': 'T' # 주문 금액 조회 권한
                        }

                        cafe24_update_suppliers_user = self.cafe24_api.update_suppliers_user(user_id=str(cafe24_suppliers_user['user_id']), request_data=request_data)
                        ApiLog.save(type='suppliers user', message='UPDATE SUPPLIERS USER', cafe24_key=str(cafe24_supplier['supplier_code']), response=cafe24_update_suppliers_user)

                        result_cafe24_suppliers_users.append(str(cafe24_suppliers_user['user_id']))

            return jsonify(result_cafe24_suppliers_users)

        except Exception as e:
            logger.error(f"Failed to update suppliers users: {e}")
            Log.save("ERROR", f"Failed to update suppliers users: {e}")
            raise

    def __generate_alphabet_sequence(self, index):
        alphabet = string.ascii_uppercase
        length = len(alphabet)
        result = ""

        while index >= 0:
            result = alphabet[index % length] + result
            index = index // length - 1

        return result
