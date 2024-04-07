# 爬虫工具练手项目
**本项目仅供学习参考，请勿用于商业用途**  
本项目基于DrissionPage框架开发  
目目前支持小红书指定关键词文章的爬取。  

DrissionPage框架地址：[https://drissionpage.cn/](https://drissionpage.cn/)
## 使用方法
项目配置在`config.py`中
1. 获取cookie
```bash
python main.py --cookie get_red_book_cookie
```
2. 获取指定关键词文章
```angular2html
python main.py -t red_book -k 爬虫
```

案例图片：  
![demo.png](img%2Fdemo.png)

