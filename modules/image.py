from PIL import Image
import os 
from modules.deck import *
from modules.helpers import make_embed
from modules import button
from typing import List, Tuple
import discord
    
def output1(name , dict) -> None:
    """Generate upside down card with length and stick it to background -> Display.png"""
    create_table_card(dict).save(f'{name}') #LƯU HÌNH ÀNH VỚI TÊN= name để dễ dàng trích xuất và gửi lên kênh
    
def create_table_card(dict:dict) -> Image.Image:#  dict = {102: [], 103 : [card,...]}
    """Tạo hình ảnh bàn chơi với bài và avatar người chơi """
    background : Image.Image= Image.open(os.path.join('modules/', 'board.png'))
    avatars_id = [id for id in dict]

    bg_left_x = background.size[0] - 120
    bg_right_x = 120
    bg_center_x = (background.size[0] - 100) // 2 
    bg_center_y = (background.size[1] - 150) // 2
    bg_top_y = 50
    bg_bottom_y = background.size[1] - 150

    mask_im = Image.open('image/mask.png')
    card_ = []
    for cards in dict.items():
        lencard = len(cards[1])
        card_.append(Image.open(f'image/{lencard}.png').resize((70,105)) if lencard > 0 else 0)
    #print(f'________Create display -> card_image: {card_}')

    background.paste(Image.open(f"avatar/{avatars_id[0]}.png").resize((100,100)) , (bg_center_x - 100, bg_bottom_y), mask_im)
    background.paste(Image.open(f"avatar/{avatars_id[1]}.png").resize((100,100)) , (bg_right_x -100 , bg_center_y), mask_im)

    if card_[0] != 0:
        background.alpha_composite(card_[0], (bg_center_x + 20 , bg_bottom_y))
    if card_[1] != 0:        
        #Left card
        background.alpha_composite(card_[1], (bg_right_x + 20 , bg_center_y))
    
    if len(dict) >= 3:
    #Top card
        background.paste(Image.open(f"avatar/{avatars_id[2]}.png").resize((100,100)) , (bg_center_x - 100 , bg_top_y), mask_im)
        if card_[2] != 0:
            background.alpha_composite(card_[2], (bg_center_x + 20 , bg_top_y))
        
    if len(dict) == 4:
    #Right card
        background.paste(Image.open(f"avatar/{avatars_id[3]}.png").resize((100,100)) , (bg_left_x  , bg_center_y), mask_im)
        if card_[3] != 0:
            background.alpha_composite(card_[3], (bg_left_x - 90, bg_center_y))
        
    return background

@staticmethod
def hand_to_image(hand: List[Card]) -> List[Image.Image]:
    """ Chuyển list bài thành ảnh"""
    #print([card for card in hand])
    return ([
        Image.open(os.path.join('modules/cards/', card.image))   
        for card in hand
    ])

def output(name, namebg, *hands: Tuple[List[Card]]) -> None:
    print(f'{hands} --- hands in output')
    center(namebg , *map(hand_to_image, hands)).save(f'{name}')# MAP giống như nhân phương thức, có bao nhiêu bộ bài thì có bấy nhiêu phương thức (mà thôi bỏ qua đi)

