import re
password = input("Enter the password: ")
if len(password < 8):
    print("Password length must be atleast 8 characters long")
elif not re.search("[A-Z]", password):
    print("Password must have atleast one uppercase letter.")
elif not re.search("[a-z]", password):
    print("Pass")