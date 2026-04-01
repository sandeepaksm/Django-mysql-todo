pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "your-dockerhub-username/django-todo"
        DOCKER_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/saikksub/Django-mysql-todo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }

        stage('Run Migrations') {
            steps {
                sh """
                    docker-compose -f docker-compose.yml up -d db
                    sleep 20
                    docker-compose -f docker-compose.yml run --rm web python manage.py migrate
                    docker-compose -f docker-compose.yml down
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-cred',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                        echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                    """
                }
            }
        }

    }

    post {
        always {
            sh 'docker-compose down || true'
        }
    }
}
