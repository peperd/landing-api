import requests
import json


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
              "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/97.0.4692.99 Safari/537.36"
}


def get_data_file(headers):
    """Collect data and return JSON file"""
    offset = 0
    result = []
    img_count = 0
    while True:
        url = f'https://s1.landingfolio.com/api/v1/inspiration?offset={offset}color=%23undefined'
        response = requests.get(url=url, headers=headers)
        data = response.json()
        for item in data:
            if 'description' in item:
                images = item.get("images")
                img_count += len(images)
                for img in images:
                    img.update({"url": f"https://landingfoliocom.imgix.net/{img.get('url')}"})
                result.append(
                    {
                        "title": item.get("title"),
                        "description": item.get("description"),
                        "url": item.get("url"),
                        "images": images
                    }
                )
            else:
                with open("result.json", 'a') as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)
                    return f'[INFO] Work finished. Image count is {img_count}/n{"=" * 20}'
        print(f"[+] Processed {offset}")
        offset += 1


def main():
    print(get_data_file(headers=headers))


if __name__ == '__main__':
    main()
