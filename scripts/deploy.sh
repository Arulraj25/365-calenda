#!/bin/bash
# Manual deployment script

set -e

ENVIRONMENT=${1:-dev}
BUILD_ID=${2:-manual-$(date +%Y%m%d%H%M%S)}

echo "Deploying 365 Calendar to $ENVIRONMENT..."

# Check AWS CLI
aws --version || { echo "AWS CLI not installed"; exit 1; }

# Check Terraform
terraform --version || { echo "Terraform not installed"; exit 1; }

# Build Docker image
echo "Building Docker image..."
docker build -t 365-calendar:$BUILD_ID .

# Push to registry (optional)
# docker tag 365-calendar:$BUILD_ID your-registry/365-calendar:$BUILD_ID
# docker push your-registry/365-calendar:$BUILD_ID

# Terraform deploy
cd terraform
terraform init
terraform apply -auto-approve \
  -var="environment=$ENVIRONMENT" \
  -var="build_id=$BUILD_ID"

# Get endpoint
ENDPOINT=$(terraform output -raw app_endpoint)
echo "✅ Deployment complete!"
echo "🌐 Application URL: $ENDPOINT"
echo "🔗 API Health: $ENDPOINT/api/health"