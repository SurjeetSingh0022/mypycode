a="hello, World!"
print (a)

the_world_is_flat = True
if the_world_is_flat:
    print("the_world_is_flat_true")
else:
    print("the_world_is_flat_false")
  

17 / 3  # classic division returns a float
#5.666666666666667

17 // 3  # floor division discards the fractional part
#5
17 % 3  # the % operator returns the remainder of the division
#2
5 * 3 + 2  # floored quotient * divisor + remainder
#17

a=12.5625
print(round(a,))

print('C:\some\name')  # here \n means newline!
#C:\some
#ame
print(r'C:\some\name')  # note the r before the quote
#C:\some\name




ip="192.168.1.1/24"
ifname='eth0/0'

print({ifname}," ",{ip})

table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 7678}
for name, phone in table.items():
    print(f'{name:10} ==> {phone:10d}')

print('We are the {} who say "{}!"'.format('knights', 'Ni'))

bugs = 'roaches'
count = 13
area = 'living room'
print(f'Debugging {bugs=} {count=} {area=}')

print('This {food} is {adjective}.'.format(
      food='spam', adjective='absolutely horrible'))

table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 8637678}
print('Jack: {0[Jack]:d}; Sjoerd: {0[Sjoerd]:d}; '
      'Dcab: {0[Dcab]:d}'.format(table))
#Jack: 4098; Sjoerd: 4127; Dcab: 8637678

#Handling Exceptions¶
while True:
    try:
        x = int(input("Please enter a number: "))
        break
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")


