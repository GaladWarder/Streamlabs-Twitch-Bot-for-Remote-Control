import socket
import pyautogui
import requests
import webbrowser
import time
import string
from threading import Thread

x, y = pyautogui.size()

#pyautogui failsafes
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

# Set all the variables necessary to connect to Twitch IRC and joining
HOST = "irc.twitch.tv"
NICK = "F*ckWithGaladBot"
PORT = 6667
#TODO: Enter yout Twitch oauth Code
PASS = "oauth:ENTER_TWITCH_OAUTH_HERE"
readbuffer = ""
MODT = False
s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS " + PASS + "\r\n")
s.send("NICK " + NICK + "\r\n")
#TODO: Enter Channel Name after the '#'
s.send("JOIN #CHANNEL_NAME \r\n")


#authorizing app to use account
url = "https://streamlabs.com/api/v1.0/authorize"
#TODO: Enter Streamlabs Client ID, Redirect URI here.
querystring = {"response_type":"code","client_id":"ENTER STREAMLABS CLIENT ID","redirect_uri":"REDIRECT_URI","scope":"points.write"}
response = requests.request("GET", url, params=querystring)
webbrowser.open(response.url)

accessTokenCode = raw_input('Enter the code here: ')

#retrieving the access token from Streamlabs
tokenUrl = "https://streamlabs.com/api/v1.0/token"
#TODO: Enter Streamlabs Client ID, Client Secret, and Redirect URI here
querystringtwo = {"grant_type": "authorization_code",
                  "client_id": "CLIENT_ID_HERE",
                  "client_secret": "CLIENT_SECRET_HERE",
                  "redirect_uri": "REDIRECT_URI_HERE",
                  "code": accessTokenCode}
response = requests.request("POST", tokenUrl, data=querystringtwo)
dataFromServer = response.json()
print(dataFromServer)

accessToken = dataFromServer['access_token']
refreshToken = dataFromServer['refresh_token']

def refreshthetoken():
    global refreshToken
    global accessToken
    #timing the refresh to happen every hour
    oldtime = time.time()
    # check
    while oldtime + 3590 != time.time():

        if oldtime + 3589 == time.time():
            #refreshing the token before it expires
            #TODO: Enter Streamlabs CLIENT ID, CLIENT SECRET, and REDIRECT URI here
            tokenurl = "https://streamlabs.com/api/v1.0/token"
            querystringthree = {"grant_type": "refresh_token",
                                  "client_id": "CLIENT_ID_HERE",
                                  "client_secret": "CLIENT_SECRET_HERE",
                                  "redirect_uri": "REDIRECT_URI_HERE",
                                  "refresh_token": refreshToken}
            response = requests.request("POST", tokenurl, data=querystringthree)
            dataFromServer = response.json()
            refreshToken = dataFromServer['refresh_token']
            accessToken = dataFromServer['access_token']
            print(dataFromServer)
            break

# Method for sending a message
def Send_message(message):
    #TODO: ENTER CHANNEL NAME HERE, lowercase
    s.send("PRIVMSG #CHANNEL_NAME :" + message + "\r\n")

#TODO: You can replace 'Dongers' with your channel currency name in these methods
# Method to charge 20 dongers to user executing the command
def charge_20_Dongers():
    url = "https://streamlabs.com/api/v1.0/points/subtract"
    #TODO: Enter Twitch Channel Name, lowercase
    kwargs = {"access_token": accessToken, "username": username, "channel": "#CHANNEL NAME HERE", "points": 20}
    response = requests.request("POST", url, data=kwargs)

    if response == {"message": "User does not have enough points"}:
        Send_message("You don't have enough dongers to do that, " + username)

# method to charge 10 dongers to command-executing user
def charge_10_Dongers():
    url = "https://streamlabs.com/api/v1.0/points/subtract"
    # TODO: Enter Twitch Channel Name, lowercase
    kwargs = {"access_token": accessToken, "username": username, "channel": "#CHANNEL NAME HERE", "points": 10}
    response = requests.request("POST", url, data=kwargs)
    print(response.text)

