from selenium import webdriver
import time
import json
import datetime, time
from bs4 import BeautifulSoup


JD_quan_url = 'https://a.jd.com/?cateId='
JD_quan_ids = ['135','134','143','136','137','138','139','140','142' \
            ,'146','149','150','152','153','154','159']



def Get_jd_quan_html(url, driver):
        
    driver.get(url)
    for i in range(2, 10):
        js = "var q=document.documentElement.scrollTop={}".format(
            i*1000)
        time.sleep(1)
        driver.execute_script(js)
    page = driver.page_source
   
    return page

def Parser_jd_quan_2_json(html, id):

    json_list = []
    soup = BeautifulSoup(html, "lxml")
    start = soup.find(attrs={"id":"quanlist"})
    count = 0
    for item in start.find_all('div', recursive=False):

        map = {}

        map['data-key'] = item['data-key']
        img = item.find(class_="err-product")
        if 'src' in img.attrs:
            map['img_src'] = img["src"]
        else:
            map['img_src'] = img["data-lazy-img"]
        
        coupon = ""
        for string in item.find(class_="q-price").strings:
            coupon += string
        map['coupon'] = coupon

        range = []
        for string in item.find(class_="q-range").strings:
            range.append(string)
        map['range'] = range
        
        progress = []
        for string in item.find(class_="q-progress").strings:
            progress.append(string)
        map['progress'] = progress
        
        map['item-url'] = 'https:' + item.find(class_="q-opbtns").a['data-url']

        map['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %X")

        map['category_id'] = id

        json_list.append(map)

        count += 1
        # print(count)

    return json_list

def Run_jd_quan():

    driver = webdriver.Chrome()
    result = []
    for id in JD_quan_ids:
        url = JD_quan_url + id
        page = Get_jd_quan_html(url, driver)
        print("request " + id + " success!")
        result.extend(Parser_jd_quan_2_json(page, id))
        print("parser " + id + " success!")

    with open("jd_quan.json", 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False)


if __name__ == "__main__":

    Run_jd_quan()
