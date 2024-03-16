from fastapi import FastAPI, File, UploadFile, HTTPException
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

@app.post("/images/")
async def upload_file(path: str , file: UploadFile = File(...)):
    try:
        if not is_valid_image_filename(file.filename):
            raise HTTPException(status_code=400, detail="Only images with extensions {} are allowed.".format(ALLOWED_IMAGE_EXTENSIONS))
        
        save_uploaded_file(path, file)
        return JSONResponse(content={"message": "File uploaded successfully"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"An error occurred: {str(e)}"})

@app.get("/images/")
def get_image(image_name: str, path: str):
    if not is_valid_image_filename(image_name):
        raise HTTPException(status_code=400, detail="Only images with extensions {} are allowed.".format(ALLOWED_IMAGE_EXTENSIONS))
    image_path = os.path.join(path, image_name)
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")
    
@app.delete("/images/")
def delete_image(image_name: str, path: str):
    if not is_valid_image_filename(image_name):
        raise HTTPException(status_code=400, detail="Only images with extensions {} are allowed.".format(ALLOWED_IMAGE_EXTENSIONS))
    image_path = os.path.join(path, image_name)
    if os.path.exists(image_path):
        os.remove(image_path)
        return {"message": "Image deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Image not found")
    
@app.get("/")
def read_root():
    return {"Hello" : "World!"}