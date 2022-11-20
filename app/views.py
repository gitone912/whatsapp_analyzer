import matplotlib.pyplot as plt
from django.shortcuts import render
from django.http import HttpResponse
from models import process
import urllib,base64
from models import graphs
from io import StringIO
import numpy as np
import seaborn as sns
from IPython.display import HTML
# Create your views here.
def index(request):
    return render(request,'app/contact.html')

def file_up(request):
    if request.method == 'POST':
        temp = request.POST.get('username')
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
    
    #users
    def total_users():
        t_users = main_class.num_media()
        return t_users

    #links
    def total_links():
        links = main_class.all_links()
        return links
    
    #most_busy useres
    def most_busy():
        most_busy_users = main_class.most_busy_users()
        return most_busy_users
    
    def common_word():
        most_common_word = main_class.most_common_words()
        return most_common_word
    
    def total_emoji():
        emoji= main_class.emoji()
        return emoji
    
    def monthly_timeline():
        monthly=main_class.monthly_timeline()
        return monthly
    
    def daily_timeline():
        daily = main_class.daily_timeline()
        return daily
    
    def week_activity_map():
        weekly = main_class.week_activity_map()
        return weekly
    
    def month_activity():
        monthly_activity = main_class.month_activity_map()
        return monthly_activity
    
    months = plot_months
    days = plot_days
    dates = plot_dates
    years = plot_years
    _users = total_users
    all_links = total_links
    busy = most_busy
    emoji = total_emoji
    most_common_word = common_word
    monthly = monthly_timeline
    daily = daily_timeline
    week_activity = week_activity_map
    monthly_activity = month_activity
    
    context = {'file': file1, 'months': months ,'days': days,'dates':dates,'years':years,'name':temp,'total_media': _users,'all_links':all_links,'busy':busy,'common_word':most_common_word,'emoji':emoji,'monthly':monthly,'daily':daily,'week_activity':week_activity,'monthly_activity':monthly_activity}
    
    return render(request, 'app/homepage-2.html', context)
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

