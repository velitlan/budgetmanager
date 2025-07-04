import csv
import os
from collections import defaultdict

FIELDNAMES = ['date', 'amount', 'category', 'description']

class Transaction:
    def __init__(self, date, amount, category, description):
        self.date = date
        self.amount = float(amount)
        self.category = category
        self.description = description

    def to_dict(self):
        return {
            'date': self.date,
            'amount': self.amount,
            'category': self.category,
            'description': self.description
        }

class BudgetManager:
    def __init__(self, file_path='transactions.csv'):
        self.file_path = file_path
        self.transactions = self.load_transactions()

    def load_transactions(self):
        transactions = []
        if os.path.exists(self.file_path):
            with open(self.file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        transactions.append(Transaction(
                            row['date'], row['amount'], row['category'], row['description']
                        ))
                    except KeyError:
                        continue 
        return transactions

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        write_header = not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0
        with open(self.file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
            if write_header:
                writer.writeheader()
            writer.writerow(transaction.to_dict())

    def get_summary(self):
        income = sum(t.amount for t in self.transactions if t.amount > 0)
        expenses = sum(t.amount for t in self.transactions if t.amount < 0)
        return income, expenses, income + expenses

    def get_by_category(self):
        categories = defaultdict(float)
        for t in self.transactions:
            categories[t.category] += t.amount
        return categories

def main():
    manager = BudgetManager()

    while True:
        print("\n1 - Neue Transaktion")
        print("2 - Budgetübersicht")
        print("3 - Ausgaben nach Kategorie")
        print("4 - Beenden")

        choice = input("Auswahl: ").strip()

        if choice == '1':
            date = input("Datum (YYYY-MM-DD): ").strip()
            try:
                amount = float(input("Betrag (+ Einnahme / - Ausgabe): ").strip())
            except ValueError:
                print("Ungültiger Betrag.")
                continue
            category = input("Kategorie: ").strip()
            description = input("Beschreibung: ").strip()
            t = Transaction(date, amount, category, description)
            manager.add_transaction(t)
            print("Transaktion gespeichert.")

        elif choice == '2':
            income, expenses, balance = manager.get_summary()
            print(f"Einnahmen: {income:.2f}")
            print(f"Ausgaben: {expenses:.2f}")
            print(f"Bilanz: {balance:.2f}")

        elif choice == '3':
            categories = manager.get_by_category()
            for cat, total in categories.items():
                print(f"{cat}: {total:.2f}")

        elif choice == '4':
            print("Programm beendet.")
            break

        else:
            print("Ungültige Eingabe.")

if __name__ == "__main__":
    main()