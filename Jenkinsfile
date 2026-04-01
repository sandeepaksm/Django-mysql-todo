pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "sandeep2862/django-todo"
        DOCKER_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/sandeepaksm/Django-mysql-todo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build --no-cache -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }

        stage('Run Tests') {
    steps {
        sh """
            docker-compose -f docker-compose.yml up -d db
            sleep 20
            docker exec django-todo-pipeline01-db-1 mysql -uroot -prootpass -e "GRANT ALL PRIVILEGES ON *.* TO 'todouser'@'%'; FLUSH PRIVILEGES;"
            docker-compose -f docker-compose.yml run --rm web python manage.py test
            docker-compose -f docker-compose.yml down -v
        """
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
            sh 'docker-compose down -v || true'
        }
    }
}

