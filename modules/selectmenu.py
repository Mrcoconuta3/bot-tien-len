from discord.ui import Select, View ,Button
import discord
from discord import SelectOption
from typing import List
from modules.image import out_table1, out_table_last
from modules.card import Card, reverse_translation
from modules.player import Player
from modules.deck import Deck

#List['3 Bích'] Đơn - Dài 1 
#List['3 Bích', '3 Chuồng']  Đôi - Dài 2
#List['3 Bích', '3 Chuồng','3 Cơ'] Ba lá - Dài 3
#List['4 Bích', '4 Chuồng','4 Cơ' ,'4 Rô'] Tứ Quý - Dài 4
#List['3 Bích', '4 Bích', 5 Bích'] Sảnh - Dài >=3
#List['3 Bích', '3 Chuồng','4 Cơ', '4 Rô','5 Bích',5 Chuồng'] Ba Đôi Thông  - Dài 6
#List['3 Bích', '3 Chuồng','4 Cơ', '4 Rô','5 Bích',5 Chuồng',6 Bích','6 Rô'] Bốn Đôi Thông - Dài 8

class selectmenu(Select):
    def __init__(self, ctx, game, placeholder = None, min_values: int = 1, max_values: int = 1, 
        dictonary = [], prev_turn = None, prev_move= [] , first_turn=False, player_list ={}, button =None, num_passes = 0, just_end =False, *, options: List[SelectOption] = ...):

        super().__init__(placeholder=placeholder, min_values=min_values, max_values=max_values, options= options)
        self.ctx = ctx #Dùng để gửi tin nhắn
        self.game = game #Bàn chơi number
        self.style = prev_turn #Dạng bài trước đó (Style) 'tứ quý',...
        self.prev_move = prev_move #List bài đã được đi trước đó
        self.dict:dict = dictonary #Danh sách người chơi và bài
        self.player_list = player_list#Danh sách người chơi, Dùng để chuyển lượt (cần thiết)
        self.first_turn = first_turn    #Nếu = True thì Đi phải có 3 bích . Sửa thành khi đi phải đi bài nhỏ nhất
        self.num_passes = num_passes
        self.button = button
        self.just_end = just_end

    async def callback(self, interaction):
        #card_move = self.values #-> Danh sách các lá bài được đi
        temp_turn = interaction.user.id 
        if 'Bỏ lượt' in self.values:
            if self.first_turn:
                await interaction.response.send_message("Người chơi đầu tiên không được bỏ lượt", ephemeral= True, delete_after= 10)
            else:
                print(f'{interaction.user.id} Bỏ lượt')
                self.num_passes += 1
                print(f'Số người đã bỏ lượt: {self.num_passes} >? {len(self.player_list) - 1}')
                self.player_turn = Player().change_player1(self.player_list, interaction.user.id)
                self.player_list[interaction.user.id] = False
                if self.just_end: #Patch 2 
                    print('Some one just finished their hand: *** True ***')
                    if self.num_passes >= len(self.player_list) or self.player_turn == temp_turn:
                        print(f'>>>>>>> Bỏ lượt! tất cả lượt đi được reset')
                        self.player_list = {x: True for x in self.player_list}
                        self.prev_move = []
                        self.num_passes = 0
                        self.style = None
                        self.just_end = False
                else:      
                    if self.num_passes >= len(self.player_list) - 1 or self.player_turn == temp_turn:
                        print(f'>>>>>>> Bỏ lượt! tất cả lượt đi được reset')
                        self.player_list = {x: True for x in self.player_list}
                        self.prev_move = []
                        self.num_passes = 0
                        self.style = None
                            
                #self.justend biến thành false khi đã đủ người chơi bỏ lượt hoặc có người chơi đi thay vì bỏ lượt- >self.just_end = False
                
                await interaction.response.edit_message(content=f"Bạn chọn bỏ lượt", view=None)
                await disable_button(self.button)
                await self.ctx.send(f"<@{interaction.user.id}> chọn bỏ lượt")
                await out_table1(self.ctx, 
                                self.dict, 
                                game = self.game, 
                                player_turn= self.player_turn, 
                                prev_turn=self.style, 
                                prev_move=self.prev_move, 
                                first_turn= False,
                                player_list= self.player_list,
                                num_passes = self.num_passes,
                                just_end = self.just_end,
                                content= f'Lượt của <@{self.player_turn}>',
                                title=f"Bàn: {self.game}",
                                description=f"Số người chơi: {len(self.dict)}")

        else:
            
            card_move = Deck().sorting2(self.values)
            print(card_move) #List['3 Bích', '4 Bích', 5 Bích'] Sảnh
            #Lấy dạng bài được đi -> so sánh với dạng bài trước : trả về giá trị dạng bài hiện tại nếu nước đi hợp lệ . Còn không thì trả về giá trị Invalid
            valid = True
            if self.first_turn: #Kiểm tra người dùng có 3 bích không
                user_hand = [str(card) for card in self.dict[interaction.user.id]] #List[Object(Card)] ->List(str(card))
                if '3 Spades' in user_hand and '3 Spades' not in card_move:
                    valid = False
            if valid:    #Nước đi vẫn hợp lệ
                hands = [] #Đổi thành dạng List[Card()] - > prev_move nếu nước đi thành công
                for new_card in card_move:
                    new_card = new_card.split()
                    value = new_card[0]
                    if new_card[0] in reverse_translation:
                       value = reverse_translation[new_card[0]]
                    hands.append(Card(new_card[1], (value)))

                style = Player(hands).is_valid_move(self.prev_move, self.style)
                print(style)
                try:
                    if self.prev_move != []:
                        if style not in next_turn[self.style]:
                            valid = False
                except:
                    valid = True

                if style == 'Invalid' :
                    valid = False

                else:
                    if valid:
                    # Remove card_move from user hand
                        cards = [str(card) for card in self.dict[interaction.user.id]]            
                        new_hand = Player(cards).remove_cards(card_move)
                        self.just_end = False
                        #Gắn bài mới cho ng chơi
                        self.dict[interaction.user.id] = new_hand
                        self.player_turn = Player().change_player1(self.player_list, interaction.user.id)
                        try:
                            if self.num_passes >= len(self.player_list) - 1 or self.player_turn == temp_turn:
                                print(f'>>>>>>> Tất cả lượt đi được reset')
                                self.player_list = {x: True for x in self.player_list}
                                self.prev_move = []
                                self.num_passes = 0
                                self.style = None
                        except:pass
                        
                        try:#Người chơi đã về đích
                            if len(new_hand) == 0:
                                #del self.player_list[interaction.user.id]
                                print(f'<@{interaction.user.id}> về đích!')
                                print(f'Player list: {self.player_list}')
                                await self.ctx.send(f'<@{interaction.user.id}> về đích!')
                                del self.player_list[interaction.user.id]
                                self.just_end = True
                        except:pass

                        if len(self.player_list) == 1: #Game over 
                            await interaction.response.edit_message(content= f"Trò chơi kết thúc!", view=None)
                            await disable_button(self.button)
                            await out_table_last(self.ctx, self.dict, game = self.game, prev_move=hands,
                                    content= f'Trò chơi kết thúc',
                                    title=f"Bàn: {self.game}",)

                        else:#Chuyển lượt 
                            # Xuất ra ảnh rồi gửi lên channel  
                            #prev_move= hands 
                            await interaction.response.edit_message(content =f"Nước đi của bạn: {style.capitalize()}\n", view=None)
                            await disable_button(self.button)
                            await out_table1(self.ctx, self.dict, game = self.game, player_turn= self.player_turn, prev_turn=style, prev_move=hands, first_turn= False, 
                                    player_list=self.player_list,
                                    num_passes= self.num_passes,
                                    just_end= self.just_end,
                                    content= f'Lượt của <@{self.player_turn}>',
                                    title=f"Bàn: {self.game}",
                                    description=f"Số người chơi: {len(self.dict)}")
                            
            if not valid: #Nước đi không hợp lệ
                #Print this and do nothing
                print('Your move is invalid')
                try:
                    await interaction.response.send_message("Nước đi không hợp lệ", ephemeral= True)
                except: await interaction.followup.send("Nước đi không hợp lệ", ephemeral= True)
                
