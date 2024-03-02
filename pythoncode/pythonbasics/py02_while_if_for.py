from pprint import pprint as pp
#p1 while
a,b=0,1
#print(a,b)

while a < 10:
    print(a)
    a,b=b,a+b



#p2 while  
a, b = 0, 1
while a < 1000:
    print(a, end=',')
    a, b = b, a+b

#p3 if
#x = int(input("\n Please enter an integer: "))
#print('X = ',x)    
#  
##p4 if
#if x < 0:
#    print('Negative changed to zero')
#elif x == 0:
#    print('Zero')
#elif x == 1:
#    print('Single')
#else:
#    print('More')  

#p4 for
# Measure some strings:
words = ['cat', 'window', 'defenestrate']   
for w in words:
    print(w,len(w))

#p5 for
iplist=['192.168.10.0','192.168.11.0','192.168.12.0','192.168.13.0']  
for ip in range(len(iplist)):
    if iplist[ip]=='192.168.10.0':
        iplist[ip]='192.168.100.0'
        print('iplist has been updated')
    else:
        print('ip not found in iplist to update')    
print(iplist)   

#p6 with dict
# Create a sample collection
users = {'Hans': 'active', 'surjeet': 'inactive', 'minku': 'active'}

# Strategy:  Iterate over a copy
for user, status in users.copy().items():
    if status == 'inactive':
        del users[user]
print(users)        

# Strategy:  Create a new collection
active_users = {}
for user, status in users.items():
    if status == 'active':
        active_users[user] = status


# access dict and print the output as needed
rtr={'r1':'192.168.1.1','r2':'192.168.2.1','r3':'192.168.3.1','r4':'192.168.4.1'}   
print('rtr orginal dict',rtr)
print('getting r4 ip',rtr.get('r4','not found'))
for hostame,ip in rtr.items():
    print('list of ip in rtr',hostame,ip)

#update the dict
rtr['r3']='192.168.30.1'
print('r3 new ip address is',rtr['r3'])

if 'r4' in rtr:
    rtr['r4'] = '192.168.40.1'
else:
    print("'r4' not found in the dictionary")
print('r4 new ip address is',rtr['r4'])  


# creating list
rtrhostlist=[]
for hostname,ip in rtr.items():
    rtrhostlist.append(ip)
print(rtrhostlist)
# accessing list
print(rtrhostlist[-1])


#range
for i in range(1,5):
    print(i)

a=list(range(5, 10))
print (a)

#--------------------------
#Generating interface config
#-----------------------------
# List of interfaces
iflist = ['GigabitEthernet0/1', 'GigabitEthernet0/2', 'GigabitEthernet0/3']

# List of IP addresses
iplist = ['192.168.3.1', '192.168.4.1', '192.168.5.1']

# Ensure both lists have the same length
assert len(iflist) == len(iplist), "Lists must have the same length"

# Generate interface configurations
config=[]
for i in range(len(iflist)):
    config.append([
        f"interface {iflist[i]}",
        f" ip address {iplist[i]} 255.255.255.0",
        " no shutdown",
        "!"
        ])
    
pp(config) 
 

#print list with range
a = ['Mary', 'had', 'a', 'little', 'lamb']
for i in range(len(config)):
    print(config[i])

r=range(10)
print(r)   
for r in r:
    print(r) 

print(sum(range(4)))    


# break and continue Statements, and else Clauses on Loops¶
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n//x)
            break
    else:
        # loop fell through without finding a factor
        print(n, 'is a prime number')


#p2 break and continue Statements, and else Clauses on Loops¶
for num in range(2, 10):
    if num % 2 == 0:
        print("Found an even number", num)
        continue
    print("Found an odd number", num)  


#create interface config
intlist=['eth0/0', 'eth0/1', 'eth0/2'] 
iplist= ["192.168.1."+str(x)+"/24" for x in range(10)] 
config=[(int,ip) for int in intlist for ip in iplist] 
pp(config)   

import fibo
def fib(n):    # write Fibonacci series up to n
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()

def fib2(n):   # return Fibonacci series up to n
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a+b
    return result
