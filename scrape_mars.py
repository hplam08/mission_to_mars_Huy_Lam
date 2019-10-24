from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd


def scrape():
    
    scraped_data = {}    
    
    # URL of page to be scraped - Launch page first
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
        # Use Beautiful Soup to parse the data
    html = browser.html
    soup = bs(html,'html.parser')
        # Retrieve the Latest News Title and paragraph text
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='rollover_description').text
    scraped_data['News_Title']= news_title
    scraped_data['News_Paragraph']=news_p
    
# JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # Request and parse the HTML
    html = browser.html
    soup = bs(html,'html.parser')
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(4)
    browser.click_link_by_partial_text('more info')
    
        # Request and parse again
    html_code = browser.html
    soup = BeautifulSoup(html_code, "html.parser")
    image = soup.find('figure', class_='lede').a['href']
    featured_image_url = 'https://www.jpl.nasa.gov'+image
    scraped_data['Featured_Img_URL']=featured_image_url
    
## JPL Mars Space Images - Featured Image
    url = 'https://twitter.com/marswxreport?lang=en'
    time.sleep(3)
    browser.visit(url)
    # Request and parse
    html_code = browser.html
    soup = BeautifulSoup(html_code, "html.parser")
    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    scraped_data['Mars_Weather']=mars_weather
    
## Mars Facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    # Request and parse
    html_code = browser.html
    soup = BeautifulSoup(html_code, "html.parser")
    fact_table = soup.find('table',{'class':'tablepress tablepress-id-p-mars'})    
    
    fact_table_rows = fact_table.find_all('tr')
    col_1 = []
    col_2 = []
    
    for row in fact_table_rows:
        rows = row.find_all('td')
        col_1.append(rows[0].text)
        col_2.append(rows[1].text)
        
    facts_df = pd.DataFrame({'facts':col_1, 'values':col_2})
    facts_html = facts_df.to_html()
    scraped_data['Mars_Facts']=facts_html
    
## Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Request and parse the HTML
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    #print(soup.prettify())
    images = soup.find_all('h3')
#     print(images)
    titles = []
    for image in images:
        titles.append(image.text)
#     for link in soup.find_all('a'):
#         print(link.get('href'))
    for title in titles:
        print(title)
        
    links = []
    for title in titles:
        browser.click_link_by_partial_text(title)
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        link_addr = soup.find('img',class_='wide-image')
        links.append('https://astrogeology.usgs.gov'+link_addr.attrs['src'])
        browser.back()
        
    hemisphere_image_urls = {}
    combine = list(zip(titles, links))
    title_link = []
    for title,link in combine:
        title_link.append({'title': title, 'img_url':link})
    scraped_data['Hemisphere_Image_URLs']=title_link

    return scraped_data