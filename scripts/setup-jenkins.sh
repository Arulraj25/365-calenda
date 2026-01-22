#!/bin/bash
# Setup Jenkins with Terraform and AWS

echo "Setting up Jenkins for 365 Calendar deployment..."

# Install required plugins
JENKINS_PLUGINS="pipeline-aws terraform git docker-workflow"

for plugin in $JENKINS_PLUGINS; do
    echo "Installing plugin: $plugin"
    java -jar /usr/lib/jenkins-plugin-manager.jar --plugins $plugin
done

# Configure AWS credentials in Jenkins
cat > /tmp/aws-credentials.xml <<EOF
<com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl>
  <scope>GLOBAL</scope>
  <id>aws-credentials</id>
  <description>AWS Access Key</description>
  <username>\${AWS_ACCESS_KEY_ID}</username>
  <password>\${AWS_SECRET_ACCESS_KEY}</password>
</com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl>
EOF

echo "Setup complete!"
echo "Next steps:"
echo "1. Add AWS credentials to Jenkins"
echo "2. Create SSH key for EC2: ssh-keygen -f calendar-key"
echo "3. Upload calendar-key.pem to Jenkins credentials"
echo "4. Update terraform/variables.tf with your VPC/Subnet IDs"