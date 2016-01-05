from bs4 import BeautifulSoup
import time
import requests
data = []

# 用于模拟手机登录使用
headers = {
       'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4'
}

# 使用 format(str(i)) for i in range(1, 4)获得多个网页
urls = ['http://m.58.com/bj/pbdn/pn{}/?reform=pcfront&PGTID=0d305a36-0000-140a-35f7-6753843b0650&ClickID=2&segment=true'.format(str(i)) for i in range(1, 4)]


# 获得单个商品的基本信息
def get_detail_info(url, detail_info=None):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    titles = soup.select('  div.left_tit > h1')
    page_views = soup.select('div.good_info > div > div:nth-of-type(2) > lable')
    release_times = soup.select(' div.date')
    prices = soup.select(' p.attr_price > span ')
    seller_types = soup.select('#personal > span.pcate')
    areas = soup.select('div.location > a')
    categorys = soup.select('#header > div.breadCrumb.f12 > span:nth-of-type(3) > a ')
    url_js = soup.select('head > script:nth-of-type(33)')
    print(page_views)
    print(url_js[0].get('src'))


    if detail_info is None:
        for title,  page_view,  release_time, price,  seller_type, area, in zip(titles, page_views,  release_times, prices, seller_types, areas, ):
            detail_info = {
                'title': title.get_text(),
                'page_view': page_view.get_text(),
                'release_time': release_time.get_text(strip=True),
                'price': price.get_text(),
                'seller_type': seller_type.get_text(),
                'area': area.get_text(),

            }

        return detail_info


# 获取商品的基本信息
# 在list页面获得每个商品的url
# 把url传递给detail_info()获得每个商品的基本信息
def get_list_info(url, data_list= None):

    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    url_details = soup.select(' body > li ')
    time.sleep(2)
    if data_list is None:
        for url_detail in url_details:
            url_str = url_detail.find('a',).get('href')
            url_type = url_str.find('http://m.zhuanzhuan.58.com/')
            # 网址有三种类型，http://m.zhuanzhuan.58.com/ 暂时不获取
            # 其他两种使用detail_info()方法获得数据
            if url_type == -1:
                data.append(get_detail_info(url_str))

# 获取多个网页的数据
for url in urls:
    get_list_info(url)

# 打印获取的数据
for i in data:
    print(i)

print(data.__len__())



