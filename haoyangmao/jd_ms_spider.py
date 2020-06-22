# coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
import json
import datetime
import time
from bs4 import BeautifulSoup


chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')

JD_ms_top_map = {'京东秒杀': 'https://miaosha.jd.com', 
                 '每日特价': 'https://miaosha.jd.com/specialpricelist.html', 
                 '大牌闪购': 'https://miaosha.jd.com/pinpailist.html', 
                 '品类秒杀': 'https://miaosha.jd.com/brandlist.html', 
                 '服饰内衣': 'https://miaosha.jd.com/category.html?cate_id=15', 
                 '运动户外': 'https://miaosha.jd.com/category.html?cate_id = 13', 
                 '食品饮料': 'https://miaosha.jd.com/category.html?cate_id = 10', 
                 '电脑数码': 'https://miaosha.jd.com/category.html?cate_id = 3', 
                 '母婴': 'https://miaosha.jd.com/category.html?cate_id = 9', 
                 '潮流鞋靴': 'https://miaosha.jd.com/category.html?cate_id = 14', 
                 '美妆护肤': 'https://miaosha.jd.com/category.html?cate_id = 12', 
                 '家装建材': 'https://miaosha.jd.com/category.html?cate_id = 23',
                 '家居厨具': 'https://miaosha.jd.com/category.html?cate_id = 16', 
                 '手机通讯': 'https://miaosha.jd.com/category.html?cate_id = 4', 
                 '酒水': 'https://miaosha.jd.com/category.html?cate_id = 7', 
                 '家用电器': 'https://miaosha.jd.com/category.html?cate_id = 2', 
                 '医药保健': 'https://miaosha.jd.com/category.html?cate_id = 19', 
                 '个人护理': 'https://miaosha.jd.com/category.html?cate_id = 8', 
                 '家具': 'https://miaosha.jd.com/category.html?cate_id = 24', 
                 '钟表': 'https://miaosha.jd.com/category.html?cate_id = 17', 
                 '清洁用品': 'https://miaosha.jd.com/category.html?cate_id = 11', 
                 '箱包皮具': 'https://miaosha.jd.com/category.html?cate_id = 20', 
                 '汽车用品': 'https://miaosha.jd.com/category.html?cate_id = 21', 
                 '生鲜': 'https://miaosha.jd.com/category.html?cate_id = 25'}
                 
driver = webdriver.Chrome(chrome_options=chrome_options)

def Get_jd_ms_html(url, wait_time, lrange, step):

    driver.get(url)
    time.sleep(wait_time)
    for i in range(2, lrange):
        js = "var q=document.documentElement.scrollTop={}".format(
            i*step)
        driver.execute_script(js)
        time.sleep(0.5) 
    page = driver.page_source
    return page

def Brand_parser():

    json_list = []
    prefix = "https://miaosha.jd.com/brand.html?brand_id="
    url = JD_ms_top_map['品类秒杀']
    page = Get_jd_ms_html(url, 3, 10, 1000)
    soup = BeautifulSoup(page, 'lxml')
    items = soup.find_all(class_="brandsknow_item brandItem")

    for item in items:
        url = prefix+item['data-brid']
        page = Get_jd_ms_html(url, 3, 10, 100000)
        soup = BeautifulSoup(page, 'lxml')
        good_list = soup.find_all(class_="seckill_mod_goods")
        len1 = len(json_list)
        for good in good_list:
            map = {}  
            map['item_url'] = good.a['href']
            map['title'] = good.find(class_="seckill_mod_goods_title").string

            map['new_price'] = ''
            strs = good.find(class_="seckill_mod_goods_price_now").strings
            for string in strs:
                map['new_price'] += string

            map['old_price'] = ''
            strs = good.find(class_="seckill_mod_goods_price_pre").strings
            for string in strs:
                map['old_price'] += string

            map['state'] = good.find(class_="seckill_mod_goods_progress_txt").string
            json_list.append(map)
        len2 = len(json_list)

        print(item['data-brid'] + " finish!")
        print("goods_count: " + str(len2-len1))
        print("total_count: " + str(len2))
    
    return json_list
        

if __name__ == "__main__":

    result = Brand_parser()
    with open("jd_ms.json", 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False)
    
