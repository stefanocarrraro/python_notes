# this is a try


n1 = float(input('Enter the first number: '))
n2 = float(input('Enter the second number: '))

s = n1 + n2

print(s)

# --------------------

weight = float(input('Enter your weight: '))

unit = 'A'
while unit!='K' and unit!='k' and unit!='L' and unit!='l':
    unit = str(input('kg (K) or lb (L): '))

if unit=='K' or unit=='k':
    weight = str(2.20462 * weight)
    print('Your weight in lb is: ' + weight)
else:
    weight = str(weight / 2.20462 )
    print('Your weight in kg is: ' + weight)


# ----------------------

i = 1
while i <= 10:
    print(i * '*')
    i += 1



