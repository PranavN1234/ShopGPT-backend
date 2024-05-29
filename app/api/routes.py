from . import api_blueprint
from flask import request, jsonify
from app.services.openai_service import get_image_information
from app.services.openai_service import search_products
from app.services.awsdynamo_service import search_item_by_name, store_phone_number, get_tries
from app.services.twilio_service import send_twilio_otp, verify_twilio_otp
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


@api_blueprint.route('/send-otp', methods=['POST'])
def send_otp():

    data = request.json
    phone_number = data.get('phone_number')
    print('phone number is ', phone_number)
    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400

    store_phone_number(phone_number)

    try:
        verification_status = send_twilio_otp(phone_number)
        return jsonify({"status": verification_status}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_blueprint.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    otp = data.get('otp')
    phone_number = data.get('phone_number')

    if not otp:
        return jsonify({"error": "No OTP sent"}), 400

    try:
        status = verify_twilio_otp(otp, phone_number)
        if status == "approved":
            tries = get_tries(phone_number)
            print(tries)
            return jsonify({"status": status, "tries": tries}), 200
        return jsonify({"status": status}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500








