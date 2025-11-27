from fastapi import FastAPI

from registerRoute import router as registerRouter

app = FastAPI()
app.include_router(registerRouter)
