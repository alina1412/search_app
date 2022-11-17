import uvicorn


from service.endpoints.put_handlers import api_router as put_routes
from service.endpoints.get_handlers import api_router as get_routes
from service.endpoints.data_handlers import api_router as data_routes

from service.config import app

app.include_router(put_routes)
app.include_router(get_routes)
app.include_router(data_routes)


if __name__ == "__main__":
    uvicorn.run("service.__main__:app", host="0.0.0.0", port=8000, reload=True)
