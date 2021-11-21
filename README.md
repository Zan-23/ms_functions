# Cloud-based AI Inspection

## How we built it
Our cloud-based AI inspection demo has three main components - image preprocessing Azure Function, model trained and inferenced with Azure Vision API and Plotly board for an easy visualization of results. Once the image of the chip is uploaded in the Azure Storage it triggers the pre-processing python script of the image in the Azure Functions and it calls Azure Custom Vision API Request to make a prediction, whether a chip has a defect or not.

## Image Processing
- Python script running with Azure Functions to preprocess data:
  - ML for line detection,
  - Custom search of sensor's screen position,
  - Pixel values transformation,
  - Selected augmentation
- Triggered by uploading an image to Azure Storage
  - Preprocessing is run
  - Azure Custom Vision model is inferenced
  - Results are displayed at the dashboard

## Object Detector
- Azure Custom Vision for Object Detection
- Training set contains ~ 100 images each containing a scratched screen of sensor

## Dashboard
- Plotly Dash
- Mark of the last inspected chip
- Image of the last inspected chip
- Precission, Recall, F-1

## Challenges we ran into
1. One of the most challenging parts was the integration of image processing pipeline into the python script. We were also dealing with many problems when deploying the python script in the Azure Functions, as the application was perfectly working localy but wasn't working deployed. Therefore, we decided to run it localy.
2. Detection of small objects is a whole research area. We have put a lot of effort to simplify data (from sensor image to image of screen) and brainstormed on approaches to maximize the appearance of searched objects in the data.

## What we learned
We have learned how to distribute the work among ourselves and also gain experience in the fields we have never worked before (Azure Cloud Computing Services). Every member of the team had a lot of unique problems to solve and contributed a lot into the final result.

## What's next for united jackets
We will continue to strive for improvements in our algorithm design and also in the cloud-based pipeline in order to connect the output with a better dashboard.
We would also like to test out alternative idea related to ML: binary classification of patches of screen images for the task of defect detection.

## Requirements
- Azure credentials
- Plotly Dash
- python dependecises - see 'requirements.txt'

## Contributors: 
- Daria Matiunina
- Selman Özleyen
- Žan Stanovnik
- Gregor Caf
