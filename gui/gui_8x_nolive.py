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
        self.setWindowTitle('SK + KEI GUI for pyControl Behavior')
        self.setFixedSize(1500, 750)
        # Variables.
        #self.board = None
        #self.text_edit_widget = None
        self.board_1 = None  # Pycboard class instance.
        self.board_2 = None  # Pycboard class instance.
        self.board_3 = None  # Pycboard class instance.
        self.board_4 = None  # Pycboard class instance.
        self.board_5 = None  # Pycboard class instance.
        self.board_6 = None  # Pycboard class instance.
        self.board_7 = None  # Pycboard class instance.
        self.board_8 = None  # Pycboard class instance.

        self.task = None  # Pycboard class instance.
        self.task_1 = None  # Task currently uploaded on pyboard.
        self.task_2 = None  # Task currently uploaded on pyboard.
        self.task_3 = None  # Task currently uploaded on pyboard.
        self.task_4 = None  # Task currently uploaded on pyboard.
        self.task_5 = None  # Task currently uploaded on pyboard.
        self.task_6 = None  # Task currently uploaded on pyboard.
        self.task_7 = None  # Task currently uploaded on pyboard.
        self.task_8 = None  # Task currently uploaded on pyboard.
         # Task currently uploaded on pyboard.
        self.task_hash_1 = None  # Used to check if file has changed.
        self.task_hash_2 = None  # Used to check if file has changed.
        self.task_hash_3 = None  # Used to check if file has changed.
        self.task_hash_4 = None  # Used to check if file has changed.
        self.task_hash_5 = None  # Used to check if file has changed.
        self.task_hash_6 = None  # Used to check if file has changed.
        self.task_hash_7 = None  # Used to check if file has changed.
        self.task_hash_8 = None  # Used to check if file has changed.
         # Used to check if file has changed.
        self.sm_info_1 = None  # Information about current state machine.
        self.sm_info_2 = None  # Information about current state machine.
        self.sm_info_3 = None  # Information about current state machine.
        self.sm_info_4 = None  # Information about current state machine.
        self.sm_info_5 = None  # Information about current state machine.
        self.sm_info_6 = None  # Information about current state machine.
        self.sm_info_7 = None  # Information about current state machine.
        self.sm_info_8 = None  # Information about current state machine.
         #Information about current state machine.
        self.data_dir = None  # data directory
        self.subject_id_1 = None
        self.subject_id_2 = None
        self.subject_id_3 = None
        self.subject_id_4 = None
        self.subject_id_5 = None
        self.subject_id_6 = None
        self.subject_id_7 = None
        self.subject_id_8 = None

        self.exp_name = None  # experimenter name
        self.project = None

        self.data_logger1 = Data_logger(print_func=self.print_to_log)
        self.data_logger2 = Data_logger(print_func=self.print_to_log)
        self.data_logger3 = Data_logger(print_func=self.print_to_log)
        self.data_logger4 = Data_logger(print_func=self.print_to_log)
        self.data_logger5 = Data_logger(print_func=self.print_to_log)
        self.data_logger6 = Data_logger(print_func=self.print_to_log)
        self.data_logger7 = Data_logger(print_func=self.print_to_log)
        self.data_logger8 = Data_logger(print_func=self.print_to_log)

        self.connected_1 = False  # Whether gui is connected to pyboard.
        self.connected_2 = False  # Whether gui is connected to pyboard.
        self.connected_3 = False  # Whether gui is connected to pyboard.
        self.connected_4 = False  # Whether gui is connected to pyboard.
        self.connected_5 = False  # Whether gui is connected to pyboard.
        self.connected_6 = False  # Whether gui is connected to pyboard.
        self.connected_7 = False  # Whether gui is connected to pyboard.
        self.connected_8 = False  # Whether gui is connected to pyboard.

        self.uploaded_1 = False  # Whether selected task is on board.
        self.uploaded_2 = False  # Whether selected task is on board.
        self.uploaded_3 = False  # Whether selected task is on board.
        self.uploaded_4 = False  # Whether selected task is on board.
        self.uploaded_5 = False  # Whether selected task is on board.
        self.uploaded_6 = False  # Whether selected task is on board.
        self.uploaded_7 = False  # Whether selected task is on board.
        self.uploaded_8 = False  # Whether selected task is on board.

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
        self.pushButton_connect_5.clicked.connect(
            lambda: self.disconnect_5() if self.connected_1 else self.connect_5())
        self.pushButton_connect_6.clicked.connect(
            lambda: self.disconnect_6() if self.connected_6 else self.connect_6())
        self.pushButton_connect_7.clicked.connect(
            lambda: self.disconnect_7() if self.connected_7 else self.connect_7())
        self.pushButton_connect_8.clicked.connect(
            lambda: self.disconnect_8() if self.connected_8 else self.connect_8())

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
        self.pushButton_config_5.clicked.connect(
            lambda: self.Board_config_dialog_5.exec_())
        self.pushButton_config_6.clicked.connect(
            lambda: self.Board_config_dialog_6.exec_())
        self.pushButton_config_7.clicked.connect(
            lambda: self.Board_config_dialog_7.exec_())
        self.pushButton_config_8.clicked.connect(
            lambda: self.Board_config_dialog_8.exec_())

        self.pushButton_data_dir.clicked.connect(self.select_data_dir)
        self.pushButton_upload_1.clicked.connect(lambda: self.setup_task_1())
        self.pushButton_upload_2.clicked.connect(lambda: self.setup_task_2())
        self.pushButton_upload_3.clicked.connect(lambda: self.setup_task_3())
        self.pushButton_upload_4.clicked.connect(lambda: self.setup_task_4())
        self.pushButton_upload_5.clicked.connect(lambda: self.setup_task_5())
        self.pushButton_upload_6.clicked.connect(lambda: self.setup_task_6())
        self.pushButton_upload_7.clicked.connect(lambda: self.setup_task_7())
        self.pushButton_upload_8.clicked.connect(lambda: self.setup_task_8())

        self.pushButton_var1.clicked.connect(lambda x: self.variables_dialog_1.exec_())
        self.pushButton_var2.clicked.connect(lambda x: self.variables_dialog_2.exec_())
        self.pushButton_var3.clicked.connect(lambda x: self.variables_dialog_3.exec_())
        self.pushButton_var4.clicked.connect(lambda x: self.variables_dialog_4.exec_())
        self.pushButton_var5.clicked.connect(lambda x: self.variables_dialog_5.exec_())
        self.pushButton_var6.clicked.connect(lambda x: self.variables_dialog_6.exec_())
        self.pushButton_var7.clicked.connect(lambda x: self.variables_dialog_7.exec_())
        self.pushButton_var8.clicked.connect(lambda x: self.variables_dialog_8.exec_())

        self.pushButton_Start1.clicked.connect(lambda: self.start_task_1())
        self.pushButton_Start2.clicked.connect(lambda: self.start_task_2())
        self.pushButton_Start3.clicked.connect(lambda: self.start_task_3())
        self.pushButton_Start4.clicked.connect(lambda: self.start_task_4())
        self.pushButton_Start5.clicked.connect(lambda: self.start_task_5())
        self.pushButton_Start6.clicked.connect(lambda: self.start_task_6())
        self.pushButton_Start7.clicked.connect(lambda: self.start_task_7())
        self.pushButton_Start8.clicked.connect(lambda: self.start_task_8())

        self.pushButton_Stop1.clicked.connect(lambda: self.stop_task_1())
        self.pushButton_Stop2.clicked.connect(lambda: self.stop_task_2())
        self.pushButton_Stop3.clicked.connect(lambda: self.stop_task_3())
        self.pushButton_Stop4.clicked.connect(lambda: self.stop_task_4())
        self.pushButton_Stop5.clicked.connect(lambda: self.stop_task_5())
        self.pushButton_Stop6.clicked.connect(lambda: self.stop_task_6())
        self.pushButton_Stop7.clicked.connect(lambda: self.stop_task_7())
        self.pushButton_Stop8.clicked.connect(lambda: self.stop_task_8())
          
          # LineEdit
        self.lineEdit_status_1.setReadOnly(True)
        self.lineEdit_status_2.setReadOnly(True)
        self.lineEdit_status_3.setReadOnly(True)
        self.lineEdit_status_4.setReadOnly(True)
        self.lineEdit_status_5.setReadOnly(True)
        self.lineEdit_status_6.setReadOnly(True)
        self.lineEdit_status_7.setReadOnly(True)
        self.lineEdit_status_8.setReadOnly(True)


        ####
        ####
        #### kei edits: thinking about how to expand to 12 boxes efficiently
        ####
        ####

        self.lineEdit_data_dir.setText(data_dir)

        self.lineEdit_data_dir.textChanged.connect(self.test_data_path_1)
        self.lineEdit_data_dir.textChanged.connect(self.test_data_path_2)
        self.lineEdit_data_dir.textChanged.connect(self.test_data_path_3)
        self.lineEdit_data_dir.textChanged.connect(self.test_data_path_4)
        self.lineEdit_data_dir.textChanged.connect(self.test_data_path_5)
        self.lineEdit_data_dir.textChanged.connect(self.test_data_path_6)
        self.lineEdit_data_dir.textChanged.connect(self.test_data_path_7)
        self.lineEdit_data_dir.textChanged.connect(self.test_data_path_8)

        self.lineEdit_subid1.textChanged.connect(self.test_data_path_1)
        self.lineEdit_subid2.textChanged.connect(self.test_data_path_2)
        self.lineEdit_subid3.textChanged.connect(self.test_data_path_3)
        self.lineEdit_subid4.textChanged.connect(self.test_data_path_4)
        self.lineEdit_subid1.textChanged.connect(self.test_data_path_5)
        self.lineEdit_subid2.textChanged.connect(self.test_data_path_6)
        self.lineEdit_subid3.textChanged.connect(self.test_data_path_7)
        self.lineEdit_subid4.textChanged.connect(self.test_data_path_8)

        self.comboBox_srport_1.setEditable(True)
        self.comboBox_srport_2.setEditable(True)
        self.comboBox_srport_3.setEditable(True)
        self.comboBox_srport_4.setEditable(True)
        self.comboBox_srport_5.setEditable(True)
        self.comboBox_srport_6.setEditable(True)
        self.comboBox_srport_7.setEditable(True)
        self.comboBox_srport_8.setEditable(True)

        # Graph Plotter
        # self.task_plot = Task_plotter()
        # Create dialogs.
        self.Board_config_dialog_1 = Board_config_dialog_1(parent=self)
        self.Board_config_dialog_2 = Board_config_dialog_2(parent=self)
        self.Board_config_dialog_3 = Board_config_dialog_3(parent=self)
        self.Board_config_dialog_4 = Board_config_dialog_4(parent=self)
        self.Board_config_dialog_5 = Board_config_dialog_5(parent=self)
        self.Board_config_dialog_6 = Board_config_dialog_6(parent=self)
        self.Board_config_dialog_7 = Board_config_dialog_7(parent=self)
        self.Board_config_dialog_8 = Board_config_dialog_8(parent=self)

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
        self.process_timer_5 = QtCore.QTimer()  # Timer to regularly call process_data() during run.
        self.process_timer_5.timeout.connect(self.process_data_5)
        self.refresh_timer_5 = QtCore.QTimer()  # Timer to regularly call refresh() when not running.
        self.refresh_timer_5.timeout.connect(self.refresh)
        self.process_timer_6 = QtCore.QTimer()  # Timer to regularly call process_data() during run.
        self.process_timer_6.timeout.connect(self.process_data_6)
        self.refresh_timer_6 = QtCore.QTimer()  # Timer to regularly call refresh() when not running.
        self.refresh_timer_6.timeout.connect(self.refresh)
        self.process_timer_7 = QtCore.QTimer()  # Timer to regularly call process_data() during run.
        self.process_timer_7.timeout.connect(self.process_data_7)
        self.refresh_timer_7 = QtCore.QTimer()  # Timer to regularly call refresh() when not running.
        self.refresh_timer_7.timeout.connect(self.refresh)
        self.process_timer_8 = QtCore.QTimer()  # Timer to regularly call process_data() during run.
        self.process_timer_8.timeout.connect(self.process_data_8)
        self.refresh_timer_8 = QtCore.QTimer()  # Timer to regularly call refresh() when not running.
        self.refresh_timer_8.timeout.connect(self.refresh)

        # Initial setup.
        self.disconnect_1()  # Set initial state as disconnected.
        self.disconnect_2()
        self.disconnect_3()
        self.disconnect_4()
        self.disconnect_5()  # Set initial state as disconnected.
        self.disconnect_6()
        self.disconnect_7()
        self.disconnect_8()


        self.refresh()
        # self.refresh()# Refresh tasks and ports lists.
        
        self.refresh_timer_1.start(self.refresh_interval)
        self.refresh_timer_2.start(self.refresh_interval)
        self.refresh_timer_3.start(self.refresh_interval)
        self.refresh_timer_4.start(self.refresh_interval)
        self.refresh_timer_5.start(self.refresh_interval)
        self.refresh_timer_6.start(self.refresh_interval)
        self.refresh_timer_7.start(self.refresh_interval)
        self.refresh_timer_8.start(self.refresh_interval)
        
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

        self.sample_start_time_5 = 0
        self.iti_start_time_5 = 0
        self.sample_start_time_6 = 0
        self.iti_start_time_6 = 0
        self.sample_start_time_7 = 0
        self.iti_start_time_7 = 0
        self.sample_start_time_8 = 0
        self.iti_start_time_8 = 0

        self.correct_time_start_5 = 0
        self.correct_time_start_6 = 0
        self.correct_time_start_7 = 0
        self.correct_time_start_8 = 0

        self.Correct_response_5 = 0
        self.correct_latency_5 = 0
        self.correct_cv_list_5 = []
        self.correct_lat_5 = 0
        self.correct_stdev_5 = 0
        self.correct_mean_5 = 0
        self.correct_cv_5 = 0
        self.Incorrect_response_5 = 0
        self.incorrect_latency_5 = 0
        self.incorrect_cv_list_5 = []
        self.incorrect_lat_5 = 0
        self.incorrect_stdev_5 = 0
        self.incorrect_mean_5 = 0
        self.incorrect_cv_5 = 0
        self.Premature_response_5 = 0
        self.premature_latency_latency_5 = 0
        self.premature_latency_cv_list_5 = []
        self.premature_latency_lat_5 = 0
        self.premature_latency_stdev_5 = 0
        self.premature_latency_mean_5 = 0
        self.premature_latency_cv_5 = 0
        self.reward_latancy_latency_5 = 0
        self.reward_latancy_cv_list_5 = []
        self.reward_latancy_lat_5 = 0
        self.reward_latancy_stdev_5 = 0
        self.reward_latancy_mean_5 = 0
        self.reward_latancy_cv_5 = 0
        self.omission_5 = 0
        self.perseverate_5 = 0
        self.resp_timeout_5 = 0
        self.Receptacle_entries_5 = 0
        self.Nosepokes_5poke_5 = 0
        self.Choice_state_5 = 0
        self.per_omission_5 = 0
        self.per_accuracy_5 = 0
        self.per_correct_5 = 0
        self.per_premature_5 = 0
        self.per_perseverate_5 = 0

        self.Correct_response_6 = 0
        self.correct_latency_6 = 0
        self.correct_cv_list_6 = []
        self.correct_lat_6 = 0
        self.correct_stdev_6 = 0
        self.correct_mean_6 = 0
        self.correct_cv_6 = 0
        self.Incorrect_response_6 = 0
        self.incorrect_latency_6 = 0
        self.incorrect_cv_list_6 = []
        self.incorrect_lat_6 = 0
        self.incorrect_stdev_6 = 0
        self.incorrect_mean_6 = 0
        self.incorrect_cv_6 = 0
        self.Premature_response_6 = 0
        self.premature_latency_latency_6 = 0
        self.premature_latency_cv_list_6 = []
        self.premature_latency_lat_6 = 0
        self.premature_latency_stdev_6 = 0
        self.premature_latency_mean_6 = 0
        self.premature_latency_cv_6 = 0
        self.reward_latancy_latency_6 = 0
        self.reward_latancy_cv_list_6 = []
        self.reward_latancy_lat_6 = 0
        self.reward_latancy_stdev_6 = 0
        self.reward_latancy_mean_6 = 0
        self.reward_latancy_cv_6 = 0
        self.omission_6 = 0
        self.perseverate_6 = 0
        self.resp_timeout_6 = 0
        self.Receptacle_entries_6 = 0
        self.Nosepokes_5poke_6 = 0
        self.Choice_state_6 = 0
        self.per_omission_6 = 0
        self.per_accuracy_6 = 0
        self.per_correct_6 = 0
        self.per_premature_6 = 0
        self.per_perseverate_6 = 0

        self.Correct_response_7 = 0
        self.correct_latency_7 = 0
        self.correct_cv_list_7 = []
        self.correct_lat_7 = 0
        self.correct_stdev_7 = 0
        self.correct_mean_7 = 0
        self.correct_cv_7 = 0
        self.Incorrect_response_7 = 0
        self.incorrect_latency_7 = 0
        self.incorrect_cv_list_7 = []
        self.incorrect_lat_7 = 0
        self.incorrect_stdev_7 = 0
        self.incorrect_mean_7 = 0
        self.incorrect_cv_7 = 0
        self.Premature_response_7 = 0
        self.premature_latency_latency_7 = 0
        self.premature_latency_cv_list_7 = []
        self.premature_latency_lat_7 = 0
        self.premature_latency_stdev_7 = 0
        self.premature_latency_mean_7 = 0
        self.premature_latency_cv_7 = 0
        self.reward_latancy_latency_7 = 0
        self.reward_latancy_cv_list_7 = []
        self.reward_latancy_lat_7 = 0
        self.reward_latancy_stdev_7 = 0
        self.reward_latancy_mean_7 = 0
        self.reward_latancy_cv_7 = 0
        self.omission_7 = 0
        self.perseverate_7 = 0
        self.resp_timeout_7 = 0
        self.Receptacle_entries_7 = 0
        self.Nosepokes_5poke_7 = 0
        self.Choice_state_7 = 0
        self.per_omission_7 = 0
        self.per_accuracy_7 = 0
        self.per_correct_7 = 0
        self.per_premature_7 = 0
        self.per_perseverate_7 = 0

        self.Correct_response_8 = 0
        self.correct_latency_8 = 0
        self.correct_cv_list_8 = []
        self.correct_lat_8 = 0
        self.correct_stdev_8 = 0
        self.correct_mean_8 = 0
        self.correct_cv_8 = 0
        self.Incorrect_response_8 = 0
        self.incorrect_latency_8 = 0
        self.incorrect_cv_list_8 = []
        self.incorrect_lat_8 = 0
        self.incorrect_stdev_8 = 0
        self.incorrect_mean_8 = 0
        self.incorrect_cv_8 = 0
        self.Premature_response_8 = 0
        self.premature_latency_latency_8 = 0
        self.premature_latency_cv_list_8 = []
        self.premature_latency_lat_8 = 0
        self.premature_latency_stdev_8 = 0
        self.premature_latency_mean_8 = 0
        self.premature_latency_cv_8 = 0
        self.reward_latancy_latency_8 = 0
        self.reward_latancy_cv_list_8 = []
        self.reward_latancy_lat_8 = 0
        self.reward_latancy_stdev_8 = 0
        self.reward_latancy_mean_8 = 0
        self.reward_latancy_cv_8 = 0
        self.omission_8 = 0
        self.perseverate_8 = 0
        self.resp_timeout_8 = 0
        self.Receptacle_entries_8 = 0
        self.Nosepokes_5poke_8 = 0
        self.Choice_state_8 = 0
        self.per_omission_8 = 0
        self.per_accuracy_8 = 0
        self.per_correct_8 = 0
        self.per_premature_8 = 0
        self.per_perseverate_8 = 0

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

    def clear_task_combo_box(self):
        self.comboBox_task5.clear()
        self.comboBox_task6.clear()
        self.comboBox_task7.clear()
        self.comboBox_task8.clear()

    def clear_srport_combo_box(self):
        self.comboBox_srport_5.clear()
        self.comboBox_srport_6.clear()
        self.comboBox_srport_7.clear()
        self.comboBox_srport_8.clear()

    def add_to_srport_combo_box(self, ports):
        self.comboBox_srport_5.addItems(sorted(ports))
        self.comboBox_srport_6.addItems(sorted(ports))
        self.comboBox_srport_7.addItems(sorted(ports))
        self.comboBox_srport_8.addItems(sorted(ports))

    def enable_srport_combo_box(self, state):
        self.comboBox_srport_5.setEnabled(state)
        self.comboBox_srport_6.setEnabled(state)
        self.comboBox_srport_7.setEnabled(state)
        self.comboBox_srport_8.setEnabled(state)

    def enable_task_combo_box(self, state):
        self.comboBox_task5.setEnabled(state)
        self.comboBox_task6.setEnabled(state)
        self.comboBox_task7.setEnabled(state)
        self.comboBox_task8.setEnabled(state)

    def combo_box_add_items(self, tasks):
        self.comboBox_task5.addItems(sorted(tasks))
        self.comboBox_task6.addItems(sorted(tasks))
        self.comboBox_task7.addItems(sorted(tasks))
        self.comboBox_task8.addItems(sorted(tasks))

    def disable_widgets(self):
        self.lineEdit_subid5.setEnabled(True)
        self.pushButton_Start5.setEnabled(False)
        self.pushButton_Stop5.setEnabled(False)
        self.pushButton_upload_5.setEnabled(False)
        self.comboBox_task5.setEnabled(False)
        self.pushButton_var5.setEnabled(False)
        self.pushButton_config_5.setEnabled(False)
        self.lineEdit_status_5.setEnabled(False)

        self.pushButton_Start6.setEnabled(False)
        self.pushButton_Stop6.setEnabled(False)
        self.pushButton_upload_6.setEnabled(False)
        self.lineEdit_subid6.setEnabled(True)
        self.comboBox_task6.setEnabled(False)
        self.pushButton_var6.setEnabled(False)
        self.pushButton_config_6.setEnabled(False)
        self.lineEdit_status_6.setEnabled(False)

        self.pushButton_Start7.setEnabled(False)
        self.pushButton_Stop7.setEnabled(False)
        self.pushButton_upload_7.setEnabled(False)
        self.lineEdit_subid7.setEnabled(True)
        self.comboBox_task7.setEnabled(False)
        self.pushButton_var7.setEnabled(False)
        self.pushButton_config_7.setEnabled(False)
        self.lineEdit_status_7.setEnabled(False)
        
        self.pushButton_Start8.setEnabled(False)
        self.pushButton_Stop8.setEnabled(False)
        self.pushButton_upload_8.setEnabled(False)
        self.lineEdit_subid8.setEnabled(True)
        self.comboBox_task8.setEnabled(False)
        self.pushButton_var8.setEnabled(False)
        self.pushButton_config_8.setEnabled(False)
        self.lineEdit_status_8.setEnabled(False)
        self.pushButton_data_dir.setEnabled(True)

    def enable_widgets(self, com_list):
        if len(com_list) == 5:
            self.comboBox_srport_5.setEnabled(True)
            self.pushButton_connect_5.setEnabled(True)
        if len(com_list) == 6:
            self.comboBox_srport_6.setEnabled(True)
            self.pushButton_connect_6.setEnabled(True)
        if len(com_list) == 7:
            self.comboBox_srport_7.setEnabled(True)
            self.pushButton_connect_7.setEnabled(True)
        if len(com_list) == 8:
            self.comboBox_srport_8.setEnabled(True)
            self.pushButton_connect_8.setEnabled(True)

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
        
        self.tableWidget.setItem(6, 1,
                                 QtWidgets.QTableWidgetItem(str('BOX-5')))
        self.tableWidget.setItem(7, 1,
                                 QtWidgets.QTableWidgetItem(str('BOX-6')))
        self.tableWidget.setItem(8, 1,
                                 QtWidgets.QTableWidgetItem(str('BOX-7')))
        self.tableWidget.setItem(9, 1,
                                 QtWidgets.QTableWidgetItem(str('BOX-8')))



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
## add 8
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

        if self.task_5:
            try:
                task_5 = self.comboBox_task5.currentText()
                task_path_5 = os.path.join(tasks_dir, task_5 + '.py')
                if not self.task_hash_5 == _djb6_file(task_path_5):  # Task file modified.
                    self.task_changed_5()
            except FileNotFoundError:
                pass
        if self.task_6:
            try:
                task_6 = self.comboBox_task6.currentText()
                task_path_6 = os.path.join(tasks_dir, task_6 + '.py')
                if not self.task_hash_6 == _djb6_file(task_path_6):  # Task file modified.
                    self.task_changed_6()
            except FileNotFoundError:
                pass
        if self.task_7:
            try:
                task_7 = self.comboBox_task7.currentText()
                task_path_7 = os.path.join(tasks_dir, task_7 + '.py')
                if not self.task_hash_7 == _djb6_file(task_path_7):  # Task file modified.
                    self.task_changed_7()
            except FileNotFoundError:
                pass
        if self.task_8:
            try:
                task_8 = self.comboBox_task8.currentText()
                task_path_8 = os.path.join(tasks_dir, task_8 + '.py')
                if not self.task_hash_8 == _djb6_file(task_path_8):  # Task file modified.
                    self.task_changed_8()
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

    def task_changed_5(self):
        self.uploaded_5 = False
        self.pushButton_upload_5.setText('Upload')
        self.pushButton_Start5.setEnabled(False)

    def task_changed_6(self):
        self.uploaded_6 = False
        self.pushButton_upload_6.setText('Upload')
        self.pushButton_Start6.setEnabled(False)

    def task_changed_7(self):
        self.uploaded_7 = False
        self.pushButton_upload_7.setText('Upload')
        self.pushButton_Start7.setEnabled(False)

    def task_changed_8(self):
        self.uploaded_8 = False
        self.pushButton_upload_8.setText('Upload')
        self.pushButton_Start8.setEnabled(False)

