student_number = 12728489

student_name = "Aidan Inglis"


import sys
import re
from PySide6.QtWidgets import QLabel, QWidget, QApplication, QGridLayout, QLineEdit, QListWidget, QComboBox
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt
import csv 


ROUND_ORDER = [
    "Round 1", "Round 2", "Round 3", "Round 4", "Round 5",
    "Round 6", "Round 7", "Round 8", "Round 9", "Round 10",
    "Round 11", "Round 12", "Round 13", "Round 14", "Round 15",
    "Round 16", "Round 17", "Round 18", "Round 19", "Round 20",
    "Round 21", "Round 22", "Round 23", "Round 24",
    "Qualifying Final",
    "Elimination Final",
    "Semi Final",
    "Preliminary Final",
    "Grand Final"]


with open('games.csv', 'r') as file:
    reader = csv.reader(file)

    rows = []

    #appending csv data to a list for easy access and referal
    for row in reader:
        rows.append(row)


    def on_season_clicked(item):
        round_list_widget.clear()
        game_list_widget.clear()

        #the year will be the 2nd word (index of 1) as the item is "Season 2023", 
        # so the example would result in just 2023 (how its reffered to in the csv data)
        year = item.text().split()[1]

        # a set is used rather than a list as a list.append() will add the item to the end of the list regardless of if it is already
        # present. a set.add() does not add the item if it is already included.
        rounds = set()

        for row in rows:
            if row[1] == year:   # column 1 is the year in the csv
                rounds.add(row[2])  # column 2 is the round in the csv
               
        
        ordered_rounds = [round for round in ROUND_ORDER if round in rounds] # orders the rounds so they match the format
                                                                             # of the "ROUND ORDER" variable

        for round in ordered_rounds:
            round_list_widget.addItem(round)


    def on_round_clicked(item):
        game_list_widget.clear()

        # selects the specific round (that was just added by the above function) when it is clicked
        selected_round = item.text()
        year = list_widget.currentItem().text().split()[1]

        for row in rows:
            if row[1] == year and row[2] == selected_round:
                team1 = row[10]
                team2 = row[16]
                team1_score = row[15]
                team2_score = row[21]

                game_list_widget.addItem(f"{team1} vs {team2} - {team1_score} - {team2_score}")

    def team_search():
        results_widget.clear()
        input = specific_entry.text().strip()
        
        # regular expression that ignores case sensitivity when users submit a search (for an easier search)
        # re.compile makes it so it follows a pattern so the whole word doesnt need to be spelt out
        pattern = re.compile(input, re.IGNORECASE)

        selected_season = dropdown.currentText()
        
        for row in rows:
            year = row [1]
            round = row[2]
            team1 = row[10]
            team2 = row[16]
            team1_score = row[15]
            team2_score = row[21]

            
            if selected_season != "All Seasons" and year != selected_season:
                continue


            if pattern.search(team1) or pattern.search(team2):
                results_widget.addItem(f"{year} - {round} : {team1} vs {team2} - {team1_score} - {team2_score}")




# GUI setup

    font = QFont("Arial", 18)

    app = QApplication([])
    app_window = QWidget()
    
    app_window.setWindowTitle("AFL Results Search")

    logo_label = QLabel()
    the_image = QPixmap("AFL.png")
    logo_label.setPixmap(the_image)
    logo_label.setAlignment(Qt.AlignCenter)


    select_season_label = QLabel("Select a Season:")
    select_season_label.setFont(font)

    select_round_label = QLabel("Select a Round:")
    select_round_label.setFont(font)

    games_label = QLabel("Games in the Round:")
    games_label.setFont(font)
    

    list_widget = QListWidget()
    for i in range(2012, 2026):
        list_widget.addItem(f"Season {i}")

  

    
    round_list_widget = QListWidget()
    game_list_widget = QListWidget()

    list_widget.itemClicked.connect(on_season_clicked)
    round_list_widget.itemClicked.connect(on_round_clicked)


    specific_entry_label = QLabel("Search for specific team data:")
    specific_entry_label.setFont(font)

    specific_entry = QLineEdit()
    specific_entry.setPlaceholderText("Enter Team Name")


    dropdown = QComboBox()
    dropdown.setPlaceholderText("Select a Year")
    dropdown.addItems(['All Seasons', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025'])

    dropdown.currentIndexChanged.connect(team_search)


    results_widget = QListWidget()

    

    layout = QGridLayout()
    #setContentsMargins(left, top, right, bottom)
    layout.setContentsMargins(30, 30, 30, 30)
    layout.setHorizontalSpacing(30)
    layout.setVerticalSpacing(10)

    layout.addWidget(logo_label, 0, 1, 1, 1)

    layout.addWidget(select_season_label, 1, 0)
    layout.addWidget(select_round_label, 1, 1)
    layout.addWidget(games_label, 1, 2)


    layout.addWidget(list_widget, 3, 0)

    
    layout.addWidget(round_list_widget, 3, 1)
    layout.addWidget(game_list_widget, 3, 2)


    layout.addWidget(specific_entry_label, 4, 1)
    layout.addWidget(specific_entry, 5, 1)

    layout.addWidget(dropdown, 6, 1)


    layout.addWidget(results_widget, 8, 1)
    



    app_window.setLayout(layout)

    app_window.show()
    sys.exit(app.exec())
