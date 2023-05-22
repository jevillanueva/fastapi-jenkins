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
        stage('Deploy') {
            steps {
                sshagent(credentials: ['kubernetes']) {
                    sh '''
                    [ -d ~/.ssh ] || mkdir ~/.ssh && chmod 0700 ~/.ssh
                    ssh-keyscan -t rsa,dsa ${K8S} >> ~/.ssh/known_hosts
                    ssh ubuntu@${K8S} mkdir -p jenkins/${NAME_IMAGE}
                    scp -r k8s/* ubuntu@${K8S}:jenkins/${NAME_IMAGE}
                    ssh ubuntu@${K8S} kubectl apply -f jenkins/${NAME_IMAGE}/deploy.yaml
                    ssh ubuntu@${K8S} kubectl apply -f jenkins/${NAME_IMAGE}/service.yaml
                    '''
                }
            }
        }
    }
}
