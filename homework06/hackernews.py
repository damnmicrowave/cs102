from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label.is_(None)).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    news_id = request.query['id']
    label = request.query['label']
    s = session()
    news_item = s.query(News).filter(News.id == news_id).all()[0]
    news_item.label = label
    s.add(news_item)
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()

    for n in get_news('https://news.ycombinator.com/newest'):
        title = n['title']
        author = n['author']
        if not s.query(News).filter(News.title.is_(title), News.author.is_(author)).count():
            news_item = News(
                title=n['title'],
                author=n['author'],
                url=n['url'],
                domain=n['domain'],
                comments=n['comments'],
                points=n['points'],
            )
            s.add(news_item)

    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080)
