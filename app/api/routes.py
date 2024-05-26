import os
from . import api_blueprint
from flask import request, jsonify, current_app
from flask_cors import CORS, cross_origin
from app.openai_service import get_image_information
from app.openai_service import search_products
from app.awsdynamo_service import search_item_by_name
import boto3

import base64

@api_blueprint.route('/', methods=['GET'])
def hello_world():
    return jsonify({"hello world": "hello world"})

@api_blueprint.route('/identify-image', methods=['POST'])
def get_image():
    try:
        image_file = request.files['image']
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
        product_name = get_image_information(image_data)
        return jsonify({"product_name": product_name})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api_blueprint.route('/shop-products', methods=['POST'])
def get_products():

    data = request.json
    product_name = data.get('product_name')

    products = search_products(product_name)

    products_with_brand = []

    for product in products:
        brand = search_item_by_name(product.website)

        if brand:
            product_dict = product.dict()
            product_dict['logo'] = brand['logo_url']
            query = brand['search_query'].replace('<search_query>', product.name)
            product_dict['search_query'] = query
        else:
            product_dict = product.dict()
            product_dict['logo'] = None
            product_dict['search_query'] = None

        products_with_brand.append(product_dict)

    return jsonify(products=products_with_brand)







