from abc import ABC, abstractmethod
import argparse
from datetime import datetime
import json, os,csv, io

class Expense:
	counter_id = 1
	def __init__(self, category, description, amount) -> None:
		self.id = Expense.counter_id
		Expense.counter_id += 1
		self.created_at = None
		self.description = description
		self.amount = amount
		self.category = category
		self.created_at = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		self.updated_at = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
	
	def __str__(self) -> str:
		return (f"[{self.id}] {self.category} | {self.description} | "
				f"${self.amount:.2f} | {self.created_at} | {self.updated_at}")
	
	def to_dict(self):
		return {
			"id": self.id,
			"category": self.category,
			"description": self.description,
			"amount": self.amount,
			"created_at": self.created_at,
			"updated_at": self.updated_at
		}
	
	@classmethod
	def from_dict(cls, data):
		expense = cls(data["category"], data["description"], data["amount"]) #creo una instancia de la clase cls
		expense.id = int(data["id"])
		expense.created_at = data["created_at"]
		expense.updated_at = data['updated_at']
		return expense
	
class ReportGenerator(ABC):
	@abstractmethod
	def generate(self, expenses:dict) -> str:
		pass

class JSONReportGenerator(ReportGenerator):
	def generate(self, expenses: dict): 
		return json.dumps(expenses,indent=2)

class ReportWriter(ABC):
	@abstractmethod
	def write(self,report:str, filename:str='expenses'):
		pass

class JSONReportWriter(ReportWriter):
	def write(self, report: str, filename: str = 'expenses'):
		try:
			with open(f"{filename}.json", 'w') as f:
				f.write(report)		
			print(f"Report saved to {filename}.json")
		except IOError:
			print("Error: Could not save report")

class ExpenseManager:
	def __init__(self, report_generator:ReportGenerator, report_writer:ReportWriter):
		self.expenses = {}
		self.report_generator = report_generator
		self.report_writer = report_writer
		if os.path.exists("expenses.json"):
			with open("expenses.json", 'r') as f:
				expense_dict = json.load(f)
				for expense_id,expense_data in expense_dict.items():
					self.expenses[int(expense_id)] = Expense.from_dict(expense_data)
			if self.expenses:
				Expense.counter_id = max(self.expenses.keys())+1
			else:
				Expense.counter_id = 1
			#print(f"Expense counter_id set to {Expense.counter_id}")

	def add_expense(self,category,description,amount):
		expense = Expense(category,description,amount)
		self.expenses[expense.id] = expense
		self.save_expense()
		print(f"Expense added Succesfully (ID: {expense.id})")
	
	def save_expense(self):
		with open("expenses.json", 'w') as f:
			json.dump(self.to_json_dict(), f, indent=2)

	def list_expenses(self):
		if not self.expenses:
			print('no expenses found.')
			return
		print('all expenses')
		for expense in self.expenses.values():
			print(expense)

	def filter_expenses(self,category:str):
		if not category:
			raise ValueError("missed category argument")
		for expense in self.expenses.values():
			if category == expense.category:
				print(expense)

	def delete_expense(self, expense_id:int):
		if expense_id in self.expenses:
			del self.expenses[expense_id]
			self.save_expense()
			print(f"Expense ID {expense_id} was deleted")
		else:
			print(f"Expense {expense_id} not found")

	def update_expense(self, expense_id:int, description:str, amount:float):
		if expense_id in self.expenses:
			if description:
				self.expenses[expense_id].description = description
			if amount:
				self.expenses[expense_id].amount = amount
			self.expenses[expense_id].updated_at = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
			self.save_expense()
			print(f"Expense ID:{expense_id} was updated at {self.expenses[expense_id].updated_at}")
	
	def summary_expenses(self, month:int):
		total = 0
		total_by_month = 0

		if month:
			month_name = datetime.strptime(str(month),"%m").strftime("%B")
			for expense in self.expenses.values():
				expense_month = int(expense.created_at[5:7])
				if month == expense_month:
					total_by_month += expense.amount
			print(f"Total Expenses for {month_name}: ${total_by_month:.2f}")
		else:
			for expense in self.expenses.values():
				total += expense.amount
			print(f"Total expenses: ${total:.2f}")

	def to_json_dict(self):
		expense_list = {str(expense_id):expense.to_dict()
		for expense_id,expense in self.expenses.items()}
		return expense_list

	def generate_report(self):
		report = self.report_generator.generate(self.to_json_dict())
		self.report_writer.write(report)

	def export_to_csv(self, filename:str = 'expenses'):
		try:
			with open(f"{filename}.csv", 'w', newline='') as f:
				writer = csv.DictWriter(f, fieldnames=["id", "category","description","amount","created_at","updated_at"])
				writer.writeheader()
				for expense in self.expenses.values():
					writer.writerow(expense.to_dict())
			print(f"Expenses exported to {filename}.csv")
		except IOError:
			print("Error: Could not export to CSV")
		
def main():

	client = ExpenseManager(JSONReportGenerator(),JSONReportWriter())

	parser = argparse.ArgumentParser(description="Expense Tracker APP CLI")
	subparsers = parser.add_subparsers(dest='command', help='Sub-commands')

	#parser for add command
	parser_add = subparsers.add_parser('add', help='Add a new expense')
	parser_add.add_argument('-c','--category', required=True, type=str, help='Category of expense')
	parser_add.add_argument('-d','--description', required=True, type=str, help='Description of expense')
	parser_add.add_argument('-a','--amount', required=True, type=float, help='Amount of the expense')

	parser_list = subparsers.add_parser('list', help="list all expenses")

	#parser for delete
	parser_delete = subparsers.add_parser('delete', help='Delete an expense')
	parser_delete.add_argument('id', type=int, help="ID of expense to delete")

	#parser for update
	parser_update  = subparsers.add_parser('update', help='update an expense')
	parser_update.add_argument('id', type=int, help='ID of expense')
	parser_update.add_argument('-d','--description', type=str, help="Expense Description")
	parser_update.add_argument('-a','--amount', type=str, help='Expense amount')

	#parser for summary
	parser_summary = subparsers.add_parser('summary', help='Expenses Summary')
	parser_summary.add_argument('--month', type=int, help='Expenses Summary by Month')

	#parser for filter
	parser_filter = subparsers.add_parser('filter', help='Filter by Category')
	parser_filter.add_argument('-c', '--category', type=str, help='Expense by category')

	#parser export to csv
	parser_export = subparsers.add_parser('export', help='Export to CSV')
	parser_export.add_argument('-f', '--filename', type=str, default='expenses', help='Output to CSV')


	args = parser.parse_args()

	
	match args.command:
		case 'add':
			#Implement add expense logic
			client.add_expense(args.category, args.description, args.amount)
		case 'list':
			#Implement list expenses logic
			client.list_expenses()
		case 'delete':
			#Implement delete expense logic
			client.delete_expense(args.id)
		case 'update':
			client.update_expense(args.id,args.description,float(args.amount))
		case 'summary':
			client.summary_expenses(args.month)
		case 'filter':
			client.filter_expenses(args.category)
		case 'export':
			client.export_to_csv(args.filename)
		case _:
			parser.print_help()

if __name__ == "__main__":
	main()
