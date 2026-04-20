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
    - if it asks for a password when running install.sh, enter student as the password.
# PLEASE NOTE: Pygames is no longer supported, to run the game and hear the music, you may have to run an older version of python. The game will still run using the install script but music might not play

### Running with traffic genarator DO THIS FIRST
1. Navigate to project directory
   - cd ~/Software-Engineering-project-spring-26
2. Pull changes from GitHub
   - git pull origin main
3. run this line: python3 python_trafficgenarator_v2.py
4. You will then be prompted to enter hardware ID for the two players on each team
5. Red teams should have an odd hardware ID like 1 and 3
6. Green teams should have an even hardware ID like 2 and 4
7. Please remember these because you will need to input them again in the main program after you enter each team member and press F3 to start the game
8. Open a new terminal and follow the next section's instructions to run the main program file for the game 

### Running the program after first time setup
1. Navigate to project directory
   - cd ~/Software-Engineering-project-spring-26
2. Pull changes from GitHub
   - git pull origin main
3. Compile and run
   - python3 LaserTagMain.py

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


