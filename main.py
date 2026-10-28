import io
import requests
import replicate
from typing import List
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

# Change these 3 lines if your model's API tab shows different names
MODEL = "lucataco/faceswap"
FRAME_FIELD = "target_image"   # the picture that gets the new face
FACE_FIELD = "swap_image"      # the photo of your model

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/api/swap")
def swap(
    frame: UploadFile = File(...),
    models: List[UploadFile] = File(...),
    outfit: str = Form(""),
    body: str = Form(""),
    expression: str = Form(""),
):
    frame_file = io.BytesIO(frame.file.read())
    face_file = io.BytesIO(models[0].file.read())

    output = replicate.run(
        MODEL,
        input={FRAME_FIELD: frame_file, FACE_FIELD: face_file},
    )

    if isinstance(output, list):
        output = output[0]
    if hasattr(output, "read"):
        image_bytes = output.read()
    else:
        image_bytes = requests.get(str(output)).content

    return Response(content=image_bytes, media_type="image/png")
