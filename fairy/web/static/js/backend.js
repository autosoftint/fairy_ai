const HEARTBEAT_INTERVAL = 30000 // 30 second a heartbeat
let message_socket = null
let message_heartbeat = null


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
                elementResult.innerText = "（爱莉希雅正在思考……）"
            } else {
                elementResult.innerText = ""
            }
        } else if (op === "say") {
            if (request.hasOwnProperty("text")) {
                let text_delta = request["text"];
                if (elementResult.innerText.length === 0) {
                    text_delta = text_delta.trimStart()
                }
                elementResult.innerText += text_delta
            }
        } else if (op === "done") {
            // Show the restart button.
            elementFairyButtonStop.hidden = true
            elementFairyButtonContinue.hidden = false
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