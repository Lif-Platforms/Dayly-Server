import websocket
import yaml 
import json
import asyncio

#Loads config
with open("config.yml", 'r') as file:
    configFile = yaml.safe_load(file)

# Function for verifying user credentials 
async def verifyCredentials(username, password):
    # Create a future object to capture the return value
    result = asyncio.Future()

    # Function for when the connection opens
    def on_open(ws):
        print("Connection opened")
        ws.send("VERIFY_CREDENTIALS")

    # Function for handling messages received from the server
    def on_message(ws, message):
        print(message)
        
        # Checks if the server has requested the user credentials
        if message == "CREDENTIALS?":
            # prepares credentials for sending
            rawCredentials = {"Username": username, "Password": password}
            credentials = json.dumps(rawCredentials)

            # Sends credentials to server
            ws.send(credentials)

        # Checks if the server has approved the login credentials
        if message == "LOGIN_GOOD": 
            print("login was good")
            # Sets the future result with "Good_Login"
            result.set_result("Good_Login")
            ws.close()
        
        # Checks if the server has denied the credentials
        if message == "LOGIN_BAD": 
            # Sets the future result with "Bad_Login"
            result.set_result("Bad_Login")
            ws.close()

    # Url for connecting to the server
    url = f"ws://{configFile['host']}:{configFile['port']}/websocket"

    # Opens the connection 
    ws = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message)
    ws.run_forever()

    # Wait for the result to be set and return it
    return await result