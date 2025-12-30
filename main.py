#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from weather_service import WeatherService
from wechat_service import WeChatService

def main():
    """主函数"""
    
    print("=" * 50)
    print("🚀 开始执行微信天气推送")
    print("=" * 50)
    
    # 1. 获取配置的城市名称
    city_name = os.environ.get('CITY_NAME', '广州')
    print(f"\n📍 当前配置城市: {city_name}")
    
    # 2. 初始化服务
    weather_service = WeatherService()
    wechat_service = WeChatService()
    
    # 3. 获取天气
    print(f"\n🌤️ 正在获取 {city_name} 的天气...")
    weather_data = weather_service.get_weather_by_city_name(city_name)
    
    if not weather_data:
        print("❌ 无法获取天气信息,推送终止")
        return
    
    print(f"✅ 天气:{weather_data.get('weather')}")
    print(f"   温度:{weather_data.get('min_temp')} ~ {weather_data.get('max_temp')}")
    print(f"   提醒:{weather_data.get('tips')}")
    
    # 4. 发送微信推送
    print("\n💌 正在发送微信推送...")
    success = wechat_service.send_template_message(city_name, weather_data)
    
    if success:
        print("\n" + "=" * 50)
        print("✅ 推送完成!")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ 推送失败,请检查日志")
        print("=" * 50)

if __name__ == '__main__':
    main()
