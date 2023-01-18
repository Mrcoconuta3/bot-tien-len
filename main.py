import discord, os 
from discord.ext import commands
from PIL import Image, ImageDraw

intent = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or('!'),intents= intent, help_command=None)

@client.event 
async def on_ready():
  print('Im in finally!, logged in as {0.user.name}'.format(client))

@client.event
async def on_message(message):
  await client.process_commands(message)

@client.event
async def setup_hook():
  for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
      await client.load_extension(f"cogs.{filename[:-3]}")
      print(f"Load Cog: {filename[:-3]}")   

@client.command()
async def avatar(ctx:commands.Context):
  name = f'image/avatar{ctx.author.id}.png'
  await ctx.author.display_avatar.save(name)
  background : Image.Image= Image.open(os.path.join('modules/', 'board.png')).convert("RGB")
  bg = background.copy()

  avatar = Image.open(name).resize((100,100))
  mask_im = mask(avatar, name)
  
  bg.paste(avatar, (400 , 640), mask_im)
  bg.save(name)
  embed = discord.Embed(title='Here is your embed')
  file = discord.File(name, filename=name)
  embed.set_image(url=f"attachment://{name}")
  await ctx.reply(embed =embed, file = file)

def mask(image,name):
  print(image.size)
  mask_im = Image.new("L", image.size, 0)
  draw = ImageDraw.Draw(mask_im)
  draw.pieslice([(0,0), (image.size)], 0, 360, fill = 255, outline = "white")
  mask_im.save('mask.png', quality=95)
  return mask_im

client.run("Your bot token here")
