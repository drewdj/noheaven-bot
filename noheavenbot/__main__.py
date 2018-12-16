import os
from asyncio import sleep

from discord import Game
from discord.ext.commands import Bot, when_mentioned_or


from noheavenbot.logger.bot_log import Log, Disconnecting
from noheavenbot.utils.cogs_manager import load_cogs
from noheavenbot.utils.login import Tokens

try:
    debug_mode = os.environ['DEBUG_MODE']
except KeyError:
    debug_mode = False


class CustomBot(Bot):
    def __init__(self, prefix, status_name):

        super().__init__(command_prefix=when_mentioned_or(prefix), activity=Game(name=status_name))

    @property
    def bot_log(self):
        return Log()

    @property
    def bot_disconnect(self):
        self.http.close()
        return Disconnecting


_bot = CustomBot('!' if not debug_mode else '%', '!help -- para ayuda')
_bot.remove_command('help')

if __name__ == '__main__':

    load_cogs(_bot)

    _bot.run(Tokens.sur if debug_mode else Tokens.nhbot)

    if _bot.is_closed():
        try:
            _bot.bot_disconnect.disconnect()
        except Exception as e:
            print(e)
        finally:
            exit()
