const elementResult = document.getElementById("result_message")
const elementThinking = document.getElementById("thinking_state")
const elementUserText = document.getElementById("user_message")
const elementUserInput = document.getElementById("user_input")
const elementUserSayText = document.getElementById("user_say_text")

const HEARTBEAT_INTERVAL = 30000 // 30 second a heartbeat
let message_socket = null
let message_heartbeat = null

function lockUserInput() {
    elementUserInput.disabled = true
    elementUserSayText.disabled = true
}

function unlockUserInput() {
    elementUserInput.disabled = false
    elementUserSayText.disabled = false
}

elementUserSayText.onclick = function () {
    const userInput = elementUserInput.value.trim();
    if(userInput.length === 0) {
        return
    }
    // Clear the user input.
    lockUserInput()
    elementUserInput.value = ""
    elementUserText.innerText = userInput
    // Construct the text payload.
    fetch(window.location.protocol + "//" + window.location.host + "/chat", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // Specify JSON data
        },
        body: JSON.stringify({"mode": "text", "text": userInput})
    }).then(response => response.json())
        .then(function (response) {
            console.log(response)
        })
        .catch(function (error) {
            console.log(error)
            unlockUserInput()
        })

}

function connect_message_socket() {
    message_socket = new WebSocket("ws://" + window.location.host + "/")
    message_socket.onopen = function (e) {
        // Reset the previous heartbeat function.
        if (message_heartbeat !== null) {
            clearInterval(message_heartbeat)
        }
        message_heartbeat = setInterval(function () {
            if (message_socket) {
                message_socket.send('')
            }
        }, HEARTBEAT_INTERVAL)
    }

    message_socket.onmessage = function (e) {
        const request = JSON.parse(e.data)
        if (!request.hasOwnProperty("op")) {
            return
        }
        // Extract the op.
        const op = request.op;
        if (op === "think") {
            if (!request.hasOwnProperty("state")) {
                return
            }
            const think_state = request["state"]
            if (think_state) {
                // Reset the result content.
                elementResult.innerText = ""
                elementThinking.innerText = "thinking..."
            } else {
                elementThinking.innerText = ""
            }
        } else if (op === "say") {
            if (request.hasOwnProperty("text")) {
                elementResult.innerText += request["text"]
            }
        } else if (op === "done") {
            // Unlock the textarea and submit button.
            unlockUserInput()
        }

    }

    message_socket.onclose = function (e) {
        // Reset the heartbeat function.
        if (message_heartbeat !== null) {
            clearInterval(message_heartbeat)
            message_heartbeat = null
        }
        // Retry connection.
        console.log('Connection closed, retry after 0.5 seconds...');
        setTimeout(connect_message_socket, 500);    //Retry after 0.5 seconds.
    }
}

function entry () {
    // Connect to server command queue.
    connect_message_socket()
}