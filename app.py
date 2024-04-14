import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def sidebar_filters(data):
    st.sidebar.markdown("Select a range on the slider (it represents movie score) to view the total number of movies in a genre that falls within that range")
    min_score, max_score = st.sidebar.slider("Choose a value:", 0.0, 10.0, value=(3.0, 4.0), step=0.1)
    
    st.sidebar.markdown("Select your preferred genre(s) and year to view the movies released that year and on that genre")
    genre = data['genre'].unique()   
    selected_genre = st.sidebar.multiselect('Select Genre', genre, default=['Animation','Horror','Fantasy','Romance'])
    
    years = data['year'].unique().astype(str)
    selected_year = st.sidebar.selectbox('Select Year', years)

    return selected_year, selected_genre, min_score, max_score

def main():
    st.set_page_config(layout="wide")

    st.header("Interactive Dashboard")
    movies_data = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/movies.csv")
    movies_data.dropna()
    
    movies_data['score'] = pd.to_numeric(movies_data['score'], errors='coerce')
    movies_data['year'] = movies_data['year'].astype(str)
    
    row_1, row_2 = st.columns([5,5])
    selected_year, selected_genre, min_score, max_score = sidebar_filters(movies_data)
    with row_1:    
        st.subheader("Lists of movies filtered by year and Genre")
        filtered_data = movies_data[(movies_data['year'] == selected_year) & (movies_data['genre'].isin(selected_genre))]
        df = pd.DataFrame(filtered_data, columns=('name', 'genre', 'year'))
        st.dataframe(df.reset_index(drop=True), height=350, width=1000)
        
    with row_2:
        st.subheader("User Score of Movies and Their Genre")

        plotly_data = movies_data[(movies_data['score'] >= min_score) & (movies_data['score'] <= max_score)]
        avg_user_score = plotly_data.groupby('genre')['score'].count()

        figpx = go.Figure(data=go.Scatter(x=avg_user_score.index, y=avg_user_score.values, mode='lines+markers'), 
                        layout=dict(xaxis=dict(showgrid=True, gridcolor='white', gridwidth=1),
                                    yaxis=dict(showgrid=True, gridcolor='white', gridwidth=1),
                                    width=650, plot_bgcolor='#202324',
                                    margin=dict(t=50)))  # Điều chỉnh margin ở trên
        st.plotly_chart(figpx)

    st.write("""Average Movie Budget, Grouped by Genre""")
    avg_budget = movies_data.groupby('genre')['budget'].mean().round()
    avg_budget = avg_budget.reset_index()
    genre = avg_budget['genre']
    avg_bud = avg_budget['budget']

    fig = plt.figure(figsize = (19, 10))
    plt.bar(genre, avg_bud, color = 'maroon')
    plt.xlabel('genre')
    plt.ylabel('budget')
    plt.title('Matplotlib Bar Chart Showing the Average Budget of Movies in Each Genre')
    
    st.pyplot(fig)

if __name__ == "__main__":
    main()
