import random

listofstudents = []
slot_frequency = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
students_allotted = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
batches = []

def giveMeRandom4Slots():
    ans = []
    while(len(ans) != 4):
        my_random_slot = random.randint(1,13)
        if(my_random_slot not in ans):
            ans.append(my_random_slot)
    return ans

def rankMyChoices(choices):
    ans = []
    for i in range(0,4):
        ans.append(slot_frequency[choices[i]]%15)
    return choices.index(min(choices))


for i in range(0,500):
    listofstudents.append([f'student{i}@email.com', giveMeRandom4Slots()])

for i in range(0,500):
    print(listofstudents[i])

for i in listofstudents:
    chosen_slot = rankMyChoices(i[1])
    slot_frequency[i[1][chosen_slot]] += 1
    students_allotted[i[1][chosen_slot]].append(i[0])

for i in students_allotted:
    print(i)

batch_number = 1
one_batch = []
for i in range(len(students_allotted)):
    for j in students_allotted[i]:
        if(len(one_batch) < 15):
            one_batch.append(j)
        else:
            batches.append([batch_number, i, one_batch])
            batch_number += 1
            one_batch = []
            one_batch.append(j)
    if(len(one_batch) > 0):
        batches.append([batch_number, i, one_batch])
        batch_number += 1
        one_batch = []

for i in batches:
    print(i)

