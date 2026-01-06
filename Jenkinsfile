pipeline {
    agent any

    options {
        retry(3)
    }

    environment {
        DOCKERHUB_REPO = 'dn070017/cicd_practice'
        GIT_HASH = "${env.GIT_COMMIT?.take(7) ?: 'unknown'}"
        DOCKER_TAG = "${env.BRANCH_NAME == 'main' ? 'latest' : env.BRANCH_NAME}"
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Continuous Integration') {
            stages {
                stage('Checkout') {
                    steps {
                        checkout scm
                    }
                }

                stage('Build') {
                    steps {
                        script {
                            echo "🚀 Building on node: ${env.NODE_NAME}"
                            echo "📦 Branch: ${env.BRANCH_NAME}, Commit: ${env.GIT_HASH}"

                            sh """
                                docker build \
                                    --build-arg BUILD_ENV=${env.BRANCH_NAME == 'main' ? 'production' : 'develop'} \
                                    --cache-from ${DOCKERHUB_REPO}:${DOCKER_TAG} \
                                    -t ${DOCKERHUB_REPO}:${env.GIT_HASH} \
                                    -t ${DOCKERHUB_REPO}:${DOCKER_TAG} \
                                    .
                            """
                        }
                    }
                }

                stage('Test') {
                    steps {
                        script {
                            echo '🧪 Running tests...'
                            sh "docker run --rm ${DOCKERHUB_REPO}:${env.GIT_HASH} poetry run tox"
                        }
                    }
                }
            }
        }

        stage('Continuous Deployment') {
            when {
                allOf {
                    expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
                    anyOf {
                        branch 'main'
                        branch 'develop'
                    }
                }
            }

            stages {
                stage('Manual Approval') {
                    when {
                        branch 'develop'
                        branch 'main'
                    }
                    steps {
                        script {
                            timeout(time: 1, unit: 'HOURS') {
                                input(
                                    message: "Deploy ${env.GIT_HASH} to DockerHub as 'latest'?",
                                    ok: 'Deploy'
                                )
                            }
                        }
                    }
                }

                stage('Push to DockerHub') {
                    steps {
                        script {
                            echo '🐳 Pushing to DockerHub...'
                            withCredentials([usernamePassword(
                                credentialsId: 'dockerhub-credentials',
                                usernameVariable: 'DOCKER_USER',
                                passwordVariable: 'DOCKER_PASS'
                            )]) {
                                sh """
                                    echo "\$DOCKER_PASS" | docker login -u "\$DOCKER_USER" --password-stdin

                                    # Push commit hash tag
                                    docker push ${DOCKERHUB_REPO}:${env.GIT_HASH}

                                    # Push branch tag (develop or latest)
                                    docker push ${DOCKERHUB_REPO}:${DOCKER_TAG}

                                    docker logout
                                """
                            }
                            echo "✅ Successfully pushed ${DOCKERHUB_REPO}:${env.GIT_HASH} and ${DOCKERHUB_REPO}:${DOCKER_TAG}"
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
        always {
            script {
                echo '🧹 Cleaning up Docker images...'
                sh """
                    docker rmi ${DOCKERHUB_REPO}:${env.GIT_HASH} || true
                    docker rmi ${DOCKERHUB_REPO}:${DOCKER_TAG} || true
                """
            }
        }
    }
}
