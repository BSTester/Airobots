# Airobots

全端自动化测试框架Airobots，整合了Airtest、RobotFramework、Selenium、Appium、HTTPRunner、Locust框架的方法，从而实现一套框架，能够进行全端的测试，统一执行入口和报告的输出。

本质上，Airobots可看成是以上优秀开源测试框架的集成库，整合后以实现方法的共用，比如在Selenium和Appium中使用Airtest的图像识别功能。实现一个框架同时支持Android、IOS、WEB、API的自动化测试及性能测试(HTTPRunner提供的基于Locust的压力生成器)，并且统一了测试报告输出格式，使用美观大气的Allure作为测试报告，可详细记录测试过程日志、测试步骤和截图。

安装框架依赖包, 执行

```
pip install airobots -i https://mirrors.aliyun.com/pypi/simple
```

> windows系统下, 如果安装失败, 可能需要安装C++编译工具: visualcppbuildtools_full.exe, 具体错误请留意控制台报错信息。


运行WEB测试，需要安装ChromeDriver，请自行下载安装，或安装node之后执行 `npm install -g chromedriver` 安装

## 执行测试 

Allure 报告(推荐)
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

## 查看Allure报告

```
allure serve ./Results
```

## 安装Allure

### Linux
```
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update 
sudo apt-get install allure
```

### Mac OS X

对于Mas OS，可通过[Homebrew](https://brew.sh/)进行自动安装

```
brew install allure
```

### Windows

对于Windows，可从[Scoop](https://scoop.sh/)命令行安装程序获得Allure。

要安装Allure，请下载并安装Scoop，然后在Powershell中执行

```
scoop install allure
```



演示项目: https://github.com/BSTester/AirobotsDemo

