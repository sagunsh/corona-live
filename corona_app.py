import csv

import pymysql
from flask import Flask, render_template, request, jsonify
from env import HOST, DATABASE, USER, PASSWORD

app = Flask(__name__)


def create_connection():
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DATABASE,
                           cursorclass=pymysql.cursors.DictCursor)
    return conn


@app.route('/corona-news/from')
def from_source():
    site = request.args.get('site', '')
    page = request.args.get('page', 1)
    try:
        page = int(page)
    except:
        page = 1

    if page < 1:
        page = 1

    limit = 30
    offset = (page - 1) * limit

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM news WHERE source="{site}" ORDER BY published_date DESC LIMIT {offset}, {limit}')
    news = cursor.fetchall()  # list of dict
    return render_template('site.html', news=news, next_page=page + 1, site=site)


@app.route('/corona-news')
def corona_news():
    page = request.args.get('page', 1)
    try:
        page = int(page)
    except:
        page = 1

    if page < 1:
        page = 1

    limit = 30
    offset = (page - 1) * limit

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM news ORDER BY published_date DESC LIMIT {offset}, {limit}')
    news = cursor.fetchall()
    return render_template('index.html', news=news, next_page=page + 1)


@app.route('/corona-live')
def live_update():
    with open('data.csv') as file:
        reader = csv.DictReader(file)
        items = []
        total = {'Country': 'Total', 'Province': '', 'Confirmed': 0, 'Deaths': 0, 'Recovered': 0}
        for row in reader:
            items.append(dict(row))
            total['LastUpdate'] = row['LastUpdate']
            total['Confirmed'] += int(row['Confirmed'])
            total['Deaths'] += int(row['Deaths'])
            total['Recovered'] += int(row['Recovered'])
    return render_template('live_update.html', items=items, total=total)


@app.route('/')
def home():
    return '<h1 align="center" style="margin-top:200px;">Hello World!</h1>'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
