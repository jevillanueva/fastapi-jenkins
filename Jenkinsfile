pipeline {
    agent any
    environment {
        NAME_IMAGE = 'jevillanueva/fastapi-jenkins'
        K8S = 'a.k8.jevillanueva.dev'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
    }
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/jevillanueva/fastapi-jenkins.git'
            }
        }
        stage('Login') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t ${NAME_IMAGE} .'
            }
        }
        stage('Test') {
            steps {
                sh 'docker run ${NAME_IMAGE} python test.py'
            }
        }
        stage('Push') {
            steps {
                sh 'docker push ${NAME_IMAGE}'
            }
        }
    }
}
