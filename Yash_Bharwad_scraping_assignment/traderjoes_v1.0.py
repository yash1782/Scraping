import requests
import json
from scrapy.http import HtmlResponse
import re

BASE_URL = 'https://www.traderjoes.com/api/graphql'
CATEGORY_URL = 'https://www.traderjoes.com/home/products/category'

COOKIES = {
    '_gid': 'GA1.2.1215721217.1721595263',
    'AMCVS_B5B4708F5F4CE8D80A495ED9%40AdobeOrg': '1',
    's_cc': 'true',
    'affinity': '"40647b0bf93fb651"',
    's_sq': '%5B%5BB%5D%5D',
    's_ptc': '%5B%5BB%5D%5D',
    '_gat_UA-15671700-1': '1',
    'AMCV_B5B4708F5F4CE8D80A495ED9%40AdobeOrg': '-2121179033%7CMCIDTS%7C19927%7CMCMID%7C64868470262732932604594383754572402923%7CMCAAMLH-1722270717%7C12%7CMCAAMB-1722270717%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1721673117s%7CNONE%7CvVersion%7C5.3.0',
    'gpv_c51': 'https%3A%2F%2Fwww.traderjoes.com%2Fhome%2Fproducts%2Fcategory',
    's_nr30': '1721665917159-Repeat',
    's_vncm': '1722450599606%26vn%3D6',
    's_ivc': 'true',
    's_lv': '1721665917160',
    's_lv_s': 'Less%20than%201%20day',
    's_visit': '1',
    's_ips': '405',
    's_tp': '705',
    's_ppv': 'www.traderjoes.com%257Chome%257Cproducts%257Ccategory%2C57%2C57%2C405%2C1%2C1',
    's_dur': '1721665917163',
    's_tslv': '1721665917164',
    's_inv': '10876',
    's_pvs': '%5B%5BB%5D%5D',
    's_tps': '%5B%5BB%5D%5D',
    '_ga_2HMPBJHQ41': 'GS1.1.1721665916.6.1.1721665917.0.0.0',
    '_ga': 'GA1.1.145682013.1721322636',
}

HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.traderjoes.com',
    'priority': 'u=1, i',
    'referer': CATEGORY_URL,
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

def clean_html(raw_html):
    # Remove HTML tags
    clean_text = re.sub(r'<.*?>', '', raw_html)
    # Remove any remaining HTML entities
    clean_text = re.sub(r'&.*?;', '', clean_text)
    # Remove extra whitespace
    clean_text = ' '.join(clean_text.split())
    return clean_text

def get_json_response(url, headers, cookies, json_data):
    response = requests.post(url, cookies=cookies, headers=headers, json=json_data)
    return response.json() , response.status_code

