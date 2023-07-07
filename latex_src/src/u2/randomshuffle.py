import random

cards = 
[ [i+"_"+j for i in ['2','3','4','5','6','7','8','9','10','J','Q','K','A']] 
for j in ["Spoofing","Tampering","Repudiation","InfoDisclosure","DOS"]] +
[['5_EoP','6_EoP','7_EoP','8_EoP','9_EoP','10_EoP','J_EoP','Q_EoP','K_EoP','A_EoP']]

flat_cards = [card for subl in cards for card in subl]
random.shuffle(flat_cards)
n = len(flat_cards)
p1 = flat_cards[0:n//4]
p2 = flat_cards[n//4:n//2]
p3 = flat_cards[n//2:n//2+n//4]
p4 = flat_cards[n//2+n//4:n]
print()
print(p1)
print()
print(p2) 
print()
print(p3)
print()
print(p4)