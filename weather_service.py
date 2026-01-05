#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import os

class WeatherService:
    """天气服务"""
    
    def __init__(self):
        self.amap_key = os.environ.get('AMAP_KEY', '')
    
    def get_weather_by_city_name(self, city_name):
        """根据城市名称获取天气"""
        try:
            # 第一步:获取城市编码
            city_code = self.get_city_code(city_name)
            if not city_code:
                print(f"⚠️ 未找到城市 {city_name} 的编码")
                return None
            
            # 第二步:根据编码获取天气
            url = 'https://restapi.amap.com/v3/weather/weatherInfo'
            params = {
                'key': self.amap_key,
                'city': city_code,
                'extensions': 'all'
            }
            
            response = requests.get(url, params=params, timeout=10)
            result = response.json()
            
            if result.get('status') == '1' and result.get('count') != '0':
                forecasts = result.get('forecasts', [])[0]
                today = forecasts.get('casts', [])[0]
                
                weather_data = {
                    'weather': today.get('dayweather', '未知'),
                    'temperature': today.get('daytemp', '--'),
                    'max_temp': today.get('daytemp', '--') + '℃',
                    'min_temp': today.get('nighttemp', '--') + '℃',
                    'wind': today.get('daywind', '') + today.get('daypower', '') + '级',
                }
                
                # 生成智能提醒
                weather_data['tips'] = self.generate_tips(today)
                
                return weather_data
            else:
                print(f"⚠️ 获取天气失败:{result}")
                return None
                
        except Exception as e:
            print(f"❌ 获取天气异常:{e}")
            return None
    
    def get_city_code(self, city_name):
        """根据城市名称获取城市编码"""
        city_codes = {
            '北京': '110000', '上海': '310000', '天津': '120000', '重庆': '500000',
            '广州': '440100', '深圳': '440300', '成都': '510100', '杭州': '330100',
            '武汉': '420100', '西安': '610100', '郑州': '410100', '南京': '320100',
            '济南': '370100', '沈阳': '210100', '长沙': '430100', '哈尔滨': '230100',
            '昆明': '530100', '福州': '350100', '石家庄': '130100', '苏州': '320500',
            '佛山': '440600', '东莞': '441900', '无锡': '320200', '烟台': '370600',
            '太原': '140100', '合肥': '340100', '南昌': '360100', '青岛': '370200',
            '大连': '210200', '厦门': '350200', '宁波': '330200', '长春': '220100',
            '南充': '511300', '自贡': '510300',
        }
        
        city_name = city_name.replace('市', '')
        return city_codes.get(city_name, '440100')  # 默认广州
    
    def generate_tips(self, weather_data):
        """根据天气生成智能提醒"""
        tips = []
        
        weather = weather_data.get('dayweather', '')
        try:
            temp_max = int(weather_data.get('daytemp', 25))
        except:
            temp_max = 25
        
        # 温度提醒
        if temp_max >= 35:
            tips.append("今天很热,记得多喝水,别中暑了哦")
        elif temp_max >= 30:
            tips.append("今天有点热,注意防晒")
        elif temp_max <= 10:  # 修复: <= 10
            tips.append("今天很冷,记得多穿点,别冻着了")
        elif temp_max <= 15:
            tips.append("今天有点凉,注意保暖哦")
        
        # 天气提醒
        if '雨' in weather:
            tips.append("今天有雨,记得带伞哦")
        elif '雪' in weather:
            tips.append("今天下雪了,路滑要小心")
        elif '雾' in weather or '霾' in weather:
            tips.append("今天空气不太好,记得戴口罩")
        elif '晴' in weather:
            tips.append("今天天气不错,心情也要美美哒")
        elif '阴' in weather:
            tips.append("今天阴天,记得带个好心情")
        elif '多云' in weather:
            tips.append("今天多云,天气还不错哦")
        
        # 返回第一条提醒,如果没有就返回默认值
        result = tips[0] if tips else '今天天气适宜,适合出门~'
        print(f"💡 生成的温馨提示: {result}")
        return result
