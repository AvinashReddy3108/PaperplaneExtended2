from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.types import ChatBannedRights

from asyncio import sleep
from userbot import CMD_HELP
from userbot.events import register, errors_handler


@register(outgoing=True, pattern=r"^.lock ?(.*)")
@errors_handler
async def locks(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        input_str = event.pattern_match.group(1)
        if not input_str:
            await event.edit("`I can't lock nothing in this chat !!`")
            return
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
        if input_str == "msg":
            msg = True
            what = "messages"
        if input_str.lower() == "media":
            media = True
            what = "media"
        if input_str.lower() == "sticker":
            sticker = True
            what = "stickers"
        if input_str.lower() == "gif":
            gif = True
            what = "GIFs"
        if input_str.lower() == "game":
            gamee = True
            what = "games"
        if input_str.lower() == "inline":
            ainline = True
            what = "inline bots"
        if input_str.lower() == "poll":
            gpoll = True
            what = "polls"
        if input_str.lower() == "invite":
            adduser = True
            what = "invites"
        if input_str.lower() == "pin":
            cpin = True
            what = "pins"
        if input_str.lower() == "info":
            changeinfo = True
            what = "chat info"
        if input_str.lower() == "all":
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
            what = "everything"
        else:
            await event.edit(f"`Invalid lock type:` {input_str}")
            return
        
        lock_rights = ChatBannedRights(
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
            await event.client(
                EditChatDefaultBannedRightsRequest(peer=peer_id,
                                                   banned_rights=lock_rights))
            await event.edit(f"`Locked {what} for this chat !!`")
            await sleep(3)
            await event.delete()
        except BaseException as e:
            await event.edit(f"`Do I have proper rights for that ??`\n**Error:** {str(e)}")
            return


@register(outgoing=True, pattern=r"^.unlock ?(.*)")
@errors_handler
async def rem_locks(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        input_str = event.pattern_match.group(1)
        if not input_str:
            await event.edit("`I can't unlock nothing in this chat !!`")
            return
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
        if input_str.lower() == "msg":
            msg = False
            what = "messages"
        if input_str.lower() == "media":
            media = False
            what = "media"
        if input_str.lower() == "sticker":
            sticker = False
            what = "stickers"
        if input_str.lower() == "gif":
            gif = False
            what = "GIFs"
        if input_str.lower() == "game":
            gamee = False
            what = "games"
        if input_str.lower() == "inline":
            ainline = False
            what = "inline bots"
        if input_str.lower() == "poll":
            gpoll = False
            what = "polls"
        if input_str.lower() == "invite":
            adduser = False
            what = "invites"
        if input_str.lower() == "pin":
            cpin = False
            what = "pins"
        if input_str.lower() == "info":
            changeinfo = False
            what = "chat info"
        if input_str.lower() == "all":
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
            what = "everything"
        else:
            await event.edit(f"`Invalid unlock type:` {input_str}")
            return
        
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
            await event.client(
                EditChatDefaultBannedRightsRequest(peer=peer_id,
                                                   banned_rights=unlock_rights)
            )
            await event.edit(f"`Unlocked {what} for this chat !!`")
            await sleep(3)
            await event.delete()
        except BaseException as e:
            await event.edit(f"`Do I have proper rights for that ??`\n**Error:** {str(e)}")
            return


CMD_HELP.update({
    "locks":
    ".lock <all (or) type(s)> or .unlock <all (or) type(s)>\
\nUsage: Allows you to lock/unlock some common message types in the chat.\
[NOTE: Requires proper admin rights in the chat !!]\
\n\nAvailable message types to lock/unlock are: \
\n`all, msg, media, sticker, gif, game, inline, poll, invite, pin, info`"
})
