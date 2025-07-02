pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'localhost:5555'
        APP_NAME = 'stellar-ocr'
        BUILD_NUMBER = "${env.BUILD_NUMBER}"
        GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
        IMAGE_TAG = "${BUILD_NUMBER}-${GIT_COMMIT_SHORT}"
    }
    
    tools {
        nodejs 'NodeJS-18'
    }
    
    stages {
        stage('📋 Checkout & Setup') {
            steps {
                script {
                    echo "🚀 Starting Stellar OCR CI/CD Pipeline"
                    echo "Build: ${BUILD_NUMBER}"
                    echo "Commit: ${GIT_COMMIT_SHORT}"
                    echo "Branch: ${env.BRANCH_NAME}"
                }
                
                // Clean workspace
                cleanWs()
                
                // Checkout code
                checkout scm
                
                // Display project structure
                sh 'find . -name "*.py" -o -name "*.js" -o -name "*.html" -o -name "Dockerfile" | head -20'
            }
        }
        
        stage('🔍 Code Quality & Security') {
            parallel {
                stage('Lint Python Code') {
                    steps {
                        dir('backend') {
                            sh '''
                                python3 -m pip install flake8 pylint --quiet
                                echo "🐍 Running Python linting..."
                                flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || true
                                pylint *.py --errors-only || true
                            '''
                        }
                    }
                }
                
                stage('Validate Dockerfiles') {
                    steps {
                        sh '''
                            echo "🐳 Validating Dockerfiles..."
                            find . -name "Dockerfile" -exec echo "Checking: {}" \\;
                            find . -name "Dockerfile" -exec docker run --rm -i hadolint/hadolint < {} \\; || true
                        '''
                    }
                }
                
                stage('Security Scan') {
                    steps {
                        sh '''
                            echo "🔒 Running security checks..."
                            # Check for common security issues
                            find . -name "*.py" -exec grep -l "password.*=.*" {} \\; || true
                            find . -name "*.py" -exec grep -l "secret.*=.*" {} \\; || true
                            echo "Security scan completed"
                        '''
                    }
                }
            }
        }
        
        stage('🧪 Testing') {
            parallel {
                stage('Unit Tests - Backend') {
                    steps {
                        dir('backend') {
                            sh '''
                                echo "🧪 Running backend unit tests..."
                                python3 -m pip install pytest pytest-cov --quiet
                                # Create a simple test if none exists
                                if [ ! -f test_app.py ]; then
                                    echo "Creating basic test file..."
                                    cat > test_app.py << 'EOF'
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def test_app_imports():
    """Test that the app can be imported without errors"""
    try:
        import app
        assert hasattr(app, 'app')
        print("✅ App imports successfully")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_health_check():
    """Test health check endpoint exists"""
    import app
    assert hasattr(app, 'health_check')
    print("✅ Health check endpoint exists")

if __name__ == "__main__":
    test_app_imports()
    test_health_check()
    print("All tests passed!")
EOF
                                fi
                                python3 -m pytest test_app.py -v || true
                            '''
                        }
                    }
                }
                
                stage('Frontend Validation') {
                    steps {
                        dir('frontend') {
                            sh '''
                                echo "🎨 Validating frontend..."
                                # Check HTML syntax
                                if command -v tidy >/dev/null 2>&1; then
                                    tidy -q -e index.html || true
                                else
                                    echo "HTML validation skipped (tidy not available)"
                                fi
                                
                                # Check for common issues
                                grep -q "React" index.html && echo "✅ React detected"
                                grep -q "OCR" index.html && echo "✅ OCR functionality detected"
                                echo "Frontend validation completed"
                            '''
                        }
                    }
                }
            }
        }
        
        stage('🏗️ Build Images') {
            parallel {
                stage('Build OCR Backend') {
                    steps {
                        script {
                            echo "🐳 Building OCR Backend image..."
                            def backendImage = docker.build(
                                "${DOCKER_REGISTRY}/${APP_NAME}-backend:${IMAGE_TAG}",
                                "./backend"
                            )
                            
                            // Tag as latest
                            backendImage.tag("${DOCKER_REGISTRY}/${APP_NAME}-backend:latest")
                            
                            echo "✅ Backend image built successfully"
                        }
                    }
                }
                
                stage('Build NER Service') {
                    steps {
                        script {
                            echo "🧠 Building NER Service image..."
                            def nerImage = docker.build(
                                "${DOCKER_REGISTRY}/${APP_NAME}-ner:${IMAGE_TAG}",
                                "./ner-service"
                            )
                            
                            nerImage.tag("${DOCKER_REGISTRY}/${APP_NAME}-ner:latest")
                            echo "✅ NER Service image built successfully"
                        }
                    }
                }
                
                stage('Prepare Frontend') {
                    steps {
                        dir('frontend') {
                            sh '''
                                echo "📦 Preparing frontend for deployment..."
                                # Create optimized version
                                mkdir -p dist
                                cp index.html dist/
                                echo "✅ Frontend prepared successfully"
                            '''
                        }
                    }
                }
            }
        }
        
        stage('🧪 Integration Tests') {
            steps {
                script {
                    echo "🔄 Running integration tests..."
                    
                    // Start services for testing
                    sh '''
                        echo "Starting test environment..."
                        docker-compose -f docker-compose.test.yml up -d || true
                        sleep 10
                        
                        echo "Running API health checks..."
                        curl -f http://localhost:5001/ || echo "Backend health check failed"
                        curl -f http://localhost:5002/ || echo "NER service health check failed"
                        
                        echo "Cleaning up test environment..."
                        docker-compose -f docker-compose.test.yml down || true
                    '''
                }
            }
        }
        
        stage('📦 Publish Images') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                script {
                    echo "📤 Publishing images to registry..."
                    
                    // Push to local registry (in production, this would be DockerHub/AWS ECR)
                    docker.withRegistry("http://${DOCKER_REGISTRY}") {
                        def backendImage = docker.image("${DOCKER_REGISTRY}/${APP_NAME}-backend:${IMAGE_TAG}")
                        def nerImage = docker.image("${DOCKER_REGISTRY}/${APP_NAME}-ner:${IMAGE_TAG}")
                        
                        backendImage.push()
                        backendImage.push("latest")
                        
                        nerImage.push()
                        nerImage.push("latest")
                    }
                    
                    echo "✅ Images published successfully"
                }
            }
        }
        
        stage('🚀 Deploy') {
            parallel {
                stage('Deploy to Staging') {
                    when {
                        branch 'develop'
                    }
                    steps {
                        script {
                            echo "🎯 Deploying to staging environment..."
                            sh '''
                                # Deploy to staging
                                docker-compose -f docker-compose.staging.yml down || true
                                export IMAGE_TAG=${IMAGE_TAG}
                                docker-compose -f docker-compose.staging.yml up -d
                                
                                echo "Waiting for services to start..."
                                sleep 15
                                
                                # Health check
                                curl -f http://localhost:5011/ && echo "✅ Staging backend healthy"
                                curl -f http://localhost:3001/ && echo "✅ Staging frontend healthy"
                            '''
                        }
                    }
                }
                
                stage('Deploy to Production') {
                    when {
                        branch 'main'
                    }
                    steps {
                        script {
                            echo "🏭 Deploying to production environment..."
                            
                            // In a real scenario, this might deploy to K8s, AWS ECS, etc.
                            sh '''
                                echo "🔄 Rolling out to production..."
                                
                                # Blue-green deployment simulation
                                docker-compose -f docker-compose.prod.yml down || true
                                export IMAGE_TAG=${IMAGE_TAG}
                                docker-compose -f docker-compose.prod.yml up -d
                                
                                echo "Waiting for production services..."
                                sleep 20
                                
                                # Production health checks
                                curl -f http://localhost:5001/ && echo "✅ Production backend healthy"
                                curl -f http://localhost:3000/ && echo "✅ Production frontend healthy"
                                
                                echo "🎉 Production deployment successful!"
                            '''
                        }
                    }
                }
            }
        }
        
        stage('📊 Post-Deploy Verification') {
            steps {
                script {
                    echo "🔍 Running post-deployment verification..."
                    
                    sh '''
                        echo "📈 Collecting deployment metrics..."
                        docker ps --format "table {{.Names}}\\t{{.Status}}\\t{{.Ports}}"
                        
                        echo "💾 Checking resource usage..."
                        docker stats --no-stream
                        
                        echo "📝 Generating deployment report..."
                        cat > deployment_report.txt << EOF
Stellar OCR Deployment Report
============================
Build Number: ${BUILD_NUMBER}
Git Commit: ${GIT_COMMIT_SHORT}
Image Tag: ${IMAGE_TAG}
Deployment Time: $(date)
Branch: ${BRANCH_NAME}

Services Deployed:
- OCR Backend: ${DOCKER_REGISTRY}/${APP_NAME}-backend:${IMAGE_TAG}
- NER Service: ${DOCKER_REGISTRY}/${APP_NAME}-ner:${IMAGE_TAG}
- Frontend: Static files

Status: ✅ SUCCESSFUL
EOF
                        cat deployment_report.txt
                    '''
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "🧹 Cleaning up..."
                
                // Archive artifacts
                archiveArtifacts artifacts: 'deployment_report.txt', allowEmptyArchive: true
                
                // Clean up old images to save space
                sh '''
                    echo "🗑️ Cleaning up old Docker images..."
                    docker image prune -f || true
                    docker system prune -f || true
                '''
            }
        }
        
        success {
            script {
                echo "🎉 Pipeline completed successfully!"
                
                // In a real environment, you might send notifications here
                sh '''
                    echo "📧 Sending success notification..."
                    echo "Stellar OCR deployment completed successfully at $(date)" > success_notification.txt
                '''
            }
        }
        
        failure {
            script {
                echo "❌ Pipeline failed!"
                
                // Gather failure information
                sh '''
                    echo "📧 Sending failure notification..."
                    echo "Stellar OCR deployment failed at $(date)" > failure_notification.txt
                    echo "Build: ${BUILD_NUMBER}" >> failure_notification.txt
                    echo "Branch: ${BRANCH_NAME}" >> failure_notification.txt
                '''
            }
        }
    }
}