def process_product_url(sku):
    json_data = {
        'operationName': 'SearchProduct',
        'variables': {
            'storeCode': 'TJ',
            'published': '1',
            'sku': sku,
        },
        'query': 'query SearchProduct($sku: String, $storeCode: String = "TJ", $published: String = "1") {\n  products(\n    filter: {sku: {eq: $sku}, store_code: {eq: $storeCode}, published: {eq: $published}}\n  ) {\n    items {\n      category_hierarchy {\n        id\n        url_key\n        description\n        name\n        position\n        level\n        created_at\n        updated_at\n        product_count\n        __typename\n      }\n      item_story_marketing\n      product_label\n      fun_tags\n      primary_image\n      primary_image_meta {\n        url\n        metadata\n        __typename\n      }\n      other_images\n      other_images_meta {\n        url\n        metadata\n        __typename\n      }\n      context_image\n      context_image_meta {\n        url\n        metadata\n        __typename\n      }\n      published\n      sku\n      url_key\n      name\n      item_description\n      item_title\n      item_characteristics\n      item_story_qil\n      use_and_demo\n      sales_size\n      sales_uom_code\n      sales_uom_description\n      country_of_origin\n      availability\n      new_product\n      promotion\n      price_range {\n        minimum_price {\n          final_price {\n            currency\n            value\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      retail_price\n      nutrition {\n        display_sequence\n        panel_id\n        panel_title\n        serving_size\n        calories_per_serving\n        servings_per_container\n        details {\n          display_seq\n          nutritional_item\n          amount\n          percent_dv\n          __typename\n        }\n        __typename\n      }\n      ingredients {\n        display_sequence\n        ingredient\n        __typename\n      }\n      allergens {\n        display_sequence\n        ingredient\n        __typename\n      }\n      created_at\n      first_published_date\n      last_published_date\n      updated_at\n      related_products {\n        sku\n        item_title\n        primary_image\n        primary_image_meta {\n          url\n          metadata\n          __typename\n        }\n        price_range {\n          minimum_price {\n            final_price {\n              currency\n              value\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        retail_price\n        sales_size\n        sales_uom_description\n        category_hierarchy {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    total_count\n    page_info {\n      current_page\n      page_size\n      total_pages\n      __typename\n    }\n    __typename\n  }\n}\n',
    }
    prod_data , status_code= get_json_response(BASE_URL, HEADERS, COOKIES, json_data)
    if status_code == 200:
        item = prod_data['data']['products']['items'][0]

        ret_data = {
            'product_id': item['url_key'],
            'title': item['item_title'],
            'image': "https://www.traderjoes.com" + item['primary_image'],
            'price': float(item['retail_price']),
            'description': str(item['item_story_marketing']),
            'sale_prices': [float(item['retail_price'])],
            'prices': [float(item['retail_price'])],
            'images': ["https://www.traderjoes.com" + img for img in [item['primary_image']] + item['other_images']],
            'url': f"https://www.traderjoes.com/home/products/pdp/{'-'.join(item['url_key'].split('-')[1:])}-{sku}",
            'brand': "Trader Joe's",
            'models': [{
                'variants': [{
                    'id': item['url_key'],
                    'image': "https://www.traderjoes.com" + item['primary_image'],
                    'price': float(item['retail_price']),
                    'uom': item['sales_uom_description']
                }]
            }]
        }
        
        with open('traderjones_output.jsonl', 'a') as f:
            f.write(json.dumps(ret_data) + '\n')
        print(f"DATA INSERTED SUCCESSFULLY FOR URL: {ret_data['url']}")

def scrape_data():
    page = 1
    while True:
        json_data = {
            'operationName': 'SearchProducts',
            'variables': {
                'storeCode': 'TJ',
                'availability': '1',
                'published': '1',
                'categoryId': 2,
                'currentPage': page,
                'pageSize': 15,
            },
            'query': 'query SearchProducts($categoryId: String, $currentPage: Int, $pageSize: Int, $storeCode: String = "TJ", $availability: String = "1", $published: String = "1") {\n  products(\n    filter: {store_code: {eq: $storeCode}, published: {eq: $published}, availability: {match: $availability}, category_id: {eq: $categoryId}}\n    currentPage: $currentPage\n    pageSize: $pageSize\n  ) {\n    items {\n      sku\n      item_title\n      category_hierarchy {\n        id\n        name\n        __typename\n      }\n      primary_image\n      primary_image_meta {\n        url\n        metadata\n        __typename\n      }\n      sales_size\n      sales_uom_description\n      price_range {\n        minimum_price {\n          final_price {\n            currency\n            value\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      retail_price\n      fun_tags\n      item_characteristics\n      __typename\n    }\n    total_count\n    pageInfo: page_info {\n      currentPage: current_page\n      totalPages: total_pages\n      __typename\n    }\n    aggregations {\n      attribute_code\n      label\n      count\n      options {\n        label\n        value\n        count\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',
        }

        cat_data , status_code = get_json_response(BASE_URL, HEADERS, COOKIES, json_data)
        if status_code == 200:
                prod_skus = cat_data['data']['products']['items']
                if not prod_skus:
                    break
                for sku in prod_skus:
                    try:
                        process_product_url(sku['sku'])
                    except Exception as e:
                        print(e)

                if len(prod_skus) < 15:
                    break
                page += 1

if __name__ == "__main__":
    scrape_data()