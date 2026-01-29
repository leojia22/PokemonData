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

1. Make sure you're in the project directory:
```bash
cd PokemonData
```

2. Start the Flask application:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5001
```

The application will run in debug mode by default.

## Project Structure

```
PokemonData/
├── app.py                      # Main Flask application
├── requirements.txt             # Python dependencies
├── pokemon_tournament_data.csv # Tournament data file
├── torontoregionals.txt       # Additional tournament data
├── templates/
│   └── index.html             # Frontend HTML template
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
