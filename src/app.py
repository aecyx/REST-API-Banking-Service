from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database.migrations import run_migrations
from src.routes import accounts, transactions, transfers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform any startup tasks here (e.g., database connection)
    print("Starting up the application...")
    run_migrations()
    yield
    # Perform any shutdown tasks here (e.g., closing database connection)
    print("Shutting down the application...")

app = FastAPI(lifespan=lifespan)

app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(transfers.router)