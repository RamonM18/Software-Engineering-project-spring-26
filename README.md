# Software-Engineering-project-spring-26
Photon project for Software Engineering 

Table with team members' name and username

| Name            | GitHub Username |
|-----------------|-----------------|
| Ramon Morales   | RamonM18        |
| Kyle Schwartz   | kdschw          |
| Michael Knepler | MichaelK6       |
| Steven Hale     | StevenHale11    |

## How to run the program
### First time setup
1. login to the VM with username and password: student
2. open terminal and go to home directory
3. cd ~
4. sudo apt-get update
   - If it asks for a password, use student
6. Clone the repository
   - git clone https://github.com/RamonM18/Software-Engineering-project-spring-26.git
7. Navigate to the project
    - cd ~/Software-Engineering-project-spring-26
8. Run the install script and it will have directions for you in the terminal on how to compile and run the program
    - bash install.sh

### Running the program after first time setup
1. Navigate to project directory
   - cd ~/Software-Engineering-project-spring-26
2. Pull changes from GitHub
   - git pull origin main
3. Compile and run
   - javac -cp ".:lib/postgresql-42.7.1.jar" *.java
   - java -cp ".:lib/postgresql-42.7.1.jar" Main

## Sprint 2 Overview

For Sprint 2, our team completed the following:

- Created team Github repository
- Implemented splash screen
- Created player entry screen
- Connected application to PostgreSQL database
- Added ability to insert and retrieve players from database
- Set up UDP sockets (7500 broadcast, 7501 receive)
- Broadcast equipment ID after each player addition
- Added option to change network address for UDP sockets
- Made weekly Slack status reports
- Created Trello task assignments for each team member
- Each team member made at least one programming commit
- Included install script for project setup

## How the Program Works

When the program starts:
- A spash screen is displayed for a few seconds
- The system automatically transitions to the Player Entry Screen

Player Entry Screen:
- User enters player ID
- Application connects to the PostSQL database
- If player ID is found, the codename is retrieved
- If player ID is not found, user is prompted to enter a new codename
- User enters equipment ID
- Equipment ID is broadcasted using UDP on port 7500

Database allows for two main operations:
  - These operations allows the user to add 
  - Check for existing players

Network Communication Uses Two UDP Sockets
  - Port 7500 for broadcasting
  - Port 7501 for receiving


## Project structure

- **Player Class** - This stores information about the player and score
- **GUI** - Splash screen and player entry screen
- **Database Connection** - Handles PostgreSQL communication
- **UDP Sockets** - Handles broadcasting equipment IDs


