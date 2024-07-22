import requests
import json
from scrapy.http import HtmlResponse
from collections import defaultdict

BASE_URL = 'https://foreignfortune.com'
COOKIES = {
    'secure_customer_sig': '',
    'localization': 'IN',
    '_tracking_consent': '%7B%22con%22%3A%7B%22CMP%22%3A%7B%22a%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22%22%2C%22s%22%3A%22%22%7D%7D%2C%22v%22%3A%222.1%22%2C%22region%22%3A%22INGJ%22%2C%22reg%22%3A%22%22%7D',
    '_cmp_a': '%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22sale_of_data_region%22%3Afalse%7D',
    '_shopify_y': '14247d20-a5dd-4cb6-bdca-118126d1310a',
    '_orig_referrer': '',
    '_landing_page': '%2F',
    'receive-cookie-deprecation': '1',
    '_shopify_sa_p': '',
    '_ga': 'GA1.2.1906576078.1721322457',
    '_gid': 'GA1.2.983093818.1721322457',
    '_fbp': 'fb.1.1721322457751.945443452797898178',
    '_shopify_country': 'India',
    '_gat': '1',
    'keep_alive': 'ec443e8f-125b-4cd6-82ad-710e00e74a63',
    '_shopify_s': '633e6211-a10f-42b8-9e9c-ff966eb8a6c6',
    '_shopify_sa_t': '2024-07-18T17%3A23%3A15.786Z',
    '_ga_CGNL2FX8HR': 'GS1.2.1721322457.1.1.1721323396.0.0.0',
    '__kla_id': 'eyJjaWQiOiJORGcyTkdabE5USXRNekUyWkMwME56a3lMVGt4TW1ZdFlXTTVaall5T1RrMU1tTTMiLCIkcmVmZXJyZXIiOnsidHMiOjE3MjEzMjI0NjAsInZhbHVlIjoiIiwiZmlyc3RfcGFnZSI6Imh0dHBzOi8vZm9yZWlnbmZvcnR1bmUuY29tLyJ9LCIkbGFzdF9yZWZlcnJlciI6eyJ0cyI6MTcyMTMyMzM5NiwidmFsdWUiOiIiLCJmaXJzdF9wYWdlIjoiaHR0cHM6Ly9mb3JlaWduZm9ydHVuZS5jb20vIn19',
}

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-cookie-deprecation': 'label_only_3',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1', 
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

def get_html_response(url):
    response = requests.get(url, cookies=COOKIES, headers=HEADERS)
    return HtmlResponse(url=url, body=response.text, encoding='utf-8')

def extract_product_data(jd, vjd):
    return {
        'product_id': jd['handle'],
        'title': jd['title'],
        'image': f"https://foreignfortune.com{jd['featured_image']}",
        'price': float(jd['price']) / 100,
        'description': jd['description'].replace('<br>', '').strip(),
        'sale_prices': [float(jd['price']) / 100],
        'prices': [float(jd['price']) / 100],
        # 'sale_prices': list({pr['price']['amount'] for pr in vjd['initData']['productVariants']}),
        # 'prices': list({pr['price']['amount'] for pr in vjd['initData']['productVariants']}),
        'images': [img.replace('//', 'https://') for img in jd['images']],
        'url': f"https://foreignfortune.com/products/{jd['handle']}",
        'brand': jd['vendor']
    }

def process_product_url(prod_url):
    prod_response = requests.get(prod_url, cookies=COOKIES, headers=HEADERS)
    prod_selector = HtmlResponse(url=prod_url, body=prod_response.text, encoding='utf-8')

    master_json = prod_selector.xpath("//script[@id='ProductJson-product-template']/text()").extract_first()
    variant_json = prod_selector.xpath("//script[@id='web-pixels-manager-setup']/text()").extract_first().split('initData')[1].split(']},}')[0]
    vjs = '{"initData"' + variant_json + ']}' + '}'

    try:
        vjd = json.loads(vjs)
    except json.decoder.JSONDecodeError as e:
        print(f"JSONDecodeError at {e.pos}: {vjs[max(0, e.pos - 40):min(len(vjs), e.pos + 40)]}")
        return

    jd = json.loads(master_json)
    ret_data = extract_product_data(jd, vjd)
    status = any("title" in ch.lower() for ch in jd['options'])
    if not status:
        variants = []
        for mlt_dt in jd['variants']:
            for img_mth in vjd['initData']['productVariants']:
                if int(mlt_dt['id']) == int(img_mth['id']):
                    sub_val = {
                        'id': mlt_dt['id'],
                        'price': float(mlt_dt['price'] / 100),
                        'image': img_mth['image']['src'].replace('//', 'http://')
                    }
                    for idx, opt in enumerate(jd['options']):
                        sub_val[opt] = mlt_dt['options'][idx]
                    variants.append(sub_val)
                    break

        grouped_data = defaultdict(lambda: defaultdict(list))
        for variant in variants:
            third_key = list(variant.keys())[2]
            third_value = variant.pop(third_key)
            grouped_data[third_key][third_value].append(variant)

        ret_data['models'] = [
            {third_key: third_value, 'variants': vars}
            for third_key, values in grouped_data.items()
            for third_value, vars in values.items()
        ]
    else:
        ret_data['models'] = []

    with open('foreignfortunecom_output.jsonl', 'a') as f:
        f.write(json.dumps(ret_data) + '\n')
    print(f"DATA INSERTED SUCCESSFULLY FOR URL: {prod_url}")

def scrape_data():
    response = get_html_response(BASE_URL)
    category_urls = response.xpath("//ul[@class='site-nav list--inline site-nav--centered']//a/@href").extract()

    for url in category_urls:
        page = 1
        while True:
            cat_url = f"{BASE_URL}{url}?page={page}"
            cat_response = get_html_response(cat_url)
            prod_urls = cat_response.xpath("//div[@class='grid grid--uniform grid--view-items']//a/@href").extract()
            if not prod_urls:
                break
            for prod_url in prod_urls:
                process_product_url(f"{BASE_URL}{prod_url}")
            if len(prod_urls) < 8:
                break
            page += 1

if __name__ == "__main__":
    scrape_data()