from splinter import Browser
from bs4 import BeautifulSoup
from splinter.exceptions import ElementDoesNotExist
import requests
import os
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"} 
    return Browser("chrome", **executable_path, headless=False)

mars_scrape = {}

def scrape():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html

    soup = BeautifulSoup(html, "html.parser")
    mars_scrape["news_title"] = soup.find('div', class_="content_title").text.lstrip()
    mars_scrape["news_p"] = soup.find('div', class_="article_teaser_body").text
    browser.quit()

    return mars_scrape

def scrape_featured():
    browser = init_browser()
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    img = soup.find('article')['style']
    sep = "'"
    rest = img.split(sep, 2)[1]
    mars_scrape["featured_img"] = image_url + rest
    browser.quit()
    
    return mars_scrape

def scrape_wx():
    browser = init_browser()
    mars_wx_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_wx_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_scrape["mars_wx"] = soup.find('div',class_='js-tweet-text-container').find('p').text
    browser.quit()

    return mars_scrape

def scrape_facts():
    browser = init_browser()
    mars_facts = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts)

    df = tables[0]
    html_table = df.to_html()
    html_table.replace('\n', '')

    mars_scrape["mars_facts"] = html_table
    browser.quit()

    return mars_scrape

def scrape_hemispheres():
    browser = init_browser()
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemisphere_url)
    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item')

    base_url = 'https://astrogeology.usgs.gov'
    hemisphere_list = []

    for item in items:
        hem_url = item.a['href']
        hemisphere = item.find('h3').text
        #hem_list.append(item.find('h3').text)
        browser.visit(base_url + hem_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        #hemisphere = soup.find('div',class_='content').find('h2').text
        images = soup.find('div',class_='downloads').find_all('li')
        hemisphere_list.append({"Title": hemisphere, "Image" : images[1].a['href']})
        
    mars_scrape["hemisphere_list"] = hemisphere_list
    browser.quit()

    return mars_scrape