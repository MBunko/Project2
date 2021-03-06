pipeline{
    agent any
    environment{
        DATABASE_URI = credentials("DATABASE_URI")
        DATABASE_URI2= credentials("DATABASE_URI2")
        app_version=3
        rollback='true'
    }
    stages{
        stage("Tests"){
            steps{
                sh "bash jenkinsbash/test.sh"
            }
        }
        stage("Build and push images"){
            steps{
                script{
                    if (env.rollback == 'false') {
                        sh "docker rmi -f \$(docker images -qa) || true"
                        sh "docker-compose build --parallel --build-arg APP_VERSION=${app_version} && docker-compose push"
                    }
                }     
            }
        }
        
        stage("Configure Swarm"){
            steps{
                sh "cd ansible && /home/jenkins/.local/bin/ansible-playbook -i inventory playbook.yaml"
            }
        }
        stage("Deploy application"){
            steps{
                sh "bash jenkinsbash/stack.sh"
            }
        }
    }    
    post{
        always{
            junit "**/junit.xml"
            cobertura coberturaReportFile: '**/coverage.xml', failNoReports: false, failUnstable: false, onlyStable: false
        }
    }
}
