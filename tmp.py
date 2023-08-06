async def findTeam(mess):
    while True:
        if getId(mess) in teamIds:
            print(teamIds)
            if getId(mess) in owners:
                owner = owners[getId(mess)]
            else:
                owner = getId(mess)

            if useSql(f"SELECT ready FROM teams WHERE owner='{owner}'")[0][0] == 1:
                print(1)
                await bot.send_message(mess.chat.id, 'Компания сформирована:', reply_markup=kb_leave)
                teamId = teamIds[owner]
                teamIds[getId(mess)] = teamId
                members = json.loads(useSql(f"SELECT members FROM teams WHERE id={teamId}")[0][0])
                members.remove(getId(mess))
                for member in members:
                    await getUser(mess, member, getId(mess))

                global action
                action[getId(mess)] = 'chat'
                await bot.send_message(mess.chat.id, 'Общий чат:', reply_markup=kb_leave)
                while getId(mess) in teamIds:

                    username = getId(mess)
                    oldChat = json.loads(useSql(f"SELECT chat FROM teams WHERE id={teamId}")[0][0])
                    await asyncio.sleep(0.5)
                    newChat = json.loads(useSql(f"SELECT chat FROM teams WHERE id={teamId}")[0][0])
                    if not(oldChat == newChat):
                        for i in oldChat:
                            if i in newChat:
                                newChat.remove(i)

                        for i in newChat:
                            if i[0] == username:
                                newChat.remove(i)

                        for i in newChat:
                            await bot.send_message(mess.chat.id, f'{i[0]}: {i[1]}', reply_markup=kb_leave)

        await asyncio.sleep(2)
