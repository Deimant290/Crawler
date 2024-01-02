import requests
from lxml.etree import HTML
from io import BytesIO
from PIL import Image
import csv


def find_lowest_prices(html_content):
    # Parse the HTML content
    tree = HTML(html_content)

    # Extract product items
    product_items = tree.xpath("//div[contains(@class, 'product-item')]")

    if not product_items:
        return None

    # Initialize a list to store product information
    products = []

    # Iterate over product items
    for product in product_items:
        name = product.xpath("./input[@name='productName']/@value")[0]
        price = float(product.xpath("./input[@name='productPrice']/@value")[0])
        image_url = product.xpath(".//img/@src")[0]

        products.append({'Name': name, 'Price': price, 'ImageURL': image_url})

    # Sort products by price in ascending order
    sorted_products = sorted(products, key=lambda x: x['Price'])

    return sorted_products


def display_lowest_price_product(products):
    if not products:
        print("No products found.")
        return

    lowest_price_product = products[0]

    print("Product with Lowest Price:")
    print(f"Name: {lowest_price_product['Name']}, Price: {lowest_price_product['Price']}")

    # Display the image of the product with the lowest price
    image_url = lowest_price_product['ImageURL']
    response = requests.get(image_url)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.show()
    else:
        print("Failed to retrieve the image.")


def main():
    response = requests.get("https://www.gintarine.lt/search?q=veido+kremai").text
    products = find_lowest_prices(response)

    """Display information and image of the product with the lowest price"""

    display_lowest_price_product(products)

    # Write all sorted products to a CSV file

    csv_file_path = "sorted_products.csv"
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Name', 'Price', 'ImageURL']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for product in products:
            writer.writerow({'Name': product['Name'], 'Price': product['Price'], 'ImageURL': product['ImageURL']})


if __name__ == "__main__":
    main()