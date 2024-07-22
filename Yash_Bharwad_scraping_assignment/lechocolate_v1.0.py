import requests
import json
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = 'https://www.lechocolat-alainducasse.com/uk/'
COOKIES = {
    'PHPSESSID': 'amei8jc6t32pu04tihfgppg4v0',
    '_pin_unauth': 'dWlkPVl6VXdNbUkxWlRVdE1UazNZeTAwTnpSaExXSmtOV1F0WWpCbU9UTTBNMkl3WlRJMw',
    '__zlcmid': '1MomsU4TZWhqGlO',
    'beyable-TrackingId': '7f552857-d50a-4158-918e-e3bf6ea49c2b',
    'beyable-MustBeDisplayed': 'true',
    'PrestaShop-24e2bc2623ae1acf5fc87570f4da228f': 'def502004cb5cbb4368eeec41264f0220e5e13deeef47a7bbd4dc6fbe9a9ee25adddf426fda538ead78d0d7dd67a5a838ed21a3f9d3be34863cdff2a57d4c96ad7129c68698a9f6ae7a48fb70dcd03cc0960030c086b32ca95a07192c40905984ec02b747d79f2d68b78b90723221741780c13888949ba6924ff91ad35e84df85068ee8b7686ab16b9baf2881a32863b94c94d6d10ff5053ff8fc875d4f10b7efac7a55f355b49b0090eb106be23a77c9f645750185a54f5bb4ad9a120dd463ba02a5d5039401a5f8d122cd023115547435f21d73c4cdd29e456a5649a3f7a12d9b37029c0d335bc209f763b9b7988f3da7764eaf31b14b8f6f233a828e72322b97ed8b245269a5d90c898ce2c4e5cf9ed8be09559de65ea7a8acc49ad8c6ce2424da5bde5623f0ac7cdf3d44913dea63f3617f8e34169a8a2883ea788f2edc0c60d0c62cd41b024ca53bad4d582b1117d5b14db',
    '_hjSessionUser_2339094': 'eyJpZCI6IjQ5NzJjMmJhLTBlNDMtNTZhZS1iODg3LTI0ZDQ0ZTM4NDgyMCIsImNyZWF0ZWQiOjE3MjEzMjI2NDEyMjMsImV4aXN0aW5nIjp0cnVlfQ==',
    '_gid': 'GA1.2.1682996725.1721494181',
    '_gcl_au': '1.1.588436503.1721494181',
    'axeptio_authorized_vendors': '%2Cgoogle_analytics%2Chotjar%2Cbeyable%2Cfacebook_pixel%2Cbing%2Cgoogle_ads%2Cpinterest%2Ccriteo%2CBing%2CGoogle_Ads%2CCriteo%2C',
    'axeptio_all_vendors': '%2Cgoogle_analytics%2Chotjar%2Cbeyable%2Cfacebook_pixel%2Cbing%2Cgoogle_ads%2Cpinterest%2Ccriteo%2CBing%2CGoogle_Ads%2CCriteo%2C',
    'axeptio_cookies': '{%22$$token%22:%22uiyrs5jj3gif2zf4slu6b8%22%2C%22$$date%22:%222024-07-20T16:49:41.255Z%22%2C%22$$cookiesVersion%22:{%22name%22:%22pp%20choco-fr_Cp%22%2C%22identifier%22:%2262c827885e01ed76613bca1d%22}%2C%22google_analytics%22:true%2C%22hotjar%22:true%2C%22beyable%22:true%2C%22facebook_pixel%22:true%2C%22bing%22:true%2C%22google_ads%22:true%2C%22pinterest%22:true%2C%22criteo%22:true%2C%22$$googleConsentMode%22:{%22version%22:2%2C%22analytics_storage%22:%22granted%22%2C%22ad_storage%22:%22granted%22%2C%22ad_user_data%22:%22granted%22%2C%22ad_personalization%22:%22granted%22}%2C%22Bing%22:true%2C%22Google_Ads%22:true%2C%22Criteo%22:true%2C%22$$completed%22:true}',
    '_fbp': 'fb.1.1721494208974.696194058521930553',
    '_hjSession_2339094': 'eyJpZCI6IjM1OTJkZGQyLTA0ZmYtNDNmMy1iYjY4LTM2YzgzNDJhODg0ZCIsImMiOjE3MjE1NzE2Njc0NzAsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
    'aaaaaaaaa78627c24380a4a17909617b94cc4b3cf_loc': '21.19594$bey$72.83023',
    'beyable-cart': '0',
    'beyable-cartd': '',
    'aaaaaaaaa78627c24380a4a17909617b94cc4b3cf_cs': '',
    'PrestaShop-50f128867babcd0e7b227041d6c1fd04': 'def50200c9dbadf40e737f5a00f3ba1f532410bea45c5c11aa41dce53e8b9df87097a5c2a86bce6ca02013d1a58ac993fea602173a58e89a5a463f1c035481838fc0be2cc762da7f5f6f06b945c7031367eae32e7d497d88e55dbb74f5161e2255122ea18d1d829114c3c5885dbc0d9cd11de7ca4106a233b8e140a1e5f2b0de996687b55c2decfb7a3ac0c7fad377bb84a37d4d028e0b151307251e49ffe512694f622bd67d7adb6cce92eb26cfe063b25155d20ff27b9037bfacb5bb812626ee54f99936fb554ecaf2ea3df44bb98ec761c4a340fe462063c5446334556614626c8e61d50ef47d57c808ef4d35e58cefda4a59b186d9d1be04104047f645754da5a9f706454c7df28eff00447cd614d3327c6fab3acc4feb259e819ab769d9aba49065e350a1e0932493f4e905b775afe55ae6ca5b0b757543e59325468d447c9b5a8a2a09fa48071dffb7e01f65d8c1440924561e3ce6b9e3bbdb56b808da91487281c2da81529467b2cd70378a8940459d4fb990b8489c6e73e4511bdb464517f94e8fa1f8e13730a86146c9e0596446c53799c54b6247de295817f1d6d22f7ad55a8cc61eebee0c58d46c6917ae1fe40eafb75556e333de61b3235541b6',
    'PrestaShop-997dcb94ebfc976352b86afa477dea7e': 'def50200fb8e1ccd36ae835313ab1baf33d93d58356b338aa3e579689fd93c1197042bfcbb60668ce021801496f5be63a953b406306be04d8e809e1991d1aa9a3f6b178b9832692180c6bfbbe4adcfb00fa45a7134a7c9b385572e5be81434da23350eb93ba7e89cf3779e3510ca12281d08af3479ee77abae4a6f26029a7d8f2dded298ad26bd2d5489309bee29eb3b2dd47b52a083cab2df24a57cfcaef352e11891c1aa9e180d89329c8a185e9d5000cdc9843149c15d9503386a4c6a423f6c444fc9ad550d5abbeaf9ec707e30140c191b2c01338353516f104442b968098032e108b3e7df5f4c2b1a7256f2eebd72e2c7152fb0fa1ce5a70bc0a572be91ae2f0a0b274c84095facd099d052db7ed45876d9e67243c6ddb21932414e1374e9d72141b5d03c3df1042597453dd44ce318d952c83764c4f2fab1b2b4cae1bfeb8d60755a856078eb92ed333d84ac6a7feca6ae3dcc635d577a89438aef67622335e8c9cd8d12159b31eb09175ff96636366b4ccb2127258c2c21cca5747cbee3b2dc19cce4a28a9831f05436f36d46e787db0a56cf4068a565af31f202a2eff2be63907d00ce7b19d35077786bd24ca89e72b04d2ffe04231a7acb6c67128d1df175a818c6322d9f201c8648857041bc1b8e86c95894419278392544a6',
    '_ga_JETBMHQH4E': 'GS1.1.1721571667.2.1.1721572275.60.0.0',
    '_ga': 'GA1.2.637430888.1721494172',
    '_uetsid': 'db03482046b711efb55a3139d2ab8e94',
    '_uetvid': 'a6099400452811ef81b3ddab3b82b6aa',
    'cto_bundle': 'EjF8ml9sb1QyMlBuMUtBZW1OSDFjOEJBd1k4QThYN0wyRmF2T3I3Q2JrSzYxMXlMJTJGekNYS3olMkJaeW5rNlYzZ2lTdGtkRFlFd3R1VUZoc3pRaiUyQkxmOFA4MU9sQkRFVkxRaXd5RklaUFNJU0tNTmgzWmZLYkJHR29YaVdlTSUyRmN0SlRDcVN1Uko3TVZmd3VHdmRxT1NOQlJMWGlZaVhkNU0xNWt1VFduWmROdnJsZXRGOCUzRA',
    'aaaaaaaaa78627c24380a4a17909617b94cc4b3cf': '5f61bb5b-0e49-4df4-a3f3-0c4cb282e707.1721572276876.1721571669529.$bey$https%3a%2f%2fwww.lechocolat-alainducasse.com%3a443%2fuk%2f$bey$17',
    'aaaaaaaaa78627c24380a4a17909617b94cc4b3cf_v': '3.31.958488.H:3:6$bey$C:9:10$bey$FP:4:14$bey$G:1:1....$:$.C$b$1721571669529',
}

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

