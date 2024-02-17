import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    for i in range(len(dates)):
        dates[i] = date_formatting(dates[i])
    df = pd.DataFrame({'Message': messages, 'Dates': dates})
    df['Dates'] = pd.to_datetime(df['Dates'], format='%m/%d/%Y, %H:%M - ')
    users = []
    messages = []
    for message in df['Message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Notification')
            messages.append(entry[0])

    df['User'] = users
    df['Message'] = messages
    df.rename({'Dates': 'Date'}, inplace=True, axis=1)
    df['Month'] = df['Date'].dt.month_name()
    df['Month Number'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df['Day'] = df['Date'].dt.day
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute
    df['Only Date'] = df['Date'].dt.date
    df['Day Name'] = df['Date'].dt.day_name()

    period = []
    for hour in df[['Day Name','Hour']]['Hour']:
        if hour == 23:
            period.append((str(hour)+'-'+str('00')))
        elif hour == 0:
            period.append((str('00') + '-' + str(hour+1)))
        else:
            period.append((str(hour) + '-' + str(hour+1)))
    df['Period'] = period

    return df

def date_formatting(date_string):
    if len(date_string) == 17:
        if date_string[1]=='/':
            dummy = date_string
            dummy = '0'+ dummy
            date_string = dummy
        elif date_string[2]=='/':
            dummy = date_string
            dummy = dummy[:3]+'0'+dummy[3:]
            date_string = dummy
    elif len(date_string) == 16:
        dummy = date_string
        dummy = '0'+ dummy
        dummy = dummy[:3]+'0'+dummy[3:]
        date_string = dummy

    dummy = date_string
    dummy = dummy[:6]+'20'+dummy[6:]
    date_string = dummy

    return date_string
