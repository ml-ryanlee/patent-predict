# patent-predict
Predicting whether a patent will be granted based on images, text, and metadata

# Generating the text and numerical (metadata) datasets
1. Upload PatEx dataset to src/data
2. Run processmetadata.py --> generates (doc-id,labels) and (metadata,labels) datasets
3. Upload unparsed xml files to "docs2005" folder. We chose the first 24 xml files from 2005.
4. Run processclaims.py --> generates (claims,labels) dataset
5. (optional) as an alternative to running processclaims.py, run extractiveclaims.py to reduce claims to top 3 textrank sentences (if number of sentences >3).

Patex database is application data csv: https://www.uspto.gov/ip-policy/economic-research/research-datasets/patent-examination-research-dataset-public-pair
Unparsed xml files are from: https://developer.uspto.gov/product/patent-application-full-text-dataxml

# Set-up Text dataset for Transformer Model Notebooks
Transformer models are fine-tuned on Google Collab. To navigate to them, go to notebooks.
1. Move the text_patentability_data.csv from src/data to notebooks/data
2. Run preprocess.ipynb code on Google Collab to generate the text_df_all.csv dataset for training the models. Simply removes (canceled) keyword
3. To generate dataset with an "abstracts" column, run bart.ipynb, which will use BART to create an abstractive summary of the claims text

# Running Fine-tune Model Code (BERT, RoBERTa, BigBird, LongFormer, GPT2)
1. BigBird and RoBERTa require the use of an A100 GPU, due to the memory requirements, available through Google Collab Pro
2. For BERT, RoBERTa, BigBird, a custom Pytorch dataset was defined. There are two lines of code, shown below, to enable fine-tuning on claims or the abstractive summaries. 
        #text = self.data_frame.iloc[idx]['claims']
        text = self.data_frame.iloc[idx]['abstracts']
