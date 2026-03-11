from fastapi import FastAPI, UploadFile
import shutil
import uuid
from .extractor import Extractor

app = FastAPI()

extractor = Extractor()


@app.post("/extract")
async def extract(file: UploadFile):

    temp = f"/tmp/{uuid.uuid4()}_{file.filename}"

    with open(temp, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extractor.extract(temp)

    return {
        "filename": file.filename,
        "text": text
    }