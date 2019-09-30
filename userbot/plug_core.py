from userbot import bot, LOAD_PLUG
from importlib import import_module
from userbot.events import register

@register(pattern="^.unload (?P<shortname>\w+)$", outgoing=True)
async def unload(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    try:
        remove_plugin(shortname)
        await event.edit(f"Unloaded {shortname} successfully")
    except Exception as e:
        await event.edit("Could not unload {} due to the following error.\n{}".format(shortname, str(e)))

@register(pattern="^.load (?P<shortname>\w+)$", outgoing=True)
async def load(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    try:
        try:
            remove_plugin(shortname)
        except:
            pass
        import_module(f"userbot.modules.{shortname}")
        await event.edit(f"Successfully loaded {shortname}")
    except Exception as e:
        await event.edit(f"Could not load {shortname} because of the following error.\n{str(e)}")

def remove_plugin(shortname):
    for i in LOAD_PLUG[shortname]:
        bot.remove_event_handler(i)
    del LOAD_PLUG[shortname]
