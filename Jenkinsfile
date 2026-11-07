pipeline {
    agent any

    environment {
        AWS_REGION = 'us-west-1'
        AWS_ACCOUNT_ID = '426550965418'
        ECR_REPOSITORY = 'devops-ic4-app'
        ECR_REGISTRY = '426550965418.dkr.ecr.us-west-1.amazonaws.com'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$BUILD_NUMBER .
                    docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$BUILD_NUMBER $ECR_REGISTRY/$ECR_REPOSITORY:latest
                '''
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                    docker push $ECR_REGISTRY/$ECR_REPOSITORY:$BUILD_NUMBER
                    docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest
                '''
            }
        }
    }
}
