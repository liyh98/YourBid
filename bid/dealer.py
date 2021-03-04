import random


class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    @classmethod
    def fromNumber(cls, number):
        suits = {
            0: "C",
            1: "D",
            2: "H",
            3: "S"
        }
        return cls(suits[number // 13], number % 13 + 2)

    def display(self):
        print(self.suit, self.number)



class Player:
    def __init__(self, vul, pos):
        self.hand = {
            "S": [],
            "H": [],
            "D": [],
            "C": [],
        }
        self.vul = vul
        self.hcp = 0
        self.pos = pos
        self.bal = None

    def toJson(self):
        return {
            'hand': self.hand,
            'vul': self.vul,
            'hcp': self.hcp,
            'pos': self.pos,
            'bal': self.bal,
        }

    def fromJson(self, json):
        self.hand = json['hand']
        self.vul = json['vul']
        self.hcp = json['hcp']
        self.pos = json['pos']
        self.bal = json['bal']

    def display(self):
        hand = ['', '', '', '', '']
        cnt = 0
        for suit, numbers in self.hand.items():
            st = suit + ' '
            transfer = {
                2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9,
                10: 'T', 11: 'J', 12: 'Q', 13: "K", 14: "A"
            }
            for num in numbers:
                st += str(transfer[num])
            hand[cnt] = st
            cnt += 1
        hand[cnt] = self.pos + ' HCP:' + str(self.hcp)
        return hand

    def addCard(self, card):
        self.hand[card.suit].append(card.number)
        self.hand[card.suit].sort(reverse=True)
        if card.number > 10:
            self.hcp += card.number - 10

    def isBal(self):
        if self.bal is None:
            self.bal = min(len(self.hand["S"]), len(self.hand["H"]), len(self.hand["D"]), len(self.hand["C"])) >= 2
        return self.bal

    def suitLen(self, suit):
        return len(self.hand[suit])

    def firstBid(self):
        self.display()
        ##2nt(20-21,bal)
        if (self.hcp >= 20 and self.hcp <= 21) and self.isBal():
            print("2nt")
            return
        ##1c(16+unbal,17+bal)
        if (self.isBal() and self.hcp >= 17) or (not self.isBal() and self.hcp >= 16):
            print("1c")
            return
        ##1d()

        ##1h(11-15,5h)
        if (self.hcp >= 11 and self.hcp <= 15) and self.suitLen("H") >= 5:
            print("1h")
            return
        ##1s(11-15,5s)
        if (self.hcp >= 11 and self.hcp <= 15) and self.suitLen("S") >= 5:
            print("1s")
            return
        ##1nt(14-16,bal)
        if (self.hcp >= 14 and self.hcp <= 16) and self.isBal():
            print("1nt")
            return
        ##2c(11-15,6c)
        if (self.hcp >= 11 and self.hcp <= 15) and self.suitLen("C") >= 6:
            print("2c")
            return
        ##2d(11-15,5441-1)
        if (self.hcp >= 11 and self.hcp <= 15) and self.suitLen("D") <= 1 and self.suitLen("C") <= 5 and self.suitLen(
                "H") <= 4 and self.suitLen("S") <= 4:
            print("2d")
            return
        if self.hcp >= 11:
            print("1d")
            return
        print("pass")




def get_hash(s):
    hash = 0
    for x in s:
        hash = (hash * 53 + x) % 100003
    return hash



def dealer():
    s = [x for x in range(52)]
    random.shuffle(s)
    hash = get_hash(s)
    cards = list(map(Card.fromNumber, s))  ## transform numbers to cards
    return hash, cards[:13], cards[13:26], cards[26:39], cards[39:]



class Game():
    def __init__(self, vul, _dealer):
        self.pe, self.ps = Player("None", "East"), Player("None", "South")
        self.pw, self.pn = Player("None", "West"), Player("None", "North")
        self.bids = []
        self.vul = vul
        self.dealer = _dealer
        self.hash, e, s, w, n = dealer()
        for card in e:
            self.pe.addCard(card)
        for card in s:
            self.ps.addCard(card)
        for card in w:
            self.pw.addCard(card)
        for card in n:
            self.pn.addCard(card)

    def toJson(self):
        return {
            'hash': self.hash,
            'pe': self.pe.toJson(),
            'ps': self.ps.toJson(),
            'pw': self.pw.toJson(),
            'pn': self.pn.toJson(),
            'bids': self.bids,
            'vul': self.vul,
            'dealer': self.dealer,
        }

    def fromJson(self, json):
        self.hash = json['hash']
        self.pe.fromJson(json['pe'])
        self.ps.fromJson(json['ps'])
        self.pw.fromJson(json['pw'])
        self.pn.fromJson(json['pn'])
        self.bids = json['bids']
        self.vul = json['vul']
        self.dealer = json['dealer']

    def display(self):
        self.pe.display()
        self.ps.display()
        self.pw.display()
        self.pn.display()

    def startBid(self):
        self.pn.firstBid()