def get_html_response(url):
    response = requests.get(url, cookies=COOKIES, headers=HEADERS)
    return HtmlResponse(url=url, body=response.text, encoding='utf-8')

def extract_product_data(prod_selector):
    price = float(prod_selector.xpath("//meta[@property='product:price:amount']/@content").extract_first())
    ret_data = {
        'product_id': prod_selector.xpath("//meta[@property='og:url']/@content").extract_first().split('/uk/')[1].strip(),
        'title': prod_selector.xpath("//meta[@property='og:title']/@content").extract_first(),
        'image': prod_selector.xpath("//meta[@property='og:image']/@content").extract_first(),
        'price': price,
        'description': prod_selector.xpath("//meta[@property='og:description']/@content").extract_first(),
        'sale_prices': [price],
        'prices': [price],
        'images': prod_selector.xpath("//section[@class='productImages images-container']//a/@href").extract(),
        'url': prod_selector.xpath("//meta[@property='og:url']/@content").extract_first(),
        'brand': "Le Chocolat Alain Ducasse"
    }
    return ret_data

def process_product_url(prod_url):
    prod_response = requests.get(prod_url, cookies=COOKIES, headers=HEADERS)
    prod_selector = HtmlResponse(url=prod_url, body=prod_response.text, encoding='utf-8')
    ret_data = extract_product_data(prod_selector)

    if prod_selector.xpath("//ul[@class='linkedProducts__list']/li"):
        ret_data['model'] = process_linked_products(prod_selector, ret_data)
    elif prod_selector.xpath("//div[@class='product-variants-item']//li[@class='input-container']"):
        ret_data['model'] = process_variants(prod_selector, ret_data)
    else:
        ret_data['models'] = []

    with open('letchodcolate_output.jsonl', 'a') as f:
        f.write(json.dumps(ret_data) + '\n')
    print(f"DATA INSERTED SUCCESSFULLY FOR URL: {prod_url}")

