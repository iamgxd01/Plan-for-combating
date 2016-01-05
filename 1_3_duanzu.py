from bs4 import  BeautifulSoup
import requests
import time

headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
     'Cookie': 'BAIDUID=17DC21D2626EE4DD9D2E338D4C82E0D2:FG=1; BIDUPSID=17DC21D2626EE4DD9D2E338D4C82E0D2; PSTM=1448509781; BDUSS=JFcFUzUGUzQ3JyQWNaYUZSTnprTlpLTi1tWEg5ZEdmVzV1UVhMWnVWWn5OWUpXQVFBQUFBJCQAAAAAAAAAAAEAAAAAqRM7Nzg5v6rQxNK7v8wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH-oWlZ~qFpWNU; BDRCVFR[hyLLCYbpewf]=aeXf-1x8UdYcs; H_PS_PSSID=18451_18285_1458_18284_18535_12825_18731_18546_17000_17072_15133_11896_18089'

}

data = []

url ='http://bj.xiaozhu.com/search-duanzufang-p1-0/'
house_urls =[ 'http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i)) for i in range(1,2)]


def get_house_info(url, house_data = None):
    wb_data = requests.get(url )
    soup = BeautifulSoup(wb_data.text,'lxml')
    time.sleep(2)

    titles = soup.select('#page_list > ul > li > div.result_btm_con.lodgeunitname > div > a ')
    images = soup.select('#page_list > ul > li > a > img')
    addresses = soup.select(' div.result_btm_con.lodgeunitname > div > em')
    rents = soup.select(' span.result_price > i')
    imag_urls = soup.select('#page_list > ul > li > a ')
    print(titles)

    if house_data is None:
        for title, image, address, rent, imag_url in zip(titles, images, addresses, rents, imag_urls):
            address_str = address.get_text().split('-')
            imag_urls_str = imag_url.get('href')
            print( imag_urls_str)
            house_data = {
                'title': title.get_text(),
                'image': image.get('src'),
                'address': address_str[address_str.__len__()-1].strip() ,
                 'rent': rent.get_text()+'/晚',
                'lorder_name': get_landlord_info(imag_urls_str)
            }
            data.append(house_data)


def get_landlord_info(url,lorder_data=None):
    # url= "http://bj.xiaozhu.com/fangzi/495862701.html"
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    sexs = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > span')
    lorder_names = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')
    imgs = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > a > img')
    print(sexs)

    for sex, lorder_name, img in zip(sexs, lorder_names ,imgs):
        print(sex.get('class'))

        if sex.get('class')[0] == 'member_girl_ico' :
            sex = '女'
        else:
            sex = '男'
        lorder_data = {
            'sex':sex ,
            'lorder_name':lorder_name.get('title'),
            'img': img.get('src')
        }
    return lorder_data




for single_url in house_urls :
    get_house_info(single_url)


# for i in data:
#     print(i['title'], i['image'], i['address'], i['rent'],i['lorder_name'], sep='****')
# print('长度',data.__len__())










