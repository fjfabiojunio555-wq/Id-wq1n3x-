from fastapi import FastAPI, UploadFile, File
import shutil
import subprocess

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/processar/")
async def processar(file: UploadFile = File(...)):
    input_file = "input.mp4"
    
    with open(input_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output = "final.mp4"

    comando = [
        "ffmpeg",
        "-i", input_file,
        "-vf", "scale=1080:1920",
        "-c:a", "aac",
        output
    ]

    subprocess.run(comando)

    return {"video": output}
