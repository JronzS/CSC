from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import Response
from image_ops import process_image
import uvicorn


app = FastAPI()


@app.post('/process')
async def process(
file: UploadFile = File(...),
filter: str | None = Form(None),
blur_ksize: int | None = Form(None),
flip: int | None = Form(None),
crop: str | None = Form(None) # crop as 'x,y,w,h'
):
data = await file.read()
ops = {}
if filter:
ops['filter'] = filter
if blur_ksize:
ops['blur_ksize'] = blur_ksize
if flip is not None:
ops['flip'] = flip
if crop:
try:
parts = [int(p) for p in crop.split(',')]
if len(parts) == 4:
ops['crop'] = parts
except Exception:
pass


out_bytes, mime = process_image(data, ops)
return Response(content=out_bytes, media_type=mime)


if __name__ == '__main__':
uvicorn.run(app, host='0.0.0.0', port=8000)