from playwright.sync_api import sync_playwright
import pandas as pd
from time import sleep, time

def run(playwright,url):
     browser = playwright.chromium.launch(headless=False)
     context = browser.new_context()
     page = context.new_page()
     data:list = []
     try:
          for i in url:
               page.goto(i)
               page.wait_for_selector('.s-main-slot')
               price_selector = 'span.a-price-whole'
               price = page.text_content(price_selector)
               items = page.query_selector_all('.s-main-slot .s-result-item')
               for i in items:
                    data_asin = i.get_attribute('data-asin')
                    link = i.query_selector('div > div > span > div > div > div > div.puisg-col.puisg-col-4-of-12.puisg-col-8-of-16.puisg-col-12-of-20.puisg-col-12-of-24.puis-list-col-right > div > div > div.a-section.a-spacing-none.puis-padding-right-small.s-title-instructions-style > h2 > a')
                    link = "https://www.amazon.in"+link.get_attribute('href') if link else 'No link'
                    title = i.query_selector("h2 a span")
                    title = title.text_content() if title else 'No title'
                    price = i.query_selector("span.a-price-whole")
                    price = price.text_content() if price else 'No price'
                    original_price = i.query_selector(" a > div > span.a-price.a-text-price > span.a-offscreen")
                    original_price = original_price.text_content() if original_price else 'No ORIGINAL PRICE'
                    original_price = original_price.replace("₹","")
                    ratin = i.query_selector("span.a-size-base.s-underline-text")
                    ratin = ratin.text_content() if ratin else 'No Rating'
                    if data_asin:
                         res:dict = {
                              'data_asin':data_asin,
                              'title':title,
                              'price':price,
                              'original_price':original_price,
                              'rating':ratin,
                              'link':link
                         }
                         data.append(res)
                         print(res)
               sleep(5)
     except Exception as e:
          print(f"ERROR:{e}")
     finally:
          browser.close()
          save_to_csv(data=data)

def save_to_csv(data:list):
     frame:list = []
     for i in data:
          data_asin = i["data_asin"]
          title = i["title"]
          price = i["price"]
          original_price = i["original_price"]
          rating = i["rating"]
          link = i["link"]
          if data_asin:
               frame.append([data_asin,title,price,original_price,rating,link])
     df = pd.DataFrame(data, columns=["data_asin", "title", "price","original_price","rating","link"])
     from time import time
     df.to_csv(f"{int(time())}.csv", index=False)

def main():
     from lst import items
     with sync_playwright() as app:
          run(playwright=app,url=items)

if __name__=="__main__":
     a = time()
     main()
     b = time()
     res = int(b - a)
     print(f"Took {res} seconds..")
