import sys
import re
import os
import glob
import pandas as pd
import numpy as np

def main():
    # specify datatype

    # read the PatEx data into a dataframe
    datatypes = {
        'application_number':'int64',
        'filing_data': 'datetime64',
        'examiner_id': 'int64',
        
    }
    info_df = pd.read_csv('../data/application_data.csv')

    for column in info_df:
        print('column name:', column)
        #print('column type:', column.unique())

    #info_df = pd.read_csv('../data/application_data.csv',dtype=datatypes)

    # create a dataframe with only certain columns
    # check that you have data generated for the correct years
    # iterate through the dataframe (practice lambda expressions) to generate metadata features
    
    print('info_df read, with specified datatypes.')

if __name__ == '__main__':
    main()