#import dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import numpy as np
import pandas as pd
import requests
 

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser
    mars_dict = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text
    news_title = soup.find("div", class_= "content_title").text
    news_p = soup.find("div", class_= "article_teaser_body").text
    
    #add to mars dictionary 
    mars_dict["news_title"] = news_title
    mars_dict["news_p"] = news_p

    #Visit the url for JPL Featured Space Image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = bs(html, "html.parser")
    #collect and print featured image url
    featured_image_url = []
    images = soup.find_all("a", class_= "fancybox")
    for image in images:
        image = image['data-fancybox-href']
        featured_image_url.append(image)

    #add to mars dictionary
    mars_dict["featured_image_url"] = "https://www.jpl.nasa.gov" + featured_image_url[0]

    #Visit the Mars Weather twitter account
    mars_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_url)
    response = requests.get(mars_url)
    soup = bs(response.text, "html.parser")
    mars_weather = []
    tweets = soup.find_all("div", class_= "content")
    for tweet in tweets:
        tweet = tweet.find("div", class_= "js-tweet-text-container").text
        mars_weather.append(tweet)

    #add to mars dictionary
    mars_dict["mars_weather"] = mars_weather[0]

    #Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet
    mars_facts_url = "https://space-facts.com/mars/"
    fact_table = pd.read_html(mars_facts_url)
    mars_df = fact_table[0]
    #convert the data to a HTML table string
    mars_html = mars_df.to_html()
    
    #add to mars dictionary
    mars_dict["fact_table"] = mars_html

    #hemispheres

    return mars_dict
