import os

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from pydub import AudioSegment
from uuid import uuid4

app = FastAPI()

# временная БД
users_db = {}


@app.post("/users/")
async def create_user(username: str):

    user_id = str(uuid4())
    access_token = str(uuid4())
    users_db[user_id] = {"username": username, "access_token": access_token}
    return {"user_id": user_id, "access_token": access_token}



@app.post("/records/")
async def add_record(user_id: str, access_token: str, file: UploadFile = File(...)):

    if user_id in users_db and users_db[user_id]["access_token"] == access_token:

        audio = AudioSegment.from_file(file.file, format="wav")
        record_id = str(uuid4())
        record_url = f"http://host:port/record?id={record_id}&user={user_id}"
        audio.export(f"{record_id}.mp3", format="mp3")
        return {"record_url": record_url}
    else:
        return {"error": "User not found or wrong token"}


@app.get("/record/")
async def get_record(record_id: str, user_id: str):
    if user_id in users_db and f"{record_id}.mp3" in os.listdir():
        return FileResponse(f"{record_id}.mp3")
    else:
        return {"error": "Запись не найдена или доступ запрещен"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
