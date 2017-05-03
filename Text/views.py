# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .forms import NameForm
from .fileforms import UploadFileForm
from TextAndAPI import predictTextData
import json
from filePrediction import predictFile
import os, tempfile, zipfile
#from django.core.servers.basehttp import FileWrapper
from wsgiref.util import FileWrapper
from django.conf import settings
import mimetypes
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Text.serializer import APISerializer
import unicodedata
from Text.PersonalitySerializer import PersonalitySerializer
from Text.Personality import Personality
from Text.models import API
#from Text.models import API_Mongo
import sys
import logging
from fusioncharts import FusionCharts
import os 

logger = logging.getLogger(__name__)

#Home Screen
def homeIndex(request):
    logger.debug('Home Page Opened')
    return render(request,'home/Home.html')
	
#dummy 	
def secondIndex(request):
    return render(request,'home/index.html')


#/fileprocess/	
def upload_file(request):
    msg = "File Uploaded"
    print "inside upload_file function"
    if request.method == 'POST':
        print "inside upload_file function2"
        file = UploadFileForm(request.POST, request.FILES)
        if file.is_valid():
            logger.debug('Home Page Opened')
            print "inside upload_file function3"
            handle_uploaded_file(request.FILES['file'])
            print "file saved locally"
            response_data = {}
            response_data['success'] = 'true'
            try:
                predictFile()
            except Exception as e:
                logger.error("Exception occurred")
                logger.error(e)
            print "going to return something"    
            return HttpResponse(json.dumps(response_data),content_type="application/json")
        else :
            print "File errors"
            print file.errors
    else:
        form = UploadFileForm()
    #return render(request, 'upload.html', {'form': form}) 
    return render(request,'home/DownloadFile.html',{'content': msg})

### Used to write the file into server folder	
def handle_uploaded_file(f):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path+'/File/Input/Input.csv', 'wb+') as destination:
        for chunk in f.chunks():
            try:
                l = chunk.splitlines()
                for line in l:
                    #mongo = API_Mongo()
                    chunk = chunk.decode('utf-8','ignore').encode("utf-8")
                    #mongo.content = chunk
                    #mongo.save()
            except :
                e = sys.exc_info()[0]
                logger.error('Exception while saving into databse')
                logger.error(e)
            destination.write(chunk)

#/Download/
def download_option(request):
     dir_path = os.path.dirname(os.path.realpath(__file__))
     filename     = dir_path+"/File/File_Prediction.csv" # Select your file here.
     download_name ="File_Prediction.csv"
     wrapper      = FileWrapper(open(filename))
     content_type = mimetypes.guess_type(filename)[0]
     response     = HttpResponse(wrapper,content_type=content_type)
     response['Content-Length']      = os.path.getsize(filename)    
     response['Content-Disposition'] = "attachment; filename=%s"%download_name
     return response
    
#/analyze/
def get_text(request):
    msg = "File Uploaded"
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # print (form.cleaned_data['for_analysis'])
            #mongo = API_Mongo()
            #mongo.content = form.cleaned_data['for_analysis']
            #mongo.save()
            logger.debug('Text Data saved to Mongo DB')
            data = form.cleaned_data['for_analysis'].encode("utf-8")
            #data = data.decode('utf-8','ignore').encode("utf-8")
	    msg = predictTextData(data)
	    print msg
            return render(request,'home/Analyze_Character.html',{'Extraversion':msg})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request,'home/Analyze_Character.html',{'content': msg})

#/snippets/
@api_view(['POST'])
def api_Data_process(request,format=None):
    """
    List all snippets, or create a new snippet.
    """

    if request.method == 'POST':
        serializer = APISerializer(data=request.data)
        data=request.POST.get("content", "")
        data = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
        msg = predictTextData(data)
        if serializer.is_valid():
            logger.debug('API data serialized is valid')
            serializer.save()
            P= Personality(EXT=msg['Extraversion'],NEU=msg['Neuroticism'],AGR=msg['Agreeableness'],CON=msg['Conscientiousness'],OPN=msg['Openness'])
            serializerP = PersonalitySerializer(P)
            #mongo = API_Mongo()
            #mongo.content = data
            #mongo.save()
            logger.debug('API data stored to Mongo DB')
            return Response(serializerP.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def chart(request):
    return render(request, 'home/BarChart.html')

def charttry(request):
    return render(request, 'home/Bar.html')
    
