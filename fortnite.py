import fortnitepy
from fortnitepy.errors import *
import json
import aiohttp
import time

with open('config.json') as f:
    data = json.load(f)[0]

client = fortnitepy.Client(
    email=data['email'],
    password=data['password'],
    net_cl=data['netcl'],
    status=data['status'],
    platform=data['platform']
)

BEN_BOT_BASE = 'http://benbotfn.tk:8080/api/cosmetics/search/multiple'

typeSpecified = ""

print('fortnitepy-bot made by xMistt. credit to Terbau for creating the library.'.format(client))

@client.event
async def event_ready():
    print('Client ready as {0.user.display_name}'.format(client))

@client.event
async def event_party_invite(invitation):
    try:
        await invitation.accept()
        print('[CLIENT] Accepted party invite.')
    except fortnitepy.errors.PartyError:
        print("[ERROR] Couldn't accept invitation, incompatible net_cl.")

@client.event
async def event_friend_request(request):
    if data['friendaccept'] == "true":
        await request.accept()
    else:
        await request.decline()

@client.event
async def event_party_member_join(member):
    await client.user.party.me.set_outfit(asset=data['cid'])
    await client.user.party.me.set_backpack(asset=data['bid'])
    await client.user.party.me.set_banner(icon=data['banner'], color=data['banner_colour'], season_level=data['level'])
    time.sleep(2)
    await client.user.party.me.set_emote(asset=data['eid'])
    await client.user.party.me.set_battlepass_info(has_purchased=True, level=data['bp_tier'], self_boost_xp=data['self_xp_boost'], friend_boost_xp=data['friend_xp_boost'])

async def fetch_cosmetic_id(display_name):
    idint = 0
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(BEN_BOT_BASE, params={'displayName': display_name}) as r:
                data = await r.json()
                type = data[idint]["type"]
                if type == typeSpecified:
                            id = data[idint]["id"]
                            return id
                else:
                    idint += 1

@client.event
async def event_friend_message(message):
    args = message.content.split()
    split = args[1:]
    joinedArguments = " ".join(split)
    print('Received message from {0.author.display_name} | Content: "{0.content}"'.format(message))

    if "!skin" in args[0]:
        global typeSpecified
        typeSpecified = "Outfit"
        id = await fetch_cosmetic_id(' '.join(split))
        await client.user.party.me.set_outfit(
            asset=id
        )

        await message.reply('Skin set to ' + id)
        
    if "!backpack" in args[0]:
        typeSpecified = "Back Bling"
        id = await fetch_cosmetic_id(' '.join(split))
        await client.user.party.me.set_backpack(
            asset=id
        )

        await message.reply('Backpack set to ' + id)

    if "!emote" in args[0]:
        global typeSpecified
        typeSpecified = "Emote"
        id = await fetch_cosmetic_id(' '.join(split))
        await client.user.party.me.set_emote(
            asset=id
        )

        await message.reply('Emote set to ' + id)

    if "!pickaxe" in args[0]:
        typeSpecified = "Harvesting Tool"
        id = await fetch_cosmetic_id(' '.join(split))
        await client.user.party.me.set_pickaxe(
            asset=id
        )

        await message.reply('Pickaxe set to ' + id)

    if "!purpleskull" in args[0]:
        global typeSpecified
        variants = client.user.party.me.create_variants(
           clothing_color=1
        )

        await client.user.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Purple Skull Trooper!')

    if "!banner" in args[0]:
        await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=args[3])

    if "CID_" in args[0]:
        await client.user.party.me.set_outfit(
            asset=args[0]
        )

        await message.reply('Skin set to ' + args[0])

    if "!variants" in args[0]:
        args3 = int(args[3])
        variants = client.user.party.me.create_variants(**{args[2]: args3})

        await client.user.party.me.set_outfit(
            asset=args[1],
            variants=variants
        )

        await message.reply('Skin set to checkered Renegade Raider!')

    if "!checkeredrenegade" in args[0]:

        variants = client.user.party.me.create_variants(
           material=2
        )

        await client.user.party.me.set_outfit(
            asset='CID_028_Athena_Commando_F',
            variants=variants
        )

        await message.reply('Skin set to ' + args[0] + '!')

    if "EID_" in args[0]:
        await client.user.party.me.set_emote(asset="StopEmote")
        await client.user.party.me.set_emote(
            asset=args[0]
        )
        await message.reply('Emote set to ' + args[0] + '!')
        
    if "!stop" in args[0]:
        await client.user.party.me.set_emote(
            asset="StopEmote"
        )
        await message.reply('Stopped emoting.')

    if "BID_" in args[0]:
        await client.user.party.me.set_backpack(
            asset=args[0]
        )

        await message.reply('Backbling set to ' + message.content + '!')

    if "!help" in args[0]:
        await message.reply('For a list of commands, goto; https://github.com/xMistt/fortnitepy-bot')
    if "PICKAXE_ID_" in args[0]:
        await client.user.party.me.set_pickaxe(
                asset=args[0]
        )

        await message.reply('Pickaxe set to ' + args[0] + '!')

    if "!pettest" in args[0]:
        await client.user.party.me.set_backpack(
                asset='PetCarrier_001_Dog'
        )

    if "!legacypickaxe" in args[0]:
        await client.user.party.me.set_pickaxe(
                asset=args[1]
        )

        await message.reply('Pickaxe set to ' + args[1] + '!')

    if "!ready" in args[0]:
        await client.user.party.me.set_ready(True)
        await message.reply('Ready!')

    if "!unready" in args[0]:
        await client.user.party.me.set_ready(False)
        await message.reply('Unready!')

    if "!bp" in args[0]:
        await client.user.party.me.set_battlepass_info(has_purchased=True, level=args[1], self_boost_xp=args[2], friend_boost_xp=args[3])

    if "!point" in args[0]:
        await client.user.party.me.set_pickaxe(asset=args[1])
        await client.user.party.me.set_emote(asset='EID_IceKing')

        await message.reply('Pickaxe set to ' + args[1] + ' & Point It Out played.')

    if "!searchpoint" in args[0]:
        id = await fetch_cosmetic_id(' '.join(split))
        await client.user.party.me.set_pickaxe(asset=id)
        await client.user.party.me.set_emote(asset='EID_IceKing')

        await message.reply('Pickaxe set to ' + args[1] + ' & Point It Out played.')

    if "!update" in args[0]:
        with open('config.json', 'r') as f:
            data = json.load(f)
            emailjson = data[0]['email']
            passwordjson = data[0]['password']
            netcljson = data[0]['netcl']
            cid = data[0]['cid']
            bid = data[0]['bid']
            eid = data[0]['eid']
            banner = data[0]['banner']
            banner_colour = data[0]['banner_colour']
            level = data[0]['level']
            bp_tier = data[0]['bp_tier']
            self_xp_boost = data[0]['self_xp_boost']
            friend_xp_boost = data[0]['friend_xp_boost']
            friendaccept = data[0]['friendaccept']
        await message.reply('Updated config.json!')

    if "!echo" in args[0]:
        await client.user.party.send(joinedArguments)

@client.event
async def event_party_message(message):
    # these aren't needed anymore as you can whisper bots on console but ¯\_(ツ)_/¯
    print('Received message from {0.author.display_name} | Content: "{0.content}"'.format(message))

client.run()
