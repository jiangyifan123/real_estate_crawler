# Redis数据库地址
REDIS_HOST = '127.0.0.1'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

# 产生器使用的浏览器
BROWSER_TYPE = 'Chrome'

# 产生器类，如扩展其他站点，请在此配置
GENERATOR_MAP = {
    # 'weibo': 'WeiboCookiesGenerator',
    # 'zillow': 'ZillowCookiesGenerator',
    'realtor': 'RealtorCookiesGenerator',
}

# 测试类，如扩展其他站点，请在此配置
TESTER_MAP = {
    # 'weibo': 'WeiboValidTester'
    'realtor': 'RealtorValidTester',
}

TEST_URL_MAP = {
    # 'weibo': 'https://m.weibo.cn/'
    'realtor': 'https://www.realtor.com/realestateandhomes-detail/312-W-5th-St-Apt-1005_Los-Angeles_CA_90013_M24602-35146'
}

# 产生器和验证器循环周期
CYCLE = 120

# API地址和端口
API_HOST = '0.0.0.0'
API_PORT = 5020

# 产生器开关，模拟登录添加Cookies
GENERATOR_PROCESS = True
# 验证器开关，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = True
# API接口服务
API_PROCESS = True
