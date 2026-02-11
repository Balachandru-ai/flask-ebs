pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                sh '''
                pip3 install -r requirements.txt
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                echo "Stopping old gunicorn if running"
                pkill -f gunicorn || true

                echo "Starting gunicorn"
                nohup /var/lib/jenkins/.local/bin/gunicorn app:app --bind 0.0.0.0:5000 > app.log 2>&1 &
                '''
            }
        }
    }
}

