import requests
from bs4 import BeautifulSoup
import time
import random


def get_movie_list(url, headers):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    movies = soup.find_all('div', class_='item')
    movie_list = []

    for movie in movies:
        title = movie.find('span', class_='title').text
        link = movie.find('a')['href']
        movie_list.append((title, link))

    return movie_list


def get_douban_comments(url, headers):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    comments = soup.find_all('div', class_='comment-item')

    for comment in comments:
        user = comment.find('span', class_='comment-info').a.text.strip()
        rating = comment.find('span', class_='rating')['title'] if comment.find('span', class_='rating') else "未评分"
        time = comment.find('span', class_='comment-time').text.strip()
        content = comment.find('span', class_='short').text.strip()

        print(f"用户: {user}")
        print(f"评分: {rating}")
        print(f"时间: {time}")
        print(f"评论: {content}")
        print("-" * 50)

    next_page = soup.find('a', class_='next')
    if next_page:
        return url.split('?')[0] + next_page['href']
    else:
        return None


# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 豆瓣电影 Top 250 页面
top_movies_url = "https://movie.douban.com/top250"

# 获取电影列表
movies = get_movie_list(top_movies_url, headers)

# 打印电影列表供用户选择
for i, (title, _) in enumerate(movies, 1):
    print(f"{i}. {title}")

# 用户选择电影
choice = int(input("请选择一部电影 (输入序号): ")) - 1
selected_movie, movie_url = movies[choice]

print(f"\n你选择了: {selected_movie}")
print("开始爬取评论...\n")

# 构造评论页面URL
comments_url = f"{movie_url}comments?status=P"

# 爬取评论
while comments_url:
    print(f"正在爬取: {comments_url}")
    comments_url = get_douban_comments(comments_url, headers)

    # 添加随机延迟，避免被封IP
    time.sleep(random.uniform(1, 3))

print("评论爬取完成。")