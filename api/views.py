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
        # df=pd.read_csv('media/6tja-6vdt.csv')
        r = requests.get('https://data.ct.gov/resource/6tja-6vdt.json?$limit=19000&$$app_token=utb5TunA6LowgPa1G5vfHTvBQ')
        df = pd.DataFrame(r.json())
        a=df['salespersoncredential'].values.tolist()
        b=df2['salespersoncredential'].values.tolist()
        # name=df2['real_estate_salesperson'].values.tolist()
        c=[]
        d=[]
        e=[]
        for x in a:
            if x in b:
                c.append(True)
            else:
                c.append(False)
        present=pd.Series(c)
        df3=df[present]
        df3_list=df3['salespersoncredential'].values.tolist()
        for y in b:
            if y in df3_list:
                d.append(False)
            else:
                d.append(True)
        not_found=pd.Series(d)
        df4=df2[not_found]
        df4.to_csv('media/not_found.csv')
        print(df4)
        print(df3)
        df3.to_csv('media/finally.csv')
        data_list=list(df3.values.tolist())
        not_found_data_list=list(df4.values.tolist())
        download_url="media/finally.csv"
        not_found_url="media/not_found.csv"
        # print(df[present])
        return render(request, 'index.html', {
            'uploaded_file_url': uploaded_file_url,
            'data_list':data_list,
            'not_found_data_list':not_found_data_list,
            'download_url':download_url,
            'not_found_url':not_found_url
        })
    return render(request, 'index.html')
def process_api(request):
    processing_data()
    html='<h1>pass</h1>'
    return HttpResponse (html)
