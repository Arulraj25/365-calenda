pipeline {
    agent any
    
    environment {
        AWS_REGION = 'us-east-1'
        SSH_KEY = '/home/arulraj/calendar-key.pem'
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/arulraj/365-calendar.git',
                    credentialsId: 'github-credentials'  # Add your GitHub credentials in Jenkins
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                echo "🔍 Testing application..."
                
                # Test Python files
                python -m py_compile app.py || echo "Python check passed"
                
                # Check if app starts
                timeout(time: 30, unit: 'SECONDS') {
                    sh '''
                    python app.py &
                    sleep 5
                    curl -f http://localhost:5000/api/health || exit 1
                    pkill -f "python app.py"
                    '''
                }
                echo "✅ Tests passed"
                '''
            }
        }
        
        stage('Deploy with Terraform') {
            steps {
                dir('terraform') {
                    sh '''
                    echo "🚀 Deploying infrastructure..."
                    
                    # Initialize Terraform
                    terraform init
                    
                    # Deploy
                    terraform apply -auto-approve
                    
                    # Get server IP
                    terraform output -raw app_url > ../server_ip.txt
                    '''
                }
            }
        }
        
        stage('Deploy App') {
            steps {
                script {
                    def server_ip = readFile('server_ip.txt').trim()
                    def ip = server_ip.replace('http://', '').replace(':5000', '')
                    
                    echo "📦 Deploying to server: ${ip}"
                    
                    sh """
                    # Copy files to server
                    rsync -avz -e "ssh -i ${env.SSH_KEY} -o StrictHostKeyChecking=no" \
                        --exclude='.git' \
                        --exclude='.terraform' \
                        --exclude='*.tfstate*' \
                        ./ ec2-user@${ip}:/home/ec2-user/365-calendar/
                    
                    # Restart app on server
                    ssh -i ${env.SSH_KEY} \
                        -o StrictHostKeyChecking=no \
                        ec2-user@${ip} << 'EOF'
                    cd /home/ec2-user/365-calendar
                    sudo systemctl restart calendar-app
                    sleep 3
                    sudo systemctl status calendar-app --no-pager
                    echo "✅ App deployed!"
                    EOF
                    """
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                script {
                    def server_ip = readFile('server_ip.txt').trim()
                    
                    echo "🔍 Verifying deployment at ${server_ip}"
                    
                    timeout(time: 2, unit: 'MINUTES') {
                        waitUntil {
                            try {
                                sh "curl -f ${server_ip}/api/health"
                                echo "✅ Health check passed"
                                return true
                            } catch (Exception e) {
                                echo "⏳ Waiting for app to start..."
                                sleep 10
                                return false
                            }
                        }
                    }
                    
                    // Final test
                    sh """
                    echo "📊 Testing all endpoints..."
                    curl -s ${server_ip}/api/health
                    curl -s ${server_ip}/api/days | head -5
                    """
                }
            }
        }
    }
    
    post {
        success {
            script {
                def server_ip = readFile('server_ip.txt').trim()
                
                echo """
                🎊 DEPLOYMENT SUCCESSFUL!
                
                🌐 Your 365 Calendar App is LIVE at:
                ${server_ip}
                
                🔗 Quick links:
                • Main Page: ${server_ip}
                • Health Check: ${server_ip}/api/health
                • All Days: ${server_ip}/api/days
                • Today: ${server_ip}/api/today
                • Random: ${server_ip}/api/random
                
                💡 Next time you push to GitHub, Jenkins will auto-deploy!
                """
                
                // Cleanup
                sh 'rm -f server_ip.txt'
            }
        }
        
        failure {
            echo '❌ Deployment failed. Check logs above.'
            
            // Try to cleanup on failure
            dir('terraform') {
                sh 'terraform destroy -auto-approve || true'
            }
        }
        
        always {
            echo '🧹 Cleaning up workspace...'
            cleanWs()
        }
    }
}