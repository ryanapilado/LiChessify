## INTRO

This is the back-end of the LiChessify add-on, implemented as an Azure Function.
It takes an image of a chess position and gets the FEN of that position using
an [open-sourced pre-trained TensorFlow model](https://github.com/Elucidation/tensorflow_chessbot),
then returns a link to a playable lichess game from that position.

A POST request with a photo of a chess position in the body will return a JSON
containing the link as well as the certainty of the analysis. For example:

```json
{
    "link":"https://lichess.org/analysis/r2qk2r/1pp1bppp/p2p1n2/6B1/3QP3/2N5/PPP2PPP/R3K2R",
    "certainty":100.0
}
```

All credit for the actual hard work of building the classifier goes to its [creator](https://github.com/Elucidation). 
The intention of this code (together with the browser add-on) is simply to 
provide a convenient web interface through which to use it.

## SETUP

The code requires that tensorflow_chessbot be built and ready to run in the
`~/tensorflow_chessbot` directory of some VM or container. This can be anywhere,
so long as the function can SSH to it.

The function also needs a storage account, and a container within that storage
account to which to write the images. This is usually created automatically
during function deployment.

The code is intended to be deployed to an Azure Functions app running on Linux and using a Python runtime stack. Instructions to create a function app can be found [here](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python#create-a-function-app-in-azure). Deploying requires the installation of the Azure CLI tool. Instructions for the installation can be found [here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest). Once installed, navigate to the root directory and run the command `func azure functionapp publish <app-name> --build remote`, where `<app-name>` is the name of the functionapp that was created previously.

Once deployed, following environment variables ('Application Settings' in Azure)
need to be set:

1. CHESSBOT_IP: The IP of the VM/container where `tensorflow_chessbot` is located.
2. CHESSBOT_PORT: The port through which to SSH to the VM/container, usually 22.
3. CHESSBOT_USERNAME: The username to use when seting up the SSH.
4. CHESSBOT_PASSWORD: The password to use when setting up the SSH.
5. STORAGE_ACCOUNT_NAME: The name of the storage account to which to write the images.
6. STORAGE_ACCOUNT_KEY: The key used for writing to the storage account.
7. STORAGE_CONTAINER_NAME: The container within the storage account to which to write to.