import re

pattern = r"^[0-9][0-9]-[0-9][0-9][0-9]$"

post_code = input("Podaj kod pocztowy: ")
print(re.search(pattern, post_code) != None)