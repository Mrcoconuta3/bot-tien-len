import json

#translate ace, jack, queen, king from numbers to human readable format
card_translation = {
  1: "A",
  11: "J",
  12: "Q",
  13: "K",
}

reverse_translation = {
  'A': 1,
  'J': 11,
  'Q': 12,
  'K': 13
}

#translate card to number representing presedence (low to high)
card_hierarchy = {
  3: 0,
  4: 1,
  5: 2,
  6: 3,
  7: 4, 
  8: 5,
  9: 6,
  10: 7,
  11: 8,
  12: 9,
  13: 10,
  1: 11,
  2: 12
}

#translate suit to number representing presedence (low to high)
suit_hierarchy = {
  "Spades": 0, #Bích
  "Clubs": 1, #Chuồng
  "Diamonds": 2, #Rô
  "Hearts": 3 #Cơ
}

with open('emoji.json', encoding='utf-8') as f:
    data = json.load(f)

class Card:
  def __init__(self, suit:str, value:int, down=False):
    self.suit = suit
    self.value = int(value)
    self.down = down
    self.symbol = self.name[0].upper()
    self.emojiname = f'{self.name}{self.suit[0].upper()}'
    self.emoji = data[self.emojiname]

  @property
  def name(self) -> str:
        """The name of the card value."""
        if self.value in card_translation: return card_translation[self.value]
        else: return str(self.value)

  @property
  def image(self):
        return (
            f"{self.symbol if self.name != '10' else '10'}"\
            f"{self.suit[0].upper()}.png" \
            if not self.down else "red_back.png"
        )

  def flip(self):
    self.down = not self.down
    return self
  
  def __str__(self) -> str:
        return f'{self.name.title()} {self.suit.title()}'

  def __repr__(self) -> str:
    return str(self)
    
  #def peek(self) -> str:
  #  if self.value in card_translation: value= card_translation[self.value]
  #  else: value= self.value
  #  return("{} {}".format(value, self.suit))

  def pong(self):
    value = self.value
    return("{} {}".format(value, self.suit))

