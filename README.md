# patent-predict
Predicting whether a patent will be granted based on images, text, and metadata

## Generating the text and numerical (metadata) datasets
1. Upload PatEx dataset to src/data
2. Run processmetadata.py --> generates (doc-id,labels) and (metadata,labels) datasets
3. Upload unparsed xml files to "docs2005" folder. We chose the first 24 xml files from 2005.
4. Run processclaims.py --> generates (claims,labels) dataset
5. (optional) as an alternative to running processclaims.py, run extractiveclaims.py to reduce claims to top 3 textrank sentences (if number of sentences >3).

- Patex database is application data csv: https://www.uspto.gov/ip-policy/economic-research/research-datasets/patent-examination-research-dataset-public-pair
- Unparsed xml files are from: https://developer.uspto.gov/product/patent-application-full-text-dataxml

## Set-up Text dataset for Transformer Model Notebooks
Transformer models are fine-tuned on Google Collab. To navigate to them, go to notebooks. Copy these notebooks to your Google Drive and follow the below instructions.
1. Move the text_patentability_data.csv from src/data to a subfolder in Google drive labeled data
2. Run preprocess.ipynb code on Google Collab to generate the text_df.csv dataset for training the models. Simply removes (canceled) keyword and "pending" examples
3. To generate dataset with an "abstracts" column, run bart.ipynb, which will use BART to create an abstractive summary of the claims text

## Running Fine-tune Model Code (BERT, RoBERTa, BigBird, LongFormer, GPT2)
1. Model notebook files are located in notebooks folder
2. BigBird and RoBERTa require the use of an A100 GPU, due to the memory requirements, available through Google Collab Pro
3. Make sure to change any folder paths to the appropriate paths for the text_df.csv datafile and model saving path
4. For BERT, RoBERTa, BigBird, a custom Pytorch dataset was defined. There are two lines of code, shown below, to enable fine-tuning on claims or the abstractive summaries. Comment out the definition of the text data that is not used to fine-tune. 
- #text = self.data_frame.iloc[idx]['claims'] #using abstracts not claims
- text = self.data_frame.iloc[idx]['abstracts']
