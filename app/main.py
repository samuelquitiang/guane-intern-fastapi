from fastapi import FastAPI
import dogs, authentication, users

app = FastAPI()

app.include_router(authentication.router)
app.include_router(dogs.router)
app.include_router(users.router)