function js_url(js_name) {
    return "/static/js/" + js_name + ".js"
}

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
        const module_names = [
            // Live2D Cubism SDK v2 and v4
            "live2d.min", "live2dcubismcore.min",
            // Pixi.JS v6
            "pixi.min",
            // Pixi.JS Live2D Display Plugin
            "pixi-live2d-display.min",
            // Fairy Live2d module.
            "ui_live2d",
        ]
        // Load the target UI module.
        for (const js_name of module_names) {
            await loadScript(js_url(js_name));
        }
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