from useSql import *
async def buildTeam(team, username):
    new('teams')
    global teams
    team.append(username)
    team = [el for el, _ in groupby(team)]
    teamId = random.randint(0, 10000)
    for i in team:
        teams[i] = teamId
        useSql(f"DELETE FROM inSearch WHERE username='{i}'")
    team = json.dumps(team).replace("'", '"')
    chat = json.dumps([]).replace("'", '"')
    useSql(f"INSERT INTO teams (id, members, chat) VALUES ('{teamId}', '{team}', '{chat}')")
    print('Team was created')
    print(team)

