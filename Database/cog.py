import discord, settings, asyncio
from discord.ext import commands
from Users.models import User
from Utils.checks import is_command_channel
from .models import LevelSystem, UserActivity, PointType
from Database.draw import RankImage
from .checks import has_rank

class Ranks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    async def rules(self, ctx):
        ...

    @rules.command()
    async def accept(self, ctx):
        roles = [ctx.guild.get_role(role_id) for role_id in settings.ROLE_ACCEPT] # makes uuid into object
        member = ctx.author
        await ctx.send(f'{member.mention} accepted the rules. Welcome to Of Feral Tendencies! :wolf:') 
        await member.add_roles(roles[0]); await member.add_roles(roles[1])
        await asyncio.sleep(15); await ctx.message.delete()
    
    @commands.group()
    async def lvl(self, ctx):
        ...
    
    @lvl.command()
    @is_command_channel()
    async def give(self, ctx, member: discord.Member, points: int):
        await self.bot.ranks.add_points(ctx.message.id, member.id, PointType.MANUAL, points)

    @lvl.command()
    @has_rank(5)
    async def member(self, ctx):
        member = ctx.author
        await ctx.send('Congratulations for reaching level 5. You are now a Member! :wolf:')
        await member.add_roles(ctx.guild.get_role(settings.ROLE_LEVEL5)); await ctx.message.delete()

    @lvl.command()
    @has_rank(10)
    async def expert(self, ctx):
        member = ctx.author
        await ctx.send('Congratulations for reaching level 10. You are now an Expert! :wolf:')
        await member.add_roles(ctx.guild.get_role(settings.ROLE_LEVEL10)); await ctx.message.delete()

    @lvl.command()
    @has_rank(19)
    async def veteran(self, ctx):
        member = ctx.author
        await ctx.send('Congratulations for reaching level 20. You are now a Veteran! :wolf:')
        await member.add_roles(ctx.guild.get_role(settings.ROLE_LEVEL20)); await ctx.message.delete()

    @lvl.command()
    @has_rank(29)
    async def champion(self, ctx):
        member = ctx.author
        await ctx.send('Congratulations for reaching level 30. You are now an Expert! :wolf:')
        await member.add_roles(ctx.guild.get_role(settings.ROLE_LEVEL30)); await ctx.message.delete()
    
    @lvl.command()
    async def leaderboard(self, ctx, limit: int = 5):
        if limit > 5:
            limit = 5
        leaderboard_users = User.get_leaderboard(limit)
        embed = discord.Embed(title = ':wolf: Alpha Wolves of Feralis :wolf:')
        output = '```'
        for user in leaderboard_users:
            try:
                discord_member = await ctx.message.guild.fetch_member(user.user_id)
                output += f'{discord_member.display_name:25} {int(user.total_points)} XP\n'
            except discord.errors.NotFound:
                output += f'{user.user_id:25} {int(user.total_points)} XP\n'
        output += '```'
        embed.add_field(name = 'Users', value = output, inline = False)
        await ctx.send(embed = embed)
    
    @lvl.command()
    async def rank(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author
        
        # draws user rank and level
        total_points = UserActivity.get_points(member.id)
        current_rank = LevelSystem.get_rank(total_points)
        current_xp_level = LevelSystem.get_level_xp(current_rank)
        next_level_xp = LevelSystem.get_level_xp(current_rank + 1)

        # calculate required xp to reach current and next
        #next_level_xp_diff = next_level_xp - current_xp_level
        level_progress = total_points - current_xp_level
        current_level_xp = LevelSystem.get_level_xp(current_rank)
        xp_required_for_next_level = next_level_xp - current_xp_level

        count_messages = UserActivity.count_messages(member.id)
        count_reactions = UserActivity.count_reactions(member.id)

        # draws the rank image
        rank_image = RankImage()
        full_image_path = rank_image.draw_basic_information(member.display_name, total_points, current_rank, count_messages, count_reactions)
        print(xp_required_for_next_level, level_progress)
        # rank_image.draw_progress_bar(full_image_path, next_level_xp_diff, level_progress)
        rank_image.draw_progress_bar(full_image_path, xp_required_for_next_level, level_progress)

        # draws the user avatar
        member_avatar_path = settings.IMAGES_AVATAR_TEMP_DIR / f'{member.id}.jpg'
        await member.avatar.save(member_avatar_path)
        rank_image.draw_member_avatar(full_image_path, member_avatar_path)
        rank_card_img = discord.File(full_image_path, 'rank.png')

        embed = discord.Embed(title = 'Progress')
        embed.set_image(url = 'attachment://rank.png')
        await ctx.send(embed = embed, file = rank_card_img)

        rank_image.delete_image(full_image_path)


async def setup(bot):
    await bot.add_cog(Ranks(bot))