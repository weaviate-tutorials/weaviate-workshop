# Weaviate Workshop

## What you need for the workshop

* API Keys for embedding models, like:
  * OpenAI - [API keys](https://platform.openai.com/settings/profile?tab=api-keys)
  * etc,

## GitHub CodeSpaces instructions

1. Go to the project [https://github.com/weaviate-tutorials/weaviate-workshop](https://github.com/weaviate-tutorials/weaviate-workshop)

Make sure you are logged in with GitHub.

2. Create a Codespace project
  * Press the green `<> Code` button, then switch to `Codespaces` tab.
  * Press the `Create codespace on main` button.
  * Your codespace project will install all the necessary components, it will take a few minutes.

## Create a Weaviate Cloud instance

  * Head to [Weaviate Cloud console](https://console.weaviate.cloud/) and log in, or create a new account.
  * Create a free `Sandbox` cluster. Give it a name, select the cloud region and press "Create".

![wcd create cluster - step 1](img/wcd-create-cluster-1.jpg)
![wcd create cluster - step 2](img/wcd-create-cluster-2.jpg)

<!-- 4. Start docker container
  * In the VS Code, open `_docker` folder
  * Right click on `docker-compose.yml` and select `Compose Up` -->


<!--
## What you need for the workshop

* API Keys for embedding models, like:
  * OpenAI Key
  * Cohere Key
  * etc,

 * Python 3.9 or newer

* Docker Compose (Todo: update this in case we can do it all with WCS)

# Local Setup
> (if not using GitHub Codespaces)

> Ideally, run this workshop in GitHub Codespaces, see [instructions](#github-codespaces-instructions).

## How to setup the python environment with venv
To run the project locally, it is best to setup python environment with venv.

### Setup - running locally – do this only once
First create a new venv configuration.
```
python3 -m venv .venv
```

Then switch to the new configuration:
```
source .venv/bin/activate
```

And install the required packages.
```
pip install -r requirements.txt
```

**All together**
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Activate
If in the future, you need to switch to the venv setup, just call:
```
source .venv/bin/activate
```

### Deactivate
To disconnect from the venv environment, call:
```
source deactivate
```
-->