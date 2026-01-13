pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Pulling code from GitHub...'
                checkout scm
                sh 'ls -la'
            }
        }
        
        stage('Setup') {
            steps {
                sh '''
                    echo "🐍 Setting up environment..."
                    
                    # Create virtual environment
                    python3 -m venv venv
                    
                    # Use venv's pip directly
                    venv/bin/pip install --upgrade pip
                    echo "✅ Virtual environment created"
                '''
            }
        }
        
        stage('Install') {
            steps {
                sh '''
                    echo "📦 Installing dependencies..."
                    
                    # Install using venv pip
                    venv/bin/pip install -r requirements.txt
                    echo "✅ Dependencies installed"
                '''
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    echo "🧪 Testing application..."
                    
                    # Start app using venv python
                    venv/bin/python app.py &
                    APP_PID=$!
                    sleep 5
                    
                    # Test endpoints
                    echo "Testing API..."
                    curl -f http://localhost:5000/api/health && echo "✅ Health check passed"
                    
                    DAYS_COUNT=$(curl -s http://localhost:5000/api/days | jq '.days | length')
                    echo "📅 Found $DAYS_COUNT special days"
                    
                    # Kill app
                    kill $APP_PID
                    echo "✅ All tests passed"
                '''
            }
        }
        
        stage('Build') {
            steps {
                sh '''
                    echo "🔨 Creating package..."
                    
                    # Create build info
                    cat > build-info.txt << EOF
Build: ${BUILD_NUMBER}
Date: $(date)
Commit: $(git log --oneline -1)
Status: SUCCESS
EOF
                    
                    # Create archive
                    tar -czf calendar-build-${BUILD_NUMBER}.tar.gz --exclude=venv --exclude=.git *
                    echo "📦 Package: calendar-build-${BUILD_NUMBER}.tar.gz"
                '''
            }
        }
    }
    
    post {
        success {
            echo "🎉 Pipeline SUCCESS!"
            archiveArtifacts artifacts: 'calendar-build-*.tar.gz, build-info.txt', allowEmptyArchive: true
        }
        failure {
            echo "❌ Pipeline FAILED!"
        }
        always {
            sh 'rm -f calendar-build-*.tar.gz build-info.txt'
        }
    }
}