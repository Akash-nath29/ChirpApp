var socketio = io();

const messages = document.getElementById("messages");
const createMessage = (name, msg) => {
    const content = `
    <div class="text">
        <span>
            <strong  id="userName">${name}</strong>: ${msg}    
        </span>
        <span class="muted" style="font-size: 10px;">
            <i>${new Date().toLocaleString()}</i>              
        </span>
    </div>
    `
    messages.innerHTML += content;
};

socketio.on("message", (data) => {
    createMessage(data.name, data.message)
})

const sendMesage = () => {
    const message = document.getElementById("message");
    if (message.value == "") {
        return
    };
    socketio.emit("message", { data: message.value });
    message.value = "";

};

var helpBtn = document.getElementById("help");
var helpDetails = document.getElementById("helpDetails");
helpDetails.style.maxHeight = "0px";

helpBtn.addEventListener('click', () => {
    if (helpDetails.style.maxHeight == "0px") {
        helpDetails.style.maxHeight = "130px";
    }
    else {
        helpDetails.style.maxHeight = "0px";
    }
})