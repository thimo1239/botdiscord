import discord
import asyncio
import copy

# please set token her.
Token = "MzYxNTY4ODA5MzM4OTI5MTYz.Ddy1Nw.2lTHw3WohrNzT_RIxewOzKlmQbQ"
# and set the name here
Robot = "robot#5259"
Scrim = "446014106248413194"
Dig3 = "446014060941672468"
Server = "400385307150778379"
General = "446014012195471380"
MinMembers = 1
client = discord.Client()
Chans = {}


@client.event
async def on_ready():
    print(client.user.name + " is ready!")
    print(client.user.id)
    if not discord.opus.is_loaded():
        discord.opus.load_opus()



@client.event
async def on_message(message):
    if str(message.author) == Robot:
        return
    #if the message starts with ! it will go trough the commands
    elif message.content.startswith("!"):
        Message = message.content.split()
        #!hello says hello back
        if Message[0].lower() == "!hello" and Message[1].lower() == "robot":
            await client.send_message(message.channel, "hello " + message.author)
        #it plays mp3
        if Message[0].lower() == "!clean":
            return
    elif str(message.channel) == "3-digits" and len(message.content) == 3:
        if message.content.upper() in Chans:
            welif = client.get_channel(Chans[message.content.upper()])
            await client.move_member(message.author, welif)
            await client.send_message(message.channel, "Moved " + str(message.author) + " to " + message.content.upper())
        else:
            chan2 = await client.create_channel(client.get_server(Server), message.content.upper(), type=discord.ChannelType.voice)
            await client.send_message(message.channel,"Moved " + str(message.author) + " to " + message.content.upper())
            await client.move_member(message.author, chan2)
            Chans[message.content.upper()] = str(chan2.id)
            await client.move_channel(chan2, 1)


async def my_background_task():
    await client.wait_until_ready()
    while not client.is_closed:
        scrim = client.get_channel(Scrim)
        server = client.get_server(Server)
        if len(scrim.voice_members) >= MinMembers and not client.is_voice_connected(server):
            general = client.get_channel(General)
            dig3 = client.get_channel(Dig3)
            await client.send_message(general, "Scrim starting in 1 minute. @everyone")
            scrim = client.get_channel(Scrim)
            voice = await client.join_voice_channel(scrim)
            player = voice.create_ffmpeg_player("cool.mp3")
            player.start()
            await asyncio.sleep(10)
            player.stop()
            await voice.disconnect()
        if Chans:
            chand = copy.deepcopy(Chans)
            for channame, chankey in chand.items():
                welif = client.get_channel(chankey)
                if len(welif.voice_members) == 0:
                    print(welif.id)
                    await client.delete_channel(welif)
                    await asyncio.sleep(1)
                    del Chans[channame]
        await asyncio.sleep(10)

client.loop.create_task(my_background_task())
client.run(Token)