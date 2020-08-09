from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
def init_browser():
	# @NOTE: Replace the path with your actual path to the chromedriver
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
        return browser
   
mars_data= {}
def mars_news_scrape():
         browser = init_browser()
        #Visit Nasa News url  using splinter module
    
         url = 'https://mars.nasa.gov/news/'
         browser.visit(url)    
	     #create HTMl Object
         html = browser.html
         #parse HTML with beautiful soup
         soup = bs(html, 'html.parser')
    
         # Extract title text
         #news_title = soup.find('div',class_='content_title').text
         news_title = soup.find('div',class_='content_title').text
         mars_data['news_title']= news_title
         print(f"title {news_title}")
         # Extract Paragraph text
         #news_p = soup.find('div',class_='article_teaser_body').text
         news_p = soup.find('div',class_='article_teaser_body')
         mars_data['news_p'] = news_p
         #print(news_p)
         print(f"paragraph {news_p}")
       
         return mars_data
   
def img_scrape():
       browser = init_browser()
       #Visit Nasa's JPL Mars Space url  using splinter module
       url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
       browser.visit(url)
   
       #Getting the base url
       from urllib.parse import urlsplit
       base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
       print(base_url)
   
       #Design an xpath selector to grab the image
       xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"
   
       #Use splinter to click on the mars featured image
       #to bring the full resolution image
       results = browser.find_by_xpath(xpath)
       img = results[0]
       img.click()
   
       #get image url using BeautifulSoup
       html_image = browser.html
       soup = bs(html_image, "html.parser")
       img_url = soup.find("img", class_="fancybox-image")["src"]
       full_image_url = base_url + img_url
       mars_data['full_image_url'] = full_image_url
       print(full_image_url)
   
       return mars_data
 
def mars_weather():
       browser = init_browser()
       #Visit the Mars Weather twitter account
       url='https://twitter.com/marswxreport?lang=en'
       browser.visit(url)
       #create HTML object
       #html=browser.html
       soup = bs(html, 'html.parser')
   
       #find tweet and extract text
       mars_weather = soup.find_all('span')
       for i in range(len(mars_weather)):
           if ("InSight" in mars_weather[i].text):
               weather = mars_weather[i].text
               mars_data['mars_weather']=mars_weather
               mars_data['weather']=weather
               break
       return mars_data

def mars_facts():
        # Visit the Mars Facts webpage
        mars_facts_url='https://space-facts.com/mars/'
        mars_fact_table=pd.read_html(mars_facts_url)
   
        #Create Dataframe to store table data
        df = mars_fact_table[0]
        df.columns = ['Mars-Earth Comparison', 'Mars', 'Earth']
        mars_facts = df.to_html()
        mars_data['mars_facts'] = mars_facts
        return mars_data
 
def mars_hem():
 
       url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
       browser.visit(url4)
       html4 = browser.html
       soup4 = bs(html4, 'html.parser')
       links = browser.find_by_css("a.product-item h3")
   
       hemisphere_image_urls = []
   
       # First, get a list of all of the hemispheres
       links = browser.find_by_css("a.product-item h3")
   
       # Next, loop through those links, click the link, find the sample anchor, return the href
       for i in range(len(links)):
            hemisphere = {}
   
       		# We have to find the elements on each loop to avoid a stale element exception
            browser.find_by_css("a.product-item h3")[i].click()
   
            # Next, we find the Sample image anchor tag and extract the href
            sample_elem = browser.find_link_by_text('Sample').first
            hemisphere['img_url'] = sample_elem['href']
   
            # Get Hemisphere title
            hemisphere['title'] = browser.find_by_css("h2.title").text
   
            # Append hemisphere object to list
            hemisphere_image_urls.append(hemisphere)
   
            # Finally, we navigate backwards
            browser.back()
     
            hemisphere_img_urls.append(img_data)
            mars_data['hemisphere_img_urls']=hemisphere_img_urls
   
       return mars_data
  