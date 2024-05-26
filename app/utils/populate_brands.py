import requests
from io import BytesIO
from PIL import Image
from app import create_app, db
from app.models import Brand

def download_and_process_logo(url, size=(100, 100)):
    print('processed:', url)
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image = image.convert('RGB')  # Ensure the image is in RGB format
    image = image.resize(size)  # Resize image to the desired size
    output = BytesIO()
    image.save(output, format='JPEG')  # Save the image as JPEG to maintain consistency
    return output.getvalue()

# List of brands with their details

brands = [
    {
        "name": "Amazon",
        "logo_url": "https://www.fineprintart.com/images/blog/amazon-logo/amazon_logo_history_5.jpg",
        "search_query": "https://www.amazon.com/s?k=<search_query>"
    },
    {
        "name": "eBay",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/4/48/EBay_logo.png",
        "search_query": "https://www.ebay.com/sch/i.html?_nkw=<search_query>"
    },
    {
        "name": "Target",
        "logo_url": "https://icon2.cleanpng.com/20180925/piu/kisspng-logo-symbol-target-corporation-brand-image-the-mall-at-prince-georges-directory-hyattsvil-5baaa280d54053.2640922315379093768735.jpg",
        "search_query": "https://www.target.com/s?searchTerm=<search_query>"
    },
    {
        "name": "Walmart",
        "logo_url": "https://s3.amazonaws.com/www-inside-design/uploads/2018/04/walmart-square.jpg",
        "search_query": "https://www.walmart.com/search/?query=<search_query>"
    },
    {
        "name": "Best Buy",
        "logo_url": "https://corporate.bestbuy.com/wp-content/uploads/2017/03/best-buy-logo-652x368.jpg",
        "search_query": "https://www.bestbuy.com/site/searchpage.jsp?st=<search_query>"
    },
    {
        "name": "Macy's",
        "logo_url": "https://www.pinpng.com/pngs/m/72-728213_macys-logo-macys-gift-card-hd-png-download.png",
        "search_query": "https://www.macys.com/shop/featured/<search_query>"
    }
]

def populate_brands():
    # Populate the database with the brand data
    for brand in brands:
        logo = download_and_process_logo(brand["logo_url"])

        new_brand = Brand(
            name=brand["name"],
            logo=logo,
            search_query=brand["search_query"]
        )
        db.session.add(new_brand)
    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        populate_brands()
