from fastapi import FastAPI
from app.core.log_config import setup_logging
from app.api.v1.routes import users, events
import logging

setup_logging()
logger = logging.getLogger(__name__)
logger.info("✅ Json logging works!")
app = FastAPI()

app.include_router(users.router,prefix="/api/v1/users", tags=["Users"])
app.include_router(events.router, prefix="/api/v1/events", tags=["Events"])

@app.get("/")
def root():
    return {"message": "Event CRM API is running"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
