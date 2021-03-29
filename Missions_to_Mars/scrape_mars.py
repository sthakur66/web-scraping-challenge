# import dependencies
from bs4 import BeautifulSoup as bs
import os
import requests
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    browser = init_browser()

    ###############################################   NASA Mars News   ###############################################

    url ="https://mars.nasa.gov/news/"

    # open the url
    # browser.visit(url)
    response = requests.get(url)

    # create html to parse
    #html = browser.html
    

    # create soup object to parse html
    #soup = bs(html, "html.parser")
    soup = bs(response.text, 'html.parser')

    # Use below variables to create dictionary
    news_title = soup.find("div", class_="content_title").a.text
    paragraph = soup.find("div", class_="rollover_description_inner").text



    ####################################   JPL Mars Space Images - Featured Image    #################################

    jpl_url ="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"

    # open the url
    browser.visit(jpl_url)

    # create html to parse
    html = browser.html

    # create soup object to parse html
    soup = bs(html, "html.parser")

    # use beautifulsoup to navigate to the image
    image = soup.find("img", class_="headerimage fade-in")['src']

    # Use below variable to create dictionary
    # create the url for the image
    featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + image 



    ###########################################   Mars Facts    ######################################################

    mars_url = 'https://space-facts.com/mars/'

    # Use panda's to get the tabular data from page
    table = pd.read_html(mars_url)

    # convert table to pandas dataframe
    mars_df = table[0]

    # rename the columns
    mars_df.columns=["Description", "Mars"]

    # reset the index for the df
    mars_df.set_index("Description", inplace=True)

    # convert dataframe to an html table string
    html_table = mars_df.to_html(justify='left')




    ####################################   Mars Hemispheres    #########################################################

    hemi_url ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # open the url
    browser.visit(hemi_url)

    # create html to parse
    html = browser.html

    # create soup object to parse html
    soup = bs(html, "html.parser")

    # use beautifulsoup to navigate to the main class
    results = soup.find_all("div", class_="item")

    hemisphere_image_urls = []

    # loop through image data to find title and url info
    for result in results:
        
        # get the title
        title = result.find("h3").text
        
        # get the image url
        img_url = result.a["href"]
        
        # visit the image url page to get full image
        main_img_url = "https://astrogeology.usgs.gov" + img_url
        
        # use requests to get full images url 
        response = requests.get(main_img_url)
        
        # create soup object
        soup = bs(response.text,"html.parser")
        
        # find full image url
        new_url = soup.find("img", class_="wide-image")["src"]
        
        # create full image url
        full_img_url = "https://astrogeology.usgs.gov" + new_url
        
        # make a dict and append to the list
        hemisphere_image_urls.append({"title": title, "img_url": full_img_url})

    

    
    # create mars data dictionary to hold data
    mars_data = {
        "news_title": news_title,
        "paragraph" : paragraph,
        "featured_image_url": featured_image_url,
        "html_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }



    # Quit the browser
    browser.quit()



    # Return the results
    return mars_data
