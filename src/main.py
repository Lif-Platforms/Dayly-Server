from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form
import yaml
import utils.passwordHasher as passwordHasher
import utils.lifAuthenticator as authenticator
import utils.db_interface as database
import uvicorn
import os
import uuid
 
app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/new_post/{username}/{token}")
async def upload_image(username: str, token: str, file: UploadFile = File(), title: str = Form(), description: str = Form()):
    # Verifies token with Lif Auth server
    authentication = authenticator.verify_token(username=username, token=token)

    if authentication:
        # Extract the original filename with extension
        original_filename = file.filename

        # Grabs the file extension from the filename 
        file_extension = os.path.splitext(original_filename)[1]

        # Generates a unique id for the file
        file_id = str(uuid.uuid4())

        filename = file_id + file_extension

        save_path = os.path.join("images/", filename)  # Specify the desired save path

        # Save the uploaded file to disk
        with open(save_path, "wb") as f:
            contents = await file.read()
            f.write(contents)

        # Creates new post in database
        database.new_post(author=username, title=title, description=description, content=filename)

        # Return a response if needed
        return {"status": "Ok"}
    
    else:
        return {"status": "Unsuccessful", "reason": "invalid token"}

if __name__ == '__main__':
    uvicorn.run(app="main:app", port=8004)