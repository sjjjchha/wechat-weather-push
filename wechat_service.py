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
        """计算下一个休息日或节假日"""
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
            holiday_date = datetime.datetime(today.year, month, day)
            if holiday_date > today:
                days_diff = (holiday_date - today).days
                if days_diff < min_days:
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
            "不用看星星了，我的眼里就是星光，而我的星光都是你。",
            "想把春夏秋冬的温柔，都揉进对你的喜欢里。",
            "和你在一起的每一天，连发呆都是甜甜的。",
            "早餐想和你分享，晚霞想和你共赏，余生想和你共度。",
            "柴米油盐不算平淡，有你相伴就是浪漫。",
            "睡前想的最后一个人是你，醒来想的第一个人也是你。",
            "就算什么都不做，只要和你待在一起，就觉得很安心。",
            "想和你窝在沙发上，裹着同一条毯子，看一部慢悠悠的电影。",
            "你的碎碎念，是我听过最温柔的人间烟火。",
            "把平凡的日子，过成有你的独家浪漫。",
            "我的偏爱和例外，从来都只给你一个人。",
            "绕过江山错落，才发现你是人间星火。",
            "你不是我权衡利弊后的选择，而是我怦然心动后，明知不可为而为之的坚定。",
            "人间纵有百媚千红，唯独你是我情之所钟。",
            "山野千里，你是我藏在微风里的喜欢。",
            "我见过千万人，像你的发，像你的眼，却都不是你的脸。",
            "对你的喜欢，是藏不住的心动，是说不尽的温柔。",
            "如果爱意有声音，那我的心跳早就震耳欲聋了。",
            "我想把所有的温柔和偏爱，都攒起来给你。",
            "这辈子，只想和你，一屋两人，三餐四季，岁岁年年。",
            "申请成为你心里永久的居民，不接受反驳哦～",
            "今天的我超喜欢你，明天的我，会更喜欢你。",
            "我的心是甜的，因为里面装的全是你呀。",
            "想偷你的体温，想蹭你的温柔，想做你一辈子的小朋友。",
            "你不用多好，我喜欢就好；我没有很好，你不嫌弃就好。",
            "警告！你已经被我的喜欢包围，不准逃跑～",
            "我对你的喜欢，就像小熊软糖，甜滋滋还弹弹的。",
            "要抱抱，要摸头，要你的全部偏爱和温柔。",
            "你是我的小笨蛋，也是我的小宝贝，别人不许碰～",
            "我想住进你的心里，没有房租，永远定居。",
            "晚风轻踩着云朵，月亮在贩售快乐，而我在偷偷想你。",
            "人间烟火，山河远阔，无一是你，无一不是你。",
            "我把温柔设置成了仅你可见，把偏爱都留给了你。",
            "星河滚烫，你是人间理想；世事无常，你是人间琳琅。",
            "愿有岁月可回首，且以深情共白头。",
            "我在人间贩卖黄昏，只为收集世间温柔去见你。",
            "山野万里，你是我藏在微风里的欢喜。",
            "你是揉碎的日光，落入我梦境的一片温良。",
            "绕过日月星辰，越过山川河流，只想和你相守。",
            "世间万般美好，都不及你眉眼间的温柔。",
            "不管世界多吵，只要有你在，我的心就安安稳稳。",
            "你不是救赎，却是我疲惫生活里唯一的甜。",
            "难过的时候抱抱我，开心的时候亲亲我，有你就够了。",
            "我想做你的太阳，温暖你所有不开心的时光。",
            "就算生活有点苦，有你在，就能嚼出甜味来。",
            "你的存在，就是我对抗所有不美好的勇气。",
            "不用刻意迎合，做你自己就好，我会永远偏向你。",
            "累了就靠在我肩上，我永远是你的避风港。",
            "平生不会相思，才会相思，便害相思。",
            "晓看天色暮看云，行也思君，坐也思君。",
            "愿我如星君如月，夜夜流光相皎洁。",
            "山有木兮木有枝，心悦君兮君不知。",
            "衣带渐宽终不悔，为伊消得人憔悴。",
            "金风玉露一相逢，便胜却人间无数。",
            "只愿君心似我心，定不负相思意。",
            "玲珑骰子安红豆，入骨相思知不知。",
            "我爱你，没有任何附加条件。",
            "想你，不分昼夜，不问朝夕。",
            "和你在一起，就是最好的时光。",
            "你在，心安；你走，心乱。",
            "这辈子，就想赖着你。",
            "我的满心欢喜，都是因为你。",
            "往后余生，皆是你。",
            "你是我唯一的选择，从来都是。"
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
