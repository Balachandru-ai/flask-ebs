pipeline {
    agent {
        label 'deploy'
    }

    environment {
        AWS_REGION       = 'eu-north-1'
        AWS_ACCOUNT_ID   = '201063584539'
        ECR_REPOSITORY   = 'flask-ebs'
        IMAGE_NAME       = 'flask-ebs'

        BLUE_CONTAINER   = 'flask-blue'
        GREEN_CONTAINER  = 'flask-green'

        BLUE_PORT        = '8003'
        GREEN_PORT       = '8004'
        CONTAINER_PORT   = '8000'

        ECR_REGISTRY     = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        IMAGE_TAG        = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m pip install -r requirements.txt
                '''
            }
        }

        stage('Code Analysis') {
            steps {
                sh '''
                    python3 -m py_compile app.py
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} \
                        -t ${IMAGE_NAME}:latest \
                        .
                '''
            }
        }

        stage('Docker Image Scan') {
            steps {
                sh '''
                    trivy image \
                        --severity HIGH,CRITICAL \
                        --exit-code 1 \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password \
                        --region ${AWS_REGION} | \
                    docker login \
                        --username AWS \
                        --password-stdin ${ECR_REGISTRY}
                '''
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh '''
                    docker tag \
                        ${IMAGE_NAME}:${IMAGE_TAG} \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}

                    docker tag \
                        ${IMAGE_NAME}:${IMAGE_TAG} \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest

                    docker push \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}

                    docker push \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest
                '''
            }
        }

        stage('Deploy Green') {
            steps {
                sh '''
                    echo "Stopping old Green container..."

                    docker stop ${GREEN_CONTAINER} || true
                    docker rm ${GREEN_CONTAINER} || true

                    echo "Starting new Green container..."

                    docker run -d \
                        --name ${GREEN_CONTAINER} \
                        -p ${GREEN_PORT}:${CONTAINER_PORT} \
                        ${IMAGE_NAME}:${IMAGE_TAG}

                    sleep 10

                    docker ps | grep ${GREEN_CONTAINER}
                '''
            }
        }

        stage('Green Health Check') {
            steps {
                sh '''
                    echo "Checking Green application..."

                    curl -f http://localhost:${GREEN_PORT}/ || {
                        echo "Green health check failed!"
                        docker logs ${GREEN_CONTAINER}
                        exit 1
                    }

                    echo "Green application is healthy."
                '''
            }
        }

        stage('Switch Traffic to Green') {
            steps {
                sh '''
                    echo "Switching traffic to Green..."

                    sudo sed -i \
                    's/server 127.0.0.1:8003 weight=[0-9]*;/server 127.0.0.1:8003 weight=0;/' \
                    /etc/nginx/nginx.conf

                    sudo sed -i \
                    's/server 127.0.0.1:8004 weight=[0-9]*;/server 127.0.0.1:8004 weight=100;/' \
                    /etc/nginx/nginx.conf

                    sudo nginx -t

                    sudo systemctl reload nginx
                '''
            }
        }

        stage('Production Health Check') {
            steps {
                sh '''
                    echo "Checking application through Nginx..."

                    curl -f http://localhost:8000/ || {
                        echo "Production health check failed!"
                        exit 1
                    }

                    echo "Production application is healthy."
                '''
            }
        }
    }

    post {

        success {
            echo 'Deployment completed successfully!'
        }

        failure {
            echo 'Deployment failed!'

            sh '''
                docker ps -a
                docker logs ${GREEN_CONTAINER} || true
            '''
        }

        always {
            echo 'Pipeline execution completed.'
        }
    }
}
