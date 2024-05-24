from fastapi import FastAPI
from routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins=[
    "https://hidden-caverns-01384-1c5c4dad7960.herokuapp.com",
    "http://www.ps99clanbattlestats.com",
    "https://www.ps99clanbattlestats.com",
    "http://www.ps99clanbattlestats.io",
    "https://www.ps99clanbattlestats.io",
    "ps99clanbattlestats.com",
    "ps99clanbattlestats.io"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the SOUP Clan Battle Tracker API"}
