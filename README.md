# Airobots

整合了Airtest Project和RobotFramework框架的方法。

另外整合了HTTPRunner，实现一个框架同时支持Android、IOS、WEB、API的自动化测试及性能测试(HTTPRunner提供的基于Locust的压力生成器，不带资源监控)。

安装框架依赖包, 执行

```
pip install https://github.com/BSTester/Airtest/archive/master.zip          # Python3.8 请先安装这个版本的Airtest
pip install airobots -i https://mirrors.aliyun.com/pypi/simple
```

运行WEB测试，需要安装ChromeDriver，请自行下载安装，或安装node之后执行 `npm install -g chromedriver` 安装

## 执行测试 

Allure 报告
```
airobots -t api ./API/Case/Path/ --alluredir=Results             # API测试
airobots -t web ./Web/Case/Path/ --alluredir=Results             # Web测试
airobots -t android ./Android/Case/Path/ --alluredir=Results     # Android测试
airobots -t ios ./IOS/Case/Path/ --alluredir=Results             # IOS测试
```

HTML 报告
```
airobots -t api ./API/Case/Path/ --html=Results/report.html          # API测试
airobots -t web ./Web/Case/Path/ --html=Results/report.html          # Web测试
airobots -t android ./Android/Case/Path/ --html=Results/report.html  # Android测试
airobots -t ios ./IOS/Case/Path/ --html=Results/report.html          # IOS测试
```