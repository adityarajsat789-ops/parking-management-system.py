# Parking Management System

**Problem Statement:** PS No. 47  
**Language:** Python 3  
**Application:** Console-based parking management system

## Overview

A simple parking management program for a small parking area containing five numbered slots. It supports vehicle entry, vehicle exit, fee calculation, parking status, and saving occupied slots between program runs.

## Requirements

- Total parking capacity: 5 vehicles
- Car rate: Rs. 20 per hour
- Bike rate: Rs. 10 per hour
- Supported vehicle types: `car` and `bike`
- Parking time is rounded up to the next whole hour.
- Minimum charge: 1 hour
- Parking data is stored in `parking.txt`.

## Features

1. **Entry:** Parks a vehicle in the first available slot.
2. **Exit:** Removes a parked vehicle and calculates its fee.
3. **Status:** Displays all five slots and the number of free slots.
4. **Validation:** Rejects duplicate vehicle numbers, unsupported vehicle types, unknown exit vehicles, and invalid parking hours.
5. **Persistence:** Saves the current slot data to `parking.txt` after each successful entry or exit.

## Project Structure

```text
Parking-Management-System/
├── one.py          # Main Python program
├── parking.txt     # Saved parking data (starts empty)
├── test_one.py     # Automated test cases
└── README.md       # Project documentation
```

## Run the Project

Make sure Python 3 is installed. Open a terminal in the project folder and run:

```bash
python one.py
```

### Menu

- `1` — Entry
- `2` — Exit
- `3` — Status
- `4` — Quit

For exit, enter the parking duration in hours when prompted. For example, 2.5 hours is charged as 3 hours.

## Run Automated Tests

```bash
python -m unittest -v
```

The tests cover the four supplied problem-statement scenarios, full-lot handling, data persistence, and invalid hours.

## Concepts Used

- Lists
- Dictionaries
- Conditional statements
- Functions and methods
- File handling
- Input validation

## Fee Examples

| Vehicle | Entered hours | Charged hours | Fee |
|---|---:|---:|---:|
| Car | 0.5 | 1 | Rs. 20 |
| Bike | 2.5 | 3 | Rs. 30 |
| Car | 2 | 2 | Rs. 40 |
| Bike | 1 | 1 | Rs. 10 |

## Notes

- `parking.txt` is initialized as an empty parking lot. The program updates it automatically.
- If the data file is missing, the program starts with all five slots free.
- The duration is entered at exit, as required by the supplied test cases; the program does not calculate elapsed time from real clock timestamps.
