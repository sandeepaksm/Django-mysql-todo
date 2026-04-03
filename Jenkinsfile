pipeline {
    agent { label 'Jenkins_Agent' }
    environment {
        DOCKER_IMAGE = "sandeep2862/django-todo"
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    stages {
        stage('Check Commit') {
            steps {
                script {
                    def commitMsg = sh(script: 'git log -1 --pretty=%B', returnStdout: true).trim()
                    if (commitMsg.startsWith('Update image to version')) {
                        currentBuild.result = 'ABORTED'
                        error('Skipping build triggered by Jenkins manifest update')
                    }
                }
            }
        }
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/sandeepaksm/Django-mysql-todo.git'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withCredentials([string(credentialsId: 'SONAR_AUTH_TOKEN', variable: 'SONAR_TOKEN')]) {
                    sh """
                        /opt/sonar-scanner/bin/sonar-scanner \
                            -Dsonar.projectKey=django-todo \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=http://3.26.165.35:9000 \
                            -Dsonar.login=${SONAR_TOKEN}
                    """
                }
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
                    docker exec django-todo-pipeline_db_1 mysql -uroot -prootpass -e "GRANT ALL PRIVILEGES ON *.* TO 'todouser'@'%'; FLUSH PRIVILEGES;"
                    docker run --rm \
                        --network django-todo-pipeline_default \
                        -e DB_NAME=tododb \
                        -e DB_USER=todouser \
                        -e DB_PASSWORD=todopass \
                        -e DB_HOST=django-todo-pipeline-db_1 \
                        -e DB_PORT=3306 \
                        -e SECRET_KEY=your-secret-key \
                        ${DOCKER_IMAGE}:${DOCKER_TAG} python manage.py test
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
        stage('Update K8s Manifest') {
            steps {
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GITHUB_TOKEN')]) {
                    sh """
                        git config user.email "sandeepaksm@gmail.com"
                        git config user.name "sandeepaksm"
                        sed -i 's|sandeep2862/django-todo:.*|sandeep2862/django-todo:${DOCKER_TAG}|g' k8s/deployment.yaml
                        git add k8s/deployment.yaml
                        git diff --staged --quiet || git commit -m "Update image to version ${DOCKER_TAG}"
                        git push https://${GITHUB_TOKEN}@github.com/sandeepaksm/Django-mysql-todo.git HEAD:main
                    """
                }
            }
        }
    }
    post {
        always {
            sh 'docker-compose down -v || true'
            sh 'docker image prune -f || true'
        }
    }
}
