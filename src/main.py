from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form
import yaml
import json
import utils.passwordHasher as passwordHasher
import utils.lifAuthenticator as authenticator
import utils.db_interface as database
import uvicorn
import os
import uuid

resources_folder = os.path.join(os.path.dirname(__file__), "resources")

# Check config
if not os.path.isfile("../config.yml"):
    with open("config.yml", 'x') as config:
        config.close()

with open("../config.yml", "r") as config:
    contents = config.read()
    configurations = yaml.safe_load(contents)
    config.close()

# Ensure the configurations are not None
if configurations == None:
    configurations = {}

# Open reference json file for config
with open(f"{resources_folder}/config-template.json", "r") as json_file:
    json_data = json_file.read()
    default_config = json.loads(json_data)

# Compare config with json data
for option in default_config:
    if not option in configurations:
        configurations[option] = default_config[option]
        print(f"Added '{option}' to config!")

# Open config in write mode to write the updated config
with open("../config.yml", "w") as config:
    new_config = yaml.safe_dump(configurations)
    config.write(new_config)
    config.close()

if not os.path.isdir("../user_content"):
    os.mkdir("../user_content")

# Set database path
database.set_db_path(configurations['path-to-database'])

# Set auth url
authenticator.set_auth_url(configurations['auth-server-url'])
 
app = FastAPI()

# Configure CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=configurations['allow-origins'],
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