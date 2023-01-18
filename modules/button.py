import discord
from modules.image import *
from modules.selectmenu import getselector
from modules.player import Player
#from modules.helpers import check_is_allowed, mongoose

def get_first_user(dict:dict):
    for key in dict.items():
        bol = get_first_turn(key[1])
        if bol == True:
            return key[0]
    else:
        for user in dict:
            return user 

class Button(discord.ui.View):
    def __init__(self, ctx, playerdict:dict, client, game_number):
        super().__init__(timeout = 15)
        self.ctx = ctx
        self.client = client 
        self.dict = playerdict
        self.game = game_number

    def add_item_dict(self, item):
        self.dict[item] = []
        get_index = list(self.dict.keys()).index(item)
        return get_index

    async def interaction_check(self, interaction):
        if interaction.user.id in self.dict:     
            await interaction.response.send_message("Bạn đã tham gia rồi", ephemeral=True)
            return False

        elif interaction.user != self.ctx.author:
        #    if not check_is_allowed(interaction.user.id):
        #        await interaction.response.send_message('Bạn đang ở trong bàn chơi khác', ephemeral=True)
        #        return False
        #    mongoose(interaction.user.id)
            while len(self.dict) < 4 :
                return True
            else:
                self.stop()
                await self.on_timeout()
                return False
        
        else:
            return False

    @discord.ui.button(label="Tham gia trò chơi", style=discord.ButtonStyle.green)
    async def ENTERGAME(self, interaction: discord.Interaction, button: discord.ui.Button):
        index = self.add_item_dict(interaction.user.id)
        await interaction.user.display_avatar.save(f'avatar/{interaction.user.id}.png')
        await interaction.response.send_message("Bạn vừa tham gia với tư cách người chơi số {}".format(index+1), ephemeral= True)
        if len(self.dict) == 4:
            self.stop()
            await self.on_timeout()
    
    async def on_timeout(self):
        try:
            await self.message.delete()
        except:
            pass
        if len(self.dict) < 2:
            #re_mongoose(self.ctx.author.id)
            await self.ctx.send("Số lượng người chơi ko đủ. Terminating the game")
            return False
        else:#Run the game
            #dict = {'id' : ["card"], 'id2': ["card2"]}
            #chia bài cho ng chơi -> Dict hoàn chỉnh
            Cards = Deck().build_hand(len(self.dict))# _> Card list of the hand
            for user in self.dict.keys():
                index = list(self.dict).index(user)
                try:
                    self.dict[user] = Cards[index]
                except:pass            
            first_player = get_first_user(self.dict)
            # Gửi tin nhắn bàn chơi với nút game button
            await out_table1(self.ctx, self.dict, game = self.game, player_turn= first_player, prev_turn=None, prev_move=[], first_turn = True, player_list= {x: True for x in self.dict}, content= f'Lượt của <@{first_player}>',
                        title=f"Bàn: {self.game}",
                        description=f"Số người chơi: {len(self.dict)}")
  
class Game_Button(discord.ui.View):
    def __init__(self, ctx, game, playerdict:dict, player_turn, prev_turn,prev_move = [], player_list ={}, num_passes= 0, just_end =False ,first_turn:bool = ...):
        super().__init__(timeout = 30)
        self.ctx = ctx
        self.game = game
        self.dict = playerdict
        self.turn = player_turn
        self.prev_turn = prev_turn
        self.prev = prev_move
        self.first = first_turn
        self.num_passes = num_passes
        self.running = False
        self.player_list = player_list
        self.just_end = just_end

    async def interaction_check(self, interaction):
        if interaction.user.id not in self.dict:
            await interaction.response.send_message("Bạn không phải người tham gia", ephemeral=True)
            return False
        else:
            return True

    @discord.ui.button(label="Xem Bài", style=discord.ButtonStyle.primary)
    async def Viewhand(self, interaction: discord.Interaction, button: discord.ui.Button):
        hand = self.dict[interaction.user.id]
        file, embed = await out_table_user(interaction.user.id, hand= hand)
        await interaction.response.send_message(file= file, embed= embed,ephemeral= True,delete_after=30)

    @discord.ui.button(label="Đi bài", style=discord.ButtonStyle.green)
    async def Go(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.turn:
            return await interaction.response.send_message("Đây ko phải lượt của bạn", ephemeral=True)
        if self.running == True:
            return await interaction.response.send_message('Bạn đang có select menu đang đợi',ephemeral=True, delete_after=10)
        else:
            self.running = True
            cards = self.dict[interaction.user.id]
            view = getselector(self.ctx , self.game, self.dict, cards_hand=cards, 
                first_turn=self.first, player_list=self.player_list, num_passes=self.num_passes, just_end=self.just_end, prev_turn = self.prev_turn, prev_move= self.prev , button = self)
            view.message = await interaction.response.send_message(view=view, ephemeral=True ,delete_after=30)
            return 

    #@discord.ui.button(label="Bỏ bài", style=discord.ButtonStyle.red)
    #async def Quit(self, interaction: discord.Interaction, button: discord.ui.Button):
    #    view = xacnhan(self.dict)
    #    view.message = await interaction.response.send_message('Bạn có chắc muốn bỏ bài. Lưu ý: **Không thể hoàn tác**', view  = view, ephemeral= True)

    async def on_timeout(self) -> None:
        try:
            for child in self:
                child.disable = True
            await self.message.edit(view=self)
        except: pass
        #if self.running == False:
            #Người dùng hết thời gian để đi
        #if self.prev != []:
        self.num_passes += 1
        temp_turn = self.turn

        self.turn = Player().change_player1(self.player_list, self.turn)
        self.player_list[temp_turn] = False
        if self.just_end: #Patch 2 
            print('Some one just finished their hand: *** True ***')
            if self.num_passes >= len(self.player_list):
                print(f'>>>>>>> Bỏ lượt! tất cả lượt đi được reset')
                self.player_list = {x: True for x in self.player_list}
                self.prev = []
                self.num_passes = 0
                self.prev_turn = None
                self.just_end = False

        else:  
            if self.num_passes >= len(self.player_list) - 1:
                print(f'>>>>>>> Bỏ lượt! tất cả lượt đi được reset')
                self.player_list = {x: True for x in self.player_list}
                self.prev = []
                self.num_passes = 0
                self.prev_turn = None
        
        return await out_table1(self.ctx, dictonary= self.dict, game=self.game, player_turn=self.turn, prev_move= self.prev, prev_turn=self.prev_turn, first_turn= False, player_list=self.player_list, num_passes= self.num_passes,
                    just_end= self.just_end,
                    content= f"Lượt của <@{self.turn}>",
                    title=f"Bàn: {self.game}",
                    description=f"Số người chơi: {len(self.dict)}")
        
    
class xacnhan(discord.ui.View):
    def __init__(self, dict):
        super().__init__(timeout=10)
        self.dict = dict

    @discord.ui.button(label="Tiếp tục", style=discord.ButtonStyle.red)
    async def End(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.dict.pop(interaction.user.id)
        await interaction.response.send_message(f'{interaction.user.mention} đã rời khỏi trò chơi')
        await interaction.followup.delete_message(interaction.message.id)
        self.stop()
        return self.dict


    async def on_timeout(self):
        try:
            await self.message.edit('Huỷ bỏ do thời gian đợi quá lâu', view =None)
        except:
            pass
