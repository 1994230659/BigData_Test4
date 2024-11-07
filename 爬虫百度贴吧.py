import re
import requests

def get(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

    # 发送请求
    request = requests.get(url=url, headers=headers)

    # 返回html源代码
    html = request.text

    # 标题
    titel = re.compile('"j_th_tit ">(.*)</a>')
    titles = re.findall(titel, html)
    # 发帖人
    author = re.compile('"主题作者: (.*)"')
    authors = re.findall(author, html)
    # 发帖时间
    time = re.compile('时间">(.*)</span>')
    times = re.findall(time, html)

    # 在控制台显示爬取的内容
    print("爬取结果:")
    print("-" * 50)
    for i in range(len(titles)):
        print(f"标题: {titles[i]}")
        print(f"作者: {authors[i]}")
        print(f"时间: {times[i]}")
        print("-" * 50)

    print("爬取完成")

url = "https://tieba.baidu.com/f?kw=%E4%B8%AD%E5%8C%97%E5%A4%A7%E5%AD%A6&ie=utf-8&tab=main"
get(url)