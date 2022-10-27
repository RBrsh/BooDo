from fastapi import FastAPI
import sqlalchemy

boo_do = FastAPI()


@boo_do.get("/")
def root():
    return {"message": "Stub for get."}


@boo_do.post("/")
def root():
    return {"message": "Stub for post."}


@boo_do.put("/")
def root():
    return {"message": "Stub for put."}


@boo_do.delete("/")
def root():
    return {"message": "Stub for delete."}


def create_todo():
    pass


def get_todo():
    pass


def update_todo():
    pass


def delete_todo():
    pass
