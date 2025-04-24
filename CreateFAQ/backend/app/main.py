from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import faq, jobs
import uvicorn

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Include the FAQ router
app.include_router(faq.router)
app.include_router(jobs.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FAQ API!"}


# Main entry point
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

# run `python -m app.main`` in CreateFAQ/backend path
