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
                ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Restart App') {
            steps {
                sh '''
                pkill -f gunicorn || true
                nohup ./venv/bin/gunicorn app:app --bind 0.0.0.0:5000 > app.log 2>&1 &
                '''
            }
        }
    }
}

