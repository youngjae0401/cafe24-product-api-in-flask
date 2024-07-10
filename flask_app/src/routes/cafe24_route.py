from flask import Blueprint, request
from src.services.cafe24_service import Cafe24Service

cafe24_bp = Blueprint('cafe24', __name__, url_prefix='/cafe24')
cafe24_service = Cafe24Service()

@cafe24_bp.route('/product-count', methods=['GET'])
def call_find_product_count():
    return cafe24_service.find_product_count()

@cafe24_bp.route('/products', methods=['GET'])
def call_find_products():
    return cafe24_service.find_products(request.args)

@cafe24_bp.route('/product/<string:cafe24_product_no>', methods=['GET'])
def call_find_product(cafe24_product_no):
    return cafe24_service.find_product(cafe24_product_no=cafe24_product_no)

@cafe24_bp.route('/update-products', methods=['GET'])
def call_update_products():
    return cafe24_service.update_products()

@cafe24_bp.route('/update-product/<string:origin_product_no>', methods=['GET'])
def call_update_product(origin_product_no):
    return cafe24_service.update_product(origin_product_no=origin_product_no)

@cafe24_bp.route('/product/<string:cafe24_product_no>/variants', methods=['GET'])
def call_find_product_variants(cafe24_product_no):
    return cafe24_service.find_product_variants(cafe24_product_no=cafe24_product_no)

@cafe24_bp.route('/product/<string:cafe24_product_no>/variants/<string:cafe24_variant_code>', methods=['GET'])
def call_find_product_variant(cafe24_product_no, cafe24_variant_code):
    return cafe24_service.find_product_variant(cafe24_product_no=cafe24_product_no, cafe24_variant_code=cafe24_variant_code)

@cafe24_bp.route('/delete-product/<string:cafe24_product_no>', methods=['GET'])
def call_delete_product(cafe24_product_no):
    return cafe24_service.delete_product(cafe24_product_no=cafe24_product_no)
