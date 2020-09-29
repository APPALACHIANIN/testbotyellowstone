import discord
from discord.ext import commands 
import os
import datetime



PREFIX = '$'

client = commands.Bot( command_prefix = PREFIX )
client.remove_command( 'help' )

@client.event

async def on_ready():
	print( 'Бот подключился к серверу' )

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
	emb = discord.Embed( title = 'Блокировка участника', colour = discord.Color.red() )
	await ctx.channel.purge( limit = 1 )

	await member.ban( reason = reason )

	emb.set_author( name = member.name, icon_url = member.avatar_url )
	emb.add_field( name = 'Бан' , value = 'Пользователь заблокирован : {}'.format( member.mention ) )
	emb.set_footer( text = 'Был забанен администратором {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )

	await ctx.send( embed = emb )

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
	emb = discord.Embed( title = 'Навигация по командам сервера', colour = discord.Color.orange() )

	emb.add_field( name = '{}clear'.format( PREFIX ), value = 'Очистка чата на n-количество сообщений' )
	emb.add_field( name = '{}kick'.format( PREFIX ), value = 'Дисквалификация участника с сервера' )
	emb.add_field( name = '{}ban'.format( PREFIX ), value = 'Ограничение участнику доступа к серверу' )
	emb.add_field( name = '{}unban'.format( PREFIX ), value = 'Возобновление участнику доступа к серверу' )
	emb.add_field( name = '{}time'.format( PREFIX ), value = 'Время по Иркутску' )

	await ctx.send( embed = emb )

# Time

async def time( ctx ):
	emb = discord.Embed( title = 'Ваше время', description = 'Здесь вы сможете узнать время по городу' , colour = discord.Color.green(), url = 'https://www.timeserver.ru/cities/kz/taldykorgan' )

	emb.set_author( name = client.user.name, icon_url = client.user.avatar_url )
	emb.set_footer( text = 'Иди своей дорогой, сталкер' , icon_url = ctx.author.avatar_url )
	emb.set_image( url = 'http://pics.wikireality.ru/upload/e/ed/Villi-vonka-nastalo-vremya.jpeg' )
	emb.set_thumbnail( url = 'https://soundtimes.ru/images/simfjniya/610.jpg' )

	now_date = datetime.datetime.now()

	emb.add_field( name = 'Время', value = 'То самое время : {}'.format( now_date ) )

	await ctx.send( embed = emb )

# Mute
@client.command()
@commands.has_permissions( administrator = True )

async def mute( ctx, member: discord.Member ):
	await ctx.channel.purge( limit = 1 )

	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'MUTE' )

	await member.add_roles( mute_role )
	await ctx.send( f'У { member.mention }, ограничение чата за нарушение прав!' )

# Get token
token = os.environ.get('BOT_TOKEN')

client.run(str(token))




