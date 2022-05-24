import json
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
	QDialog, 
	QApplication,
	QFileDialog,
	QFrame,
	QMainWindow,
	QPushButton, 
	QHBoxLayout,
	QVBoxLayout, 
	QFormLayout,
	QLineEdit,
	QWidget
)
import random
import sys
from ui_functions.load import load_clicked
from ui_functions.save import save_clicked
from utils.value_generator import normal_distribution, plot_histogram

class MyWindow(QMainWindow):
	def __init__(self):
		super(MyWindow,self).__init__()
		self.initUI()

	'''
	Actions called by the 'Save' and 'Load' buttons. Defined in ./ui_functions
	'''
	def save(self):
		save_clicked(self)

	def load(self):
		load_clicked(self)
	
	# action called by the plot button
	def plot(self):
		
		# random data
		chart_data = normal_distribution(25, 5, 5000)

		# clearing old figure
		self.figure.clear()

		# plotting as a histogram
		plot_histogram(chart_data, "variation")

		# refresh canvas
		self.canvas.draw()

	def initUI(self):
		self.outerLayout = QVBoxLayout()
		self.topLayout = QVBoxLayout()

		'''
		Save and Load buttons
		'''
		self.saveLayout = QHBoxLayout()
		self.save_button = (QPushButton("Save"))
		self.saveLayout.addWidget(self.save_button)
		self.save_button.clicked.connect(self.save)
		self.load_button = (QPushButton("Load"))
		self.saveLayout.addWidget(self.load_button)
		self.load_button.clicked.connect(self.load)
		
		'''
		Primary variables
		Loads initial values from default.json
		'''
		try:
			with open('saves/default.json', 'r') as default_file:
				d = json.load(default_file)
				d_sdk = str(d['sdk_key'])
				d_api = str(d['api_key'])
				d_proj = str(d['proj_key'])
				d_flag = str(d['flag_key'])
				d_metric = str(d['metric_key'])
				d_iterations = str(d['iterations'])
		except:
			d_sdk, d_api, d_proj, d_flag, d_metric, d_iterations = '', '', '', '', '', ''


		self.formLayout = QFormLayout()
		self.formLayout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
		self.sdk_key = QLineEdit()
		self.sdk_key.setText(d_sdk)
		self.formLayout.addRow("SDK Key:", self.sdk_key)
		self.api_key = QLineEdit()
		self.api_key.setText(d_api)
		self.formLayout.addRow("API Key:", self.api_key)
		self.proj_key = QLineEdit()
		self.proj_key.setText(d_proj)
		self.formLayout.addRow("Project Key:", self.proj_key)
		self.flag_key = QLineEdit()
		self.flag_key.setText(d_flag)
		self.formLayout.addRow("Flag Key:", self.flag_key)
		self.metric_key = QLineEdit()
		self.metric_key.setText(d_metric)
		self.formLayout.addRow("Metric Key:", self.metric_key)
		self.iterations = QLineEdit()
		self.iterations.setText(d_iterations)
		self.formLayout.addRow("Iterations:", self.iterations)

		'''
		Variation list, mean values, and spread
		'''
		self.bottomLayout = QHBoxLayout()
		self.bottomFormLayout = QFormLayout()
		self.newButton = QPushButton('Get Variations')
		self.bottomFormLayout.addWidget(self.newButton)
		self.variation1 = self.bottomFormLayout.addRow("Variation1:", QLineEdit())

		'''
		Chart
		'''
		self.chartLayout = QVBoxLayout()
		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)
		self.chartLayout.addWidget(self.canvas)
		self.toolbar = NavigationToolbar(self.canvas, self)
		self.chartLayout.addWidget(self.toolbar)
		self.chart_button = QPushButton('Plot')
		self.chartLayout.addWidget(self.chart_button)
		self.chart_button.clicked.connect(self.plot)

		'''
		Construct layouts
		'''
		self.outerLayout.addLayout(self.topLayout)
		self.topLayout.addLayout(self.saveLayout)
		self.topLayout.addLayout(self.formLayout)
		
		self.outerLayout.addLayout(self.bottomLayout)
		self.bottomLayout.addLayout(self.bottomFormLayout)
		self.bottomLayout.addLayout(self.chartLayout)

		widget = QWidget()
		widget.setLayout(self.outerLayout)
		self.setCentralWidget(widget)
	

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()