from fastapi import FastAPI, UploadFile, File
import shutil
import whisper
import subprocess

app = FastAPI()
model = whisper.load_model("base")

@app.post("/processar/")
async def processar(file: UploadFile = File(...)):
    input_file = file.filename
    
    with open(input_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = model.transcribe(input_file)

    outputs = []

    for i, seg in enumerate(result["segments"][:3]):
        inicio = seg['start']
        fim = seg['end']
        texto = seg['text'].replace("'", "")

        output = f"final_{i}.mp4"

        comando = [
            "ffmpeg",
            "-i", input_file,
            "-ss", str(inicio),
            "-to", str(fim),
            "-vf", f"crop=in_h*9/16:in_h,scale=1080:1920,drawtext=text='{texto}':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=h-120",
            "-c:a", "aac",
            output
        ]

        subprocess.run(comando)
        outputs.append(output)

    return {"videos": outputs}
