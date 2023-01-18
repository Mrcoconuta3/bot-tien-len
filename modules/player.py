from typing import List
from modules.deck import *

#So sánh giữa các lá bài đơn -> trả về lá bài nhỏ hơn
def compare_card_single(a, b):
  a_card_order = card_hierarchy[a.value]
  b_card_order = card_hierarchy[b.value]
  if a_card_order > b_card_order:
    return b
  elif a_card_order == b_card_order:
    a_suit_order = suit_hierarchy[a.suit]
    b_suit_order = suit_hierarchy[b.suit]
    if a_suit_order > b_suit_order:
      return b
    else:
      return a
  else:
    return a


def sảnh(card_values): #Kiểm tra danh sách bài có phải là sảnh không
    if sorted(card_values) == list(range(min(card_values), max(card_values)+1)):
        return 'sảnh'
    return 'Invalid'

#So sánh cho số lượng bài >= 2
def compare_value(cards , prev_cards):
    if prev_cards== []:
      return True
    highest_card = cards[len(cards) - 1] #array bắt đầu từ 0 nên phải trừ 1
    rank = card_hierarchy[highest_card.value] + (suit_hierarchy[highest_card.suit] /10)
    hprev_card = prev_cards[len(prev_cards) - 1]
    rank2 = card_hierarchy[hprev_card.value] + (suit_hierarchy[hprev_card.suit] /10)
    if rank > rank2 or len(prev_cards) == 0:
        return True
    return False

#So sánh sảnh trả về Boolean --> Lấy lá bài cao nhất của mỗi bên rồi so sánh giống như compare_card_single
def compare_run(cards , prev_cards):
    if prev_cards== []:
      return True
    if len(cards) != len(prev_cards):
      return False
    highest_card = cards[len(cards) - 1]
    rank = card_hierarchy[highest_card.value] + (suit_hierarchy[highest_card.suit] /10)
    hprev_card = prev_cards[len(prev_cards) - 1]
    rank2 = card_hierarchy[hprev_card.value] + (suit_hierarchy[hprev_card.suit] /10)
    if rank > rank2 or len(prev_cards) == 0:
        return True
    return False

class Player:
    def __init__(self, hand:List=None):
        self.hand = hand

    def remove_cards(self, cards): #Gỡ các lá bài ra khỏi tụ của người chơi
        for card in cards:
          self.hand.remove(card)
        #Gán newhand cho user
        newhand = []
        for new_card in self.hand:
            new_card = new_card.split()
            value = new_card[0]
            if new_card[0] in reverse_translation:
               value = reverse_translation[new_card[0]]
            newhand.append(Card(new_card[1], (value)))
        return newhand

    #Kiểm tra nước đi có hợp lệ -> move_style
    def is_valid_move(self, prev_move, prev_style):
      card_values = [card.value for card in self.hand]
      try: #Fix potential bug (may be ... Who know)
        if 1 in card_values:# A giá trị 1 đối thành 14 
          for x in range(len(card_values) + 1):
             try:
                one_index = card_values.index(1)
                card_values[one_index] = 14
             except:
                pass
      except:pass
      print('SELF.hand:{} \nSELF.prev_move{}'.format(self.hand, prev_move))
      #print(f'SORTED CARD VALUES: {sorted(card_values)}')
      move = 'Invalid'
      if len(self.hand) > 2: #Sảnh
          moves = sảnh(card_values)
          if moves == 'sảnh':
            if prev_move == [] or compare_run(self.hand, prev_move):
              if 2 not in card_values: #Sảnh ko được có heo
                move = 'sảnh'

      if len(self.hand) == 1: 
          if prev_move == [] or compare_card_single(self.hand[0], prev_move[0]) == prev_move[0]:
            if 2 in card_values:
              move = '1heo'
            else:
              move = 'đơn'

      elif len(self.hand) == 2:
        if sorted(card_values) == list((min(card_values), min(card_values))):
          if prev_move == [] or compare_value(self.hand, prev_move):
            if 2 in card_values:
              move = '2heo'
            else:
              move = 'đôi'

      elif len(self.hand) == 3:
        if sorted(card_values) == list(self.hand[0].value for i in range(3)):
          if prev_move == [] or compare_value(self.hand, prev_move):
            if 2 in card_values:
              move = '3heo'
            else:
              move = 'ba lá'   

      elif len(self.hand) == 4:
        if sorted(card_values) == list(self.hand[0].value for i in range(4)):
            if prev_move == [] or compare_value(self.hand, prev_move):
              move= 'tứ quý' 
            elif prev_style in ['1heo','2heo','ba đôi thông']: #Nước đi trước đó phải là nước đi có thể bị chặt
              move = 'tứ quý'

              
      elif len(self.hand) == 6: #3 đôi thông
        if sorted(card_values) == [min(card_values),min(card_values), min(card_values)+1,min(card_values)+1, max(card_values), max(card_values)]:
            if prev_move == [] or compare_value(self.hand, prev_move):
              if 2 not in card_values:
                move = 'ba đôi thông'
            elif prev_style in ['1heo','2heo']:
              move = 'ba đôi thông'

      elif len(self.hand) == 8: #4 đôi thông
        if sorted(card_values) == [min(card_values),min(card_values), min(card_values)+1,min(card_values)+1, max(card_values)-1, max(card_values)-1 ,max(card_values), max(card_values)]:
            if prev_move == [] or compare_value(self.hand, prev_move):
              if 2 not in card_values:
                move = 'bốn đôi thông'
            elif prev_style in ['1heo','2heo','ba đôi thông','tứ quý']:
              move = 'bốn đôi thông'     
      return move
          
    #Thay đổi người chơi bản cũ, Ko dùng nữa
    def change_player(self, dicting:dict , player_turn):
      player_list = [user[0] for user in dicting.items() if len(user[1]) > 0] 
      print(player_list)

      index = player_list.index(player_turn)
      if index == len(player_list) - 1:
        player_turn = player_list[0]
      else:
        player_turn = player_list[index+1]
      return player_turn

    def change_player1(self, player_list:dict, player_turn): #ĐỆ QUY 
      """Thay đổi lượt người chơi""" #Thay đổi cách hoạt động playerlist thành dict {123 : True hoặc False,...}
      index = list(player_list.keys()).index(player_turn)
      if index == len(player_list) - 1:
        player_turn = list(player_list)[0]
        print('Trở về người chơi đầu tiên')
      else:
        player_turn = list(player_list)[index+1] 

      if player_list[player_turn] == False:
        print(f'{player_turn} đã bỏ lượt')
        return self.change_player1(player_list, player_turn)

      else:
        print(f'This turn is : {player_turn}')
        return player_turn

if __name__ == "__main__":
    hand = [Card(suit,value) for value in range(3,7) for suit in suits ]
    #print(f'Hand: {hand}')
    player = Player(name=10382, hand = hand)
    print(player.hand)
    play =player.play_single(card= 3, card_stack=[], prev_move=[])  #dùng index number để remove lá bài
    print(play)
    print(player.hand)

