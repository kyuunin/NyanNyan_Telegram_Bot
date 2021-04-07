import os
colors = [0xff0000, 0xff0000, 0, 0]
suits = ['♦','♥','♣','♠']
ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
with open("sample_card.svg","r") as f:
    text = f.read()
data = {"white":0xffffff,"black":0}
for data["rank"] in ranks:
    for data["color"], data["suit"] in zip(colors, suits):
        with open("svg/%(rank)s%(suit)s.svg"%data,"w") as f:
            f.write(text%data)
        os.system("inkscape -h 512 svg/%(rank)s%(suit)s.svg -e png/%(rank)s%(suit)s.png"%data)
        
colors = [0xcb3535, 0xcb3535, 0x323232, 0x323232]
data = {"white":0xc8c8c8,"black":0x323232}
for data["rank"] in ranks:
    for data["color"], data["suit"] in zip(colors, suits):
        with open("svg/off_%(rank)s%(suit)s.svg"%data,"w") as f:
            f.write(text%data)
        os.system("inkscape -h 512 svg/off_%(rank)s%(suit)s.svg -e png/off_%(rank)s%(suit)s.png"%data)

