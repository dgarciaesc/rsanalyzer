# Airbnb Search Web Application

A full-stack web application that allows users to search for Airbnb listings in any city for specific dates. The application features a modern React frontend with a calendar interface and a Flask backend that handles the Airbnb API integration.

## Features

- 🏠 Search for Airbnb listings in any city
- 📅 User-friendly calendar interface for selecting check-in and check-out dates
- 💾 Automatically saves search results to CSV files
- 🎨 Modern Material-UI interface
- 🔄 Real-time search results display
- ⚡ Fast and responsive design

## Tech Stack

### Frontend
- React
- Material-UI
- Axios for API calls
- Date-fns for date handling

### Backend
- Flask
- Flask-CORS
- pyairbnb (Airbnb API wrapper)

## Prerequisites

- Python 3.7+
- Node.js 14+
- npm or yarn

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install Python dependencies:
```bash
pip install flask flask-cors pyairbnb
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

## Running the Application

1. Start the Flask backend:
```bash
# From the root directory
python app.py
```
The backend will run on http://localhost:5000

2. Start the React frontend:
```bash
# From the frontend directory
npm start
```
The frontend will run on http://localhost:3000

## How to Use

1. Open your browser and navigate to http://localhost:3000
2. Enter the city name in the location field
3. Select check-in and check-out dates using the calendar interface
4. Click the "Search" button
5. View the search results displayed on the page
6. The results will also be automatically saved to a CSV file in the backend directory

## API Endpoints

### POST /api/search
Search for Airbnb listings with the following parameters:
- `check_in`: Check-in date (YYYY-MM-DD)
- `check_out`: Check-out date (YYYY-MM-DD)
- `location`: City name
- `currency`: Currency code (default: EUR)
- `locale`: Language code (default: en)

## Output Files

The application automatically saves search results to CSV files:
- `search_results.csv`: Contains the latest search results
- `details_data.csv`: Contains detailed information about specific listings
- `search_results_from_url.csv`: Contains results from URL-based searches

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
