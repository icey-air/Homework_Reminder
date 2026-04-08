from datetime import datetime, timezone, timedelta

#将毫秒时间戳转换为北京时间字符串
def ms_to_beijing_str(ms:str):
    """毫秒时间戳 变成 北京时间字符串"""
    ms=int(ms)
    dt = datetime.fromtimestamp(ms / 1000.0, tz=timezone(timedelta(hours=8)))
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def check_deadline_reminder(deadline_ms:str,homework_name:str):
    """检查截止时间"""
    deadline_dt = datetime.fromtimestamp(int(deadline_ms) / 1000.0, tz=timezone(timedelta(hours=8)))
    current_time = datetime.now(timezone(timedelta(hours=8)))
    # 截止时间减去当前时间，得到距离截止还剩多少
    remaining_time = deadline_dt - current_time
    remaining_day = remaining_time.total_seconds() / (24 * 3600)

    if 0 <= remaining_day <= 5:
        days = remaining_time.days
        hours = remaining_time.seconds // 3600
        minutes = (remaining_time.seconds % 3600) // 60
        print(f"作业 {homework_name} 的截止时间是 {deadline_dt.strftime('%Y-%m-%d %H:%M:%S')}，距离截止还有 {days}天{hours}小时{minutes}分钟，请尽快完成！")
    else:
        return
        
#将cookie字符串转换为字典
def parse_cookie(cookie_str):
    cookies = {}
    for item in cookie_str.split('; '):
        if '=' in item:
            k, v = item.split('=', 1)
            cookies[k] = v
    return cookies
