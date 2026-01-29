# Pokemon Tournament Data Dashboard

A Flask-based web application for analyzing and visualizing Pokemon tournament data, including player statistics, deck performance, and win rates.

## Features

- **Dashboard Overview**: View tournament statistics and player data
- **Deck Analysis**: Analyze deck performance, win rates, and popularity
- **Data Filtering**: Filter by deck type, country, and placement range
- **Interactive Charts**: Visual representations of tournament data
- **REST API**: JSON endpoints for data access

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd PokemonData
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Option 1: Flask (Local Development)

1. Make sure you're in the project directory:
```bash
cd PokemonData
```

2. Install Flask dependencies:
```bash
pip install -r requirements.txt
```

3. Start the Flask application:
```bash
python app.py
```

4. Open your web browser and navigate to:
```
http://localhost:5001
```

### Option 2: Streamlit (Cloud Hosting)

1. Install Streamlit dependencies:
```bash
pip install -r requirements_streamlit.txt
```

2. Run the Streamlit app locally:
```bash
streamlit run streamlit_app.py
```

3. For cloud hosting on Streamlit Cloud:
   - Push your code to GitHub
   - Connect your repository to Streamlit Cloud
   - Streamlit will automatically detect and run `streamlit_app.py`

**Note**: Use the Streamlit version for cloud hosting on Streamlit Cloud, as Flask apps are not supported on the platform.

## Project Structure

```
PokemonData/
├── app.py                      # Main Flask application
├── streamlit_app.py           # Streamlit version for cloud hosting
├── requirements.txt           # Flask dependencies
├── requirements_streamlit.txt # Streamlit dependencies
├── pokemon_tournament_data.csv # Tournament data file
├── torontoregionals.txt       # Additional tournament data
├── templates/
│   └── index.html             # Frontend HTML template for Flask
└── README.md                  # This file
```

## API Endpoints

- `GET /` - Main dashboard page
- `GET /api/data` - Get filtered tournament data and statistics
- `GET /api/decks` - Get deck performance statistics
- `GET /api/winrate-stats` - Get detailed win rate statistics for each deck

## Data

The application uses Pokemon tournament data including:
- Player names and countries
- Deck types and archetypes
- Tournament placements and points
- Win/loss/tie records

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Data Processing**: Pandas
- **Frontend**: HTML, CSS, JavaScript
- **Visualization**: Chart.js (via frontend)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.
