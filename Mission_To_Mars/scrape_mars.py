# Dependencies
import time
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd



def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Dictionary for all scraped data
    mars_data = {}

    # Visit the Mars news page. 
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
 

    # Search for news
    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the latest Mars news.
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text
  
    # Add the news date, title and summary to the dictionary
    mars_data["news_date"] = news_date
    mars_data["news_title"] = news_title
    mars_data["summary"] = news_p


    # Visit the url for JPL Featured Space Image here.
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    # Make sure to find the image url to the full size .jpg image.
    # Make sure to save a complete url string for this image.
    
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find('img', class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    
    
    # Adding featured image url to the dictionary
    mars_data["featured_image_url"] = img_url


    # Mars Weather 
    # Scraping most recent tweet 

    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3) 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    tweet = soup.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
    mars_weather = tweet.text
    
    # Adding weather to dictionary
    mars_data["mars_weather"] = mars_weather

    # Mars Facts
    url4 = "https://space-facts.com/mars/"
    browser.visit(url4)

    grab = pd.read_html(url4)
    mars_info = pd.DataFrame(grab[0])
    mars_info.columns = ['Mars','Data']
    mars_table=mars_info.set_index("Mars")
    marsdata = mars_table.to_html(classes='marsinformation')
    marsdata = mars_info.replace('\n', ' ')

    # Adding Mars facts table to dictionary
    mars_data["mars_table"] = marsdata 


    # Visit the USGS Astogeology site and scrape pictures of the hemispheres
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_hemis=[]
    
    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()
        mars_data['mars_hemis'] = mars_hemis
    return mars_data




