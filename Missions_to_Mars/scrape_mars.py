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
             weather = mars_weather[i].text
         break
    
     # Mars Facts
     url_facts = "https://space-facts.com/mars/"
     browser.visit(url_facts)
     df_facts = pd.read_html(url_facts)[0]
     df_facts.columns = ["Facts","Values"]
     clean_table = df_facts.set_index(["Facts"])
     mars_table = clean_table.to_html()
     mars_table = mars_table.replace("\n", "")
	

     # # Mars Hemispheres
     hemisphere_image_urls = []
     time.sleep(2)
     # Cerberus Hemispheres
     url_cerberus = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
     browser.visit(url_cerberus)
     time.sleep(1)
     response_cerberus = browser.html
     soup4 = bs(response_cerberus, 'html.parser')
     cerberus_img = soup4.find_all('div', class_="wide-image-wrapper")

     for img in cerberus_img:
        pic_cerberus = img.find('li')
        cerberus_full_img = pic_cerberus.find('a')['href']
        cerberus_title = soup4.find('h2', class_='title').get_text()
        cerberus_hem = {"Title": cerberus_title, "url": cerberus_full_img}

     hemisphere_image_urls.append(cerberus_hem)

     # Schiaparelli Hemisphere

     url_schiaparelli = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
     browser.visit(url_cerberus)
     time.sleep(1)
     response_schiaparelli = browser.html
     soup5 = bs(response_schiaparelli, 'html.parser')
     schiaparelli_img = soup5.find_all('div', class_="wide-image-wrapper")

     for img in schiaparelli_img:
         pic_schiaparelli = img.find('li')
         schiaparelli_full_img = pic_schiaparelli.find('a')['href']
     shiaparelli_title = soup5.find('h2', class_='title').get_text()
     shiaparelli_hem = {"Title": shiaparelli_title, "url": schiaparelli_full_img}
     
     hemisphere_image_urls.append(shiaparelli_hem)

     # Syrtis Hemisphere

     url_syrtis = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced')
     browser.visit(url_syrtis)
     time.sleep(1)
     response_syrtis = browser.html
     soup6 = bs(response_syrtis, 'html.parser')
     syrtris_img = soup6.find_all('div', class_="wide-image-wrapper")

     for img in syrtris_img:
         pic_syrtris = img.find('li')
         syrtris_full_img = pic_syrtris.find('a')['href']
         syrtris_title = soup6.find('h2', class_='title').get_text()
         syrtris_hem = {"Title": syrtris_title, "url": syrtris_full_img}

     hemisphere_image_urls.append(syrtris_hem)

     # Valles Marineris Hemisphere

     url_valles = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced')
     browser.visit(url_valles)
     time.sleep(1)
     response_valles = browser.html
     soup7 = bs(response_valles, 'html.parser')
     valles_img = soup7.find_all('div', class_="wide-image-wrapper")

     for img in valles_img:
         pic_valles = img.find('li')
         valles_full_img = pic_valles.find('a')['href']
     valles_title = soup7.find('h2', class_='title').get_text()
     valles_hem = {"Title": valles_title, "url": valles_full_img}
     
     hemisphere_image_urls.append(valles_hem)

     # Store data in a dictionary
     mars_data= {

         'news_title':news_title,
         'news_p':  news_p,
         'full_image_url': full_image_url,
         'weather': mars_weather,
         'fact_table': mars_table,
         'hemisphere_image': hemisphere_image_urls
    }
     browser.quit()
     return mars_data


