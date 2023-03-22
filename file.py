from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By

driver = webdriver.Chrome('./chromedriver')


url="https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"





def get_result_data(url,place_id=None):

    driver.get(url)

    time.sleep(5)
    result_data = pd.DataFrame(columns=["url", "name", "price", "rating", "no. of reviews","description","ASIN","product description","manufacturer"])

    pg_cnt=1
    


    driver.maximize_window()
    # cnt=0
    next_page_link=""


    while pg_cnt<21 :    

        next_page_link=""
        cnt=0
        while cnt!=-1:

            data={
                "url" :"",
                "name": "",
                "price": "",
                "rating": "",
                "no. of reviews": "",
                "description":"",
                "ASIN":"",
                "product description":"",
                "manufacturer":""
                
            }


            try:
                product = driver.find_element("xpath",f'.//div[@data-cel-widget="search_result_{cnt}"]')
                
                
                try:

                    get_url = driver.find_element('xpath',f'.//div[@cel_widget_id="MAIN-SEARCH_RESULTS-{cnt}"]//div[@class="a-section a-spacing-none puis-padding-right-small s-title-instructions-style"]/h2/a').get_attribute("href")
                    get_name = driver.find_element('xpath',f'.//div[@cel_widget_id="MAIN-SEARCH_RESULTS-{cnt}"]//div[@class="a-section a-spacing-none puis-padding-right-small s-title-instructions-style"]/h2/a/span').get_attribute("innerHTML")
                    get_price= driver.find_element('xpath',f'.//div[@cel_widget_id="MAIN-SEARCH_RESULTS-{cnt}"]//span[@class="a-price"]//span[@class="a-offscreen"]').get_attribute("innerHTML")
                    get_rating=driver.find_element('xpath',f'.//div[@cel_widget_id="MAIN-SEARCH_RESULTS-{cnt}"]//span[@class="a-size-base"]').get_attribute("innerHTML")
                    get_reviews=driver.find_element('xpath',f'.//div[@cel_widget_id="MAIN-SEARCH_RESULTS-{cnt}"]//span[@class="a-size-base s-underline-text"]').get_attribute("innerHTML")



                    data["url"]=get_url
                    data["name"]=get_name
                    data["price"]=get_price
                    data["rating"]=get_rating
                    data["no. of reviews"]=get_reviews



                    # ///////////////////////////////////// ( GETTING DETAILS OF SPECIFIC PRODUCTS ) //////////////
                    # /////////////////////////// ( PART 2 ) //////////////////////////////////////////////////////

                    try :
                        page= driver.find_element('xpath',f'.//div[@cel_widget_id="MAIN-SEARCH_RESULTS-{cnt}"]//div[@class="a-section a-spacing-none puis-padding-right-small s-title-instructions-style"]/h2/a')
                        driver.execute_script("arguments[0].click()",page)
                        time.sleep(6)
                        chwd = driver.window_handles

                        driver.switch_to.window(chwd[1])
                        leave=3

                        pre_height=0
                        new_height=0;    
                        while leave>0 :

                            try:
                                if data["manufacturer"]=="":
                                    manufacturer = driver.find_element('xpath',f'//div[@id="detailBullets_feature_div"]//li[3]/span/span[2]').get_attribute("innerHTML")
                                    data["manufacturer"]=manufacturer
                                    leave=leave-1
                            except:
                                pass
                            
                            try:
                                if data["ASIN"]=="" :
                                    asin = driver.find_element('xpath',f'//div[@id="detailBullets_feature_div"]//li[4]/span/span[2]').get_attribute("innerHTML")
                                    data["ASIN"]=asin
                                    leave=leave-1
                            except:
                                pass
                            
                            try:
                                if data["product description"]=="":
                                    productDesc =driver.find_element('xpath',f'//div[@id="productDescription"]//span').get_attribute("innerHTML")
                                    data["product description"]=productDesc
                                    data["description"]=productDesc
                                    leave=leave-1
                            except:
                                pass

                            driver.execute_script("window.scrollBy(0,250)") 

                            new_height= driver.execute_script("return document.body.scrollHeight")
                            if pre_height < new_height:
                                pre_height=new_height
                            else:
                                break

                        driver.close()
                        driver.switch_to.window(chwd[0])
                    
                    except:
                        pass

                    # //////////////////////////////////////////////////////////////////////////////////////////////////
                    # //////////////////////////////////////////////////////////////////////////////////////////////////


                    result_data=result_data.append(data,ignore_index=True, sort=False)

                except:
                    pass
                    
                
                driver.execute_script("arguments[0].scrollIntoView(true);",product) 
                cnt=cnt+1

                # if result_data.size>0 :
                #    break

                try:
                    next_page_link=driver.find_element('xpath',f'.//a[@aria-label="Go to next page, page {pg_cnt+1}"]').get_attribute("href")
                except:
                    pass


            except:
                cnt=-1

        pg_cnt=pg_cnt+1

        if pg_cnt<21 and next_page_link!="" :
            driver.get(next_page_link)
            time.sleep(3)
        else :
            break





    result_data.to_csv('result_data.csv', index=False)      
    # result_data.to_excel('result_data.xlsx', index=False)      


get_result_data(url)



