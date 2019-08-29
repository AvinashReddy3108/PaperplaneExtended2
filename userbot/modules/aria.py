# By:- @Zero_cool7870

import aria2p
from telethon import events
import asyncio
import os
from userbot.events import register
from userbot import CMD_HELP

cmd = "aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port 6800  --max-connection-per-server=10 --rpc-max-request-size=1024M --seed-time=0.01 --min-split-size=10M --follow-torrent=mem --split=10 --daemon=true"

aria2_is_running = os.system(cmd)

aria2 = aria2p.API(aria2p.Client(host="http://localhost", port=6800, secret=""))


@register(outgoing=True, pattern="^.magnet(?: |$)(.*)")
async def magnet_download(event):
    if event.fwd_from:
        return
    var = event.text
    var = var[8:]

    magnet_uri = var
    magnet_uri = magnet_uri.replace("`", "")
    print(magnet_uri)

    # Add Magnet URI Into Queue
    try:
        download = aria2.add_magnet(magnet_uri)
        gid = download.gid
        complete = None
        previous_message = None
        while complete != True:
            file = aria2.get_download(gid)
            complete = file.is_complete
            try:
                if not file.error_message:
                    msg = "Downloading Metadata: `" + str(
                        file.name) + "`\nSpeed: " + str(
                            file.download_speed_string()
                        ) + "\nProgress: " + str(file.progress_string(
                        )) + "\nTotal Size: " + str(
                            file.total_length_string()) + "\nStatus: " + str(
                                file.status) + "\nETA:  " + str(
                                    file.eta_string()) + "\n\n"
                    if msg != previous_message:
                        await event.edit(msg)
                        previous_message = msg
                        await asyncio.sleep(10)
                else:
                    msg = file.error_message
                    await event.edit("`" + msg + "`")
                    return
            except Exception as e:
                # print(str(e))
                pass
        await asyncio.sleep(3)
        new_gid = await check_metadata(gid)
        complete = None
        previous_message = None
        while complete != True:
            file = aria2.get_download(new_gid[0])
            complete = file.is_complete
            try:
                if not file.error_message:
                    msg = "Downloading File: `" + str(
                        file.name) + "`\nSpeed: " + str(
                            file.download_speed_string()
                        ) + "\nProgress: " + str(file.progress_string(
                        )) + "\nTotal Size: " + str(
                            file.total_length_string()) + "\nStatus: " + str(
                                file.status) + "\nETA:  " + str(
                                    file.eta_string()) + "\n\n"
                    if previous_message != msg:
                        await event.edit(msg)
                        previous_message = msg
                        await asyncio.sleep(15)
                else:
                    msg = file.error_message
                    await event.edit("`" + msg + "`")
                    return
            except Exception as e:
                # print(str(e))
                pass

    except Exception as e:
        if "EditMessageRequest" in str(e):
            pass
        elif " not found" in str(e):
            await event.edit("Download Cancelled:\n`" + file.name + "`")
            return
        else:
            print(str(e))
            await event.edit("Error:\n`" + str(e) + "`")
            return
    await event.edit("File Downloaded Successfully:\n`" + file.name + "`")


async def check_metadata(gid):
    file = aria2.get_download(gid)
    new_gid = file.followed_by_ids
    print("Changing GID " + gid + " to " + new_gid[0])
    return new_gid


@register(outgoing=True, pattern="^.tor(?: |$)(.*)")
async def torrent_download(event):
    if event.fwd_from:
        return

    var = event.text[5:]

    torrent_file_path = var
    torrent_file_path = torrent_file_path.replace("`", "")
    print(torrent_file_path)

    # Add Torrent Into Queue
    try:
        download = aria2.add_torrent(torrent_file_path,
                                     uris=None,
                                     options=None,
                                     position=None)
    except BaseException:
        await event.edit("`Torrent File Not Found...`")
        return

    gid = download.gid
    complete = None
    previous_message = None
    while complete != True:
        try:
            file = aria2.get_download(gid)
            complete = file.is_complete
            if not file.error_message:
                msg = "Downloading File: `" + str(
                    file.name) + "`\nSpeed: " + str(file.download_speed_string(
                    )) + "\nProgress: " + str(
                        file.progress_string()) + "\nTotal Size: " + str(
                            file.total_length_string()) + "\nStatus: " + str(
                                file.status) + "\nETA:  " + str(
                                    file.eta_string()) + "\n\n"
                if msg != previous_message:
                    await event.edit(msg)
                    previous_message = msg
                    await asyncio.sleep(15)
            else:
                msg = file.error_message
                await event.edit("`" + msg + "`")
                return
        except Exception as e:
            if "EditMessageRequest" in str(e):
                pass
            elif "not found" in str(e):
                await event.edit("Download Cancelled:\n`" + file.name + "`")
                print("Download Aborted: " + gid)
                return
            else:
                print(str(e))
                await event.edit("Error:\n`" + str(e) + "`")
                return

    await event.edit("File Downloaded Successfully:\n`" + download.name + "`")


