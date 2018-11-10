import time 
import re
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options  


# a lazy wrapper function
def scrape(username, verbose=False):
    
    chrome_options = Options()  
    chrome_options.add_argument("window-size=900,900")
    
    chrome_options.add_argument("--headless")  
    
    # if this is wrong, run $which chromium-browser
    chrome_options.binary_location = "/usr/bin/chromium-browser"
    
    # just download the binary and put it in the working directory
    driver = webdriver.Chrome(executable_path="./chromedriver",
                              options=chrome_options)
    
    driver.get("https://www.instagram.com/"+username)
    
    # get amount of posts.
    postnum_xpath = '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/a'
    postnum_elem = driver.find_element_by_xpath(postnum_xpath)
    postnum = postnum_elem.get_attribute("innerText");
    
    postnum = postnum.replace(",","")
    postnum = postnum.replace(" ","")
    
    p = re.compile('\d+')
    postnum = int(p.match(postnum)[0])
    if(verbose):
        print(str(postnum) + " total posts")
    
    rows_xpath = '//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div'
    #rows_elem = driver.find_element_by_xpath(rows_xpath)
    
    #-------------------------------------------------
    # Unused, not needed if you can debug in headed mode
    def dump_screenie(n):
        element = driver.find_element_by_tag_name('body')
        element_png = element.screenshot_as_png
        with open("./debug_pics/last"+str(n)+".png", "wb") as file:
            file.write(element_png)
        print("screenshot written to last"+str(n)+".png")
    
    
    #-------------------------------------------------    
    
    # So, we update the dictionary every time regardless of whether or not 
    # the image is unique.
    def update_data(new_elem, data):
        imgs = new_elem.find_elements_by_tag_name("img")
        
        for i in range(0,len(imgs)):
            img = imgs[i]
            img_id = img.get_attribute("src")
            content = img.get_attribute("alt")
            data[img_id] = content
            
        return data;
        
    def scroll_bottom():
        
        children_xpath = rows_xpath + "/*"
        data = {}
        SCROLL_PAUSE_TIME = 1.0
        # an estimate
        TIME_PER_QUERY = 0.25
        # When a query fails, wait this amount of extra seconds
        BACKOFF_TIME = 5
        
        # Get scroll height
        extra_wait = 0
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        # 12 posts per query, SCROLL_PAUSE_TIME seconds per pause
        estimate = (postnum/12)*(SCROLL_PAUSE_TIME + TIME_PER_QUERY)
        if(verbose):
            print("Estimate: " + str(estimate) + " seconds.")
        
        extra_wait = 0
        
        # set data dictionary to first page
        children = driver.find_elements_by_xpath(children_xpath)
        for i in range(0, len(children)):
            data = update_data(children[i], data)

        while True:
            
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            time.sleep(extra_wait)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")


            # update data
            children = driver.find_elements_by_xpath(children_xpath)
            for i in range(0, len(children)):
                data = update_data(children[i], data)


            
            if (len(data) == postnum):
                if(verbose):
                    print("Success")
                break
            else:
                if(verbose):
                    print(str(len(data)) + "/" + str(postnum))
                    
            # Go slower when the last query didn't get a response
            if(last_height == new_height):
                if(verbose):
                    print("Didn't refresh in time, moving too fast?")
                if(extra_wait <= 55):
                    extra_wait = extra_wait + BACKOFF_TIME
                else:
                    # TODO: Give up and throw exception here. 
                    print("Error: instagram request failed.")

            else:                
                if(extra_wait > SCROLL_PAUSE_TIME):
                    if(verbose):
                        print("Request successful, lowering extra_wait time")
                    extra_wait = extra_wait - BACKOFF_TIME
        
            last_height = new_height
            
        driver.close()
        return data
    
    return scroll_bottom()
    

data = scrape("modenesegiorgia")
        
#-------------------------------------------------
