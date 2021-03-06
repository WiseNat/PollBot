import json
import os
import traceback
from datetime import datetime

import discord
from discord.ext import commands


async def generate_user_error_embed(ctx, message):
    embed = discord.Embed(title="**Error**", description=message, colour=0xA50B06)
    await ctx.send(embed=embed)


async def send_traceback(ctx, exception):
    tb_lines = traceback.format_exception(type(exception), exception, exception.__traceback__, 4)
    await ctx.send("An unexpected error occurred and will be logged ~\n```Python\n{}```".format(''.join(tb_lines)))

    if not os.path.exists("logs"):
        os.mkdir("logs")

    today = datetime.utcnow()
    path_pattern = "logs/{}-{}-{} %s.json".format(today.day, today.month, today.year)
    i = 1

    # First do an exponential search
    while os.path.exists(path_pattern % i):
        i = i * 2

    # Result lies somewhere in the interval (i/2..i]
    # We call this interval (a..b] and narrow it down until a + 1 = b
    a, b = (i // 2, i)
    while a + 1 < b:
        c = (a + b) // 2  # interval midpoint
        a, b = (c, b) if os.path.exists(path_pattern % c) else (a, c)

    path = path_pattern % b

    # Saving log to JSON file - easier to manage later on if needed
    with open(path, "w") as logfile:
        command = ctx.invoked_with
        args = [str(arg) for arg in ctx.args]
        kwargs = [str(kwargs) for kwargs in ctx.kwargs]

        data = {"User ID": ctx.author.id,
                "Command": command,
                "Args": args,
                "Kwargs": kwargs,
                "Traceback": tb_lines}

        json.dump(data, logfile, indent=4)


class Bot(commands.Bot):
    def __init__(self):
        prefix = "*"
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix=prefix,
                         description="Pole",
                         intents=intents,
                         activity=discord.Activity(type=discord.ActivityType.listening, name=prefix + "help"))
        self.cog_list = []

    async def on_ready(self):
        print(f"Name:\t{super().user.name}\nID:\t{super().user.id}")

    async def on_command_error(self, ctx, exception):
        # This prevents any commands with local handlers being handled here
        if hasattr(ctx.command, "on_error"):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here
        if ctx.cog and ctx.cog._get_overridden_method(ctx.cog.cog_command_error) is not None:
            return

        # This prevents errors being thrown if the command doesn't exist
        if isinstance(exception, commands.errors.CommandNotFound):
            return

        # All stations good, send the error log!
        await send_traceback(ctx, exception)

    def run(self):
        super().run(open("token.secret", "r").read())

    def load_cog(self, cog):
        super().load_extension(cog)
        self.cog_list.append(cog)


if __name__ == "__main__":
    bot = Bot()
    bot.remove_command("help")
    bot.load_cog("cogs.commands")
    bot.run()
