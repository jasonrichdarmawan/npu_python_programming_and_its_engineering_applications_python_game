# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 16:41:45 2024

@author: HP
"""

import os

DIARY_FILE = "db/diary.txt"

def pause_after(func):
    def wrapper(*args, **kwargs):
      os.system('clear')
      func(*args, **kwargs)
      input("Press Enter to continue...")
      os.system('clear')
    return wrapper

__running__ = True
@pause_after
def writeNewDiaryEntryDialog():
  __running__ = True

  """
  Function to write a new diary entry.

  This function prompts the user for the date, title, and content of the diary entry.
  It then appends the entry in the specified format to the diary file.

  feat 3: add multi-line support for the content of the diary entry
  """
  date = input("Please enter the date (YYYY-MM-DD): ")
  title = input("Please enter the title of the diary: ")

  print("Please enter the content of the diary (type 'SAVE' on a new line to save, 'DISCARD' to discard): ")
  lines: list[str] = []
  while True:
    line = input()
    match line.strip():
      case "SAVE":
        break
      case "DISCARD":
        print("Diary entry discarded.")
        return
    lines.append(line)
  content = "\\n".join(lines)

  # Format the diary entry
  entry = f"{date}|{title}|{content}\n"

  with open(DIARY_FILE, "a") as f:
    f.write(entry)

  print("Diary entry successfully written!")

@pause_after
def printDiaryEntries():
  """
  Function to view all diary entries.

  This function reads the diary file, parses each entry, and displays the date,
  title, and a short preview of the content for each entry.
  """
  if not os.path.exists(DIARY_FILE):
    print("No diary entries found.")
    return

  with open(DIARY_FILE, "r") as f:
    entries = f.readlines()

  for entry in entries:
    date, title, content = entry.strip().split("|")
    preview = content[:50].replace("\\n", "\n")
    print("Date: %s" % (date))
    print("Title: %s" % (title))
    print("Preview:")
    print("%s...\n" % (preview))

@pause_after
def searchDiaryEntryByKeywordDialog():
  """
  Function to search for diary entries based on a keyword.

  This function prompts the user for a keyword and searches through the diary
  entries. If a match is found in the title or content, it displays the relevant entry.

  fix 2: find entries that match the keyword in the date as well
  """
  keyword = input("Please enter the keyword to search for: ")

  if not os.path.exists(DIARY_FILE):
    print("No diary entries found.")
    return

  with open(DIARY_FILE, "r") as f:
    entries = f.readlines()

  foundEntries: list[str] = []
  for entry in entries:
    date, title, content = entry.strip().split("|")
    if (keyword in date or
        keyword in title or 
        keyword in content):
      foundEntries.append(entry)

  if foundEntries:
    print("Found %d entries matching the keyword:" % (len(foundEntries)))
    for entry in foundEntries:
      date, title, content = entry.strip().split("|")
      print(f"Date: {date}")
      print(f"Title: {title}")
      print(f"Preview: {content[:50]}...\n")
  else:
      print("No entries found matching the keyword.")

@pause_after
def deleteDiaryEntryDialog():
  """
  Function to delete a specific diary entry.

  This function prompts the user for the date and title of the entry to delete.
  It then reads the diary file, removes the matching entry, and rewrites the file
  without the deleted entry.

  fix 1: print error if the diary entry is not found
  """
  dateToDelete = input("Please enter the date (YYYY-MM-DD) of the entry to delete: ")
  titleToDelete = input("Please enter the title of the entry to delete: ")

  if not os.path.exists(DIARY_FILE):
    print("No diary entries found.")
    return

  with open(DIARY_FILE, "r") as f:
    entries = f.readlines()

  entryFound = False
  entryIndex = -1
  for index, entry in enumerate(entries):
    date, title, _ = entry.strip().split("|")
    if date == dateToDelete and title == titleToDelete:
      entryFound = True
      entryIndex = index
      break

  if not entryFound:
    print("Diary entry not found.")
    return

  filteredEntries = [entry for i, entry in enumerate(entries) if i != entryIndex]
  with open(DIARY_FILE, "w") as f:
    f.writelines(filteredEntries)

  print("Diary entry successfully deleted!")

if __name__ == "__main__":
  """
  chore 1: rename the functions to make them more descriptive
  chore 2: use match case instead of if else for the choice
  chore 3: add key "q" to quit the program
  chore 4: 
    after invalid choice, 
    wait for the user to press enter before printing the menu again
  feat 1: clear the screen before printing the menu at program start
  feat 2: 
    add a pause after each menu option is executed, 
    clear before and after printing the menu
  chore 5: change diary file path to db/diary.txt
  """

  os.system('clear')

  while True:
    print("Diary Management System")
    print("1. Write a new diary entry")
    print("2. View all diary entries")
    print("3. Search for diary entries by keyword")
    print("4. Delete a diary entry")
    print("5. Quit")

    choice = input("Please enter your choice (1-5): ")

    match choice:
      case "1":
        writeNewDiaryEntryDialog()
      case "2":
        printDiaryEntries()
      case "3":
        searchDiaryEntryByKeywordDialog()
      case "4":
        deleteDiaryEntryDialog()
      case "5" | "q":
        break
      case _: # default case
        print("Invalid choice. Please try again.")