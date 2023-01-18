from datetime import datetime
from discord import Color, Embed
import pymongo
from bson import ObjectId

def make_embed(title=None, description=None, color=None, author=None,
               image=None, link=None, footer=None) -> Embed:
    """Wrapper for making discord embeds"""
    arg = lambda x: x if x else None
    embed = Embed(
        title=arg(title),
        description=arg(description),
        url=arg(link),
        color=color if color else Color.random()
    )
    if author: embed.set_author(name=author)
    if image: embed.set_image(url=image)
    if footer: embed.set_footer(text=footer)
    else: embed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
    return embed

#def mongoose(id):
#    player_in_tables.update_one({"_id": ObjectId("63c6913e899384accb6beb03")}, {"$set" : {str(id) : 1}})

#def re_mongoose(id):
#    player_in_tables.update_one({"_id": ObjectId("63c6913e899384accb6beb03")}, {"$unset" : {str(id) : 1}})

#def check_is_allowed(id):
#    uses = player_in_tables.find_one({"_id": ObjectId("63c6913e899384accb6beb03")})
#    print(uses)
#    if str(id) in uses:
#        return False
#    return True
