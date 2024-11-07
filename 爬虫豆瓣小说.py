import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pylab as mpl
import os

# 让用户输入想要爬取的页数
pages = int(input("请输入你想爬取的页数: "))

all_titles = []
all_authors = []
all_scores = []

for i in range(pages):
    url = f'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start={i * 20}&type=T'
    page_text = requests.get(url=url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'})
    soup = BeautifulSoup(page_text.text, "html.parser")

    title = soup.find_all("h2")
    autor = soup.find_all("div", class_="pub")
    score = soup.find_all("span", class_="rating_nums")

    print(f"页面 {i + 1} 的数据：")
    print("--------------------")
    for x, y, z in zip(title, autor, score):
        title1 = x.get_text().strip("\n /")
        autor1 = y.get_text().strip("\n /")
        score1 = z.get_text().strip("\n /")
        print(f"书名: {title1}")
        print(f"作者: {autor1}")
        print(f"评分: {score1}")
        print("--------------------")

        all_titles.append(title1)
        all_authors.append(autor1)
        all_scores.append(float(score1))
    print("\n")
# 获取当前脚本的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 拼接字体文件的完整路径
font_path = os.path.join(script_dir, '.venv', 'lib', 'python3.10', 'site-packages', 'matplotlib', 'mpl-data', 'fonts', 'ttf', 'SimHei.ttf')

# 检查字体文件是否存在
if not os.path.exists(font_path):
    raise FileNotFoundError(f"字体文件未找到: {font_path}")

# 使用 FontProperties 加载字体
font = FontProperties(fname=font_path)


mpl.rcParams['axes.unicode_minus'] = False  # 用于正常显示负


# 创建饼图
plt.figure(figsize=(8, 8))
plt.pie(all_scores[:10], labels=all_titles[:10], autopct='%1.1f%%', startangle=140, textprops={'fontproperties': font})
plt.title("前10本书的评分比例", fontproperties=font)
plt.tight_layout()
plt.show()

# 使用 Plotly 创建交互式散点图
fig = go.Figure(data=go.Scatter(
    x=all_scores,
    y=all_titles,
    mode='markers',
    marker=dict(
        size=10,
        color=all_scores,  # 根据评分设置颜色
        colorscale='Viridis',  # 选择一个颜色比例
        showscale=True
    ),
    text=[f"作者: {author}" for author in all_authors],  # 悬停时显示作者信息
    hoverinfo='text+y+x'
))

fig.update_layout(
    title='书籍评分散点图',
    xaxis_title='评分',
    yaxis_title='书名',
    height=800
)

fig.show()