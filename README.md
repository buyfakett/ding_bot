# ding_bot

## 快速开始

1、创建企业内部应用

进入[钉钉开发者后台](https://open-dev.dingtalk.com/)，创建企业内部应用，获取ClientID（即 AppKey）和ClientSecret（ 即AppSecret）。

发布应用：在开发者后台左侧导航中，点击“版本管理与发布”，点击“确认发布”，并在接下来的可见范围设置中，选择“全部员工”，或者按需选择部分员工。

2、Stream 模式的机器人

如果不需要使用机器人功能的话，可以不用创建。

在应用管理的左侧导航中，选择“消息推送”，打开机器人能力，设置机器人基本信息。

注意：消息接收模式中，选择 “Stream 模式”

![Stream 模式](https://img.alicdn.com/imgextra/i3/O1CN01XL4piO1lkYX2F6sW6_!!6000000004857-0-tps-896-522.jpg)

点击“点击调试”按钮，可以创建测试群进行测试。

3、把配置文件设置好

4、`bash setup.sh`