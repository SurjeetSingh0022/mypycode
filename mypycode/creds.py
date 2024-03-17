from pykeepass import PyKeePass

# Load the KeePass database
kp = PyKeePass(rf'D:\keepass\keepass_lab.db', password='admin')

# Find an entry by its title (e.g., 'lab01-router')
entry = kp.find_entries(title='lab01-router', first=True)

if entry:
   username = entry.username
   password = entry.password
else:
    print("Entry not found.")


# Close the database (optional)
#kp.close()