class MenuView(discord.ui.View):
    def __init__(self, ctx , select):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.add_item(select)
    
    async def on_timeout(self):
        pass
    

def getselector(ctx , game, dict, cards_hand, first_turn , player_list, num_passes, just_end, prev_turn, prev_move=[] ,button =None):
    #Các nước đi bắt buộc tiếp theo)
    min_values = 1 ; max_values = len(cards_hand)
    #min_values, max_values = min_max(prev_turn, cards_hand, prev_move)
    option = [discord.SelectOption(label='Bỏ lượt', emoji='❌')]
    option += [discord.SelectOption(label=str(card), emoji=card.emoji) for card in cards_hand]       
    select = selectmenu(ctx = ctx, game = game, placeholder='Chọn nước đi', 
        min_values=min_values, max_values=max_values, dictonary =dict, first_turn= first_turn, player_list=player_list,
        num_passes =num_passes, just_end=just_end ,prev_turn=prev_turn, prev_move= prev_move, button = button,options= option)
    
    view = MenuView(ctx, select)
    return view
    
#Valid_turn là nước đi bắt buộc đi
#Sảnh thì min = max = len(previous_move) 
#   TRƯỜNG HỢP                 NƯỚC ĐI TIẾP THEO
#     Đôi heo                tứ quý hoặc bốn đôi thông
#     1 heo           heo lớn hơn/3 đôi thông/tứ quý/4 đôi thông
#  3 đôi thông            3 đôi thông, tứ quý, 4 đôi thông
#  4 đôi thông                   4 đôi thông
#   Tứ quý                     tứ quý, 4 đôi thông

def min_max(prev_turn, cards_hand, prev_move): #Ko dùng nữa
    if prev_turn is None or prev_move == [] : min_values = 1; max_values = len(cards_hand)
    elif prev_turn == 'sảnh' : min_values = max_values = len(prev_move)
    else: value = valid_turn[prev_turn] ; min_values = value[0]; max_values = value[1] 
    return min_values, max_values

valid_turn = { #[min, max] #Ko dùng nữa
    'đơn' : [1, 1],
    'đôi' : [2, 2],
    '1heo': [1, 8],
    '2heo' : [2, 8],
    '3heo' : [3, 3],
    'ba lá' : [3, 3],
    'tứ quý' : [4, 8],
    'ba đôi thông' : [4, 8],
    'bốn đôi thông' : [8, 8],
    }

next_turn = {
    'đơn': ('đơn','1heo'),
    'đôi': ('đôi','2heo'),
    '1heo' : ('1heo','ba đôi thông','tứ quý','bốn đôi thông'),
    '2heo' : ('2heo','tứ quý','bốn đôi thông'),
    '3heo' : ('3heo'),
    'ba lá' : ('ba lá','3heo'),
    'sảnh' : ('sảnh'),
    'ba đôi thông' : ('ba đôi thông','tứ quý','bốn đôi thông'),
    'tứ quý' : ('tứ quý','bốn đôi thông'),
    'bốn đôi thông' : ('bốn đôi thông')
    }

async def disable_button(button) -> None: #Bỏ nút khi có người chơi đi bài
    #try:
        button.stop()
        await button.message.edit(view = None)
    #except:
    #    pass
