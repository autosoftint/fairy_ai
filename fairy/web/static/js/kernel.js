function static_url(suffix) {
    return "/static" + suffix
}

function js_url(js_name) {
    return static_url("/js/" + js_name + ".js")
}

function model_url(module_suffix) {
    return static_url("/model/" + module_suffix)
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

async function loadHtml(src) {
    fetch(src)
        .then(response => response.text())
        .then(html_source => {
            appDiv.insertAdjacentHTML('afterbegin', html_source);
        })
}

async function loadUiModule(ui_settings) {
    const details = ui_settings['result'];
    const ui_type = details['type'];

    if ("placeholder" in details) {
        elementUserTextArea.placeholder = details['placeholder'];
    }

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
        // Create the Live2D canvas.
        const canvas = document.createElement("canvas");
        canvas.id = "live2d";
        appDiv.insertBefore(canvas, appDiv.firstChild);
        // Load Live2D avatar model.
        (loadLive2D)(details["background"], details["model_url"]);
    } else if (ui_type === 'html') {
        // Load HTML source code.
        await loadHtml(model_url(details["url"]))
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
            // Based on the response, load the UI module.
            (loadUiModule)(response);
            // Based on the response, load the dialogue.
        })
}