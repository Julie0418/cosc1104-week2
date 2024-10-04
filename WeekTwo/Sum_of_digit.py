
user_input = int(input ('enter any number: '))
sum_total = 0

while user_input > 0:
    last_digit = user_input % 10
    sum_total += last_digit
    user_input = user_input // 10
print (sum_total)