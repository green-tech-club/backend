from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.users import user_routes
from api.items import item_routes
origins = [
           "http://localhost:8000",
           "http://localhost:3333",
]

app = FastAPI()
app.include_router(user_routes)
app.include_router(item_routes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello It's Greentech!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)