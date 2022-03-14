import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import datetime as dt
@st.cache
def get_plots(name):
    if name == "Risu":
        df = pd.read_csv('risu.csv')
    elif name == "Reine":
        df = pd.read_csv('rini.csv')
    elif name == "Ollie":
        df = pd.read_csv('ollie.csv')
    elif name == "Mori":
        df = pd.read_csv('mori.csv')
    else:
        return

    df['dtstart'] = pd.to_datetime(df['dtstart'])
    df = df.drop(['dtend','dtstamp','organizer','uid','attendee','created','description','last-modified','location','sequence','status','transp'], axis=1)
    df['dtstart'] = pd.to_datetime(df['dtstart'], utc=True) #, utc=True required for Reine because Python is ...Python.
    df['day-of-week'] = df['dtstart'].dt.day_name()
    plt.style.use('dark_background')
    st.bar_chart(df['day-of-week'].value_counts())
    df['day-of-week'].value_counts().plot.bar()
    df['stremtime'] = df['dtstart'] + dt.timedelta(hours=7) #9 for mori, 7 for risu
    df['hour'] = df['stremtime'].dt.hour
    df['weeknum'] = df['dtstart'].dt.dayofweek
    df2 = pd.crosstab(df['hour'], df['weeknum']).div(len(df))
    #print(df2)
    plt.figure(figsize=(14, 15))
    heat = sns.heatmap(df2, annot=True, fmt=".1%")
    st.pyplot(fig=heat.figure)
    df['pos'] = df['summary'].str.find(']')+1

    df['tos'] = df.apply(lambda x: x['summary'][0:x['pos']],axis=1)
    dflower= df.applymap(lambda s:s.lower() if type(s) == str else s)
    dflower["tos"].replace({"[superchats]": "[donation reading]", "[superchat reading]": "[donation reading]", "[superchat]": "[donation reading]","[member]":"[members]"}, inplace=True)
    dflower["tos"].replace({"[song cover release]": "[song release]","[cover release]": "[song release]", "[song cover]": "[song release]","[member]":"[members]"}, inplace=True) #normalise here. I-
    dflower["tos"].replace({"[mv premiere]": "[mv]","[mv release]": "[mv]", "[ep release]": "[ep release]","[ep trailer]":"[ep release]"}, inplace=True)
    dflower["tos"].replace({"[chess tournament]": "[chess]","[chatthing]": "[chatting]", "[drawing]": "[art]","[pi]":"[math]","":"[chatting]","[holoro relay]":"[gaming]", "[maths]":"[math]","[language]":"[chatting]","[celebration]":"[chatting]"}, inplace=True)

    df3 = pd.crosstab(dflower['tos'], df['weeknum'],margins=True,normalize='all')
    df3.drop(df3.tail(1).index, inplace=True)
    df3 = df3.drop('All',1)
    plt.figure(figsize=(14, 17))
    heat2 = sns.heatmap(df3, annot=True, fmt=".1%")
    st.pyplot(fig=heat2.figure)
option = st.selectbox(
     'Who\'s your oshi?',
     ('Risu', 'Reine', 'Ollie'))
if (option == "Risu"):
    get_plots("Risu")
elif option == "Reine":
    get_plots("Reine")
elif option == "Ollie":
    get_plots("Ollie")
elif option == "Mori":
    get_plots("Mori")