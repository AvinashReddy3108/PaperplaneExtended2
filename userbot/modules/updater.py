# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
"""
This module updates the userbot based on Upstream revision
"""

from os import remove, execle, path, makedirs, getenv
from shutil import rmtree
import asyncio
import sys

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import CMD_HELP, bot, HEROKU_APIKEY, HEROKU_APPNAME, UPSTREAM_REPO_URL
from userbot.events import register

requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), 'requirements.txt')


async def gen_chlog(repo, diff):
    ch_log = ''
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += f'•[{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n'
    return ch_log


async def initial_git(repo):
    update = repo.create_remote('master', UPSTREAM_REPO_URL)
    update.pull('master')


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            ' '.join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


@register(outgoing=True, pattern="^.update(?: |$)(.*)")
async def upstream(ups):
    "For .update command, check if the bot is up to date, update if specified"
    await ups.edit("`Checking for updates, please wait....`")
    conf = ups.pattern_match.group(1)
    off_repo = UPSTREAM_REPO_URL

    try:
        txt = "`Oops.. Updater cannot continue due to "
        txt += "some problems occured`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await ups.edit(f'{txt}\n`directory {error} is not found`')
        return
    except GitCommandError as error:
        await ups.edit(f'{txt}\n`Early failure! {error}`')
        return
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote('upstream', off_repo)
        origin.fetch()
        repo.create_head('master', origin.refs.master)
        repo.heads.master.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != 'master':
        await ups.edit(
            f'**[UPDATER]:**` Looks like you are using your own custom branch ({ac_br}). '
            'in that case, Updater is unable to identify '
            'which branch is to be merged. '
            'please checkout to any official branch`')
        return

    try:
        repo.create_remote('upstream', off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote('upstream')
    ups_rem.fetch(ac_br)
    
    changelog = await gen_chlog(repo, f'HEAD..upstream/{ac_br}')

    if not changelog:
        await ups.edit(
            f'\n`Your BOT is`  **up-to-date**  `with`  **{ac_br}**\n')
        return

    if conf != "now":
        changelog_str = f'**New UPDATE available for [{ac_br}]:\n\nCHANGELOG:**\n`{changelog}`'
        if len(changelog_str) > 4096:
            await ups.edit("`Changelog is too big, view the file to see it.`")
            file = open("output.txt", "w+")
            file.write(changelog_str)
            file.close()
            await ups.client.send_file(
                ups.chat_id,
                "output.txt",
                reply_to=ups.id,
            )
            remove("output.txt")
        else:
            await ups.edit(changelog_str)
        await ups.respond('`do \".update now\" to update`')
        return

    await ups.edit('`New update found, updating...`')
    ups_rem.fetch(ac_br)
    repo.git.reset("--hard")
    if getenv("DYNO", False):
        import heroku3
        if not HEROKU_APIKEY:
            await ups.edit('`[HEROKU MEMEZ] Please set up the HEROKU_APIKEY variable to be able to update userbot.`')
            return
        heroku = heroku3.from_key(HEROKU_APIKEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not HEROKU_APPNAME:
            await ups.edit('`[HEROKU MEMEZ] Please set up the HEROKU_APPNAME variable to be able to update userbot.`')
            return
        for app in heroku_applications:
            if app.name == str(HEROKU_APPNAME):
                heroku_app = app
                break
            if heroku_app is None:
                await ups.edit(f'{txt}\n`Invalid Heroku credentials for updating userbot dyno.`')
                return
            else:
                for build in heroku_app.builds():
                    if build.status == "pending":
                        await ups.edit('`A userbot dyno build is in progress, please wait for it to finish.`')
                        return
            url = f"https://api:{HEROKU_APIKEY}@git.heroku.com/{heroku_app.name}.git"
            if "heroku" in repo.remotes:
                repo.remotes['heroku'].set_url(url)
            else:
                repo.create_remote('heroku', url)
            heroku_app.enable_feature('runtime-dyno-metadata')
            await ups.edit('`[HEROKU MEMEZ] Userbot dyno build in progress, please wait.`')
            remote = repo.remotes['heroku']
            try:
                remote.push(refspec=f'{repo.active_branch.name}:master')
            except GitCommandError as error:
                await ups.edit(f'{txt}\n`Here is the error log:\n{error}`')
                return
            await ups.edit('`Successfully Updated!\n'
                               'Bot is restarting... Wait for a second!`')
    else:
        reqs_upgrade = await update_requirements()
        await ups.edit('`Successfully Updated!\n'
                       'Bot is restarting... Wait for a second!`')
        await ups.client.disconnect()
        # Spin a new instance of bot
        args = [sys.executable, "-m", "userbot"]
        execle(sys.executable, *args, os.environ)
        return


CMD_HELP.update({
    'update':
    ".update\
\nUsage: Checks if the main userbot repository has any updates and shows a changelog if so.\
\n\n.update now\
\nUsage: Updates your userbot, if there are any updates in the main userbot repository."
})
