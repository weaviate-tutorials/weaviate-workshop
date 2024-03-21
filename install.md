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

### How to use after

**Activate**
If in the future, you need to switch to the venv setup, just call:
```
source .venv/bin/activate
```

**Deactivate**
To disconnect from the venv environment, call:
```
source deactivate
```