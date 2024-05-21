# weaviate-aws-fargate

## NOTE: Running the setup.sh script more than once will break python module dependencies at this time.
## Creating a new notebook instance and re-running the full script is the recommended troubleshooting.

1. Start your SageMaker Studio Jupyterlab instance.
2. Start a terminal session within your running instance.
3. Retrieve your AWS CLI Credentials from the event dashboard.
4. Paste and set your AWS CLI Credentials into your terminal session.
5. Clone this repository.
6. Use chmod to make the setup.sh script executable.
```
chmod 755 setup.sh
```
7. Run setup.sh.
```
./setup.sh
```
8. Record your weaviate IP address from the script's output to use in your python code.
9. A sample python script is included in this repo, weaviate-example.py.