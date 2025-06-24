# Airbnb Search Web Application

A full-stack web application that allows users to search for Airbnb listings in any city for specific dates. The application features a modern React frontend with a calendar interface and a Flask backend that handles the Airbnb API integration, all containerized for easy local development.

## Features

- 🏠 Search for Airbnb listings in any city
- 📅 User-friendly calendar interface for selecting check-in and check-out dates
- 💾 Automatically saves search results to CSV files
- 🎨 Modern Material-UI interface
- 🔄 Real-time search results display
- ⚡ Fast and responsive design

## Tech Stack

### Frontend
- React (frontend/)
- Material-UI
- Axios for API calls
- Date-fns for date handling

### Backend
- Flask (app.py, models.py, config.py)
- Flask-CORS
- Flask-SQLAlchemy
- pyairbnb (Airbnb API wrapper, src/pyairbnb/)
- PostgreSQL (via Docker)

## Project Structure

```
.
├── app.py                # Flask backend entry point
├── models.py             # SQLAlchemy models
├── config.py             # Configuration
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # Docker Compose setup
├── Dockerfile            # Backend Dockerfile
├── wait-for-it.sh        # Script to wait for DB
├── frontend/             # React frontend
│   ├── src/              # React source code
│   └── public/           # Static files
├── src/pyairbnb/         # Airbnb API wrapper and utilities
├── details_data.csv      # Output CSV (auto-generated)
├── search_results.csv    # Output CSV (auto-generated)
├── search_results_from_url.csv # Output CSV (auto-generated)
└── ...
```

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) and Docker Compose

## Running the Application with Docker

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Build and start the containers:**
   ```bash
   docker-compose up --build
   ```
   This will start:
   - The Flask backend (http://localhost:5000)
   - A PostgreSQL database (http://localhost:5432)

3. **Start the React frontend:**
   In a new terminal, run:
   ```bash
   cd frontend
   npm install
   npm start
   ```
   The frontend will run on http://localhost:3000

> **Note:** You can also add a Dockerfile and service for the frontend if you want to run it in a container as well.

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
