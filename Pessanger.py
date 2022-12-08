from tkinter import *
from firebase import firebase
from simplecrypt import encrypt, decrypt

firebase = firebase.FirebaseApplication("https://login-encryption-2-default-rtdb.firebaseio.com/", None)


loginWindow = Tk()
loginWindow.geometry("400x400")
loginWindow.config(bg="grey")
loginWindow.title("Login")

username = ""
yourCode = ""
yourFriendsCode = ""
messageTextVal = ""
messageEntryVal = ""
lastValue = ""

def getData(): 
    global messageTextVal
    global lastValue
    global yourCode
    global yourFriendsCode
    
    getYourData = firebase.get('/', yourCode)
    print(getYourData)
    
    byteStr = bytes.fromhex(getYourData)
    original = decrypt("AIM", byteStr)
    print("Original Data", original)
    
    finalMessage = original.decode("utf-8")
    print(finalMessage)
    
    messageTextVal.insert(END, finalMessage + "\n")
    
    getFriendsData = firebase.get('/', yourFriendsCode)
    if(getFriendsData != None):
        print("Data: ", getFriendsData)
        byteStr = bytes.fromhex(getFriendsData)
        original = decrypt("AIM", byteStr)
        
        finalMessage = original.decode("utf-8")
        if(finalMessage not in lastValue):
            print(finalMessage)
            messageTextVal.insert(END, finalMessage + "\n")
            lastValue = finalMessage
            
          
    


def sendData():
    global username
    global messageEntryVal
    global yourCode
    message = username + ": " + messageEntryVal.get()
    cipherCode = encrypt("AIM", message)
    hexString = cipherCode.hex()
    putData = firebase.put("/", yourCode, hexString)
    print(putData)
    getData()
    
def enterRoom():
    global username
    global yourCode
    global yourFriendsCode
    global messageEntryVal
    global messageTextVal
    
    yourCode = yourCodeEntry.get()
    yourFriendsCode = FriendsCodeEntry.get()
    username = usernameEntry.get()
    
    messageWindow = Tk()
    messageWindow.geometry("600x500")
    messageWindow.config(bg="#AFC1D6")
    messageWindow.title("Messages")
    
    messageTextVal = Text(messageWindow, height = 20, width = 72)
    messageTextVal.place(relx=0.5, rely=0.35, anchor=CENTER)
    
    messageLabel = Label(messageWindow, font="arial 13", text="Message", bg="#AFC1D6", fg="white")
    messageLabel.place(relx=0.3, rely=0.8, anchor=CENTER)
    
    messageEntryVal = Entry(messageWindow, font="arial 13")
    messageEntryVal.place(relx=0.6, rely=0.8, anchor=CENTER)
    
    btnSend = Button(messageWindow, text="Send", relief=FLAT, command=sendData)
    btnSend.place(relx= 0.5, rely=0.9, anchor=CENTER)
    
    loginWindow.destroy()
    
    messageWindow.mainloop()
    
usernameLabel = Label(loginWindow, text="User: ", font="arial 13", bg="#AB92BF", fg="white")
usernameLabel.place(relx=0.3, rely=0.3, anchor=CENTER)

usernameEntry = Entry(loginWindow)
usernameEntry.place(relx=0.6, rely=0.3, anchor=CENTER)

yourCodeLabel = Label(loginWindow, text="Your Code: ", font="arial 13", bg="#AB92BF", fg="white")
yourCodeLabel.place(relx=0.3, rely=0.4, anchor=CENTER)

yourCodeEntry = Entry(loginWindow)
yourCodeEntry.place(relx=0.6, rely=0.4, anchor=CENTER)

FriendsCodeLabel = Label(loginWindow, text="Friends Code: ", font="arial 13", bg="#AB92BF", fg="white")
FriendsCodeLabel.place(relx=0.22, rely=0.5, anchor=CENTER)

FriendsCodeEntry = Entry(loginWindow)
FriendsCodeEntry.place(relx=0.6, rely=0.5, anchor=CENTER)

btnStart = Button(loginWindow, text="Start", font="arial 13", command=enterRoom, relief=FLAT, padx=10)
btnStart.place(relx=0.5, rely=0.65, anchor=CENTER)


loginWindow.mainloop()