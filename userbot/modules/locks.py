from telethon import events, functions, types
from userbot import bot, CMD_HELP
from userbot.events import errors_handler

@bot.on(events.NewMessage(pattern=r"^.lock ?(.*)", outgoing=True))
@errors_handler
async def locks(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        input_str = event.pattern_match.group(1)
        peer_id = event.chat_id
        msg = None
        media = None
        sticker = None
        gif = None
        gamee = None
        ainline = None
        gpoll = None
        adduser = None
        cpin = None
        changeinfo = None
        if input_str is "msg":
            msg = True
        if input_str is "media":
            media = True
        if input_str is "sticker":
            sticker = True
        if input_str is "gif":
            gif = True
        if input_str is "game":
            gamee = True
        if input_str is "inline":
            ainline = True
        if input_str is "poll":
            gpoll = True
        if input_str is "invite":
            adduser = True
        if input_str is "pin":
            cpin = True
        if input_str is "info":
            changeinfo = True
        if input_str is "all":
            msg = True
            media = True
            sticker = True
            gif = True
            gamee = True
            ainline = True
            gpoll = True
            adduser = True
            cpin = True
            changeinfo = True

        lock_rights = types.ChatBannedRights(
            until_date=None,
            send_messages=msg,
            send_media=media,
            send_stickers=sticker,
            send_gifs=gif,
            send_games=gamee,
            send_inline=ainline,
            send_polls=gpoll,
            invite_users=adduser,
            pin_messages=cpin,
            change_info=changeinfo,
        )
        try:
            await bot(
                functions.messages.EditChatDefaultBannedRightsRequest(peer=peer_id,
                                                                      banned_rights=lock_rights))
            await event.delete()
        except BaseException as e:
            await event.edit(f"`Do I have proper rights for that ??`\n{str(e)}")
            

@bot.on(events.NewMessage(pattern=r"^.unlock ?(.*)", outgoing=True))
@errors_handler
async def rem_locks(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        input_str = event.pattern_match.group(1)
        peer_id = event.chat_id
        msg = None
        media = None
        sticker = None
        gif = None
        gamee = None
        ainline = None
        gpoll = None
        adduser = None
        cpin = None
        changeinfo = None
        if input_str is "msg":
            msg = False
        if input_str is "media":
            media = False
        if input_str is "sticker":
            sticker = False
        if input_str is "gif":
            gif = False
        if input_str is "game":
            gamee = False
        if input_str is "inline":
            ainline = False
        if input_str is "poll":
            gpoll = False
        if input_str is "invite":
            adduser = False
        if input_str is "pin":
            cpin = False
        if input_str is "info":
            changeinfo = False
        if input_str is "all":
            msg = False
            media = False
            sticker = False
            gif = False
            gamee = False
            ainline = False
            gpoll = False
            adduser = False
            cpin = False
            changeinfo = False

        unlock_rights = ChatBannedRights(
            until_date=None,
            send_messages=msg,
            send_media=media,
            send_stickers=sticker,
            send_gifs=gif,
            send_games=gamee,
            send_inline=ainline,
            send_polls=gpoll,
            invite_users=adduser,
            pin_messages=cpin,
            change_info=changeinfo,
        )
        try:
            await bot(
                functions.messages.EditChatDefaultBannedRightsRequest(peer=peer_id,
                                                                      banned_rights=unlock_rights)
            )
            await event.delete()
        except BaseException as e:
            await event.edit(f"`Do I have proper rights for that ??`\n{str(e)}")


CMD_HELP.update({
    "locks":
    ".lock <all (or) type(s)> or .unlock <all (or) type(s)>\
\nUsage: Allows you to lock/unlock some common message types in the chat.\
[NOTE: Requires proper admin rights in the chat !!]\
\n\nAvailable message types to lock/unlock are: \
\n`all, msg, media, sticker, gif, game, inline, poll, invite, pin, info`\
"
})
