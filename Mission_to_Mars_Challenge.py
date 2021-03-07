#!/usr/bin/env python
# coding: utf-8

# In[21]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup

from webdriver_manager.chrome import ChromeDriverManager


# In[22]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[23]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[24]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[25]:


slide_elem.find("div", class_='content_title')


# In[26]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[27]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images

# In[29]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[30]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[31]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[32]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[33]:


# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# In[34]:


import pandas as pd
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[35]:


df.to_html()


# In[36]:


# Scrape the photos of Mars Hemispheres
# Visit the site
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[37]:


html = browser.html
first_soup = soup(html, 'html.parser')
first = first_soup.find('div', class_="collapsible results")
items = first.find_all('div', class_="item")
items


# In[38]:


hemispheres = []
for item in items:
    x = item.find("h3").text
    hemispheres.append(x)
hemispheres


# In[42]:


hemi_data = []

for hemi in hemispheres:
        browser.visit(url)
        browser.is_element_present_by_text(hemi, wait_time=1)
        enhanced_image_elem = browser.links.find_by_partial_text(hemi)
        enhanced_image_elem.click()
        
        html = browser.html
        hemi_soup = soup(html, 'html.parser')
       
        hemi_url = hemi_soup.find("a", text="Original").get("href")
        hemi_title = hemi_soup.find("h2", class_="title").text
        hemi_dict = {'title':hemi_title, 'img_url': hemi_url}
       
    # append to list of dictionaries
        hemi_data.append(hemi_dict)
hemi_url


# In[43]:



hemi_data


# In[44]:


def hemisphere_images(browser):
    # declare the variable that will contain a list of dicts having the title and urls appended 
    hemi_data = []

    # Scrape the photos of Mars Hemispheres
    # Visit the site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    # Convert the browser html to a soup object 
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    
    # Go to parent div & grab all 4 hemisphere info
    hemis = hemi_soup.find('div', class_="collapsible results")
    items = hemis.find_all('div', class_="item")
    
    # loop thru items to get a list of hemisphere names then use to find click path to enhanced 
    hemispheres = []
    for item in items:
        x = item.find("h3").text
        hemispheres.append(x)

    # Go to each hemisphere page, one at a time
    for hemi in hemispheres:
        browser.visit(url)
        browser.is_element_present_by_text(hemi, wait_time=1)
        enhanced_image_elem = browser.links.find_by_partial_text(hemi)
        enhanced_image_elem.click()
        
        # Convert the browser html to a soup object 
        html = browser.html
        hemi_soup = soup(html, 'html.parser')

        # get title of enhanced image
        hemi_title = hemi_soup.find("h2", class_="title").text
        # get url of enhanced image
        hemi_url = hemi_soup.find("a", text="Original").get("href")
        # append to dictionary
        hemi_dict = {'title':hemi_title, 'img_url': hemi_url}
        # append to list of dictionaries
        hemi_data.append(hemi_dict)
        # return list of dictionaries
        return hemi_data


# In[ ]:




