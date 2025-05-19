
import csv
from fpdf import FPDF

# Step 1: Read CSV data
def read_data(filename):
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

# Step 2: Analyze Data
def analyze_data(data):
    total_sales = 0
    department_sales = {}
    for row in data:
        sales = int(row['Sales'])
        total_sales += sales
        dept = row['Department']
        department_sales[dept] = department_sales.get(dept, 0) + sales

    average_sales = total_sales / len(data) if data else 0
    return total_sales, average_sales, department_sales

# Step 3: Generate PDF Report
class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Automated Report Generation", border=False, ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_summary(self, total, average, dept_sales):
        self.set_font("Arial", size=12)
        self.cell(0, 10, f"Total Sales: {total}", ln=True)
        self.cell(0, 10, f"Average Sales per Person: {average:.2f}", ln=True)
        self.ln(5)

        self.cell(0, 10, "Sales by Department:", ln=True)
        for dept, amount in dept_sales.items():
            self.cell(0, 10, f" - {dept}: {amount}", ln=True)

    def add_table(self, data):
        self.ln(10)
        self.set_font("Arial", "B", 12)
        self.cell(50, 10, "Name", border=1)
        self.cell(50, 10, "Department", border=1)
        self.cell(50, 10, "Sales", border=1)
        self.ln()

        self.set_font("Arial", size=12)
        for row in data:
            self.cell(50, 10, row["Name"], border=1)
            self.cell(50, 10, row["Department"], border=1)
            self.cell(50, 10, row["Sales"], border=1)
            self.ln()

# Main Execution
if __name__ == "__main__":
    data = read_data("data.csv")
    total, average, dept_sales = analyze_data(data)

    pdf = PDFReport()
    pdf.add_page()
    pdf.add_summary(total, average, dept_sales)
    pdf.add_table(data)

    pdf.output("output_report.pdf")
    print("Report generated successfully as output_report.pdf")