# method to charge 10 dongers to command-executing user
def charge_5_Dongers():
    url = "https://streamlabs.com/api/v1.0/points/subtract"
    # TODO: Enter Twitch Channel Name, lowercase
    kwargs = {"access_token": accessToken, "username": username, "channel": "#CHANNEL NAME HERE", "points": 5}
    response = requests.request("POST", url, data=kwargs)
    print(response.text)

def chatmonitoring():
    global readbuffer
    readbuffer = readbuffer + s.recv(1024)
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()
    global username
    for line in temp:
        # Passing Twitch afk checks
        if (line[0] == "PING"):
            s.send("PONG %s\r\n" % line[1])
        else:
            # Splits the given string to work with it more easily
            parts = string.split(line, ":")

            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                try:
                    # Sets the message variable to the actual message sent
                    message = parts[2][:len(parts[2]) - 1]
                except:
                    message = ""
                # Sets the username variable to the actual username
                usernamesplit = string.split(parts[1], "!")
                username = usernamesplit[0]

                # Only works after twitch is done announcing stuff (MODT = Message of the day)
                global MODT
                if MODT:
                    print username + ": " + message

                    #allows a check to see if the bot is in the channel
                    if message == "!testing":
                        Send_message("I am here, " + username)

                    # button commands go here
                    if message == "!press-shift":
                        #charges Streamlabs currency
                        charge_10_Dongers()
                        #checking that the user can afford the command
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.typewrite(['shift'])

                    if message == "!press-q":
                        charge_20_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.typewrite(['q'])

                    if message == "!press-b":
                        charge_10_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.typewrite(['b'])

                    if message == "!press-e":
                        charge_10_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.typewrite(['e'])

                        # mouse clicks go here
                    if message == "!click":
                        charge_5_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.click()

                    if message == "!right-click":
                        charge_5_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.click(button='right')

                    if message == "!longclick":
                        charge_10_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            #clicks the mouse for one second
                            pyautogui.mouseDown()
                            time.sleep(1)
                            pyautogui.mouseUp()

                        # movement controls here
                    if message == "!reload":
                        charge_10_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.typewrite(['r'])

                    if message == "!jump":
                        charge_5_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.typewrite(['space'])

                    if message == "!crouch":
                        charge_5_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.typewrite(['c'])

                    if message == "!move-forward":
                        charge_10_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            #moves for 1.5 seconds
                            pyautogui.keyDown('w')
                            time.sleep(1.5)
                            pyautogui.keyUp('w')

                    if message == "!move-left":
                        charge_10_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.keyDown('a')
                            time.sleep(1.5)
                            pyautogui.keyUp('a')

                    if message == "!move-right":
                        charge_10_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.keyDown('d')
                            time.sleep(1.5)
                            pyautogui.keyUp('d')

                    if message == "!move-back":
                        charge_10_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.keyDown('s')
                            time.sleep(1.5)
                            pyautogui.keyUp('s')

                        # Mouse inputs go here
                    if message == "!mouse-right":
                        charge_20_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.moveTo(800, 0, 0.5)

                    if message == "!mouse-left":
                        charge_20_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.moveTo(-800, 0, 0.5)

                    if message == "!mouse-up":
                        charge_20_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.moveTo(0, -800, 0.5)

                    if message == "!mouse-down":
                        charge_20_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.moveTo(0, 800, 0.5)

                    if message == "!scroll-up":
                        charge_10_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.scroll(1)

                    if message == "!scroll-down":
                        charge_10_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.scroll(-1)

                        # Macros go here
                    if message == "!undo":
                        charge_20_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            #macros an undo in Photoshop
                            pyautogui.keyDown('ctrl')
                            pyautogui.keyDown('alt')
                            pyautogui.typewrite(['z'])
                            pyautogui.keyUp('alt')
                            pyautogui.keyUp('ctrl')

                    if message == "!brushbigger":
                        charge_5_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.keyDown(']')
                            time.sleep(0.25)
                            pyautogui.keyUp(']')

                    if message == "!brushsmaller":
                        charge_5_Dongers()
                        if response == {"message": "User does not have enough points"}:
                            break
                        else:
                            pyautogui.keyDown('[')
                            time.sleep(0.25)
                            pyautogui.keyUp('[')

                for l in parts:
                    if "End of /NAMES list" in l:
                        MODT = True
#starts them both
while True:
    Thread(target = refreshthetoken()).start()
    Thread(target = chatmonitoring()).start()