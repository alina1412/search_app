import uvicorn

from service.config import app
from service.endpoints.delete_handlers import api_router as delete_routes
from service.endpoints.get_handlers import api_router as get_routes

app.include_router(get_routes)
app.include_router(delete_routes)


if __name__ == "__main__":
    uvicorn.run("service.__main__:app", host="0.0.0.0", port=8000, reload=True)