## add 8
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

## try copy here

    def connect_5(self):
        try:
            self.lineEdit_status_5.setText('Connecting...')
            self.pushButton_Stop5.setEnabled(False)
            self.lineEdit_subid5.setEnabled(False)
            self.pushButton_var5.setEnabled(False)
            self.comboBox_srport_5.setEnabled(False)
            self.pushButton_connect_5.setEnabled(False)
            self.repaint()
            self.board_5 = Pycboard(self.comboBox_srport_5.currentText(),
                                    data_logger=self.data_logger5)
            if not self.board_5.status['framework']:
                self.board_5.load_framework()
            self.connected_5 = True
            self.pushButton_config_5.setEnabled(True)
            self.pushButton_connect_5.setEnabled(True)
            self.comboBox_task5.setEnabled(True)
            self.pushButton_upload_5.setEnabled(True)
            self.lineEdit_subid5.setEnabled(True)
            self.pushButton_connect_5.setText('Disconnect')

            self.lineEdit_status_5.setText('Connected')
        except SerialException:
            self.lineEdit_status_5.setText('Connection failed')
            self.pushButton_connect_5.setEnabled(True)

    def connect_6(self):
        try:
            self.lineEdit_status_6.setText('Connecting...')
            self.pushButton_Stop6.setEnabled(False)
            self.lineEdit_subid6.setEnabled(False)
            self.pushButton_var6.setEnabled(False)
            self.comboBox_srport_6.setEnabled(False)
            self.pushButton_connect_6.setEnabled(False)
            self.repaint()
            self.board_6 = Pycboard(self.comboBox_srport_6.currentText(),
                                    data_logger=self.data_logger6)
            if not self.board_6.status['framework']:
                self.board_6.load_framework()
            self.connected_6 = True
            self.pushButton_config_6.setEnabled(True)
            self.pushButton_connect_6.setEnabled(True)
            self.comboBox_task6.setEnabled(True)
            self.pushButton_upload_6.setEnabled(True)
            self.lineEdit_subid6.setEnabled(True)
            self.pushButton_connect_6.setText('Disconnect')

            self.lineEdit_status_6.setText('Connected')
        except SerialException:
            self.lineEdit_status_6.setText('Connection failed')
            self.pushButton_connect_6.setEnabled(True)

    def connect_7(self):
        try:
            self.lineEdit_status_7.setText('Connecting...')
            self.pushButton_Stop7.setEnabled(False)
            self.lineEdit_subid7.setEnabled(False)
            self.pushButton_var7.setEnabled(False)
            self.comboBox_srport_7.setEnabled(False)
            self.pushButton_connect_7.setEnabled(False)
            self.repaint()
            self.board_7 = Pycboard(self.comboBox_srport_7.currentText(),
                                    data_logger=self.data_logger7)
            if not self.board_7.status['framework']:
                self.board_7.load_framework()
            self.connected_7 = True
            self.pushButton_config_7.setEnabled(True)
            self.pushButton_connect_7.setEnabled(True)
            self.comboBox_task7.setEnabled(True)
            self.pushButton_upload_7.setEnabled(True)
            self.lineEdit_subid7.setEnabled(True)
            self.pushButton_connect_7.setText('Disconnect')

            self.lineEdit_status_7.setText('Connected')
        except SerialException:
            self.lineEdit_status_7.setText('Connection failed')
            self.pushButton_connect_7.setEnabled(True)

    def connect_8(self):
        try:
            self.lineEdit_status_8.setText('Connecting...')
            self.pushButton_Stop8.setEnabled(False)
            self.lineEdit_subid8.setEnabled(False)
            self.pushButton_var8.setEnabled(False)
            self.comboBox_srport_8.setEnabled(False)
            self.pushButton_connect_8.setEnabled(False)
            self.repaint()
            self.board_8 = Pycboard(self.comboBox_srport_8.currentText(),
                                    data_logger=self.data_logger8)
            if not self.board_8.status['framework']:
                self.board_8.load_framework()
            self.connected_8 = True
            self.pushButton_config_8.setEnabled(True)
            self.pushButton_connect_8.setEnabled(True)
            self.comboBox_task8.setEnabled(True)
            self.pushButton_upload_8.setEnabled(True)
            self.lineEdit_subid8.setEnabled(True)
            self.pushButton_connect_8.setText('Disconnect')

            self.lineEdit_status_8.setText('Connected')
        except SerialException:
            self.lineEdit_status_8.setText('Connection failed')
            self.pushButton_connect_8.setEnabled(True)


    def disconnect_5(self):
        # Disconnect from pyboard.
        if self.board_5: self.board_5.close()
        self.board_5 = None
        self.pushButton_config_5.setEnabled(False)
        self.pushButton_var5.setEnabled(False)
        self.comboBox_task5.setEnabled(False)
        self.pushButton_Start5.setEnabled(False)
        self.pushButton_Stop5.setEnabled(False)
        self.pushButton_upload_5.setEnabled(False)
        self.lineEdit_subid5.setEnabled(False)
        self.enable_srport_combo_box(True)
        self.pushButton_connect_5.setText('Connect')
        self.lineEdit_status_5.setText('Not connected')
        self.lineEdit_status_5.setEnabled(False)
        self.connected_5 = False

    def disconnect_6(self):
        if self.board_6: self.board_6.close()
        self.board_6 = None
        self.pushButton_config_6.setEnabled(False)
        self.pushButton_var6.setEnabled(False)
        self.comboBox_task6.setEnabled(False)
        self.pushButton_Start6.setEnabled(False)
        self.pushButton_Stop6.setEnabled(False)
        self.pushButton_upload_6.setEnabled(False)
        self.lineEdit_subid6.setEnabled(False)
        self.enable_srport_combo_box(True)
        self.pushButton_connect_6.setText('Connect')
        self.lineEdit_status_6.setText('Not connected')
        self.lineEdit_status_6.setEnabled(False)
        self.connected_6 = False

    def disconnect_7(self):
        if self.board_7: self.board_7.close()
        self.board_7 = None
        self.pushButton_config_7.setEnabled(False)
        self.pushButton_var7.setEnabled(False)
        self.comboBox_task7.setEnabled(False)
        self.pushButton_Start7.setEnabled(False)
        self.pushButton_Stop7.setEnabled(False)
        self.pushButton_upload_7.setEnabled(False)
        self.lineEdit_subid7.setEnabled(False)
        self.enable_srport_combo_box(True)
        self.pushButton_connect_7.setText('Connect')
        self.lineEdit_status_7.setText('Not connected')
        self.lineEdit_status_7.setEnabled(False)
        self.connected_7 = False

    def disconnect_8(self):
        if self.board_8: self.board_8.close()
        self.board_8 = None
        self.pushButton_config_8.setEnabled(False)
        self.pushButton_var8.setEnabled(False)
        self.comboBox_task8.setEnabled(False)
        self.pushButton_Start8.setEnabled(False)
        self.pushButton_Stop8.setEnabled(False)
        self.pushButton_upload_8.setEnabled(False)
        self.lineEdit_subid8.setEnabled(False)
        self.enable_srport_combo_box(True)
        self.pushButton_connect_8.setText('Connect')
        self.lineEdit_status_8.setText('Not connected')
        self.lineEdit_status_8.setEnabled(False)
        self.connected_8 = False

    def status_update(self, msg):
        self.lineEdit_status_5.setText(msg)
        self.lineEdit_status_6.setText(msg)
        self.lineEdit_status_7.setText(msg)
        self.lineEdit_status_8.setText(msg)

    def setup_task_5(self):
        try:
            task_5 = self.comboBox_task5.currentText()
            if self.uploaded_5:
                self.lineEdit_status_5.setText('Resetting task..')
            else:
                self.lineEdit_status_5.setText('Uploading..')
                self.task_hash_5 = _djb6_file(os.path.join(tasks_dir, task_5 + '.py'))
            self.pushButton_Start5.setEnabled(False)
            self.pushButton_var5.setEnabled(False)
            self.repaint()
            self.sm_info_5 = self.board_5.setup_state_machine(task_5, uploaded=self.uploaded_5)
            self.variables_dialog_5 = Variables_dialog(parent=self, variable=5)
            self.pushButton_var5.setEnabled(True)
            # self.task_plot.set_state_machine(self.sm_info)
            self.pushButton_Start5.setEnabled(True)
            self.lineEdit_subid5.setEnabled(True)
            self.pushButton_Stop5.setEnabled(False)
            self.lineEdit_status_5.setText('Uploaded : ' + task_5)
            self.task_5 = task_5
            self.uploaded_5 = True
            self.pushButton_upload_5.setText('Reset')
        except PyboardError:
            self.lineEdit_status_5.setText('Error setting up state machine.')

    def setup_task_6(self):
        try:
            task_6 = self.comboBox_task6.currentText()
            if self.uploaded_6:
                self.lineEdit_status_6.setText('Resetting task..')
            else:
                self.lineEdit_status_6.setText('Uploading..')
                self.task_hash_6 = _djb6_file(os.path.join(tasks_dir, task_6 + '.py'))
            self.pushButton_Start6.setEnabled(False)
            self.pushButton_var6.setEnabled(False)
            self.repaint()
            self.sm_info_6 = self.board_6.setup_state_machine(task_6, uploaded=self.uploaded_6)
            self.variables_dialog_6 = Variables_dialog(parent=self, variable=6)
            self.pushButton_var6.setEnabled(True)
            # self.task_plot.set_state_machine(self.sm_info)
            self.pushButton_Start6.setEnabled(True)
            self.lineEdit_subid6.setEnabled(True)
            self.pushButton_Stop6.setEnabled(False)
            self.lineEdit_status_6.setText('Uploaded : ' + task_6)
            self.task_6 = task_6
            self.uploaded_6 = True
            self.pushButton_upload_6.setText('Reset')
        except PyboardError:
            self.lineEdit_status_6.setText('Error setting up state machine.')

    def setup_task_7(self):
        try:
            task_7 = self.comboBox_task7.currentText()
            if self.uploaded_7:
                self.lineEdit_status_7.setText('Resetting task..')
            else:
                self.lineEdit_status_7.setText('Uploading..')
                self.task_hash_7 = _djb6_file(os.path.join(tasks_dir, task_7 + '.py'))
            self.pushButton_Start7.setEnabled(False)
            self.pushButton_var7.setEnabled(False)
            self.repaint()
            self.sm_info_7 = self.board_7.setup_state_machine(task_7, uploaded=self.uploaded_7)
            self.variables_dialog_7 = Variables_dialog(parent=self, variable=7)
            self.pushButton_var7.setEnabled(True)
            # self.task_plot.set_state_machine(self.sm_info)
            self.pushButton_Start7.setEnabled(True)
            self.lineEdit_subid7.setEnabled(True)
            self.pushButton_Stop7.setEnabled(False)
            self.lineEdit_status_7.setText('Uploaded : ' + task_7)
            self.task_7 = task_7
            self.uploaded_7 = True
            self.pushButton_upload_7.setText('Reset')
        except PyboardError:
            self.lineEdit_status_7.setText('Error setting up state machine.')

    def setup_task_8(self):
        try:
            task_8 = self.comboBox_task8.currentText()
            if self.uploaded_8:
                self.lineEdit_status_8.setText('Resetting task..')
            else:
                self.lineEdit_status_8.setText('Uploading..')
                self.task_hash_8 = _djb6_file(os.path.join(tasks_dir, task_8 + '.py'))
            self.pushButton_Start8.setEnabled(False)
            self.pushButton_var8.setEnabled(False)
            self.repaint()
            self.sm_info_8 = self.board_8.setup_state_machine(task_8, uploaded=self.uploaded_8)
            self.variables_dialog_8 = Variables_dialog(parent=self, variable=8)
            self.pushButton_var8.setEnabled(True)
            # self.task_plot.set_state_machine(self.sm_info)
            self.pushButton_Start8.setEnabled(True)
            self.lineEdit_subid8.setEnabled(True)
            self.pushButton_Stop8.setEnabled(False)
            self.lineEdit_status_8.setText('Uploaded : ' + task_8)
            self.task_8 = task_8
            self.uploaded_8 = True
            self.pushButton_upload_8.setText('Reset')
        except PyboardError:
            self.lineEdit_status_8.setText('Error setting up state machine.')

