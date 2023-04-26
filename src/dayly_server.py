import asyncio
import websockets
import json
import yaml
import packages.logger as logger
import packages.passwordHasher as passwordHasher
import packages.lifAuthenticator as authenticator
 
#Loads config
with open("config.yml", 'r') as file:
    configFile = yaml.safe_load(file)

# create handler for each connection
async def handle(websocket, path):
    async for message in websocket:

        if message == "DAYLY_LOGIN":
            #requests user credentials 
            await websocket.send("CREDENTIALS?")
            rawCredentials = await websocket.recv()
            
            # Loading the credentials
            loadCredentials = json.loads(rawCredentials)

            # Defines the username and password for verifying credentials
            username = loadCredentials['Username']
            password = passwordHasher.get_initial_hash(loadCredentials['Password'])

            # Verifies credentials with Lif authenticator server
            status = await authenticator.verifyCredentials(username, password)

            print(status)

            # Checks the status and reply's to the client
            if status == "Good_Login": 
                print("Login Confirmed")
                await websocket.send("LOGIN_GOOD")

            if status == "Bad_Login":
                await websocket.send("LOGIN_BAD")

        if message == "TOKEN_LOGIN":
            print("token login")
            #asks client for token
            await websocket.send("TOKEN?")

            #retrieves token from client
            token = await websocket.recv()
            print(token)

            #opens token json file to check token provided by client
            with open("tokens.json", "r") as file:
                #reads content of file
                content = file.read() 
                #converts data into json
                loadData = json.loads(content)


                #checks if token exists 
                if token in loadData:
                    await websocket.send("TOKEN_ACCEPTED")
                    print("token accepted")
                else:
                    await websocket.send("INVALID_TOKEN")
                    print("invalid token")

                #receives request for username associated with the token 
                requestUsername = await websocket.recv() 

                #checks if client requested username
                if requestUsername == "USERNAME?":
                    #username is paired with the toke with the token being the key. to access the username you access the token key
                    await websocket.send(loadData[token])
                    print('sent username')
                    print(loadData[token])


    #reply = f"Data recieved as:  {data}!"
 
    #await websocket.send(reply)
 
async def start_server():
    async with websockets.serve(handle, "localhost", 8001):
        logger.showInfo("Server Running!")
        await asyncio.Future()  # Keep the server running indefinitely

asyncio.run(start_server())