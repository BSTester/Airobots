# 公共变量

# 预发布环境
db_host = 'gz-cdb-nw6294kl.sql.tencentcdb.com' 
db_port = 61421 
db_user = 'staging_test'
db_passwd = 'heyteago!@#qwe'
db_name = 'db_production' 

redis_host = '10.0.1.40'
redis_port = 6379
redis_passwd = '1KXCXupuAi'

test_host = 'https://staging.heytea.com'
test_php_host = 'https://staging.vip.heytea.com'

redis_ssh_host = '118.126.99.131'
redis_ssh_port = 22
redis_ssh_user = 'ubuntu'
redis_ssh_key = os.path.join(os.path.dirname(__file__), 'TestFiles', 'HeyteaGo_develop.pem')

browser = 'Chrome'    # 启动浏览器类型，可选：Firefox、Chrome、PhantomJS
remote_url = 'http://grid:4444/wd/hub'

