import os
import subprocess
import uuid
from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()
TEMP_DIR = Path("/tmp/conv")
TEMP_DIR.mkdir(exist_ok=True)

def cleanup(paths: list):
    for path in paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass

@app.post("/convert")
async def convert_to_pdf(file: UploadFile, background_tasks: BackgroundTasks):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".doc", ".docx"]:
        raise HTTPException(status_code=400, detail="Invalid format")

    job_id = str(uuid.uuid4())
    input_path = TEMP_DIR / f"{job_id}{ext}"
    output_pdf = TEMP_DIR / f"{job_id}.pdf"

    # Save binary
    with input_path.open("wb") as buffer:
        buffer.write(await file.read())

    try:
        # Standard system call to the 'libreoffice' we installed via apt
        command = [
            "libreoffice",
            "--headless",
            "--invisible",
            "--nodefault",
            "--nofirststartwizard",
            "--nologo",
            f"-env:UserInstallation=file:///tmp/{job_id}_prof",
            "--convert-to", "pdf:writer_pdf_Export",
            "--outdir", str(TEMP_DIR),
            str(input_path)
        ]

        subprocess.run(command, check=True, capture_output=True)

        # Schedule cleanup of both files after the response is sent
        background_tasks.add_task(cleanup, [str(input_path), str(output_pdf)])

        return FileResponse(
            path=output_pdf,
            media_type="application/pdf",
            filename=f"{os.path.splitext(file.filename)[0]}.pdf"
        )

    except Exception as e:
        cleanup([str(input_path)])
        raise HTTPException(status_code=500, detail=str(e))