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

@cafe24_bp.route('/suppliers-count', methods=['GET'])
def call_find_supplier_count():
    return cafe24_service.find_suppliers_count()

@cafe24_bp.route('/suppliers', methods=['GET'])
def call_find_suppliers():
    return cafe24_service.find_suppliers(request.args)

@cafe24_bp.route('/supplier/<string:cafe24_supplier_code>', methods=['GET'])
def call_find_supplier(cafe24_supplier_code):
    return cafe24_service.find_supplier(cafe24_supplier_code=cafe24_supplier_code)

@cafe24_bp.route('/suppliers/users', methods=['GET'])
def call_find_suppliers_users():
    return cafe24_service.find_suppliers_users(request.args)

@cafe24_bp.route('/suppliers/user/<string:cafe24_supplier_user_id>', methods=['GET'])
def call_find_suppliers_user(cafe24_supplier_user_id):
    return cafe24_service.find_suppliers_user(cafe24_supplier_user_id=cafe24_supplier_user_id)

@cafe24_bp.route('/update-supplier-users', methods=['GET'])
def call_update_suppliers_users():
    return cafe24_service.update_suppliers_users(request.args)

@cafe24_bp.route('/customers', methods=['GET'])
def call_find_customers():
    return cafe24_service.find_customers(request.args)

@cafe24_bp.route('/orders', methods=['GET'])
def call_find_orders():
    return cafe24_service.find_orders(request.args)
