from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sqlite3
from datetime import datetime, timedelta
from enum import Enum


class StatusEnum(str, Enum):
    Open = "Open"
    InProgress = "In Progress"
    Closed = "Closed"


app = FastAPI(title="Customer Support Ticket API")


class TicketCreate(BaseModel):
    title: str
    description: str
    status: StatusEnum = StatusEnum.Open
    tags: str = ""


DATABASE = "tickets.db"


def create_table():
    connection = sqlite3.connect(DATABASE)

    connection.execute("""
       CREATE TABLE IF NOT EXISTS tickets (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       title TEXT NOT NULL,
       description TEXT NOT NULL,
       status TEXT NOT NULL,
       tags TEXT,
       created_at TEXT NOT NULL,
       response_deadline TEXT NOT NULL
       )
    """)

    connection.commit()
    connection.close()


create_table()


@app.get("/")
def home():
    return {"message": "Customer Support Ticket API is running"}


@app.post("/tickets")
def create_ticket(ticket: TicketCreate):

    connection = sqlite3.connect(DATABASE)
    created_at = datetime.now()
    response_deadline = calculate_response_deadline(created_at)

    cursor = connection.execute(

        """
        INSERT INTO tickets (title, description, status, tags, created_at, response_deadline)
        VALUES (?, ?, ?, ?, ?,?)
        """,
        (
            ticket.title,
            ticket.description,
            ticket.status,
            ticket.tags,
            created_at.isoformat(),
            response_deadline.isoformat()
        )
    )

    connection.commit()

    ticket_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Ticket created successfully",
        "id": ticket_id
    }


@app.get("/tickets")
def get_tickets():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    tickets = connection.execute(
        "SELECT * FROM tickets"
    ).fetchall()

    connection.close()

    return [dict(ticket) for ticket in tickets]


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    ticket = connection.execute(
        "SELECT * FROM tickets WHERE id = ?",
        (ticket_id,)
    ).fetchone()

    connection.close()

    if ticket is None:
        return {"message": "Ticket not found"}

    return dict(ticket)


@app.post("/tickets/web-submit", response_class=HTMLResponse)
def web_submit(ticket: TicketCreate):

    connection = sqlite3.connect(DATABASE)

    created_at = datetime.now()
    response_deadline = calculate_response_deadline(created_at)

    connection.execute(
        """
        INSERT INTO tickets
        (title, description, status, tags, created_at, response_deadline)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            ticket.title,
            ticket.description,
            ticket.status,
            ticket.tags,
            created_at.isoformat(),
            response_deadline.isoformat()
        )
    )

    connection.commit()
    connection.close()

    return "<h1>Ticket Created Successfully!</h1>"


def calculate_response_deadline(created_at):
    current_date = created_at
    business_days = 0

    while business_days < 3:
        current_date += timedelta(days=1)

        if current_date.weekday() < 5:
            business_days += 1

    return current_date
