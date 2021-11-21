import logging

import azure.functions as func
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

import numpy as np
from dotenv import load_dotenv   # for variables
import base64
import io
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import cv2
import os, time, uuid


def convert_blob_to_bytes(data_blob: func.InputStream):
    image_name = str(data_blob.name).split("/")[-1]
    # logging.warn("Converting image: {} ...".format(image_name))
    img_bytes = data_blob.read() 

    # imageStream = io.BytesIO(base_64_img)
    # imageFile = Image.open(imageStream)
    # imageFile.save("test_2.png")
    # # write to the file
    # with open(image_name,'wb') as image_file:
    #     logging.warn("Writting to image")
    #     image_file.write(img_bytes)
    return img_bytes, image_name


def load_env_variables():
    load_dotenv()             
    endpoint = os.environ.get("ENDPOINT")
    prediction_key = os.environ.get("PREDICTION_KEY")
    published_iteration_name = os.environ.get("PUBLISHED_ITERATION_NAME")
    project_id = os.environ.get("PROJECT_ID")

    return endpoint, prediction_key, published_iteration_name, project_id


def detect_scratches(png_bytes):
    endpoint, pred_key, pub_iter_name, project_id = load_env_variables()

    # feed the image to Custom Vision -> CustomVisionPredictionClient 
    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": pred_key})
    predictor = CustomVisionPredictionClient(endpoint, prediction_credentials)
    # logging.warn("tralla {}, {}".format(project_id, pub_iter_name))

    # Retrieve results
    results = predictor.detect_image(project_id, pub_iter_name, png_bytes)
    return results

def draw_rectangle_and_save_image(detection_results, picture_bytes, image_name):
    # Save image if it has scratches 
    is_scratch = False
    source_img = Image.open(io.BytesIO(picture_bytes)).convert("RGB")
    drawed_image = ImageDraw.Draw(source_img)
    
    # Display the results.    
    for prediction in detection_results.predictions:
        prediction_accuracy = prediction.probability * 100
        logging.info("Accuracy: {}%".format(prediction_accuracy))
        
        if prediction_accuracy >= 50:
            is_scratch = True
            width = source_img.width
            height = source_img.height
            top_left_cord = (prediction.bounding_box.left * width, prediction.bounding_box.top * height)
            bottom_right_cord = (top_left_cord[0] + (prediction.bounding_box.width * width), 
                                top_left_cord[1] + (prediction.bounding_box.height * height))

            logging.warn("Coordinates {}{}".format(top_left_cord, bottom_right_cord))
            drawed_image.rectangle((top_left_cord, bottom_right_cord), fill=None)

    if is_scratch:
        source_img.save("rec_" + image_name, "JPEG")
    else:
        logging.info("No scratches on this image ...")


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")    
    # Converting blob data to bytes
    png_bytes, image_name = convert_blob_to_bytes(myblob)

    # TODO preprocess image 

    # Retrieve results
    results = detect_scratches(png_bytes)

    # Save image if it has high enough classification acc 
    draw_rectangle_and_save_image(results, png_bytes, image_name)

    # TODO Pass the results to the Power BI or PowerApps
    

    #

