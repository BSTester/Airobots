import os

# 公共变量

# 预发布环境
db_host = '' 
db_port = 3306 
db_user = ''
db_passwd = ''
db_name = 'db_production' 

redis_host = ''
redis_port = 6379
redis_passwd = ''

test_host = ''
test_php_host = ''

redis_ssh_host = ''
redis_ssh_port = 22
redis_ssh_user = 'ubuntu'
redis_ssh_key = os.path.join(os.path.dirname(__file__), 'TestFiles', 'HeyteaGo_develop.pem')

browser = 'Chrome'    # 启动浏览器类型，可选：Firefox、Chrome、PhantomJS
remote_url = 'http://grid:4444/wd/hub'

