#!/bin/sh
echo "Installing Weaviate Python Client..."
pip install -q weaviate-client
echo "Creating ECS Cluster: weaviate-cluster..."
aws ecs create-cluster --cluster-name weaviate-cluster > /dev/null
echo "Creating ECS Task Definition: weaviate-task..."
aws ecs register-task-definition --cli-input-json file://weaviate-task.json  > /dev/null
AWS_SUBNETS=$(aws ec2 describe-subnets --query "Subnets[*].SubnetId" --output text | tr '\t' ',')
AWS_SG=$(aws ec2 describe-security-groups --filters Name=group-name,Values=default --query 'SecurityGroups[0].GroupId' --output text)
echo "Creating ECS Service: weaviate-service..."
aws ecs create-service --cluster weaviate-cluster --service-name weaviate-service --task-definition weaviate-task --desired-count 1 --launch-type "FARGATE" --network-configuration "awsvpcConfiguration={securityGroups=[${AWS_SG}],subnets=[${AWS_SUBNETS}],assignPublicIp=ENABLED}"  > /dev/null
SM_IP=$(host myip.opendns.com resolver1.opendns.com | awk '/has address/ { print $4 }')
echo "Configuring Default Security Group..."
aws ec2 authorize-security-group-ingress --group-id ${AWS_SG} --protocol tcp --port 8080-50051 --cidr ${SM_IP}/32
attempt=0
while [ -z "${ENI_ID}" ]; do
        echo "Waiting for Weaviate to become ready..."
        export TASK_ARN=$(aws ecs list-tasks --cluster weaviate-cluster --service weaviate-service --query 'taskArns[0]' --output text)
        export ENI_ID=$(aws ecs describe-tasks --cluster weaviate-cluster --tasks ${TASK_ARN} --query "tasks[*].attachments[*].details[?name=='networkInterfaceId'].value" --output text)
        sleep 2
done
WEAVIATE_IP=$(aws ec2 describe-network-interfaces --network-interface-id ${ENI_ID} --query "NetworkInterfaces[0].Association.PublicIp" --output text)
echo ""
echo ""
echo "Please use the following IP address to access your weaviate instance."
echo "Weaviate Endpoint Reachable at: ${WEAVIATE_IP}"
echo "Example usage: curl ${WEAVIATE_IP}:8080/v1/nodes"