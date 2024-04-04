import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px




st.title ("Job Posting Analysis of DataScientists 2024")
st.sidebar.title ("Job Posting Analysis of DataScientists 2024")

st.markdown ("This application is about to analyze the job postings of DataScientists")
st.sidebar.markdown ("This application is about to analyze the job postings of DataScientists")

Data_URL = ('job_postings.csv')

@st.cache_data(persist=True)

def load_data():
    data = pd.read_csv(Data_URL)
    data['first_seen'] = pd.to_datetime(data['first_seen'])
    return data
data = load_data()

st.sidebar.subheader("Show Random Job Type")
random_job_type = st.sidebar.radio ('job type', ('Onsite','Remote','Hybrid'))

# st.sidebar.markdown (data.query('job_type==@random_job_type')[["job_title","job_link"]].sample(n=1).iat[0,0])

random_job = data.query('job_type == @random_job_type')[["job_title", "job_link"]].sample(n=1)

job_title = random_job.iloc[0]["job_title"]
job_link = random_job.iloc[0]["job_link"]

st.sidebar.markdown(f"[{job_title}]({job_link})")

st.sidebar.markdown("### Number of Jobs by Job Type")
select = st.sidebar.selectbox('Visualization type', ['Histogram' , 'pie chart'], key='1')
job_type_count = data['job_type'].value_counts()

job_type_count = pd.DataFrame({'Job Type':job_type_count.index, 'Jobs':job_type_count.values})

if not st.sidebar.checkbox("Hide",True ):
    st.markdown ("### Number of Jobs by Job Type")
    if select == "Histogram":
        fig = px.bar(job_type_count,x='Job Type',y='Jobs',color='Jobs')
        st.plotly_chart(fig)
    else:
        fig =  px.pie(job_type_count,values='Jobs', names='Job Type')
        st.plotly_chart(fig)





