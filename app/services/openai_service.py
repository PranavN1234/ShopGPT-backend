import os
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from openai import OpenAI
from app.models import Product, Products
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
CHATGPT_MODEL = 'gpt-4o'

def get_image_information(image):
    chatinstance = OpenAI(api_key=OPENAI_API_KEY)
    response = chatinstance.chat.completions.create(
        model=CHATGPT_MODEL,
        messages=[
            {"role": "system", "content": "Identify Product from image"},
            {"role": "user", "content": [
                {"type": "text",
                 "text": "NAME the product, brand or item DON'T ADD ANYTHING ELSE IF YOU CANNOT RECOGNIZE IT RETURN NOTHING"},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image}"}
                 }
            ]}
        ],
        temperature=0
    )
    product_name = response.choices[0].message.content
    return product_name

def search_products(product_name):
    llm_openai = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o", temperature=0)
    parser = JsonOutputParser(pydantic_object=Products)
    format_response_parser = parser.get_format_instructions()

    prompt_template = '''Search the web for the product, \n {format_instructions} \n Question: {question}'''
    prompt = PromptTemplate(template=prompt_template, input_variables=["question"],
                            partial_variables={"format_instructions": format_response_parser})

    chain = prompt | llm_openai | parser
    response = chain.invoke({"question": product_name})

    try:
        # Attempt to parse the response as the Products model
        parsed_response = Products.parse_obj(response)
        products_list = []
        for product in parsed_response.products:
            print(f"Name: {product.name}, Link: {product.link}, Price: {product.price}, Website: {product.website}")
            products_list.append(product)
        return products_list
    except Exception as e:
        print(f"Error parsing response: {e}")
        print("Raw response:", response)

