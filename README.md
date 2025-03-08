# Weaviate Workshop

## What you need for the workshop

* API Keys for embedding models, like:
  * OpenAI - [API keys](https://platform.openai.com/settings/profile?tab=api-keys)
  * etc,

## Create a Weaviate Cloud instance

  * Head to [Weaviate Cloud console](https://console.weaviate.cloud/) and log in, or create a new account.
  * Create a free `Sandbox` cluster. Give it a name, select the cloud region and press "Create".

![wcd create cluster - step 1](img/wcd-create-cluster-1.jpg)
![wcd create cluster - step 2](img/wcd-create-cluster-2.jpg)

## Running the workshop

You can follow this workshop using:
- a [local Devcontainer](#local-devcontainer-setup)
- [GitHub Codespaces](#github-codespaces-setup)

You can also run the code on your local machine, using your preferred environment manager and package manager. This is not covered in this README.

### Local Devcontainer setup

#### Prerequisites

- Install VSCode (https://code.visualstudio.com/download)
- Install Docker (https://www.docker.com/products/docker-desktop/)

#### Installation

First, copy this repository to your local machine:

```shell
git clone https://github.com/weaviate-tutorials/weaviate-workshop
```

Move into the directory:

```shell
cd weaviate-tutorials
```

Then, open the project in VSCode:

```shell
code .
```

This will open VSCode.

You may be prompted "Folder contains a Dev Container configuration file. Reopen folder to develop in a container". Click "Reopen in Container".

If not:
- Install the "Dev Containers" extension in VSCode (by Microsoft), if you don't have it already.
- Open the command palette (Ctrl+Shift+P / Cmd+Shift+P) and type "Rebuild and Reopen in Container".

You should see a popup at the bottom right corner, indicating that the project is being reopened in a container.

When the container is ready, you should see a terminal in VSCode.
- It should include messages from a `pip install ...` command, indicating packages being installed.
- It should finish with a message like: `Done. Press any key to close the terminal.`
- Press enter, and you should be in a terminal window, with a prompt such as `/workspaces/weaviate-workshop#`

Run the following command to check that everything is running:

```shell
python check-env.py
```

You should see an output, similar to:

```shell
Python version: 3.11.11 (main, Feb 25 2025, 09:36:46) [GCC 10.2.1 20210110]
Weaviate Python Client package version: 4.11.0
```

Then, you are good to go.

If you are prompted to identify which Python interpreter to use, select the one that is in the `/usr/local/bin/python` directory. This is the Python interpreter in the container.

It will include the required packages, such as the Weaviate Python client.

### Option 2 - GitHub CodeSpaces instructions

1. Go to the project [https://github.com/weaviate-tutorials/weaviate-workshop](https://github.com/weaviate-tutorials/weaviate-workshop)

Make sure you are logged in with GitHub.

2. Create a Codespace project
  * Press the green `<> Code` button, then switch to `Codespaces` tab.
  * Press the `Create codespace on main` button.
  * Your codespace project will install all the necessary components, it will take a few minutes.

## Environment variables

Update env vars in .env.

Hint. you can find your Weaviate Cluster URL and API keys in the [WCD console](https://console.weaviate.cloud/).

* WEAVIATE_URL - is the `REST Endpoint`
* WEAVIATE_KEY - is the `Admin` key in `API Keys`

## Test your setup

Head to [1-intro/0-prep-run.ipynb](./1-intro/0-prep-run.ipynb), and run through all steps.

## Download the pre-vectorized data

Head to [prep-data.ipynb](./prep-data.ipynb) and run all the cells. This should download the data we will use in the second lesson.
