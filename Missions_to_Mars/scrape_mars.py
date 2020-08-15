from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from splinter.exceptions import ElementDoesNotExist
import re


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser
	 
def mars_news_scrape():
    mars_data={}
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)    
    time.sleep(1)
    #create HTMl Object
    html = browser.html
    #parse HTML with beautiful soup
    soup = bs(html, 'html.parser')
    # Extract title text
    news_title = soup.find_all("div", class_ = "content_title")[1].a.text
    news_p = soup.find("div", class_ = "article_teaser_body").text 
	
    
    
    #Visit Nasa's JPL Mars Space url  using splinter module
    jplNasa_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jplNasa_url)
    html = browser.html
    #parse HTML with beautiful soup
    soup = bs(html, 'html.parser')
    #get base Nasa link
    main_url ='https://www.jpl.nasa.gov'
    img_url = soup.find_all('a', class_='fancybox')[0].get('data-fancybox-href').strip()
    full_image_url = main_url + img_url
	 

    # #### Mars Facts
    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'
    # use Pandas to get the url table
    tables = pd.read_html(url)
    # Convert list of table into pandas dataframe
    df = tables[0]
    # update column name
    df.columns=['description','value']
    #Set the index to the description column
    df.set_index('description', inplace=True)
    # Use pandas to  generate HTML tables from DataFrames and save as html file
    mars_table=df.to_html(justify='left')
    
    # Visit the Mars Facts webpage
    # Visit the USGS Astrogeology site
    USGS_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    short_url="https://astrogeology.usgs.gov"
    browser = init_browser()
    browser.visit(USGS_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    main_url = soup.find_all('div', class_='item')
     
    hemisphere_img_urls=[]      
    for x in main_url:
        title = x.find('h3').text
        url = x.find('a')['href']
        hem_img_url= short_url+url
        #print(hem_img_url)
        browser.visit(hem_img_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        hemisphere_img_original= soup.find('div',class_='downloads')
        hemisphere_img_url=hemisphere_img_original.find('a')['href']
          
        print(hemisphere_img_url)
        img_data=dict({'title':title, 'img_url':hemisphere_img_url})
        hemisphere_img_urls.append(img_data)


        
    #Visit the Mars Weather twitter account
    url='https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    
    mars_weather = soup.find_all('span')
    for i in range(len(mars_weather)):
        if ("InSight" in mars_weather[i].text):
            mars_weather = mars_weather[i].text
        break

    mars_weather=soup.find('script', 'src').text
    

# Store data in a dictionary
    mars_data= {

        'news_title':news_title,
        'news_p':  news_p,
        'full_image_url': full_image_url,
        'mars_weather': mars_weather,
        'fact_table': mars_table,
        'hemi_img': hemisphere_img_urls
    }

    return mars_data
    browser.quit()


