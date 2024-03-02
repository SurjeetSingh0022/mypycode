import getpass
import telnetlib

HOST = "192.168.2.13"
user = input("Enter your remote account: ")
password = getpass.getpass()
cmd = input("Enter Your Command : ")

tn = telnetlib.Telnet(HOST)

tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.write(b"terminal len 0\n")
tn.write(cmd.encode('ascii') + b"\n")  # Encode the command as bytes
tn.write(b"exit\n")
inter = tn.read_until(b"exit\n").decode('ascii')
tn.close()

## print(tn.read_all().decode('ascii'))
print(inter)