@staticmethod
def center(namebg, *hands: Tuple[Image.Image]) -> Image.Image:
    """Đưa các lá bài đã đi ra giữa bàn cho người dùng dễ xem"""
    background : Image.Image= Image.open(os.path.join(namebg))
    #X pixel cột ngang, Y pixel cột dọc
    try:
        bg_center_x = background.size[0] // 2
        bg_center_y = background.size[1] // 2
        img_dai = hands[0][0].size[0]
        img_cao = hands[0][0].size[1]
        #điểm bắt đầu theo cột dọc : Bài ở giữa trung tâm
        start_y = bg_center_y - (((len(hands)*img_cao) + ((len(hands) - 1) * 15)) // 2)
        for hand in hands:
            #Theo cột ngang (+20 pixel cho mỗi lá bài được đánh ra)
            start_x = bg_center_x - ((img_dai + ((len(hand) - 1) *20)) //2)
            for card in hand:
                background.alpha_composite(card, (start_x, start_y))
                start_x += 20
    except:
        pass
    return background

async def out_table_user(id, hand, **kwargs):
    """Dùng đế cho từng người chơi xem bài (riêng tư)"""
    output(f'game/{id}.png', 'modules/table.png', hand)
    embed = make_embed(**kwargs)
    file = discord.File(
        f"game/{id}.png", filename=f"{id}.png"
    )
    embed.set_image(url=f"attachment://{id}.png")
    return file, embed


async def out_table1(ctx, dictonary, game , player_turn, prev_turn, prev_move, first_turn, player_list, num_passes=0, just_end =False ,content =None, **kwargs) -> discord.Message:
        """Sends a picture of the current table"""
        print(f'-----Prev move in out_table1: {prev_move}')
        view = button.Game_Button(ctx, game, dictonary, player_turn, prev_turn, prev_move, first_turn= first_turn, player_list = player_list, num_passes=num_passes, just_end =just_end)
        display_name = f'game/Display{game}.png'
        output1(display_name, dictonary)
        if not first_turn:
            if prev_move != []:
                display_name = f'game/Display0{game}.png'
            output(display_name, f'game/Display{game}.png', prev_move)

        embed = make_embed(**kwargs)
        file = discord.File(
            f"{display_name}", filename=f"Display{game}.png"
        )
        embed.set_image(url=f"attachment://Display{game}.png")
        view.message: discord.Message = await ctx.send(content = content,file=file, embed=embed, view = view )  

async def out_table_last(ctx, dictonary, game , prev_move, content , **kwargs) -> discord.Message:
    print(f'OUT_TABLE_Last : {prev_move}')
    
    display_name = f'game/Display0{game}.png'
    output1(f'game/Display{game}.png', dictonary)
    output(display_name, f'game/Display{game}.png', prev_move)
    embed = make_embed(**kwargs)
    file = discord.File(
        f"{display_name}", filename=f"Display{game}.png"
    )
    embed.set_image(url=f"attachment://Display{game}.png")
    message: discord.Message = await ctx.send(content = content,file=file, embed=embed)  
    try:
        os.remove(display_name)
        os.remove(f'game/Display{game}.png')
    except: pass
    for userid in dictonary:
        try:
            os.remove(f'game/{userid}.png')
            os.remove(f'avatar/{userid}.png')
        except: continue  
    return message

#def getflipcard():
#    image = Image.open(os.path.join('modules/cards/red_back.png'))
#    return(image.resize((70,105)))

#async def out_table(ctx , num_player, **kwargs) -> discord.Message:
#        """Sends a picture of the current table"""
#        ghost('game/Display.png', dict=['2C','2C','2C','2C'], player=num_player)
#        embed = make_embed(**kwargs)
#        file = discord.File(
#            f"game/Display.png", filename=f"Display.png"
#        )
#        embed.set_image(url=f"attachment://Display.png")
#        msg: discord.Message = await ctx.send(file=file, embed=embed)
#        return msg

#def ghost(name , dict, player):
#    """Generate upside down card and stick it to background"""
#    ghost_deck =  [Card(suit, num, down=True) for num in range(1,2) for suit in suits]
#    flipcard: List[Card] = []
#    for i in range(player):
#        flipcard.append(ghost_deck.pop())
#    avatars_id = [key for key in dict]#List
#    output2(name ,flipcard ,avatars_id)
#    
#def output2(name , hands , avatars_id) -> None:
#    create_table(hands, avatars_id).save(f'{name}')
#
#def create_table(hands, avatars_id) -> Image.Image:# Hands = [13,13,13,13],  [12,0,12,0] .. {102: 10, 103 : 0}
#    background : Image.Image= Image.open(os.path.join('modules/', 'board.png'))
#    card = getflipcard()
#    bg_left_x = background.size[0] - 120
#    bg_right_x = 120
#    bg_center_x = (background.size[0] - card.size[0]) // 2 
#    bg_center_y = (background.size[1] - card.size[1]) // 2
#    bg_top_y = 50
#    bg_bottom_y = background.size[1] - 150
#    
#    mask_im = Image.open('image/mask.png')
#    #Bị đảo ngược chiều như trong gương
#    #Bottom card
#    # #avatar1 = Image.open(f"image/{avatars_id[0]}.png").resize((150,150))
#    background.alpha_composite(card, (bg_center_x + 20 , bg_bottom_y))
#    background.paste(Image.open(f"avatar/{avatars_id[0]}.png").resize((100,100)) , (bg_center_x - 100, bg_bottom_y), mask_im)
#    #Left card
#    background.alpha_composite(card, (bg_right_x + 20 , bg_center_y))
#    background.paste(Image.open(f"avatar/{avatars_id[1]}.png").resize((100,100)) , (bg_right_x -100 , bg_center_y), mask_im)
#    
#    if len(hands) >= 3:
#    #Top card
#        background.alpha_composite(card, (bg_center_x + 20 , bg_top_y))
#        background.paste(Image.open(f"avatar/{avatars_id[2]}.png").resize((100,100)) , (bg_center_x - 100 , bg_top_y), mask_im)
#    if len(hands) == 4:
#    #Right card
#        background.alpha_composite(card, (bg_left_x - 90, bg_center_y))
#        background.paste(Image.open(f"avatar/{avatars_id[3]}.png").resize((100,100)) , (bg_left_x  , bg_center_y), mask_im)
#    return background

#if __name__ == "__main__":
#    image = ghost('Test1', dict=['2C','2C','2C','2C'], player=4)
    #image.show()
#        async def out_table_main(whose_turn, card_list ,**kwargs) -> discord.Message:
#            """Sends a picture of the current table"""
#            self.output('Tienlen', hands= card_list)
#            embed = make_embed(**kwargs)
#            file = discord.File(
#                f"Tienlen.png", filename=f"Tienlen.png"
#            )
#            embed.set_image(url=f"attachment://Tienlen.png")
#            msg: discord.Message = await ctx.send(content= f'Lượt của {whose_turn}', file=file, embed=embed)
#            return msg
#
#        Player_dict = {f"{ctx.author.id}": []} 
#        view = Button(ctx, Player_dict)
#        view.message = await ctx.reply('{} đang mở bàn chơi. Ấn nút bên dưới để tham gia'.format(ctx.author.mention), view = view)
    
        #    deck = [Card(suit, num) for num in range(2,15) for suit in Card.suits]
        #    random.shuffle(deck) 
        #    #dict = {'id' : ["card"], 'id2': ["card2"]}
        #    for user in dicto.key():

            #for i in num_player:
            #    name = f'player {i}'
            #    name : List[Card] = []
            #    for card in range(13):
            #        name.append(deck.pop())
            #    print('---------{} : {}'.format(i ,name))

            #ms = await out_table(ctx, len(self.dict),
            #        title="Tiến lên",
            #        description=f"Số người chơi: {self.dict}" 
            #    ) 
#
            #msg = await out_table_main(
            #        whose_turn= "id",
            #        card_list= [],
            #        title="Tiến lên",
            #        description=f"Số người chơi: {num_player}" 
            #    )
        #output('Table', )

    #Tom_hand: List[Card] = []
    #Jerry_hand: List[Card] = []
    #Dog_hand: List[Card] = []
    #Mouse_hand: List[Card] = []
    #for i in range(13):
    #    Tom_hand.append(deck.pop())
    #    Jerry_hand.append(deck.pop())
    #    Dog_hand.append(deck.pop())
    #    Mouse_hand.append(deck.pop())

    #print('---------Player Tom : {}'.format(Tom_hand))
    #print('---------Player Jerry : {}'.format(Jerry_hand))

    #def extract_to_image() -> Image: 
    #    output('Table',Tom_hand, Jerry_hand, Dog_hand, Mouse_hand)
#
    #extract_to_image()
