from fastapi import FastAPI

from workhub.api.routes.users import router as user_router


app = FastAPI(
    title="WorkHub",
    version="1.0.0",
)


app.include_router(user_router)


@app.get("/")
async def root():
    return {
        "message": "WorkHub API is running"
    }