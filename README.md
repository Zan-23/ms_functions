# Cloud-based AI Inspection
...

# How we built it
Our cloud-based AI inspection demo has three main components. Once the image of the chip is uploaded in the Azure Storage it triggers the pre-processing python script of the image in the Azure Functions and it calls Azure Custom Vision API Request to make a prediction, whether a chip has a defect or not.

## Image Processing
- Python script running with Azure Functions
- Triggered by uploading an image to Azure Storage
- .....
- .....
- .....

## Image Classifier
- Azure Custom Vision
- Training set contains ..... images
- .....

## Dashboard
- Plotly Dash
- Mark of the last inspected chip
- Image of the last inspected chip
- Precission, Recall, F-1

## Challenges we ran into
One of the most challenging parts was the integration of image processing pipeline into the python script. We were also dealing with many problems when deploying the python script in the Azure Functions, as the application was perfectly working localy but wasn't working deployed. Therefore, we decided to run it localy.

## What we learned
We have learned how to distribute the work among ourselves and also gain experience in the fields we have never worked before (Azure Cloud Computing Services).

## What's next for united jackets
We will continue to strive for improvements in our classifier's performance and also in the cloud-based pipeline in order to connect the output with the better dashboard.

## Requirements
- Azure credentials
- Plotly Dash
- python dependecises - see 'requirements.txt'

## Running the Inspection
.....

## HackaTum presentation: .....
## Devpost link: .....
## Contributors: 
- Daria Matiunina
- Selman Özleyen
- Žan Stanovnik
- Gregor Caf
