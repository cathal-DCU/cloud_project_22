# Getting started

To start with you will need to download the Google Command Line interface from https://cloud.google.com/sdk/docs/install

To set up the project on your cloud run the following command from Google CLI(after logging in to your cloud account on the CLI):

gcloud projects create dcucloudsystemsproject22

To set the project as current project, run:

gcloud config set project dcucloudsystemsproject22

To enable billing so that Google APIs can be enabled, run(after inserting billing details from Google Cloud):

gcloud alpha billing projects link dcucloudsystemsproject22 --billing-account 0X0X0X-0X0X0X-0X0X0X

To enable required APIs(some might be superfluous in the end):

gcloud services enable dataproc.googleapis.com compute.googleapis.com storage-component.googleapis.com 

To set up the project bucket, run:

gsutil mb -c standard -l europe-west3 gs://cloud-project-bucket-22

To set up a Dataproc cluster with required python dependencies run:

gcloud dataproc clusters create sent-analysis-22 --region=europe-west3 --zone=europe-west3-b --image-version=2.0 --master-machine-type=n1-standard-4 --worker-machine-type=n1-standard-2 --master-boot-disk-size=1000GB --worker-boot-disk-size=500GB --bucket=dcucloudsystemsproject22 --optional-components=JUPYTER --enable-component-gateway --metadata “PIP_PACKAGES=google-cloud-bigquery string dash pyorbital  tweepy google-cloud-storage pandas numpy matplotlib jupyterlab_dash seaborn pathlib sklearn socket wordcloud spark-nlp-display spark-nlp==3.3.1 plotly>=5 chart_studio ipywidgets>=7.6 geopy findspark nltk textblob” --initialization-action-timeout=30m --initialization-actions gs://goog-dataproc-initialization-actions-europe-west3/python/pip-install.sh

To get the link to the JupyterLab notebook for this cluster, run:

gcloud beta dataproc clusters describe sent-analysis-22 --region=europe-west3

Then put that link into your browser

*If you need to delete the cluster, run the following:

gcloud beta dataproc clusters delete sent-analysis-22 --region=europe-west3
