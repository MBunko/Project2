# Crazy Character roller- A D&D character randomiser

### Contents

1. [Brief](#Brief) 
2. [Software design](#Software-design)
 2.1. [ED](#ED)
 2.2. [Services](#Services)
 2.3. [CI pipeline](#CI-pipeline)
 2.4. [Swarm][#Swarm]
3. [Project planning](#Project-planning)
 3.1. [Asana board](#Asana-board)
 3.2. [Expanded user stories](#Expanded-user-stories)
4. [Risk assessment](#Risk-assessment)
5. [Testing](#Testing)
 5.1. [Unit testing](#Unit-testing)
 5.2. [Testing coverage](#Testing-coverage)
6. [Front end](#Front-end)
7. [Evaluation](#Evaluation)
 7.1. [Issues](#Issues)
 7.2. [Possible improvements](#Possible-improvements)
8. [Appendix](#Appendix)
 8.1. [Licensing](#Licensing)
 8.2. [Contributors and Acknowledgement](#Contributors-and-Acknowledgement)
 8.3. [Versioning](#Versioning)







## Brief  
This is a Devops project to create a simple web application made up of four services. The first being a front end that interacts with the back end and displays a page to the user. The second and third generate random objects and return them to the front end. The fourth must use the 2 other random objects to generate it's own object. This application must also be set up to utilise automatic continuous integration (CI) and deployment (CD) using a CI server. There are also the following requirements for the project:

* Using a Kanban board with full expansion on tasks needed to complete the project.
* An Application fully integrated using the Feature-Branch model into a Version Control System.
* Be built through a CI server and deployed to a cloud-based virtual machine.
* Have two different versions that can be easily swapped out.
* Use Webhooks so that Jenkins recreates and redeploys the changed application.
* The project must be deployed using containerisation and an orchestration tool.
* Use of an Ansible Playbook that will provision the environment that your application needs to run.
* The project must make use of a reverse proxy for accessibility to the user.

For my project I am making a dungeons and dragons character creator where services 2 and 3 generate a random character class and race from a list respectively. The fourth service takes both the above to generate a random but fitting description for the character which is all displayed on the first service with a click of a button.  


## Software design

Throughout the project various software has been used in the creation, testing, and implementation of the application.

### ED  

An ED is an entity diagram and shows the table used for this project. The table is used in the project to store the results rolled by users and the app displays the last 5 rolls. You can see the diagram below: 
  
  
![ERD][Initial ERD]  
 
The Id is the primary key as shown and the date is green because it was added later in production and was not part of the initial design but i thought it would be interesting for users to see how long ago the last rolls were. You will see how this information is displayed in the front end section.

### Services

Below you can see how my services interact with one another. The yellow arrows show the class generated by service 2 which is pulled to service 1 via a get request and is also posted to service 4. The red arrows indicate the same for the race generated by service 3. Finally the green is the descriptor generated by service 4 after utilising the data from services 2&3. Service one then uses the data in the front end seen by users.    

![Sv][Sv]

### CI pipeline

Below is a continuous integration (CI) pipeline diagram showing how all the software involved in the project connects.  

![CI][CI]

Here you can see the code was developed on Flask and pushed to Github, all changes were pushed to feature branches and merged to my dev branch although small issues caught in my dev branch have been changed within that branch directly. I then update my asana board with work done and use it determine my next tasks. At the same time Jenkins uses a webhook to  automatically pull the code down. It does this for both my dev branch and main branch which only has fully working and tested dev branches merged into it. The code includes a Jenkinsfile so that any Jenkins server can grab this code and build it if they so desire. The only thing they would need to do is set the credentials that are listed in the environment section of the Jenkinsfile on their Jenkins application(and set up their own MySql servers). Below you can see the order of operations for each build of the pipeline.

![CI1][CI1]

First the server uses pytest to test the code. You can see at the end it generates a report which uses Cobertura and Junit for the test results and coverage report which can be used to help debug if there are any issues (these are shown in the testing section). It then builds the services as container images using Docker-compose onto Docker hub as the artefacts unless rollback is set to true in which case it will pull a pre existing image later. It then sets up the docker swarm (explained below) and deploys the services built or the ones specified on Docker hub using docker-stack deploy through the swarm which is run by a manager node and used on Nginx which serves as the reverse proxy and the live environment for the users. This whole process is automatic.   

The build failures were caused by my webhook. I did not know that merging branches triggered the webhook for the branch being copied so both my dev and main branches would attempt to build and would interfere with one another. After noticing this my webhook was deactivated for my dev branch and only automatically builds my main branch. 

### Swarm

Below you can see a diagram of my docker swarm that is set up by the pipeline.

![Sw][Sw]

The swarm manager, both workers and the nginx balancer are all run on separate virtual machines on google cloud (this is also true for the Jenkins server). The manager pulls down the services and runs copies of them across the swarm workers and itself. For my project I have 2 workers and 3 replicas of each service. The tasks in the workers are individual copies of the containers for a service. This exists so that the individual containers aren't overloaded by heavy traffic and so that if either server or any container stops working the app will continue to run. Nginx then acts as a reverse proxy so it's IP is where users will actually visit the web app keeping them from directly accessing the back end. It also directs which tasks will be used for each user balancing the load and making sure the containers are distributed appropriately.

## Project planning

This project was planned and tracked using an Asana board.

### Asana board  
  
Below is the Asana board for the project:  
  
![TB1][TB1]  

The sections above are fairly self explanatory. The only thing in the not done section was using nexus as a repository for my docker images and docker hub was used instead for its ease of use. While nexus is more secure than docker hub this project is open source so people are free to downlaod my images and docker hub does still protect from people pushing their own changes up without my login information.  


### Expanded user stories  
  
Here is a table of the user stories above. The user stories exist so that I don't lose focus of why tasks on the board need to be done so that if there are any issues I can use the user stories for my work around:

|As a…|I want to…|	So that I can…|Priority|
|---|---|---|---|
|User|See a large range of possible characters|Reuse the app to roll future characters without being bored|Should
|User|See some previously rolled characters|See the variance of characters immediately|Should
|User|Have the application running during updates|Use the site anytime regardless of what's going on|Must
|User|Have a roll character button|Avoid refreshing the page every time I want a character|Could
|Host|Have changes automatically integrated and deployed/delivered|Save time on doing it manually in future|Must
|Host|Have tests run automatically|See results immediately upon commits|Must
|Host|Make sure users only have access to front end |Prevent unauthorized access to my code, database etc.|Must
|Host|Have an uncluttered back end|Run it cheaply and debug issues more easily|Should
|Host|Have passwords and secrets completely unaccessible|be certain that sensitive data is secured|Must




## Risk assessment  

### Start of project risk assessment

Below is my risk assessment from the start of the project.

![RA1][RA1]

### Final risk assessment

Below is my risk assessment from nearer the end of the project with a deeper understanding. You can see there are a few more risks identified as well as some updates to possible mitigating actions.

![RA2][RA2]

## Testing

Pytest was used for the testing as stated above since all the code to be tested was python based.


### Unit testing

For the unit tests i tested that all 4 services could be accessed with get requests without causing an error. For the first service I tested integration with the database by making sure that if something is in the database it can be read on the homepage. You can see in the code I used a separate DATABASE_URI for testing so that it wouldn't bring down the original. It is functionally identical as it uses the same table in the same server just within a different database. I also used mock testing to simulate returns from the other services to make sure it would correctly use, add and display the information to the homepage. This one test simultaneously tests create and read functionality.

For services 2 & 3 I tested that they would return one of the items in their lists when run to make sure they were doing their job. I had this test run 10 times for each using a for loop to test consistency since the result is random. I initially didn't do this and the tests failed once randomly several builds in because one of the items was misspelled in the test from the beginning which is why this change was implemented to catch issues with individual returns within less builds. 

For service 4 I tested that when certain data from services 2 and 3 was received it would randomly return one of the descriptions that would match for the data sent to it, testing proper functionality. I did not test this for additional imported values from services 2 and 3 because there are hundreds of possible combinations and since all the data would be received as basic text it would work equally for any of them as if anything within service 4 was improperly formatted to not work with say a specific class the whole thing would break as it is one line of code.    

I also did not do Selenium testing as with the simplicity of this app it would only test that physically pressing the roll button would work which is easily done in QA testing as it only needs to be done once since it is one line of code that acts as a redirect.

![Pytest][Pytest]

As you can see above all of my tests passed successfully showing that the program works as intended and passes functionality. This is from my dev branch and you can see that with previous builds there were failures. One of these was discussed above and the other was because when that build was created the database was offline showing that even when changes aren't relevant to the code tested that automated testing is still important as debugging when the app was not working would've been much harder without the test results.  

### Testing coverage

For the coverage test I used Pytest –-cov=application to check the testing coverage for everything within the application folder for each service as that is where all the code that runs the app itself is stored. 

![Cov][Cov]

![Cov1][Cov1]

As you can see my tests cover 100% of all files in the application folders meaning that the full breadth of the application has been tested making the tests a success. The dip in coverage in build 12 was caused by the database being offline crashing one of the tests. This shows the functionality of Cobertura being able to show results over multiple builds clearly in one graph making it more useful than a simple HTML report.

## Front end

This section will cover the front end of my project. As you can see below it displays all the information randomly generated from the four services in a coherent manner to give users their randomly rolled character.

![F1][F1]

Above is the home page for version one, it is the only page users can navigate to. The likely dead characters section shows the last 5 rolled characters stored in the database. 

![F2][F2]

The next picture shows version two. It has a button to roll a new character so the user doesn't have to reload the page to get a new character. It also has 2 new classes including the above Blood-hunter and the Artificer. The descriptors from service 4 have been updated to account for these and has 4 new descriptors, 2 specific to each new class. Finally the races have been reformatted to flow better as you can see the difference between Gnome being rolled in version one and Gnomish in version two. 

The important thing here is that the Jenkinfile is set up so that by entering a 1 or a 2 for the version in environments the pipeline will activate and deploy the chosen version allowing for easy, quick and convenient switching between versions and this can also be applied to future updates.



## Evaluation

### Issues

The main issue is that docker hub is used to store the images as mentioned above. Beyond what is mentioned above using nexus would have removed pull limits as docker hub only allows free users 200 pulls per six hours and nexus is a lot more customisable.

### Possible improvements

In future versions more descriptions can always be added for variety. To really push variance a second descriptor dictionary with more depth to the descriptions could be added to service 4 that follows on at the end on the homepage. Also customisability could be added letting users select whether they want the class and race to fit with one another making service 2 and 3 potentially dependent on one another.

## Appendix

### Licensing 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

This permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### Contributors and Acknowledgement 

Author: Michael Bunko

Acknowledgement: I would like to thank my trainers for their teaching and support including Harry Volker, Jay Grindrod, Nathan Forester and Peter Rhodes.
I would also like to thank the members of my teams during training for their help and support as well as the community of stack overflow.

### Versioning

App version: 2

Version 1 code is avaiable to view in the branch feature-v1 and if you wish to deploy this application remember it will deploy whichever version is selected in the Jenkinsfile.

There are currently no other working versions beyond these 2 and their differences are highlighted in the front end section above.

[Initial ERD]: https://i.imgur.com/59nalIJ.png
[TB1]: https://i.imgur.com/nI9mu4Z.png
[CI]: https://i.imgur.com/MAjGhBP.png
[Sv]: https://i.imgur.com/PH4btzi.png
[Sw]: https://i.imgur.com/plscEEM.png
[RA1]: https://i.imgur.com/9SN6DUH.png
[RA2]: https://i.imgur.com/u2bVFch.png
[Pytest]: https://i.imgur.com/n25GBku.png
[Cov]: https://i.imgur.com/0f6hBDf.png
[Cov1]: https://i.imgur.com/zX4AjEg.png
[F1]: https://i.imgur.com/k4eWWGb.png
[F2]: https://i.imgur.com/jPSWqO3.png
[CI1]: https://i.imgur.com/ZcU1I6I.png
