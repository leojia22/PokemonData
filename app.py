from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
import json

app = Flask(__name__)

# Load the data
DATA_FILE = 'pokemon_tournament_data.csv'

def load_data():
    df = pd.read_csv(DATA_FILE)
    # Clean up the Deck names for better display
    df['Deck'] = df['Deck'].str.replace('-', ' ').str.title()
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    df = load_data()
    
    # Apply filters if any
    deck_filter = request.args.get('deck')
    country_filter = request.args.get('country')
    min_placement = request.args.get('min_placement')
    max_placement = request.args.get('max_placement')
    
    if deck_filter and deck_filter != 'All':
        df = df[df['Deck'].str.contains(deck_filter, case=False, na=False)]
    if country_filter and country_filter != 'All':
        df = df[df['Country'].str.upper() == country_filter.upper()]
    if min_placement:
        df = df[df['Placement'] >= int(min_placement)]
    if max_placement:
        df = df[df['Placement'] <= int(max_placement)]
    
    # Convert to list of dictionaries for JSON serialization
    data = df.to_dict('records')
    
    # Get unique values for filters
    decks = ['All'] + sorted(df['Deck'].unique().tolist())
    countries = ['All'] + sorted(df['Country'].unique().tolist())
    
    # Calculate some basic statistics
    stats = {
        'total_players': len(df),
        'unique_decks': len(df['Deck'].unique()),
        'top_deck': df['Deck'].value_counts().idxmax() if not df.empty else 'N/A',
        'top_country': df['Country'].value_counts().idxmax() if not df.empty else 'N/A',
        'average_placement': round(df['Placement'].mean(), 2) if not df.empty else 0,
    }
    
    return jsonify({
        'data': data,
        'filters': {
            'decks': decks,
            'countries': countries,
            'min_placement': 1,
            'max_placement': int(df['Placement'].max()) if not df.empty else 0
        },
        'stats': stats
    })

@app.route('/api/decks')
def get_deck_stats():
    df = load_data()
    
    # Calculate total wins and losses for each deck
    deck_stats = df.groupby('Deck').agg({
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
    
    # Calculate average wins and losses
    deck_stats['avg_wins'] = deck_stats['total_wins'] / deck_stats['count']
    deck_stats['avg_losses'] = deck_stats['total_losses'] / deck_stats['count']
    
    # Convert to list of dictionaries for JSON serialization
    result = deck_stats.to_dict('records')
    
    # Add a color field for the pie chart using a simple color palette
    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
        '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5'
    ]
    
    for i, deck in enumerate(result):
        deck['color'] = colors[i % len(colors)]
    
    return jsonify(result)

@app.route('/api/winrate-stats')
def get_winrate_stats():
    df = load_data()
    
    # Calculate win rate statistics for each deck
    deck_stats = df.groupby('Deck').agg({
        'Name': 'count',
        'Wins': 'sum',
        'Losses': 'sum',
        'Ties': 'sum',
        'Placement': ['mean', 'min', 'max'],
        'Points': 'mean'
    })
    
    # Flatten the multi-index columns
    deck_stats.columns = ['_'.join(col).strip('_') for col in deck_stats.columns.values]
    deck_stats = deck_stats.rename(columns={
        'Name_count': 'player_count',
        'Wins_sum': 'total_wins',
        'Losses_sum': 'total_losses',
        'Ties_sum': 'total_ties',
        'Placement_mean': 'avg_placement',
        'Placement_min': 'best_placement',
        'Placement_max': 'worst_placement',
        'Points_mean': 'avg_points'
    }).reset_index()
    
    # Calculate win rate (handling division by zero)
    deck_stats['total_matches'] = deck_stats['total_wins'] + deck_stats['total_losses'] + deck_stats['total_ties']
    deck_stats['win_rate'] = deck_stats.apply(
        lambda x: (x['total_wins'] + 0.5 * x['total_ties']) / x['total_matches'] * 100 
        if x['total_matches'] > 0 else 0, 
        axis=1
    )
    
    # Add color based on average placement (better placement = greener)
    max_placement = deck_stats['avg_placement'].max()
    min_placement = deck_stats['avg_placement'].min()
    placement_range = max_placement - min_placement if max_placement > min_placement else 1
    
    def get_color(placement):
        if pd.isna(placement):
            return '#CCCCCC'
        # Scale from red (bad placement) to green (good placement)
        normalized = (max_placement - placement) / placement_range
        r = int(255 * (1 - normalized))
        g = int(255 * normalized)
        b = 0
        return f'rgb({r},{g},{b})'
    
    deck_stats['color'] = deck_stats['avg_placement'].apply(get_color)
    
    # Convert to list of dictionaries for JSON serialization
    result = deck_stats.to_dict('records')
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
