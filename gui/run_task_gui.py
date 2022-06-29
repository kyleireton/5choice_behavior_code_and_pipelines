import time
from datetime import timedelta
import statistics
import os
import sys, csv
from gui import Ui_MainWindow
from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtGui, QtCore
from datetime import datetime
from serial import SerialException
from serial.tools import list_ports

# Add parent directory to path to allow imports.
top_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not top_dir in sys.path: sys.path.insert(0, top_dir)

from com.pycboard import Pycboard, PyboardError, _djb2_file
from com.data_logger import Data_logger

from config.paths import data_dir, tasks_dir
from config.gui_settings import update_interval

from dialogs import Board_config_dialog_1, Board_config_dialog_2, \
    Board_config_dialog_3, Board_config_dialog_4, \
    Board_config_dialog_5, Board_config_dialog_6, \
    Board_config_dialog_7, Board_config_dialog_8, Variables_dialog

# from plotting import Task_plotter

# Run_task_gui ------------------------------------------------------------------------

# Create widgets.


def gui_excepthook(error_type, error_msg, traceback):
    sys.__excepthook__(error_type, error_msg, traceback)


sys.excepthook = gui_excepthook


class MainGui(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('5-Choice_Serial_Reaction_Test')
        self.setFixedSize(1800, 400)
        # Variables.
        #self.board = None
        #self.text_edit_widget = None
        self.board_1 = None  # Pycboard class instance.
        self.board_2 = None  # Pycboard class instance.
        self.board_3 = None  # Pycboard class instance.
        self.board_4 = None  # Pycboard class instance.
        self.task = None  # Pycboard class instance.
        self.task_1 = None  # Task currently uploaded on pyboard.
        self.task_2 = None  # Task currently uploaded on pyboard.
        self.task_3 = None  # Task currently uploaded on pyboard.
        self.task_4 = None  # Task currently uploaded on pyboard.
         # Task currently uploaded on pyboard.
        self.task_hash_1 = None  # Used to check if file has changed.
        self.task_hash_2 = None  # Used to check if file has changed.
        self.task_hash_3 = None  # Used to check if file has changed.
        self.task_hash_4 = None  # Used to check if file has changed.
         # Used to check if file has changed.
        self.sm_info_1 = None  # Information about current state machine.
        self.sm_info_2 = None  # Information about current state machine.
        self.sm_info_3 = None  # Information about current state machine.
        self.sm_info_4 = None  # Information about current state machine.
         #Information about current state machine.
        self.data_dir = None  # data directory
        self.subject_id_1 = None
        self.subject_id_2 = None
        self.subject_id_3 = None
        self.subject_id_4 = None

        self.exp_name = None  # experimenter name
        self.project = None

        self.data_logger1 = Data_logger(print_func=self.print_to_log)
        self.data_logger2 = Data_logger(print_func=self.print_to_log)
        self.data_logger3 = Data_logger(print_func=self.print_to_log)
        self.data_logger4 = Data_logger(print_func=self.print_to_log)

        self.connected_1 = False  # Whether gui is connected to pyboard.
        self.connected_2 = False  # Whether gui is connected to pyboard.
        self.connected_3 = False  # Whether gui is connected to pyboard.
        self.connected_4 = False  # Whether gui is connected to pyboard.

        self.uploaded_1 = False  # Whether selected task is on board.
        self.uploaded_2 = False  # Whether selected task is on board.
        self.uploaded_3 = False  # Whether selected task is on board.
        self.uploaded_4 = False  # Whether selected task is on board.

        self.subject_changed = False
        self.available_tasks = None
        self.available_ports = None
        #self.showlcd()
        self.refresh_interval = 1000  # Interval to refresh tasks and ports when not running (ms).
        # Buttons for connect teh gui to pyboards
        self.pushButton_connect_1.clicked.connect(
            lambda: self.disconnect_1() if self.connected_1 else self.connect_1())
        self.pushButton_connect_2.clicked.connect(
            lambda: self.disconnect_2() if self.connected_2 else self.connect_2())
        self.pushButton_connect_3.clicked.connect(
            lambda: self.disconnect_3() if self.connected_3 else self.connect_3())
        self.pushButton_connect_4.clicked.connect(
            lambda: self.disconnect_4() if self.connected_4 else self.connect_4())

        self.exportdata.clicked.connect(lambda: self.save_file())
        self.Exportdata2.clicked.connect(lambda: self.save_file())
        self.resettable.clicked.connect(lambda: self.items_clear())

        self.pushButton_config_1.clicked.connect(
            lambda: self.Board_config_dialog_1.exec_())
        self.pushButton_config_2.clicked.connect(
            lambda: self.Board_config_dialog_2.exec_())
        self.pushButton_config_3.clicked.connect(
            lambda: self.Board_config_dialog_3.exec_())
        self.pushButton_config_4.clicked.connect(
            lambda: self.Board_config_dialog_4.exec_())

        self.pushButton_data_dir.clicked.connect(self.select_data_dir)
        self.pushButton_upload_1.clicked.connect(lambda: self.setup_task_1())
        self.pushButton_upload_2.clicked.connect(lambda: self.setup_task_2())
        self.pushButton_upload_3.clicked.connect(lambda: self.setup_task_3())
        self.pushButton_upload_4.clicked.connect(lambda: self.setup_task_4())

        self.pushButton_var1.clicked.connect(lambda x: self.variables_dialog_1.exec_())
        self.pushButton_var2.clicked.connect(lambda x: self.variables_dialog_2.exec_())
        self.pushButton_var3.clicked.connect(lambda x: self.variables_dialog_3.exec_())
        self.pushButton_var4.clicked.connect(lambda x: self.variables_dialog_4.exec_())

        self.pushButton_Start1.clicked.connect(lambda: self.start_task_1())
        self.pushButton_Start2.clicked.connect(lambda: self.start_task_2())
        self.pushButton_Start3.clicked.connect(lambda: self.start_task_3())
        self.pushButton_Start4.clicked.connect(lambda: self.start_task_4())

        self.pushButton_Stop1.clicked.connect(lambda: self.stop_task_1())
        self.pushButton_Stop2.clicked.connect(lambda: self.stop_task_2())
        self.pushButton_Stop3.clicked.connect(lambda: self.stop_task_3())
        self.pushButton_Stop4.clicked.connect(lambda: self.stop_task_4())
          # LineEdit
        self.lineEdit_status_1.setReadOnly(True)
        self.lineEdit_status_2.setReadOnly(True)
        self.lineEdit_status_3.setReadOnly(True)
        self.lineEdit_status_4.setReadOnly(True)
        self.lineEdit_data_dir.setText(data_dir)
        self.lineEdit_data_dir.textChanged.connect(self.test_data_path_1)
        self.lineEdit_data_dir.textChanged.connect(self.test_data_path_2)
        self.lineEdit_data_dir.textChanged.connect(self.test_data_path_3)
        self.lineEdit_data_dir.textChanged.connect(self.test_data_path_4)
        self.lineEdit_subid1.textChanged.connect(self.test_data_path_1)
        self.lineEdit_subid2.textChanged.connect(self.test_data_path_2)
        self.lineEdit_subid3.textChanged.connect(self.test_data_path_3)
        self.lineEdit_subid4.textChanged.connect(self.test_data_path_4)
        self.comboBox_srport_1.setEditable(True)
        self.comboBox_srport_2.setEditable(True)
        self.comboBox_srport_3.setEditable(True)
        self.comboBox_srport_4.setEditable(True)
        # Graph Plotter
        # self.task_plot = Task_plotter()
        # Create dialogs.
        self.Board_config_dialog_1 = Board_config_dialog_1(parent=self)
        self.Board_config_dialog_2 = Board_config_dialog_2(parent=self)
        self.Board_config_dialog_3 = Board_config_dialog_3(parent=self)
        self.Board_config_dialog_4 = Board_config_dialog_4(parent=self)
        # Create timers
        self.process_timer_1 = QtCore.QTimer()  # Timer to regularly call process_data() during run.
        self.process_timer_1.timeout.connect(self.process_data_1)
        self.refresh_timer_1 = QtCore.QTimer()  # Timer to regularly call refresh() when not running.
        self.refresh_timer_1.timeout.connect(self.refresh)
        self.process_timer_2 = QtCore.QTimer()  # Timer to regularly call process_data() during run.
        self.process_timer_2.timeout.connect(self.process_data_2)
        self.refresh_timer_2 = QtCore.QTimer()  # Timer to regularly call refresh() when not running.
        self.refresh_timer_2.timeout.connect(self.refresh)
        self.process_timer_3 = QtCore.QTimer()  # Timer to regularly call process_data() during run.
        self.process_timer_3.timeout.connect(self.process_data_3)
        self.refresh_timer_3 = QtCore.QTimer()  # Timer to regularly call refresh() when not running.
        self.refresh_timer_3.timeout.connect(self.refresh)
        self.process_timer_4 = QtCore.QTimer()  # Timer to regularly call process_data() during run.
        self.process_timer_4.timeout.connect(self.process_data_4)
        self.refresh_timer_4 = QtCore.QTimer()  # Timer to regularly call refresh() when not running.
        self.refresh_timer_4.timeout.connect(self.refresh)

        # Initial setup.
        self.disconnect_1()  # Set initial state as disconnected.
        self.disconnect_2()
        self.disconnect_3()
        self.disconnect_4()


        self.refresh()
        # self.refresh()# Refresh tasks and ports lists.
        self.refresh_timer_1.start(self.refresh_interval)
        self.refresh_timer_2.start(self.refresh_interval)
        self.refresh_timer_3.start(self.refresh_interval)
        self.refresh_timer_4.start(self.refresh_interval)
        self.disable_widgets()
        self.tableWidget.clearContents()
        self.sample_start_time_1 = 0
        self.iti_start_time_1 = 0
        self.sample_start_time_2 = 0
        self.iti_start_time_2 = 0
        self.sample_start_time_3 = 0
        self.iti_start_time_3 = 0
        self.sample_start_time_4 = 0
        self.iti_start_time_4 = 0
        self.sample_start_time_5 = 0
        self.correct_time_start_1 = 0
        self.correct_time_start_2 = 0
        self.correct_time_start_3 = 0
        self.correct_time_start_4 = 0
        self.Correct_response_1 = 0
        self.correct_latency_1 = 0
        self.correct_cv_list_1 = []
        self.correct_lat_1 = 0
        self.correct_stdev_1 = 0
        self.correct_mean_1 = 0
        self.correct_cv_1 = 0
        self.Incorrect_response_1 = 0
        self.incorrect_latency_1 = 0
        self.incorrect_cv_list_1 = []
        self.incorrect_lat_1 = 0
        self.incorrect_stdev_1 = 0
        self.incorrect_mean_1 = 0
        self.incorrect_cv_1 = 0
        self.Premature_response_1 = 0
        self.premature_latency_latency_1 = 0
        self.premature_latency_cv_list_1 = []
        self.premature_latency_lat_1 = 0
        self.premature_latency_stdev_1 = 0
        self.premature_latency_mean_1 = 0
        self.premature_latency_cv_1 = 0
        self.reward_latancy_latency_1 = 0
        self.reward_latancy_cv_list_1 = []
        self.reward_latancy_lat_1 = 0
        self.reward_latancy_stdev_1 = 0
        self.reward_latancy_mean_1 = 0
        self.reward_latancy_cv_1 = 0
        self.omission_1 = 0
        self.perseverate_1 = 0
        self.resp_timeout_1 = 0
        self.Receptacle_entries_1 = 0
        self.Nosepokes_5poke_1 = 0
        self.Choice_state_1 = 0
        self.per_omission_1 = 0
        self.per_accuracy_1 = 0
        self.per_correct_1 = 0
        self.per_premature_1 = 0
        self.per_perseverate_1 = 0
        self.Correct_response_2 = 0
        self.correct_latency_2 = 0
        self.correct_cv_list_2 = []
        self.correct_lat_2 = 0
        self.correct_stdev_2 = 0
        self.correct_mean_2 = 0
        self.correct_cv_2 = 0
        self.Incorrect_response_2 = 0
        self.incorrect_latency_2 = 0
        self.incorrect_cv_list_2 = []
        self.incorrect_lat_2 = 0
        self.incorrect_stdev_2 = 0
        self.incorrect_mean_2 = 0
        self.incorrect_cv_2 = 0
        self.Premature_response_2 = 0
        self.premature_latency_latency_2 = 0
        self.premature_latency_cv_list_2 = []
        self.premature_latency_lat_2 = 0
        self.premature_latency_stdev_2 = 0
        self.premature_latency_mean_2 = 0
        self.premature_latency_cv_2 = 0
        self.reward_latancy_latency_2 = 0
        self.reward_latancy_cv_list_2 = []
        self.reward_latancy_lat_2 = 0
        self.reward_latancy_stdev_2 = 0
        self.reward_latancy_mean_2 = 0
        self.reward_latancy_cv_2 = 0
        self.omission_2 = 0
        self.perseverate_2 = 0
        self.resp_timeout_2 = 0
        self.Receptacle_entries_2 = 0
        self.Nosepokes_5poke_2 = 0
        self.Choice_state_2 = 0
        self.per_omission_2 = 0
        self.per_accuracy_2 = 0
        self.per_correct_2 = 0
        self.per_premature_2 = 0
        self.per_perseverate_2 = 0
        self.Correct_response_3 = 0
        self.correct_latency_3 = 0
        self.correct_cv_list_3 = []
        self.correct_lat_3 = 0
        self.correct_stdev_3 = 0
        self.correct_mean_3 = 0
        self.correct_cv_3 = 0
        self.Incorrect_response_3 = 0
        self.incorrect_latency_3 = 0
        self.incorrect_cv_list_3 = []
        self.incorrect_lat_3 = 0
        self.incorrect_stdev_3 = 0
        self.incorrect_mean_3 = 0
        self.incorrect_cv_3 = 0
        self.Premature_response_3 = 0
        self.premature_latency_latency_3 = 0
        self.premature_latency_cv_list_3 = []
        self.premature_latency_lat_3 = 0
        self.premature_latency_stdev_3 = 0
        self.premature_latency_mean_3 = 0
        self.premature_latency_cv_3 = 0
        self.reward_latancy_latency_3 = 0
        self.reward_latancy_cv_list_3 = []
        self.reward_latancy_lat_3 = 0
        self.reward_latancy_stdev_3 = 0
        self.reward_latancy_mean_3 = 0
        self.reward_latancy_cv_3 = 0
        self.omission_3 = 0
        self.perseverate_3 = 0
        self.resp_timeout_3 = 0
        self.Receptacle_entries_3 = 0
        self.Nosepokes_5poke_3 = 0
        self.Choice_state_3 = 0
        self.per_omission_3 = 0
        self.per_accuracy_3 = 0
        self.per_correct_3 = 0
        self.per_premature_3 = 0
        self.per_perseverate_3 = 0
        self.Correct_response_4 = 0
        self.correct_latency_4 = 0
        self.correct_cv_list_4 = []
        self.correct_lat_4 = 0
        self.correct_stdev_4 = 0
        self.correct_mean_4 = 0
        self.correct_cv_4 = 0
        self.Incorrect_response_4 = 0
        self.incorrect_latency_4 = 0
        self.incorrect_cv_list_4 = []
        self.incorrect_lat_4 = 0
        self.incorrect_stdev_4 = 0
        self.incorrect_mean_4 = 0
        self.incorrect_cv_4 = 0
        self.Premature_response_4 = 0
        self.premature_latency_latency_4 = 0
        self.premature_latency_cv_list_4 = []
        self.premature_latency_lat_4 = 0
        self.premature_latency_stdev_4 = 0
        self.premature_latency_mean_4 = 0
        self.premature_latency_cv_4 = 0
        self.reward_latancy_latency_4 = 0
        self.reward_latancy_cv_list_4 = []
        self.reward_latancy_lat_4 = 0
        self.reward_latancy_stdev_4 = 0
        self.reward_latancy_mean_4 = 0
        self.reward_latancy_cv_4 = 0
        self.omission_4 = 0
        self.perseverate_4 = 0
        self.resp_timeout_4 = 0
        self.Receptacle_entries_4 = 0
        self.Nosepokes_5poke_4 = 0
        self.Choice_state_4 = 0
        self.per_omission_4 = 0
        self.per_accuracy_4 = 0
        self.per_correct_4 = 0
        self.per_premature_4 = 0
        self.per_perseverate_4 = 0

    # General methods
    def print_to_log(self, print_string, end='\n'):
        print(print_string + end)

    def clear_task_combo_box(self):
        self.comboBox_task1.clear()
        self.comboBox_task2.clear()
        self.comboBox_task3.clear()
        self.comboBox_task4.clear()

    def clear_srport_combo_box(self):
        self.comboBox_srport_1.clear()
        self.comboBox_srport_2.clear()
        self.comboBox_srport_3.clear()
        self.comboBox_srport_4.clear()

    def add_to_srport_combo_box(self, ports):
        self.comboBox_srport_1.addItems(sorted(ports))
        self.comboBox_srport_2.addItems(sorted(ports))
        self.comboBox_srport_3.addItems(sorted(ports))
        self.comboBox_srport_4.addItems(sorted(ports))

    def enable_srport_combo_box(self, state):
        self.comboBox_srport_1.setEnabled(state)
        self.comboBox_srport_2.setEnabled(state)
        self.comboBox_srport_3.setEnabled(state)
        self.comboBox_srport_4.setEnabled(state)

    def enable_task_combo_box(self, state):
        self.comboBox_task1.setEnabled(state)
        self.comboBox_task2.setEnabled(state)
        self.comboBox_task3.setEnabled(state)
        self.comboBox_task4.setEnabled(state)

    def combo_box_add_items(self, tasks):
        self.comboBox_task1.addItems(sorted(tasks))
        self.comboBox_task2.addItems(sorted(tasks))
        self.comboBox_task3.addItems(sorted(tasks))
        self.comboBox_task4.addItems(sorted(tasks))

    def disable_widgets(self):
        self.lineEdit_subid1.setEnabled(True)
        self.pushButton_Start1.setEnabled(False)
        self.pushButton_Stop1.setEnabled(False)
        self.pushButton_upload_1.setEnabled(False)
        self.comboBox_task1.setEnabled(False)
        self.pushButton_var1.setEnabled(False)
        self.pushButton_config_1.setEnabled(False)
        self.lineEdit_status_1.setEnabled(False)
        self.pushButton_Start2.setEnabled(False)
        self.pushButton_Stop2.setEnabled(False)
        self.pushButton_upload_2.setEnabled(False)
        self.lineEdit_subid2.setEnabled(True)
        self.comboBox_task2.setEnabled(False)
        self.pushButton_var2.setEnabled(False)
        self.pushButton_config_2.setEnabled(False)
        self.lineEdit_status_2.setEnabled(False)
        self.pushButton_Start3.setEnabled(False)
        self.pushButton_Stop3.setEnabled(False)
        self.pushButton_upload_3.setEnabled(False)
        self.lineEdit_subid3.setEnabled(True)
        self.comboBox_task3.setEnabled(False)
        self.pushButton_var3.setEnabled(False)
        self.pushButton_config_3.setEnabled(False)
        self.lineEdit_status_3.setEnabled(False)
        self.pushButton_Start4.setEnabled(False)
        self.pushButton_Stop4.setEnabled(False)
        self.pushButton_upload_4.setEnabled(False)
        self.lineEdit_subid4.setEnabled(True)
        self.comboBox_task4.setEnabled(False)
        self.pushButton_var4.setEnabled(False)
        self.pushButton_config_4.setEnabled(False)
        self.lineEdit_status_4.setEnabled(False)
        self.pushButton_data_dir.setEnabled(True)
       
    def enable_widgets(self, com_list):
        if len(com_list) == 1:
            self.comboBox_srport_1.setEnabled(True)
            self.pushButton_connect_1.setEnabled(True)
        if len(com_list) == 2:
            self.comboBox_srport_2.setEnabled(True)
            self.pushButton_connect_2.setEnabled(True)
        if len(com_list) == 3:
            self.comboBox_srport_3.setEnabled(True)
            self.pushButton_connect_3.setEnabled(True)
        if len(com_list) == 4:
            self.comboBox_srport_4.setEnabled(True)
            self.pushButton_connect_4.setEnabled(True)

    def table_fill(self):
        self.tableWidget.setItem(0, 3,
                                 QtWidgets.QTableWidgetItem(str('Session:')))
        self.Session = str(self.lineEdit_prj_2.text())
        self.tableWidget.setItem(0, 4,
                                 QtWidgets.QTableWidgetItem(str(self.Session)))
        self.tableWidget.setItem(1, 3,
                                 QtWidgets.QTableWidgetItem(str('DATE:')))
        self.date = datetime.today()
        self.tableWidget.setItem(1, 4,
                                 QtWidgets.QTableWidgetItem(str(self.date)))
        self.tableWidget.setItem(0, 6,
                                 QtWidgets.QTableWidgetItem(str('Experimenter_name:')))
        self.exp_name = str(self.lineEdit_exp.text())
        self.tableWidget.setItem(0, 7,
                                 QtWidgets.QTableWidgetItem(str(self.exp_name)))
        self.tableWidget.setItem(0, 9,
                                 QtWidgets.QTableWidgetItem(str('Project:')))
        self.project = str(self.lineEdit_prj.text())
        self.tableWidget.setItem(0, 10,
                                 QtWidgets.QTableWidgetItem(str(self.project)))
        self.tableWidget.setItem(1, 0,
                                 QtWidgets.QTableWidgetItem(str('DATA_Live')))
        self.tableWidget.setItem(1, 1,
                                 QtWidgets.QTableWidgetItem(str('BOX')))
        self.tableWidget.setItem(1, 2,
                                 QtWidgets.QTableWidgetItem(str('Sub_ID')))
        self.tableWidget.setItem(1, 3,
                                 QtWidgets.QTableWidgetItem(str('TASK')))
        self.tableWidget.setItem(1, 4,
                                 QtWidgets.QTableWidgetItem(str('Accuracy(%)')))
        self.tableWidget.setItem(1, 5,
                                 QtWidgets.QTableWidgetItem(str('Omission(%)')))
        self.tableWidget.setItem(1, 6,
                                 QtWidgets.QTableWidgetItem(str('Correct(%)')))
        self.tableWidget.setItem(1, 7,
                                 QtWidgets.QTableWidgetItem(str('#Correct')))
        self.tableWidget.setItem(1, 8,
                                 QtWidgets.QTableWidgetItem(str('Premature(%)')))
        self.tableWidget.setItem(1, 9,
                                 QtWidgets.QTableWidgetItem(str('Rew. Lat.')))
        self.tableWidget.setItem(1, 10,
                                 QtWidgets.QTableWidgetItem(str('#Trials')))
        self.tableWidget.setItem(1, 11,
                                 QtWidgets.QTableWidgetItem(str('Perseverative(%)')))
        self.tableWidget.setItem(1, 12,
                                 QtWidgets.QTableWidgetItem(str('#Prematures')))
        self.tableWidget.setItem(1, 13,
                                 QtWidgets.QTableWidgetItem(str('correct_CV')))
        self.tableWidget.setItem(1, 14,
                                 QtWidgets.QTableWidgetItem(str('response_lat.')))
        self.tableWidget.setItem(1, 15,
                                 QtWidgets.QTableWidgetItem(str('#Omision')))
        self.tableWidget.setItem(1, 16,
                                 QtWidgets.QTableWidgetItem(str('#Incorrect')))
        self.tableWidget.setItem(1, 17,
                                 QtWidgets.QTableWidgetItem(str('incorrect_lat.')))
        self.tableWidget.setItem(1, 18,
                                 QtWidgets.QTableWidgetItem(str('premature_lat.')))
        self.tableWidget.setItem(1, 19,
                                 QtWidgets.QTableWidgetItem(str('#Perseveratives')))
        self.tableWidget.setItem(1, 20,
                                 QtWidgets.QTableWidgetItem(str('#Receptacle_entries')))
        self.tableWidget.setItem(1, 21,
                                 QtWidgets.QTableWidgetItem(str('#Nosepokes_5poke')))
        self.tableWidget.setItem(1, 22,
                                 QtWidgets.QTableWidgetItem(str('#Resp_timeouts')))
        self.tableWidget.setItem(1, 23,
                                 QtWidgets.QTableWidgetItem(str('REMARKS')))
        self.tableWidget.setItem(1, 27,
                                 QtWidgets.QTableWidgetItem(str('stdev_correct_lat.')))
        self.tableWidget.setItem(1, 28,
                                 QtWidgets.QTableWidgetItem(str('stdev_incorrect_lat.')))
        self.tableWidget.setItem(1, 29,
                                 QtWidgets.QTableWidgetItem(str('stdev_premature_lat.')))
        self.tableWidget.setItem(1, 30,
                                 QtWidgets.QTableWidgetItem(str('stdev_reward_lat.')))
        self.tableWidget.setItem(1, 32,
                                 QtWidgets.QTableWidgetItem(str('correct_lat_list')))
        self.tableWidget.setItem(1, 33,
                                 QtWidgets.QTableWidgetItem(str('incorrect_lat_list')))
        self.tableWidget.setItem(1, 34,
                                 QtWidgets.QTableWidgetItem(str('premature_lat_list')))
        self.tableWidget.setItem(1, 35,
                                 QtWidgets.QTableWidgetItem(str('reward_lat_list')))
        self.tableWidget.setItem(1, 37,
                                 QtWidgets.QTableWidgetItem(str('incorrect_lat_cv')))
        self.tableWidget.setItem(1, 38,
                                 QtWidgets.QTableWidgetItem(str('premature_lat_cv')))
        self.tableWidget.setItem(2, 1,
                                 QtWidgets.QTableWidgetItem(str('BOX-1')))
        self.tableWidget.setItem(3, 1,
                                 QtWidgets.QTableWidgetItem(str('BOX-2')))
        self.tableWidget.setItem(4, 1,
                                 QtWidgets.QTableWidgetItem(str('BOX-3')))
        self.tableWidget.setItem(5, 1,
                                 QtWidgets.QTableWidgetItem(str('BOX-4')))



    def scan_ports(self):
        # Scan serial ports for connected boards and update ports list if changed.
        ports = set([c[0] for c in list_ports.comports()
                     if ('Pyboard' in c[1]) or ('USB Serial Device' in c[1])])
        port_list = list(ports)
        if not ports == self.available_ports:
            self.clear_srport_combo_box()
            self.enable_widgets(port_list)
            self.add_to_srport_combo_box(ports)
            self.available_ports = ports

    def scan_tasks(self):
        # Scan task folder for available tasks and update tasks list if changed.
        tasks = set([t.split('.')[0] for t in os.listdir(tasks_dir)
                     if t[-3:] == '.py'])
        if not tasks == self.available_tasks:
            self.clear_task_combo_box()
            self.combo_box_add_items(sorted(tasks))
            self.available_tasks = tasks
        if self.task_1:
            try:
                task_1 = self.comboBox_task1.currentText()
                task_path_1 = os.path.join(tasks_dir, task_1 + '.py')
                if not self.task_hash_1 == _djb2_file(task_path_1):  # Task file modified.
                    self.task_changed_1()
            except FileNotFoundError:
                pass
        if self.task_2:
            try:
                task_2 = self.comboBox_task2.currentText()
                task_path_2 = os.path.join(tasks_dir, task_2 + '.py')
                if not self.task_hash_2 == _djb2_file(task_path_2):  # Task file modified.
                    self.task_changed_2()
            except FileNotFoundError:
                pass
        if self.task_3:
            try:
                task_3 = self.comboBox_task3.currentText()
                task_path_3 = os.path.join(tasks_dir, task_3 + '.py')
                if not self.task_hash_3 == _djb2_file(task_path_3):  # Task file modified.
                    self.task_changed_3()
            except FileNotFoundError:
                pass
        if self.task_4:
            try:
                task_4 = self.comboBox_task4.currentText()
                task_path_4 = os.path.join(tasks_dir, task_4 + '.py')
                if not self.task_hash_4 == _djb2_file(task_path_4):  # Task file modified.
                    self.task_changed_4()
            except FileNotFoundError:
                pass

    def task_changed_1(self):
        self.uploaded_1 = False
        self.pushButton_upload_1.setText('Upload')
        self.pushButton_Start1.setEnabled(False)

    def task_changed_2(self):
        self.uploaded_2 = False
        self.pushButton_upload_2.setText('Upload')
        self.pushButton_Start2.setEnabled(False)

    def task_changed_3(self):
        self.uploaded_3 = False
        self.pushButton_upload_3.setText('Upload')
        self.pushButton_Start3.setEnabled(False)

    def task_changed_4(self):
        self.uploaded_4 = False
        self.pushButton_upload_4.setText('Upload')
        self.pushButton_Start4.setEnabled(False)


    # Widget methods.
    def connect_1(self):
        try:
            self.lineEdit_status_1.setText('Connecting...')
            self.pushButton_Stop1.setEnabled(False)
            self.lineEdit_subid1.setEnabled(False)
            self.pushButton_var1.setEnabled(False)
            self.comboBox_srport_1.setEnabled(False)
            self.pushButton_connect_1.setEnabled(False)
            self.repaint()
            self.board_1 = Pycboard(self.comboBox_srport_1.currentText(),
                                    data_logger=self.data_logger1)
            if not self.board_1.status['framework']:
                self.board_1.load_framework()
            self.connected_1 = True
            self.pushButton_config_1.setEnabled(True)
            self.pushButton_connect_1.setEnabled(True)
            self.comboBox_task1.setEnabled(True)
            self.pushButton_upload_1.setEnabled(True)
            self.lineEdit_subid1.setEnabled(True)
            self.pushButton_connect_1.setText('Disconnect')

            self.lineEdit_status_1.setText('Connected')
        except SerialException:
            self.lineEdit_status_1.setText('Connection failed')
            self.pushButton_connect_1.setEnabled(True)

    def connect_2(self):
        try:
            self.lineEdit_status_2.setText('Connecting...')
            self.pushButton_Stop2.setEnabled(False)
            self.lineEdit_subid2.setEnabled(False)
            self.pushButton_var2.setEnabled(False)
            self.comboBox_srport_2.setEnabled(False)
            self.pushButton_connect_2.setEnabled(False)
            self.repaint()
            self.board_2 = Pycboard(self.comboBox_srport_2.currentText(),
                                    data_logger=self.data_logger2)
            if not self.board_2.status['framework']:
                self.board_2.load_framework()
            self.connected_2 = True
            self.pushButton_config_2.setEnabled(True)
            self.pushButton_connect_2.setEnabled(True)
            self.comboBox_task2.setEnabled(True)
            self.pushButton_upload_2.setEnabled(True)
            self.lineEdit_subid2.setEnabled(True)
            self.pushButton_connect_2.setText('Disconnect')

            self.lineEdit_status_2.setText('Connected')
        except SerialException:
            self.lineEdit_status_2.setText('Connection failed')
            self.pushButton_connect_2.setEnabled(True)

    def connect_3(self):
        try:
            self.lineEdit_status_3.setText('Connecting...')
            self.pushButton_Stop3.setEnabled(False)
            self.lineEdit_subid3.setEnabled(False)
            self.pushButton_var3.setEnabled(False)
            self.comboBox_srport_3.setEnabled(False)
            self.pushButton_connect_3.setEnabled(False)
            self.repaint()
            self.board_3 = Pycboard(self.comboBox_srport_3.currentText(),
                                    data_logger=self.data_logger3)
            if not self.board_3.status['framework']:
                self.board_3.load_framework()
            self.connected_3 = True
            self.pushButton_config_3.setEnabled(True)
            self.pushButton_connect_3.setEnabled(True)
            self.comboBox_task3.setEnabled(True)
            self.pushButton_upload_3.setEnabled(True)
            self.lineEdit_subid3.setEnabled(True)
            self.pushButton_connect_3.setText('Disconnect')

            self.lineEdit_status_3.setText('Connected')
        except SerialException:
            self.lineEdit_status_3.setText('Connection failed')
            self.pushButton_connect_3.setEnabled(True)

    def connect_4(self):
        try:
            self.lineEdit_status_4.setText('Connecting...')
            self.pushButton_Stop4.setEnabled(False)
            self.lineEdit_subid4.setEnabled(False)
            self.pushButton_var4.setEnabled(False)
            self.comboBox_srport_4.setEnabled(False)
            self.pushButton_connect_4.setEnabled(False)
            self.repaint()
            self.board_4 = Pycboard(self.comboBox_srport_4.currentText(),
                                    data_logger=self.data_logger4)
            if not self.board_4.status['framework']:
                self.board_4.load_framework()
            self.connected_4 = True
            self.pushButton_config_4.setEnabled(True)
            self.pushButton_connect_4.setEnabled(True)
            self.comboBox_task4.setEnabled(True)
            self.pushButton_upload_4.setEnabled(True)
            self.lineEdit_subid4.setEnabled(True)
            self.pushButton_connect_4.setText('Disconnect')

            self.lineEdit_status_4.setText('Connected')
        except SerialException:
            self.lineEdit_status_4.setText('Connection failed')
            self.pushButton_connect_4.setEnabled(True)


    def disconnect_1(self):
        # Disconnect from pyboard.
        if self.board_1: self.board_1.close()
        self.board_1 = None
        self.pushButton_config_1.setEnabled(False)
        self.pushButton_var1.setEnabled(False)
        self.comboBox_task1.setEnabled(False)
        self.pushButton_Start1.setEnabled(False)
        self.pushButton_Stop1.setEnabled(False)
        self.pushButton_upload_1.setEnabled(False)
        self.lineEdit_subid1.setEnabled(False)
        self.enable_srport_combo_box(True)
        self.pushButton_connect_1.setText('Connect')
        self.lineEdit_status_1.setText('Not connected')
        self.lineEdit_status_1.setEnabled(False)
        self.connected_1 = False

    def disconnect_2(self):
        if self.board_2: self.board_2.close()
        self.board_2 = None
        self.pushButton_config_2.setEnabled(False)
        self.pushButton_var2.setEnabled(False)
        self.comboBox_task2.setEnabled(False)
        self.pushButton_Start2.setEnabled(False)
        self.pushButton_Stop2.setEnabled(False)
        self.pushButton_upload_2.setEnabled(False)
        self.lineEdit_subid2.setEnabled(False)
        self.enable_srport_combo_box(True)
        self.pushButton_connect_2.setText('Connect')
        self.lineEdit_status_2.setText('Not connected')
        self.lineEdit_status_2.setEnabled(False)
        self.connected_2 = False

    def disconnect_3(self):
        if self.board_3: self.board_3.close()
        self.board_3 = None
        self.pushButton_config_3.setEnabled(False)
        self.pushButton_var3.setEnabled(False)
        self.comboBox_task3.setEnabled(False)
        self.pushButton_Start3.setEnabled(False)
        self.pushButton_Stop3.setEnabled(False)
        self.pushButton_upload_3.setEnabled(False)
        self.lineEdit_subid3.setEnabled(False)
        self.enable_srport_combo_box(True)
        self.pushButton_connect_3.setText('Connect')
        self.lineEdit_status_3.setText('Not connected')
        self.lineEdit_status_3.setEnabled(False)
        self.connected_3 = False

    def disconnect_4(self):
        if self.board_4: self.board_4.close()
        self.board_4 = None
        self.pushButton_config_4.setEnabled(False)
        self.pushButton_var4.setEnabled(False)
        self.comboBox_task4.setEnabled(False)
        self.pushButton_Start4.setEnabled(False)
        self.pushButton_Stop4.setEnabled(False)
        self.pushButton_upload_4.setEnabled(False)
        self.lineEdit_subid4.setEnabled(False)
        self.enable_srport_combo_box(True)
        self.pushButton_connect_4.setText('Connect')
        self.lineEdit_status_4.setText('Not connected')
        self.lineEdit_status_4.setEnabled(False)
        self.connected_4 = False

    def status_update(self, msg):
        self.lineEdit_status_1.setText(msg)
        self.lineEdit_status_2.setText(msg)
        self.lineEdit_status_3.setText(msg)
        self.lineEdit_status_4.setText(msg)

    def setup_task_1(self):
        try:
            task_1 = self.comboBox_task1.currentText()
            if self.uploaded_1:
                self.lineEdit_status_1.setText('Resetting task..')
            else:
                self.lineEdit_status_1.setText('Uploading..')
                self.task_hash_1 = _djb2_file(os.path.join(tasks_dir, task_1 + '.py'))
            self.pushButton_Start1.setEnabled(False)
            self.pushButton_var1.setEnabled(False)
            self.repaint()
            self.sm_info_1 = self.board_1.setup_state_machine(task_1, uploaded=self.uploaded_1)
            self.variables_dialog_1 = Variables_dialog(parent=self, variable=1)
            self.pushButton_var1.setEnabled(True)
            # self.task_plot.set_state_machine(self.sm_info)
            self.pushButton_Start1.setEnabled(True)
            self.lineEdit_subid1.setEnabled(True)
            self.pushButton_Stop1.setEnabled(False)
            self.lineEdit_status_1.setText('Uploaded : ' + task_1)
            self.task_1 = task_1
            self.uploaded_1 = True
            self.pushButton_upload_1.setText('Reset')
        except PyboardError:
            self.lineEdit_status_1.setText('Error setting up state machine.')

    def setup_task_2(self):
        try:
            task_2 = self.comboBox_task2.currentText()
            if self.uploaded_2:
                self.lineEdit_status_2.setText('Resetting task..')
            else:
                self.lineEdit_status_2.setText('Uploading..')
                self.task_hash_2 = _djb2_file(os.path.join(tasks_dir, task_2 + '.py'))
            self.pushButton_Start2.setEnabled(False)
            self.pushButton_var2.setEnabled(False)
            self.repaint()
            self.sm_info_2 = self.board_2.setup_state_machine(task_2, uploaded=self.uploaded_2)
            self.variables_dialog_2 = Variables_dialog(parent=self, variable=2)
            self.pushButton_var2.setEnabled(True)
            # self.task_plot.set_state_machine(self.sm_info)
            self.pushButton_Start2.setEnabled(True)
            self.lineEdit_subid2.setEnabled(True)
            self.pushButton_Stop2.setEnabled(False)
            self.lineEdit_status_2.setText('Uploaded : ' + task_2)
            self.task_2 = task_2
            self.uploaded_2 = True
            self.pushButton_upload_2.setText('Reset')
        except PyboardError:
            self.lineEdit_status_2.setText('Error setting up state machine.')

    def setup_task_3(self):
        try:
            task_3 = self.comboBox_task3.currentText()
            if self.uploaded_3:
                self.lineEdit_status_3.setText('Resetting task..')
            else:
                self.lineEdit_status_3.setText('Uploading..')
                self.task_hash_3 = _djb2_file(os.path.join(tasks_dir, task_3 + '.py'))
            self.pushButton_Start3.setEnabled(False)
            self.pushButton_var3.setEnabled(False)
            self.repaint()
            self.sm_info_3 = self.board_3.setup_state_machine(task_3, uploaded=self.uploaded_3)
            self.variables_dialog_3 = Variables_dialog(parent=self, variable=3)
            self.pushButton_var3.setEnabled(True)
            # self.task_plot.set_state_machine(self.sm_info)
            self.pushButton_Start3.setEnabled(True)
            self.lineEdit_subid3.setEnabled(True)
            self.pushButton_Stop3.setEnabled(False)
            self.lineEdit_status_3.setText('Uploaded : ' + task_3)
            self.task_3 = task_3
            self.uploaded_3 = True
            self.pushButton_upload_3.setText('Reset')
        except PyboardError:
            self.lineEdit_status_3.setText('Error setting up state machine.')

    def setup_task_4(self):
        try:
            task_4 = self.comboBox_task4.currentText()
            if self.uploaded_4:
                self.lineEdit_status_4.setText('Resetting task..')
            else:
                self.lineEdit_status_4.setText('Uploading..')
                self.task_hash_4 = _djb2_file(os.path.join(tasks_dir, task_4 + '.py'))
            self.pushButton_Start4.setEnabled(False)
            self.pushButton_var4.setEnabled(False)
            self.repaint()
            self.sm_info_4 = self.board_4.setup_state_machine(task_4, uploaded=self.uploaded_4)
            self.variables_dialog_4 = Variables_dialog(parent=self, variable=4)
            self.pushButton_var4.setEnabled(True)
            # self.task_plot.set_state_machine(self.sm_info)
            self.pushButton_Start4.setEnabled(True)
            self.lineEdit_subid4.setEnabled(True)
            self.pushButton_Stop4.setEnabled(False)
            self.lineEdit_status_4.setText('Uploaded : ' + task_4)
            self.task_4 = task_4
            self.uploaded_4 = True
            self.pushButton_upload_4.setText('Reset')
        except PyboardError:
            self.lineEdit_status_4.setText('Error setting up state machine.')

    def select_data_dir(self):
        self.lineEdit_data_dir.setText(
            QtGui.QFileDialog.getExistingDirectory(self, 'Select data folder', data_dir))

    def test_data_path_1(self):
        # Checks whether data dir and subject ID are valid.
        self.data_dir = self.lineEdit_data_dir.text()
        subject_id_1 = self.lineEdit_subid1.text()
        if os.path.isdir(self.data_dir) and subject_id_1:
            self.pushButton_Start1.setText('RECORD')
            return True
        else:
            self.pushButton_Start1.setText('START')

    def test_data_path_2(self):
        # Checks whether data dir and subject ID are valid.
        self.data_dir = self.lineEdit_data_dir.text()
        subject_id_2 = self.lineEdit_subid2.text()
        if os.path.isdir(self.data_dir) and subject_id_2:
            self.pushButton_Start2.setText('RECORD')
            return True
        else:
            self.pushButton_Start2.setText('START')

    def test_data_path_3(self):
        # Checks whether data dir and subject ID are valid.
        self.data_dir = self.lineEdit_data_dir.text()
        subject_id_3 = self.lineEdit_subid3.text()
        if os.path.isdir(self.data_dir) and subject_id_3:
            self.pushButton_Start3.setText('RECORD')
            return True
        else:
            self.pushButton_Start3.setText('START')

    def test_data_path_4(self):
        # Checks whether data dir and subject ID are valid.
        self.data_dir = self.lineEdit_data_dir.text()
        subject_id_4 = self.lineEdit_subid4.text()
        if os.path.isdir(self.data_dir) and subject_id_4:
            self.pushButton_Start4.setText('RECORD')
            return True
        else:
            self.pushButton_Start4.setText('START')

    def start_task_1(self):
        if self.test_data_path_1():
            self.subject_id_1 = str(self.lineEdit_subid1.text())
            self.data_logger1.open_data_file(self.data_dir, self.exp_name, self.subject_id_1, self.project)
        self.resettable.setEnabled(False)
        self.tableWidget.setItem(2, 2,
                                 QtWidgets.QTableWidgetItem(str(self.subject_id_1)))
        self.tableWidget.setItem(2, 3,
                                 QtWidgets.QTableWidgetItem(str(self.task_1)))
        self.board_1.start_framework()
        self.start_time_1 = time.time()
        # self.task_plot.run_start()
        self.comboBox_task1.setEnabled(False)
        self.pushButton_upload_1.setEnabled(False)
        self.pushButton_Start1.setEnabled(False)
        self.pushButton_config_1.setEnabled(False)
        self.pushButton_Stop1.setEnabled(True)
        self.pushButton_connect_1.setEnabled(False)
        self.lineEdit_subid1.setEnabled(True)
        print('\nRun started at: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        self.process_timer_1.start(update_interval)
        self.refresh_timer_1.stop()
        self.lineEdit_status_1.setText('Running: ' + self.task_1)
        self.table_fill()

    def start_task_2(self):
        if self.test_data_path_2():
            self.subject_id_2 = str(self.lineEdit_subid2.text())
            self.data_logger2.open_data_file(self.data_dir, self.exp_name, self.subject_id_2, self.project)
        self.tableWidget.setItem(3, 2,
                                 QtWidgets.QTableWidgetItem(str(self.subject_id_2)))
        self.tableWidget.setItem(3, 3,
                                 QtWidgets.QTableWidgetItem(str(self.task_2)))
        self.board_2.start_framework()
        self.start_time_2 = time.time()
        self.resettable.setEnabled(False)
        # self.task_plot.run_start()
        self.comboBox_task2.setEnabled(False)
        self.pushButton_upload_2.setEnabled(False)
        self.pushButton_Start2.setEnabled(False)
        self.pushButton_config_2.setEnabled(False)
        self.pushButton_Stop2.setEnabled(True)
        self.pushButton_connect_2.setEnabled(False)
        self.lineEdit_subid1.setEnabled(True)
        print('\nRun started at: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        self.process_timer_2.start(update_interval)
        self.refresh_timer_2.stop()
        self.lineEdit_status_2.setText('Running: ' + self.task_2)
        self.table_fill()

    def start_task_3(self):
        if self.test_data_path_3():
            self.subject_id_3 = str(self.lineEdit_subid3.text())
            self.data_logger3.open_data_file(self.data_dir, self.exp_name, self.subject_id_3, self.project)
        self.tableWidget.setItem(4, 2,
                                 QtWidgets.QTableWidgetItem(str(self.subject_id_3)))
        self.tableWidget.setItem(4, 3,
                                 QtWidgets.QTableWidgetItem(str(self.task_3)))
        self.board_3.start_framework()
        self.start_time_3 = time.time()
        self.resettable.setEnabled(False)
        # self.task_plot.run_start()
        self.comboBox_task3.setEnabled(False)
        self.pushButton_upload_3.setEnabled(False)
        self.pushButton_Start3.setEnabled(False)
        self.pushButton_config_3.setEnabled(False)
        self.pushButton_Stop3.setEnabled(True)
        self.pushButton_connect_3.setEnabled(False)
        print('\nRun started at: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        self.process_timer_3.start(update_interval)
        self.refresh_timer_3.stop()
        self.lineEdit_status_3.setText('Running: ' + self.task_3)
        self.table_fill()

    def start_task_4(self):
        if self.test_data_path_4():
            self.subject_id_4 = str(self.lineEdit_subid4.text())
            self.data_logger4.open_data_file(self.data_dir, self.exp_name, self.subject_id_4, self.project)
        self.tableWidget.setItem(5, 2,
                                 QtWidgets.QTableWidgetItem(str(self.subject_id_4)))
        self.tableWidget.setItem(5, 3,
                                 QtWidgets.QTableWidgetItem(str(self.task_4)))
        self.board_4.start_framework()
        self.start_time_4 = time.time()
        self.resettable.setEnabled(False)
        # self.task_plot.run_start()
        self.comboBox_task4.setEnabled(False)
        self.pushButton_upload_4.setEnabled(False)
        self.pushButton_Start4.setEnabled(False)
        self.pushButton_config_4.setEnabled(False)
        self.pushButton_Stop4.setEnabled(True)
        self.pushButton_connect_4.setEnabled(False)
        self.lineEdit_subid4.setEnabled(True)
        print('\nRun started at: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        self.process_timer_4.start(update_interval)
        self.refresh_timer_4.stop()
        self.lineEdit_status_4.setText('Running: ' + self.task_4)
        self.table_fill()

    def stop_task_1(self, error=False, stopped_by_task=False):
        self.process_timer_1.stop()
        self.refresh_timer_1.start(self.refresh_interval)
        if not (error or stopped_by_task):
            self.board_1.stop_framework()
            QtCore.QTimer.singleShot(100, self.process_data_1)  # Catch output after framework stops.
        self.data_logger1.close_files()
        self.pushButton_Start1.setEnabled(True)
        self.pushButton_connect_1.setEnabled(True)
        self.comboBox_task1.setEnabled(True)
        self.resettable.setEnabled(False)
        self.pushButton_upload_1.setEnabled(True)
        self.pushButton_Stop1.setEnabled(False)
        self.tableWidget.setItem(2, 0,
                                 QtWidgets.QTableWidgetItem(str(self.date)))
        self.lineEdit_status_1.setText('Uploaded : ' + self.task_1)

    def stop_task_2(self, error=False, stopped_by_task=False):
        self.process_timer_2.stop()
        self.refresh_timer_2.start(self.refresh_interval)
        if not (error or stopped_by_task):
            self.board_2.stop_framework()
            QtCore.QTimer.singleShot(100, self.process_data_2)  # Catch output after framework stops.
        self.data_logger2.close_files()
        self.pushButton_Start2.setEnabled(True)
        self.pushButton_connect_2.setEnabled(True)
        self.comboBox_task2.setEnabled(True)
        self.resettable.setEnabled(False)
        self.pushButton_upload_2.setEnabled(True)
        self.pushButton_Stop2.setEnabled(False)
        self.tableWidget.setItem(3, 0,
                                 QtWidgets.QTableWidgetItem(str(self.date)))
        self.lineEdit_status_2.setText('Uploaded : ' + self.task_2)

    def stop_task_3(self, error=False, stopped_by_task=False):
        self.process_timer_3.stop()
        self.refresh_timer_3.start(self.refresh_interval)
        if not (error or stopped_by_task):
            self.board_3.stop_framework()
            QtCore.QTimer.singleShot(100, self.process_data_3)  # Catch output after framework stops.
        self.data_logger3.close_files()
        self.pushButton_Start3.setEnabled(True)
        self.pushButton_connect_3.setEnabled(True)
        self.comboBox_task3.setEnabled(True)
        self.resettable.setEnabled(False)
        self.pushButton_upload_3.setEnabled(True)
        self.pushButton_Stop3.setEnabled(False)
        self.tableWidget.setItem(4, 0,
                                 QtWidgets.QTableWidgetItem(str(self.date)))
        self.lineEdit_status_3.setText('Uploaded : ' + self.task_3)

    def stop_task_4(self, error=False, stopped_by_task=False):
        self.process_timer_4.stop()
        self.refresh_timer_4.start(self.refresh_interval)
        if not (error or stopped_by_task):
            self.board_4.stop_framework()
            QtCore.QTimer.singleShot(100, self.process_data_4)  # Catch output after framework stops.
        self.data_logger4.close_files()
        self.pushButton_Start4.setEnabled(True)
        self.pushButton_connect_4.setEnabled(True)
        self.comboBox_task4.setEnabled(True)
        self.resettable.setEnabled(False)
        self.pushButton_upload_4.setEnabled(True)
        self.pushButton_Stop4.setEnabled(False)
        self.tableWidget.setItem(5, 0,
                                 QtWidgets.QTableWidgetItem(str(self.date)))
        self.lineEdit_status_4.setText('Uploaded : ' + self.task_4)

    # Timer updates
    def process_data_1(self):
        # Called regularly during run to process data from board.
        try:
            new_data_1 = self.board_1.process_data()
            # update timer here
            run_time_1 = time.time() - self.start_time_1
            run_time_1 = str(timedelta(seconds=run_time_1))[:7]
            self.lcdNumber_Timer_BOX1.display(run_time_1)

            # self.task_plot.process_data(new_data_1)
            if not self.board_1.framework_running:
                self.stop_task_1(stopped_by_task=True)
            self.update_data_table_1(new_data_1)
        except PyboardError as e:
            self.print_to_log('\nError during framework run.')
            self.stop_task_1(error=True)

    def process_data_2(self):
        # Called regularly during run to process data from board.
        try:
            new_data_2 = self.board_2.process_data()
            # update timer here
            run_time = time.time() - self.start_time_2
            run_time = str(timedelta(seconds=run_time))[:7]
            self.lcdNumber_Timer_BOX2.display(run_time)
            # self.task_plot.process_data(new_data_2)
            if not self.board_2.framework_running:
                self.stop_task_2(stopped_by_task=True)
            self.update_data_table_2(new_data_2)
        except PyboardError as e:
            self.print_to_log('\nError during framework run.')
            self.stop_task_2(error=True)

    def process_data_3(self):
        # Called regularly during run to process data from board.
        try:
            new_data_3 = self.board_3.process_data()
            # update timer here
            run_time_3 = time.time() - self.start_time_3
            run_time_3 = str(timedelta(seconds=run_time_3))[:7]
            self.lcdNumber_Timer_BOX3.display(run_time_3)
            # self.task_plot.process_data(new_data_3)
            if not self.board_3.framework_running:
                self.stop_task_3(stopped_by_task=True)
            self.update_data_table_3(new_data_3)
        except PyboardError as e:
            self.print_to_log('\nError during framework run.')
            self.stop_task_3(error=True)

    def process_data_4(self):
        # Called regularly during run to process data from board.
        try:
            new_data_4 = self.board_4.process_data()
            # update timer here
            run_time_4 = time.time() - self.start_time_4
            run_time_4 = str(timedelta(seconds=run_time_4))[:7]
            self.lcdNumber_Timer_BOX4.display(run_time_4)
            # self.task_plot.process_data(new_data_4)
            if not self.board_4.framework_running:
                self.stop_task_4(stopped_by_task=True)
            self.update_data_table_4(new_data_4)
        except PyboardError as e:
            self.print_to_log('\nError during framework run.')
            self.stop_task_4(error=True)

    def update_data_table_1(self, new_data_1):
        if new_data_1:
            for value in new_data_1:
                for string in value:
                    self.tableWidget.setItem(2, 0,
                                             QtWidgets.QTableWidgetItem(str(value[2])))
                    if "Sample_state" in str(string):
                        self.sample_start_time_1 = time.time()
                        self.tableWidget.setItem(2, 58,
                                                 QtWidgets.QTableWidgetItem(str(self.sample_start_time_1)))
                    elif "Correct_response" in str(string):
                        self.Correct_response_1 += 1
                        self.tableWidget.setItem(2, 7,
                                                 QtWidgets.QTableWidgetItem(str(self.Correct_response_1)))
                        try:
                            self.correct_latency_1 = time.time() - self.sample_start_time_1
                            self.correct_cv_list_1.append(self.correct_latency_1)
                            self.tableWidget.setItem(2, 32,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_cv_list_1)))
                            self.correct_time_start_1 = time.time()
                            self.tableWidget.setItem(2, 62,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_time_start_1)))
                            self.correct_lat_1 = [float(i) for i in self.correct_cv_list_1]
                            self.correct_stdev_1 = statistics.stdev(self.correct_lat_1)
                            self.tableWidget.setItem(2, 27,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_stdev_1)))
                            self.correct_mean_1 = statistics.mean(self.correct_lat_1)
                            self.tableWidget.setItem(2, 14,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_mean_1)))
                            self.correct_cv_1 = self.correct_stdev_1 / self.correct_mean_1
                            self.tableWidget.setItem(2, 13,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_cv_1)))
                        except:
                            pass
                    elif 'Incorrect_response' in str(string):
                        self.Incorrect_response_1 += 1
                        self.tableWidget.setItem(2, 18,
                                                 QtWidgets.QTableWidgetItem(str(self.Incorrect_response_1)))
                        try:
                            self.incorrect_latency_1 = time.time() - self.sample_start_time_1
                            self.incorrect_cv_list_1.append(self.incorrect_latency_1)
                            self.tableWidget.setItem(2, 33,
                                                     QtWidgets.QTableWidgetItem(str(self.incorrect_cv_list_1)))
                            self.incorrect_lat_1 = [float(i) for i in self.incorrect_cv_list_1]
                            self.incorrect_stdev_1 = statistics.stdev(self.incorrect_lat_1)
                            self.tableWidget.setItem(2, 28,
                                                     QtWidgets.QTableWidgetItem(str(self.incorrect_stdev_1)))
                            self.incorrect_mean_1 = statistics.mean(self.incorrect_lat_1)
                            self.tableWidget.setItem(2, 17,
                                                     QtWidgets.QTableWidgetItem(str(self.incorrect_mean_1)))
                            self.incorrect_cv_1 = self.incorrect_stdev_1 / self.incorrect_mean_1
                            self.tableWidget.setItem(2, 37,
                                                     QtWidgets.QTableWidgetItem(str(self.incorrect_cv_1)))
                        except:
                            pass
                    elif "iti_start_time" in str(string):
                        self.iti_start_time_1 = time.time()
                        self.tableWidget.setItem(2, 60,
                                                 QtWidgets.QTableWidgetItem(str(self.iti_start_time_1)))
                    elif 'Premature_response' in str(string):
                        self.Premature_response_1 += 1
                        self.tableWidget.setItem(2, 12,
                                                 QtWidgets.QTableWidgetItem(str(self.Premature_response_1)))
                        try:
                            self.premature_latency_latency_1 = time.time() - self.iti_start_time_1
                            self.premature_latency_cv_list_1.append(self.premature_latency_latency_1)
                            self.tableWidget.setItem(2, 34,
                                                     QtWidgets.QTableWidgetItem(str(self.premature_latency_cv_list_1)))
                            self.premature_latency_lat_1 = [float(i) for i in self.premature_latency_cv_list_1]
                            self.premature_latency_stdev_1 = statistics.stdev(self.premature_latency_lat_1)
                            self.tableWidget.setItem(2, 29,
                                                     QtWidgets.QTableWidgetItem(str(self.premature_latency_stdev_1)))
                            self.premature_latency_mean_1 = statistics.mean(self.premature_latency_lat_1)
                            self.tableWidget.setItem(2, 18,
                                                     QtWidgets.QTableWidgetItem(str(self.premature_latency_mean_1)))
                            self.premature_latency_cv_1 = self.premature_latency_stdev_1 / self.premature_latency_mean_1
                            self.tableWidget.setItem(2, 38,
                                                     QtWidgets.QTableWidgetItem(str(self.premature_latency_cv_1)))
                        except:
                            pass
                    elif 'Reward_taken' in str(string):
                        try:
                            self.reward_latancy_latency_1 = time.time() - self.correct_time_start_1
                            self.reward_latancy_cv_list_1.append(self.reward_latancy_latency_1)
                            self.tableWidget.setItem(2, 35,
                                                     QtWidgets.QTableWidgetItem(str(self.reward_latancy_cv_list_1)))
                            self.reward_latancy_lat_1 = [float(i) for i in self.reward_latancy_cv_list_1]
                            self.reward_latancy_stdev_1 = statistics.stdev(self.reward_latancy_lat_1)
                            self.tableWidget.setItem(2, 30,
                                                     QtWidgets.QTableWidgetItem(str(self.reward_latancy_stdev_1)))
                            self.reward_latancy_mean_1 = statistics.mean(self.reward_latancy_lat_1)
                            self.tableWidget.setItem(2, 9,
                                                     QtWidgets.QTableWidgetItem(str(self.reward_latancy_mean_1)))
                            self.reward_latancy_cv_1 = self.reward_latancy_stdev_1 / self.reward_latancy_mean_1
                            self.tableWidget.setItem(2, 39,
                                                     QtWidgets.QTableWidgetItem(str(self.reward_latancy_cv_1)))
                        except:
                            pass
                    elif 'omission' in str(string):
                        self.omission_1 += 1
                        self.tableWidget.setItem(2, 15,
                                                 QtWidgets.QTableWidgetItem(str(self.omission_1)))
                    elif 'perseverate' in str(string):
                        self.perseverate_1 += 1
                        self.tableWidget.setItem(2, 19,
                                                 QtWidgets.QTableWidgetItem(str(self.perseverate_1)))
                    elif 'attempts_dur_penalty' in str(string):
                        self.resp_timeout_1 += 1
                        self.tableWidget.setItem(2, 22,
                                                 QtWidgets.QTableWidgetItem(str(self.resp_timeout_1)))
                    elif 'receptacle_entries' in str(string):
                        self.Receptacle_entries_1 += 1
                        self.tableWidget.setItem(2, 20,
                                                 QtWidgets.QTableWidgetItem(str(self.Receptacle_entries_1)))
                    elif '5_poke_entries' in str(string):
                        self.Nosepokes_5poke_1 += 1
                        self.tableWidget.setItem(2, 21,
                                                 QtWidgets.QTableWidgetItem(str(self.Nosepokes_5poke_1)))
                    elif "Event Closing" in str(string):
                        self.tableWidget.setItem(2, 0,
                                                 QtWidgets.QTableWidgetItem(str(self.date)))
                    try:
                        self.Choice_state_1 = self.omission_1 + self.Correct_response_1 \
                                              + self.Incorrect_response_1 + self.Premature_response_1
                        self.tableWidget.setItem(2, 10,
                                                 QtWidgets.QTableWidgetItem(str(self.Choice_state_1)))
                        self.per_omission_1 = (self.omission_1 / (self.omission_1 + self.Correct_response_1
                                                                  + self.Incorrect_response_1)) * 100
                        self.tableWidget.setItem(2, 5,
                                                 QtWidgets.QTableWidgetItem(str(self.per_omission_1)))
                        self.per_accuracy_1 = (self.Correct_response_1 / (self.Correct_response_1
                                                                          + self.Incorrect_response_1)) * 100
                        self.tableWidget.setItem(2, 4,
                                                 QtWidgets.QTableWidgetItem(str(self.per_accuracy_1)))
                        self.per_correct_1 = (self.Correct_response_1 / (self.Correct_response_1
                                                                         + self.Incorrect_response_1
                                                                         + self.omission_1)) * 100
                        self.tableWidget.setItem(2, 6,
                                                 QtWidgets.QTableWidgetItem(str(self.per_correct_1)))
                        self.per_premature_1 = (self.Premature_response_1 / self.Choice_state_1) * 100
                        self.tableWidget.setItem(2, 8,
                                                 QtWidgets.QTableWidgetItem(str(self.per_premature_1)))
                        self.per_perseverate_1 = (self.perseverate_1 / self.Correct_response_1) * 100
                        self.tableWidget.setItem(2, 11,
                                                 QtWidgets.QTableWidgetItem(str(self.per_perseverate_1)))
                    except ZeroDivisionError:
                        pass

    def update_data_table_2(self, new_data_2):
        if new_data_2:
            for value in new_data_2:
                for string in value:
                    self.tableWidget.setItem(3, 0,
                                             QtWidgets.QTableWidgetItem(str(value[2])))
                    if "Sample_state" in str(string):
                        self.sample_start_time_2 = time.time()
                        self.tableWidget.setItem(3, 58,
                                                 QtWidgets.QTableWidgetItem(str(self.sample_start_time_2)))
                    elif "Correct_response" in str(string):
                        self.Correct_response_2 += 1
                        self.tableWidget.setItem(3, 7,
                                                 QtWidgets.QTableWidgetItem(str(self.Correct_response_2)))
                        try:
                            self.correct_latency_2 = time.time() - self.sample_start_time_2
                            self.correct_cv_list_2.append(self.correct_latency_2)
                            self.tableWidget.setItem(3, 32,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_cv_list_2)))
                            self.correct_time_start_2 = time.time()
                            self.tableWidget.setItem(3, 62,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_time_start_2)))
                            self.correct_lat_2 = [float(i) for i in self.correct_cv_list_2]
                            self.correct_stdev_2 = statistics.stdev(self.correct_lat_2)
                            self.tableWidget.setItem(3, 27,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_stdev_2)))
                            self.correct_mean_2 = statistics.mean(self.correct_lat_2)
                            self.tableWidget.setItem(3, 14,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_mean_2)))
                            self.correct_cv_2 = self.correct_stdev_2 / self.correct_mean_2
                            self.tableWidget.setItem(3, 13,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_cv_2)))
                        except:
                            pass
                    elif 'Incorrect_response' in str(string):
                        self.Incorrect_response_2 += 1
                        self.tableWidget.setItem(3, 18,
                                                 QtWidgets.QTableWidgetItem(str(self.Incorrect_response_2)))
                        try:
                            self.incorrect_latency_2 = time.time() - self.sample_start_time_2
                            self.incorrect_cv_list_2.append(self.incorrect_latency_2)
                            self.tableWidget.setItem(3, 33,
                                                     QtWidgets.QTableWidgetItem(str(self.incorrect_cv_list_2)))
                            self.incorrect_lat_2 = [float(i) for i in self.incorrect_cv_list_2]
                            self.incorrect_stdev_2 = statistics.stdev(self.incorrect_lat_2)
                            self.tableWidget.setItem(3, 28,
                                                     QtWidgets.QTableWidgetItem(str(self.incorrect_stdev_2)))
                            self.incorrect_mean_2 = statistics.mean(self.incorrect_lat_2)
                            self.tableWidget.setItem(3, 17,
                                                     QtWidgets.QTableWidgetItem(str(self.incorrect_mean_2)))
                            self.incorrect_cv_2 = self.incorrect_stdev_2 / self.incorrect_mean_2
                            self.tableWidget.setItem(3, 37,
                                                     QtWidgets.QTableWidgetItem(str(self.incorrect_cv_2)))
                        except:
                            pass
                    elif "iti_start_time" in str(string):
                        self.iti_start_time_2 = time.time()
                        self.tableWidget.setItem(3, 60,
                                                 QtWidgets.QTableWidgetItem(str(self.iti_start_time_2)))
                    elif 'Premature_response' in str(string):
                        self.Premature_response_2 += 1
                        self.tableWidget.setItem(3, 12,
                                                 QtWidgets.QTableWidgetItem(str(self.Premature_response_2)))
                        try:
                            self.premature_latency_latency_2 = time.time() - self.iti_start_time_2
                            self.premature_latency_cv_list_2.append(self.premature_latency_latency_2)
                            self.tableWidget.setItem(3, 34,
                                                     QtWidgets.QTableWidgetItem(str(self.premature_latency_cv_list_2)))
                            self.premature_latency_lat_2 = [float(i) for i in self.premature_latency_cv_list_2]
                            self.premature_latency_stdev_2 = statistics.stdev(self.premature_latency_lat_2)
                            self.tableWidget.setItem(3, 29,
                                                     QtWidgets.QTableWidgetItem(str(self.premature_latency_stdev_2)))
                            self.premature_latency_mean_2 = statistics.mean(self.premature_latency_lat_2)
                            self.tableWidget.setItem(3, 18,
                                                     QtWidgets.QTableWidgetItem(str(self.premature_latency_mean_2)))
                            self.premature_latency_cv_2 = self.premature_latency_stdev_2 / self.premature_latency_mean_2
                            self.tableWidget.setItem(3, 38,
                                                     QtWidgets.QTableWidgetItem(str(self.premature_latency_cv_2)))
                        except:
                            pass
                    elif 'Reward_taken' in str(string):
                        try:
                            self.reward_latancy_latency_2 = time.time() - self.correct_time_start_2
                            self.reward_latancy_cv_list_2.append(self.reward_latancy_latency_2)
                            self.tableWidget.setItem(3, 35,
                                                     QtWidgets.QTableWidgetItem(str(self.reward_latancy_cv_list_2)))
                            self.reward_latancy_lat_2 = [float(i) for i in self.reward_latancy_cv_list_2]
                            self.reward_latancy_stdev_2 = statistics.stdev(self.reward_latancy_lat_2)
                            self.tableWidget.setItem(3, 30,
                                                     QtWidgets.QTableWidgetItem(str(self.reward_latancy_stdev_2)))
                            self.reward_latancy_mean_2 = statistics.mean(self.reward_latancy_lat_2)
                            self.tableWidget.setItem(3, 9,
                                                     QtWidgets.QTableWidgetItem(str(self.reward_latancy_mean_2)))
                            self.reward_latancy_cv_2 = self.reward_latancy_stdev_2 / self.reward_latancy_mean_2
                            self.tableWidget.setItem(3, 39,
                                                     QtWidgets.QTableWidgetItem(str(self.reward_latancy_cv_2)))
                        except:
                            pass
                    elif 'omission' in str(string):
                        self.omission_2 += 1
                        self.tableWidget.setItem(3, 15,
                                                 QtWidgets.QTableWidgetItem(str(self.omission_2)))
                    elif 'perseverate' in str(string):
                        self.perseverate_2 += 1
                        self.tableWidget.setItem(3, 19,
                                                 QtWidgets.QTableWidgetItem(str(self.perseverate_2)))
                    elif 'attempts_dur_penalty' in str(string):
                        self.resp_timeout_2 += 1
                        self.tableWidget.setItem(3, 22,
                                                 QtWidgets.QTableWidgetItem(str(self.resp_timeout_2)))
                    elif 'receptacle_entries' in str(string):
                        self.Receptacle_entries_2 += 1
                        self.tableWidget.setItem(3, 20,
                                                 QtWidgets.QTableWidgetItem(str(self.Receptacle_entries_2)))
                    elif '5_poke_entries' in str(string):
                        self.Nosepokes_5poke_2 += 1
                        self.tableWidget.setItem(3, 21,
                                                 QtWidgets.QTableWidgetItem(str(self.Nosepokes_5poke_2)))
                    elif "Event Closing" in str(string):
                        self.tableWidget.setItem(3, 0,
                                                 QtWidgets.QTableWidgetItem(str(self.date)))
                    try:
                        self.Choice_state_2 = self.omission_2 + self.Correct_response_2 \
                                              + self.Incorrect_response_2 + self.Premature_response_2
                        self.tableWidget.setItem(3, 10,
                                                 QtWidgets.QTableWidgetItem(str(self.Choice_state_2)))
                        self.per_omission_2 = (self.omission_2 / (self.omission_2 + self.Correct_response_2
                                                                  + self.Incorrect_response_2)) * 100
                        self.tableWidget.setItem(3, 5,
                                                 QtWidgets.QTableWidgetItem(str(self.per_omission_2)))
                        self.per_accuracy_2 = (self.Correct_response_2 / (self.Correct_response_2
                                                                          + self.Incorrect_response_2)) * 100
                        self.tableWidget.setItem(3, 4,
                                                 QtWidgets.QTableWidgetItem(str(self.per_accuracy_2)))
                        self.per_correct_2 = (self.Correct_response_2 / (self.Correct_response_2
                                                                         + self.Incorrect_response_2
                                                                         + self.omission_2)) * 100
                        self.tableWidget.setItem(3, 6,
                                                 QtWidgets.QTableWidgetItem(str(self.per_correct_2)))
                        self.per_premature_2 = (self.Premature_response_2 / self.Choice_state_2) * 100
                        self.tableWidget.setItem(3, 8,
                                                 QtWidgets.QTableWidgetItem(str(self.per_premature_2)))
                        self.per_perseverate_2 = (self.perseverate_2 / self.Correct_response_2) * 100
                        self.tableWidget.setItem(3, 11,
                                                 QtWidgets.QTableWidgetItem(str(self.per_perseverate_2)))
                    except ZeroDivisionError:
                        pass

    def update_data_table_3(self, new_data_3):
        if new_data_3:
            for value in new_data_3:
                for string in value:
                    self.tableWidget.setItem(4, 0,
                                             QtWidgets.QTableWidgetItem(str(value[2])))
                    if "Sample_state" in str(string):
                        self.sample_start_time_3 = time.time()
                        self.tableWidget.setItem(4, 58,
                                                 QtWidgets.QTableWidgetItem(str(self.sample_start_time_3)))
                    elif "Correct_response" in str(string):
                        self.Correct_response_3 += 1
                        self.tableWidget.setItem(4, 7,
                                                 QtWidgets.QTableWidgetItem(str(self.Correct_response_3)))
                        try:
                            self.correct_latency_3 = time.time() - self.sample_start_time_3
                            self.correct_cv_list_3.append(self.correct_latency_3)
                            self.tableWidget.setItem(4, 32,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_cv_list_3)))
                            self.correct_time_start_3 = time.time()
                            self.tableWidget.setItem(4, 62,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_time_start_3)))
                            self.correct_lat_3 = [float(i) for i in self.correct_cv_list_3]
                            self.correct_stdev_3 = statistics.stdev(self.correct_lat_3)
                            self.tableWidget.setItem(4, 27,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_stdev_3)))
                            self.correct_mean_3 = statistics.mean(self.correct_lat_3)
                            self.tableWidget.setItem(4, 14,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_mean_3)))
                            self.correct_cv_3 = self.correct_stdev_3 / self.correct_mean_3
                            self.tableWidget.setItem(4, 13,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_cv_3)))
                        except:
                            pass
                    elif 'Incorrect_response' in str(string):
                        self.Incorrect_response_3 += 1
                        self.tableWidget.setItem(4, 18,
                                                 QtWidgets.QTableWidgetItem(str(self.Incorrect_response_3)))
                        try:
                            self.incorrect_latency_3 = time.time() - self.sample_start_time_3
                            self.incorrect_cv_list_3.append(self.incorrect_latency_3)
                            self.tableWidget.setItem(4, 33,
                                                     QtWidgets.QTableWidgetItem(str(self.incorrect_cv_list_3)))
                            self.incorrect_lat_3 = [float(i) for i in self.incorrect_cv_list_3]
                            self.incorrect_stdev_3 = statistics.stdev(self.incorrect_lat_3)
                            self.tableWidget.setItem(4, 28,
                                                     QtWidgets.QTableWidgetItem(str(self.incorrect_stdev_3)))
                            self.incorrect_mean_3 = statistics.mean(self.incorrect_lat_3)
                            self.tableWidget.setItem(4, 17,
                                                     QtWidgets.QTableWidgetItem(str(self.incorrect_mean_3)))
                            self.incorrect_cv_3 = self.incorrect_stdev_3 / self.incorrect_mean_3
                            self.tableWidget.setItem(4, 37,
                                                     QtWidgets.QTableWidgetItem(str(self.incorrect_cv_3)))
                        except:
                            pass
                    elif "iti_start_time" in str(string):
                        self.iti_start_time_3 = time.time()
                        self.tableWidget.setItem(4, 60,
                                                 QtWidgets.QTableWidgetItem(str(self.iti_start_time_3)))
                    elif 'Premature_response' in str(string):
                        self.Premature_response_3 += 1
                        self.tableWidget.setItem(4, 12,
                                                 QtWidgets.QTableWidgetItem(str(self.Premature_response_3)))
                        try:
                            self.premature_latency_latency_3 = time.time() - self.iti_start_time_3
                            self.premature_latency_cv_list_3.append(self.premature_latency_latency_3)
                            self.tableWidget.setItem(4, 34,
                                                     QtWidgets.QTableWidgetItem(str(self.premature_latency_cv_list_3)))
                            self.premature_latency_lat_3 = [float(i) for i in self.premature_latency_cv_list_3]
                            self.premature_latency_stdev_3 = statistics.stdev(self.premature_latency_lat_3)
                            self.tableWidget.setItem(4, 29,
                                                     QtWidgets.QTableWidgetItem(str(self.premature_latency_stdev_3)))
                            self.premature_latency_mean_3 = statistics.mean(self.premature_latency_lat_3)
                            self.tableWidget.setItem(4, 18,
                                                     QtWidgets.QTableWidgetItem(str(self.premature_latency_mean_3)))
                            self.premature_latency_cv_3 = self.premature_latency_stdev_3 / self.premature_latency_mean_3
                            self.tableWidget.setItem(4, 38,
                                                     QtWidgets.QTableWidgetItem(str(self.premature_latency_cv_3)))
                        except:
                            pass
                    elif 'Reward_taken' in str(string):
                        try:
                            self.reward_latancy_latency_3 = time.time() - self.correct_time_start_3
                            self.reward_latancy_cv_list_3.append(self.reward_latancy_latency_3)
                            self.tableWidget.setItem(4, 35,
                                                     QtWidgets.QTableWidgetItem(str(self.reward_latancy_cv_list_3)))
                            self.reward_latancy_lat_3 = [float(i) for i in self.reward_latancy_cv_list_3]
                            self.reward_latancy_stdev_3 = statistics.stdev(self.reward_latancy_lat_3)
                            self.tableWidget.setItem(4, 30,
                                                     QtWidgets.QTableWidgetItem(str(self.reward_latancy_stdev_3)))
                            self.reward_latancy_mean_3 = statistics.mean(self.reward_latancy_lat_3)
                            self.tableWidget.setItem(4, 9,
                                                     QtWidgets.QTableWidgetItem(str(self.reward_latancy_mean_3)))
                            self.reward_latancy_cv_3 = self.reward_latancy_stdev_3 / self.reward_latancy_mean_3
                            self.tableWidget.setItem(4, 39,
                                                     QtWidgets.QTableWidgetItem(str(self.reward_latancy_cv_3)))
                        except:
                            pass
                    elif 'omission' in str(string):
                        self.omission_3 += 1
                        self.tableWidget.setItem(4, 15,
                                                 QtWidgets.QTableWidgetItem(str(self.omission_3)))
                    elif 'perseverate' in str(string):
                        self.perseverate_3 += 1
                        self.tableWidget.setItem(4, 19,
                                                 QtWidgets.QTableWidgetItem(str(self.perseverate_3)))
                    elif 'attempts_dur_penalty' in str(string):
                        self.resp_timeout_3 += 1
                        self.tableWidget.setItem(4, 22,
                                                 QtWidgets.QTableWidgetItem(str(self.resp_timeout_3)))
                    elif 'receptacle_entries' in str(string):
                        self.Receptacle_entries_3 += 1
                        self.tableWidget.setItem(4, 20,
                                                 QtWidgets.QTableWidgetItem(str(self.Receptacle_entries_3)))
                    elif '5_poke_entries' in str(string):
                        self.Nosepokes_5poke_3 += 1
                        self.tableWidget.setItem(4, 21,
                                                 QtWidgets.QTableWidgetItem(str(self.Nosepokes_5poke_3)))
                    elif "Event Closing" in str(string):
                        self.tableWidget.setItem(4, 0,
                                                 QtWidgets.QTableWidgetItem(str(self.date)))
                    try:
                        self.Choice_state_3 = self.omission_3 + self.Correct_response_3 \
                                              + self.Incorrect_response_3 + self.Premature_response_3
                        self.tableWidget.setItem(4, 10,
                                                 QtWidgets.QTableWidgetItem(str(self.Choice_state_3)))
                        self.per_omission_3 = (self.omission_3 / (self.omission_3 + self.Correct_response_3
                                                                  + self.Incorrect_response_3)) * 100
                        self.tableWidget.setItem(4, 5,
                                                 QtWidgets.QTableWidgetItem(str(self.per_omission_3)))
                        self.per_accuracy_3 = (self.Correct_response_3 / (self.Correct_response_3
                                                                          + self.Incorrect_response_3)) * 100
                        self.tableWidget.setItem(4, 4,
                                                 QtWidgets.QTableWidgetItem(str(self.per_accuracy_3)))
                        self.per_correct_3 = (self.Correct_response_3 / (self.Correct_response_3
                                                                         + self.Incorrect_response_3
                                                                         + self.omission_3)) * 100
                        self.tableWidget.setItem(4, 6,
                                                 QtWidgets.QTableWidgetItem(str(self.per_correct_3)))
                        self.per_premature_3 = (self.Premature_response_3 / self.Choice_state_3) * 100
                        self.tableWidget.setItem(4, 8,
                                                 QtWidgets.QTableWidgetItem(str(self.per_premature_3)))
                        self.per_perseverate_3 = (self.perseverate_3 / self.Correct_response_3) * 100
                        self.tableWidget.setItem(4, 11,
                                                 QtWidgets.QTableWidgetItem(str(self.per_perseverate_3)))
                    except ZeroDivisionError:
                        pass

    def update_data_table_4(self, new_data_4):
        if new_data_4:
            for value in new_data_4:
                for string in value:
                    self.tableWidget.setItem(5, 0,
                                             QtWidgets.QTableWidgetItem(str(value[2])))
                    if "Sample_state" in str(string):
                        self.sample_start_time_4 = time.time()
                        self.tableWidget.setItem(5, 58,
                                                 QtWidgets.QTableWidgetItem(str(self.sample_start_time_4)))
                    elif "Correct_response" in str(string):
                        self.Correct_response_4 += 1
                        self.tableWidget.setItem(5, 7,
                                                 QtWidgets.QTableWidgetItem(str(self.Correct_response_4)))
                        try:
                            self.correct_latency_4 = time.time() - self.sample_start_time_4
                            self.correct_cv_list_4.append(self.correct_latency_4)
                            self.tableWidget.setItem(5, 32,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_cv_list_4)))
                            self.correct_time_start_4 = time.time()
                            self.tableWidget.setItem(5, 62,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_time_start_4)))
                            self.correct_lat_4 = [float(i) for i in self.correct_cv_list_4]
                            self.correct_stdev_4 = statistics.stdev(self.correct_lat_4)
                            self.tableWidget.setItem(5, 27,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_stdev_4)))
                            self.correct_mean_4 = statistics.mean(self.correct_lat_4)
                            self.tableWidget.setItem(5, 14,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_mean_4)))
                            self.correct_cv_4 = self.correct_stdev_4 / self.correct_mean_4
                            self.tableWidget.setItem(5, 13,
                                                     QtWidgets.QTableWidgetItem(str(self.correct_cv_4)))
                        except:
                            pass
                    elif 'Incorrect_response' in str(string):
                        self.Incorrect_response_4 += 1
                        self.tableWidget.setItem(5, 18,
                                                 QtWidgets.QTableWidgetItem(str(self.Incorrect_response_4)))
                        try:
                            self.incorrect_latency_4 = time.time() - self.sample_start_time_4
                            self.incorrect_cv_list_4.append(self.incorrect_latency_4)
                            self.tableWidget.setItem(5, 33,
                                                     QtWidgets.QTableWidgetItem(str(self.incorrect_cv_list_4)))
                            self.incorrect_lat_4 = [float(i) for i in self.incorrect_cv_list_4]
                            self.incorrect_stdev_4 = statistics.stdev(self.incorrect_lat_4)
                            self.tableWidget.setItem(5, 28,
                                                     QtWidgets.QTableWidgetItem(str(self.incorrect_stdev_4)))
                            self.incorrect_mean_4 = statistics.mean(self.incorrect_lat_4)
                            self.tableWidget.setItem(5, 17,
                                                     QtWidgets.QTableWidgetItem(str(self.incorrect_mean_4)))
                            self.incorrect_cv_4 = self.incorrect_stdev_4 / self.incorrect_mean_4
                            self.tableWidget.setItem(5, 37,
                                                     QtWidgets.QTableWidgetItem(str(self.incorrect_cv_4)))
                        except:
                            pass
                    elif "iti_start_time" in str(string):
                        self.iti_start_time_4 = time.time()
                        self.tableWidget.setItem(5, 60,
                                                 QtWidgets.QTableWidgetItem(str(self.iti_start_time_4)))
                    elif 'Premature_response' in str(string):
                        self.Premature_response_4 += 1
                        self.tableWidget.setItem(5, 12,
                                                 QtWidgets.QTableWidgetItem(str(self.Premature_response_4)))
                        try:
                            self.premature_latency_latency_4 = time.time() - self.iti_start_time_4
                            self.premature_latency_cv_list_4.append(self.premature_latency_latency_4)
                            self.tableWidget.setItem(5, 34,
                                                     QtWidgets.QTableWidgetItem(str(self.premature_latency_cv_list_4)))
                            self.premature_latency_lat_4 = [float(i) for i in self.premature_latency_cv_list_4]
                            self.premature_latency_stdev_4 = statistics.stdev(self.premature_latency_lat_4)
                            self.tableWidget.setItem(5, 29,
                                                     QtWidgets.QTableWidgetItem(str(self.premature_latency_stdev_4)))
                            self.premature_latency_mean_4 = statistics.mean(self.premature_latency_lat_4)
                            self.tableWidget.setItem(5, 18,
                                                     QtWidgets.QTableWidgetItem(str(self.premature_latency_mean_4)))
                            self.premature_latency_cv_4 = self.premature_latency_stdev_4 / self.premature_latency_mean_4
                            self.tableWidget.setItem(5, 38,
                                                     QtWidgets.QTableWidgetItem(str(self.premature_latency_cv_4)))
                        except:
                            pass
                    elif 'Reward_taken' in str(string):
                        try:
                            self.reward_latancy_latency_4 = time.time() - self.correct_time_start_4
                            self.reward_latancy_cv_list_4.append(self.reward_latancy_latency_4)
                            self.tableWidget.setItem(5, 35,
                                                     QtWidgets.QTableWidgetItem(str(self.reward_latancy_cv_list_4)))
                            self.reward_latancy_lat_4 = [float(i) for i in self.reward_latancy_cv_list_4]
                            self.reward_latancy_stdev_4 = statistics.stdev(self.reward_latancy_lat_4)
                            self.tableWidget.setItem(5, 30,
                                                     QtWidgets.QTableWidgetItem(str(self.reward_latancy_stdev_4)))
                            self.reward_latancy_mean_4 = statistics.mean(self.reward_latancy_lat_4)
                            self.tableWidget.setItem(5, 9,
                                                     QtWidgets.QTableWidgetItem(str(self.reward_latancy_mean_4)))
                            self.reward_latancy_cv_4 = self.reward_latancy_stdev_4 / self.reward_latancy_mean_4
                            self.tableWidget.setItem(5, 39,
                                                     QtWidgets.QTableWidgetItem(str(self.reward_latancy_cv_4)))
                        except:
                            pass
                    elif 'omission' in str(string):
                        self.omission_4 += 1
                        self.tableWidget.setItem(5, 15,
                                                 QtWidgets.QTableWidgetItem(str(self.omission_4)))
                    elif 'perseverate' in str(string):
                        self.perseverate_4 += 1
                        self.tableWidget.setItem(5, 19,
                                                 QtWidgets.QTableWidgetItem(str(self.perseverate_4)))
                    elif 'attempts_dur_penalty' in str(string):
                        self.resp_timeout_4 += 1
                        self.tableWidget.setItem(5, 22,
                                                 QtWidgets.QTableWidgetItem(str(self.resp_timeout_4)))
                    elif 'receptacle_entries' in str(string):
                        self.Receptacle_entries_4 += 1
                        self.tableWidget.setItem(5, 20,
                                                 QtWidgets.QTableWidgetItem(str(self.Receptacle_entries_4)))
                    elif '5_poke_entries' in str(string):
                        self.Nosepokes_5poke_4 += 1
                        self.tableWidget.setItem(5, 21,
                                                 QtWidgets.QTableWidgetItem(str(self.Nosepokes_5poke_4)))
                    elif "Event Closing" in str(string):
                        self.tableWidget.setItem(5, 0,
                                                 QtWidgets.QTableWidgetItem(str(self.date)))
                    try:
                        self.Choice_state_4 = self.omission_4 + self.Correct_response_4 \
                                              + self.Incorrect_response_4 + self.Premature_response_4
                        self.tableWidget.setItem(5, 10,
                                                 QtWidgets.QTableWidgetItem(str(self.Choice_state_4)))
                        self.per_omission_4 = (self.omission_4 / (self.omission_4 + self.Correct_response_4
                                                                  + self.Incorrect_response_4)) * 100
                        self.tableWidget.setItem(5, 5,
                                                 QtWidgets.QTableWidgetItem(str(self.per_omission_4)))
                        self.per_accuracy_4 = (self.Correct_response_4 / (self.Correct_response_4
                                                                          + self.Incorrect_response_4)) * 100
                        self.tableWidget.setItem(5, 4,
                                                 QtWidgets.QTableWidgetItem(str(self.per_accuracy_4)))
                        self.per_correct_4 = (self.Correct_response_4 / (self.Correct_response_4
                                                                         + self.Incorrect_response_4
                                                                         + self.omission_4)) * 100
                        self.tableWidget.setItem(5, 6,
                                                 QtWidgets.QTableWidgetItem(str(self.per_correct_4)))
                        self.per_premature_4 = (self.Premature_response_4 / self.Choice_state_4) * 100
                        self.tableWidget.setItem(5, 8,
                                                 QtWidgets.QTableWidgetItem(str(self.per_premature_4)))
                        self.per_perseverate_4 = (self.perseverate_4 / self.Correct_response_4) * 100
                        self.tableWidget.setItem(5, 11,
                                                 QtWidgets.QTableWidgetItem(str(self.per_perseverate_4)))
                    except ZeroDivisionError:
                        pass

    def items_clear(self):
        self.tableWidget.clearContents()
        self.lcdNumber_Timer_BOX1.display(0)
        self.lcdNumber_Timer_BOX2.display(0)
        self.lcdNumber_Timer_BOX3.display(0)
        self.lcdNumber_Timer_BOX4.display(0)
        self.Correct_response_1 = 0
        self.correct_latency_1 = 0
        self.correct_cv_list_1 = []
        self.correct_lat_1 = 0
        self.correct_stdev_1 = 0
        self.correct_mean_1 = 0
        self.correct_cv_1 = 0
        self.Incorrect_response_1 = 0
        self.incorrect_latency_1 = 0
        self.incorrect_cv_list_1 = []
        self.incorrect_lat_1 = 0
        self.incorrect_stdev_1 = 0
        self.incorrect_mean_1 = 0
        self.incorrect_cv_1 = 0
        self.Premature_response_1 = 0
        self.premature_latency_latency_1 = 0
        self.premature_latency_cv_list_1 = []
        self.premature_latency_lat_1 = 0
        self.premature_latency_stdev_1 = 0
        self.premature_latency_mean_1 = 0
        self.premature_latency_cv_1 = 0
        self.reward_latancy_latency_1 = 0
        self.reward_latancy_cv_list_1 = []
        self.reward_latancy_lat_1 = 0
        self.reward_latancy_stdev_1 = 0
        self.reward_latancy_mean_1 = 0
        self.reward_latancy_cv_1 = 0
        self.omission_1 = 0
        self.perseverate_1 = 0
        self.resp_timeout_1 = 0
        self.Receptacle_entries_1 = 0
        self.Nosepokes_5poke_1 = 0
        self.Choice_state_1 = 0
        self.per_omission_1 = 0
        self.per_accuracy_1 = 0
        self.per_correct_1 = 0
        self.per_premature_1 = 0
        self.per_perseverate_1 = 0
        self.Correct_response_2 = 0
        self.correct_latency_2 = 0
        self.correct_cv_list_2 = []
        self.correct_lat_2 = 0
        self.correct_stdev_2 = 0
        self.correct_mean_2 = 0
        self.correct_cv_2 = 0
        self.Incorrect_response_2 = 0
        self.incorrect_latency_2 = 0
        self.incorrect_cv_list_2 = []
        self.incorrect_lat_2 = 0
        self.incorrect_stdev_2 = 0
        self.incorrect_mean_2 = 0
        self.incorrect_cv_2 = 0
        self.Premature_response_2 = 0
        self.premature_latency_latency_2 = 0
        self.premature_latency_cv_list_2 = []
        self.premature_latency_lat_2 = 0
        self.premature_latency_stdev_2 = 0
        self.premature_latency_mean_2 = 0
        self.premature_latency_cv_2 = 0
        self.reward_latancy_latency_2 = 0
        self.reward_latancy_cv_list_2 = []
        self.reward_latancy_lat_2 = 0
        self.reward_latancy_stdev_2 = 0
        self.reward_latancy_mean_2 = 0
        self.reward_latancy_cv_2 = 0
        self.omission_2 = 0
        self.perseverate_2 = 0
        self.resp_timeout_2 = 0
        self.Receptacle_entries_2 = 0
        self.Nosepokes_5poke_2 = 0
        self.Choice_state_2 = 0
        self.per_omission_2 = 0
        self.per_accuracy_2 = 0
        self.per_correct_2 = 0
        self.per_premature_2 = 0
        self.per_perseverate_2 = 0
        self.Correct_response_3 = 0
        self.correct_latency_3 = 0
        self.correct_cv_list_3 = []
        self.correct_lat_3 = 0
        self.correct_stdev_3 = 0
        self.correct_mean_3 = 0
        self.correct_cv_3 = 0
        self.Incorrect_response_3 = 0
        self.incorrect_latency_3 = 0
        self.incorrect_cv_list_3 = []
        self.incorrect_lat_3 = 0
        self.incorrect_stdev_3 = 0
        self.incorrect_mean_3 = 0
        self.incorrect_cv_3 = 0
        self.Premature_response_3 = 0
        self.premature_latency_latency_3 = 0
        self.premature_latency_cv_list_3 = []
        self.premature_latency_lat_3 = 0
        self.premature_latency_stdev_3 = 0
        self.premature_latency_mean_3 = 0
        self.premature_latency_cv_3 = 0
        self.reward_latancy_latency_3 = 0
        self.reward_latancy_cv_list_3 = []
        self.reward_latancy_lat_3 = 0
        self.reward_latancy_stdev_3 = 0
        self.reward_latancy_mean_3 = 0
        self.reward_latancy_cv_3 = 0
        self.omission_3 = 0
        self.perseverate_3 = 0
        self.resp_timeout_3 = 0
        self.Receptacle_entries_3 = 0
        self.Nosepokes_5poke_3 = 0
        self.Choice_state_3 = 0
        self.per_omission_3 = 0
        self.per_accuracy_3 = 0
        self.per_correct_3 = 0
        self.per_premature_3 = 0
        self.per_perseverate_3 = 0
        self.Correct_response_4 = 0
        self.correct_latency_4 = 0
        self.correct_cv_list_4 = []
        self.correct_lat_4 = 0
        self.correct_stdev_4 = 0
        self.correct_mean_4 = 0
        self.correct_cv_4 = 0
        self.Incorrect_response_4 = 0
        self.incorrect_latency_4 = 0
        self.incorrect_cv_list_4 = []
        self.incorrect_lat_4 = 0
        self.incorrect_stdev_4 = 0
        self.incorrect_mean_4 = 0
        self.incorrect_cv_4 = 0
        self.Premature_response_4 = 0
        self.premature_latency_latency_4 = 0
        self.premature_latency_cv_list_4 = []
        self.premature_latency_lat_4 = 0
        self.premature_latency_stdev_4 = 0
        self.premature_latency_mean_4 = 0
        self.premature_latency_cv_4 = 0
        self.reward_latancy_latency_4 = 0
        self.reward_latancy_cv_list_4 = []
        self.reward_latancy_lat_4 = 0
        self.reward_latancy_stdev_4 = 0
        self.reward_latancy_mean_4 = 0
        self.reward_latancy_cv_4 = 0
        self.omission_4 = 0
        self.perseverate_4 = 0
        self.resp_timeout_4 = 0
        self.Receptacle_entries_4 = 0
        self.Nosepokes_5poke_4 = 0
        self.Choice_state_4 = 0
        self.per_omission_4 = 0
        self.per_accuracy_4 = 0
        self.per_correct_4 = 0
        self.per_premature_4 = 0
        self.per_perseverate_4 = 0
        self.sample_start_time_1 = 0
        self.iti_start_time_1 = 0
        self.sample_start_time_2 = 0
        self.iti_start_time_2 = 0
        self.sample_start_time_3 = 0
        self.iti_start_time_3 = 0
        self.sample_start_time_4 = 0
        self.iti_start_time_4 = 0
        self.sample_start_time_5 = 0
        self.lineEdit_subid1.clear()
        self.lineEdit_subid2.clear()
        self.lineEdit_subid3.clear()
        self.lineEdit_subid4.clear()

    def refresh(self):
        # Called regularly when not running to update tasks and ports.
        self.scan_tasks()
        self.scan_ports()

    def save_file(self):
        self.resettable.setEnabled(True)
        path = QtGui.QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                for row in range(self.tableWidget.rowCount()):
                    row_data = []
                    for column in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append(' ')
                    writer.writerow(row_data)

    # Cleanup.
    def closeEvent(self, event):
        # Called when GUI window is closed.
        if self.board_1:
            self.board_1.stop_framework()
            self.board_1.close()
        elif self.board_2:
            self.board_2.stop_framework()
            self.board_2.close()
        elif self.board_3:
            self.board_3.stop_framework()
            self.board_3.close()
        elif self.board_4:
            self.board_4.stop_framework()
            self.board_4.close()
        event.accept()


# Main ----------------------------------------------------------------

if __name__ == '__main__':
    try:
        print('Starting Application')
        app = QtWidgets.QApplication(sys.argv)
        gui_app = MainGui()
        gui_app.show()
        app.exec_()
    except RuntimeError as error:
        print('-' * 150)
        print(error)
        print('-' * 150)
    except BaseException as error:
        print('-' * 150)
        print(error)
        print('-' * 150)
    finally:
        print('Exiting Application')
