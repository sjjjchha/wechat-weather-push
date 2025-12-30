#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import datetime
import random
import os

class WeChatService:
    """微信推送服务"""
    
    def __init__(self):
        self.app_id = os.environ.get('WECHAT_APP_ID', '')
        self.app_secret = os.environ.get('WECHAT_APP_SECRET', '')
        self.template_id = os.environ.get('WECHAT_TEMPLATE_ID', '')
        self.user_id = os.environ.get('WECHAT_USER_ID', '')
        self.love_date = os.environ.get('LOVE_DATE', '2024-01-01')
    
    def get_access_token(self):
        """获取微信access_token"""
        url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}'
        
        # 重试3次
        for i in range(3):
            try:
                response = requests.get(url, timeout=30)
                result = response.json()
                if 'access_token' in result:
                    return result['access_token']
                else:
                    print(f"❌ 获取access_token失败: {result}")
                    return None
            except Exception as e:
                print(f"❌ 第{i+1}次尝试失败: {e}")
                if i < 2:
                    print("⚙️ 等待5秒后重试...")
                    import time
                    time.sleep(5)
        return None
    
    def get_love_days(self):
        """计算恋爱天数"""
        try:
            start_date = datetime.datetime.strptime(self.love_date, '%Y-%m-%d')
            today = datetime.datetime.now()
            delta = today - start_date
            return delta.days + 1
        except Exception as e:
            print(f"❌ 计算恋爱天数异常: {e}")
            return 0
    
    def get_next_holiday(self):
        """计算下一个休息日或节假日(已修复跨年bug)"""
        today = datetime.datetime.now()
        current_weekday = today.weekday()  # 0=星期一, 6=星期日
        
        # 2025年法定节假日(格式: (month, day, '名称'))
        holidays_2025 = [
            (1, 1, '元旦'),
            (1, 28, '除夕'),
            (1, 29, '春节'),
            (1, 30, '春节'),
            (1, 31, '春节'),
            (2, 1, '春节'),
            (2, 2, '春节'),
            (2, 3, '春节'),
            (4, 4, '清明节'),
            (4, 5, '清明节'),
            (4, 6, '清明节'),
            (5, 1, '劳动节'),
            (5, 2, '劳动节'),
            (5, 3, '劳动节'),
            (5, 4, '劳动节'),
            (5, 5, '劳动节'),
            (5, 31, '端午节'),
            (6, 1, '端午节'),
            (6, 2, '端午节'),
            (10, 1, '国庆节'),
            (10, 2, '国庆节'),
            (10, 3, '国庆节'),
            (10, 4, '国庆节'),
            (10, 5, '国庆节'),
            (10, 6, '国庆节'),
            (10, 7, '国庆节'),
            (10, 8, '国庆节'),
        ]
        
        # 计算下个周六(周末)
        if current_weekday < 5:  # 周一到周五
            days_until_saturday = 5 - current_weekday
            weekend_text = f"还有3天就周六啦" if days_until_saturday == 3 else f"还有{days_until_saturday}天就周六啦"
        elif current_weekday == 5:  # 周六
            weekend_text = "今天就是周六啦，休息日快乐！"
        else:  # 周日
            weekend_text = "今天是周日，但明天要上班啦~"
        
        # 查找最近的节假日
        closest_holiday = None
        min_days = 999
        
        for month, day, name in holidays_2025:
            # 先尝试今年的日期
            holiday_date = datetime.datetime(today.year, month, day)
            
            # 如果今年的日期已过,尝试明年的日期
            if holiday_date <= today:
                holiday_date = datetime.datetime(today.year + 1, month, day)
            
            days_diff = (holiday_date - today).days
            if days_diff < min_days and days_diff >= 0:
                min_days = days_diff
                closest_holiday = (days_diff, name)
        
        # 如果有节假日且比周六更近,优先显示节假日
        if closest_holiday:
            # 计算到下一个周六的天数
            if current_weekday < 5:  # 周一到周五
                days_until_saturday = 5 - current_weekday
            elif current_weekday == 5:  # 已经是周六
                days_until_saturday = 0
            else:  # 周日
                days_until_saturday = 6
            
            print(f"📅 调试: 节假日={closest_holiday}, 周六还有{days_until_saturday}天, 当前周{current_weekday}")
            
            if closest_holiday[0] < days_until_saturday or (closest_holiday[0] == days_until_saturday and days_until_saturday > 0):
                return f"还有{closest_holiday[0]}天就是{closest_holiday[1]}啦！"
        
        # 返回周末提醒
        return weekend_text
    
    def get_encouragement(self):
        """获取随机鼓励语"""
        encouragements = [
            "再坚持坚持吧，宝贝！",
            "加油哦，快到休息日啦！",
            "要好好的哦，快放假啦！",
            "要快乐哦，马上就能休息啦！",
            "坚持一下，周末马上就到啦！",
        ]
        return random.choice(encouragements)
    
    def get_sweet_words(self):
        """获取随机情话"""
        words = [
            "我喜欢你,认真且怂,从一而终。",
            "想和你在一起,不分秋冬,不顾冷暖,想给你最好的爱情。",
            "遇见你之后,我就没想过要和别人在一起了。",
            "我想和你一房二人三餐四季,四海三山二心一生。",
            "你是我今生渡不过的劫,多看一眼就心软,拥抱一下就沦陷。",
            "世界上最美好的三个字不是我爱你,而是在一起。",
            "我希望,以后你能用我的名字拒绝所有人。",
            "最美不过夕阳红,温馨又从容,最浪漫不过和你一起慢慢变老。",
        ]
        return random.choice(words)
    
    def send_template_message(self, city_name, weather_data):
        """发送模板消息"""
        access_token = self.get_access_token()
        if not access_token:
            return False
            
        # 获取当前时间
        now = datetime.datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        week = week_list[now.weekday()]
            
        # 获取节假日提醒和鼓励语
        holiday_reminder = self.get_next_holiday()
        encouragement = self.get_encouragement()
        sweet_words = self.get_sweet_words()
        
        print(f"💬 节假日提醒: {holiday_reminder}")
        print(f"💬 鼓励语: {encouragement}")
        print(f"💕 情话: {sweet_words}")
        print(f"💡 温馨提示: {weather_data.get('tips', '空')}")
            
        # 构造消息数据
        data = {
            "touser": self.user_id,
            "template_id": self.template_id,
            "data": {
                "date": {"value": f"{date_str} {week}", "color": "#FF1493"},
                "city": {"value": f"📍{city_name}", "color": "#00CED1"},
                "weather": {"value": f"🌤️{weather_data.get('weather', '未知')}", "color": "#FF6347"},
                "temperature": {"value": f"🌡️{weather_data.get('min_temp', '--')}~{weather_data.get('max_temp', '--')}", "color": "#0099FF"},
                "love_days": {"value": str(self.get_love_days()), "color": "#FF1493"},
                "holiday": {"value": holiday_reminder, "color": "#FFD700"},
                "encouragement": {"value": encouragement, "color": "#FF69B4"},
                "tips": {"value": weather_data.get('tips', '今天天气适宜'), "color": "#FFA500"},
                "sweet_words": {"value": sweet_words, "color": "#FF69B4"}
            }
        }
            
        # 发送请求(重试3次)
        url = f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}'
        
        for i in range(3):
            try:
                response = requests.post(url, json=data, timeout=30)
                result = response.json()
                    
                if result.get('errcode') == 0:
                    print(f"✅ 消息发送成功!城市:{city_name}")
                    print(f"   节假日提醒: {holiday_reminder}")
                    print(f"   鼓励语: {encouragement}")
                    return True
                else:
                    print(f"❌ 消息发送失败:{result}")
                    return False
            except Exception as e:
                print(f"❌ 第{i+1}次推送尝试失败:{e}")
                if i < 2:
                    print("⚙️ 等待10秒后重试...")
                    import time
                    time.sleep(10)
        
        print("❌ 重试3次均失败")
        return False
