import pandas as pd
import numpy as np
import re
from urlextract import URLExtract
from collections import Counter
import emoji
extract = URLExtract()


class main:
    def __init__(self, data) -> None:
        self.data = data.decode('utf-8')
        # f = open("models/WhatsApp Chat with Young Genius 🙉☺️.txt" , 'r' ,encoding='utf-8')
        # self.data =f.read()
        self.pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\S{2}\s-\s'
        self.messages = re.split(self.pattern, self.data)[1:]
        self.dates = re.findall(self.pattern, self. data)
        df = pd.DataFrame({'user_message': self.messages,
                          'message_date': self.dates})
        for columns in df['message_date']:
            df['message_date'] = df['message_date'].str.upper()
        df['message_date'] = df["message_date"].str.replace("-", "")
        df['message_date'] = df["message_date"].str.replace(",", " ")
        # Print the formatted date
        df['message_date'] = pd.to_datetime(df['message_date'])
        df['message_date'] = df['message_date'].dt.strftime(
            '%d/%m/%Y %I:%M %p')
        df['message_date'] = pd.to_datetime(
            df['message_date'], format='%d/%m/%Y %I:%M %p')
        df['message_date'].dt.date
        df.rename(columns={'message_date': 'date'}, inplace=True)
        users = []
        for message in df['user_message']:
            entry = re.split('([\w\W]+?):\s', message)
            if entry[1:]:  # user name
                users.append(entry[1])
            else:
                users.append('group_notification')
        df['user'] = users
        self.users = users
        messages = []
        for message in df['user_message']:
            entry = re.split('([\w\W]+?):\s', message)
            if entry[1:]:  # user name
                messages.append(" ".join(entry[2:]))
            else:
                messages.append(entry[0])
        df['message'] = messages
        self.messages = messages
        links = []
        for message in df['message']:
            links.extend(extract.find_urls(message))
        self.links = links
        self.df = df

    def func1(self):
        return self.df

    def most_busy_users(self):
        x = self.df['user'].value_counts().head()
        self.df = round((self.df['user'].value_counts() / self.df.shape[0]) * 100, 2).reset_index().rename(
            columns={'index': 'name', 'user': 'percent'})
        return x, self.df

    def most_common_words(self):
        f = open('models/stop_hinglish.txt', 'r')
        stop_words = f.read()
        temp = self.df[self.df['user'] != 'group_notification']
        temp = temp[temp['message'] != '<Media omitted>\n']
        words = []
        for message in temp['message']:
            words.extend(word for word in message.lower().split()
                         if word not in stop_words)
        most_common_df = pd.DataFrame(Counter(words).most_common(20))
        return most_common_df

    def emoji(self):
        emojis = []
        for message in self.df['message']:
            emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
        emoji_df = pd.DataFrame(
            Counter(emojis).most_common(len(Counter(emojis))))
        return emoji_df

    def all_users(self):
        return self.users

    def all_links(self):
        return len(self.links)

    def num_media(self):
        num_media_messages = self.df[self.df['message']
                                     == '<Media omitted>\n'].shape[0]
        return num_media_messages

    def all_messages(self):
        return self.messages

    def dates_only(self):
        self.df['only_date'] = self.df['date'].dt.date
        dates = self.df['only_date']
        return dates

    def years_only(self):
        self.df['year'] = self.df['date'].dt.year
        years = self.df['year']
        return years

    def months_only(self):
        self.df['month_num'] = self.df['date'].dt.month
        self.df['month'] = self.df['date'].dt.month_name()
        months = self.df['month']
        return months

    def days_only(self):
        self.df['day'] = self.df['date'].dt.day
        self.df['day_name'] = self.df['date'].dt.day_name()
        days = self.df['day_name']
        return days

    def hours_only(self):
        self.df['hour'] = self.df['date'].dt.hour
        hours = self.df['hour']
        return hours

    def minutes_only(self):
        self.df['minute'] = self.df['date'].dt.minute
        minutes = self.df['minute']
        return minutes

    def monthly_timeline(self):  # sourcery skip: for-append-to-extend, list-comprehension
        self.df['year'] = self.df['date'].dt.year
        self.df['month_num'] = self.df['date'].dt.month
        self.df['month'] = self.df['date'].dt.month_name()
        timeline = self.df.groupby(['year', 'month_num', 'month']).count()[
            'message'].reset_index()
        time = []
        for i in range(timeline.shape[0]):
            time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
        timeline['time'] = time
        return timeline

    def daily_timeline(self):
        self.df['only_date'] = self.df['date'].dt.date
        daily_timeline = self.df.groupby('only_date').count()[
            'message'].reset_index()
        return daily_timeline

    def week_activity_map(self):
        self.df['day'] = self.df['date'].dt.day
        self.df['day_name'] = self.df['date'].dt.day_name()
        return self.df['day_name'].value_counts()

    def month_activity_map(self):
        self.df['month_num'] = self.df['date'].dt.month
        self.df['month'] = self.df['date'].dt.month_name()
        return self.df['month'].value_counts()

