from app.interface import *

# redirect to selected main menu option
def dfs(state):
    while state <= 3 and state >= 0:
        if state == 0:
            state = welcome()
        elif state == 1:
            state = league_manage()
        elif state == 2:
            state = player_manage()
        elif state == 3:
            state = match_manage()
    exit()

if __name__ == '__main__':
    dfs(0)
    