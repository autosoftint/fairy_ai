function updateSpriteSize() {
    if (avatarModel === null || background === null) {
        return;
    }
    // Calculate the window width and height.
    const appRect = appDiv.getBoundingClientRect();
    // Resize the background, scale to fit the content.
    const rawBackgroundWidth = backgroundTexture.baseTexture.width;
    const rawBackgroundHeight = backgroundTexture.baseTexture.height;
    // Calculate the image and background ratio.
    const imageRatio = rawBackgroundWidth / rawBackgroundHeight;
    const appRatio = appRect.width / appRect.height;
    const imageScale = (imageRatio > appRatio) ? (appRect.height / rawBackgroundHeight) : (appRect.width / rawBackgroundWidth);
    background.width = rawBackgroundWidth * imageScale;
    background.height = rawBackgroundHeight * imageScale;
    background.x = (appRect.width - background.width) / 2;
    background.y = (appRect.height - background.height) / 2;

    // Calculate the raw model size.
    const avatarRawHeight = avatarModel.height / avatarModel.scale.y;
    // Update the model scale size, make sure the model use the entire height of the window.
    const scaleFactor = appRect.height / avatarRawHeight;
    avatarModel.scale.set(scaleFactor);
    // Move the model to the central of the window.
    avatarModel.x = (appRect.width - avatarModel.width) / 2;

    // Stare at the front.
    // avatarModel.focus(avatarModel.width / 2, 0)
}

let avatarModel = null;
let backgroundTexture = null;
let background = null;

async function loadLive2D(background_url, model_url) {
    // Construct the PixiJS application.
    const app = new PIXI.Application({
        view: document.getElementById("live2d"),
        autoStart: true,
        antialias: true,
        resizeTo: window
    });

    // Add the background sprite.
    backgroundTexture = PIXI.Texture.from("/static/assert/" + background_url);
    background = new PIXI.Sprite(backgroundTexture);
    app.stage.addChild(background);

    // Add the Live2D model to stage.
    const modelUrl = "/static/model/" + model_url;
    avatarModel = await PIXI.live2d.Live2DModel.from(modelUrl, {
        autoInteract: false,
        motionPreload: PIXI.live2d.MotionPreloadStrategy.ALL,
    });
    app.stage.addChild(avatarModel);

    // Resize the background and Live2D model.
    updateSpriteSize();

    // Add the resize event handler.
    window.addEventListener('resize', (event) => {
        // Update the PIXI.JS Scale.
        updateSpriteSize();
    }, true);

    // const hitAreaFrames = new PIXI.live2d.HitAreaFrames();
    // hitAreaFrames.visible = true;
    // avatarModel.addChild(hitAreaFrames);

    // // Add hit handler.
    // avatarModel.on("hit", (hitAreas) => {
    //
    // })
}