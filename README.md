# pong
Interface for managing the Princeton University Ping Pong League. **Dependencies:** virtualenv, mysql, python 2.7.

## Setup and first execution:
1. Adjust `config.py` file based on your preferences and include your personal credentials.
2. Setup virtual environment:
```
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
```   
3. Start mysql and create pong database:
```
    $ sudo service mysql start
    $ mysql -u <username> -p <password>
      > create database pong;
      > exit;
```
4. Define the database tables and run the Pong Interface:
```
    $ python initialize.py
```
    
## Load the pong interface given successful setup:
1. Activate virtual environment:
```
    $ source venv/bin/activate
```
2. Start mysql:
```
    $ sudo service mysql start
```
3. Run the Pong Interface:
```
    $ python run.py
```

## User Guide:
 To create a new league, you will need a csv file with the information of all the players, adhering to the following format: Then create a league by using the pong interface (Menu Path: 1 - 1). Make sure to jot down the League ID of the generated league, as it is required for performing all core league operations. After you have generated your league, generate your first round matches (Menu Path: 1 - 3).

You have already created your new league. You have generated the first round matches and collected the results. Now what? This section is guiding you through the recommended steps for processing the results, generating the updated leaderboard, and producing the next round matches:  
1. Manually produce the csv file with the results from the matches of the previous round. Each row should contain a single match in the following format:
2. Add new players that just joined the league (Menu Path: 2 - 1).  
**Required input:** League ID and each new player's email and full name. No output.
3. Process the results and generate the updated leaderboard (Menu Path: 1 - 3).  
**Required input:** League ID and the csv file produced in step 1. **Output:** A csv file containing the updated leaderboard.
4. Remove players that requested to be removed from the league (Menu Path: 2 - 2).  
**Required input:** Each player's email. No output. 
5. Generate the next round matches(Menu Path: 1 - 3).  
**Required input:** League ID. **Output:** A csv file containing the next round matches.
6. Update the website (https://pu-ping-pong-league.github.io/), pick a featured match, and notify the players via email.

This flow is relevant for every round.


    
    
    
