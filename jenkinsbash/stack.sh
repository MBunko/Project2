#!/bin/bash
scp -i ~/.ssh/id_rsa docker-compose.yaml jenkins@projectm:/home/jenkins/docker-compose.yaml
ssh -i ~/.ssh/id_rsa jenkins@projectm << EOF
    export DATABASE_URI=${DATABASE_URI} app_version=${app_version}
    docker stack deploy --compose-file /home/jenkins/docker-compose.yaml roller
EOF
