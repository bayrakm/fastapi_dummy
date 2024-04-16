from fastapi import FastAPI
from .routers import post, user, auth, vote
# from . import models
# from .database import engine
from fastapi.middleware.cors import CORSMiddleware

# connect DB for our sqlalchemy modelling
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def connected():
    return {"message": "you are connected!!!!"}

# to allow where and how people communicate with api
origins = ["*"] # set to everyone for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # which url can send request
    allow_credentials=True,
    allow_methods=["*"], # which methods are allowed to use
    allow_headers=["*"], # which headers are allowed to use
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



