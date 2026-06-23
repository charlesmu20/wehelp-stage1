import urllib.request
from bs4 import BeautifulSoup
import csv
#抓3頁
url = "https://www.ptt.cc/bbs/Steam/index.html"
pages = []

for i in range(3):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html,"html.parser")
        pages.append(soup)
        prev = soup.find("a", string= "‹ 上頁")
        url = "https://www.ptt.cc" + prev["href"]

with open("articles.csv","w",newline="",encoding="utf-8") as f:
    writer = csv.writer(f)
# 遍歷每一頁的文章
    for page_soup in pages:
        articles = page_soup.find_all("div",class_="r-ent")
        for article in articles:
            title_tag = article.find("div",class_="title").find("a")
            if title_tag is None:
                continue
            title = title_tag.text
            likes = article.find("div",class_ = "nrec").text
            link = "https://www.ptt.cc" + title_tag["href"]
            with urllib.request.urlopen(link) as res:
                article_html = res.read()
                article_soup = BeautifulSoup(article_html,"html.parser")
                meta_value = article_soup.find_all("span",class_="article-meta-value")
                if meta_value:
                    publish_time = meta_value[-1].text
                else:
                    publish_time=""
            writer.writerow([title,likes,publish_time])
