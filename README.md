# Weaviate Workshop

## What you need for the workshop

* API Keys for embedding models, like:
  * OpenAI Key
  * etc,
* Python 3.9 or newer

## Local Setup

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
