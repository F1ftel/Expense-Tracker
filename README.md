# Expense Tracker - Python Project

## Project Overview

Expense Tracker is a desktop application written in Python that allows users to record, manage, analyze, and visualize personal expenses. The project demonstrates object-oriented programming, file handling, data analysis, and graphical user interface development using modern Python libraries. This application was developed as a final course project for a Python programming course.

## Project Objectives

The project fulfills the course goals by:

- Applying Python fundamentals and OOP principles
- Using standard and external Python libraries
- Solving a real-world problem using programming
- Working with files, data structures, and data analysis tools
- Creating a complete, user-friendly application

## Key Features

### 1. Expense Management

- **Add new expenses** with:
  - Date (calendar-based, default = today)
  - Predefined categories
  - Amount
  - Optional description
- Automatically validates input data
- Delete existing expenses
- Automatically saves data to CSV
- Automatically loads saved data on startup

### 2. Analytics & Statistics

- Total expenses
- Average daily expenses
- Number of used categories
- **Expense aggregation by**:
  - Category
  - Date
  - Month

### 3. Data Visualization

- Pie chart: expenses by category
- Line chart: expenses over time
- Bar chart: monthly totals
- Charts embedded directly in the GUI

### 4. Graphical User Interface

- Built with CustomTkinter
- Clean, modern, and responsive layout
- Tab-based navigation
- Scrollable expense list
- Integrated charts and statistics dashboard

## Project Structure

```
Expense Tracker/
│
├── data/
│   └── expenses.csv        # Stored expense data
│
├── analytics.py            # Expense analysis logic
├── expense.py              # Expense data model & validation
├── tracker.py              # Data storage & management
├── gui.py                  # Graphical user interface
│
├── requirements.txt        # Required Python packages
└── README.md               # Project documentation
```

## Technologies Used

- **Python 3**
- **Pandas** - data handling and analysis
- **Matplotlib** - data visualization
- **CustomTkinter** - modern GUI framework
- **CSV** - persistent data storage

## How to Run the Application

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the application:
   ```bash
   python gui.py
   ```

## Design & Architecture

### Object-Oriented Design

- **Expense** - represents a single expense
- **ExpenseTracker** - manages storage and retrieval
- **ExpenseAnalytics** - performs calculations and aggregations
- **ExpenseTrackerGUI** - handles user interaction

### Key Principles

- Separation of concerns between logic, data, and UI
- Automatic data persistence using CSV files
- Defensive programming and input validation

## Authors

**Course Project - Python Programming**

This project was created for educational purposes to demonstrate practical Python programming skills by:

- Maksims Selkovskis (ms24100)
- Raimonds Silinevics (rs24085)
