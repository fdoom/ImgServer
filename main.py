from fastapi import FastAPI, File, UploadFile, HTTPException, Header, Depends
from fastapi.responses import JSONResponse, FileResponse
import shutil
import os

app = FastAPI()

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def is_valid_image_filename(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def save_uploaded_file(path: str, file: UploadFile):
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, file.filename), "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

api_keys = os.getenv("IMG_SERVER_API_KEY")
# API 키를 확인하는 의존성 함수
async def get_api_key(api_key: str):
    if api_key != api_keys:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

@app.post("/images/")
async def upload_file(path: str , file: UploadFile = File(...), api_key: str = Depends(get_api_key)):
    try:
        if not is_valid_image_filename(file.filename):
            raise HTTPException(status_code=400, detail="Only images with extensions {} are allowed.".format(ALLOWED_IMAGE_EXTENSIONS))
        
        save_uploaded_file(path, file)
        return JSONResponse(content={"message": "File uploaded successfully"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"An error occurred: {str(e)}"})

@app.get("/images/")
async def get_image(image_name: str, path: str):
    if not is_valid_image_filename(image_name):
        raise HTTPException(status_code=400, detail="Only images with extensions {} are allowed.".format(ALLOWED_IMAGE_EXTENSIONS))
    image_path = os.path.join(path, image_name)
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")
    
@app.delete("/images/")
async def delete_image(image_name: str, path: str, api_key: str = Depends(get_api_key)):
    if not is_valid_image_filename(image_name):
        raise HTTPException(status_code=400, detail="Only images with extensions {} are allowed.".format(ALLOWED_IMAGE_EXTENSIONS))
    image_path = os.path.join(path, image_name)
    if os.path.exists(image_path):
        os.remove(image_path)
        return {"message": "Image deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Image not found")
    
@app.get("/")
async def get_image_paths():
    image_paths = [
        os.path.join(root, file)
        for root, _, files in os.walk(".")
        for file in files
        if os.path.splitext(file)[1].lower()[1:] in ALLOWED_IMAGE_EXTENSIONS
    ]

    return {"paths": image_paths}