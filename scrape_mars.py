from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd

import tweepy
import json
import numpy as np
import matplotlib.pyplot as plt
from config import consumer_key, consumer_secret, access_token, access_token_secret

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    
    mars_data = {}


    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text

    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

    url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_img)
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    image_source= soup2.find(class_="articles")
    image = image_source.find("a")["data-fancybox-href"]
    featured_image_url = 'https://www.jpl.nasa.gov'+image

    mars_data["featured_image_url"] = featured_image_url

    target_user = "@MarsWxReport"
    tweet_texts = []

    public_tweets = api.user_timeline(target_user, count=1)

    for tweet in public_tweets:

        print(tweet["text"])

        tweet_texts.append(tweet["text"])

    mars_data["mars_weather"] = tweet_texts


    fact_url = 'http://space-facts.com/mars/'
    fact_tables = pd.read_html(fact_url)
    fact_df = fact_tables[0]
    fact_df.columns = ['Mars', "Facts"]
    mars_fact_df=fact_df.set_index("Mars")
    html_table = mars_fact_df.to_html()
    html_table = html_table.replace('\n', '')
    html_table = mars_fact_df.to_html('table.html')
    mars_data["fact_html"] = html_table


    # url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # browser.visit(url_hemisphere)
    # html_hem = browser.html
    # soup_hem = BeautifulSoup(html_hem, 'html.parser')
    #hemisphere_url = soup_hem.find_all("a", class_ = "itemLink product-item")


    url_Cerberus = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    browser.visit(url_Cerberus)
    hemisphere_image_urls = []

    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')
    Cerberus_final_url = soup3.find('div', class_='downloads').a["href"]
    Cerberus_title = soup3.find("h2", class_="title").text

    cerberus = {
        "title": Cerberus_title,
        "img_url": Cerberus_final_url
    }

    hemisphere_image_urls.append(cerberus)


    url_schiaparelli = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    browser.visit(url_schiaparelli)
    html4 = browser.html
    soup4 = BeautifulSoup(html4, 'html.parser')

    schiaparelli_final_url = soup4.find('div', class_='downloads').a["href"]
    schiaparelli_title = soup4.find("h2", class_="title").text

    schiaparelli= {
        "title": schiaparelli_title,
        "img_url": schiaparelli_final_url
    }

    hemisphere_image_urls.append(schiaparelli)

    url_syrtis_major = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    browser.visit(url_syrtis_major)

    html5 = browser.html
    soup5 = BeautifulSoup(html5, 'html.parser')
    syrtis_major_final_url = soup5.find('div', class_='downloads').a["href"]
    syrtis_major_title = soup5.find("h2", class_="title").text



    syrtis_major= {
        "title": syrtis_major_title,
        "img_url": syrtis_major_final_url
    }

    hemisphere_image_urls.append(syrtis_major)

    url_valles_marineris = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    browser.visit(url_valles_marineris)

    html6 = browser.html
    soup6 = BeautifulSoup(html6, 'html.parser')
    valles_marineris_final_url = soup6.find('div', class_='downloads').a["href"]
    valles_marineris_title = soup6.find("h2", class_="title").text

    valles_marineris= {
        "title": valles_marineris_title,
        "img_url": valles_marineris_final_url
    }

    hemisphere_image_urls.append(valles_marineris)

    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    return mars_data
