#!/bin/bash

function pause(){
   read -p "$*"
}

<<comment
mkdir temp
cd temp
# wget http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip
# unzip ~$OBJECT_LOCATION
# delete the zip file and the test data
# the reason why I'm not using this test data is because
# the training data only has two target labels: negative, positive
# but the test data has three target labels: negative, neutral, positive
# to simplify I won't do any neutral class classification with predicted probabilities
rm trainingandtestdata.zip test*.csv
comment

<<comment1
# go back to the parent directory and run train_test_split.py
# cd ~$OBJECT_LOCATION
python train_test_split.py
# delete temporary directory and the files in it
rm -rf temp
# upload training_data and test_data created by train_test_split.py to Google Cloud Storage
#gsutil cp pyspark_sa_train_data.csv gs://${PROJECT_ID}/pyspark_nlp/data/training_data.csv
#gsutil cp pyspark_sa_test_data.csv gs://${PROJECT_ID}/pyspark_nlp/data/test_data.csv
gsutil cp pyspark_sa_train_data.csv gs://bigquery-bucket-2
gsutil cp pyspark_sa_test_data.csv gs://bigquery-bucket-2

# remove the training_data and test_data after uploading
rm pyspark_sa_train_data.csv pyspark_sa_test_data.csv
comment1

<<comment2
mkdir temp
cd temp
rm -rf temp
# https://cloud.google.com/build/docs/running-builds/start-build-command-line-api
# https://cloud.google.com/build/docs/automating-builds/create-manual-triggers
You can use . to specify that the source code is in the current working directory:
gcloud builds submit --config cloudbuild.yaml .
gcloud builds submit --config build-config source-code

comment2

# gcloud projects create PROJECT_ID
# http://www.compciv.org/topics/bash/variables-and-substitution/



# PROJECT_ID=$cloudsystemsproject2018
gcloud projects create dcucloudsystemsproject22
gcloud config set project dcucloudsystemsproject22
# enable billing
# gcloud alpha billing accounts list
gcloud alpha billing projects link dcucloudsystemsproject22 --billing-account 0X0X0X-0X0X0X-0X0X0X

gcloud services enable dataproc.googleapis.com compute.googleapis.com storage-component.googleapis.com bigquery.googleapis.com bigquerystorage.googleapis.com
gsutil mb -c standard -l europe-west3 gs://cloud-project-bucket-4
gcloud dataproc clusters create sent-analysis-22 --region=europe-west3 --zone=europe-west3-a --image-version=2.0 --master-machine-type=n1-standard-4  --worker-machine-type=n1-standard-2 --master-boot-disk-size=1000GB --worker-boot-disk-size=500GB --bucket=cloud-project-bucket-3 --optional-components=JUPYTER --enable-component-gateway --metadata “PIP_PACKAGES=google-cloud-bigquery tweepy google-cloud-storage pandas numpy matplotlib seaborn pathlib sklearn wordcloud spark-nlp-display spark-nlp==3.3.1 nltk textblob” --initialization-action-timeout=30m --initialization-actions gs://goog-dataproc-initialization-actions-europe-west3/python/pip-install.sh
# DELETE gcloud beta dataproc clusters delete spark-jupyter-cathal --region=europe-west3

PYTHON download_and_upload.py
gsutil cp C:\Users\catha\Downloads\sentiment140\Sentiment_Analysis_Dataset.csv gs://cloud-project-bucket-4
gsutil ls -r gs://cloud-project-bucket-3**

# Get JupyterLab notebook link:
gcloud beta dataproc clusters describe sent-analysis-22 --region=europe-west3

# ...
# call it
pause 'Press [Enter] key to continue...'
