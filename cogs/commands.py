import discord
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def post_polls(ctx, description, footer, colour=0x9b59b6):
        for d, f in zip(description, footer):
            main_embed = discord.Embed(title="Poll", description=d, colour=colour)
            main_embed.set_footer(text=f)
            message = await ctx.send(embed=main_embed)
            await message.add_reaction("<:tick:671116183751360523>")
            await message.add_reaction("<:question:671119072024461342>")
            await message.add_reaction("<:cross:671116183780720670>")

    @commands.command(aliases=["h"])
    async def help(self, ctx):
        async with ctx.typing():
            colour = 0x3DE1FF
            creator = self.bot.get_user(188341441603305472)
            file = discord.File("example.gif", filename="example.gif")

            embed = discord.Embed(title="**Help**", colour=colour)
            embed.set_image(url="attachment://example.gif")
            embed.set_footer(text=str(creator) + " - contact for further information", icon_url=creator.avatar_url)

            embed.add_field(name="**Commands**",
                            value="`*poll <query>` - creates poll(s) from a given query\n"
                                  "`*autopoll` - creates polls from the user application Google Sheets\n\u200b",
                            inline=False)
            embed.add_field(name="**Query Info**",
                            value="`&` - denotes the end of a polls description so that you can define a footer\n"
                                  "`|` - denotes the end of a poll so that you can create another\n\u200b",
                            inline=False)
            embed.add_field(name="**Poll Command Examples**",
                            value="Try giving these all a go:\n"
                                  "```*poll A Desc & B Foot\n"
                                  "*poll Create new world & World | Upgrade server\n"
                                  "*poll Poll | Hello World & Programming | Fsh & i```\n\u200b",
                            inline=False)

        await ctx.send(embed=embed, file=file)

    @commands.command(aliases=["p"])
    async def poll(self, ctx, *args):
        await ctx.message.delete()
        async with ctx.typing():
            # Merge entire command into one string
            message = " ".join(args)

            # *poll Text & Footer | Text & Footer | Text & Footer...
            poll_list = message.split(" | ")
            description = []
            footer = []
            for poll in poll_list:
                buffer = poll.split(" & ")
                description.append(buffer[0])
                if len(buffer) == 2:
                    footer.append(buffer[1])
                else:
                    footer.append("")

            await self.post_polls(ctx, description, footer)

    @commands.command(aliases=["ap"])
    async def autopoll(self, ctx):
        await ctx.message.delete()
        description = []
        footer = []
        await self.post_polls(ctx, description, footer)


def setup(bot):
    bot.add_cog(Commands(bot))
