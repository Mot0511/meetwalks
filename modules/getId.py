def getId(mess):
    if mess.from_user.username:
        return mess.from_user.username
    return mess.from_user.id
