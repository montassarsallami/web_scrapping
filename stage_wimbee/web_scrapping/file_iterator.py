import os 
import pandas as pd


directory  = os.getcwd()+'\web_scrapping\monster_fr'
monster_V2 = os.getcwd()+'\web_scrapping\monster_fr_v2'
os.makedirs(monster_V2, exist_ok=True)
for filename in os.listdir(directory) : 
    domain_name = filename.replace('.csv', '')
    
    csv_file = os.path.join(directory, filename)
    
    df = pd.read_csv(csv_file)
    new_df = df.assign(Domain = domain_name)

    
    #new_df.to_csv(monster_V2+'\\'+domain_name+'.csv', mode="w")
    
