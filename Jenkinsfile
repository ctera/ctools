@Library('devops-library') l1
pipeline {
    agent {
        node { 
            label "microservices-agent-automation"
        }
    }

    stages {
        stage("First_stage") {
            steps {
                printTitle "First_stage"

                script {
                    sh "ls -la"
                }
            }
        }
    }
}
                    
                    