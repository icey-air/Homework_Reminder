import requests
import json
import function

cookies_str=''

payload={
    'type': '30',
    'p':'1',
    'psize':'8',
    'courseType':'1'
}

User_Agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'

session=requests.session()#创建session对象

session.headers.update({
       'User-Agent': User_Agent
})#更新session的headers，模拟浏览器访问
session.cookies.update(function.parse_cookie(cookies_str))#更新session的cookie
csrf_key = session.cookies.get('NTESSTUDYSI')#更新session的cookie后从cookie中获取csrfKey，部分接口需要这个参数，如果没有可能会返回403错误
url=f'https://www.icourse163.org/web/j/learnerCourseRpcBean.getMyLearnedCoursePanelList.rpc?csrfKey={csrf_key}'

response=session.post(url,data=payload)

if response.status_code == 200:
    print("请求成功")
    data=json.loads(response.text)

    result=data['result']['result']
    for course in result:
        print(course['name'])
        print(function.ms_to_beijing_str(course['termPanel']['endTime']))

    