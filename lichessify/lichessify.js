function getGameUrl() {

    window.navigator.clipboard.read().then(data => {

        let image = null;
        try {
            // find the first image in the clipboard
            for (let key in data.items) {
                if (data.items[key].type.startsWith("image")) {
                    image = data.items[key].getAsFile();
                    break;
                }
            }
            if (image === null) {
                throw Error("No image found in clipboard.");
            }
        } 
        catch {
            sendErrorNotification("No image found in clipboard.");
            return;
        }

        fetch(serverUrl, {
            method: 'POST',
            body: image
        }).then(
            response => response.json().then( json => sendSuccessNotification(json) )
        ).catch(
            () => sendErrorNotification("Couldn't generate a game from this image.")
        );

    });
}

function sendSuccessNotification(response) {
    browser.notifications.create({
        type: "basic",
        iconUrl: browser.extension.getURL("icons/page-32.png"),
        title: "LiChessified!",
        message: `LiChess game created with ${response.certainty}% certainty. Click here to open game.`
    }).then(() => {
        browser.notifications.onClicked.addListener(() => {
            browser.tabs.create({ url: response.link })
        });
    });
}

function sendErrorNotification(message) {
    browser.notifications.create({
        type: "basic",
        iconUrl: browser.extension.getURL("icons/page-32.png"),
        title: "Failed to Create Game...",
        message: message
    });
}

var serverUrl = "https://lichessify.azurewebsites.net/api/lichessify-func";
browser.browserAction.onClicked.addListener(getGameUrl);