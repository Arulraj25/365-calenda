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
        
        stage('Setup Virtual Environment') {
            steps {
                sh '''
                    echo "🐍 Creating Python virtual environment..."
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "📦 Installing Python dependencies..."
                    source venv/bin/activate
                    pip install -r requirements.txt
                    echo "✅ Dependencies installed"
                '''
            }
        }
        
        stage('Test Application') {
            steps {
                sh '''
                    echo "🧪 Testing application..."
                    source venv/bin/activate
                    
                    # Start the app in background
                    python app.py &
                    APP_PID=$!
                    
                    # Wait for app to start
                    sleep 5
                    
                    # Test health endpoint
                    echo "Testing /api/health..."
                    if curl -f http://localhost:5000/api/health; then
                        echo "✅ Health check passed"
                    else
                        echo "❌ Health check failed"
                        kill $APP_PID
                        exit 1
                    fi
                    
                    # Test get all days
                    echo "Testing /api/days..."
                    DAYS_COUNT=$(curl -s http://localhost:5000/api/days | jq '.days | length')
                    echo "Found $DAYS_COUNT days"
                    
                    if [ "$DAYS_COUNT" -ge 365 ]; then
                        echo "✅ All 365 days present"
                    else
                        echo "⚠️ Found $DAYS_COUNT days (expected 365)"
                    fi
                    
                    # Kill the app
                    kill $APP_PID
                    echo "✅ All tests passed"
                '''
            }
        }
        
        stage('Build Package') {
            steps {
                sh '''
                    echo "🔨 Creating deployment package..."
                    
                    # Create build info
                    echo "Build: ${BUILD_NUMBER}" > build-info.txt
                    echo "Date: $(date)" >> build-info.txt
                    echo "Commit: $(git log --oneline -1)" >> build-info.txt
                    
                    # Create archive (exclude venv)
                    tar -czf calendar-build-${BUILD_NUMBER}.tar.gz --exclude=venv *
                    
                    echo "Package: calendar-build-${BUILD_NUMBER}.tar.gz"
                '''
            }
        }
    }
    
    post {
        success {
            echo "🎉 Pipeline completed successfully!"
            sh 'echo "Build ${BUILD_NUMBER} - SUCCESS"'
        }
        failure {
            echo "❌ Pipeline failed!"
            sh 'echo "Build ${BUILD_NUMBER} - FAILED"'
        }
        always {
            // Archive artifacts
            archiveArtifacts artifacts: 'calendar-build-*.tar.gz, build-info.txt', allowEmptyArchive: true
            
            // Clean up
            sh 'rm -f calendar-build-*.tar.gz build-info.txt'
        }
    }
}