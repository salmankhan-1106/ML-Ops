pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'ml-api'
        DOCKER_TAG = 'latest'
        CONTAINER_NAME = 'ml-api-container'
        API_PORT = '8000'
    }
    
    triggers {
        // Poll GitHub every minute for changes in dataset folder
        pollSCM('* * * * *')
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo '=== Stage 1: Checking out code from GitHub ==='
                }
                checkout scm
            }
        }
        
        stage('Check Dataset Changes') {
            steps {
                script {
                    echo '=== Stage 2: Checking if dataset changed ==='
                    def changes = sh(
                        script: 'git diff HEAD^ HEAD --name-only',
                        returnStdout: true
                    ).trim()
                    
                    echo "Changed files: ${changes}"
                    
                    if (!changes.contains('dataset/train.csv')) {
                        echo 'Dataset not changed, skipping pipeline'
                        currentBuild.result = 'SUCCESS'
                        return
                    }
                    echo 'Dataset changed, proceeding with pipeline'
                }
            }
        }
        
        stage('Fetch Data') {
            steps {
                script {
                    echo '=== Stage 3: Fetching data from GitHub ==='
                    sh '''
                        echo "Data fetched from GitHub repository"
                        ls -la dataset/
                        head -5 dataset/train.csv
                    '''
                }
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                script {
                    echo '=== Stage 4: Setting up Python environment ==='
                    sh '''
                        python3 -m pip install --user --upgrade pip
                        python3 -m pip install --user -r requirements.txt
                    '''
                }
            }
        }
        
        stage('Train Model') {
            steps {
                script {
                    echo '=== Stage 5: Training model ==='
                    sh '''
                        python3 train.py
                        echo "Model training completed"
                        ls -la *.pkl
                    '''
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo '=== Stage 6: Building Docker image ==='
                    sh """
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker images | grep ${DOCKER_IMAGE}
                    """
                }
            }
        }
        
        stage('Stop Old Container') {
            steps {
                script {
                    echo '=== Stage 7: Stopping old container ==='
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                    """
                }
            }
        }
        
        stage('Run Docker Container') {
            steps {
                script {
                    echo '=== Stage 8: Running Docker container ==='
                    sh """
                        docker run -d \
                            --name ${CONTAINER_NAME} \
                            -p ${API_PORT}:${API_PORT} \
                            ${DOCKER_IMAGE}:${DOCKER_TAG}
                        
                        echo "Container started successfully"
                        docker ps | grep ${CONTAINER_NAME}
                    """
                }
            }
        }
        
        stage('Verify API') {
            steps {
                script {
                    echo '=== Stage 9: Verifying API is accessible ==='
                    sh '''
                        sleep 10
                        curl -f http://localhost:8000/metrics || exit 1
                        echo "API is accessible and responding"
                    '''
                }
            }
        }
        
        stage('Display Metrics') {
            steps {
                script {
                    echo '=== Stage 10: Displaying current metrics ==='
                    sh '''
                        echo "Current Model Metrics:"
                        curl -s http://localhost:8000/metrics | python3 -m json.tool
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo '=== Pipeline completed successfully ==='
            echo "API is accessible at: http://YOUR_SERVER_IP:${API_PORT}/metrics"
        }
        failure {
            echo '=== Pipeline failed ==='
            sh '''
                echo "Checking logs..."
                docker logs ${CONTAINER_NAME} || true
            '''
        }
        always {
            echo '=== Cleaning up ==='
            sh 'docker image prune -f || true'
        }
    }
}
