from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'c:/users/anali/bin/chromedriver.exe'}
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
    #get base Nasa link
    main_url ='https://www.jpl.nasa.gov'
    #get image url from the soup object.
    #featured_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    featured_image_url = soup.find_all('img')[2]["src"]
    #Create one full image url link
    full_image_url=main_url+featured_image_url
	 
    
    #Visit the Mars Weather twitter account
    url='https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    
    #find tweet and extract text
    mars_weather = soup.find_all('span')
    for i in range(len(mars_weather)):
        if ("InSight" in mars_weather[i].text):
            mars_weather[i].text
        break
    
    # Mars Facts
    url_facts = "https://space-facts.com/mars/"
    browser.visit(url_facts)
    df_facts = pd.read_html(url_facts)[0]
    df_facts.columns = ["Facts","Values"]
    clean_table = df_facts.set_index(["Facts"])
    mars_table = clean_table.to_html()
    mars_table = mars_table.replace("\n", "")
	

    #Hemisphere Images Scraping
    hemispheres_url ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_hemispheres = soup.find_all('h3')
	
	
    hemisphere_image_urls = []
	#Loop to scrape all hemispheres
    for row in mars_hemispheres:
        title= row.text
        browser.click_link_by_partial_text(title)
        time.sleep(1)
        img_html = browser.html
        soup_h = bs(img_html, 'html.parser')
        url_img = soup_h.find('div',class_='downloads').a['href']
        print ("Hemisphere Name :  "+ str(title))
        print ("Hemisphere URL:  " + str(url_img))

        img_dict = {}
        img_dict['title']= title
        img_dict['img_url']= url_img
        hemisphere_image_urls.append(img_dict)	
        
        browser.visit(hemispheres_url)


# Store data in a dictionary
    mars_data= {

        'news_title':news_title,
        'news_p':  news_p,
        'full_image_url': full_image_url,
        'weather': mars_weather,
        'fact_table': mars_table,
        'hemisphere_image': hemispheres_url
    }
    browser.quit()
    return mars_data


