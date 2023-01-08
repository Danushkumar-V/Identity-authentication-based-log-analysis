from datetime import datetime
import pandas as pd
import streamlit as st

def dailyattendence(date,df):
    present_list = df["Name "].loc[df["Date"] == date]
    present_std = pd.unique(present_list).tolist()
    present_count = len(present_std)
    return present_std,present_count

def calc_in_out(a,b,df):
    data_af_filter = df.loc[(df['Name '] == a) & (df['Date'] == b)]
    e = data_af_filter['Time'].tolist()
    if(len(e)!=0):

        intime = datetime.strptime(e[0], "%H-%M-%S")
        outtime = datetime.strptime(e[len(e)-1], "%H-%M-%S")
        
        total_time = outtime - intime
        return intime, outtime,total_time, 1

    else:
        st.warning("He / She is absent on that day!")
        return 0, 0, 0 , 0


def getdata(a,df):
    data_af_filter = df.loc[df['Name '] == a]
    no_of_logs = data_af_filter['Date'].value_counts().tolist()
    per_day = data_af_filter['Date'].value_counts().index.tolist()
    return per_day,no_of_logs

def getabs(std, present_std):
    Absent_std = []
    for i in std: 
        if(i not in present_std):
            Absent_std.append(i)
    return Absent_std

def get_std_data(std, df):
    total_working_days = len(pd.unique(df["Date"]).tolist())
    total_present_days = len(pd.unique(df["Date"].loc[df["Name "]==std]).tolist())
    total_absent_days = total_working_days - total_present_days
    return total_working_days,total_present_days,total_absent_days

def df_create(total_absent_days,total_present_days):
    df2 = pd.DataFrame()
    x = ["Total absent days","Total present days"]
    y = [total_absent_days,total_present_days]
    df2["x"] = x
    df2["y"] = y
    return df2

def intime(a,b,df):
    data_af_filter = df.loc[(df['Name '] == a) & (df['Date'] == b)]
    e = data_af_filter['Time'].tolist()
    e.sort()
    return e[0]


def late_entry(a,df):
    data_af_filter = df.loc[(df['Name '] == a)]
    f = pd.unique(data_af_filter['Date']).tolist()
    intime_ttl = []
    late_intime = []
    for i in f:
        intime1 = intime(a,i,df)
        intime_ttl.append(intime1)
    for j in intime_ttl:
        if str(j) >= "08-45-00":
            late_intime.append(j)
    count_late = len(late_intime)
    count_crct = len(intime_ttl) - count_late
    df2 = pd.DataFrame()
    x = ["No. of late entries","No. of on time entries"]
    y = [count_late,count_crct]
    df2['No. of late entries'] = x
    df2['No. of on time entries'] = y
    return df2

def abs_value(date,total_classes,df):
    filter_df = df["Name "].loc[df["Date"] == date]
    present_list = pd.unique(filter_df).tolist()
    present_list.sort()
    absent_list = []
    for i in total_classes:
        if i not in present_list:
            absent_list.append(i)
    return absent_list