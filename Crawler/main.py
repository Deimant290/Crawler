import requests
from lxml.etree import HTML
from io import BytesIO
from PIL import Image
import csv
import pytest

TIMEOUT = 60  # Set the timeout value in seconds


def find_lowest_prices(html_content):
    try:
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
    except Exception as e:
        print(f"Error parsing HTML content: {e}")
        return None


def display_lowest_price_products(products):
    if not products:
        print("No products found.")
        return

    lowest_price = products[0]['Price']
    lowest_price_products = [product for product in products if product['Price'] == lowest_price]

    print("Products with Lowest Price:")
    for idx, product in enumerate(lowest_price_products):
        print(f"{idx + 1}. Name: {product['Name']}, Price: {product['Price']}")

        """ Display the image of the product with the lowest price """
        image_url = product['ImageURL']
        try:
            response = requests.get(image_url, timeout=TIMEOUT, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()

            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                image.show()
            else:
                print("Failed to retrieve the image.")
        except Exception as e:
            print(f"Error retrieving image: {e}")


@pytest.fixture
def sample_products():
    # Mock data for testing
    return [
        {'Name': 'Product A', 'Price': 10.0, 'ImageURL': 'https://example.com/imageA.jpg'},
        {'Name': 'Product B', 'Price': 9.0, 'ImageURL': 'https://example.com/imageB.jpg'},
        {'Name': 'Product C', 'Price': 10.0, 'ImageURL': 'https://example.com/imageC.jpg'},
    ]


def test_display_lowest_price_products(capsys, sample_products):
    display_lowest_price_products(sample_products)
    captured = capsys.readouterr()
    assert "Product with Lowest Price:" in captured.out
    assert "1. Name: Product A, Price: 10.0" in captured.out
    assert "2. Name: Product C, Price: 10.0" in captured.out


def main():
    try:
        response = requests.get(
            "https://www.gintarine.lt/search?q=veido+kremai", timeout=TIMEOUT, headers={'User-Agent': 'Mozilla/5.0'}
        ).text
        products = find_lowest_prices(response)

        """ Display information and image of the product with the lowest price """
        display_lowest_price_products(products)

        # Write all sorted products to a CSV file
        csv_file_path = "sorted_products.csv"
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['Name', 'Price', 'ImageURL']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for product in products:
                writer.writerow({'Name': product['Name'], 'Price': product['Price'], 'ImageURL': product['ImageURL']})
    except requests.RequestException as e:
        print(f"Error making the request: {e}")


if __name__ == "__main__":
    main()
