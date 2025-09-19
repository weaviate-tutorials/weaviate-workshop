# Weaviate Workshop

## What you need for the workshop

* Docker installed and running on your computer
* An running Docker service

Download [Docker](https://docs.docker.com/get-started/get-docker/)

Open terminal and enter the _docker folder and start the service
cd _docker
docker-compose up 

## Running the workshop

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


## Install ollama

Open terminal and paste the follwoing commands:
 

* brew install ollama - Installs Ollama

 
* ollama serve - Runs Ollama service
### Pull an embedding model

Open a new terminal and run:

ollama pull nomic-embed-text

### Pull a generative model

ollama pull llama3.2:1b
- Memory: ~2-3GB RAM when running
- Parameters: 1 billion
- Better quality responses

**OR**

ollama pull qwen2.5:0.5b
- Memory: ~1GB RAM when running
- Parameters: 0.5 billion
- Faster but lower quality responses


## Env vars

Update env vars in .env.


* WEAVIATE_URL=http://localhost:8080
* WEAVIATE_KEY=root-user-key
* OPENAI_URL=http://localhost:11434/v1
* OPENAI_API_KEY=ollama


## Test your setup

Head to [1-intro/0-prep-run.ipynb](./1-intro/0-prep-run.ipynb), and run through all steps.

## Download the prevectorized data

Head to [prep-data.ipynb](./prep-data.ipynb) and run all the cells. This should download the data we will use in the second lesson.




