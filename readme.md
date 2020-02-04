# CoronaVirus Live Updates

A simple news aggregator that updates news about coronavirus periodically.

Requires Python 3.6 or above

### Install requirements

    pip install -r requirements.txt
    
### Database

Inside MySQL console

    create database corona_news;
    use corona_news;

    create table if not exists news
    (
        id int auto_increment
            primary key,
        title varchar(1024) null,
        link varchar(512) null,
        source varchar(255) null,
        published_date datetime default CURRENT_TIMESTAMP null,
        constraint news_link_uindex
            unique (link)
    );
    
Initialize env.py with proper variables

Update live stats csv

    python csv_downloader.py


### Running the spider

    scrapy runspider rss_scraper.py
    
### Running the app locally

    python corona_app.py

For deployment check [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04) on DigitalOcean
