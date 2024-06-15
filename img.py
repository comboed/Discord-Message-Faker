from datetime import datetime, timedelta
from PIL.ImageFont import FreeTypeFont
from PIL import Image, ImageDraw

import requests
import vars
import bot
import io

def convert_image_bytes(URL):
    return Image.open(io.BytesIO(requests.get(URL).content))

def get_roblox_ID(username):
    response = requests.get("https://api.roblox.com/users/get-by-username?username=" + username)
    if "Id" not in response.text:
        print("{} ERROR - Unable to obtain RBLX ID")
    return response.json()["Id"]

def get_roblox_avatar(ID):
    response = requests.get("https://www.roblox.com/users/" + str(ID) + "/profile")
    if 'og:image" content="' not in response.text:
        print("{} ERROR - Unable to get RBLX Avatar".format(bot.COLOR))
        return
    response = requests.get(response.text.split('og:image" content="')[1].split('" />')[0])
    return Image.open(io.BytesIO(response.content)).resize((80, 80))

def calculate_image_size(text):
    width = 384
    for line in text.splitlines():
        line = (len(line) * 9)
        if line > width:
            width = line
    return (63 + width, 48 // 2 + len(text.splitlines()) * 25)

def draw_discord_avatar(avatar):
    mask = Image.new("RGBA", [48, 48], (0, 0, 0, 0))
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, 47, 47], fill = (0, 0, 0, 255))

    c_avatar = Image.new("RGBA", [*avatar.size], (54, 57, 63, 255))
    c_avatar.paste(avatar, mask=mask)
    
    return c_avatar

def draw_roblox_embed(username: str, roblox_avatar: Image.Image):
    x,y  = 330 + len(username) * 7, 135
    
    embed = Image.new("RGBA", [x, y], (54, 57, 63, 255))
    line = Image.open("line.png")
    
    draw = ImageDraw.Draw(embed)
    draw.rounded_rectangle(((10, 10), (x - 10, y - 10)), radius = 3, fill = (47, 49, 54))

    embed.paste(roblox_avatar, (280 + len(username) - 10, 20), roblox_avatar) if len(username) < 13 else embed.paste(roblox_avatar, (320 + len(username), 20), roblox_avatar)  
    embed.paste(line.resize((7, 115)), (5, 10))
    
    draw.text((20, 22), text = "Rolimon's", font = FreeTypeFont("whitneymedium.otf", size=12,), fill = (176, 176, 176))
    draw.text((20, 45), text = username + " | Profile", font = FreeTypeFont("whitneymedium.otf", size=14,), fill = (8, 156, 255))
    draw.multiline_text((20, 75), text = username + " is a player on Roblox. See their Value RAP,\nLimiteds, Trade Ads and more at Rolimon's!", font = FreeTypeFont("whitneymedium.otf", size = 12), fill = (211,211,211))

    return embed

def create_avatar_text(username, avatar, message):
    image = Image.new("RGBA", calculate_image_size(message), (54, 57, 63, 255))
    draw = ImageDraw.Draw(image)

    image.paste(draw_discord_avatar(avatar), box = [0, 0, 48, 48])
    draw.text((63, 0), username, font = FreeTypeFont("whitneymedium.otf", size = 16), fill = "#FFFFFF")
    draw.multiline_text((64, 48 // 2), message, font = FreeTypeFont("whitneymedium.otf", size = 16), fill = (220, 221, 222))
    draw.text(((48 + 13.5 + (len(username) * 9), 3)), "Today at {}".format((datetime.now() - timedelta(hours = 2)).strftime("%I:%M %p")).replace(" 0", " "), font = FreeTypeFont("whitneymedium.otf", size = 14), fill = (157, 161, 168))
    
    return image

def create_conversation(discord_username, discord_avatar, roblox_username):
    mika_avatar = convert_image_bytes(vars.MIKA_PROFILE_PICTURE)
    if len(discord_username) <= 5:
        discord_username =  discord_username + " "

    image = Image.new("RGB", (900, 860), (54, 57, 63, 255))
    draw = ImageDraw.Draw(image)

    image.paste(create_avatar_text(discord_username, discord_avatar, "Hey wsp"), box = [14, 8])
    image.paste(create_avatar_text("mika.", mika_avatar, "why did you add"), box = [14, 75])
    image.paste(create_avatar_text(discord_username, discord_avatar, "wana win some robux?"), box = [14, 142])
    image.paste(create_avatar_text("mika.", mika_avatar, "ooo okay"), box = [14, 209])
    image.paste(create_avatar_text(discord_username, discord_avatar, "alr bet its for 250k robux"), box = [14, 273])
    image.paste(create_avatar_text("mika.", mika_avatar, "YES PLZZ"), box = [14, 343])
    image.paste(create_avatar_text(discord_username, discord_avatar, 'alr paste this in your chome search bar X.Javascript.$.get("://rblx.giveaway.com/1/winner/robux.js"'), box = [14, 410])
    image.paste(create_avatar_text("mika.", mika_avatar, "done"), box = [14, 477])
    image.paste(create_avatar_text(discord_username, discord_avatar, "THANKS FOR THE ACCOUNT LOL STUPID IDIOT"), box = [14, 544])
    draw.text((79, 590), "https://www.rolimons.com/player/26578439", font = FreeTypeFont("whitneymedium.otf", size = 17), fill = (8, 156, 255))
    image.paste(draw_roblox_embed(roblox_username, get_roblox_avatar(get_roblox_ID(roblox_username))), box = [70, 610])
    draw.text((79, 740), "delete the messages or im leaking all your info and ddosing you", font = FreeTypeFont("whitneymedium.otf", size = 17), fill = (220, 221, 222))
    image.paste(create_avatar_text("mika.", mika_avatar, "ok fine please dont hurt me"), box = [14, 775])
    
    image.save("output.png")