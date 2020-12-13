from django.shortcuts import render
import requests
import csv
import pandas as pd
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import numpy as np

def index(request):
    return render(request,'index.html')
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        file_path="http://127.0.0.1:8000"+uploaded_file_url
        df2=pd.read_csv(file_path)
        r = requests.get('https://data.ct.gov/resource/6tja-6vdt.json')
        df = pd.DataFrame(r.json())
        a=df['salespersoncredential'].values.tolist()
        b=df2['salespersoncredential'].values.tolist()
        c=[]
        for x in a:
            if x in b:
                c.append(True)
            else:
                c.append(False)
        present=pd.Series(c)
        df3=df[present]
        df3.to_csv('media/finally.csv')
        data_list=list(df3.values.tolist())
        download_url="media/finally.csv"
        print(df[present])
        return render(request, 'index.html', {
            'uploaded_file_url': uploaded_file_url,
            'data_list':data_list,
            'download_url':download_url
        })
    return render(request, 'index.html')
def process_api(request):
    processing_data()
    html='<h1>pass</h1>'
    return HttpResponse (html)
