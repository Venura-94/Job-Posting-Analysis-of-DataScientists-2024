import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


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

st.sidebar.markdown("### Number of Jobs by Job Type & Job Level")
select = st.sidebar.selectbox('Visualization type', ['Histogram' , 'pie chart'], key='1')
job_type_count = data['job_type'].value_counts()

job_type_count = pd.DataFrame({'Job Type':job_type_count.index, 'Jobs':job_type_count.values})

hide_checkbox_key = "hide_checkbox"

# Use the unique key for the checkbox
if not st.sidebar.checkbox("Hide Job Type", True, key=hide_checkbox_key):
    st.markdown("### Number of Jobs by Job Type")
    if select == "Histogram":
        fig = px.bar(job_type_count, x='Job Type', y='Jobs', color='Jobs')
        st.plotly_chart(fig)
    else:
        fig = px.pie(job_type_count, values='Jobs', names='Job Type')
        st.plotly_chart(fig)

if not st.sidebar.checkbox("Hide Job Level", True, key=hide_checkbox_key + "_level"):
    st.markdown("### Number of Jobs by Job Level")
    if select == "Histogram":
        job_level_counts = data['job_level'].value_counts().reset_index()
        job_level_counts.columns = ['Job Level', 'Count']
        fig_bar = px.bar(job_level_counts, x='Job Level', y='Count', color='Job Level', title='Distribution of Job Levels')
        st.plotly_chart(fig_bar)
    else:
        job_level_counts = data['job_level'].value_counts().reset_index()
        job_level_counts.columns = ['Job Level', 'Count']
        fig_pie = px.pie(job_level_counts, values='Count', names='Job Level', title='Distribution of Job Levels')
        st.plotly_chart(fig_pie)

# Show Raw Data According to Job Type
st.sidebar.markdown("### Show Raw Data According to Job Type")
selected_job_type = st.sidebar.selectbox("Select Job Type", ['Onsite', 'Remote', 'Hybrid'])

# Filter data based on selected job type
filtered_data = data[data['job_type'] == selected_job_type]

# Display filtered raw data
st.subheader(f"Raw Data for {selected_job_type} Jobs")
st.dataframe(filtered_data[['job_link', 'job_title', 'company', 'job_location']])

st.sidebar.header("Word Cloud")
job_type1 = st.sidebar.radio('Display word cloud for Job Location', ('Onsite', 'Remote', 'Hybrid'))

st.set_option('deprecation.showPyplotGlobalUse', False)
if not st.sidebar.checkbox("Close", True, key='3'):
    st.subheader('Word Cloud for %s Job Type to Show Job Location' % (job_type1))
    df = data[data['job_type'] == job_type1]

    # Preprocess job locations
    job_locations = df['job_location'].str.replace('-', ',').str.split(',')
    all_locations = [location.strip() for sublist in job_locations.dropna() for location in sublist]
    text = ' '.join(all_locations)

    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Plot word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot()







