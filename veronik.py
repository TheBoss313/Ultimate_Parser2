from random import *


def make(difficulty):
    numbers = []
    if difficulty == '1':
        while True:
            num = randint(0, 9)
            if len(numbers) == 2:
                numbers2 = numbers.copy()
                numbers2.sort(reverse=True)
                break
            elif num not in numbers:
                numbers.append(num)
        shuffle(numbers)
        return f'Question: {numbers} \nAnswer: {numbers2}'
    elif difficulty == '2':
        while True:
            num = randint(0, 9)
            if len(numbers) == 3:
                numbers2 = numbers.copy()
                numbers2.sort(reverse=True)
                break
            elif num not in numbers:
                numbers.append(num)
        shuffle(numbers)
        return f'Question: {numbers} \nAnswer: {numbers2}'
    else:
        while True:
            num = randint(0, 9)
            if len(numbers) == 5:
                numbers2 = numbers.copy()
                numbers2.sort(reverse=True)
                break
            elif num not in numbers:
                numbers.append(num)
        shuffle(numbers)
        return f'Question: {numbers} \nAnswer: {numbers2}'


diffic = input().split(',')
len(diffic)
for i in diffic:
    print(make(i))
    print()
