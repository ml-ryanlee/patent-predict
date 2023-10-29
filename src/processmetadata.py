import sys
import re
import os
import glob
import pandas as pd
import numpy as np

# counters, global variables
examiner_id_counter = {}
examiner_allowance_counter = {}
class_counter = {}
subclass_counter = {}
customer_id_counter = {}
customer_patent_counter = {}

def main():
    info_df = pd.read_csv('../data/application_data.csv')
    info_df = info_df[['application_number','filing_date','examiner_id','uspc_class',
                   'uspc_subclass','customer_number','disposal_type']]
    
    info_df = preprocess(info_df)
    info_df.to_csv('../data/post_application_data.csv', index=False)
    
    meta_df = extract_metadata(info_df)
    meta_df.to_csv('../data/application_metadata.csv', index=False)

def preprocess(info_df):
    # Drop NAN examples and examples with a "." which indicate missing data
    info_df = info_df[info_df != '.'].dropna()

    #explicitly typecast the information columns for easy operations
    type_dict = {
        'application_number':'int64',
        'filing_date':'datetime64',
        'examiner_id':'int64',
        'uspc_class':'string',
        'uspc_subclass':'string',
        'customer_number':'int64',
        'disposal_type':'string'
    }
    # Type casting multiple columns
    info_df = info_df.astype(type_dict)

    # order by filing date
    info_df = info_df.sort_values(by='filing_date')

    # after ordering, drop filing date
    info_df = info_df.drop('filing_date', axis=1)

    # reset index after ordering
    info_df = info_df.reset_index(drop=True)

    # correct issue of decimal strings being created after uspc class and subclass
    info_df = info_df.applymap(convert_decimal_string)

    return info_df

# method which takes a string with decimal point and removes any content after and including "."
def convert_decimal_string(s):
    if isinstance(s, str) and '.' in s:
        try:
            float_val = float(s)
            if float_val.is_integer():
                return str(int(float_val))
        except ValueError:
            pass
    return s

def extract_metadata(info_df):
    # create a new, empty dataframe to store the following metadata features (keep it separate from post process)
    meta_df = pd.DataFrame(columns=['doc-id','examiner_experience','examiner_allowance_ratio','class_saturation',
                                    'subclass_saturation','customer_experience','customer_success_ratio','status'])

    # store document id for matching files
    meta_df['doc-id'] = info_df['application_number']

    # Feature 1,2 examiner experience and allowance rate: # of times examiner_id appeared prior this exampl
    results = info_df.apply(prior_examiner_counts, axis=1)
    meta_df['examiner_experience'], meta_df['examiner_allowance_ratio'] = zip(*results)

    # Feature 3, class saturation: # of prior patents in same uspc_class
    meta_df['class_saturation'] = info_df.apply(prior_class_counts,axis=1)

    # Feature 4, subclass saturation: # of prior patents in same uspc_subclass
    meta_df['subclass_saturation'] = info_df.apply(prior_subclass_counts,axis=1)

    # Feature 5, 6 customer experience and success rate: # of prior applications submitted by same customer_number
    results = info_df.apply(prior_customer_counts, axis=1)
    meta_df['customer_experience'], meta_df['customer_success_ratio'] = zip(*results)

    # Feature 7, label: ABN, ISS, PEND
    meta_df['status'] = info_df['disposal_type'] 
    return meta_df

def prior_examiner_counts(info_df_row):
    this_examiner = info_df_row['examiner_id']
    
    # feature calculation, based on prior examples
    prior_count = examiner_id_counter.get(this_examiner,0)
    prior_allowed = examiner_allowance_counter.get(this_examiner,0)    
    prior_ratio = prior_allowed / float(prior_count) if prior_count != 0 else 0
    assert prior_count >= 0, 'prior count must be greater or equal to 0'
    assert prior_ratio <= 1.0, 'ratio must be less than 1'
    
    # update counts depending on outcome
    examiner_id_counter[this_examiner] = prior_count + 1
    if info_df_row['disposal_type'] == 'ISS': examiner_allowance_counter[this_examiner] = prior_allowed + 1

    return (prior_count,prior_ratio)

def prior_class_counts(info_df_row):
    this_class = info_df_row['uspc_class']
    prior_count = class_counter.get(this_class,0)
    assert prior_count >= 0, 'prior count must be greater or equal to 0'
    
    class_counter[this_class] = prior_count + 1
    return prior_count

def prior_subclass_counts(info_df_row):
    this_subclass = info_df_row['uspc_subclass']
    prior_count = subclass_counter.get(this_subclass,0)
    assert prior_count >= 0, 'prior count must be greater or equal to 0'
    
    subclass_counter[this_subclass] = prior_count + 1
    return prior_count

def prior_customer_counts(info_df_row):
    this_customer = info_df_row['examiner_id']
    
    # feature calculation, based on prior examples
    prior_count = customer_id_counter.get(this_customer,0)
    prior_patents = customer_patent_counter.get(this_customer,0)
    prior_ratio = prior_patents / float(prior_count) if prior_count !=0 else 0
    assert prior_count >= 0, 'prior count must be greater or equal to 0'
    assert prior_ratio <= 1.0, 'ratio must be less than 1'
    
    # update counts depending on outcome
    customer_id_counter[this_customer] = prior_count + 1
    if info_df_row['disposal_type']=='ISS': customer_patent_counter[this_customer] = prior_patents + 1
        
    return (prior_count, prior_ratio)


if __name__ == '__main__':
    main()