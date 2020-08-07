import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="*", description="It's a poll bot")
bot.remove_command("help")


@bot.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def help(ctx, *args):
    await ctx.message.delete()
    creator = bot.get_user(188341441603305472)

    main_embed = discord.Embed(title="__**Help Commands**__", colour=0x3DE1FF)
    main_embed.add_field(name="**Command Help**",
                         value=("**General Command usage** *poll <Syntax>\n"
                                "**&** char for syntax that allows you to define a footer\n"
                                "**|** char for syntax that allows you to create another poll\n"),
                         inline=False)
    main_embed.add_field(name="\u200b", value="\u200b")
    main_embed.add_field(name="**Example 1**",
                         value="***poll Ban user & Ban Poll** - creates a poll with the description as 'Ban User' and "
                               "the footer of 'Ban Poll''",
                         inline=False)
    main_embed.add_field(name="**Example 2**",
                         value="***poll Create new world & World | Upgrade server** - creates two polls. One with the "
                               "description 'Create new world' and footer 'World'. The other with only the "
                               "description 'Upgrade server'",
                         inline=False)
    main_embed.add_field(name="**Example 3**",
                         value="***poll Hello there | Hello World & Programming Basics | Third Poll? & Yep...** - "
                               "creates three polls. The first has only the description 'Hello there'. The second has "
                               "the description 'Hello World' and footer 'Programming Basics'. The final one has the "
                               "description 'Third Poll?' and footer 'Yep...'.",
                         inline=False)
    main_embed.add_field(name="\u200b", value="\u200b")
    main_embed.set_footer(text=str(creator) + " - contact for further information", icon_url=creator.avatar_url)

    help_message = await ctx.send(embed=main_embed)
    await help_message.add_reaction("<:cross:671116183780720670>")

    def check(reaction, user, *args):
        return str(reaction) == "<:cross:671116183780720670>" and \
               str(reaction.message) == str(help_message) and \
               user != reaction.message.author
    
    reaction, user = await bot.wait_for("reaction_add", check=check)
    await help_message.delete()

    
@bot.command()
async def poll(ctx, *args):
    await ctx.message.delete()

    # Convert to string
    message = ""
    for i in args:
        message += str(i) + " "

    # !poll Text & Footer | Text & Footer | Text & Footer...
    message_sections = message.split(" | ")
    description = []
    footer = []
    for i in message_sections:
        buffer = i.split(" & ")
        description.append(buffer[0])
        if len(buffer) == 2:
            footer.append(buffer[1])
        else:
            footer.append("")

    for i in range(len(description)):
        main_embed = discord.Embed(title="Poll", description=description[i], colour=0x9b59b6)
        main_embed.set_footer(text=footer[i])
        message = await ctx.send(embed=main_embed)
        await message.add_reaction("<:tick:671116183751360523>")
        await message.add_reaction("<:question:671119072024461342>")
        await message.add_reaction("<:cross:671116183780720670>")


bot.run(open("token.secret").read())
