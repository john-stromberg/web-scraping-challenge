#import dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import numpy as np
import pandas as pd
import requests

 
def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

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
    featured_image = "https://www.jpl.nasa.gov"+ featured_image_url[0]

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
       

    #Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet
    mars_facts_url = "https://space-facts.com/mars/"
    fact_table = pd.read_html(mars_facts_url)
    mars_df = fact_table[0]
    #convert the data to a HTML table string
    mars_html = mars_df.to_html('table.html')
    
    #hemispheres
    #visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    mars_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_url) 

    html = browser.html
    soup = bs(html, "html.parser")

    #create empty list to store dictionaries of titles & links to images
    hemisphere_image_urls = []

    #retrieve all elements that contain image information
    results = soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all("div", class_="item")

    #loop through each image
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        #remove Enhanced from image title 
        title = title.replace(" Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    hemisphere_image_urls

    #store data in dictionary 
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image,
        "mars_weather": mars_weather[0],
        "mars_html": mars_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

    return mars_data

if __name__ == '__main__':
    scrape()
