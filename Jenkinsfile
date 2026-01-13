pipeline {
    agent any
    
    tools {
        python 'Python3'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'echo "Repository: ${env.GIT_URL}"'
                sh 'echo "Branch: ${env.BRANCH_NAME}"'
                sh 'git log --oneline -3'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "Installing Python dependencies..."
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    echo "Running application tests..."
                    
                    # Check if app.py exists
                    if [ ! -f "app.py" ]; then
                        echo "ERROR: app.py not found!"
                        exit 1
                    fi
                    
                    # Check Python syntax
                    python -m py_compile app.py
                    
                    # Simple test: Start app and check health endpoint
                    echo "Starting application in background..."
                    python app.py &
                    APP_PID=$!
                    
                    # Wait for app to start
                    sleep 5
                    
                    # Test health endpoint
                    echo "Testing health endpoint..."
                    curl -f http://localhost:5000/api/health || (kill $APP_PID && exit 1)
                    
                    # Test get all days
                    echo "Testing /api/days endpoint..."
                    DAYS_COUNT=$(curl -s http://localhost:5000/api/days | jq '.days | length')
                    echo "Found $DAYS_COUNT special days"
                    
                    if [ "$DAYS_COUNT" -lt 365 ]; then
                        echo "ERROR: Expected at least 365 days, got $DAYS_COUNT"
                        kill $APP_PID
                        exit 1
                    fi
                    
                    # Test search
                    echo "Testing search endpoint..."
                    SEARCH_RESULT=$(curl -s "http://localhost:5000/api/search?q=new%20year" | jq '. | length')
                    echo "Search results: $SEARCH_RESULT"
                    
                    # Kill the app
                    kill $APP_PID
                    
                    echo "✅ All tests passed!"
                '''
            }
        }
        
        stage('Build & Package') {
            steps {
                sh '''
                    echo "Creating deployment package..."
                    
                    # Create version file
                    echo "Version: ${BUILD_NUMBER}" > version.txt
                    echo "Build Date: $(date)" >> version.txt
                    echo "Commit: $(git rev-parse HEAD)" >> version.txt
                    
                    # Create archive
                    tar -czf 365-calendar-build-${BUILD_NUMBER}.tar.gz \
                        index.html \
                        style.css \
                        script.js \
                        app.py \
                        requirements.txt \
                        version.txt
                    
                    echo "Package created: 365-calendar-build-${BUILD_NUMBER}.tar.gz"
                '''
            }
        }
    }
    
    post {
        success {
            echo "✅ Pipeline completed successfully!"
            sh '''
                echo "Build ${BUILD_NUMBER} passed!"
                # You can add deployment steps here
            '''
        }
        failure {
            echo "❌ Pipeline failed!"
            sh 'echo "Build ${BUILD_NUMBER} failed. Check logs for details."'
        }
        always {
            // Archive artifacts
            archiveArtifacts artifacts: '365-calendar-build-*.tar.gz, version.txt', allowEmptyArchive: true
            
            // Clean up
            sh 'rm -f 365-calendar-build-*.tar.gz version.txt'
            
            // Create simple report
            sh '''
                echo "Build Report" > build-report.txt
                echo "=============" >> build-report.txt
                echo "Status: ${currentBuild.result}" >> build-report.txt
                echo "Build: ${BUILD_NUMBER}" >> build-report.txt
                echo "Duration: ${currentBuild.durationString}" >> build-report.txt
                echo "URL: ${BUILD_URL}" >> build-report.txt
            '''
        }
    }
}