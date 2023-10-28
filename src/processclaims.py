import sys
import re
import os
import glob
import pandas as pd
import numpy as np

# Instance variables
claims_dict = {}
xml_counter = 0

def main():
  # create a pandas dataframe from csv with labels
  df = pd.read_csv('../data/applabels-2000-2012.csv')
  df.columns = ['doc-id','status']

  # get filepaths of all *.xml files 
  docspath = os.path.abspath(os.path.join(os.getcwd(), os.pardir))+'/data/docs2005'
  datapath = os.path.abspath(os.path.join(os.getcwd(), os.pardir))+'/data/split2005'
  csvpath = os.path.abspath(os.path.join(os.getcwd(), os.pardir))+'/data'

  # NEW CODE
  #split_xml(docspath, datapath)
  doc_files = glob.glob(os.path.join(docspath, '*.xml'))
  for file in doc_files:
     split_xml(file,output_directory=datapath)

  # Use glob to find all .xml files in the directory
  xml_files = glob.glob(os.path.join(datapath, '*.xml'))
  # Generate Claims dictionary
  for file in xml_files:
    # open xml file and search for doc id and claims
    f = open(file, 'rt', encoding = 'utf-8')
    id_matches = re.findall(r'<doc-number>(\w+)</doc-number>\n<date>',f.read())
    
    if id_matches:
      id_match = int(id_matches[0])
    else: 
      continue
    f.seek(0)
    claim_matches = re.findall(r'<claim-text>(.+)\n',f.read())
    
    # create a text file that combines all the claims, in order
    claimstext = ''
    for claim in claim_matches:
      claim = re.sub(r'<[^>]*>', '',claim)
      claimstext += claim

    # add the claims text to the claims dict
    if id_match not in claims_dict:
      claims_dict[id_match] = claimstext
  
  # Generate an ordered csv file with text (col0) to label (col1)
  df['claims'] = df['doc-id'].apply(lambda x: claims_dict.get(x,np.nan))

  # Create a filtered dataframe and save it to csv
  claims_df = df.dropna(subset=['doc-id','status','claims'])
  claims_df = claims_df.drop('doc-id',axis=1)
  ds_order = ['claims','status']
  claims_df = claims_df[ds_order]

  #check for null values
  print('CHECK1: prints value if there are null values:', claims_df.status.isnull().mean())

  # Save labeled dataset to csv
  csv_filename = csvpath+'/text_patentability_data.csv'
  claims_df.to_csv(csv_filename, index=False)
  print('CHECK2: verify claims is of type int64:',claims_df.status.dtype)
  print('CHECK3: distribution of each label:\n'+str(claims_df.status.value_counts()))

def split_xml(input_file, output_directory):
    global xml_counter
    with open(input_file, 'r', encoding='utf-8') as file:
        xml_content = file.read()

    xml_parts = xml_content.split('<?xml version="1.0" encoding="UTF-8"?>')
    
    xml_count = 0
    for i, part in enumerate(xml_parts):
        if part.strip():
            #xml_counter acts as offset, so we have unique filenames
            output_file = os.path.join(output_directory, f'split_{(xml_counter+i)}.xml')
            with open(output_file, 'w', encoding='utf-8') as out_file:
                out_file.write('<?xml version="1.0" encoding="UTF-8"?>' + part.strip())
                xml_count+=1
    xml_counter+=xml_count

if __name__ == '__main__':
    main()