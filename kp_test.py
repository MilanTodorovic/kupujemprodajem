import requests
from bs4 import BeautifulSoup as bs

base_link = "https://www.kupujemprodajem.com/"
link = "238405-1-lazar-lazic--svi-oglasi.htm"
next_page = base_link + link

f =  open("imac.txt", "r+", encoding="utf-16")
items_in_file = f.read().split("\n")
print("Items from reading: \n", items_in_file)

while True:
    print("Visiting: {}".format(next_page))
    try:
        response = requests.get(next_page)
    except Exception as e:
        break
    soup = bs(response.content, "html.parser")
    items = soup.find_all("section",{"class":"nameSec"})
    prices = soup.find_all("section", {"class":"priceSec"})
    for item, price in zip(items, prices[1:]):
        if "imac" in item.div.a.text.lower():
            s = item.div.a.text.strip()
            if s in items_in_file:
                if "-" in price.span.text:
                    items_in_file.remove(s)
                continue
            else:
                print("New item found: {} {}".format(s, price.span.text.strip()))
                items_in_file.append(s)
        else:
            continue
    pages = soup.find("ul", {"class":"pagesList clearfix"}).find_all("li")
    if bool(pages[-1].a):
        next_page = base_link + pages[-1].a["href"]
    else:
        break
content = "\n".join(items_in_file)
f.write(content)
f.close()
