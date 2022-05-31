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
from ui_functions.variations import get_variations_clicked, load_variations
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

	'''
	Auto save on close
	'''
	def closeEvent(self, event):
		self.save()

	'''
	Get variations and populate fields
	'''
	def get_variations(self):
		get_variations_clicked(self)

	
	# action called by the plot button
	def plot(self):
		
		# random data
		normal_example = normal_distribution(25, 5, 5000)
		another_normal_example = normal_distribution(30, 5, 5000)
		yet_another_normal_example = normal_distribution(40, 5, 5000)
		and_another_normal_example = normal_distribution(50, 10, 5000)

		# clearing old figure
		self.figure.clear()

		# plotting as a histogram
		plot_histogram(normal_example, "gray")
		plot_histogram(another_normal_example, "blue")
		plot_histogram(yet_another_normal_example, "purple")
		plot_histogram(and_another_normal_example, "red")

		# refresh canvas
		self.canvas.draw()

	'''
	Draw the UI
	'''
	def initUI(self):
		'''
		Layouts
		'''
		self.outerLayout = QVBoxLayout()
		self.topLayout = QVBoxLayout()
		self.saveLayout = QHBoxLayout()
		self.formLayout = QFormLayout()
		self.formLayout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
		self.bottomLayout = QHBoxLayout()
		self.bottomFormLayout = QFormLayout()
		self.chartLayout = QVBoxLayout()
		self.footerLayout = QVBoxLayout()

		'''
		Save and Load buttons
		'''
		self.save_button = (QPushButton("Save"))
		self.load_button = (QPushButton("Load"))
		self.saveLayout.addWidget(self.save_button)
		self.saveLayout.addWidget(self.load_button)
		self.save_button.clicked.connect(self.save)
		self.load_button.clicked.connect(self.load)
		
		'''
		Variation list, mean values, and spread
		'''
		self.variations_button = QPushButton('Get Variations')
		self.bottomFormLayout.addWidget(self.variations_button)
		self.variations_button.clicked.connect(self.get_variations)

		'''
		Load initial values from default.json
		'''
		try:
			with open('saves/default.json', 'r') as default_file:
				d = json.load(default_file)
				d_sdk = str(d['sdk_key'])
				d_api = str(d['api_key'])
				d_proj = str(d['proj_key'])
				d_flag = str(d['flag_key'])
				d_metric = str(d['metric_key'])
				d_events = str(d['events'])

				load_variations(self, d)

		except:
			d_sdk, d_api, d_proj, d_flag, d_metric, d_events = '', '', '', '', '', ''

		'''
		Primary fields
		'''
		self.sdk_key = QLineEdit()
		self.api_key = QLineEdit()
		self.proj_key = QLineEdit()
		self.flag_key = QLineEdit()
		self.metric_key = QLineEdit()
		self.events = QLineEdit()
		self.sdk_key.setText(d_sdk)
		self.api_key.setText(d_api)
		self.proj_key.setText(d_proj)
		self.flag_key.setText(d_flag)
		self.metric_key.setText(d_metric)
		self.events.setText(d_events)
		self.formLayout.addRow("SDK Key:", self.sdk_key)
		self.formLayout.addRow("API Key:", self.api_key)
		self.formLayout.addRow("Project Key:", self.proj_key)
		self.formLayout.addRow("Flag Key:", self.flag_key)
		self.formLayout.addRow("Metric Key:", self.metric_key)
		self.formLayout.addRow("Events:", self.events)


		'''
		Chart
		'''
		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)
		self.chartLayout.addWidget(self.canvas)
		self.toolbar = NavigationToolbar(self.canvas, self)
		self.chartLayout.addWidget(self.toolbar)
		self.chart_button = QPushButton('Preview')
		self.chartLayout.addWidget(self.chart_button)
		self.chart_button.clicked.connect(self.plot)

		'''
		Send to LD
		'''
		self.send_button = QPushButton('Run Experiments')
		self.footerLayout.addWidget(self.send_button)

		'''
		Construct layouts
		'''
		# Top
		self.outerLayout.addLayout(self.topLayout)
		self.topLayout.addLayout(self.saveLayout)
		self.topLayout.addLayout(self.formLayout)
		
		# Bottom
		self.outerLayout.addLayout(self.bottomLayout)
		self.bottomLayout.addLayout(self.bottomFormLayout)
		self.bottomLayout.addLayout(self.chartLayout)

		# Footer
		self.outerLayout.addLayout(self.footerLayout)

		widget = QWidget()
		widget.setLayout(self.outerLayout)
		self.setCentralWidget(widget)
	

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()