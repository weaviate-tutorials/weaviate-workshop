# Weaviate Workshop


## What you need for the workshop

* API Keys for embedding models, from Bedrock:
  * amazon.titan-embed-text-v1
  * cohere.embed-english-v3
  * etc,

* Python 3.9 or newer

* Docker Compose

## How to setup the python environment with venv
To run the project locally, it is best to setup python environment with venv.

### Setup – do this only once
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


## Running the project in GitHub Codespaces

1. Go to the project [https://github.com/weaviate-tutorials/weaviate-workshop](https://github.com/weaviate-tutorials/weaviate-workshop).

2. Create a Codespace project
  * Press the green `Code` button, then switch to `Codespaces` tab.
  * Press `...` (next to the `+` button) and select `New with options...`
  * Select the `aws-immersion` branch, change the `Machine type` to `4-core` and press the green `Create codespace` button

3. After the codespace is ready – set up the evironment and install the required libraries. Run:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. For "lesson 5", start the `docker-compose-clip.yml` image (and give it a couple of minutes):
```
docker compose -f "5-multivec-named-vectors/docker-compose-clip.yml" up -d
```

5. Install Jupyter notebook extension. You will be asked for it when you open any notebook. Then switch to the .venv image.