import random

data = []
teachers = [['a',0,[]],['b',0,[]],['c',0,[]],['d',0,[]],['e',0,[]],['f',0,[]],['g',0,[]],['h',0,[]],
['i',0,[]],['j',0,[]],['k',0,[]],['l',0,[]],['m',0,[]],['n',0,[]],['o',0,[]],['p',0,[]]]

# data {batch_code, slot_no, am_i_assigned}
# techers {teacher_code, number_of_assigned_slots, [{batch_code, slot_time}]}

for i in range(34):
    data.append([f'code{i}',random.randint(1,13),0])

for i in range(len(data)):
    print(data[i])

def checkIfSomeTecherIsEmpty(teachers):
    for i in teachers:
        if(len(i[2]) == 0):
            return 1
    return 0

ite = 0

while(checkIfSomeTecherIsEmpty(teachers)):
    for i in range(len(data)):
        while(data[i][2] == 0):
            current_selection = random.randint(0,len(teachers)-1)
            if(teachers[current_selection][1] < 4):
                do_we_reject = 0
                maximum_difference = 0
                for j in teachers[current_selection][2]:
                    maximum_difference = max(maximum_difference,abs(data[i][1]-j[1]))
                    if(abs(j[1]-data[i][1]) <= 1):
                        do_we_reject = 1
                        break
                if(do_we_reject == 1):
                    continue
                elif(maximum_difference > 8):
                    continue
                else:
                    teachers[current_selection][2].append([data[i][0],data[i][1]])
                    teachers[current_selection][1] += 1
                    data[i][2] = 1
    ite+=1
    print(ite)


print()
for i in teachers:
    print(i)