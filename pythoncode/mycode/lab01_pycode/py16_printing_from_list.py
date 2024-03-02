''' basic print function to print index from list'''

list=['R1','R2','R3','R4']

print(f'printing list output {list}')
# print using loop
for rtr in list:
    print(f'router {rtr}')

# print using index number
print(list[0]) 

# creating list with single dict
listwithdict=[{'R1': '192.168.2.11','R2': '192.168.2.12','R3': '192.168.2.13','R4': '192.168.2.14'}]

print(f'printing list with dict output {listwithdict}')

# Print router names and IPs
for router in listwithdict[0]:
    print(f"Router {router}: {listwithdict[0][router]}")

# creating list with multiple dict
listwithdictifname = [
    {'R1': {'ip': '192.168.2.11', 'ifname': 'eth0/0'},
     'R2': {'ip': '192.168.2.12', 'ifname': 'eth0/1'},
     'R3': {'ip': '192.168.2.13', 'ifname': 'eth0/0'},
     'R4': {'ip': '192.168.2.14', 'ifname': 'eth0/1'}}
    ]

#print(f'Printing list with dict output {listwithdictifname}')

# Print router name and it's if name from dict
for rtr in listwithdictifname:
    print(f'\n{rtr}: {rtr}.[ifname]')


listwithdictifname = [
    {'R1': {'ip': '192.168.2.11', 'ifname': 'eth0/0'},
     'R2': {'ip': '192.168.2.12', 'ifname': 'eth0/1'},
     'R3': {'ip': '192.168.2.13', 'ifname': 'eth0/0'},
     'R4': {'ip': '192.168.2.14', 'ifname': 'eth0/1'}}
]

# Print the value for R2 key
print("Value for R2 key:", listwithdictifname[0]['R2'])

# Print the ifname associated with R3
print("ifname for R3:", listwithdictifname[0]['R3']['ifname'])

# Print the hostname and IP address for each router
for router, details in listwithdictifname[0].items():
    print(f"Hostname for {router}: {details['ip']}")

devices_inventory= [
    {
     'R3': {'mgmtip': '192.168.2.13', 'ifname': 'eth0/0', 'Console_Port': '32669'},
     'R4': {'mgmtip': '192.168.2.14', 'ifname': 'eth0/1', 'Console_Port': '32670'},
     'SW01': {'mgmtip': '192.168.2.15', 'ifname': 'eth0/1', 'Console_Port': '32671'},
     'SW02': {'mgmtip': '192.168.2.16', 'ifname': 'eth0/1', 'Console_Port': '32672'}
     }
]  

def get_ip_information(device_name):
    # Print the hostname and IP address for each router
    for router, details in listwithdictifname[0].items():
        print(f"Hostname for {router}: {details['ip']} : Console: {details['Console_Port']}")

a= get_ip_information('R3')    


#list1 = ['192.168.10.1','192.168.10.11','192.168.10.21','192.168.10.31']
#list2 = []
#
#for ip in list1:
#    print(f'RTR : {ip}')
#    list2.append(f'{ip} 255.255.255.0')
#    
#print (list2)
#
#student_grades = [85, 90, 78, 92, 88]
## Print the highest grade
#print(max(student_grades))
## Print the lowest grade
#print(min(student_grades))
#
#
#book_library = ["To Kill a Mockingbird", "1984", "The Great Gatsby", "The Catcher in the Rye", "Moby Dick"]
## Print the first three books in the library
#print(book_library[:3])
## Print the last two books in the library
#print(book_library[-2:])
#
#fruits = ["apple", "banana", "cherry"]
#fruits.insert(1, "orange")
#print(fruits)  # Output: ['apple', 'orange', 'banana', 'cherry']
#

student_grades = {"John": 85, "Emily": 90, "Michael": 78}
for name in student_grades.keys():
    print(name)


student_grades = {"John": 85, "Emily": 90, "Michael": 78}
for grade in student_grades.values():
    print(grade)


student_grades = {"John": 85, "Emily": 90, "Michael": 78}
print(student_grades["Emily"])

# creating list with multiple dict
listwithdictifname = {'ip': '192.168.2.11', 'ifname': 'eth0/0'}
print(listwithdictifname["ip"])

# A dictionary representing a student and their grades in different subjects
student_grades = {
    "John": {
        "Math": 85,
        "English": 90,
        "Science": 78
    },
    "Emily": {
        "Math": 92,
        "English": 88,
        "Science": 95
    },
    "Michael": {
        "Math": 87,
        "English": 85,
        "Science": 91
    }
}

# Print all students and their grades
for student,grades in student_grades.items():
    print(f'for {student} grades:')
    for subject, grade in grades.items():
        print(f"{subject}: {grade}")
    print()  # Print a newline for better readability

print(student_grades["John"]["Math"])


# A nested list representing student grades in different subjects
student_grades = [
    ["John", [85, 90, 78]],  # John's grades in Math, English, Science
    ["Emily", [92, 88, 95]],  # Emily's grades in Math, English, Science
    ["Michael", [87, 85, 91]]  # Michael's grades in Math, English, Science
]

# Print all students and their grades
for student in student_grades:
    print(f"{student[0]}'s grades:")
    for grade in student[1]:
        print(grade)
    print()  # Print a newline for better readability











