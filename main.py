import hikari
import lightbulb
from lightbulb.ext import tasks
from private import token

bot = lightbulb.BotApp(
    intents=hikari.Intents.ALL,
    token=token.get_token()  # Here, you may want to replace the function by your own token
)
tasks.load(bot)

rollus_id = 1109510213570150503
listus = []


@bot.listen()
async def on_started(event: hikari.StartedEvent) -> None:
    bot_guild = await event.app.rest.fetch_my_guilds()
    guild_names = [guild.name for guild in bot_guild]
    print(guild_names)


# Says something when pinged
@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:
    # Do not respond to non-human interaction
    if not event.is_human:
        return

    me = bot.get_me()

    if me.id in event.message.user_mentions_ids:
        await event.message.respond("Pong!")


# Removes a user from the list https://hikari-lightbulb.readthedocs.io/en/latest/guides/error-handling.html
@bot.command
@lightbulb.option('user', 'User to remove from the list', hikari.User, required=True)
@lightbulb.command('remove', 'Removes the tagged user from the Basilus Listus.')
@lightbulb.implements(lightbulb.SlashCommand)
async def remove_from_list(ctx: lightbulb.Context) -> None:
    print(type(ctx.options.user))
    await ctx.respond('Done')


# Display every user that is on the guild
@bot.command
@lightbulb.command('list', 'Lists all users of this guild')
@lightbulb.implements(lightbulb.SlashCommand)
async def list_all_users(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()  # Get the current guild
    members = guild.get_members().values()  # Fetch all members

    member_names = [member.display_name for member in members]
    await ctx.respond(f"Members in this guild: {', '.join(member_names)}")


# Display every user that has the special role
@bot.command
@lightbulb.command('special-list', 'Lists all users that have the special role.')
@lightbulb.implements(lightbulb.SlashCommand)
async def list_special(ctx: lightbulb.Context) -> None:
    listus.clear()                                          # Clearing the listus
    guild = ctx.get_guild()                                 # Get the current guild
    members = guild.get_members().values()                  # Fetch all members

    for member in members:
        for role in await member.fetch_roles():
            if role.id == rollus_id:
                listus.append(member.display_name)
                break

    await ctx.respond(f"{', '.join(listus)}")


# Print a message every 10 seconds
# https://www.linuxtricks.fr/wiki/cron-et-crontab-le-planificateur-de-taches#copy-code-9
sunday_trigger = tasks.CronTrigger("00 00 * * sun *")


@tasks.task(sunday_trigger, auto_start=True)
def update_list_on_sundays() -> None:
    print("do something each sunday")


bot.run()
