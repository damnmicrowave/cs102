import string

from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


model = NaiveBayesClassifier()


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
    s = session()
    news = s.query(News).filter(News.label.is_(None)).all()
    news_titles = [news_item.title for news_item in news]
    news_urls = [news_item.url for news_item in news]
    news = list(zip(news_titles, news_urls))
    good = [f"{news[i][0]} {news[i][1]}" for i, p in enumerate(model.predict(news_titles)) if p == 'good']
    maybe = [news_titles[i] for i, p in enumerate(model.predict(news_titles)) if p == 'maybe']
    never = [news_titles[i] for i, p in enumerate(model.predict(news_titles)) if p == 'never']
    print(good, maybe, never)
    return template('news_recommendations', rows=good)


if __name__ == "__main__":
    x, y = [], []

    def clean(title):
        translator = str.maketrans("", "", string.punctuation)
        return title.translate(translator)

    for n in session().query(News).all():
        x.append(clean(n.title).lower())
        y.append(n.label)
    model.fit(x, y)
    run(host="localhost", port=8080)
