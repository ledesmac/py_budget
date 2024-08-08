import pandas as pd
import pdfplumber
import re

BUDGET_FILE = 'budget.csv'

def read_budget(file):
    return pd.read_csv(file)

def write_budget(file, data):
    data.to_csv(file, index=False)

def display_budget(data):
    print(data)
    
def add_expense(data):
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category: ")
    description = input("Enter description: ")
    amount = input("Enter amount: ")
    new_expense = pd.DataFrame([[date, category, description, amount]], columns=data.columns)
    data = pd.concat([data, new_expense], ignore_index=True)
    print("Expense added successfully.")
    return data

def edit_expense(data):
    display_budget(data)
    index = int(input("Enter the index of the expense you want to edit: "))
    if 0 <= index < len(data):
        print("Leave the field blank to keep the current value.")
        date = input(f"Enter new date (YYYY-MM-DD) [{data.at[index, 'date']}]: ") or data.at[index, 'date']
        category = input(f"Enter new category [{data.at[index, 'category']}]: ") or data.at[index, 'category']
        description = input(f"Enter new description [{data.at[index, 'description']}]: ") or data.at[index, 'description']
        amount = input(f"Enter new amount [{data.at[index, 'amount']}]: ") or data.at[index, 'amount']
        data.at[index, 'date'] = date
        data.at[index, 'category'] = category
        data.at[index, 'description'] = description
        data.at[index, 'amount'] = amount
        print("Expense updated successfully.")
    else:
        print("Invalid index.")
    return data

def extract_expenses_from_pdf(pdf_file):
    expenses = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")
            for line in lines:
                match = re.match(r'(\d{4}-\d{2}-\d{2}),(\w+),(.+),(\d+\.\d{2})', line)
                if match:
                    date, category, description, amount = match.groups()
                    expenses.append({'date': date, 'category': category, 'description': description, 'amount': amount})
    return expenses

def upload_expenses_from_pdf(data, pdf_file):
    expenses = extract_expenses_from_pdf(pdf_file)
    new_expenses_df = pd.DataFrame(expenses)
    data = pd.concat([data, new_expenses_df], ignore_index=True)
    print("Expenses uploaded successfully from PDF.")
    return data

def main():
    data = read_budget(BUDGET_FILE)
    while True:
        print("\nBudgeting App")
        print("1. Display Budget")
        print("2. Add Expense")
        print("3. Edit Expense")
        print("4. Upload Expenses from PDF")
        print("5. Save and Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            display_budget(data)
        elif choice == '2':
            data = add_expense(data)
        elif choice == '3':
            data = edit_expense(data)
        elif choice == '4':
            pdf_file = input("Enter the path to the PDF file: ")
            data = upload_expenses_from_pdf(data, pdf_file)
        elif choice == '5':
            write_budget(BUDGET_FILE, data)
            print("Budget saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()