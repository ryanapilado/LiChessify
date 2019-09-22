## LiChessify

This is a small Firefox add-on which makes it easy to convert images of chessboards to playable, interactive games on Lichess. The code for the add-on is in `lichessify/`, and the Azure Function is in `function/`.

This is especially useful when watching chess videos or reading articles, or even watching other people play. Often, I'll see a position that I want to interact with - but if it's a still image or a video that's not possible, unless I want to manually arrange all 32 chess pieces myself. LiChessify uses an [open-sourced chessbot](https://github.com/Elucidation/tensorflow_chessbot) to generate the FEN of the position, and then to generate a link to a playable game.

So if you've installed the add-on and you see a position you want to inspect further, simply grab a screenshot (`Win + Shift + S`, `Cmd + Shift + 4`) or copy the image to your clipboard directly. Once the image is in your clipboard, click the add-on icon in the toolbar. Wait a few seconds for the notification that the game is ready to arrive ... then click the notification to open the game in a new tab.

I played no part in building the image classifier! This project just simplifies the process of using the chessbot. All credit for the excellent tensorflow_chessbot goes to [@Elucidation](https://github.com/Elucidation/tensorflow_chessbot).