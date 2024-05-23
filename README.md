# Weaviate Workshop


## Accessing the workshop environment:

- Go to: https://catalog.us-east-1.prod.workshops.aws/join
- Enter the code shown on screen
- Open the AWS console on the bottom left corner

## Setting up Amazon Bedrock

### Open Amazon Bedrock by searching for it in the search bar
![image](./static/1.0.png)

### Select the hamburger menu on the left side to open the side bar
![image](./static/1.1.png)

### in the side bar select "model access"
![image](./static/1.2.png)

### Select Enable specific model
![image](./static/1.4.png)

### Select all models provided by Amazon 
![image](./static/1.5.png)

### Scroll down till you see the next button, and select this button
![image](./static/1.6.png)

### Submit the model request
![image](./static/1.7.png)

## Setting up the Identity and Access Management (IAM) roles

### Search for IAM in the search bar
![image](./static/2.0.png)

### Select "Roles"
![image](./static/2.1.png)

### Search for the role starting with "sagemaker-immersion-day" and click on the role name, with trusted entities note "AWS Service: sagemaker"
![image](./static/2.2.png)

### Select "Add permissions" and "Attach policies"
![image](./static/2.3.png)

### Add the policy "AmazonBedrockFullAccess"
![image](./static/2.4.png)

### Add the policy "AmazonECS_FullAccess" and select "Add permissions"
![image](./static/2.5.png)

### Check that both policies are added
![image](./static/2.6.png)

## Setting up Amazon SageMaker

### Search for Amazon SageMaker
![image](./static/3.0.png)

### When seeing the SageMaker landing page, select Domains (under Admin configurations)
![image](./static/3.1.png)

### Select the domain called "SageMakerImmersionDayDomain" by clicking on the name
![image](./static/3.2.png)

### Open "Studio" under "Launch"
![image](./static/3.3.png)

### Skip the tour for now
![image](./static/3.4.png)

### Select JupyterLab (top left) and select "Create JupyterLab space" (top right)
![image](./static/3.5.png)

### Create a new space
![image](./static/3.6.png)

### Select "Run space"
![image](./static/3.7.png)

### Select "Open JupyterLab" once it's ready
![image](./static/3.8.png)

### Open a Terminal (under other)
![image](./static/3.9.png)

Type the following:

### Clone the workshop repository
```bash
git clone -b aws-immersion https://github.com/weaviate-tutorials/weaviate-workshop
```

### Move to the setup folder
```bash
cd weaviate-workshop/0-setup/
```

### Ensure that the setup script is executable
```bash
chmod +x setup.sh
```

### Run the setup.sh script
```bash
./setup.sh
```

### Once you see the `Weaviate Endpoint Reachable at: [IP]`, copy the `[IP]` 

### Open the `1-intro` folder and paste the `[IP]` in `WEAVIATE_IP`