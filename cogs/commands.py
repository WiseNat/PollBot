from __future__ import print_function

import discord
from discord.ext import commands

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from bot import generate_user_error_embed, send_traceback


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def post_polls(ctx, description, footer, colour=0x9b59b6):
        async with ctx.typing():
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
                                  "`*autopoll <spreadsheet id> <cell range> <footer: optional>` - creates polls from "
                                  "the Staff Application Google Sheets\n\u200b",
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
    async def autopoll(self, ctx, spid, rnge, footer=""):
        await ctx.message.delete()
        async with ctx.typing():
            # If modifying these scopes, delete the file token.pickle.
            SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

            # The ID and range of a sample spreadsheet.
            SPREADSHEET_ID = spid
            RANGE_NAME = rnge  # E.g. "Sheet1!A6:A"

            creds = None
            # The file token.pickle stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists("token.pickle"):
                with open("token.pickle", "rb") as token:
                    creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        "credentials.json", SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open("token.pickle", "wb") as token:
                    pickle.dump(creds, token)

            service = build("sheets", "v4", credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                        range=RANGE_NAME).execute()
            descriptions = [i[-1] for i in result.get("values", []) if i != []]
            footers = [footer for _ in range(len(descriptions))]
            await self.post_polls(ctx, descriptions, footers)

    @autopoll.error
    async def autopoll_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            if str(error.param) == "spid":
                message = "```Missing SpreadSheet ID```\n\n"
            else:
                message = "```Missing Cell Range```\n\n"
            await generate_user_error_embed(ctx, message)
            return

        await send_traceback(ctx, error)


def setup(bot):
    bot.add_cog(Commands(bot))
