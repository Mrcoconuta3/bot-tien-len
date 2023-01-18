import random
from modules.card import *

suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

#compare two cards return lower card
def compare_cards(a, b):
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
    
#Rối đúng không? phương thức này đúng rồi đấy
#return the high card in a card set
def high_card(card_set):                                           
  high_card = Card("Spades", 3)                                    
  for card in card_set:                                                 
    low_card = compare_cards(high_card, card)                      
    high_card = high_card if low_card == card else card                 
  return high_card 

#Compare 2 cards return highest card:
def compare_card_2(a, b):
  a_card_order = card_hierarchy[a.value]
  b_card_order = card_hierarchy[b.value]
  if a_card_order > b_card_order:
    return a
  elif a_card_order == b_card_order:
    a_suit_order = suit_hierarchy[a.suit]
    b_suit_order = suit_hierarchy[b.suit]
    if a_suit_order > b_suit_order:
      return a
    else:
      return b
  else:
    return b

#return True if player has 3 spades else: False ->Bool
def get_first_turn(card_set):
  compare = Card("Spades", 3)
  for card in card_set:
    higher_card = compare_card_2(compare, card)
    if str(higher_card) == str(compare):
      return True
  return False

def get_first_turn2(card_set):
  """Tìm ra quân nhỏ nhất giữa các người chơi"""
  compare = Card("Spades", 3)
  for card in card_set:
    higher_card = compare_card_2(compare, card)
    if str(higher_card) == str(compare):
      return True
  return False

def low_card(card_set):
    #output the users lowest card
    #2 of hearts is the highest card in the game
    low_card = Card("Hearts", 2)
    for card in card_set:
      low_card = compare_cards(low_card, card) 
    return low_card



#instance of a deck of cards
class Deck:
  def __init__(self):
      self.cards = []
      self.build()
      self.shuffle()

  def build(self):
    for suit in suits:
      for value in range(1, 14):
        self.cards.append(Card(suit, value))
    random.shuffle(self.cards)

  def shuffle(self):
    for i in range(len(self.cards) - 1, 0, -1):
      r = random.randint(0, i)
      self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

  def show(self):
    deck = [card.pong() for card in self.cards]
    return deck

  def draw_card(self):
    if self.cards:
      return self.cards.pop()

  def build_hand(self, time=None):
    decking= self.show()
    tuble = []
    if time: time = int(time)
    else:time = 1
    for ha in range(time):
      hand= []
      for c in range(13):
        hand.append(decking.pop())
      newhand = self.sorting(hand)
      outputhand : list = []
      for a in newhand:
        a = a.split()
        outputhand.append(Card(a[1],a[0]))
      tuble.append(outputhand)
    #print(tuble)
    return tuble
    

  def sorting(self, hand):
    def myfunc(e):  
        e= e.split()
        value = card_hierarchy[int(e[0])]
        suit = suit_hierarchy[e[1]]
        output = value + (suit /10)
        return output

    hand.sort(key=myfunc)
    return hand
  
  def sorting2(self, hand):
    def myfunc(e):  
        e= e.split()
        v = e[0] 
        if e[0] in reverse_translation:
          v = reverse_translation[e[0]]
        value = card_hierarchy[int(v)]
        suit = suit_hierarchy[e[1]]
        rank = value + (suit /10)
        return rank

    hand.sort(key=myfunc)
    return hand

#just a test to see if the deck works
if __name__ == "__main__":
  deck = Deck()
  tuble = deck.build_hand(2)
  print()
  for t in tuble:
    print(t)
    bol = get_first_turn(t)
    print(bol)
    if bol == True:
      print(f'This guy has it : {t}')
      break 
    
  #deck.show()

