from django.shortcuts import render
import requests
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

# Create your views here.

def index(request):

    return render(request, 'index.html')

def imgurl(request):
    url = "https://www.albawaba.com/sites/default/files/styles/large/public/2019-09/shutterstock_1014638701.jpg"
    if request.method == 'POST':
        url = request.POST['url']
        subscription_key = "8740c8a8744343a59a2b1876c5e2e955"
        endpoint = "https://textimage.cognitiveservices.azure.com/"

        computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
        remote_image_url = url
        '''
        Describe an Image - remote
        This example describes the contents of an image with the confidence score.
        '''
        print("===== Describe an image - remote =====")
        # Call API
        description_results = computervision_client.describe_image(remote_image_url )

        # Get the captions (descriptions) from the response, with confidence level
        print("Description of remote image: ")
        strtext = ""
        if (len(description_results.captions) == 0):
            print("No description detected.")
            strtext = "No description detected."
        else:
            for caption in description_results.captions:
                print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))
                strtext = strtext + caption.text  + " | "



        '''
        Tag an Image - remote
        This example returns a tag (key word) for each thing in the image.
        '''
        print("===== Tag an image - remote =====")
        # Call API with remote image
        tags_result_remote = computervision_client.tag_image(remote_image_url )

        # Print results with confidence score
        print("Tags in the remote image: ")
        tags = ""
        if (len(tags_result_remote.tags) == 0):
            print("No tags detected.")
            tags = "No tags detected."
        else:
            for tag in tags_result_remote.tags:
                print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
                tags = tags+ tag.name+", "

        '''
        Detect Adult or Racy Content - remote
        This example detects adult or racy content in a remote image, then prints the adult/racy score.
        The score is ranged 0.0 - 1.0 with smaller numbers indicating negative results.
        '''
        print("===== Detect Adult or Racy Content - remote =====")
        # Select the visual feature(s) you want
        remote_image_features = ["adult"]
        # Call API with URL and features
        detect_adult_results_remote = computervision_client.analyze_image(remote_image_url, remote_image_features)

        # Print results with adult/racy score
        print("Analyzing remote image for adult or racy content ... ")
        print("Is adult content: {} with confidence {:.2f}".format(detect_adult_results_remote.adult.is_adult_content, detect_adult_results_remote.adult.adult_score * 100))
        print("Has racy content: {} with confidence {:.2f}".format(detect_adult_results_remote.adult.is_racy_content, detect_adult_results_remote.adult.racy_score * 100))
        params = {'text': strtext, 'url': url, 'tags': tags}
        return render(request, 'index.html', params)
    params = {'text': "a couple of lions ", 'url': url, 'tags': "animal, mammal, big cat, lion, outdoor, big cats, terrestrial animal, wildlife, masai lion, zoo, snout, safari, felidae, whiskers, cat, brown,"}
    return render(request, 'index.html', params)
