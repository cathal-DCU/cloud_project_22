# https://github.com/RonKG/Machine-Learning-Projects-2/blob/master/3.%20NLP_twitter_sentiment_analysis/FINAL____twitter_sentiment_twitter.ipynb
# https://www.kaggle.com/kazanova/sentiment140
# https://www.analyticsvidhya.com/blog/2021/06/twitter-sentiment-analysis-a-nlp-use-case-for-beginners/
# https://github.com/AbhinavThukral97/SentimentAnalysis/blob/master/main.pyhttps://github.com/AbhinavThukral97/SentimentAnalysis/blob/master/main.py

from pathlib import Path
import urllib.request
import zipfile
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os

# Importing the dataset
#data_folder = Path(os.getcwd())
data_folder = Path("C:/Users/catha/Downloads")
zip_folder = data_folder / 'trainingandtestdata.zip'

print('Beginning Sentiment 140 dataset download')
url = 'http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip'
urllib.request.urlretrieve(url, zip_folder)

extracted_folder = data_folder / 'sentiment140'
# extracted_folder.mkdir()

with zipfile.ZipFile(zip_folder, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder)

# Renaming the file
old_name = extracted_folder / 'training.1600000.processed.noemoticon.csv'
new_name = extracted_folder / 'Sentiment_Analysis_Dataset.csv'
os.rename(old_name, new_name)
print("Sentiment Analysis Dataset downloaded")
#os.rename('training.1600000.processed.noemoticon', 'Sentiment_Analysis_Dataset.csv')


"""
# https://cloud.google.com/iam/docs/creating-managing-service-account-keys#iam-service-account-keys-create-console

credentials_dict = {
    'type': 'service_account',
    'client_id': os.environ['BACKUP_CLIENT_ID'],
    'client_email': os.environ['BACKUP_CLIENT_EMAIL'],
    'private_key_id': os.environ['BACKUP_PRIVATE_KEY_ID'],
    'private_key': os.environ['BACKUP_PRIVATE_KEY'],
}

credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    credentials_dict
)
client = storage.Client(credentials=credentials, project='cloudsystemsproject2019')
bucket = client.get_bucket('cloud-project-bucket-1')
blob = bucket.blob(new_name)
blob.upload_from_filename(new_name)

# Also upload other code files
# code to delete folder once uploaded

"""
