### Import Dependancies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():   
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # LATEST MARS NEWS SCRAPE -------------------------------------------------------
    #latest news scrape source
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)
    
    #extract html and parse with beautifulsoup
    news_html = browser.html
    news_soup = bs(news_html, "html.parser")

    # extract all title containers from the Mars news pages
    results = news_soup.find_all('div', class_='list_text')

    #define articles list
    articles = []
    story = {}
    
    # loop thru results and create a dic for the latest 4 mars stories
    # add each story to the articles list and print 
    for item in results[:4]:
        story = {}
        story["headline"] = item.find('div',class_="content_title").get_text()
        story["tagline"] = item.find("div", class_="article_teaser_body").get_text()
        articles.append(story)

    print('News scraped successfully.----------------------')
       
    # HEMI SCRAPE -------------------------------------------------------   
    #hemisphere images scrape source
    hemi_url = "https://marshemispheres.com/"
    browser.visit(hemi_url)

    #extract html and parse with beautifulsoup
    hemi_html = browser.html
    hemi_soup = bs(hemi_html, "html.parser")

    # extract all title containers from the Mars news pages
    hemi_results = hemi_soup.find_all('div', class_='description')

    #list to hold the images and titles.
    hemispheres = []

    # loop thru results and create a dic for the latest 4 mars stories
    # add each story to the articles list and print 
    for item in hemi_results[:4]:
        mars = {}
        mars['title'] = item.find('h3').get_text().replace(' Enhanced','')
        browser.click_link_by_partial_text(mars['title'])
        html=browser.html
        soup=bs(html,'html.parser')
        mars['image_src'] = (hemi_url + soup.find('li').a['href'])
        browser.back()
        hemispheres.append(mars)
    
    print('Hemispheres scraped successfully.----------------------')
    
    # FEATURED IMAGE SCRAPE ------------------------------------------------------- 
    #hemisphere images scrape source
    jpl_url = "https://spaceimages-mars.com/"
    browser.visit(jpl_url)
    
    #extract html and parse with beautifulsoup
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, "html.parser")

    featured_img_url = jpl_url + jpl_soup.find(class_='floating_text_area').a['href']
    
    print('Image of the Day scraped successfully.----------------------')

    # TABLE SCRAPE -------------------------------------------------------
    #hemisphere images scrape source
    table_url = "https://galaxyfacts-mars.com/"
    browser.visit(table_url)

    #extract html and parse with beautifulsoup
    table_html = browser.html
    table_soup = bs(table_html, "html.parser")
    
    table_src = pd.read_html(table_url)
    table_df = table_src[0]
    table_df = table_df.set_index([0])
    table_df = table_df.rename(columns={1 : "Mars", 2: "Earth"})
    table_df = table_df.drop(index='Mars - Earth Comparison')
    
    html_table = table_df.to_html(index_names=False, justify='left',
                                  classes='table table-responsive-sm table-danger table-hover')
    
    print('Table scraped successfully. ----------------------')

    # quit the browser
    browser.quit()
    
    # RETURN DATA  -------------------------------------------------------
    mars_data = {
        'featured_img_url': featured_img_url,
        'hemispheres': hemispheres,
        'articles': articles,
        'table': html_table   
    }
    
    return mars_data