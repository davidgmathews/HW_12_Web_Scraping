def scrape():
    from splinter import Browser
    from bs4 import BeautifulSoup
    import pandas as pd
    
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    headlines = soup.find_all('div', class_='content_title')
    paragraphs=soup.find_all('div',class_="article_teaser_body")
    
    latest_news_title=headlines[0].text
    latest_news_paragraph=paragraphs[0].text
    
    jpl_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    
    jpl_html=browser.html
    jpl_soup=BeautifulSoup(jpl_html,'html.parser')
    
    featured_image=jpl_soup.find_all('article')[0]
    url_start=featured_image['style'].index('url(')+5
    url_end=featured_image['style'].index(');')-1
    
    featured_image_url=f"https://www.jpl.nasa.gov{featured_image['style'][url_start:url_end]}"
    
    twitter_url='https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    
    twitter_html=browser.html
    twitter_soup=BeautifulSoup(twitter_html,'html.parser')
    
    mars_weather=f'''{twitter_soup.find_all('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text.split('pic')[0]} 
    {twitter_soup.find_all('a',class_='tweet-timestamp js-permalink js-nav js-tooltip')[0]['title']}'''
    
    tb_df=pd.read_html("https://space-facts.com/mars/")[0]
    tb_df.columns=['description','value']
    tb=tb_df.set_index('description').to_html()
    
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
    ]
    
    scrape_dict={'latest_news_title':latest_news_title,
                 'latest_news_paragraphs':latest_news_paragraph,
                 'featured_image_url':featured_image_url,
                 'mars_weather':mars_weather,
                 'table_html':tb,
                 'hemisphere_image_urls':hemisphere_image_urls
                }
    return scrape_dict
    
