from static_assets import messages    

def welcome():
    state = raw_input(messages.welcome)
    if state == 1:
        return state
    elif state == 2:
        return state
    elif state == 3:
        return -1
    else:
        return 0

def league_manage():


def player_manage():
    method = raw_input(messages.player_manage)
    if method == 1:

        return 2
    elif method == 2:

        return 2
    elif method == 3:
        return 0
    else:
        return 2

def dfs(state):
    while(state <= 2 and state >= 0):
        if state == 0:
            state = welcome()
        elif state == 1:
            state = league_manage()
        elif state == 2:
            state = player_manage()
    exit()

dfs(0)