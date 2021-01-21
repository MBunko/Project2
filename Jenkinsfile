pipeline{
    agent any
    environment{
        DATABASE_URI = credentials("DATABASE_URI")
        DATABASE_URI2= credentials("DATABASE_URI2")
    }
    stages{
        stage("Configure Swarm"){
            steps{
                sh "cd ansible && /home/jenkins/.local/bin/ansible-playbook -i inventory playbook.yaml"
            }
        }
        stage("Deploy application"){
            steps{
                sh "bash jenkins/deploy_stack.sh"
            }
        }
    }
}