import discord
from discord.ext import commands 
import os


PREFIX = '$'

client = commands.Bot( command_prefix = PREFIX )
client.remove_command( 'help' )

# Words
hello_words = [ 'hello', 'hi', 'привет', 'privet', 'ky', 'ку', 'здарова' ]
answer_words = [ 'узнать информацию о сервере', 'какая информация', 
				'команды', 'команды сервера' ]
goodbye_words = [ 'Пока', 'Удачи', 'Прощай', 'Бывай' ]

@client.event

async def on_ready():
	print( 'BOT connected' )
	
# Words
@client.event

async def on_message( message ):
	msg = message.content.lower()

	if msg in hello_words:
		await message.channel.send( 'Чем могу быть полезен?' )

	if msg in answer_words:
		await message.channel.send( 'Напиши команду .help' )

	if msg in goodbye_words:
		await message.channel.send( 'Пока' )

	
# Clear message
@client.command ( pass_context = True )
@commands.has_permissions( administrator = True )

async def clear( ctx, amount = 100):
	await ctx.channel.purge( limit = amount )

# Kick
@client.command( pass_context = True )
@commands.has_permissions( administrator = True)

async def kick( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )

	await member.kick( reason = reason )
	await ctx.send( f'Пользователь { member.mention } был дисквалифицирован с сервера' )

# Ban
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def ban( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )

	await member.ban( reason = reason )
	await ctx.send( f'Пользователь { member.mention } был забанен за нарушение правил сервера' )

# Unban
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def unban( ctx, *, member ):
	await ctx.channel.purge( limit = 1 )

	banned_users = await ctx.guild.bans()

	for ban_entry in banned_users:
		user = ban_entry.user

		await ctx.guild.unban( user )
		await ctx.send( f'Пользователь { user.mention } был разбанен' )

		return

# Command help
@client.command( pass_context = True )
@commands.has_permissions( administrator = True ) 

async def help( ctx ):
	emb = discord.Embed( title = 'Навигация по командам сервера')

	emb.add_field( name = '{}clear'.format( PREFIX ), value = 'Очистка чата на n-количество сообщений' )
	emb.add_field( name = '{}kick'.format( PREFIX ), value = 'Дисквалификация участника с сервера' )
	emb.add_field( name = '{}ban'.format( PREFIX ), value = 'Ограничение участнику доступа к серверу' )
	emb.add_field( name = '{}unban'.format( PREFIX ), value = 'Возобновление участнику доступа к серверу' )

	await ctx.send( embed = emb )

# Get token
token = os.environ.get('BOT_TOKEN')

client.run(str(token))




