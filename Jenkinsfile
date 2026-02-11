pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                git 'https://github.com/Balachandru-ai/flask-ebs.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run App') {
            steps {
                sh '''
                nohup python3 app.py > output.log 2>&1 &
                '''
            }
        }
    }
}

