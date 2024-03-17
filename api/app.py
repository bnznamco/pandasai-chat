from uuid import uuid4
from fastapi import FastAPI, UploadFile, Depends, HTTPException, Response
import csv, base64, codecs, json, os
from pathlib import Path
from datetime import datetime
from .sessions import SessionData, cookie, backend
from pandas.core.frame import DataFrame
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from .models import ChatMessage, OpenaiToken
from openai import APIStatusError
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_PATH = BASE_DIR / "uploads"

CHARTS_PATH = BASE_DIR / "charts"

os.makedirs(UPLOAD_PATH, exist_ok=True)
os.makedirs(CHARTS_PATH, exist_ok=True)

app = FastAPI()

origins = [
    "http://localhost:4321",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/set-openai-token")
async def set_openai_token(data: OpenaiToken, response: Response):
    try:
        OpenAI(api_token=data.token).chat_completion("!", memory=None)
    except APIStatusError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.response.json().get("error", {}).get("message", ""),
        )
    session = uuid4()
    json.dump(
        {"token": data.token, "created": datetime.now().isoformat()},
        open(UPLOAD_PATH / f"{session}.openai.json", "w"),
    )
    data = SessionData(username=str(session))
    await backend.create(session, data)
    cookie.attach_to_response(response, session)
    return {"status": "ok"}


@app.post("/api/clear-session")
async def del_session(response: Response, session_id: uuid4 = Depends(cookie)):
    for file in UPLOAD_PATH.glob(f"{session_id}.*"):
        file.unlink()
    cookie.delete_from_response(response)
    return {"status": "ok"}


@app.post("/api/upload-file")
async def upload(file: UploadFile, session: SessionData = Depends(cookie)):
    try:
        csv.DictReader(codecs.iterdecode(file.file, "utf-8"))
    except csv.Error:
        raise HTTPException(status_code=400, detail="Invalid CSV file")
    content = file.file.read()
    file_path = UPLOAD_PATH / f"{session}.csv"
    with open(file_path, "wb") as f:
        f.write(content)
    file_info = {"file_name": file.filename, "file_path": str(file_path)}
    json.dump(file_info, open(UPLOAD_PATH / f"{session}.json", "w"))
    file.file.close()
    return file_info


@app.post("/api/chat")
async def chat(body: ChatMessage, session: SessionData = Depends(cookie)):
    file_info = json.load(open(UPLOAD_PATH / f"{session}.json"))
    openai_info = json.load(open(UPLOAD_PATH / f"{session}.openai.json"))
    df = SmartDataframe(
        file_info["file_path"],
        config={
            "llm": OpenAI(api_token=openai_info["token"]),
            "save_charts": True,
            "save_charts_path": str(CHARTS_PATH),
        },
    )
    response = df.chat(body.message)
    if isinstance(response, str):
        if "/charts" in response:
            resp_parts = response.split(" ")
            path_part = next((part for part in resp_parts if "/charts" in part), None)
            if path_part:
                with open(path_part, "rb") as f:
                    return {
                        "content": base64.b64encode(f.read()).decode("utf-8"),
                        "type": "image",
                    }
        return {"content": response, "type": "text"}
    elif isinstance(response, (SmartDataframe, DataFrame)):
        return {"content": response.to_markdown(), "type": "markdown"}
    else:
        return {"content": str(response), "type": "text"}
