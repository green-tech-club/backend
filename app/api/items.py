from fastapi import APIRouter


item_routes = APIRouter()
# Example dummy route for multiple routing

@item_routes.get("/items")
async def get_item():
    return {"Success":"route added"}
