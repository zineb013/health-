import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFrame, 
                             QStackedWidget, QLineEdit, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class BioGrowthApp(QMainWindow):
    def __init__(self):
        super().__init__()
       self.setWindowTitle("PediatricHealthEngine - Dynamic Child Growth & Health Tracker")
        self.setGeometry(100, 100, 1100, 720)
        self.setStyleSheet("background-color: #f8fafc;")

        # Dynamic Variables
        self.reset_data()

        self.initUI()

    def reset_data(self):
        """Reset all values to initial state"""
        self.patient_name = "Child 1"
        self.age = 10
        self.weight = 30.0 # kg
        self.height = 135.0 # cm
        self.bmi = 0.0
        self.water_needs = 0.0
        self.calories_needs = 0
        self.sleep_hours = ""
        self.max_sugar = ""
        self.screen_time = ""

    def initUI(self):
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---------------- 1. SIDEBAR MENU ----------------
        sidebar = QFrame(self)
        sidebar.setFixedWidth(230)
        sidebar.setStyleSheet("background-color: #0284c7;") # Medical Blue
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 25, 15, 25)

        brand = QLabel("PediatricHealthEngine", sidebar)
        brand.setFont(QFont("Segoe UI", 18, QFont.Bold))
        brand.setStyleSheet("color: #ffffff; margin-bottom: 30px;")
        brand.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(brand)

        self.btn_page1 = QPushButton(" Child Input Data", sidebar)
        self.btn_page2 = QPushButton(" Growth & Lifestyle", sidebar)
        self.btn_page3 = QPushButton(" Health Report", sidebar)

        menu_style = """
            QPushButton {
                color: #e0f2fe;
                background-color: transparent;
                text-align: left;
                padding: 14px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0369a1;
                color: #ffffff;
            }
        """
        for btn in (self.btn_page1, self.btn_page2, self.btn_page3):
            btn.setStyleSheet(menu_style)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Reset Button in Sidebar
        self.btn_reset = QPushButton(" Reset / New Child", sidebar)
        self.btn_reset.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                font-size: 13px;
                font-weight: bold;
                padding: 12px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        self.btn_reset.clicked.connect(self.clear_all_data)
        sidebar_layout.addWidget(self.btn_reset)

        main_layout.addWidget(sidebar)

        # ---------------- 2. PAGES (STACKED WIDGET) ----------------
        self.pages = QStackedWidget(self)
        main_layout.addWidget(self.pages)

        self.create_input_page()
        self.create_metrics_page()
        self.create_report_page()

        self.btn_page1.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.btn_page2.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.btn_page3.clicked.connect(lambda: self.pages.setCurrentIndex(2))

    # ---------------- PAGE 1: CHILD INPUT DATA ----------------
    def create_input_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 30, 40, 30)

        title = QLabel("Child Growth & Comprehensive Health Assessment", page)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #0f172a;")

        desc = QLabel("Enter child's measurements to dynamically calculate BMI, calories, water, sleep, max sugar, and screen time limits.", page)
        desc.setFont(QFont("Segoe UI", 11))
        desc.setStyleSheet("color: #64748b;")
        desc.setWordWrap(True)

        # Form Inputs
        self.input_name = QLineEdit(page)
        self.input_name.setPlaceholderText("Child Name ")
        
        self.input_age = QLineEdit(page)
        self.input_age.setPlaceholderText("Age (years)")

        self.input_weight = QLineEdit(page)
        self.input_weight.setPlaceholderText("Weight (kg)")

        self.input_height = QLineEdit(page)
        self.input_height.setPlaceholderText("Height (cm)")

        field_style = "padding: 12px; border: 1px solid #cbd5e1; border-radius: 8px; background: white; font-size: 14px;"
        for field in (self.input_name, self.input_age, self.input_weight, self.input_height):
            field.setStyleSheet(field_style)

        btn_save = QPushButton("Process Child Health Profile", page)
        btn_save.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_save.setStyleSheet("background-color: #0284c7; color: white; padding: 14px; border-radius: 8px;")
        btn_save.clicked.connect(self.process_profile)

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addSpacing(15)
        layout.addWidget(self.input_name)
        layout.addWidget(self.input_age)
        layout.addWidget(self.input_weight)
        layout.addWidget(self.input_height)
        layout.addSpacing(15)
        layout.addWidget(btn_save)
        layout.addStretch()
        self.pages.addWidget(page)

    def process_profile(self):
        if self.input_name.text():
            self.patient_name = self.input_name.text()
        try:
            self.age = float(self.input_age.text()) if self.input_age.text() else 10
            self.weight = float(self.input_weight.text()) if self.input_weight.text() else 30.0
            self.height = float(self.input_height.text()) if self.input_height.text() else 135.0
        except ValueError:
            pass

        self.lbl_active_patient.setText(f"Active Child Profile: {self.patient_name} ({int(self.age)} yrs)")
        self.pages.setCurrentIndex(1)

    # ---------------- PAGE 2: GROWTH & LIFESTYLE ----------------
    def create_metrics_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 30, 40, 30)

        self.lbl_active_patient = QLabel(f"Active Child Profile: {self.patient_name}", page)
        self.lbl_active_patient.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.lbl_active_patient.setStyleSheet("color: #0f172a;")

        btn_compute = QPushButton("Calculate Dynamic Health & Lifestyle Plan", page)
        btn_compute.setFont(QFont("Segoe UI", 13, QFont.Bold))
        btn_compute.setStyleSheet("background-color: #10b981; color: white; padding: 14px; border-radius: 8px;")
        btn_compute.clicked.connect(self.calculate_metrics)

        layout.addWidget(self.lbl_active_patient)
        layout.addSpacing(10)
        layout.addWidget(btn_compute)
        layout.addSpacing(20)

        # GRID LAYOUT FOR CARDS
        grid = QGridLayout()
        grid.setSpacing(20)

        self.card_bmi = QLabel("⚖️ Body Mass Index (BMI)\n-- kg/m²", page)
        self.card_calories = QLabel("⚡ Estimated Daily Energy\n-- kcal/day", page)
        self.card_water = QLabel("💧 Daily Water Intake\n-- L/day", page)
        self.card_sleep = QLabel("🌙 Sleep Duration\n-- Hours/night", page)
        self.card_sugar = QLabel("🍬 Max Added Sugar Limit\n--", page)
        self.card_screen = QLabel("📱 Max Screen Time\n--", page)

        card_style = """
            QLabel {
                background-color: #ffffff;
                border: 2px solid #e2e8f0;
                padding: 20px;
                border-radius: 12px;
                font-size: 15px;
                font-weight: bold;
                color: #0f172a;
            }
        """
        cards = [self.card_bmi, self.card_calories, self.card_water, 
                 self.card_sleep, self.card_sugar, self.card_screen]

        positions = [(0,0), (0,1), (1,0), (1,1), (2,0), (2,1)]

        for card, pos in zip(cards, positions):
            card.setStyleSheet(card_style)
            card.setAlignment(Qt.AlignCenter)
            grid.addWidget(card, pos[0], pos[1])

        layout.addLayout(grid)
        layout.addStretch()
        self.pages.addWidget(page)

    def calculate_metrics(self):
        height_m = self.height / 100.0
        self.bmi = round(self.weight / (height_m ** 2), 2)

        if self.age <= 5:
            self.calories_needs = int(self.weight * 60)
        elif self.age <= 12:
            self.calories_needs = int(self.weight * 50)
        else:
            self.calories_needs = int(self.weight * 40)

        self.water_needs = round((self.weight * 35) / 1000.0, 2)

        if self.age <= 5:
            self.sleep_hours = "10 - 13 Hours"
        elif self.age <= 12:
            self.sleep_hours = "9 - 12 Hours"
        else:
            self.sleep_hours = "8 - 10 Hours"

        if self.age <= 5:
            self.max_sugar = "Less than 19g / day"
            self.screen_time = "Max 1 Hour / day"
        else:
            self.max_sugar = "Less than 25g / day"
            self.screen_time = "Max 2 Hours / day"

        self.card_bmi.setText(f"⚖️ Body Mass Index (BMI)\n\n{self.bmi} kg/m²")
        self.card_calories.setText(f"⚡ Estimated Daily Energy\n\n~{self.calories_needs} kcal/day")
        self.card_water.setText(f"💧 Daily Water Intake\n\n{self.water_needs} Liters/day")
        self.card_sleep.setText(f"🌙 Sleep Duration\n\n{self.sleep_hours}")
        self.card_sugar.setText(f"🍬 Max Added Sugar Limit\n\n{self.max_sugar}")
        self.card_screen.setText(f"📱 Max Screen Time\n\n{self.screen_time}")

        self.update_report_table()

    # ---------------- PAGE 3: ENHANCED HEALTH REPORT TABLE ----------------
    def create_report_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(35, 30, 35, 30)

        title = QLabel("Pediatric Health & Growth Summary Report", page)
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #0f172a;")
        layout.addWidget(title)

        # Overview Header
        summary_box = QHBoxLayout()
        self.lbl_rep_name = QLabel("Child Profile: --", page)
        self.lbl_rep_status = QLabel("Overall Status: --", page)
        
        sum_style = "background-color: #e0f2fe; color: #0369a1; padding: 12px 22px; border-radius: 8px; font-weight: bold; font-size: 15px;"
        self.lbl_rep_name.setStyleSheet(sum_style)
        self.lbl_rep_status.setStyleSheet(sum_style)
        
        summary_box.addWidget(self.lbl_rep_name)
        summary_box.addWidget(self.lbl_rep_status)
        summary_box.addStretch()
        layout.addLayout(summary_box)
        layout.addSpacing(15)

        # FULLY EXPANDED AND LARGE TABLE
        self.table = QTableWidget(0, 7, page)
        self.table.setHorizontalHeaderLabels(["Child Name", "BMI", "Calories", "Water Need", "Sleep Target", "Growth Status", "Detailed Parent Advice"])
        
        # Style Header and Cells with Larger Fonts & Clear Paddings
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                gridline-color: #cbd5e1;
                border: 2px solid #cbd5e1;
                border-radius: 10px;
                font-size: 14px;
                color: #0f172a;
            }
            QHeaderView::section {
                background-color: #0284c7;
                color: white;
                padding: 14px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QTableWidget::item {
                padding: 15px;
            }
        """)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.Stretch)
        
        self.table.setWordWrap(True)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        # Bottom Summary Cards to Fill Extra Page Height
        layout.addSpacing(15)
        cards_layout = QHBoxLayout()

        self.box_calories = QLabel("⚡ Calories Target\n-- kcal", page)
        self.box_water = QLabel("💧 Water Target\n-- L/day", page)
        self.box_sleep = QLabel("🌙 Sleep Target\n-- Hours", page)

        box_style = """
            QLabel {
                background-color: #ffffff;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 18px;
                font-size: 15px;
                font-weight: bold;
                color: #0f172a;
            }
        """
        for box in (self.box_calories, self.box_water, self.box_sleep):
            box.setStyleSheet(box_style)
            box.setAlignment(Qt.AlignCenter)
            cards_layout.addWidget(box)

        layout.addLayout(cards_layout)
        self.pages.addWidget(page)

    def update_report_table(self):
        self.table.setRowCount(0)
        row = self.table.rowCount()
        self.table.insertRow(row)

        if self.bmi < 18.5:
            growth_status = "Underweight Range"
            advice = f"Focus: Provide protein-dense meals (~{self.calories_needs} kcal/day). Limit screen time ({self.screen_time}) and ensure {self.sleep_hours} sleep."
        elif self.bmi <= 24.9:
            growth_status = "Healthy Balance"
            advice = f"Excellent Balance: Maintain active play (60 mins/day), restrict added sugars ({self.max_sugar}), limit screens ({self.screen_time}), and drink {self.water_needs}L water daily."
        else:
            growth_status = "Above Average Weight"
            advice = f"Action Plan: Encourage outdoor active games, reduce sugary drinks ({self.max_sugar}), limit screens ({self.screen_time}), and stay hydrated."

        self.lbl_rep_name.setText(f"Child Profile: {self.patient_name} ({int(self.age)} yrs)")
        self.lbl_rep_status.setText(f"Overall Status: {growth_status}")

        self.box_calories.setText(f"⚡ Energy Target\n\n{self.calories_needs} kcal/day")
        self.box_water.setText(f"💧 Water Target\n\n{self.water_needs} Liters/day")
        self.box_sleep.setText(f"🌙 Sleep Target\n\n{self.sleep_hours}")

        items = [
            self.patient_name,
            f"{self.bmi} kg/m²",
            f"{self.calories_needs} kcal",
            f"{self.water_needs} L/day",
            self.sleep_hours,
            growth_status,
            advice
        ]

        for col, text in enumerate(items):
            item = QTableWidgetItem(text)
            if col != 6:
                item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, col, item)

        self.table.setRowHeight(row, 110) # Height increased for maximum clarity

    def clear_all_data(self):
        """Reset all data to empty state"""
        self.reset_data()
        
        self.input_name.clear()
        self.input_age.clear()
        self.input_weight.clear()
        self.input_height.clear()

        self.lbl_active_patient.setText("Active Child Profile: Child 1")
        
        self.card_bmi.setText("⚖️ Body Mass Index (BMI)\n-- kg/m²")
        self.card_calories.setText("⚡ Estimated Daily Energy\n-- kcal/day")
        self.card_water.setText("💧 Daily Water Intake\n-- L/day")
        self.card_sleep.setText("🌙 Sleep Duration\n-- Hours/night")
        self.card_sugar.setText("🍬 Max Added Sugar Limit\n--")
        self.card_screen.setText("📱 Max Screen Time\n--")

        self.lbl_rep_name.setText("Child Profile: --")
        self.lbl_rep_status.setText("Overall Status: --")
        self.box_calories.setText("⚡ Calories Target\n-- kcal")
        self.box_water.setText("💧 Water Target\n-- L/day")
        self.box_sleep.setText("🌙 Sleep Target\n-- Hours")
        self.table.setRowCount(0)

        self.pages.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BioGrowthApp()
    window.show()
    sys.exit(app.exec_())
