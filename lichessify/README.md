## LiChessify Add-on

This is the Firefox add-on for the LiChessify program. It takes an image (of a chessboard) from the system clipboard, POSTs it to the LiChessify backend, then sends a notification when the link to the game is received. Clicking the notification opens the game in a new tab. If something goes wrong a long the way, it will send a notification that an error has occurred.

### Installation

If you want to try this out, you can can temporarily install the add-on using the instructions given [here](https://extensionworkshop.com/documentation/develop/temporary-installation-in-firefox/#Reloading_a_temporary_extension). However, using this add on requires enabling the `dom.events.asyncClipboard.dataTransfer` preference; you can do this by navigating to about:config in Firefox, searching for the preference, and switching its value to `true`.

### Icon Attribution

Credit for the icon displayed in the toolbar belongs to font-awesome.
https://fontawesome.com/license