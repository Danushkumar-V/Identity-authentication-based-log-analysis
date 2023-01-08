from functions import imgprocessing as im
from functions import webcam
import streamlit as st
from App_functions import webfun as wb
import pandas as pd
import datetime
import plotly.express as px
st.set_page_config(
    page_title="Real-Time Identity Authentication",
    page_icon="🌟",
)

imagedirpath = "D:\DK\Dev\Face rec\ImageAttendence"
df = pd.read_csv("D:\DK\Dev\Face rec\Files\Dataset2.csv")
encoded_list , imgclasses= im.do_encoding(imagedirpath)
 
st.header("Identity authentication based log analysis")

option = st.selectbox(
     'Select from the options below ! ',
     ('None','Live video stream', 'Log analysis'))

if(option == "Live video stream"):
    st.header("Live video stream !")
    webcam.showvideo(encoded_list , imgclasses)

elif(option == "Log analysis"):
    st.header("Log analysis")
    
    
    options = st.selectbox("Select one among the option ", ("Overall","By person"))
    a,b = st.columns(2)
    if(options == "Overall"):
        nowdaytime = datetime.datetime.now()
        date = nowdaytime.strftime('%d-%m-%Y')
        present_std,present_count = wb.dailyattendence(date, df)
        Absent_std = wb.getabs(imgclasses, present_std)
        a.header("")
        b.header("")
        a.metric(
            label="Present 👨‍⚖️",
            value=present_count,
            delta= - len(Absent_std),
        )
        b.metric(
            label="Absent 👨‍⚖️",
            value=len(Absent_std),
            delta= present_count,
        )
        d = pd.unique(df["Date"]).tolist()
        d.sort()
        abs_every_date = []
        for i in d:
            a = wb.abs_value(i,imgclasses,df)
            abs_every_date.append(len(a))

        abs_df = pd.DataFrame()

        abs_df["Date"] = d
        abs_df["Absent"] = abs_every_date
        fig = px.bar(abs_df, x='Date', y='Absent',
                    hover_data=['Date', 'Absent'], color='Absent',
                    labels={'pop':'Absent count :'}, height=400,color_continuous_scale=px.colors.sequential.Darkmint_r,title = 'Absentees Count daty by day:')
        st.plotly_chart(fig,use_container_width = True)
        c1,c2,c3 = st.columns(3)
        today = datetime.date.today()
        date_select = c2.date_input('Select date for absentees list', today)
        date_select_str = date_select.strftime('%d-%m-%Y')
        abs_value = wb.abs_value(date_select_str,imgclasses,df)
        st.write(abs_value)
        
    elif(options == "By person"):
        std = a.selectbox("Student", imgclasses)
        today = datetime.date.today()
        date_select = b.date_input('Select date', today)
        date_select_str = date_select.strftime('%d-%m-%Y')
        unique_date = pd.unique(df["Date"])
        if(date_select_str not in unique_date):
            st.warning("No data entered in this particular day")
        else:
            intime, outtime,total_time,flag = wb.calc_in_out(std,date_select_str,df)
            if(flag == 1):
                per_day,no_of_logs = wb.getdata(std, df)
                total_time_str = ("{}").format(total_time).replace(":","-")
                st.markdown("***")
                a1,b1,c1 = st.columns(3)
                total_working_days,total_present_days,total_absent_days = wb.get_std_data(std,df)
                pres_abs_df = wb.df_create(total_absent_days,total_present_days)
                a1.metric(
                    label = "IN TIME",
                    value = datetime.time.strftime(intime.time(), "%H-%M-%S") ,
                )
                b1.metric(
                    label = "OUT TIME",
                    value = datetime.time.strftime(outtime.time(), "%H-%M-%S") ,
                )
                c1.metric(
                    label = "TOTAL TIME IN",
                    value = total_time_str,
                )
                st.markdown("***")
                a2,b2,c2 = st.columns(3)
                a2.metric(
                    label = "TOTAL NO. OF WORKING DAYS",
                    value = total_working_days,
                )
                b2.metric(
                    label = "NO. OF DAYS PRESENT",
                    value = total_present_days,
                    delta=  - total_absent_days,
                )
                c2.metric(
                    label = "NO. OF DAYS ABSENT",
                    value = total_absent_days,
                    delta = total_present_days,
                )
                st.markdown("***")
                a3,b3 = st.columns(2)
                fig2 = px.pie(pres_abs_df,hole = 0.5, values='y', names='x', title='Present / Absent pie chart :',color_discrete_sequence=px.colors.sequential.Darkmint_r)

                b3.plotly_chart(fig2,use_container_width = True)
                late_data = wb.late_entry(std,df)
                fig = px.bar(late_data, x='No. of late entries', y='No. of on time entries',
             hover_data=['No. of late entries', 'No. of on time entries'], color='No. of on time entries',
             labels={'pop':'Late entries :'}, height=400,color_continuous_scale=px.colors.sequential.Tealgrn,title = 'Sales amount by zone:')

                a3.plotly_chart(fig,use_container_width = True)


        

