def sendInvite(user1, user2):
    invites = json.loads(useSql(f"SELECT invites FROM users WHERE username='{user2}'")[0][0])
    invites.append(user1)
    invites = json.dumps(invites)
    useSql(f"UPDATE users SET invites='{invites}' WHERE username='{user2}'")