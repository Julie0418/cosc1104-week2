
# exercise 1 - vowel counter

user_string = input('Enter any text: ').lower()

vowels = ['a', 'e', 'i', 'o', 'u']

counters = [0, 0, 0, 0, 0]

for word in user_string:
    if word in vowels:
        index = vowels.index(word)
        counters[index] += 1
    
for i in range(len(vowels)):
    print(f'{ vowels[i] } - { counters[i] }')



# Sum of digit



