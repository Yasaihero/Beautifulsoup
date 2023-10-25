import requests

proxies = {
"http": "http://scraperapi:b9a89cbdfe8ae1ac866c58d7ed377d65@proxy-server.scraperapi.com:8001"
}
r = requests.get('http://httpbin.org/ip', proxies=proxies, verify=False)
print(r.text)

start_urls = ['http://httpbin.org/ip']
meta = {
"proxy": "http://scraperapi:b9a89cbdfe8ae1ac866c58d7ed377d65@proxy-server.scraperapi.com:8001"
}

def fetchAndSaveToFile(url, path):
    r = requests.get(url, proxies=proxies, headers = {"X-AUTH": "mysecret"})
    with open(path, "w", encoding="utf-8") as f:
        f.write(r.text)

url = "https://www.flipkart.com/search?q=Iphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

fetchAndSaveToFile(url, "data/times.html")
