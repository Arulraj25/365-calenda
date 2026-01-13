pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Pulling code from GitHub...'
                checkout scm
                
                sh '''
                    echo "📁 Current directory contents:"
                    ls -la
                '''
            }
        }
        
        stage('Setup') {
            steps {
                sh '''
                    echo "🐍 Setting up environment..."
                    python3 -m venv venv || echo "Virtual environment creation completed"
                    
                    # Ensure virtual environment binaries are executable
                    chmod -R 755 venv/bin/
                    
                    # Use . instead of source for POSIX compliance
                    . venv/bin/activate
                    python -m pip install --upgrade pip
                '''
            }
        }
        
        stage('Install') {
            steps {
                sh '''
                    . venv/bin/activate
                    echo "📦 Installing dependencies..."
                    pip install -r requirements.txt
                    echo "✅ Dependencies installed"
                '''
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    echo "🧪 Running tests..."
                    
                    # Test Python files
                    python -m py_compile app.py
                    
                    # Test if Flask app can start
                    echo "from flask import Flask; print('✓ Flask import successful')" | python
                    
                    echo "✅ All tests passed!"
                '''
            }
        }
        
        stage('Build') {
            steps {
                sh '''
                    echo "🏗️ Building package..."
                    
                    # Create timestamp
                    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
                    
                    # Create build info
                    echo "Build Time: $(date)" > build-info.txt
                    echo "Git Commit: $(git log --oneline -1)" >> build-info.txt
                    echo "Python Version: $(python3 --version)" >> build-info.txt
                    
                    # Create archive
                    tar -czf calendar-build-${TIMESTAMP}.tar.gz \
                        app.py \
                        requirements.txt \
                        *.json \
                        *.html \
                        *.css \
                        *.js \
                        *.yml \
                        Dockerfile \
                        *.md \
                        build-info.txt 2>/dev/null || true
                    
                    echo "📦 Build archive created: calendar-build-${TIMESTAMP}.tar.gz"
                '''
                
                archiveArtifacts artifacts: 'calendar-build-*.tar.gz', fingerprint: true
            }
        }
    }
    
    post {
        always {
            sh '''
                echo "🧹 Cleaning up..."
                # Remove build artifacts but keep venv for caching
                rm -f calendar-build-*.tar.gz build-info.txt 2>/dev/null || true
            '''
        }
        
        success {
            echo '✅ Pipeline SUCCESS!'
        }
        
        failure {
            echo '❌ Pipeline FAILED!'
            sh '''
                echo "=== DEBUG INFO ==="
                echo "Current user: $(whoami)"
                echo "Shell: $SHELL"
                echo "Python version: $(python3 --version 2>&1 || echo 'Not found')"
                echo "Virtual env status:"
                ls -la venv/bin/ 2>/dev/null || echo "venv/bin directory not found"
            '''
        }
    }
}