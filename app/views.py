import matplotlib.pyplot as plt
from django.shortcuts import render
from django.http import HttpResponse
from models import process
import urllib,base64
from models import graphs
from io import StringIO
import numpy as np
import seaborn as sns
# Create your views here.

def index(request):
    return render(request,'app/forms.html')
def predict(request):
    if request.method == 'POST':
        temp = {'username': request.POST.get('username'),
                'password':request.POST.get('password')}
    return render(request,'app/predict.html',{'temp':temp})

def file_up(request):
    if request.method == 'POST':
        file1 = request.FILES['file']
        contentOfFile = file1.read()
        main_class = process.main(contentOfFile)

    #months
    def plot_months():
        minutes = main_class.minutes_only()
        users = main_class.all_users()
        fig = plt.figure()
        plt.stem(minutes,users)
        imgdata=StringIO()
        fig.savefig(imgdata,format='svg')
        imgdata.seek(0)
        data = imgdata.getvalue()
        return data

    #dates
    def plot_dates():
        dates = main_class.dates_only()
        fig = plt.figure()
        plt.eventplot(dates)
        imgdata=StringIO()
        fig.savefig(imgdata,format='svg')
        imgdata.seek(0)
        all_dates = imgdata.getvalue()
        return all_dates

    #years
    def plot_years():
        years = main_class.years_only()
        fig = plt.figure()
        plt.hist(years)
        imgdata=StringIO()
        fig.savefig(imgdata,format='svg')
        imgdata.seek(0)
        all_years = imgdata.getvalue()
        return all_years

    #days
    def plot_days():
        days = main_class.days_only()
        fig = plt.figure()
        plt.eventplot(days)
        imgdata=StringIO()
        fig.savefig(imgdata,format='svg')
        imgdata.seek(0)
        all_dates = imgdata.getvalue()
        return all_dates

    months = plot_months
    days = plot_days
    dates = plot_dates
    years = plot_years
    return render(request, 'app/homepage-2.html', {'file': file1, 'months': months ,'days': days,'dates':dates,'years':years})
        # minutes = main_class.minutes_only()#.to_list()
        # users = main_class.all_users()
        # fig = plt.figure()
        # plt.plot(minutes,users)
        # imgdata=StringIO()
        # fig.savefig(imgdata,format='svg')
        # imgdata.seek(0)
        # data = imgdata.getvalue()
        
        # if file1:
        #     return render(request, 'app/file_upload.html', {'file': file1, 'contentOfFile': data})

# def plot_months(request):
#     total_months = file_up()
#     main_class = process.main(total_months)
#     months = main_class.months_only()
#     return render(request,'app/file_upload.html',{'file':months})

# class all_plots:
#     template_name= 'app/predict.html'
#     @staticmethod
#     def file_up(request):
#         if request.method == 'POST':
#             file1 = request.FILES['file']
#             contentOfFile = file1.read()
#             main_class = process.main(contentOfFile)
#             minutes = main_class.dates_only()
#             if file1:
#                 return render(request, 'app/file_upload.html', {'file': file1})
    
    