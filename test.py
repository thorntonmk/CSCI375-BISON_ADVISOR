import re

file = open("text.txt", "r")
lines = file.readlines()
numbersList = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
numbers = {'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
    }

total = 0
for line in lines:
    digits = re.findall("one|two|three|four|five|six|seven|eight|nine|\d", line)
    first = digits[0]
    last = digits[len(digits) - 1]
    if first in numbersList:
        first = numbers[first]
    if last in numbersList:
        last = numbers[last]
    
    digit = first + last
    print(digit)
    total += int(digit)

print(total)