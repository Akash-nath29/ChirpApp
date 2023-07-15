"""
ChirpApp 2.0

An online real-time chatting application for everyone

In this version a few changes have been added. Like the UI update, and other stuffs. The previous version is available in https://github.com/Akash-nath29/ChirpApp

Author: Akash Nath

"""
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO, emit
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "Krw90{veookke]mn!34m" #Use Storng Secret Key for Production
socketio = SocketIO(app)

"""
The function below crates 6 character room code, and adds to room object. Further this function has been used and was checked if the generated room code does exist, i.e is in the room object, then it is programmed to rejet the code and make a new one.
"""

rooms = {}
def generate_unic_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
            
        if code not in rooms:
            break
    return code

@app.route("/", methods=["GET", "POST"])
def index():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)
        
        #Different Error situation and error handeling ↓
        if not name:
            return render_template("index.html", error = "Please enter a valid name.", code=code, name=name)
        if join != False and not code:
            return render_template("index.html", error="Please enter a valid room code.", code=code, name=name)
        room = code
        if create != False:
            room = generate_unic_code(6)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("index.html", error = "Room doesn't exist.", code=code, name=name)
        
        session["room"] = room
        session["name"] = name
        
        return redirect(url_for("room"))
        
        
    return render_template("index.html")

@app.route("/room")
def room():
    room = session.get("room")

    if room is None or session.get("room") is None or room not in rooms: 
        #Checks if the room code exists or not, as mentioned earlier ↑
        return redirect(url_for("index"))
    
    return render_template("room.html", code=room, messages=rooms[room]["messages"])

"""
This following code represents the main functonality of the code. The following gets activated when client sends a message, and then the server uses the following code to emit the message and to send it to all the userr present in that room ↓↓ 
"""
@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']} ")

"""
When a client joins a room (Actually joins or creates a room and then joins it), the following code activates and sends a message to everyone that a client has joined the room. It uses the name provided by the user and sends a message to everyone like this "<Name>: has entered the room" ↓↓
"""

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name":name, "message":"has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined the room {room}")
    
"""
When a client disconnects from the server (Closes the App or refreshes the page), the follwing code activates and sends a message to every person present in the room that the person has left the room
"<Name>: has left the room" ↓↓
"""
@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)
    
    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0 :
            del rooms[room]
    send({"name":name, "message":"has left the room"}, to=room)
    print(f"{name} left the room {room}")
    
"""
When someone refreshes the page, he/she actually disconnects from the server or the room and rejoins it. So when someone refreshes the page, the server will send a message to everyone like this
"<Name>: has left the room"
"<Name>: has joined the room"
"""
    
    
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=80)