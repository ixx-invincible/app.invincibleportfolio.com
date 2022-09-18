import random


tickets = []

for i in range(3):
    random_list = random.sample([1,2,7,8,12,13,18,19,23,24,25,29,30,34,35,40,45,46], 18)

    tickets.append(random_list[0:6])
    tickets.append(random_list[6:12])
    tickets.append(random_list[12:18])

print(tickets)