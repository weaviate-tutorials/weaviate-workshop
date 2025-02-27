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

### Option 1 - Run locally

#### Virtual environment – do this only once
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

### Option 2 - GitHub CodeSpaces instructions

1. Go to the project [https://github.com/weaviate-tutorials/weaviate-workshop](https://github.com/weaviate-tutorials/weaviate-workshop)

Make sure you are logged in with GitHub.

2. Create a Codespace project
  * Press the green `<> Code` button, then switch to `Codespaces` tab.
  * Press the `Create codespace on main` button.
  * Your codespace project will install all the necessary components, it will take a few minutes.


## Env vars

Update env vars in .env.

Hint. you can find your Weaviate Cluster URL and API keys in the [WCD console](https://console.weaviate.cloud/).

* WEAVIATE_URL - is the `REST Endpoint`
* WEAVIATE_KEY - is the `Admin` key in `API Keys`

## Test your setup

Head to [1-intro/0-prep-run.ipynb](./1-intro/0-prep-run.ipynb), and run through all steps.

## Download the prevectorized data

Head to [prep-data.ipynb](./prep-data.ipynb) and run all the cells. This should download the data we will use in the second lesson.