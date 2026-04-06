import requests
import json
from datetime import datetime, timezone, timedelta

#创建一个session对象
session=requests.session()

#MOOC的csrfKey和cookie需要从浏览器中获取，以下是示例值，请替换为你自己的
csrf_key=''#后面会从cookie中获取这个值，这里只是示例
cookie_str=''


#将毫秒时间戳转换为北京时间字符串
def ms_to_beijing_str(ms:str):
    """毫秒时间戳 -> 北京时间字符串"""
    ms=int(ms)
    dt = datetime.fromtimestamp(ms / 1000.0, tz=timezone(timedelta(hours=8)))
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def now_beijing_time()->datetime:
    """获取当前北京时间的datetime对象"""
    return datetime.now(timezone(timedelta(hours=8)))

def check_deadline_reminder(deadline_ms:str,homework_name:str):
    """检查截止时间"""
    deadline_dt = datetime.fromtimestamp(int(deadline_ms) / 1000.0, tz=timezone(timedelta(hours=8)))
    current_time = now_beijing_time()
    # 截止时间减去当前时间，得到距离截止还剩多少
    remaining_time = deadline_dt - current_time
    remaining_day = remaining_time.total_seconds() / (24 * 3600)

    if 0 <= remaining_day <= 5:
        days = remaining_time.days
        hours = remaining_time.seconds // 3600
        minutes = (remaining_time.seconds % 3600) // 60
        print(f"作业 {homework_name} 的截止时间是 {deadline_dt.strftime('%Y-%m-%d %H:%M:%S')}，距离截止还有 {days}天{hours}小时{minutes}分钟，请尽快完成！")
    elif remaining_day < 0:
        overdue_days = abs(remaining_time.days)
        overdue_hours = abs(remaining_time.seconds) // 3600
        overdue_minutes = (abs(remaining_time.seconds) % 3600) // 60
       # print(f"作业 {homework_name} 的截止时间是 {deadline_dt.strftime('%Y-%m-%d %H:%M:%S')}，已超过截止时间 {overdue_days}天{overdue_hours}小时{overdue_minutes}分钟。")

#将cookie字符串转换为字典
def parse_cookie(cookie_str):
    cookies = {}
    for item in cookie_str.split('; '):
        if '=' in item:
            k, v = item.split('=', 1)
            cookies[k] = v
    return cookies

payload={
    'termId': '1476748448'
}#请求体，包含学期ID

session.headers.update({
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
})#更新session的headers，模拟浏览器访问

session.cookies.update(parse_cookie(cookie_str))#更新session的cookie

#从cookie中获取csrfKey，部分接口需要这个参数，如果没有可能会返回403错误
csrf_key = session.cookies.get('NTESSTUDYSI')
if not csrf_key:
    print("未找到 csrfKey,请检查 Cookie 是否正确")

url=f'https://www.icourse163.org/web/j/courseBean.getLastLearnedMocTermDto.rpc?csrfKey={csrf_key}'



response=session.post(url, data=payload,)

def main():
    if response.status_code == 200:
        try:
            data = json.loads(response.text)#检查响应是否是有效的JSON格式
            if 'result' not in data or data['result'] is None:
                print("API 返回数据无效，result 字段为空。可能需要更新 Cookie 或 CSRF Key。")
                return
            print(f"请求成功，状态码: {response.status_code}")
            chapters = data['result']['mocTermDto']['chapters']#获取章节列表
            for chapter in chapters:
                if 'homeworks' in chapter and chapter['homeworks']:#如果章节中有作业
                    for hw in chapter['homeworks']:
                        if 'test' in hw and hw['test']['deadline']:#如果作业中有截止时间
                            deadline_ms = hw['test']['deadline']
                            deadline_str = ms_to_beijing_str(deadline_ms)#将截止时间转换为北京时间字符串
                            if(deadline_ms > int(datetime.now().timestamp() * 1000)):#如果截止时间还未到                        
                                print(f"{hw['name']}, 截止时间: {deadline_str}")
                                check_deadline_reminder(deadline_ms, hw['name'])#检查截止时间提醒
                if 'quizs' in chapter and chapter['quizs']:#如果章节中有测验
                    for quiz in chapter['quizs']:
                        if 'test' in quiz and quiz['test']['deadline']:#如果测验中有截止时间
                            deadline_ms = quiz['test']['deadline']
                            deadline_str = ms_to_beijing_str(deadline_ms)#将截止时间转换为北京时间字符串
                            if(deadline_ms > int(datetime.now().timestamp() * 1000)):#如果截止时间还未到
                                print(f"{quiz['test']['name']}, 截止时间: {deadline_str}")
                                check_deadline_reminder(deadline_ms, quiz['test']['name'])#检查截止时间提醒
                                print()#换行
        except json.JSONDecodeError:
            print("响应不是有效的 JSON 格式,可能Cookie过期。")
            return
    else:
        print(f"请求失败，状态码: {response.status_code}")
        if response.status_code == 403:
            print("可能需要更新 Cookie 和 CSRF Key。请从浏览器开发者工具中复制最新的值。")
        elif response.status_code == 401:
            print("认证失败，请检查登录状态和 Cookie。")
        else:
            print("请检查网络连接、参数设置或网站是否更新。")



if __name__ == '__main__':
    main()