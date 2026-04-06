import requests
from bs4 import BeautifulSoup

url='https://mooc1.chaoxing.com/mooc2/work/list'
cookie_str=''#请从浏览器开发者工具中复制最新的 Cookie 字符串



Payload={
    'courseId':'240837788',
    'classId':'143329895',
    'cpi':'526508521',
    'ut':'s',
    't':'1775463360715',
    'stuenc':'7000cd30a24c1d809afe137424723ba6',
    'enc':'b824cbead06018a114e00e55342403f4'
}

User_Agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0'

#将cookie字符串转换为字典
def parse_cookie(cookie_str):
    cookies = {}
    for item in cookie_str.split('; '):
        if '=' in item:
            k, v = item.split('=', 1)
            cookies[k] = v
    return cookies

session=requests.session()

response=session.get(url,params=Payload,headers={'User-Agent':User_Agent},cookies=parse_cookie(cookie_str))

#响应文本好像是HTML
if(response.status_code==200):
    print("请求成功")
    soup = BeautifulSoup(response.text, 'html.parser')
    bottom_lists = soup.find_all('div', attrs={'class':'bottomList'})
    for bottom_list in bottom_lists:
        ul = bottom_list.find('ul')
        if ul:
            lis = ul.find_all('li')
            for li in lis:
                # 提取作业名字
                name_elem = li.find('p', class_='overHidden2 fl')
                name = name_elem.text.strip() if name_elem else '未知'
                
                # 提取状态
                status_elem = li.find('p', class_='status fl')
                status = status_elem.text.strip() if status_elem else '未知'
                
                # 提取截止时间
                time_elem = li.find('div', class_='time notOver')
                deadline = time_elem.text.strip() if time_elem else '未知'
                
                print(f"作业名字: {name}, 状态: {status}, 截止时间: {deadline}")
else:
    print(f"请求失败，状态码: {response.status_code}")