import discord
import yaml
from redbot.core.commands import commands
from dislash import *


class BtnRoles(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    def cog_unload(self):
        """
        Teardown the slash client so we don't have multiple clients
        """
        self.bot.slash.teardown()

    @commands.command()
    async def setroles(self, ctx, *, message: str):
        """Give roles using buttons & YAML."""
        if not ctx.message.attachments:
            return await ctx.send("You need to upload a YAML file.", delete_after=20)

        attachment: discord.Attachment = ctx.message.attachments[0]
        if not attachment.filename.lower().endswith((".yaml", ".yml")):
            return await ctx.send("Only YAML is supported.", delete_after=20)

        yaml_file = yaml.safe_load(await attachment.read())
        btns = []
        for label, config in yaml_file.items():
            b = Button(
                label=label,
                emoji=config.get("emoji"),
                custom_id=config.get("role_id"),
                style=config.get("style", 1))
            btns.append(b)

        row = ActionRow(*btns)
        await ctx.send(message, components=[row])

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        role = inter.guild.get_role(int(inter.component.custom_id))
        if not role:
            return await inter.reply(
                f"Something went wrong when giving you a role!",
                ephemeral=True,
                delete_after=20)

        if role.id in [r.id for r in inter.author.roles]:
            return await inter.reply(
                f"🙃 You've already got the role `{role}`!",
                ephemeral=True,
                delete_after=20)

        await inter.author.add_roles(role)
        await inter.reply(
            f"👉 You've now got the role `{role}`!",
            ephemeral=True,
            delete_after=20)