## end copy here

    def select_data_dir(self):
        self.lineEdit_data_dir.setText(
            QtGui.QFileDialog.getExistingDirectory(self, 'Select data folder', data_dir))

## start copy here

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

## end copy here

## insert start

    def test_data_path_5(self):
        # Checks whether data dir and subject ID are valid.
        self.data_dir = self.lineEdit_data_dir.text()
        subject_id_5 = self.lineEdit_subid5.text()
        if os.path.isdir(self.data_dir) and subject_id_5:
            self.pushButton_Start5.setText('RECORD')
            return True
        else:
            self.pushButton_Start5.setText('START')

    def test_data_path_6(self):
        # Checks whether data dir and subject ID are valid.
        self.data_dir = self.lineEdit_data_dir.text()
        subject_id_6 = self.lineEdit_subid6.text()
        if os.path.isdir(self.data_dir) and subject_id_6:
            self.pushButton_Start6.setText('RECORD')
            return True
        else:
            self.pushButton_Start6.setText('START')

    def test_data_path_7(self):
        # Checks whether data dir and subject ID are valid.
        self.data_dir = self.lineEdit_data_dir.text()
        subject_id_7 = self.lineEdit_subid7.text()
        if os.path.isdir(self.data_dir) and subject_id_7:
            self.pushButton_Start7.setText('RECORD')
            return True
        else:
            self.pushButton_Start7.setText('START')

    def test_data_path_8(self):
        # Checks whether data dir and subject ID are valid.
        self.data_dir = self.lineEdit_data_dir.text()
        subject_id_8 = self.lineEdit_subid8.text()
        if os.path.isdir(self.data_dir) and subject_id_8:
            self.pushButton_Start8.setText('RECORD')
            return True
        else:
            self.pushButton_Start8.setText('START')

    def start_task_5(self):
        if self.test_data_path_5():
            self.subject_id_5 = str(self.lineEdit_subid5.text())
            self.data_logger5.open_data_file(self.data_dir, self.exp_name, self.subject_id_5, self.project)
        self.resettable.setEnabled(False)
        self.tableWidget.setItem(6, 2,
                                 QtWidgets.QTableWidgetItem(str(self.subject_id_5)))
        self.tableWidget.setItem(6, 3,
                                 QtWidgets.QTableWidgetItem(str(self.task_5)))
        self.board_5.start_framework()
        self.start_time_5 = time.time()
        # self.task_plot.run_start()
        self.comboBox_task5.setEnabled(False)
        self.pushButton_upload_5.setEnabled(False)
        self.pushButton_Start5.setEnabled(False)
        self.pushButton_config_5.setEnabled(False)
        self.pushButton_Stop5.setEnabled(True)
        self.pushButton_connect_5.setEnabled(False)
        self.lineEdit_subid5.setEnabled(True)
        print('\nRun started at: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        self.process_timer_5.start(update_interval)
        self.refresh_timer_5.stop()
        self.lineEdit_status_5.setText('Running: ' + self.task_5)
        self.table_fill()

    def start_task_6(self):
        if self.test_data_path_6():
            self.subject_id_6 = str(self.lineEdit_subid6.text())
            self.data_logger6.open_data_file(self.data_dir, self.exp_name, self.subject_id_6, self.project)
        self.tableWidget.setItem(7, 2,
                                 QtWidgets.QTableWidgetItem(str(self.subject_id_6)))
        self.tableWidget.setItem(7, 3,
                                 QtWidgets.QTableWidgetItem(str(self.task_6)))
        self.board_6.start_framework()
        self.start_time_6 = time.time()
        self.resettable.setEnabled(False)
        # self.task_plot.run_start()
        self.comboBox_task6.setEnabled(False)
        self.pushButton_upload_6.setEnabled(False)
        self.pushButton_Start6.setEnabled(False)
        self.pushButton_config_6.setEnabled(False)
        self.pushButton_Stop6.setEnabled(True)
        self.pushButton_connect_6.setEnabled(False)
        self.lineEdit_subid6.setEnabled(True)
        print('\nRun started at: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        self.process_timer_6.start(update_interval)
        self.refresh_timer_6.stop()
        self.lineEdit_status_6.setText('Running: ' + self.task_6)
        self.table_fill()

    def start_task_7(self):
        if self.test_data_path_7():
            self.subject_id_7 = str(self.lineEdit_subid7.text())
            self.data_logger7.open_data_file(self.data_dir, self.exp_name, self.subject_id_7, self.project)
        self.tableWidget.setItem(8, 2,
                                 QtWidgets.QTableWidgetItem(str(self.subject_id_7)))
        self.tableWidget.setItem(8, 3,
                                 QtWidgets.QTableWidgetItem(str(self.task_7)))
        self.board_7.start_framework()
        self.start_time_7 = time.time()
        self.resettable.setEnabled(False)
        # self.task_plot.run_start()
        self.comboBox_task7.setEnabled(False)
        self.pushButton_upload_7.setEnabled(False)
        self.pushButton_Start7.setEnabled(False)
        self.pushButton_config_7.setEnabled(False)
        self.pushButton_Stop7.setEnabled(True)
        self.pushButton_connect_7.setEnabled(False)
        self.lineEdit_subid7.setEnabled(True)
        print('\nRun started at: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        self.process_timer_7.start(update_interval)
        self.refresh_timer_7.stop()
        self.lineEdit_status_7.setText('Running: ' + self.task_7)
        self.table_fill()

    def start_task_8(self):
        if self.test_data_path_8():
            self.subject_id_8 = str(self.lineEdit_subid8.text())
            self.data_logger8.open_data_file(self.data_dir, self.exp_name, self.subject_id_8, self.project)
        self.tableWidget.setItem(9, 2,
                                 QtWidgets.QTableWidgetItem(str(self.subject_id_8)))
        self.tableWidget.setItem(9, 3,
                                 QtWidgets.QTableWidgetItem(str(self.task_8)))
        self.board_8.start_framework()
        self.start_time_8 = time.time()
        self.resettable.setEnabled(False)
        # self.task_plot.run_start()
        self.comboBox_task8.setEnabled(False)
        self.pushButton_upload_8.setEnabled(False)
        self.pushButton_Start8.setEnabled(False)
        self.pushButton_config_8.setEnabled(False)
        self.pushButton_Stop8.setEnabled(True)
        self.pushButton_connect_8.setEnabled(False)
        self.lineEdit_subid8.setEnabled(True)
        print('\nRun started at: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        self.process_timer_8.start(update_interval)
        self.refresh_timer_8.stop()
        self.lineEdit_status_8.setText('Running: ' + self.task_8)
        self.table_fill()

    def stop_task_5(self, error=False, stopped_by_task=False):
        self.process_timer_5.stop()
        self.refresh_timer_5.start(self.refresh_interval)
        if not (error or stopped_by_task):
            self.board_5.stop_framework()
            QtCore.QTimer.singleShot(100, self.process_data_5)  # Catch output after framework stops.
        self.data_logger5.close_files()
        self.pushButton_Start5.setEnabled(True)
        self.pushButton_connect_5.setEnabled(True)
        self.comboBox_task5.setEnabled(True)
        self.resettable.setEnabled(False)
        self.pushButton_upload_5.setEnabled(True)
        self.pushButton_Stop5.setEnabled(False)
        self.tableWidget.setItem(6, 0,
                                 QtWidgets.QTableWidgetItem(str(self.date)))
        self.lineEdit_status_5.setText('Uploaded : ' + self.task_5)

    def stop_task_6(self, error=False, stopped_by_task=False):
        self.process_timer_6.stop()
        self.refresh_timer_6.start(self.refresh_interval)
        if not (error or stopped_by_task):
            self.board_6.stop_framework()
            QtCore.QTimer.singleShot(100, self.process_data_6)  # Catch output after framework stops.
        self.data_logger6.close_files()
        self.pushButton_Start6.setEnabled(True)
        self.pushButton_connect_6.setEnabled(True)
        self.comboBox_task6.setEnabled(True)
        self.resettable.setEnabled(False)
        self.pushButton_upload_6.setEnabled(True)
        self.pushButton_Stop6.setEnabled(False)
        self.tableWidget.setItem(7, 0,
                                 QtWidgets.QTableWidgetItem(str(self.date)))
        self.lineEdit_status_6.setText('Uploaded : ' + self.task_6)

    def stop_task_7(self, error=False, stopped_by_task=False):
        self.process_timer_7.stop()
        self.refresh_timer_7.start(self.refresh_interval)
        if not (error or stopped_by_task):
            self.board_7.stop_framework()
            QtCore.QTimer.singleShot(100, self.process_data_7)  # Catch output after framework stops.
        self.data_logger7.close_files()
        self.pushButton_Start7.setEnabled(True)
        self.pushButton_connect_7.setEnabled(True)
        self.comboBox_task7.setEnabled(True)
        self.resettable.setEnabled(False)
        self.pushButton_upload_7.setEnabled(True)
        self.pushButton_Stop7.setEnabled(False)
        self.tableWidget.setItem(8, 0,
                                 QtWidgets.QTableWidgetItem(str(self.date)))
        self.lineEdit_status_7.setText('Uploaded : ' + self.task_7)

    def stop_task_8(self, error=False, stopped_by_task=False):
        self.process_timer_8.stop()
        self.refresh_timer_8.start(self.refresh_interval)
        if not (error or stopped_by_task):
            self.board_8.stop_framework()
            QtCore.QTimer.singleShot(100, self.process_data_8)  # Catch output after framework stops.
        self.data_logger8.close_files()
        self.pushButton_Start8.setEnabled(True)
        self.pushButton_connect_8.setEnabled(True)
        self.comboBox_task8.setEnabled(True)
        self.resettable.setEnabled(False)
        self.pushButton_upload_8.setEnabled(True)
        self.pushButton_Stop8.setEnabled(False)
        self.tableWidget.setItem(9, 0,
                                 QtWidgets.QTableWidgetItem(str(self.date)))
        self.lineEdit_status_8.setText('Uploaded : ' + self.task_8)

## instert end
#
#
#
#
#

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


    def process_data_5(self):
        # Called regularly during run to process data from board.
        try:
            new_data_5 = self.board_5.process_data()
            # update timer here
            run_time_5 = time.time() - self.start_time_5
            run_time_5 = str(timedelta(seconds=run_time_5))[:7]
            self.lcdNumber_Timer_BOX5.display(run_time_5)

            # self.task_plot.process_data(new_data_5)
            if not self.board_5.framework_running:
                self.stop_task_5(stopped_by_task=True)
            self.update_data_table_5(new_data_5)
        except PyboardError as e:
            self.print_to_log('\nError during framework run.')
            self.stop_task_5(error=True)

    def process_data_6(self):
        # Called regularly during run to process data from board.
        try:
            new_data_6 = self.board_6.process_data()
            # update timer here
            run_time = time.time() - self.start_time_6
            run_time = str(timedelta(seconds=run_time))[:7]
            self.lcdNumber_Timer_BOX6.display(run_time)
            # self.task_plot.process_data(new_data_6)
            if not self.board_6.framework_running:
                self.stop_task_6(stopped_by_task=True)
            self.update_data_table_6(new_data_6)
        except PyboardError as e:
            self.print_to_log('\nError during framework run.')
            self.stop_task_6(error=True)

    def process_data_7(self):
        # Called regularly during run to process data from board.
        try:
            new_data_7 = self.board_7.process_data()
            # update timer here
            run_time_7 = time.time() - self.start_time_7
            run_time_7 = str(timedelta(seconds=run_time_7))[:7]
            self.lcdNumber_Timer_BOX7.display(run_time_7)
            # self.task_plot.process_data(new_data_7)
            if not self.board_7.framework_running:
                self.stop_task_7(stopped_by_task=True)
            self.update_data_table_7(new_data_7)
        except PyboardError as e:
            self.print_to_log('\nError during framework run.')
            self.stop_task_7(error=True)

    def process_data_8(self):
        # Called regularly during run to process data from board.
        try:
            new_data_8 = self.board_8.process_data()
            # update timer here
            run_time_8 = time.time() - self.start_time_8
            run_time_8 = str(timedelta(seconds=run_time_8))[:7]
            self.lcdNumber_Timer_BOX8.display(run_time_8)
            # self.task_plot.process_data(new_data_8)
            if not self.board_8.framework_running:
                self.stop_task_8(stopped_by_task=True)
            self.update_data_table_8(new_data_8)
        except PyboardError as e:
            self.print_to_log('\nError during framework run.')
            self.stop_task_8(error=True)

## setting up live data reports ?
## check to see strings match my 5T code

## deleting this just to test 8 slots

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
        elif self.board_5:
            self.board_5.stop_framework()
            self.board_5.close()
        elif self.board_6:
            self.board_6.stop_framework()
            self.board_6.close()
        elif self.board_7:
            self.board_7.stop_framework()
            self.board_7.close()
        elif self.board_8:
            self.board_8.stop_framework()
            self.board_8.close()
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