def process_linked_products(prod_selector, ret_data):
    if prod_selector.xpath("//span[@class='linkedProducts__bullet --active --simple']/@title"):
        size_xpath = "//span[@class='linkedProducts__bullet --active --simple']/@title"

        variants = [{"id": ret_data['product_id'], "image": ret_data['image'], "price": ret_data['price'], "size": prod_selector.xpath(size_xpath).extract_first()}]
        var_response = get_html_response(prod_selector.xpath("//ul[@class='linkedProducts__list']//a/@href").extract_first())
        variants.append({
            "id": var_response.xpath("//meta[@property='og:url']/@content").extract_first().split('/uk/')[1].strip(),
            "image": var_response.xpath("//meta[@property='og:image']/@content").extract_first(),
            "price": float(var_response.xpath("//meta[@property='product:price:amount']/@content").extract_first()),
            "size": var_response.xpath(size_xpath).extract_first()
        })
    else:
        size_xpath = "//span[@class='linkedProducts__bullet --active']/@title"
    
        variants = [{"id": ret_data['product_id'], "image": ret_data['image'], "price": ret_data['price'], "type": prod_selector.xpath(size_xpath).extract_first()}]
        var_response = get_html_response(prod_selector.xpath("//ul[@class='linkedProducts__list']//a/@href").extract_first())
        variants.append({
            "id": var_response.xpath("//meta[@property='og:url']/@content").extract_first().split('/uk/')[1].strip(),
            "image": var_response.xpath("//meta[@property='og:image']/@content").extract_first(),
            "price": float(var_response.xpath("//meta[@property='product:price:amount']/@content").extract_first()),
            "type": var_response.xpath(size_xpath).extract_first()
        })
    return [{"variants": variants}]

def process_variants(prod_selector, ret_data):
    variants = [{"id": ret_data['product_id'], "image": ret_data['image'], "price": ret_data['price'], "size": prod_selector.xpath("//div[@class='product-variants-item']//li[.//input[@checked='checked']]//input/@title").extract_first()}]
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(ret_data['url'])
        driver.maximize_window()
        driver.implicitly_wait(5)

        a_tag = driver.find_element(By.XPATH, "//div[@class='product-variants-item']//li[not(.//input[@checked='checked'])]")
        a_tag.click()
        driver.implicitly_wait(5)

        response = driver.page_source
        variant_resp = HtmlResponse(url=driver.current_url, body=response, encoding='utf-8')
        variants.append({
            "id": variant_resp.xpath("//meta[@property='og:url']/@content").extract_first().split('/uk/')[1].strip(),
            "image": variant_resp.xpath("//meta[@property='og:image']/@content").extract_first(),
            "price": float(variant_resp.xpath("//button[@class='productActions__addToCart button add-to-cart add']//text()").extract_first().split('£')[1].strip()),
            "size": variant_resp.xpath("//div[@class='product-variants-item']//li[not(.//input[@checked='checked'])]//input/@title").extract_first()
        })
    finally:
        driver.quit()
    
    return [{"variants": variants}]

def scrape_data():
    response = get_html_response(BASE_URL)
    category_urls = response.xpath("//li[@class='siteMenuItem --group']//li/a/@href").extract()

    for url in category_urls:
        cat_response = get_html_response(url)
        prod_urls = cat_response.xpath("//section[@class='productMiniature__data']/a/@href").extract()
        for prod_url in prod_urls:
            process_product_url(prod_url)

if __name__ == "__main__":
    scrape_data()