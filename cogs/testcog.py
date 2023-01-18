import math
from discord.ext import commands 
from modules.deck import *
from modules.button import *
from discord.ext.commands import BucketType
#from modules.helpers import check_is_allowed, mongoose

x_game = 0


class Test(commands.Cog):
    def __init__(self, client):
        self.client =client

    @commands.cooldown(1, 30, BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=['tl'],brief="Play a game of tiến lên",)
    async def tienlen(self, ctx: commands.Context):
        """ Game tiến lên"""
        #if not check_is_allowed(ctx.author.id):
        #    return await ctx.reply('Bạn đang ở trong bàn chơi khác')
        #mongoose(ctx.author.id)

        avatar_name = f'avatar/{ctx.author.id}.png'
        await ctx.author.display_avatar.save(avatar_name)

        global x_game
        x_game += 1
        Player_dict = {ctx.author.id: []} 
    
        view = Button(ctx, Player_dict ,self.client , x_game)
        view.message = await ctx.reply('{} đang mở bàn chơi. Ấn nút bên dưới để tham gia'.format(ctx.author.mention), view = view)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Woah! Chậm lại chút",
                description=f"Bạn không thể dùng lệnh này ngay bây giờ, thử lại sau **{math.ceil(error.retry_after)}s**.",
                color=discord.Color.random(),
            )
            await ctx.send(embed=embed)
            return

    #@commands.command(aliases=['p'],brief="Delete for owner")
    #async def purge(self, ctx: commands.Context, user: discord.Member = None):
    #    if user is None:
    #        user = ctx.author
    #   try:
    #        re_mongoose(user.id)
    #        await ctx.reply(f'{user.id} rời mongoose')
    #    except Exception as e:
    #        await ctx.reply(e)
        

async def setup(client: commands.Bot):
    await client.add_cog(Test(client))
