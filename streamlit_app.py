import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(
    page_title="Pokémon Tournament Data Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('pokemon_tournament_data.csv')
    # Clean up the Deck names for better display
    df['Deck'] = df['Deck'].str.replace('-', ' ').str.title()
    return df

# Load data
df = load_data()

# Sidebar filters
st.sidebar.title("🎮 Pokémon Tournament Dashboard")
st.sidebar.markdown("Filter and analyze tournament data")

# Deck filter
deck_options = ['All'] + sorted(df['Deck'].unique().tolist())
selected_deck = st.sidebar.selectbox('Select Deck', deck_options)

# Country filter
country_options = ['All'] + sorted(df['Country'].unique().tolist())
selected_country = st.sidebar.selectbox('Select Country', country_options)

# Placement range
min_placement = st.sidebar.number_input('Min Placement', min_value=1, max_value=df['Placement'].max(), value=1)
max_placement = st.sidebar.number_input('Max Placement', min_value=1, max_value=df['Placement'].max(), value=df['Placement'].max())

# Apply filters
filtered_df = df.copy()

if selected_deck != 'All':
    filtered_df = filtered_df[filtered_df['Deck'].str.contains(selected_deck, case=False, na=False)]

if selected_country != 'All':
    filtered_df = filtered_df[filtered_df['Country'].str.upper() == selected_country.upper()]

filtered_df = filtered_df[(filtered_df['Placement'] >= min_placement) & (filtered_df['Placement'] <= max_placement)]

# Main content
st.title("🎮 Pokémon Tournament Data Explorer")
st.markdown("---")

# Statistics cards
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Players", len(filtered_df))

with col2:
    st.metric("Unique Decks", len(filtered_df['Deck'].unique()))

with col3:
    if not filtered_df.empty:
        top_deck = filtered_df['Deck'].value_counts().idxmax()
        st.metric("Top Deck", top_deck)
    else:
        st.metric("Top Deck", "N/A")

with col4:
    if not filtered_df.empty:
        top_country = filtered_df['Country'].value_counts().idxmax()
        st.metric("Top Country", top_country)
    else:
        st.metric("Top Country", "N/A")

with col5:
    if not filtered_df.empty:
        avg_placement = round(filtered_df['Placement'].mean(), 2)
        st.metric("Avg Placement", avg_placement)
    else:
        st.metric("Avg Placement", "N/A")

st.markdown("---")

# Charts section
col1, col2 = st.columns(2)

with col1:
    st.subheader("Deck Distribution")
    if not filtered_df.empty:
        deck_counts = filtered_df['Deck'].value_counts().head(10)
        fig = px.pie(
            values=deck_counts.values,
            names=deck_counts.index,
            title="Top 10 Decks"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters")

with col2:
    st.subheader("Country Distribution")
    if not filtered_df.empty:
        country_counts = filtered_df['Country'].value_counts().head(10)
        fig = px.bar(
            x=country_counts.index,
            y=country_counts.values,
            title="Top 10 Countries"
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters")

# Deck Performance Analysis
st.subheader("📊 Deck Performance Analysis")

# Calculate deck statistics
deck_stats = filtered_df.groupby('Deck').agg({
    'Placement': 'mean',
    'Name': 'count',
    'Points': 'mean',
    'Wins': 'sum',
    'Losses': 'sum',
    'Ties': 'sum'
}).rename(columns={
    'Name': 'count',
    'Placement': 'avg_placement',
    'Points': 'avg_points',
    'Wins': 'total_wins',
    'Losses': 'total_losses',
    'Ties': 'total_ties'
}).sort_values('count', ascending=False).reset_index()

# Calculate win rates
deck_stats['total_matches'] = deck_stats['total_wins'] + deck_stats['total_losses'] + deck_stats['total_ties']
deck_stats['win_rate'] = deck_stats.apply(
    lambda x: (x['total_wins'] + 0.5 * x['total_ties']) / x['total_matches'] * 100 
    if x['total_matches'] > 0 else 0, 
    axis=1
)

if not deck_stats.empty:
    # Display deck stats table
    st.dataframe(
        deck_stats[['Deck', 'count', 'avg_placement', 'win_rate', 'avg_points']].round(2),
        column_config={
            "Deck": "Deck Name",
            "count": "Players",
            "avg_placement": "Avg Placement",
            "win_rate": "Win Rate (%)",
            "avg_points": "Avg Points"
        },
        hide_index=True
    )
    
    # Win rate vs Placement scatter plot
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Win Rate vs Average Placement")
        fig = px.scatter(
            deck_stats,
            x='avg_placement',
            y='win_rate',
            size='count',
            hover_name='Deck',
            title="Deck Performance Analysis"
        )
        fig.update_layout(xaxis_title="Average Placement", yaxis_title="Win Rate (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top Decks by Win Rate")
        top_winrate = deck_stats.nlargest(10, 'win_rate')
        fig = px.bar(
            top_winrate,
            x='win_rate',
            y='Deck',
            orientation='h',
            title="Top 10 Decks by Win Rate"
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

# Detailed Data Table
st.subheader("📋 Detailed Tournament Data")

if not filtered_df.empty:
    # Allow users to select columns to display
    all_columns = filtered_df.columns.tolist()
    selected_columns = st.multiselect(
        "Select columns to display",
        all_columns,
        default=['Name', 'Country', 'Deck', 'Placement', 'Points', 'Wins', 'Losses']
    )
    
    if selected_columns:
        # Sort options
        sort_column = st.selectbox("Sort by", selected_columns)
        sort_order = st.radio("Sort order", ["Ascending", "Descending"])
        
        # Apply sorting
        sorted_df = filtered_df.sort_values(
            by=sort_column, 
            ascending=(sort_order == "Ascending")
        )
        
        # Display data
        st.dataframe(
            sorted_df[selected_columns],
            use_container_width=True,
            hide_index=True
        )
else:
    st.warning("No data available for the selected filters")

# Footer
st.markdown("---")
st.markdown("🎮 Pokémon Tournament Data Dashboard | Built with Streamlit")
