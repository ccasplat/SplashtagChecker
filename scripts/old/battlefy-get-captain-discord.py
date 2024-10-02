csv_file_name = "path/to/battlefy.csv"

import csv

# Initialize a dictionary to store invalid entries grouped by teamName
captain_usernames = []


# Open and read the CSV file
with open(csv_file_name, mode='r', newline='') as file:
    reader = csv.DictReader(file)

    # Iterate over each row in the CSV file
    for row in reader:
        discordUsername = row['Discord Username of team captain (all lowercase, please do not include the @ symbol)']
        if discordUsername not in captain_usernames:
            captain_usernames.append(discordUsername)

for username in captain_usernames:
    print(username)

