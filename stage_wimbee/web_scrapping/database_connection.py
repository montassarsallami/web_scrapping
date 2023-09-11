

# imports
import spacy
from spacy.matcher import PhraseMatcher
from deep_translator import GoogleTranslator
from skillNer.cleaner import Cleaner
import math
# load default skills data base
from skillNer.general_params import SKILL_DB
import os 
import pandas as pd
# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor
import pyodbc

def translation_over_5000(text):
    num_segments = math.ceil(len(text) / 4000)
    segments = [text[i * 4000:(i + 1) * 4000] for i in range(num_segments)]

#    translated_segments = []
#    for segment in segments:

 #       input_en = tr.translate(segment,src="fr",dest="en")

  #      cleaned = cleaner(input_en)
   #     res_annot = skill_extractor.annotate(cleaned,0.99)
    #    nl_result = nlp(cleaned)
    #    skill_extractor.describe(res_annot)
    #    keys = [k["doc_node_value"] for k in res_annot["results"]["full_matches"] + res_annot["results"]["ngram_scored"]] 
    #    translated_segments += keys
    return segments









# init params of skill extractor
nlp = spacy.load("en_core_web_lg")
# init skill extractor
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

cnxn = pyodbc.connect('DRIVER={SQL Server};Server=montassar123;Database=TutorialDB;Port=3306;User ID=sa;Password=monta ')
cursor = cnxn.cursor() 
cursor.execute('SELECT * from monster')
# extract skills from job_description
job_description = """
You are a Python developer with a solid experience in web development
and can manage projects. You quickly adapt to new environments
and speak fluently English and French
"""

annotations = skill_extractor.annotate(job_description)

tr = GoogleTranslator(source='fr', target='en')
all_keys  = []
MAX_TEXT_LENGTH = 5000
cleaner = Cleaner(
                to_lowercase=True,
                include_cleaning_functions=["remove_punctuation", "remove_extra_space"]
            )






i = 0

res = []
for row in  cursor : 
    d = {}
    
    


    try : 
        
            
            
            
             
            input_en = tr.translate(row.description,src="fr",dest="en")
            #print(input_en)  
            cleaned = cleaner(input_en) 
            res_annot = skill_extractor.annotate(cleaned,0.99)
            nl_result = nlp(cleaned)
            skill_extractor.describe(res_annot)
             
            keys = [k["doc_node_value"] for k in res_annot["results"]["full_matches"] + res_annot["results"]["ngram_scored"]] 
            print("**************************************************" , i)
            i+=1
            
            d['skills'] = " ".join(keys)
            d['job_id'] = row.job_id
            res.append(d)
            print(d)
            #print(res)
            
    except : 
        
            translated_segments = []
            for segment in translation_over_5000(row.description):
                

                

                input_en = tr.translate(segment,src="fr",dest="en")
                #print(input_en)

                cleaned = cleaner(input_en)
                res_annot = skill_extractor.annotate(cleaned,0.99)
                nl_result = nlp(cleaned)
                skill_extractor.describe(res_annot)
                keys = [k["doc_node_value"] for k in res_annot["results"]["full_matches"] + res_annot["results"]["ngram_scored"]] 
                translated_segments += keys
            
                 
             
            print("the translated segment is " , translated_segments)
            d['skills']  = " ".join(translated_segments)
            d['job_id'] = row.job_id
            res.append(d)
            #print(res)

            
directory = os.getcwd()
monster = directory+'\web_scrapping\monster_fr'
os.makedirs(monster, exist_ok=True)

df = pd.DataFrame(res)
            #df.to_csv('bi.csv')
df.to_csv(monster+'\\skills.csv', mode="w")
