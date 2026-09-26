# Customer Support Ticket API

A RESTful API for managing customer support tickets built with Python and FastAPI.

## Features

- Create tickets via REST endpoint or web form
- Retrieve all tickets
- Retrieve a single ticket by ID
- Status field restricted to: Open, In Progress, Closed
- Tags stored as comma-separated string
- Automatic calculation of response deadline (3 business days from creation, excluding weekends)

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

Start the server with:
```
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

- `GET /` - Health check
- `POST /tickets` - Create a new ticket (JSON)
- `GET /tickets` - Retrieve all tickets
- `GET /tickets/{ticket_id}` - Retrieve a specific ticket
- `POST /tickets/web-submit` - Create a ticket via web form (returns HTML success message)

## Database

The application uses SQLite and automatically creates a `tickets.db` file in the project directory.

## Note

The virtual environment (`venv/`) and database (`tickets.db`) are excluded from version control via `.gitignore`.