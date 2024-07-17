from pyrogram import idle

from Pbxbot import __version__
from Pbxbot.core import (
    Config,
    GachaBotsSetup,
    TemplateSetup,
    UserSetup,
    db,
    Pbxbot,
)
from Pbxbot.functions.tools import initialize_git
from Pbxbot.functions.utility import BList, Flood, TGraph


async def main():
    await Pbxbot.startup()
    await db.connect()
    await UserSetup()
    await GachaBotsSetup()
    await TemplateSetup()
    await Flood.updateFromDB()
    await BList.updateBlacklists()
    await TGraph.setup()
    await initialize_git(Config.PLUGINS_REPO)
    await Pbxbot.start_message(__version__)
    await idle()


if __name__ == "__main__":
    Pbxbot.run(main())
