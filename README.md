# Weaviate Workshop


## What you need for the workshop

* API Keys for embedding models, like:
  * Google AI Studio – [get the key here](https://aistudio.google.com/app/u/0/apikey)
  * (optional) Google Vertex AI

* Python 3.9 or newer

## Local Setup

> For Windows, it is recommended to use the workshop with [GitHub workspaces](#run-the-project-in-github-codespaces).

### Setup the python environment with venv
To run the project locally, it is best to setup python environment with venv.

### Steps (do this only once)
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

### Activate/Deactivate
If in the future, you may need to switch to the venv setup again.

* To connect to `.venv`, call:
```
source .venv/bin/activate
```

* To deactivate `.venv`, call:

```
source deactivate
```

## Run the project in GitHub Codespaces

1. Go to the project [https://github.com/weaviate-tutorials/weaviate-workshop](https://github.com/weaviate-tutorials/weaviate-workshop).

2. Switch to the [nyc-roadshow](https://github.com/weaviate-tutorials/weaviate-workshop/tree/nyc-roadshow) branch.

3. Create a Codespace project
  * Press the green `Code` button, then switch to `Codespaces` tab.
  * Press `...` (next to the `+` button) and select `New with options...`
  * Select `nyc-roadshow` branch,
  * Change the `Machine type` to `4-core` and press the green `Create codespace` button

4. After the codespace is ready – set up the evironment and install the required libraries. Run:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

5. Install Jupyter notebook extension. You will be asked for it when you run the first notebook cell. Then switch to the `.venv` image.

6. Start the `docker-compose-clip.yml` image (and give it a couple of minutes), you will need it for Lesson 5:
```
docker compose -f "_docker/docker-compose-clip.yml" up -d
```