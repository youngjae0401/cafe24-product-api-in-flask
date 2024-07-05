from flask import jsonify
from src.apis.cafe24_api import Cafe24API
from src.models.log import Log
from src.models.api_log import ApiLog
from src.models.product import Product
from src.utils.logger import logger
import json, time

class Cafe24Service:
    def __init__(self):
        self.cafe24_api = Cafe24API()

    def find_product_count(self):
        return self.cafe24_api.find_product_count()
        
    def find_product(self, cafe24_product_no):
        return json.loads(self.cafe24_api.find_product(product_no=cafe24_product_no))

    def find_products(self, request):
        params = {
            'product_no': request.get('product_no'),
            'since_product_no': request.get('since_product_no'),
            'limit': request.get('limit'),
            'offset': request.get('offset')
        }
        
        return self.cafe24_api.find_products(params=params)
    
    def update_product(self, origin_product_no):
        return self.__private_update_products(origin_products=[Product.find_by_id(product_no=origin_product_no)])
        
    def update_products(self):
        return self.__private_update_products(origin_products=Product.find_all())
    
    def find_product_variant(self, cafe24_product_no, cafe24_variant_code):
        return self.cafe24_api.find_product_variant(product_no=cafe24_product_no, variant_code=cafe24_variant_code)
    
    def find_product_variants(self, cafe24_product_no):
        return self.cafe24_api.find_product_variants(product_no=cafe24_product_no)
    
    def delete_product(self, cafe24_product_no):
        return self.delete_product(product_no=cafe24_product_no)
    
    # API 호출은 초당 2회 제한이 있기 때문에 API이 호출되기 전에 sleep이 필요하다.
    def __private_update_products(self, origin_products):
        try:
            result_cafe24_products = []
            for origin_product in origin_products:
                time.sleep(0.5)

                # 자체 서비스 코드로 카페24 API에 조회
                # custom_product_code 필드는 콤마로 구분해서 다중 조회가 가능
                # API 문서에는 100개 미만까지 가능하다고 되어 있지만 실제 호출 시 10개까지만 조회되는 것을 확인
                # 그래서 일단 상품은 단일로 조회
                params = {
                    "shop_no": 1,
                    "custom_product_code": str(origin_product['id'])
                }
                cafe24_products = json.loads(self.cafe24_api.find_products(params=params))
                
                for cafe24_product in cafe24_products['products']:
                    # 카페24 상품 API에 custom_product_code로 조회 시 LIKE 검색으로 조회되기 때문에 일치하는지 확인이 필요
                    if str(origin_product['id']) == str(cafe24_product['custom_product_code']):
                        
                        time.sleep(0.5)
                        
                        logger.info(f"product_no = {cafe24_product['product_no']}")

                        # 수정할 상품 정보
                        request_product_data = {
                            "shop_no": 1,
                            "hscode": "",
                            "product_weight": "",
                            "product_volume": {
                                "use_product_volume": "",
                                "product_width": "",
                                "product_height": "",
                                "product_length": ""
                            }
                        }
                        
                        # update product
                        cafe24_update_product = self.cafe24_api.update_product(product_no=str(cafe24_product['product_no']), request_data=request_product_data)
                        ApiLog.save('UPDATE PRODUCT', origin_product['id'], int(cafe24_product['product_no']), cafe24_update_product)

                        time.sleep(0.5)
                        
                        # 카페24 상품 품목 조회
                        cafe24_product_variants = json.loads(self.cafe24_api.find_product_variants(product_no=str(cafe24_product['product_no'])))
                        
                        request_product_variant_data = []
                        for idx, variants in enumerate(cafe24_product_variants['variants']):
                            # 옵션이 없어도 품목이 조회되는 경우 발생
                            # 품목 옵션이 있는 경우만 데이터 배열에 저장
                            if variants['options']:
                                # 수정할 상품 품목 정보
                                request_product_variant_data.append({
                                    "shop_no": 1,
                                    "variant_code": variants['variant_code'], # 필수
                                    "custom_variant_code": ""
                                })
                        
                        api_log_message = 'NOT OPTIONS'
                        cafe24_update_product_variants = None
                        if request_product_variant_data:
                            # update product variants
                            cafe24_update_product_variants = self.cafe24_api.update_product_variants(product_no=str(cafe24_product['product_no']), request_data=request_product_variant_data)
                            api_log_message = 'UPDATE PRODUCT VARIANTS'
                        
                        ApiLog.save(api_log_message, origin_product['id'], int(cafe24_product['product_no']), cafe24_update_product_variants)
                        
                        result_cafe24_products.append(cafe24_product)

            return jsonify(result_cafe24_products)
        except Exception as e:
            logger.error(f"Failed to update products: {e}")
            Log.save("ERROR", f"Failed to update products: {e}")
            raise
