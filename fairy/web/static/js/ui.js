const appDiv = document.getElementById('app');

const elementPanelUserText = document.getElementById("ui_user_textbox")
const elementPanelFairyText = document.getElementById("ui_fairy_textbox")
const elementUserText = document.getElementById("ui_user_message")
const elementResult = document.getElementById("ui_fairy_text_result")
const elementUserTextArea = document.getElementById("ui_user_text_input")
const elementUserSayText = document.getElementById("ui_user_say_text")

const elementFairyButtonStop = document.getElementById("ui_user_stop")
const elementFairyButtonContinue = document.getElementById("ui_user_restart")

function hideUserTextPanel() {
    // Disable the user text input.
    elementUserTextArea.disabled = true
    elementUserSayText.disabled = true
    // Hide the user input panel.
    elementPanelUserText.hidden = true
}

function hideFairyPanel() {
    // Show Fairy result panel.
    elementPanelFairyText.hidden = false
}

function showFairyPanel() {
    // Hide the all user panels.
    hideUserTextPanel()
    // Reset panel button hidden states.
    elementFairyButtonStop.hidden = false
    elementFairyButtonContinue.hidden = true
    // Show Fairy result panel.
    elementPanelFairyText.hidden = false
}

function showUserTextPanel() {
    hideFairyPanel()
    // Release the text input panel.
    elementUserTextArea.disabled = false
    elementUserSayText.disabled = false
    // Show the panel.
    elementPanelUserText.hidden = false
}

elementFairyButtonStop.onclick = function () {
}

elementFairyButtonContinue.onclick = function () {
    showUserTextPanel()
}

elementUserSayText.onclick = function () {
    const userInput = elementUserTextArea.value.trim()
    if(userInput.length === 0) {
        return
    }
    // Clear the user input.
    showFairyPanel()
    elementUserTextArea.value = ""
    elementUserText.innerText = userInput
    elementResult.innerText = ""
    // Construct the text payload.
    fetch(get_url("chat"), {
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
            showUserTextPanel()
        })

}