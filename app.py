import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def sidebar_filters(data):
    st.sidebar.markdown("Select a range on the slider (it represents movie score) to view the total number of movies in a genre that falls within that range")
    min_score, max_score = st.sidebar.slider("Choose a value:", min_value=data['score'].min(), max_value=data['score'].max(), value=(3.0, 4.0), step=0.1)
    
    st.sidebar.markdown("Select your preferred genre(s) and year to view the movies released that year and on that genre")
    genre = data['genre'].unique()   
    selected_default = list(genre)[:4]
    selected_genre = st.sidebar.multiselect('Select Genre', genre, default=selected_default)
    
    years = data['year'].unique().astype(str)
    selected_year = st.sidebar.selectbox('Select Year', years)

    return selected_year, selected_genre, min_score, max_score

def main():
    st.set_page_config(layout="wide")

    st.header("Interactive Dashboard")
    movies_data = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/movies.csv")
    movies_data.dropna(inplace=True)
    movies_data['score'] = pd.to_numeric(movies_data['score'], errors='coerce')
    movies_data['year'] = movies_data['year'].astype(str)
    
    row_1, row_2 = st.columns([5,5])
    selected_year, selected_genre, min_score, max_score = sidebar_filters(movies_data)
    with row_1:    
        st.subheader("Lists of movies filtered by year and Genre")
        filtered_data = movies_data[(movies_data['year'] == selected_year) & (movies_data['genre'].isin(selected_genre))]
        df = pd.DataFrame(filtered_data, columns=('name', 'genre', 'year'))
        st.dataframe(df, height=300, width=1000)
        
    with row_2:
        st.subheader("User Score of Movies and Their Genre")
        
        plotly_data = movies_data[(movies_data['score'] >= min_score) & (movies_data['score'] <= max_score)]
        avg_user_score = plotly_data.groupby('genre')['score'].mean().round(2)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=avg_user_score.index, y=avg_user_score.values, mode='lines+markers', name='User Score'))
        fig.update_layout(xaxis_title='Genre', yaxis_title='Score')
        
        st.plotly_chart(fig)

    st.subheader("Average Movie Budget by Genre")
    avg_budget = movies_data.groupby('genre')['budget'].mean().round()
    avg_budget = avg_budget.reset_index()
    genre_budget = avg_budget['genre']
    avg_budget_value = avg_budget['budget']
    
    fig2, ax2 = plt.subplots(figsize=(12, 8))
    ax2.bar(genre_budget, avg_budget_value, color='maroon')
    ax2.set_xlabel('Genre')
    ax2.set_ylabel('Average Budget')
    ax2.set_title('Average Movie Budget by Genre')
    ax2.tick_params(axis='x', rotation=45)
    st.pyplot(fig2)

if __name__ == "__main__":
    main()
