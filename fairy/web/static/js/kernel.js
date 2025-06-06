async function loadScript(src) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        script.onload = () => resolve(script);
        script.onerror = () => reject(new Error(`Failed to load ${src}`));
        document.head.appendChild(script);
    });
}

async function loadUiModule(ui_settings) {
    const details = ui_settings['result'];
    const ui_type = details['type'];
    if (ui_type === 'live2d') {
        // Load the target UI module.
        await loadScript("/static/js/ui_live2d.js");
        // Load Live2D avatar model.
        (loadLive2D)(details["background"], details["model_url"]);
    }
}

function bootstrap() {
    // Fetch the UI settings.
    fetch(get_url("ui_settings"), {
        method: 'GET',
    }).then(res => res.json())
        .then(response => {
            // Connect to server command queue.
            connect_message_socket();
            // Based on the response, load the Live2D.
            (loadUiModule)(response);
        })
}