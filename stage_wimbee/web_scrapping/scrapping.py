from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep 
import pandas as pd
from selenium.webdriver.chrome.options import Options
from datetime import date
import random 
import string 
import uuid 


driver = webdriver.Chrome()
#latitude = 30.2409
#longitude = 7.5239      
#chrome_options = Options()

#chrome_options.add_argument(f'--geolocation={latitude},{longitude}')



wait = WebDriverWait(driver, 10)

def web_scrapp(domains, countries ):
    driver.get('https://www.monster.fr')
    #sleep(10)
    driver.implicitly_wait(10) # seconds
    
    search_button0 = driver.find_element(By.XPATH , '//button[@id="onetrust-accept-btn-handler"]')
    driver.implicitly_wait(10) # seconds
    search_button0.click()

    for domain in domains : 
        for country in countries :
            


            search_field = driver.find_element(By.XPATH,'//div[@class="SearchBar ds-search-bar"]//form/div[1]/div[1]//input')
           

            search_field.send_keys(domain)
        
            #search_field.send_keys(Keys.ENTER)
            recherche_button = driver.find_element(By.XPATH ,'//button[@class= "sc-kdBSHD bsjaSf sc-eIcdZJ jXQbWb ds-button"]')
            recherche_button.click()
      
            url  = driver.current_url
            #print(url)
            pieces1 = url.split('page=1')
            new_url1  =pieces1[0]+"page=1&rd=100"+pieces1[1]
           
            pieces2 = url.split("where=")
            pieces21 = pieces2[1].split("&page=1")
            res = []
            for i in range(4):
                last_url= pieces2[0]+"where="+country+"&page="+str(i+1)+"&rd=100"+pieces21[1]
                sleep(10)
                
                driver.get(last_url)
                

    #faire la filtration 
    #        filter_button = driver.find_element(By.XPATH , '//button[contains(@class,"search-filter-barstyle__FilterBarButton-sc-10nmm15-3")]')
    #        filter_button.click()
        
    #        radio_bottom = driver.find_element(By.XPATH , '//div[@class="search-filter-barstyle__FiltersGrid-sc-10nmm15-6 cVMcUx"]//fieldset[3]//div[@class="search-filter-barstyle__InputsGrid-sc-10nmm15-7 iRGMfL"]//div[4]//span')
    #        radio_bottom.click()
    #        result_buttton = driver.find_element(By.XPATH , '//button[@class="sc-kdBSHD gPaifr modalstyles__ModalViewResults-sc-1vno8zf-9 bqbjQd ds-button"]')
    #        result_buttton.click()



                path = "//section//ul//li//article"
                
                try : 
                    wait.until(EC.presence_of_all_elements_located((By.XPATH, path)))
                    desc = driver.find_elements(By.XPATH ,path)
#               sleep(10)
#                driver.implicitly_wait(3)
                except : 
                    desc = []
                    break
                
                if (len(desc) ==0 ):
                    print("there is no more jobs for " , domain)
                    break
                

                
                else : 

                    list = []
                    keys = []
                    description = []
                    keys1 = []
                    keys2 = []
                    desc_text = []
                    for  i in desc : 
                        desc_text.append(i.text)
                    if (desc_text == []): 
                        driver.close()
                    else : 
                        for elem in desc : 
                            
                            #list.append(elem.text)
                            #print(elem.text.split('\n'))
                            elem.click()
                            keys_desc = driver.find_element(By.XPATH,'//div[@id="details-table"]')
                            keys.append((keys_desc.text))
                            keys1_desc = driver.find_elements(By.XPATH , '//div[@class="detailsstyles__DetailsTableDetailHeader-sc-1deoovj-4 jdSCow"]')
                            for i in keys1_desc : 

                                keys1.append(i.text)

                            keys2_desc = driver.find_elements(By.XPATH , '//div[@class ="detailsstyles__DetailsTableDetailBody-sc-1deoovj-5 kMXVwq"]')


                            for  i in keys2_desc : 
                                keys2.append(i.text)
                            
                            row_desc = driver.find_elements(By.XPATH ,'//div[@class ="detailsstyles__DetailsTableRow-sc-1deoovj-2 gGcRmF"]')
                    

                            description_desc = driver.find_element(By.XPATH, '//div[@class="descriptionstyles__DescriptionBody-sc-13ve12b-4 crOoVX"]')
                            description.append(description_desc.text)
                            sorted_dict_1 = {}
                            d = {}
                            for  i in row_desc :
                                #d[i.find_element( By.XPATH,"div[1]").text] = i.find_element(By.XPATH, "div[2]").text
                                a = i.find_element( By.XPATH,"div[1]").text
                                b= i.text.replace(a , "")
                                d[a]=b
                            today = date.today()
                            d['current_date'] = today
                            d['job_id'] = uuid.uuid4()
                            d['job_title'] = elem.find_element(By.XPATH , ".//div[2]//div[1]//h3//a").text
                            d['description'] = description_desc.text
                            d['domain'] = domain 
                            #d['nom_societe'] = elem.text.split('\n')[1]
                            d['nom_societe'] = elem.find_element(By.XPATH , '//h2[@class ="headerstyle__JobViewHeaderCompany-sc-1ijq9nh-6 iWixRE"]').text
                            
                            
                            list_of_headers = ["nom_societe" , "domain" , "SALAIRE","TYPE DE CONTRAT","ADRESSE","DATE DE PUBLICATION","TAILLE DE LA SOCIÉTÉ","SECTEUR","SITE WEB","description","DATE DE CRÉATION","AVANTAGES SOCIAUX EMPLOYÉ","AUTRE RÉMUNÉRATION" , "job_id","job_title","SIÈGE SOCIAL"] 
                            for header in list_of_headers:
                                if (header not in d.keys()):
                                    d[header] = None
      


                            sorted_dict_1 = dict(sorted(d.items()))
                            #print(d)
                            res.append(sorted_dict_1)
              
            directory = os.getcwd()
            monster = directory+'\web_scrapping\monster_fr'
            os.makedirs(monster, exist_ok=True)

            df = pd.DataFrame(res)
            #df.to_csv('bi.csv')
            df.to_csv(monster+'\\'+domain+".csv", mode="w")
                    
                    #print(df)
            driver.get('https://www.monster.fr')


def generate_password(length)  :
    password = ''.join(random.choice(string.printable) for i in range(length))
    return password





web_scrapp(["bi"], ["france"])
#".net", "bi", "react", "data science","node js","java","c#","python","cloud","microsoft"