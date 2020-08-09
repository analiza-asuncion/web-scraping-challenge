{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import Dependecies \n",
    "from bs4 import BeautifulSoup as bs\n",
    "from splinter import Browser\n",
    "import pandas as pd \n",
    "import requests \n",
    "from selenium.webdriver.chrome.options import Options"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "def init_browser():\n",
    "    # @NOTE: Replace the path with your actual path to the chromedriver\n",
    "     executable_path = {'executable_path': 'chromedriver.exe'}\n",
    "     browser = Browser('chrome', **executable_path, headless=False)\n",
    "     return browser"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "mars_data= {}\n",
    "def mars_news_scrape():\n",
    "     browser = init_browser()\n",
    "    #Visit Nasa News url  using splinter module\n",
    "\n",
    "     url = 'https://mars.nasa.gov/news/'\n",
    "     browser.visit(url)    #create HTMl Object\n",
    "     html = browser.html\n",
    "     #parse HTML with beautiful soup\n",
    "     soup = bs(html, 'html.parser')\n",
    "\n",
    "     # Extract title text\n",
    "     news_date = soup.find('div', class_='list_date').text\n",
    "     mars_data['news_date']=news_date\n",
    "     print(f\"news date {news_date}\")\n",
    "     # Extract news title\n",
    "     news_title = soup.find('div',class_='content_title').find('a').text\n",
    "     mars_data['news_title']=news_title\n",
    "     print(f\"title {news_title}\")\n",
    "     # Extract Paragraph text\n",
    "     news_p = soup.find('div',class_='article_teaser_body').text\n",
    "     mars_data['news_p'] = news_p\n",
    "     #print(news_p)\n",
    "     print(f\"paragraph {news_p}\")\n",
    "    \n",
    "     return mars_data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "def img_scrape():\n",
    "    browser = init_browser()\n",
    "    #Visit Nasa's JPL Mars Space url  using splinter module\n",
    "    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'\n",
    "    browser.visit(url_image)\n",
    "\n",
    "    #Getting the base url\n",
    "    from urllib.parse import urlsplit\n",
    "    base_url = \"{0.scheme}://{0.netloc}/\".format(urlsplit(url_image))\n",
    "    print(base_url)\n",
    "\n",
    "    #Design an xpath selector to grab the image\n",
    "    xpath = \"//*[@id=\\\"page\\\"]/section[3]/div/ul/li[1]/a/div/div[2]/img\"\n",
    "\n",
    "    #Use splinter to click on the mars featured image\n",
    "    #to bring the full resolution image\n",
    "    results = browser.find_by_xpath(xpath)\n",
    "    img = results[0]\n",
    "    img.click()\n",
    "\n",
    "    #get image url using BeautifulSoup\n",
    "    html_image = browser.html\n",
    "    soup = bs(html_image, \"html.parser\")\n",
    "    img_url = soup.find(\"img\", class_=\"fancybox-image\")[\"src\"]\n",
    "    full_image_url = base_url + img_url\n",
    "    mars_data['full_image_url'] = full_image_url\n",
    "    print(full_image_url)\n",
    "\n",
    "    return mars_data"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "    #--------------------------------------------\n",
    "    # JPL Mars Space Images - SCRAPE FEATURED IMAGE\n",
    "    #--------------------------------------------"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "def mars_weather():\n",
    "    browser = init_browser()\n",
    "    #Visit the Mars Weather twitter account\n",
    "    url='https://twitter.com/marswxreport?lang=en'\n",
    "    browser.visit(url)\n",
    "    #create HTML object\n",
    "    html=browser.html\n",
    "    soup = bs(html, \"html.parser\")\n",
    "\n",
    "    #find tweet and extract text\n",
    "    mars_weather = soup.find_all('span')\n",
    "    for i in range(len(mars_weather)):\n",
    "        if (\"InSight\" in mars_weather[i].text):\n",
    "            weather = mars_weather[i].text\n",
    "            mars_data['mars_weather']=mars_weather\n",
    "            mars_data['weather']=weather\n",
    "        break\n",
    "    return mars_data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "def mars_facts():\n",
    "     # Visit the Mars Facts webpage\n",
    "     mars_facts_url='https://space-facts.com/mars/'\n",
    "     mars_fact_table=pd.read_html(mars_facts_url)\n",
    "\n",
    "     #Create Dataframe to store table data\n",
    "     df = mars_fact_table[0]\n",
    "     df.columns = ['Mars-Earth Comparison', 'Mars', 'Earth']\n",
    "     mars_facts = df.to_html()\n",
    "     mars_data['mars_facts'] = mars_facts\n",
    "     return mars_data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "def mars_hem():\n",
    "\n",
    "    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'\n",
    "    browser.visit(url4)\n",
    "    html4 = browser.html\n",
    "    soup4 = bs(html4, 'html.parser')\n",
    "    links = browser.find_by_css(\"a.product-item h3\")\n",
    "\n",
    "    hemisphere_image_urls = []\n",
    "\n",
    "    # First, get a list of all of the hemispheres\n",
    "    links = browser.find_by_css(\"a.product-item h3\")\n",
    "\n",
    "    # Next, loop through those links, click the link, find the sample anchor, return the href\n",
    "    for i in range(len(links)):\n",
    "        hemisphere = {}\n",
    "\n",
    "        # We have to find the elements on each loop to avoid a stale element exception\n",
    "        browser.find_by_css(\"a.product-item h3\")[i].click()\n",
    "\n",
    "        # Next, we find the Sample image anchor tag and extract the href\n",
    "        sample_elem = browser.find_link_by_text('Sample').first\n",
    "        hemisphere['img_url'] = sample_elem['href']\n",
    "\n",
    "        # Get Hemisphere title\n",
    "        hemisphere['title'] = browser.find_by_css(\"h2.title\").text\n",
    "\n",
    "        # Append hemisphere object to list\n",
    "        hemisphere_image_urls.append(hemisphere)\n",
    "\n",
    "        # Finally, we navigate backwards\n",
    "    browser.back()\n",
    "  \n",
    "    hemisphere_img_urls.append(img_data)\n",
    "    mars_data['hemisphere_img_urls']=hemisphere_img_urls\n",
    "\n",
    "    return mars_data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
