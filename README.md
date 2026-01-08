Expense Tracker - Python Project

Project Overview: 
Expense Tracker is a desktop application written in Python that allows users to record, manage, analyze, and visualize personal expenses. 
The project demonstrates object‑oriented programming, file handling, data analysis, and graphical user interface development using modern Python libraries. 
This application was developed as a final course project for a Python programming course.

Project Objectives: 
The project fulfills the course goals by: 
Applying Python fundamentals and OOP principles 
Using standard and external Python libraries 
Solving a real‑world problem using programming 
Working with files, data structures, and data analysis tools 
Creating a complete, user‑friendly application

Key Features: 
1) Expense Management: 
1.1) Add new expenses with: 
1.1.1) Date (calendar‑based, default = today) 
1.1.2) Predefined categories 
1.1.3) Amount 
1.1.4) Optional description 
1.2) Automatically validates input data 
1.3) Delete existing expenses 
1.4) Automatically saves data to CSV 
1.5) Automatically loads saved data on startup 
2) Analytics & Statistics: 
2.1) Total expenses 
2.2) Average daily expenses 
2.3) Number of used categories 
2.4) Expense aggregation by: 
2.4.1) Category 
2.4.2) Date 
2.4.3) Month 
3) Data Visualization: 
3.1) Pie chart: expenses by category 
3.2) Line chart: expenses over time 
3.3) Bar chart: monthly totals 
3.4) Charts embedded directly in the GUI 
4) Graphical User Interface: 
4.1) Built with CustomTkinter 
4.2) Clean, modern, and responsive layout 
4.3) Tab‑based navigation 
4.4) Scrollable expense list 
4.5) Integrated charts and statistics dashboard

Project Structure: 
Expense Tracker/
│
├── data/
│   └── expenses.csv        # Stored expense data
│
├── analytics.py            # Expense analysis logic
├── expense.py              # Expense data model & validation
├── tracker.py              # Data storage & management
├── gui.py                  # Graphical user interface
├── main.py                 # Application entry point
│
├── requirements.txt        # Required Python packages
└── README.md               # Project documentation

Technologies Used: 
Python 3 
Pandas - data handling and analysis 
Matplotlib - data visualization 
CustomTkinter - modern GUI framework 
CSV - persistent data storage

How to Run the Application: 
1) Install dependencies: pip install -r requirements.txt 
2) Start the application: python main.py

Design & Architecture: 
1) Object‑Oriented Design: 
1.1) Expense - represents a single expense 
1.2) ExpenseTracker - manages storage and retrieval 
1.3) ExpenseAnalytics - performs calculations and aggregations 
1.4) ExpenseTrackerGUI - handles user interaction 
2) Separation of concerns between logic, data, and UI 
3) Automatic data persistence using CSV files 
4) Defensive programming and input validation

Authors: 
Course Project - Python Programming 
This project was created for educational purposes to demonstrate practical Python programming skills by Maksims Selkovskis ms24100 and Raimonds Silinevics rs24085.