# Airobot

整合了Airtest Project和RobotFramework框架的方法。

另外整合了HTTPRunner，实现一个框架同时支持Android、IOS、WEB、API的自动化测试及性能测试(HTTPRunner提供的基于Locust的压力生成器，不带资源监控)。

目录结构说明：

    ├─Library                           # 测试相关自定义库
    ├─Resource                          # 测试相关资源文件
    │  ├─TestFiles
    │  └─TestSQL
    ├─Results                           # 测试报告存放目录
    ├─TestCase                          # 测试用例存放目录
    │  ├─APICase                        # API测试用例存放目录
    │  ├─GUICase                        # GUI测试用例存放目录
    │  ├─AndroidCase                    # Android测试用例存放目录
    │  ├─IOSCase                        # IOS测试用例存放目录
    │  └─PageObjects                    # POM文件存放目录
    └─WebChrome                         # 浏览器远程客户端相关服务
        ├─SeleniumGrid
        └─WebDriver

使用前请先执行 `pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple` 安装相关依赖包

运行GUI测试，需要安装ChromeDriver，请自行下载安装，或安装node之后执行 `npm install -g chromedriver` 安装

执行测试 `pytest .\TestCase\AndroidCase\ --alluredir=Results`