from database import CAGstatDatabase
import yaml

DatabaseCheck = CAGstatDatabase()
DatabaseCheck.DatabaseCreation()

team_id = raw_input("Enter Team ID: ")
game = raw_input("Enter the Game Number: ")
total_yards = raw_input("Enter the Total Yards: ")
passing_yards = raw_input("Enter the Passing Yards: ")
rushing_yards = raw_input("Enter the Rushing Yards: ")
turnovers = raw_input("Enter the amount of turnovers: ")

with open('configuration/CAG55_teams.yml', 'r') as f:
    doc = yaml.load(f)
    team_info = doc["0"]["team_name"]
    f.close()

print team_id + '\n' + team_info + '\n' + game + '\n' + total_yards
print passing_yards + '\n' + rushing_yards + '\n' + turnovers

#data = []
