pipeline{
    agent any
    environment{
        DATABASE_URI = credentials("DATABASE_URI")
        DATABASE_URI2= credentials("DATABASE_URI2")
    }
    stages{
        stage("Tests"){
            steps{
                python3 -m venv venv
                pip3 install -r requirements.txt
                pip3 install pytest pytest-cov flask_testing requests_mock
                python3 -m pytest --cov=application --cov-report xml --cov-report term-missing --junitxml junit.xml
                deactivate 
                cd..
            }
        }         
        //
       // stage("Configure Swarm"){
       //     steps{
         //       sh "cd ansible && /home/jenkins/.local/bin/ansible-playbook -i inventory playbook.yaml"
            }
        }
        //stage("Deploy application"){
          //  steps{
                //Still need to build deploy.sh
         //       sh "bash jenkins/deploy.sh"
 //           }
//        }
    }
}
