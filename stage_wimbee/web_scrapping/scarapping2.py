from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep 
import pandas as pd
from selenium.webdriver.chrome.options import Options
import Levenshtein


driver = webdriver.Chrome()



def informations_of_the_job(liste_of_all_societies):



#    wait = WebDriverWait(driver , 10)
 
    result1 = []    
    result2 = []
    for society in liste_of_all_societies : 
        driver.get("https://annuaire-entreprises.data.gouv.fr")





        search_field = driver.find_element(By.XPATH ,'//div[@id="search-input--lg"]//input' )
        search_field.send_keys(society)
        search_field.send_keys(Keys.ENTER)

        nodes = driver.find_elements(By.XPATH , '//div[@class ="jsx-240357328 result-item"]')

        titres = []

        sous_categories = []
        for i in nodes : 

            titre = i.find_element(By.XPATH , './/div[1]/span[@class = "jsx-240357328"]')
            titres.append(titre.text)
         



            sous_categorie = i.find_element(By.XPATH , './/div[2]')
            sous_categories.append(sous_categorie.text)
        if(len(titres)):
            final_soc  = final_society(titres , sous_categories , society)


            link = nodes[titres.index(final_soc)].find_element(By.XPATH , './/a[@class="jsx-240357328 result-link no-style-link"]')
            link.click()
            table1 = driver.find_elements(By.XPATH , '//div[@id = "entreprise"]//div[1]//tr')
       
            d = {}
            for  i in table1 :
                d[i.find_element( By.XPATH,".//td[1]").text] = i.find_element(By.XPATH, ".//td[2]").text
            d['nom_societe'] = society
            sorted_dict_1 = dict(sorted(d.items()))
            result1.append(sorted_dict_1)
            


    
            donnes_financieres = driver.find_element(By.XPATH , '//div[@class = "jsx-911246288 title-tabs"]//a[4]')
            donnes_financieres.click()
        
            rows = driver.find_elements(By.XPATH , '//table[@class="jsx-2305131526 full-table"]//tr')
            cells = driver.find_elements(By.XPATH  ,'//table[@class="jsx-2305131526 full-table"]//tr//td')
            nb_culumns = int(len(cells) / (len(rows)-1))
            #print(nb_culumns)
            if (nb_culumns == 0 ):
                print("there is no financial elements for the society " , final_soc)
            else : 
                all_culumns = []
                for p in range(nb_culumns):
                    culumns = []
                    for k in range(p,len(cells),nb_culumns) :
                        culumns.append(cells[k].text)
                    all_culumns.append(culumns)
                #print(all_culumns)
        
                
                liste1 = all_culumns[0]
                for  i in range(1,len(all_culumns)) : 
                    d1={}
                    for  j in range(len(all_culumns[i])) : 
                        d1[liste1[j]]= all_culumns[i][j]
                    #print(d1)
                    
                    id = driver.find_element(By.XPATH , '(//div[@class="jsx-5067d4f31f099298 title"]//div[1]//span[2])[3]').text
                    d1["id"] = id
                    list_of_headers = ["SALAIRE","TYPE DE CONTRAT","ADRESSE","DATE DE PUBLICATION","TAILLE DE LA SOCIÉTÉ","SECTEUR","SITE WEB","description","DATE DE CRÉATION","AVANTAGES SOCIAUX EMPLOYÉ"]
                    for i in list_of_headers:
                        if (i not in d1.keys()):
                            d1[i] = None


                    sorted_dict_2 = dict(sorted(d1.items()))
                    result2.append(sorted_dict_2)


            
        else :

            print("there is no results for the society " ,society )

    print(result2)
    df2 = pd.DataFrame(result2)
    df2.to_csv('donnees_financieres.csv')
#    print(result1)
    df1 =  pd.DataFrame(result1)
    df1.to_csv('fiche_tech.csv')
    
            

# determiner la societe la plus adequate apres un recherhe de tous les soceitees disponible avec la technique de levenstein qui permet de mesurer la distance entre le plus proche nom du societé de tous les autre noms apparu dans la recherche 


def final_society (titres , sous_categories , job):
    distances = []
    for i in titres : 
        distances.append(Levenshtein.distance(job.upper(), i.upper()))
    

    keys = ["informatique" , "consulting" , "logiciels" , "developpement"  , "data"]
    result = []
    for  i in sous_categories : 
       
        somme = 0 
        final_somme = 0
        tokens = i.split(" ")
        for  j in keys :
            for t in tokens:
                somme+= Levenshtein.distance(j.upper(), t.upper())
        somme = somme/ len(keys) / len(tokens)
        final_somme = somme + distances[sous_categories.index(i)]
        result.append(final_somme)
    

 
    final_sc = titres[result.index(min(result))]
    return final_sc





informations_of_the_job([ "business and decision","bi"," dfl;d","wimbee","sofrecom"])

