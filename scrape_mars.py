#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
import datetime as dt
from selenium import webdriver

   
def scrape():
  # Initiate headless driver for deployment
  executable_path = {"executable_path": "chromedriver"}
  browser = Browser("chrome", **executable_path, headless = True)
  news_title, news_paragraph = mars_news(browser)

  # Run all scraping functions and store in dictionary.
  data = {
    "news_title": news_title,
    "news_paragraph": news_paragraph,
    "featured_image": featured_image(browser),
    "hemispheres": hemispheres(browser),
    "weather": mars_weather(browser),
    "facts": mars_facts(),
  }

  # Stop webdriver and return data
  browser.quit()

  return data

def mars_news(browser):
  nasa = "https://mars.nasa.gov/news/"    
  browser.visit(nasa)
  time.sleep(2)

  # Get first list item and wait half a second if not immediately present
  browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)


  html = browser.html
  soup = bs(html,"html.parser")

  try:
    slide_elem = soup.select_one("ul.item_list li.slide")
    #scrapping latest news about mars from nasa
    news_title = slide_elem.find("div",class_="content_title").get_text()
    news_paragraph = slide_elem.find("div", class_="article_teaser_body").get_text()
  
  except AttributeError:
    return None, None

  return news_title, news_paragraph

def featured_image(browser):    
    #Mars Featured Image
    nasa_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
    browser.visit(nasa_image)
    time.sleep(2)

    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(nasa_image))
    
    xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"

    #Use splinter to click on the mars featured image
    #to bring the full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()
    time.sleep(2)
    
    #get image url using BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    try:
      img_url = soup.find("img", class_="fancybox-image")["src"]
    except AttributeError:
      return None

    full_img_url = base_url + img_url
    return full_img_url
    
# #### Mars Weather
def mars_weather(browser):

  #get mars weather's latest tweet from the website
  url_weather = "https://twitter.com/marswxreport?lang=en"
  browser.visit(url_weather)
  html_weather = browser.html
  soup = bs(html_weather, "html.parser")
  mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()
  return mars_weather


# #### Mars Hemisperes  
def hemispheres(browser):


  url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

  browser.visit(url)

    # Click the link, find the sample anchor, return the href
  hemisphere_image_urls = []
  for i in range(4):

    # Find the elements on each loop to avoid a stale element exception
    browser.find_by_css("a.product-item h3")[i].click()

    hemi_data = scrape_hemisphere(browser.html)

    # Append hemisphere object to list
    hemisphere_image_urls.append(hemi_data)

    # Finally, we navigate backwards
    browser.back()

  return hemisphere_image_urls
  
def scrape_hemisphere(html_text):

  # Soupify the html text
  hemi_soup = bs(html_text, "html.parser")

  # Try to get href and text except if error.
  try:
      title_elem = hemi_soup.find("h2", class_="title").get_text()
      sample_elem = hemi_soup.find("a", text="Sample").get("href")

  except AttributeError:

      # Image error returns None for better front-end handling
      title_elem = None
      sample_elem = None

  hemisphere = {
      "title": title_elem,
      "img_url": sample_elem
  }

  return hemisphere

# #### Mars Facts
# Visit Mars facts url
def mars_facts():
  try: 
    url_facts = "https://space-facts.com/mars/"
    # Use Panda's `read_html` to parse the url
    table = pd.read_html(url_facts)[0]
  except BaseException:
    return None

  # Assign the columns `['Parameter', 'Value']`
  table.columns = ["Parameter", "Values"]
  table.set_index(["Parameter"], inplace = True)

  # Add some bootstrap styling to <table>
  return table.to_html(classes="table table-striped")

  


if __name__ == "__main__":

  # If running as script, print scraped data
  print(scrape())
