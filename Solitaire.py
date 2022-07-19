import random as random
import pandas as pd

class Card:
    '''Card docstring'''
    def __init__(self, suit = None, num = None, facedown = False):
        self.suit, self.num, self.facedown = suit, num, facedown
        self.colour = 'black' if suit in ['C','S'] else 'red'
    
    def __str__(self):
        if self.facedown:
            return '[---]'
        else:
            pad = '[ ' if self.num < 10 else '['
            return pad + str(self.num) + self.suit + ']'
    
    def __repr__(self):
        return str(self)
    
    def flip(self):
        self.facedown = not(self.facedown)

class Pile:
    '''Pile docstring'''
    
    def __init__(self, cards = None, type = None):
        if cards is None:
            self.cards = []
        else:
            self.cards = cards
        self.type = type
    
    def __str__(self):
        return 'Pile(' + str(len(self)) + ')-Top:'+ str(self.top_card())

    def  __len__(self):
        return len(self.cards)
    
    def __repr__(self):
        return str(self)
        
    def __getitem__(self, i):
        return self.cards[i]
    
    def print(self):
        for _ in self.cards:
            print(_)
    
    def shuffle(self):
        random.shuffle(self.cards)
      
    def top_card(self):
        if len(self) > 0:
            return self.cards[-1]
        else:
            return None
        
    def append(self, item):
        self.cards.append(item)
    
    def remove(self, item):
        self.cards.remove(item)
    
    def pop(self):
        return self.cards.pop()
    
    def to_str_list(self):
        return [str(card) for card in self.cards]
    
class Deck(Pile):
    '''Deck docstring'''
    
    suits = ['H', 'S', 'C', 'D']
    nums = list(range(1,14))
    
    def __init__(self, cards = None):
        if cards is None:
            self.reset()
        else:
            self.cards = cards
    
    def __str__(self):
        return "Deck of " + str(len(self)) + " cards."
    
    def __repr__(self):
        return str(self)
    
    def reset(self):
        self.cards = []
        for i in Deck.suits:
            for j in Deck.nums:
                self.append(Card(i, j))
                
class SolitaireBoard:
    '''docstring'''
    
    def __init__(self, deck = Deck()):
        self.deck = deck
        self.reset()
    
    def __str__(self):
        suit_top_cards = [str(x[-1]) if len(x)>0 else None for x in self.suit_piles]
        temp = ''
        for pile in self.main_piles:
            temp += '  ' + str(pile) + '\n'
        return '---Solitaire Board---\nSuit Piles:\n' + str(suit_top_cards) + '\n7 Piles:\n' + temp + '\nFlipped cards:' + str(self.flip_pile)
    
    def reset(self):
        self.main_piles = [Pile(type='main') for _ in range(7)]
        self.suit_piles = [Pile(type='suit') for _ in range(4)]
        for i in range(len(self.main_piles)): # deal main 7 piles
            for j in range(i + 1):
                self.move_top(self.deck, self.main_piles[i])
                if j < i:
                    self.main_piles[i][-1].facedown = True
        
        self.flip_pile = Pile()
        for i in range(3):
            self.move_top(self.deck, self.flip_pile)
            self.flip_pile[-1].facedown = False
    
    def move_top(self, from_pile, to_pile):
        to_pile.append(from_pile.pop())
    
    def to_dataframe(self):
        temp_list = [pile.to_str_list() for pile in self.main_piles]
        temp_list.append(self.flip_pile)
        temp = pd.DataFrame(temp_list).transpose()
        temp.columns = ['', '', '', '', '', '', '', 'From Deck:']
        return temp.fillna(value='')
    
    def show(self):
        suit_top_cards = [str(x[-1]) if len(x)>0 else None for x in self.suit_piles]
        print('---Solitaire Board---\nSuit Piles:\n', str(suit_top_cards)), '\n7 Piles:'
        display(self.to_dataframe())
    
    def is_legal_move(self, from_pile, to_pile):
        from_card, to_card = from_pile[-1], to_pile[-1]
        if to_pile.type == 'suit':
            if (from_card.suit == to_card.suit) and (from_card.num == (to_card.num + 1)):
                return True
            else:
                return False
        elif to_pile.type == 'main':
            if from_card.colour != to_card.colour and (from_card.num == (to_card.num - 1)):
                return True
            else:
                return False
        else:
            raise('unexpected card type')