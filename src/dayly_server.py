import asyncio
import sqlite3
import websockets
import hashlib
import secrets
import json
import os
import yaml
 
#Loads config
with open("config.yml", 'r') as file:
    configFile = yaml.safe_load(file)

# create handler for each connection
 
async def handler(websocket, path):
    data = await websocket.recv()
    #client_ip = websocket.getpeername()[0]
    #print(client_ip)

    if data == "DAYLY_LOGIN":
        #requests user credentials 
        await websocket.send("USERNAME")
        username = await websocket.recv()
        await websocket.send("PASSWORD")
        password1 = await websocket.recv()

        salt = "5gz"
                        
        # Adding salt at the last of the password
        dataBase_password = password1+salt
        # Encoding the password
        hashed = hashlib.md5(dataBase_password.encode())
        print('hashed password')
        
        # Sending the Hash
        password = hashed.hexdigest()

        #connecting to lif database
        conn = sqlite3.connect(configFile['path-to-database'])
        c = conn.cursor()

        #getting all accounts from database
        c.execute("SELECT * FROM accounts")
        items = c.fetchall()

        #tells the server if the account givin was found
        foundAccount = False 

        for item in items:
            print('seraching...')
            user = item[0]
            print(user)
            password2 = item[1]
            print(password2)

            if username == user and password == password2:
                print("found account")
                foundAccount = True
                break

        if foundAccount == True:
            await websocket.send("SUCCESS")
            requestToken = await websocket.recv()
            if requestToken == "TOKEN?":
                #Generates and sends login to9ken to client
                token = secrets.token_urlsafe(16) 
                await websocket.send(token) 

                #checks if "tokens.json" exists and if not, creates the file
                if not os.path.isfile("tokens.json"):
                    with open("tokens.json", "a") as file:
                        file.write("{}")
                        file.close()

                #opens json file for reading so it can be appended to later 
                with open("tokens.json", "r") as file:
                    #gets the content of the file
                    content = file.read()
                    #loads json data from file 
                    tokens = json.loads(content)
                    file.close() 

                #appends new token to dict 
                tokens.update({token:username})

                #writes appended data to json file 
                with open("tokens.json", "w") as file:
                    #dumps the new dict into json
                    dumpContent = json.dumps(tokens)
                    #writes data to file
                    file.write(dumpContent)
                    file.close() 
        else:
            await websocket.send("INVALID_CREDENTIALS")

    if data == "TOKEN_LOGIN":
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
            else:
                await websocket.send("INVALID_TOKEN")

            #receives request for username associated with the token 
            requestUsername = await websocket.recv() 

            #checks if client requested username
            if requestUsername == "USERNAME?":
                #username is paired with the toke with the token being the key. to access the username you access the token key
                await websocket.send(loadData[token])


    #reply = f"Data recieved as:  {data}!"
 
    #await websocket.send(reply)
 
start_server = websockets.serve(handler, "localhost", 8000)
 
 
 
asyncio.get_event_loop().run_until_complete(start_server)
 
asyncio.get_event_loop().run_forever()