@register(outgoing=True, pattern="^.url(?: |$)(.*)")
async def magnet_download(event):
    if event.fwd_from:
        return
    var = event.text[5:]
    print(var)
    uris = [var]

    # Add URL Into Queue
    try:
        download = aria2.add_uris(uris, options=None, position=None)
    except Exception as e:
        await event.edit("`Error:\n`" + str(e))
        return

    gid = download.gid
    complete = None
    previous_message = None
    while complete != True:
        try:
            file = aria2.get_download(gid)
            complete = file.is_complete
            if not file.error_message:
                msg = "Downloading File: `" + str(
                    file.name) + "`\nSpeed: " + str(file.download_speed_string(
                    )) + "\nProgress: " + str(
                        file.progress_string()) + "\nTotal Size: " + str(
                            file.total_length_string()) + "\nStatus: " + str(
                                file.status) + "\nETA:  " + str(
                                    file.eta_string()) + "\n\n"
                if msg != previous_message:
                    await event.edit(msg)
                    previous_message = msg
                    await asyncio.sleep(10)
            else:
                msg = file.error_message
                await event.edit("`" + msg + "`")
                return

        except Exception as e:
            if "EditMessageRequest" in str(e):
                pass
            elif "not found" in str(e):
                await event.edit("Download Cancelled:\n`" + file.name + "`")
                print("Download Aborted: " + gid)
                return
            else:
                print(str(e))
                await event.edit("Error:\n`" + str(e) + "`")
                return

    await event.edit("File Downloaded Successfully:\n`" + file.name + "`")


@register(outgoing=True, pattern="^.ariaRM$")
async def remove_all(event):
    if event.fwd_from:
        return
    try:
        removed = aria2.remove_all(force=True)
        aria2.purge_all()
    except BaseException:
        pass

    if removed == False:  # If API returns False Try to Remove Through System Call.
        os.system("aria2p remove-all")

    await event.edit("`Removed All Downloads.`")


@register(outgoing=True, pattern="^.ariap$")
async def pause_all(event):
    if event.fwd_from:
        return
    # Pause ALL Currently Running Downloads.
    paused = aria2.pause_all(force=True)

    await event.edit("Output: " + str(paused))


@register(outgoing=True, pattern="^.ariaResume$")
async def resume_all(event):
    if event.fwd_from:
        return

    resumed = aria2.resume_all()

    await event.edit("Output: " + str(resumed))


@register(outgoing=True, pattern="^.show(?: |$)(.*)")
async def show_all(event):
    if event.fwd_from:
        return
    output = "output.txt"
    # Show All Downloads
    downloads = aria2.get_downloads()

    msg = ""

    for download in downloads:
        msg = msg + "File: `" + str(download.name) + "`\nSpeed: " + str(
            download.download_speed_string()) + "\nProgress: " + str(
                download.progress_string()) + "\nTotal Size: " + str(
                    download.total_length_string()) + "\nStatus: " + str(
                        download.status) + "\nETA:  " + str(
                            download.eta_string()) + "\n\n"
    # print(msg)
    if len(msg) <= 4096:
        await event.edit("`Current Downloads: `\n" + msg)
    else:
        await event.edit("`Output is huge. Sending as a file...`")
        with open(output, 'w') as f:
            f.write(msg)
        await asyncio.sleep(2)
        await event.delete()
        await event.client.send_file(
            event.chat_id,
            output,
            force_document=True,
            supports_streaming=False,
            allow_cache=False,
            reply_to=event.message.id,
        )


CMD_HELP.update({
    "Aria":
        ".show\
\nUsage: show Download in Aria.\
\n\n.ariaResume\
\nUsage: Resume All Downloads in Aria.\
\n\n.ariaRM\
\nUsage: Remove All Downloads in Aria.\
\n\n.ariap\
\nUsage: Pause All Downloads in Aria.\
\n\n.tor <file_path>\
\nUsage: Torrent file from local.\
\n\n.magnet <magnetLink>\
\nUsage: Download File using Aria from magnet link.\
\n\n.url <Url>\
\n\nUsage: It can download stuff over HTTP(S) and FTP etc."
})
