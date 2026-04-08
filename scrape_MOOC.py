import requests
import json
import function

#创建一个session对象
session=requests.session()

#MOOC的csrfKey和cookie需要从浏览器中获取，以下是示例值，请替换为你自己的
csrf_key=''#后面会从cookie中获取这个值，这里只是示例
cookie_str=''


payload={
    'termId': '1476748448'
}#请求体，包含学期ID

session.headers.update({
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
})#更新session的headers，模拟浏览器访问

session.cookies.update(function.parse_cookie(cookie_str))#更新session的cookie

#从cookie中获取csrfKey，部分接口需要这个参数，如果没有可能会返回403错误
csrf_key = session.cookies.get('NTESSTUDYSI')
if not csrf_key:
    print("未找到 csrfKey,请检查 Cookie 是否正确")

url=f'https://www.icourse163.org/web/j/courseBean.getLastLearnedMocTermDto.rpc?csrfKey={csrf_key}'



response=session.post(url, data=payload,)

def main():
    if response.status_code == 200:
        data = json.loads(response.text)#检查响应是否是有效的JSON格式
        print(f"请求成功，状态码: {response.status_code}")
        
        if 'result' not in data or data['result'] is None:
            print("API 返回数据无效,result 字段为空。可能需要更新 Cookie 或 CSRF Key。")
            return
        
        chapters = data['result']['mocTermDto']['chapters']#获取章节列表

        for chapter in chapters:

            for hw in chapter['homeworks']:
                deadline_ms = hw['test']['deadline']
                deadline_str = function.ms_to_beijing_str(deadline_ms)#将截止时间转换为北京时间字符串
                if(deadline_ms > int(function.datetime.now().timestamp() * 1000)):#如果截止时间还未到                        s
                    print(f"{hw['name']}, 截止时间: {deadline_str}")
                    function.check_deadline_reminder(deadline_ms, hw['name'])#检查截止时间提醒

            for quiz in chapter['quizs']:
                deadline_ms = quiz['test']['deadline']
                deadline_str = function.ms_to_beijing_str(deadline_ms)#将截止时间转换为北京时间字符串
                if(deadline_ms > int(function.datetime.now().timestamp() * 1000)):#如果截止时间还未到
                    print(f"{quiz['test']['name']}, 截止时间: {deadline_str}")
                    function.check_deadline_reminder(deadline_ms, quiz['test']['name'])#检查截止时间提醒
                    print()#换行
    else:
        print(f"请求失败，状态码: {response.status_code}")




if __name__ == '__main__':
    main()