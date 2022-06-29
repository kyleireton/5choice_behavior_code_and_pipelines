## Import All required functions
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
import port_list
# Add parent directory to path to allow imports.
top_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not top_dir in sys.path: sys.path.insert(0, top_dir)

from com.pycboard import Pycboard, PyboardError, _djb2_file
from com.data_logger import Data_logger

from config.paths import data_dir, tasks_dir_DMTP
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
        self.setWindowTitle('5-Choice_Serial_DelayedMatch')
        # Variables.
        # self.board = None
        # self.text_edit_widget = None
        self.board_1 = None  # Pycboard class instance.
        self.board_2 = None  # Pycboard class instance.
        self.board_3 = None  # Pycboard class instance.
        self.board_4 = None  # Pycboard class instance.
        self.board_5 = None  # Pycboard class instance.
        self.board_6 = None  # Pycboard class instance.
        self.board_7 = None  # Pycboard class instance.
        self.board_8 = None
        self.task = None  # Pycboard class instance.
        self.task_1 = None  # Task currently uploaded on pyboard.
        self.task_2 = None  # Task currently uploaded on pyboard.
        self.task_3 = None  # Task currently uploaded on pyboard.
        self.task_4 = None  # Task currently uploaded on pyboard.
        self.task_5 = None  # Task currently uploaded on pyboard.
        self.task_6 = None  # Task currently uploaded on pyboard.
        self.task_7 = None  # Task currently uploaded on pyboard.
        self.task_8 = None  # Task currently uploaded on pyboard.
        self.task_hash_1 = None  # Used to check if file has changed.
        self.task_hash_2 = None  # Used to check if file has changed.
        self.task_hash_3 = None  # Used to check if file has changed.
        self.task_hash_4 = None  # Used to check if file has changed.
        self.task_hash_5 = None  # Used to check if file has changed.
        self.task_hash_6 = None  # Used to check if file has changed.
        self.task_hash_7 = None  # Used to check if file has changed.
        self.task_hash_8 = None  # Used to check if file has changed.
        self.sm_info_1 = None  # Information about current state machine.
        self.sm_info_2 = None  # Information about current state machine.
        self.sm_info_3 = None  # Information about current state machine.
        self.sm_info_4 = None  # Information about current state machine.
        self.sm_info_5 = None  # Information about current state machine.
        self.sm_info_6 = None  # Information about current state machine.
        self.sm_info_7 = None  # Information about current state machine.
        self.sm_info_8 = None  # Information about current state machine.
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
        # self.showlcd()
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
            lambda: self.disconnect_5() if self.connected_5 else self.connect_5())
        self.pushButton_connect_6.clicked.connect(
            lambda: self.disconnect_6() if self.connected_6 else self.connect_6())
        self.pushButton_connect_7.clicked.connect(
            lambda: self.disconnect_7() if self.connected_7 else self.connect_7())
        self.pushButton_connect_8.clicked.connect(
            lambda: self.disconnect_8() if self.connected_8 else self.connect_8())
        self.pushButton_Connect_all.clicked.connect(
            lambda: self.disconnect_all() if self.connected_1 or self.connected_2 or self.connected_3 or self.connected_4 or self.connected_5 or self.connected_6 or self.connected_7 else self.connect_all())

        self.exportdata.clicked.connect(lambda: self.save_file())
        self.Exportdata2.clicked.connect(lambda: self.save_file())
        self.resettable.clicked.connect(lambda: self.items_clear())
        self.testboxes.clicked.connect(lambda: self.setup_task_test_poke())

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

        self.pushButton_Upload_all.clicked.connect(lambda: self.setup_task_all())

        # self.pushButton_Upload_all.clicked.connect(lambda: self.setup_task_all())
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

        self.pushButton_Start_all.clicked.connect(lambda: self.record_task_all())
        # self.pushButton.clicked.connect(lambda: self.start_task_all())

        self.pushButton_Stop1.clicked.connect(lambda: self.stop_task_1())
        self.pushButton_Stop2.clicked.connect(lambda: self.stop_task_2())
        self.pushButton_Stop3.clicked.connect(lambda: self.stop_task_3())
        self.pushButton_Stop4.clicked.connect(lambda: self.stop_task_4())
        self.pushButton_Stop5.clicked.connect(lambda: self.stop_task_5())
        self.pushButton_Stop6.clicked.connect(lambda: self.stop_task_6())
        self.pushButton_Stop7.clicked.connect(lambda: self.stop_task_7())
        self.pushButton_Stop8.clicked.connect(lambda: self.stop_task_8())

        self.pushButton_Stop_all.clicked.connect(lambda: self.stop_task_all())

        self.pushButton_setupselect_1.clicked.connect(lambda: port_list.select_setup_1(self))
        self.pushButton_setupselect_2.clicked.connect(lambda: port_list.select_setup_2(self))
        self.pushButton_setupselect_3.clicked.connect(lambda: port_list.select_setup_3(self))

        # LineEdit
        self.lineEdit_status_1.setReadOnly(True)
        self.lineEdit_status_2.setReadOnly(True)
        self.lineEdit_status_3.setReadOnly(True)
        self.lineEdit_status_4.setReadOnly(True)
        self.lineEdit_status_5.setReadOnly(True)
        self.lineEdit_status_6.setReadOnly(True)
        self.lineEdit_status_7.setReadOnly(True)
        self.lineEdit_status_8.setReadOnly(True)
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
        self.lineEdit_subid5.textChanged.connect(self.test_data_path_5)
        self.lineEdit_subid6.textChanged.connect(self.test_data_path_6)
        self.lineEdit_subid7.textChanged.connect(self.test_data_path_7)
        self.lineEdit_subid8.textChanged.connect(self.test_data_path_8)

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
        self.disconnect_5()
        self.disconnect_6()
        self.disconnect_7()
        self.disconnect_8()
        self.disconnect_all()
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

        ## ValiablesNames
        self.sample_start_time_1 = 0
        self.correct_sample_resp_time_1 = 0
        self.iti_start_time_1 = 0
        self.choice_start_time_1 = 0
        self.correct_choice_resp_time_1 = 0
        self.delay_start_time_1 = 0
        self.sample_start_time_2 = 0
        self.correct_sample_resp_time_2 = 0
        self.iti_start_time_2 = 0
        self.choice_start_time_2 = 0
        self.correct_choice_resp_time_2 = 0
        self.delay_start_time_2 = 0
        self.sample_start_time_3 = 0
        self.correct_sample_resp_time_3 = 0
        self.iti_start_time_3 = 0
        self.choice_start_time_3 = 0
        self.correct_choice_resp_time_3 = 0
        self.delay_start_time_3 = 0
        self.sample_start_time_4 = 0
        self.correct_sample_resp_time_4 = 0
        self.iti_start_time_4 = 0
        self.choice_start_time_4 = 0
        self.correct_choice_resp_time_4 = 0
        self.delay_start_time_4 = 0
        self.sample_start_time_5 = 0
        self.correct_sample_resp_time_5 = 0
        self.iti_start_time_5 = 0
        self.choice_start_time_5 = 0
        self.correct_choice_resp_time_5 = 0
        self.delay_start_time_5 = 0
        self.sample_start_time_6 = 0
        self.correct_sample_resp_time_6 = 0
        self.iti_start_time_6 = 0
        self.choice_start_time_6 = 0
        self.correct_choice_resp_time_6 = 0
        self.delay_start_time_6 = 0
        self.sample_start_time_7 = 0
        self.correct_sample_resp_time_7 = 0
        self.iti_start_time_7 = 0
        self.choice_start_time_7 = 0
        self.correct_choice_resp_time_7 = 0
        self.delay_start_time_7 = 0
        self.sample_start_time_8 = 0
        self.correct_sample_resp_time_8 = 0
        self.iti_start_time_8 = 0
        self.choice_start_time_8 = 0
        self.correct_choice_resp_time_8 = 0
        self.delay_start_time_8 = 0
        self.Correct_sample_1 = 0
        self.Correct_sample_2 = 0
        self.Correct_sample_3 = 0
        self.Correct_sample_4 = 0
        self.Correct_sample_5 = 0
        self.Correct_sample_6 = 0
        self.Correct_sample_7 = 0
        self.Correct_sample_8 = 0
        self.Premature_Response_Latency_sample_1 = 0
        self.Premature_Response_Latency_sample_2 = 0
        self.Premature_Response_Latency_sample_3 = 0
        self.Premature_Response_Latency_sample_4 = 0
        self.Premature_Response_Latency_sample_5 = 0
        self.Premature_Response_Latency_sample_6 = 0
        self.Premature_Response_Latency_sample_7 = 0
        self.Premature_Response_Latency_sample_8 = 0
        self.premature_sample_1 = 0
        self.premature_sample_2 = 0
        self.premature_sample_3 = 0
        self.premature_sample_4 = 0
        self.premature_sample_5 = 0
        self.premature_sample_6 = 0
        self.premature_sample_7 = 0
        self.premature_sample_8 = 0
        self.Premature_sample_mean_1 = 0
        self.Premature_sample_mean_2 = 0
        self.Premature_sample_mean_3 = 0
        self.Premature_sample_mean_4 = 0
        self.Premature_sample_mean_5 = 0
        self.Premature_sample_mean_6 = 0
        self.Premature_sample_mean_7 = 0
        self.Premature_sample_mean_8 = 0
        self.Premature_Response_Latency_choice_1 = 0
        self.Premature_Response_Latency_choice_2 = 0
        self.Premature_Response_Latency_choice_3 = 0
        self.Premature_Response_Latency_choice_4 = 0
        self.Premature_Response_Latency_choice_5 = 0
        self.Premature_Response_Latency_choice_6 = 0
        self.Premature_Response_Latency_choice_7 = 0
        self.Premature_Response_Latency_choice_8 = 0
        self.Premature_latancy_sample_list_1 = []
        self.Premature_latancy_sample_list_2 = []
        self.Premature_latancy_sample_list_3 = []
        self.Premature_latancy_sample_list_4 = []
        self.Premature_latancy_sample_list_5 = []
        self.Premature_latancy_sample_list_6 = []
        self.Premature_latancy_sample_list_7 = []
        self.Premature_latancy_sample_list_8 = []
        self.Premature_latancy_choice_list_1 = []
        self.Premature_latancy_choice_list_2 = []
        self.Premature_latancy_choice_list_3 = []
        self.Premature_latancy_choice_list_4 = []
        self.Premature_latancy_choice_list_5 = []
        self.Premature_latancy_choice_list_6 = []
        self.Premature_latancy_choice_list_7 = []
        self.Premature_latancy_choice_list_8 = []
        self.premature_choice_1 = 0
        self.premature_choice_2 = 0
        self.premature_choice_3 = 0
        self.premature_choice_4 = 0
        self.premature_choice_5 = 0
        self.premature_choice_6 = 0
        self.premature_choice_7 = 0
        self.premature_choice_8 = 0
        self.Premature_choice_mean_1 = 0
        self.Premature_choice_mean_2 = 0
        self.Premature_choice_mean_3 = 0
        self.Premature_choice_mean_4 = 0
        self.Premature_choice_mean_5 = 0
        self.Premature_choice_mean_6 = 0
        self.Premature_choice_mean_7 = 0
        self.Premature_choice_mean_8 = 0
        self.omission_sample_1 = 0
        self.omission_sample_2 = 0
        self.omission_sample_3 = 0
        self.omission_sample_4 = 0
        self.omission_sample_5 = 0
        self.omission_sample_6 = 0
        self.omission_sample_7 = 0
        self.omission_sample_8 = 0
        self.Incorrect_sample_1 = 0
        self.Incorrect_sample_2 = 0
        self.Incorrect_sample_3 = 0
        self.Incorrect_sample_4 = 0
        self.Incorrect_sample_5 = 0
        self.Incorrect_sample_6 = 0
        self.Incorrect_sample_7 = 0
        self.Incorrect_sample_8 = 0
        self.Reward_Latency_sample_1 = 0
        self.Reward_Latency_sample_2 = 0
        self.Reward_Latency_sample_3 = 0
        self.Reward_Latency_sample_4 = 0
        self.Reward_Latency_sample_5 = 0
        self.Reward_Latency_sample_6 = 0
        self.Reward_Latency_sample_7 = 0
        self.Reward_Latency_sample_8 = 0
        self.Premature_sample_1 = 0
        self.Premature_sample_2 = 0
        self.Premature_sample_3 = 0
        self.Premature_sample_4 = 0
        self.Premature_sample_5 = 0
        self.Premature_sample_6 = 0
        self.Premature_sample_7 = 0
        self.Premature_sample_8 = 0
        self.perseverate_sample_1 = 0
        self.perseverate_sample_2 = 0
        self.perseverate_sample_3 = 0
        self.perseverate_sample_4 = 0
        self.perseverate_sample_5 = 0
        self.perseverate_sample_6 = 0
        self.perseverate_sample_7 = 0
        self.perseverate_sample_8 = 0
        self.Premature_Response_Latency_sample_Mean_1 = 0
        self.Premature_Response_Latency_sample_Mean_2 = 0
        self.Premature_Response_Latency_sample_Mean_3 = 0
        self.Premature_Response_Latency_sample_Mean_4 = 0
        self.Premature_Response_Latency_sample_Mean_5 = 0
        self.Premature_Response_Latency_sample_Mean_6 = 0
        self.Premature_Response_Latency_sample_Mean_7 = 0
        self.Premature_Response_Latency_sample_Mean_8 = 0
        self.incorrect_latency_sample_1 = 0
        self.incorrect_latency_sample_2 = 0
        self.incorrect_latency_sample_3 = 0
        self.incorrect_latency_sample_4 = 0
        self.incorrect_latency_sample_5 = 0
        self.incorrect_latency_sample_6 = 0
        self.incorrect_latency_sample_7 = 0
        self.incorrect_latency_sample_8 = 0
        self.incorrect_latency_choice_1 = 0
        self.incorrect_latency_choice_2 = 0
        self.incorrect_latency_choice_3 = 0
        self.incorrect_latency_choice_4 = 0
        self.incorrect_latency_choice_5 = 0
        self.incorrect_latency_choice_6 = 0
        self.incorrect_latency_choice_7 = 0
        self.incorrect_latency_choice_8 = 0
        self.incorrect_latency_choice_9 = 0
        self.correct_latency_sample_1 = 0
        self.correct_latency_sample_2 = 0
        self.correct_latency_sample_3 = 0
        self.correct_latency_sample_4 = 0
        self.correct_latency_sample_5 = 0
        self.correct_latency_sample_6 = 0
        self.correct_latency_sample_7 = 0
        self.correct_latency_sample_8 = 0
        self.correct_A_sample_1 = 0
        self.correct_A_sample_2 = 0
        self.correct_A_sample_3 = 0
        self.correct_A_sample_4 = 0
        self.correct_A_sample_5 = 0
        self.correct_A_sample_6 = 0
        self.correct_A_sample_7 = 0
        self.correct_A_sample_8 = 0
        self.correct_cv_sample_list_1 = []
        self.correct_cv_sample_list_2 = []
        self.correct_cv_sample_list_3 = []
        self.correct_cv_sample_list_4 = []
        self.correct_cv_sample_list_5 = []
        self.correct_cv_sample_list_6 = []
        self.correct_cv_sample_list_7 = []
        self.correct_cv_sample_list_8 = []
        self.correct_stdev_sample_1 = 0
        self.correct_stdev_sample_2 = 0
        self.correct_stdev_sample_3 = 0
        self.correct_stdev_sample_4 = 0
        self.correct_stdev_sample_5 = 0
        self.correct_stdev_sample_6 = 0
        self.correct_stdev_sample_7 = 0
        self.correct_stdev_sample_8 = 0
        self.correct_mean_sample_1 = 0
        self.correct_mean_sample_2 = 0
        self.correct_mean_sample_3 = 0
        self.correct_mean_sample_4 = 0
        self.correct_mean_sample_5 = 0
        self.correct_mean_sample_6 = 0
        self.correct_mean_sample_7 = 0
        self.correct_mean_sample_8 = 0
        self.correct_cv_sample_1 = 0
        self.correct_cv_sample_2 = 0
        self.correct_cv_sample_3 = 0
        self.correct_cv_sample_4 = 0
        self.correct_cv_sample_5 = 0
        self.correct_cv_sample_6 = 0
        self.correct_cv_sample_7 = 0
        self.correct_cv_sample_8 = 0
        self.reward_lat_sample_list_1 = []
        self.reward_lat_sample_list_2 = []
        self.reward_lat_sample_list_3 = []
        self.reward_lat_sample_list_4 = []
        self.reward_lat_sample_list_5 = []
        self.reward_lat_sample_list_6 = []
        self.reward_lat_sample_list_7 = []
        self.reward_lat_sample_list_8 = []
        self.reward_lat_choice_list_1 = []
        self.reward_lat_choice_list_2 = []
        self.reward_lat_choice_list_3 = []
        self.reward_lat_choice_list_4 = []
        self.reward_lat_choice_list_5 = []
        self.reward_lat_choice_list_6 = []
        self.reward_lat_choice_list_7 = []
        self.reward_lat_choice_list_8 = []
        self.reward_A_sample_1 = 0
        self.reward_A_sample_2 = 0
        self.reward_A_sample_3 = 0
        self.reward_A_sample_4 = 0
        self.reward_A_sample_5 = 0
        self.reward_A_sample_6 = 0
        self.reward_A_sample_7 = 0
        self.reward_A_sample_8 = 0
        self.reward_lat_sample_mean_1 = 0
        self.reward_lat_sample_mean_2 = 0
        self.reward_lat_sample_mean_3 = 0
        self.reward_lat_sample_mean_4 = 0
        self.reward_lat_sample_mean_5 = 0
        self.reward_lat_sample_mean_6 = 0
        self.reward_lat_sample_mean_7 = 0
        self.reward_lat_sample_mean_8 = 0
        self.reward_lat_choice_list_1 = []
        self.reward_lat_sample_list_2 = []
        self.reward_lat_sample_list_3 = []
        self.reward_lat_sample_list_4 = []
        self.reward_lat_sample_list_5 = []
        self.reward_lat_sample_list_6 = []
        self.reward_lat_sample_list_7 = []
        self.reward_lat_sample_list_8 = []
        self.incorrect_A_sample_1 = 0
        self.incorrect_A_sample_2 = 0
        self.incorrect_A_sample_3 = 0
        self.incorrect_A_sample_4 = 0
        self.incorrect_A_sample_5 = 0
        self.incorrect_A_sample_6 = 0
        self.incorrect_A_sample_7 = 0
        self.incorrect_A_sample_8 = 0
        self.incorrect_lat_sample_mean_1 = 0
        self.incorrect_lat_sample_mean_2 = 0
        self.incorrect_lat_sample_mean_3 = 0
        self.incorrect_lat_sample_mean_4 = 0
        self.incorrect_lat_sample_mean_5 = 0
        self.incorrect_lat_sample_mean_6 = 0
        self.incorrect_lat_sample_mean_7 = 0
        self.incorrect_lat_sample_mean_8 = 0
        self.incorrect_cv_sample_list_1 = []
        self.incorrect_cv_sample_list_2 = []
        self.incorrect_cv_sample_list_3 = []
        self.incorrect_cv_sample_list_4 = []
        self.incorrect_cv_sample_list_5 = []
        self.incorrect_cv_sample_list_6 = []
        self.incorrect_cv_sample_list_7 = []
        self.incorrect_cv_sample_list_8 = []
        self.incorrect_latency_sample_Mean_1 = 0
        self.incorrect_latency_sample_Mean_2 = 0
        self.incorrect_latency_sample_Mean_3 = 0
        self.incorrect_latency_sample_Mean_4 = 0
        self.incorrect_latency_sample_Mean_5 = 0
        self.incorrect_latency_sample_Mean_6 = 0
        self.incorrect_latency_sample_Mean_7 = 0
        self.incorrect_latency_sample_Mean_8 = 0
        self.trial_sample_1 = 0
        self.trial_sample_2 = 0
        self.trial_sample_3 = 0
        self.trial_sample_4 = 0
        self.trial_sample_5 = 0
        self.trial_sample_6 = 0
        self.trial_sample_7 = 0
        self.trial_sample_8 = 0
        self.per_omission_sample_1 = 0
        self.per_omission_sample_2 = 0
        self.per_omission_sample_3 = 0
        self.per_omission_sample_4 = 0
        self.per_omission_sample_5 = 0
        self.per_omission_sample_6 = 0
        self.per_omission_sample_7 = 0
        self.per_omission_sample_8 = 0
        self.per_accuracy_sample_1 = 0
        self.per_accuracy_sample_2 = 0
        self.per_accuracy_sample_3 = 0
        self.per_accuracy_sample_4 = 0
        self.per_accuracy_sample_5 = 0
        self.per_accuracy_sample_6 = 0
        self.per_accuracy_sample_7 = 0
        self.per_accuracy_sample_8 = 0
        self.per_correct_sample_1 = 0
        self.per_correct_sample_2 = 0
        self.per_correct_sample_3 = 0
        self.per_correct_sample_4 = 0
        self.per_correct_sample_5 = 0
        self.per_correct_sample_6 = 0
        self.per_correct_sample_7 = 0
        self.per_correct_sample_8 = 0
        self.per_premature_sample_1 = 0
        self.per_premature_sample_2 = 0
        self.per_premature_sample_3 = 0
        self.per_premature_sample_4 = 0
        self.per_premature_sample_5 = 0
        self.per_premature_sample_6 = 0
        self.per_premature_sample_7 = 0
        self.per_premature_sample_8 = 0
        self.per_perseverate_sample_1 = 0
        self.per_perseverate_sample_2 = 0
        self.per_perseverate_sample_3 = 0
        self.per_perseverate_sample_4 = 0
        self.per_perseverate_sample_5 = 0
        self.per_perseverate_sample_6 = 0
        self.per_perseverate_sample_7 = 0
        self.per_perseverate_sample_8 = 0
        self.Correct_choice_1 = 0
        self.Correct_choice_2 = 0
        self.Correct_choice_3 = 0
        self.Correct_choice_4 = 0
        self.Correct_choice_5 = 0
        self.Correct_choice_6 = 0
        self.Correct_choice_7 = 0
        self.Correct_choice_8 = 0
        self.Incorrect_choice_1 = 0
        self.Incorrect_choice_2 = 0
        self.Incorrect_choice_3 = 0
        self.Incorrect_choice_4 = 0
        self.Incorrect_choice_5 = 0
        self.Incorrect_choice_6 = 0
        self.Incorrect_choice_7 = 0
        self.Incorrect_choice_8 = 0
        self.omission_choice_1 = 0
        self.omission_choice_2 = 0
        self.omission_choice_3 = 0
        self.omission_choice_4 = 0
        self.omission_choice_5 = 0
        self.omission_choice_6 = 0
        self.omission_choice_7 = 0
        self.omission_choice_8 = 0
        self.Reward_Latency_choice_1 = 0
        self.Reward_Latency_choice_2 = 0
        self.Reward_Latency_choice_3 = 0
        self.Reward_Latency_choice_4 = 0
        self.Reward_Latency_choice_5 = 0
        self.Reward_Latency_choice_6 = 0
        self.Reward_Latency_choice_7 = 0
        self.Reward_Latency_choice_8 = 0
        self.Premature_choice_correct_1 = 0
        self.Premature_choice_correct_2 = 0
        self.Premature_choice_correct_3 = 0
        self.Premature_choice_correct_4 = 0
        self.Premature_choice_correct_5 = 0
        self.Premature_choice_correct_6 = 0
        self.Premature_choice_correct_7 = 0
        self.Premature_choice_correct_8 = 0
        self.Premature_choice_incorrect_1 = 0
        self.Premature_choice_incorrect_2 = 0
        self.Premature_choice_incorrect_3 = 0
        self.Premature_choice_incorrect_4 = 0
        self.Premature_choice_incorrect_5 = 0
        self.Premature_choice_incorrect_6 = 0
        self.Premature_choice_incorrect_7 = 0
        self.Premature_choice_incorrect_8 = 0
        self.perseverate_choice_1 = 0
        self.perseverate_choice_2 = 0
        self.perseverate_choice_3 = 0
        self.perseverate_choice_4 = 0
        self.perseverate_choice_5 = 0
        self.perseverate_choice_6 = 0
        self.perseverate_choice_7 = 0
        self.perseverate_choice_8 = 0
        self.resp_timeout_1 = 0
        self.resp_timeout_2 = 0
        self.resp_timeout_3 = 0
        self.resp_timeout_4 = 0
        self.resp_timeout_5 = 0
        self.resp_timeout_6 = 0
        self.resp_timeout_7 = 0
        self.resp_timeout_8 = 0
        self.Premature_Response_Latency_choice_Mean_1 = 0
        self.Premature_Response_Latency_choice_Mean_2 = 0
        self.Premature_Response_Latency_choice_Mean_3 = 0
        self.Premature_Response_Latency_choice_Mean_4 = 0
        self.Premature_Response_Latency_choice_Mean_5 = 0
        self.Premature_Response_Latency_choice_Mean_6 = 0
        self.Premature_Response_Latency_choice_Mean_7 = 0
        self.Premature_Response_Latency_choice_Mean_8 = 0
        self.correct_latency_choice_1 = 0
        self.correct_latency_choice_2 = 0
        self.correct_latency_choice_3 = 0
        self.correct_latency_choice_4 = 0
        self.correct_latency_choice_5 = 0
        self.correct_latency_choice_6 = 0
        self.correct_latency_choice_7 = 0
        self.correct_latency_choice_8 = 0
        self.incorrect_lit_choice_1 = 0
        self.incorrect_lit_choice_2 = 0
        self.incorrect_lit_choice_3 = 0
        self.incorrect_lit_choice_4 = 0
        self.incorrect_lit_choice_5 = 0
        self.incorrect_lit_choice_6 = 0
        self.incorrect_lit_choice_7 = 0
        self.incorrect_lit_choice_8 = 0
        self.Receptacle_entries_1 = 0
        self.Receptacle_entries_2 = 0
        self.Receptacle_entries_3 = 0
        self.Receptacle_entries_4 = 0
        self.Receptacle_entries_5 = 0
        self.Receptacle_entries_6 = 0
        self.Receptacle_entries_7 = 0
        self.Receptacle_entries_8 = 0
        self.Nosepokes_5poke_1 = 0
        self.Nosepokes_5poke_2 = 0
        self.Nosepokes_5poke_3 = 0
        self.Nosepokes_5poke_4 = 0
        self.Nosepokes_5poke_5 = 0
        self.Nosepokes_5poke_6 = 0
        self.Nosepokes_5poke_7 = 0
        self.Nosepokes_5poke_8 = 0
        self.SP_reward_1 = 0
        self.SP_reward_2 = 0
        self.SP_reward_3 = 0
        self.SP_reward_4 = 0
        self.SP_reward_5 = 0
        self.SP_reward_6 = 0
        self.SP_reward_7 = 0
        self.SP_reward_8 = 0
        self.correct_A_choice_1 = 0
        self.correct_A_choice_2 = 0
        self.correct_A_choice_3 = 0
        self.correct_A_choice_4 = 0
        self.correct_A_choice_5 = 0
        self.correct_A_choice_6 = 0
        self.correct_A_choice_7 = 0
        self.correct_A_choice_8 = 0
        self.correct_cv_choice_list_1 = []
        self.correct_cv_choice_list_2 = []
        self.correct_cv_choice_list_3 = []
        self.correct_cv_choice_list_4 = []
        self.correct_cv_choice_list_5 = []
        self.correct_cv_choice_list_6 = []
        self.correct_cv_choice_list_7 = []
        self.correct_cv_choice_list_8 = []
        self.correct_stdev_choice_1 = 0
        self.correct_stdev_choice_2 = 0
        self.correct_stdev_choice_3 = 0
        self.correct_stdev_choice_4 = 0
        self.correct_stdev_choice_5 = 0
        self.correct_stdev_choice_6 = 0
        self.correct_stdev_choice_7 = 0
        self.correct_stdev_choice_8 = 0
        self.correct_mean_choice_1 = 0
        self.correct_mean_choice_2 = 0
        self.correct_mean_choice_3 = 0
        self.correct_mean_choice_4 = 0
        self.correct_mean_choice_5 = 0
        self.correct_mean_choice_6 = 0
        self.correct_mean_choice_7 = 0
        self.correct_mean_choice_8 = 0
        self.correct_cv_choice_1 = 0
        self.correct_cv_choice_2 = 0
        self.correct_cv_choice_3 = 0
        self.correct_cv_choice_4 = 0
        self.correct_cv_choice_5 = 0
        self.correct_cv_choice_6 = 0
        self.correct_cv_choice_7 = 0
        self.correct_cv_choice_8 = 0
        self.reward_lat_choice_mean_1 = 0
        self.reward_lat_choice_mean_2 = 0
        self.reward_lat_choice_mean_3 = 0
        self.reward_lat_choice_mean_4 = 0
        self.reward_lat_choice_mean_5 = 0
        self.reward_lat_choice_mean_6 = 0
        self.reward_lat_choice_mean_7 = 0
        self.reward_lat_choice_mean_8 = 0
        self.incorrect_lat_choice_mean_1 = 0
        self.incorrect_lat_choice_mean_2 = 0
        self.incorrect_lat_choice_mean_3 = 0
        self.incorrect_lat_choice_mean_4 = 0
        self.incorrect_lat_choice_mean_5 = 0
        self.incorrect_lat_choice_mean_6 = 0
        self.incorrect_lat_choice_mean_7 = 0
        self.incorrect_lat_choice_mean_8 = 0
        self.reward_A_choice_1 = 0
        self.reward_A_choice_2 = 0
        self.reward_A_choice_3 = 0
        self.reward_A_choice_4 = 0
        self.reward_A_choice_5 = 0
        self.reward_A_choice_6 = 0
        self.reward_A_choice_7 = 0
        self.reward_A_choice_8 = 0
        self.incorrect_choice_list_1 = []
        self.incorrect_choice_list_2 = []
        self.incorrect_choice_list_3 = []
        self.incorrect_choice_list_4 = []
        self.incorrect_choice_list_5 = []
        self.incorrect_choice_list_6 = []
        self.incorrect_choice_list_7 = []
        self.incorrect_choice_list_8 = []
        self.incorrect_latency_choice_Mean_1 = 0
        self.incorrect_latency_choice_Mean_2 = 0
        self.incorrect_latency_choice_Mean_3 = 0
        self.incorrect_latency_choice_Mean_4 = 0
        self.incorrect_latency_choice_Mean_5 = 0
        self.incorrect_latency_choice_Mean_6 = 0
        self.incorrect_latency_choice_Mean_7 = 0
        self.incorrect_latency_choice_Mean_8 = 0
        self.trial_choice_1 = 0
        self.trial_choice_2 = 0
        self.trial_choice_3 = 0
        self.trial_choice_4 = 0
        self.trial_choice_5 = 0
        self.trial_choice_6 = 0
        self.trial_choice_7 = 0
        self.trial_choice_8 = 0
        self.per_correct_choice_1 = 0
        self.per_correct_choice_2 = 0
        self.per_correct_choice_3 = 0
        self.per_correct_choice_4 = 0
        self.per_correct_choice_5 = 0
        self.per_correct_choice_6 = 0
        self.per_correct_choice_7 = 0
        self.per_correct_choice_8 = 0
        self.per_omission_choice_1 = 0
        self.per_omission_choice_2 = 0
        self.per_omission_choice_3 = 0
        self.per_omission_choice_4 = 0
        self.per_omission_choice_5 = 0
        self.per_omission_choice_6 = 0
        self.per_omission_choice_7 = 0
        self.per_omission_choice_8 = 0
        self.per_accuracy_choice_1 = 0
        self.per_accuracy_choice_2 = 0
        self.per_accuracy_choice_3 = 0
        self.per_accuracy_choice_4 = 0
        self.per_accuracy_choice_5 = 0
        self.per_accuracy_choice_6 = 0
        self.per_accuracy_choice_7 = 0
        self.per_accuracy_choice_8 = 0
        self.per_accuracy_lit_choice_1 = 0
        self.per_accuracy_lit_choice_2 = 0
        self.per_accuracy_lit_choice_3 = 0
        self.per_accuracy_lit_choice_4 = 0
        self.per_accuracy_lit_choice_5 = 0
        self.per_accuracy_lit_choice_6 = 0
        self.per_accuracy_lit_choice_7 = 0
        self.per_accuracy_lit_choice_8 = 0
        self.per_perseverate_choice_1 = 0
        self.per_perseverate_choice_2 = 0
        self.per_perseverate_choice_3 = 0
        self.per_perseverate_choice_4 = 0
        self.per_perseverate_choice_5 = 0
        self.per_perseverate_choice_6 = 0
        self.per_perseverate_choice_7 = 0
        self.per_perseverate_choice_8 = 0
        self.incorrect_A_choice_1 = 0
        self.incorrect_A_choice_2 = 0
        self.incorrect_A_choice_3 = 0
        self.incorrect_A_choice_4 = 0
        self.incorrect_A_choice_5 = 0
        self.incorrect_A_choice_6 = 0
        self.incorrect_A_choice_7 = 0
        self.incorrect_A_choice_8 = 0

    # General methods
    def print_to_log(self, print_string, end='\n'):
        print(print_string + end)

    def clear_task_combo_box(self):
        self.comboBox_task1.clear()
        self.comboBox_task2.clear()
        self.comboBox_task3.clear()
        self.comboBox_task4.clear()
        self.comboBox_task5.clear()
        self.comboBox_task6.clear()
        self.comboBox_task7.clear()
        self.comboBox_task8.clear()
        self.table_fill()

    def clear_srport_combo_box(self):
        self.comboBox_srport_1.clear()
        self.comboBox_srport_2.clear()
        self.comboBox_srport_3.clear()
        self.comboBox_srport_4.clear()
        self.comboBox_srport_5.clear()
        self.comboBox_srport_6.clear()
        self.comboBox_srport_7.clear()
        self.comboBox_srport_8.clear()
        self.table_fill()

    def add_to_srport_combo_box(self, ports):
        self.comboBox_srport_1.addItems(sorted(ports))
        self.comboBox_srport_2.addItems(sorted(ports))
        self.comboBox_srport_3.addItems(sorted(ports))
        self.comboBox_srport_4.addItems(sorted(ports))
        self.comboBox_srport_5.addItems(sorted(ports))
        self.comboBox_srport_6.addItems(sorted(ports))
        self.comboBox_srport_7.addItems(sorted(ports))
        self.comboBox_srport_8.addItems(sorted(ports))
        self.table_fill()

    def enable_srport_combo_box(self, state):
        self.comboBox_srport_1.setEnabled(state)
        self.comboBox_srport_2.setEnabled(state)
        self.comboBox_srport_3.setEnabled(state)
        self.comboBox_srport_4.setEnabled(state)
        self.comboBox_srport_5.setEnabled(state)
        self.comboBox_srport_6.setEnabled(state)
        self.comboBox_srport_7.setEnabled(state)
        self.comboBox_srport_8.setEnabled(state)
        self.table_fill()

    def enable_task_combo_box(self, state):
        self.comboBox_task1.setEnabled(state)
        self.comboBox_task2.setEnabled(state)
        self.comboBox_task3.setEnabled(state)
        self.comboBox_task4.setEnabled(state)
        self.comboBox_task5.setEnabled(state)
        self.comboBox_task6.setEnabled(state)
        self.comboBox_task7.setEnabled(state)
        self.comboBox_task8.setEnabled(state)
        self.table_fill()

    def combo_box_add_items(self, tasks):
        self.comboBox_task1.addItems(sorted(tasks))
        self.comboBox_task2.addItems(sorted(tasks))
        self.comboBox_task3.addItems(sorted(tasks))
        self.comboBox_task4.addItems(sorted(tasks))
        self.comboBox_task5.addItems(sorted(tasks))
        self.comboBox_task6.addItems(sorted(tasks))
        self.comboBox_task7.addItems(sorted(tasks))
        self.comboBox_task8.addItems(sorted(tasks))

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
        self.pushButton_Start5.setEnabled(False)
        self.pushButton_Stop5.setEnabled(False)
        self.pushButton_upload_5.setEnabled(False)
        self.lineEdit_subid5.setEnabled(True)
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
        self.testboxes.setEnabled(False)
        self.table_fill()

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
        self.tableWidget.setItem(3, 1,
                                 QtWidgets.QTableWidgetItem(str('Box 01')))
        self.tableWidget.setItem(4, 1,
                                 QtWidgets.QTableWidgetItem(str('Box 02')))
        self.tableWidget.setItem(5, 1,
                                 QtWidgets.QTableWidgetItem(str('Box 03')))
        self.tableWidget.setItem(6, 1,
                                 QtWidgets.QTableWidgetItem(str('Box 04')))
        self.tableWidget.setItem(7, 1,
                                 QtWidgets.QTableWidgetItem(str('Box 05')))
        self.tableWidget.setItem(8, 1,
                                 QtWidgets.QTableWidgetItem(str('Box 06')))
        self.tableWidget.setItem(9, 1,
                                 QtWidgets.QTableWidgetItem(str('Box 07')))
        self.tableWidget.setItem(10, 1,
                                 QtWidgets.QTableWidgetItem(str('Box 08')))
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
        self.tableWidget.setItem(1, 6,
                                 QtWidgets.QTableWidgetItem(str('Sample Phase')))
        self.tableWidget.setItem(1, 13,
                                 QtWidgets.QTableWidgetItem(str('Choice Phase')))
        self.tableWidget.setItem(1, 22,
                                 QtWidgets.QTableWidgetItem(str('Sample Phase')))
        self.tableWidget.setItem(1, 32,
                                 QtWidgets.QTableWidgetItem(str('Choice Phase')))
        self.tableWidget.setItem(2, 0,
                                 QtWidgets.QTableWidgetItem(str('DATA_Live')))
        self.tableWidget.setItem(2, 1,
                                 QtWidgets.QTableWidgetItem(str('Box')))
        self.tableWidget.setItem(2, 2,
                                 QtWidgets.QTableWidgetItem(str('SUB_ID')))
        self.tableWidget.setItem(2, 3,
                                 QtWidgets.QTableWidgetItem(str('TASK')))
        self.tableWidget.setItem(2, 4,
                                 QtWidgets.QTableWidgetItem(str('SP_reward')))
        self.tableWidget.setItem(2, 5,
                                 QtWidgets.QTableWidgetItem(str('Stage')))
        self.tableWidget.setItem(2, 6,
                                 QtWidgets.QTableWidgetItem(str('%Accuracy(SP)')))
        self.tableWidget.setItem(2, 7,
                                 QtWidgets.QTableWidgetItem(str('%Correct(SP)')))
        self.tableWidget.setItem(2, 8,
                                 QtWidgets.QTableWidgetItem(str('#Correct(SP)')))
        self.tableWidget.setItem(2, 9,
                                 QtWidgets.QTableWidgetItem(str('%Omission(SP)')))
        self.tableWidget.setItem(2, 10,
                                 QtWidgets.QTableWidgetItem(str('Rew. Lat.(SP)')))
        self.tableWidget.setItem(2, 11,
                                 QtWidgets.QTableWidgetItem(str('Correct Lat.(SP)')))
        self.tableWidget.setItem(2, 12,
                                 QtWidgets.QTableWidgetItem(str('SP_Correct_CV')))
        self.tableWidget.setItem(2, 13,
                                 QtWidgets.QTableWidgetItem(str('%Accuracy_lit(CP)')))
        self.tableWidget.setItem(2, 14,
                                 QtWidgets.QTableWidgetItem(str('%Accuracy(CP)')))
        self.tableWidget.setItem(2, 15,
                                 QtWidgets.QTableWidgetItem(str('% Correct(CP)')))
        self.tableWidget.setItem(2, 16,
                                 QtWidgets.QTableWidgetItem(str('#Correct(CP)')))
        self.tableWidget.setItem(2, 17,
                                 QtWidgets.QTableWidgetItem(str('%Omission(CP)')))
        self.tableWidget.setItem(2, 18,
                                 QtWidgets.QTableWidgetItem(str('Correct Lat.(CP)')))
        self.tableWidget.setItem(2, 19,
                                 QtWidgets.QTableWidgetItem(str('Premature_Correct(CP)')))
        self.tableWidget.setItem(2, 20,
                                 QtWidgets.QTableWidgetItem(str('#Choice trials(CP)')))
        self.tableWidget.setItem(2, 21,
                                 QtWidgets.QTableWidgetItem(str('CP_Correct_CV')))
        self.tableWidget.setItem(2, 22,
                                 QtWidgets.QTableWidgetItem(str('#Sample_trials(SP)')))
        self.tableWidget.setItem(2, 23,
                                 QtWidgets.QTableWidgetItem(str('#Premature(SP)')))
        self.tableWidget.setItem(2, 24,
                                 QtWidgets.QTableWidgetItem(str('%Premature(SP)')))
        self.tableWidget.setItem(2, 25,
                                 QtWidgets.QTableWidgetItem(str('#omission(SP)')))
        self.tableWidget.setItem(2, 26,
                                 QtWidgets.QTableWidgetItem(str('#Incorrect(SP)')))
        self.tableWidget.setItem(2, 27,
                                 QtWidgets.QTableWidgetItem(str('Incorrect Lat.(SP)')))
        self.tableWidget.setItem(2, 28,
                                 QtWidgets.QTableWidgetItem(str('Premature Lat.(SP)')))
        self.tableWidget.setItem(2, 29,
                                 QtWidgets.QTableWidgetItem(str('#Perseveratives(SP)')))
        self.tableWidget.setItem(2, 30,
                                 QtWidgets.QTableWidgetItem(str('%perseverative(SP)')))
        self.tableWidget.setItem(2, 31,
                                 QtWidgets.QTableWidgetItem(str('#Resp_timeouts(SP)')))
        self.tableWidget.setItem(2, 32,
                                 QtWidgets.QTableWidgetItem(str('#Incorrect(CP)')))
        self.tableWidget.setItem(2, 33,
                                 QtWidgets.QTableWidgetItem(str('#Incorrect_lit(CP)')))
        self.tableWidget.setItem(2, 34,
                                 QtWidgets.QTableWidgetItem(str('Incorrect Lat.(CP)')))
        self.tableWidget.setItem(2, 35,
                                 QtWidgets.QTableWidgetItem(str('Rew.Lat.(CP)')))
        self.tableWidget.setItem(2, 36,
                                 QtWidgets.QTableWidgetItem(str('Premature Lat.(CP)')))
        self.tableWidget.setItem(2, 37,
                                 QtWidgets.QTableWidgetItem(str('#Omission(CP)')))
        self.tableWidget.setItem(2, 38,
                                 QtWidgets.QTableWidgetItem(str('#Perseveratives(CP)')))
        self.tableWidget.setItem(2, 39,
                                 QtWidgets.QTableWidgetItem(str('%Perseverative(CP)')))
        self.tableWidget.setItem(2, 40,
                                 QtWidgets.QTableWidgetItem(str('#Resp_timeouts(CP)')))
        self.tableWidget.setItem(2, 41,
                                 QtWidgets.QTableWidgetItem(str('#Receptacle_entries')))
        self.tableWidget.setItem(2, 42,
                                 QtWidgets.QTableWidgetItem(str('#Nosepokes_5poke')))
        self.tableWidget.setItem(2, 43,
                                 QtWidgets.QTableWidgetItem(str('#Premature_incorrect(CP)')))
        self.tableWidget.setItem(2, 44,
                                 QtWidgets.QTableWidgetItem(str('Remarks')))
        self.tableWidget.setItem(2, 47,
                                 QtWidgets.QTableWidgetItem(str('Correct_lat_stdev(SP)')))
        self.tableWidget.setItem(2, 48,
                                 QtWidgets.QTableWidgetItem(str('Correct_lat_stdev(CP)')))
        self.tableWidget.setItem(2, 49,
                                 QtWidgets.QTableWidgetItem(str('Correct_lat_list(SP)')))
        self.tableWidget.setItem(2, 50,
                                 QtWidgets.QTableWidgetItem(str('Correct_lat_list(CP)')))
        self.tableWidget.setItem(2, 51,
                                 QtWidgets.QTableWidgetItem(str('Rew_lat_list(SP)')))
        self.tableWidget.setItem(2, 52,
                                 QtWidgets.QTableWidgetItem(str('Rew_lat_list(CP)')))
        self.tableWidget.setItem(2, 53,
                                 QtWidgets.QTableWidgetItem(str('incorrect_lat_list(SP)')))
        self.tableWidget.setItem(2, 54,
                                 QtWidgets.QTableWidgetItem(str('incorrect_lat_list(CP)')))

    def test_data_path_1(self):
        # Checks whether data dir and subject ID are valid.
        self.data_dir = self.lineEdit_data_dir.text()
        subject_id_1 = self.lineEdit_subid1.text()
        if os.path.isdir(self.data_dir) and subject_id_1:
            self.pushButton_Start1.setText('RECORD')
            self.pushButton_Start_all.setText('Record(sel)')
            return True
        else:
            self.pushButton_Start1.setText('START')
            self.pushButton_Start_all.setText('START')

    def test_data_path_2(self):
        # Checks whether data dir and subject ID are valid.
        self.data_dir = self.lineEdit_data_dir.text()
        subject_id_2 = self.lineEdit_subid2.text()
        if os.path.isdir(self.data_dir) and subject_id_2:
            self.pushButton_Start2.setText('RECORD')
            self.pushButton_Start_all.setText('Record(sel)')
            return True
        else:
            self.pushButton_Start2.setText('START')

    def test_data_path_3(self):
        # Checks whether data dir and subject ID are valid.
        self.data_dir = self.lineEdit_data_dir.text()
        subject_id_3 = self.lineEdit_subid3.text()
        if os.path.isdir(self.data_dir) and subject_id_3:
            self.pushButton_Start3.setText('RECORD')
            self.pushButton_Start_all.setText('Record(sel)')
            return True
        else:
            self.pushButton_Start3.setText('START')

    def test_data_path_4(self):
        # Checks whether data dir and subject ID are valid.
        self.data_dir = self.lineEdit_data_dir.text()
        subject_id_4 = self.lineEdit_subid4.text()
        if os.path.isdir(self.data_dir) and subject_id_4:
            self.pushButton_Start4.setText('RECORD')
            self.pushButton_Start_all.setText('Record(sel)')
            return True
        else:
            self.pushButton_Start4.setText('START')

    def test_data_path_5(self):
        # Checks whether data dir and subject ID are valid.
        self.data_dir = self.lineEdit_data_dir.text()
        subject_id_5 = self.lineEdit_subid5.text()
        if os.path.isdir(self.data_dir) and subject_id_5:
            self.pushButton_Start5.setText('RECORD')
            self.pushButton_Start_all.setText('Record(sel)')
            return True
        else:
            self.pushButton_Start5.setText('START')

    def test_data_path_6(self):
        # Checks whether data dir and subject ID are valid.
        self.data_dir = self.lineEdit_data_dir.text()
        subject_id_6 = self.lineEdit_subid6.text()
        if os.path.isdir(self.data_dir) and subject_id_6:
            self.pushButton_Start6.setText('RECORD')
            self.pushButton_Start_all.setText('Record(sel)')
            return True
        else:
            self.pushButton_Start6.setText('START')

    def test_data_path_7(self):
        # Checks whether data dir and subject ID are valid.
        self.data_dir = self.lineEdit_data_dir.text()
        subject_id_7 = self.lineEdit_subid7.text()
        if os.path.isdir(self.data_dir) and subject_id_7:
            self.pushButton_Start7.setText('RECORD')
            self.pushButton_Start_all.setText('Record(sel)')
            return True
        else:
            self.pushButton_Start7.setText('START')

    def test_data_path_8(self):
        # Checks whether data dir and subject ID are valid.
        self.data_dir = self.lineEdit_data_dir.text()
        subject_id_8 = self.lineEdit_subid8.text()
        if os.path.isdir(self.data_dir) and subject_id_8:
            self.pushButton_Start8.setText('RECORD')
            self.pushButton_Start_all.setText('Record(sel)')
            return True
        else:
            self.pushButton_Start8.setText('START')

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
        tasks = set([t.split('.')[0] for t in os.listdir(tasks_dir_DMTP)
                     if t[-3:] == '.py'])
        if not tasks == self.available_tasks:
            self.clear_task_combo_box()
            self.combo_box_add_items(sorted(tasks))
            self.available_tasks = tasks
        if self.task_1:
            try:
                task_1 = self.comboBox_task1.currentText()
                task_path_1 = os.path.join(tasks_dir_DMTP, task_1 + '.py')
                if not self.task_hash_1 == _djb2_file(task_path_1):  # Task file modified.
                    self.task_changed_1()
            except FileNotFoundError:
                pass
        if self.task_2:
            try:
                task_2 = self.comboBox_task2.currentText()
                task_path_2 = os.path.join(tasks_dir_DMTP, task_2 + '.py')
                if not self.task_hash_2 == _djb2_file(task_path_2):  # Task file modified.
                    self.task_changed_2()
            except FileNotFoundError:
                pass
        if self.task_3:
            try:
                task_3 = self.comboBox_task3.currentText()
                task_path_3 = os.path.join(tasks_dir_DMTP, task_3 + '.py')
                if not self.task_hash_3 == _djb2_file(task_path_3):  # Task file modified.
                    self.task_changed_3()
            except FileNotFoundError:
                pass
        if self.task_4:
            try:
                task_4 = self.comboBox_task4.currentText()
                task_path_4 = os.path.join(tasks_dir_DMTP, task_4 + '.py')
                if not self.task_hash_4 == _djb2_file(task_path_4):  # Task file modified.
                    self.task_changed_4()
            except FileNotFoundError:
                pass
        if self.task_5:
            try:
                task_5 = self.comboBox_task5.currentText()
                task_path_5 = os.path.join(tasks_dir_DMTP, task_5 + '.py')
                if not self.task_hash_5 == _djb2_file(task_path_5):  # Task file modified.
                    self.task_changed_5()
            except FileNotFoundError:
                pass
        if self.task_6:
            try:
                task_6 = self.comboBox_task6.currentText()
                task_path_6 = os.path.join(tasks_dir_DMTP, task_6 + '.py')
                if not self.task_hash_6 == _djb2_file(task_path_6):  # Task file modified.
                    self.task_changed_6()
            except FileNotFoundError:
                pass
        if self.task_7:
            try:
                task_7 = self.comboBox_task7.currentText()
                task_path_7 = os.path.join(tasks_dir_DMTP, task_7 + '.py')
                if not self.task_hash_7 == _djb2_file(task_path_7):  # Task file modified.
                    self.task_changed_7()
            except FileNotFoundError:
                pass
        if self.task_8:
            try:
                task_8 = self.comboBox_task8.currentText()
                task_path_8 = os.path.join(tasks_dir_DMTP, task_8 + '.py')
                if not self.task_hash_8 == _djb2_file(task_path_8):  # Task file modified.
                    self.task_changed_8()
            except FileNotFoundError:
                pass

    def task_changed_1(self):
        self.uploaded_1 = False
        self.pushButton_upload_1.setText('Upload')
        self.pushButton_Start1.setEnabled(False)
        self.table_fill()

    def task_changed_2(self):
        self.uploaded_2 = False
        self.pushButton_upload_2.setText('Upload')
        self.pushButton_Start2.setEnabled(False)
        self.table_fill()

    def task_changed_3(self):
        self.uploaded_3 = False
        self.pushButton_upload_3.setText('Upload')
        self.pushButton_Start3.setEnabled(False)
        self.table_fill()

    def task_changed_4(self):
        self.uploaded_4 = False
        self.pushButton_upload_4.setText('Upload')
        self.pushButton_Start4.setEnabled(False)
        self.table_fill()

    def task_changed_5(self):
        self.uploaded_5 = False
        self.pushButton_upload_5.setText('Upload')
        self.pushButton_Start5.setEnabled(False)
        self.table_fill()

    def task_changed_6(self):
        self.uploaded_6 = False
        self.pushButton_upload_6.setText('Upload')
        self.pushButton_Start6.setEnabled(False)
        self.table_fill()

    def task_changed_7(self):
        self.uploaded_7 = False
        self.pushButton_upload_7.setText('Upload')
        self.pushButton_Start7.setEnabled(False)
        self.table_fill()

    def task_changed_8(self):
        self.uploaded_8 = False
        self.pushButton_upload_8.setText('Upload')
        self.pushButton_Start8.setEnabled(False)
        self.table_fill()

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
            self.pushButton_Connect_all.setText('Disc..(all)')
            self.lineEdit_status_1.setText('Connected')
            self.testboxes.setEnabled(True)
            self.table_fill()
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
            self.pushButton_Connect_all.setText('Disc..(all)')
            self.lineEdit_status_2.setText('Connected')
            self.testboxes.setEnabled(True)
            self.table_fill()
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
            self.pushButton_Connect_all.setText('Disc..(all)')
            self.lineEdit_status_3.setText('Connected')
            self.testboxes.setEnabled(True)
            self.table_fill()
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
            self.pushButton_Connect_all.setText('Disc..(all)')
            self.lineEdit_status_4.setText('Connected')
            self.testboxes.setEnabled(True)
            self.table_fill()
        except SerialException:
            self.lineEdit_status_4.setText('Connection failed')
            self.pushButton_connect_4.setEnabled(True)

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
            self.pushButton_Connect_all.setText('Disc..(all)')
            self.lineEdit_status_5.setText('Connected')
            self.testboxes.setEnabled(True)
            self.table_fill()
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
            self.pushButton_Connect_all.setText('Disc..(all)')
            self.lineEdit_status_6.setText('Connected')
            self.testboxes.setEnabled(True)
            self.table_fill()
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
            self.pushButton_Connect_all.setText('Disc..(all)')
            self.lineEdit_status_7.setText('Connected')
            self.testboxes.setEnabled(True)
            self.table_fill()
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
            self.pushButton_Connect_all.setText('Disc..(all)')
            self.lineEdit_status_8.setText('Connected')
            self.testboxes.setEnabled(True)
            self.table_fill()
        except SerialException:
            self.lineEdit_status_8.setText('Connection failed')
            self.pushButton_connect_8.setEnabled(True)

    def connect_all(self):
        self.connect_1()
        self.connect_2()
        self.connect_3()
        self.connect_4()
        self.connect_5()
        self.connect_6()
        self.connect_7()
        self.connect_8()

    def disconnect_all(self):
        self.disconnect_1()
        self.disconnect_2()
        self.disconnect_3()
        self.disconnect_4()
        self.disconnect_5()
        self.disconnect_6()
        self.disconnect_7()
        self.disconnect_8()

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
        self.pushButton_Connect_all.setText('Dis/Con')
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
        self.pushButton_Connect_all.setText('Dis/Con')
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
        self.pushButton_Connect_all.setText('Dis/Con')
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
        self.pushButton_Connect_all.setText('Dis/Con')
        self.lineEdit_status_4.setText('Not connected')
        self.lineEdit_status_4.setEnabled(False)
        self.connected_4 = False

    def disconnect_5(self):
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
        self.pushButton_Connect_all.setText('Dis/Con')
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
        self.pushButton_Connect_all.setText('Dis/Con')
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
        self.pushButton_Connect_all.setText('Dis/Con')
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
        self.pushButton_Connect_all.setText('Dis/Con')
        self.lineEdit_status_8.setText('Not connected')
        self.lineEdit_status_8.setEnabled(False)
        self.connected_8 = False

    def status_update(self, msg):
        self.lineEdit_status_1.setText(msg)
        self.lineEdit_status_2.setText(msg)
        self.lineEdit_status_3.setText(msg)
        self.lineEdit_status_4.setText(msg)
        self.lineEdit_status_5.setText(msg)
        self.lineEdit_status_6.setText(msg)
        self.lineEdit_status_7.setText(msg)
        self.lineEdit_status_8.setText(msg)

    def setup_task_all(self):
        if self.connected_1:
            try:
                task_1 = self.comboBox_task1.currentText()
                if self.uploaded_1:
                    self.lineEdit_status_1.setText('Resetting task..')
                else:
                    self.lineEdit_status_1.setText('Uploading..')
                    self.task_hash_1 = _djb2_file(os.path.join(tasks_dir_DMTP, task_1 + '.py'))
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
        if self.connected_2:
            try:
                task_2 = self.comboBox_task2.currentText()
                if self.uploaded_2:
                    self.lineEdit_status_2.setText('Resetting task..')
                else:
                    self.lineEdit_status_2.setText('Uploading..')
                    self.task_hash_2 = _djb2_file(os.path.join(tasks_dir_DMTP, task_2 + '.py'))
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
        if self.connected_3:
            try:
                task_3 = self.comboBox_task3.currentText()
                if self.uploaded_3:
                    self.lineEdit_status_3.setText('Resetting task..')
                else:
                    self.lineEdit_status_3.setText('Uploading..')
                    self.task_hash_3 = _djb2_file(os.path.join(tasks_dir_DMTP, task_3 + '.py'))
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
        if self.connected_4:
            try:
                task_4 = self.comboBox_task4.currentText()
                if self.uploaded_4:
                    self.lineEdit_status_4.setText('Resetting task..')
                else:
                    self.lineEdit_status_4.setText('Uploading..')
                    self.task_hash_4 = _djb2_file(os.path.join(tasks_dir_DMTP, task_4 + '.py'))
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
        if self.connected_5:
            try:
                task_5 = self.comboBox_task5.currentText()
                if self.uploaded_5:
                    self.lineEdit_status_5.setText('Resetting task..')
                else:
                    self.lineEdit_status_5.setText('Uploading..')
                    self.task_hash_5 = _djb2_file(os.path.join(tasks_dir_DMTP, task_5 + '.py'))
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
        if self.connected_6:
            try:
                task_6 = self.comboBox_task6.currentText()
                if self.uploaded_6:
                    self.lineEdit_status_6.setText('Resetting task..')
                else:
                    self.lineEdit_status_6.setText('Uploading..')
                    self.task_hash_6 = _djb2_file(os.path.join(tasks_dir_DMTP, task_6 + '.py'))
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
        if self.connected_7:

            try:
                task_7 = self.comboBox_task7.currentText()
                if self.uploaded_7:
                    self.lineEdit_status_7.setText('Resetting task..')
                else:
                    self.lineEdit_status_7.setText('Uploading..')
                    self.task_hash_7 = _djb2_file(os.path.join(tasks_dir_DMTP, task_7 + '.py'))
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
        if self.connected_8:

            try:
                task_8 = self.comboBox_task8.currentText()
                if self.uploaded_8:
                    self.lineEdit_status_8.setText('Resetting task..')
                else:
                    self.lineEdit_status_8.setText('Uploading..')
                    self.task_hash_8 = _djb2_file(os.path.join(tasks_dir_DMTP, task_8 + '.py'))
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

    def setup_task_test_poke(self):
        if self.connected_1:
            try:
                self.comboBox_task1.setCurrentText("Z_five_poke_test")
                task_1 = self.comboBox_task1.currentText()
                if self.uploaded_1:
                    self.lineEdit_status_1.setText('Resetting task..')
                else:
                    self.lineEdit_status_1.setText('Uploading..')
                    self.task_hash_1 = _djb2_file(os.path.join(tasks_dir_DMTP, task_1 + '.py'))
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
                self.start_task_1()
                self.pushButton_upload_1.setText('Reset')
            except PyboardError:
                self.lineEdit_status_1.setText('Error setting up state machine.')
        if self.connected_2:
            try:
                self.comboBox_task2.setCurrentText("Z_five_poke_test")
                task_2 = self.comboBox_task2.currentText()
                if self.uploaded_2:
                    self.lineEdit_status_2.setText('Resetting task..')
                else:
                    self.lineEdit_status_2.setText('Uploading..')
                    self.task_hash_2 = _djb2_file(os.path.join(tasks_dir_DMTP, task_2 + '.py'))
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
                self.start_task_2()
                self.pushButton_upload_2.setText('Reset')
            except PyboardError:
                self.lineEdit_status_2.setText('Error setting up state machine.')
        if self.connected_3:
            try:
                self.comboBox_task3.setCurrentText("Z_five_poke_test")
                task_3 = self.comboBox_task3.currentText()
                if self.uploaded_3:
                    self.lineEdit_status_3.setText('Resetting task..')
                else:
                    self.lineEdit_status_3.setText('Uploading..')
                    self.task_hash_3 = _djb2_file(os.path.join(tasks_dir_DMTP, task_3 + '.py'))
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
                self.start_task_3()
                self.pushButton_upload_3.setText('Reset')
            except PyboardError:
                self.lineEdit_status_3.setText('Error setting up state machine.')
        if self.connected_4:
            try:
                self.comboBox_task4.setCurrentText("Z_five_poke_test")
                task_4 = self.comboBox_task4.currentText()
                if self.uploaded_4:
                    self.lineEdit_status_4.setText('Resetting task..')
                else:
                    self.lineEdit_status_4.setText('Uploading..')
                    self.task_hash_4 = _djb2_file(os.path.join(tasks_dir_DMTP, task_4 + '.py'))
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
                self.start_task_4()
                self.pushButton_upload_4.setText('Reset')
            except PyboardError:
                self.lineEdit_status_4.setText('Error setting up state machine.')
        if self.connected_5:
            try:
                self.comboBox_task5.setCurrentText("Z_five_poke_test")
                task_5 = self.comboBox_task5.currentText()
                if self.uploaded_5:
                    self.lineEdit_status_5.setText('Resetting task..')
                else:
                    self.lineEdit_status_5.setText('Uploading..')
                    self.task_hash_5 = _djb2_file(os.path.join(tasks_dir_DMTP, task_5 + '.py'))
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
                self.start_task_5()
                self.pushButton_upload_5.setText('Reset')
            except PyboardError:
                self.lineEdit_status_5.setText('Error setting up state machine.')
        if self.connected_6:
            try:
                self.comboBox_task6.setCurrentText("Z_five_poke_test")
                task_6 = self.comboBox_task6.currentText()
                if self.uploaded_6:
                    self.lineEdit_status_6.setText('Resetting task..')
                else:
                    self.lineEdit_status_6.setText('Uploading..')
                    self.task_hash_6 = _djb2_file(os.path.join(tasks_dir_DMTP, task_6 + '.py'))
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
                self.start_task_6()
                self.pushButton_upload_6.setText('Reset')
            except PyboardError:
                self.lineEdit_status_6.setText('Error setting up state machine.')
        if self.connected_7:
            try:
                self.comboBox_task7.setCurrentText("Z_five_poke_test")
                task_7 = self.comboBox_task7.currentText()
                if self.uploaded_7:
                    self.lineEdit_status_7.setText('Resetting task..')
                else:
                    self.lineEdit_status_7.setText('Uploading..')
                    self.task_hash_7 = _djb2_file(os.path.join(tasks_dir_DMTP, task_7 + '.py'))
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
                self.start_task_7()
                self.pushButton_upload_7.setText('Reset')
            except PyboardError:
                self.lineEdit_status_7.setText('Error setting up state machine.')
        if self.connected_8:
            try:
                self.comboBox_task8.setCurrentText("Z_five_poke_test")
                task_8 = self.comboBox_task8.currentText()
                if self.uploaded_8:
                    self.lineEdit_status_8.setText('Resetting task..')
                else:
                    self.lineEdit_status_8.setText('Uploading..')
                    self.task_hash_8 = _djb2_file(os.path.join(tasks_dir_DMTP, task_8 + '.py'))
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
                self.start_task_8()
                self.pushButton_upload_8.setText('Reset')
            except PyboardError:
                self.lineEdit_status_8.setText('Error setting up state machine.')


    def setup_task_1(self):
        try:
            task_1 = self.comboBox_task1.currentText()
            if self.uploaded_1:
                self.lineEdit_status_1.setText('Resetting task..')
            else:
                self.lineEdit_status_1.setText('Uploading..')
                self.task_hash_1 = _djb2_file(os.path.join(tasks_dir_DMTP, task_1 + '.py'))
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
                self.task_hash_2 = _djb2_file(os.path.join(tasks_dir_DMTP, task_2 + '.py'))
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
                self.task_hash_3 = _djb2_file(os.path.join(tasks_dir_DMTP, task_3 + '.py'))
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
                self.task_hash_4 = _djb2_file(os.path.join(tasks_dir_DMTP, task_4 + '.py'))
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

    def setup_task_5(self):
        try:
            task_5 = self.comboBox_task5.currentText()
            if self.uploaded_5:
                self.lineEdit_status_5.setText('Resetting task..')
            else:
                self.lineEdit_status_5.setText('Uploading..')
                self.task_hash_5 = _djb2_file(os.path.join(tasks_dir_DMTP, task_5 + '.py'))
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
                self.task_hash_6 = _djb2_file(os.path.join(tasks_dir_DMTP, task_6 + '.py'))
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
                self.task_hash_7 = _djb2_file(os.path.join(tasks_dir_DMTP, task_7 + '.py'))
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
                self.task_hash_8 = _djb2_file(os.path.join(tasks_dir_DMTP, task_8 + '.py'))
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

    def select_data_dir(self):
        self.lineEdit_data_dir.setText(
            QtGui.QFileDialog.getExistingDirectory(self, 'Select data folder', data_dir))

    def start_task_1(self):
        if self.test_data_path_1():
            self.subject_id_1 = str(self.lineEdit_subid1.text())
            self.data_logger1.open_data_file(self.data_dir, self.exp_name, self.subject_id_1, self.project)
        self.resettable.setEnabled(False)
        self.tableWidget.setItem(3, 2,
                                 QtWidgets.QTableWidgetItem(str(self.subject_id_1)))
        self.tableWidget.setItem(3, 3,
                                 QtWidgets.QTableWidgetItem(str(self.task_1)))
        self.board_1.start_framework()
        self.start_time_1 = time.time()
        # self.task_plot.run_start()
        self.comboBox_task1.setEnabled(False)
        self.pushButton_upload_1.setEnabled(False)
        self.pushButton_Start1.setEnabled(False)
        self.pushButton_config_1.setEnabled(False)
        self.pushButton_Stop1.setEnabled(True)
        self.pushButton_Stop_all.setEnabled(True)
        self.testboxes.setEnabled(False)
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
        self.tableWidget.setItem(4, 2,
                                 QtWidgets.QTableWidgetItem(str(self.subject_id_2)))
        self.tableWidget.setItem(4, 3,
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
        self.pushButton_Stop_all.setEnabled(True)
        self.pushButton_connect_2.setEnabled(False)
        self.lineEdit_subid1.setEnabled(True)
        print('\nRun started at: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        self.process_timer_2.start(update_interval)
        self.refresh_timer_2.stop()
        self.lineEdit_status_2.setText('Running: ' + self.task_2)
        self.testboxes.setEnabled(False)
        self.table_fill()

    def start_task_3(self):
        if self.test_data_path_3():
            self.subject_id_3 = str(self.lineEdit_subid3.text())
            self.data_logger3.open_data_file(self.data_dir, self.exp_name, self.subject_id_3, self.project)
        self.tableWidget.setItem(5, 2,
                                 QtWidgets.QTableWidgetItem(str(self.subject_id_3)))
        self.tableWidget.setItem(5, 3,
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
        self.pushButton_Stop_all.setEnabled(True)
        self.pushButton_connect_3.setEnabled(False)
        print('\nRun started at: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        self.process_timer_3.start(update_interval)
        self.refresh_timer_3.stop()
        self.lineEdit_status_3.setText('Running: ' + self.task_3)
        self.testboxes.setEnabled(False)
        self.table_fill()

    def start_task_4(self):
        if self.test_data_path_4():
            self.subject_id_4 = str(self.lineEdit_subid4.text())
            self.data_logger4.open_data_file(self.data_dir, self.exp_name, self.subject_id_4, self.project)
        self.tableWidget.setItem(6, 2,
                                 QtWidgets.QTableWidgetItem(str(self.subject_id_4)))
        self.tableWidget.setItem(6, 3,
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
        self.pushButton_Stop_all.setEnabled(True)
        self.pushButton_connect_4.setEnabled(False)
        self.lineEdit_subid4.setEnabled(True)
        print('\nRun started at: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        self.process_timer_4.start(update_interval)
        self.refresh_timer_4.stop()
        self.lineEdit_status_4.setText('Running: ' + self.task_4)
        self.testboxes.setEnabled(False)
        self.table_fill()

    def start_task_5(self):
        if self.test_data_path_5():
            self.subject_id_5 = str(self.lineEdit_subid5.text())
            self.data_logger5.open_data_file(self.data_dir, self.exp_name, self.subject_id_5, self.project)
        self.tableWidget.setItem(7, 2,
                                 QtWidgets.QTableWidgetItem(str(self.subject_id_5)))
        self.tableWidget.setItem(7, 3,
                                 QtWidgets.QTableWidgetItem(str(self.task_5)))
        self.board_5.start_framework()
        self.start_time_5 = time.time()
        self.resettable.setEnabled(False)
        # self.task_plot.run_start()
        self.comboBox_task5.setEnabled(False)
        self.pushButton_upload_5.setEnabled(False)
        self.pushButton_Start5.setEnabled(False)
        self.pushButton_config_5.setEnabled(False)
        self.pushButton_Stop5.setEnabled(True)
        self.pushButton_Stop_all.setEnabled(True)
        self.pushButton_connect_5.setEnabled(False)
        self.lineEdit_subid5.setEnabled(True)
        print('\nRun started at: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        self.process_timer_5.start(update_interval)
        self.refresh_timer_5.stop()
        self.lineEdit_status_5.setText('Running: ' + self.task_5)
        self.testboxes.setEnabled(False)
        self.table_fill()

    def start_task_6(self):
        if self.test_data_path_6():
            self.subject_id_6 = str(self.lineEdit_subid6.text())
            self.data_logger6.open_data_file(self.data_dir, self.exp_name, self.subject_id_6, self.project)
        self.tableWidget.setItem(8, 2,
                                 QtWidgets.QTableWidgetItem(str(self.subject_id_6)))
        self.tableWidget.setItem(8, 3,
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
        self.pushButton_Stop_all.setEnabled(True)
        self.pushButton_connect_6.setEnabled(False)
        self.lineEdit_subid6.setEnabled(True)
        print('\nRun started at: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        self.process_timer_6.start(update_interval)
        self.refresh_timer_6.stop()
        self.lineEdit_status_6.setText('Running: ' + self.task_6)
        self.testboxes.setEnabled(False)
        self.table_fill()

    def start_task_7(self):
        if self.test_data_path_7():
            self.subject_id_7 = str(self.lineEdit_subid7.text())
            self.data_logger7.open_data_file(self.data_dir, self.exp_name, self.subject_id_7, self.project)
        self.tableWidget.setItem(9, 2,
                                 QtWidgets.QTableWidgetItem(str(self.subject_id_7)))
        self.tableWidget.setItem(9, 3,
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
        self.pushButton_Stop_all.setEnabled(True)
        self.pushButton_connect_7.setEnabled(False)
        self.lineEdit_subid7.setEnabled(True)
        print('\nRun started at: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        self.process_timer_7.start(update_interval)
        self.refresh_timer_7.stop()
        self.lineEdit_status_7.setText('Running: ' + self.task_7)
        self.testboxes.setEnabled(False)
        self.table_fill()

    def start_task_8(self):
        if self.test_data_path_8():
            self.subject_id_8 = str(self.lineEdit_subid8.text())
            self.data_logger8.open_data_file(self.data_dir, self.exp_name, self.subject_id_8, self.project)
        self.tableWidget.setItem(10, 2,
                                 QtWidgets.QTableWidgetItem(str(self.subject_id_8)))
        self.tableWidget.setItem(10, 3,
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
        self.pushButton_Stop_all.setEnabled(True)
        self.pushButton_connect_8.setEnabled(False)
        self.lineEdit_subid8.setEnabled(True)
        print('\nRun started at: {}\n'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        self.process_timer_8.start(update_interval)
        self.refresh_timer_8.stop()
        self.lineEdit_status_8.setText('Running: ' + self.task_8)
        self.testboxes.setEnabled(False)
        self.table_fill()

    def record_task_all(self):
        try:
            self.start_task_1()
            self.start_task_2()
            self.start_task_3()
            self.start_task_4()
            self.start_task_5()
            self.start_task_6()
            self.start_task_7()
            self.start_task_8()
        except AttributeError:
            pass



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
        self.testboxes.setEnabled(True)

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
        self.testboxes.setEnabled(True)

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
        self.testboxes.setEnabled(True)

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
        self.testboxes.setEnabled(True)

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
        self.testboxes.setEnabled(True)

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
        self.testboxes.setEnabled(True)

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
        self.testboxes.setEnabled(True)

    def stop_task_all(self):
        try:
            self.stop_task_1()
            self.stop_task_2()
            self.stop_task_3()
            self.stop_task_4()
            self.stop_task_5()
            self.stop_task_6()
            self.stop_task_7()
            self.stop_task_8()
        except AttributeError:
            pass


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
            run_time_6 = time.time() - self.start_time_6
            run_time_6 = str(timedelta(seconds=run_time_6))[:7]
            self.lcdNumber_Timer_BOX6.display(run_time_6)
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

    def update_data_table_1(self, new_data_1):
        if new_data_1:
            for value in new_data_1:
                for string in value:
                    self.tableWidget.setItem(3, 0,
                                             QtWidgets.QTableWidgetItem("{:.2f}".format(value[2])))
                    if "sample_phase" in str(string):
                        self.sample_start_time_1 = time.time()
                        self.tableWidget.setItem(3, 58,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.sample_start_time_1)))
                    elif "Correct_sample" in str(string):
                        self.Correct_sample_1 += 1
                        self.tableWidget.setItem(3, 8,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Correct_sample_1)))
                        try:
                            self.correct_latency_sample_1 = time.time() - self.sample_start_time_1
                            self.correct_cv_sample_list_1.append(self.correct_latency_sample_1)
                            self.tableWidget.setItem(3, 49,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_sample_list_1)))
                            self.correct_sample_resp_time_1 = time.time()
                            self.tableWidget.setItem(3, 59,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_sample_resp_time_1)))
                            self.correct_A_sample_1 = [float(i) for i in self.correct_cv_sample_list_1]
                            self.correct_stdev_sample_1 = statistics.stdev(self.correct_A_sample_1)
                            self.tableWidget.setItem(3, 47,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_stdev_sample_1)))
                            self.correct_mean_sample_1 = statistics.mean(self.correct_A_sample_1)
                            self.tableWidget.setItem(3, 11,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_mean_sample_1)))
                            self.correct_cv_sample_1 = self.correct_stdev_sample_1 / self.correct_mean_sample_1
                            self.tableWidget.setItem(3, 12,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_sample_1)))
                        except:
                            pass
                    elif 'Incorrect_sample' in str(string):
                        self.Incorrect_sample_1 += 1
                        self.tableWidget.setItem(3, 26,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Incorrect_sample_1)))
                        try:
                            self.incorrect_latency_sample_1 = time.time() - self.sample_start_time_1
                            self.incorrect_cv_sample_list_1.append(self.incorrect_latency_sample_1)
                            self.tableWidget.setItem(3, 53,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_cv_sample_list_1)))
                            self.incorrect_A_sample_1 = [float(i) for i in self.incorrect_cv_sample_list_1]
                            self.incorrect_lat_sample_mean_1 = statistics.mean(self.incorrect_A_sample_1)
                            self.tableWidget.setItem(3, 27,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lat_sample_mean_1)))
                        except:
                            pass
                    elif 'omission_sample' in str(string):
                        self.omission_sample_1 += 1
                        self.tableWidget.setItem(3, 25,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.omission_sample_1)))
                    elif 'reward_sample_taken' in str(string):
                        try:
                            self.Reward_Latency_sample_1 = time.time() - self.correct_sample_resp_time_1
                            self.reward_lat_sample_list_1.append(self.Reward_Latency_sample_1)
                            self.tableWidget.setItem(3, 51,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_sample_list_1)))
                            self.reward_A_sample_1 = [float(i) for i in self.reward_lat_sample_list_1]
                            self.reward_lat_sample_mean_1 = statistics.mean(self.reward_A_sample_1)
                            self.tableWidget.setItem(3, 10,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_sample_mean_1)))
                        except:
                            pass
                    elif "iti_sample" in str(string):
                        self.iti_start_time_1 = time.time()
                        self.tableWidget.setItem(3, 60,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.iti_start_time_1)))
                    elif 'Premature_response' in str(string):
                        self.Premature_sample_1 += 1
                        self.tableWidget.setItem(3, 23,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_sample_1)))
                        try:
                            self.Premature_Response_Latency_sample_1 = time.time() - self.iti_start_time_1
                            self.Premature_latancy_sample_list_1.append(self.Premature_Response_Latency_sample_1)
                            self.tableWidget.setItem(3, 56,
                                                     QtWidgets.QTableWidgetItem(
                                                         str(self.Premature_latancy_sample_list_1)))
                            self.premature_sample_1 = [float(i) for i in self.Premature_latancy_sample_list_1]
                            self.Premature_sample_mean_1 = statistics.mean(self.premature_sample_1)
                            self.tableWidget.setItem(3, 28,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_sample_mean_1)))
                        except:
                            pass
                    elif 'perseverate_sample' in str(string):
                        self.perseverate_sample_1 += 1
                        self.tableWidget.setItem(3, 29,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.perseverate_sample_1)))
                    elif 'attempts_dur_penalty_sample' in str(string):
                        self.resp_timeout_1 += 1
                        self.tableWidget.setItem(3, 31,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.resp_timeout_1)))
                    elif "choice_phase" in str(string):
                        self.choice_start_time_1 = time.time()
                        self.tableWidget.setItem(3, 61,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.choice_start_time_1)))
                    elif "Correct_choice" in str(string):
                        self.Correct_choice_1 += 1
                        self.tableWidget.setItem(3, 16,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Correct_choice_1)))
                        try:
                            self.correct_latency_choice_1 = time.time() - self.choice_start_time_1
                            self.correct_cv_choice_list_1.append(self.correct_latency_choice_1)
                            self.tableWidget.setItem(3, 50,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_choice_list_1)))
                            self.correct_choice_resp_time_1 = time.time()
                            self.tableWidget.setItem(3, 62,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_choice_resp_time_1)))
                            self.correct_A_choice_1 = [float(i) for i in self.correct_cv_choice_list_1]
                            self.correct_stdev_choice_1 = statistics.stdev(self.correct_A_choice_1)
                            self.tableWidget.setItem(3, 48,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_stdev_choice_1)))
                            self.correct_mean_choice_1 = statistics.mean(self.correct_A_choice_1)
                            self.tableWidget.setItem(3, 18,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_mean_choice_1)))
                            self.correct_cv_choice_1 = self.correct_stdev_choice_1 / self.correct_mean_choice_1
                            self.tableWidget.setItem(3, 21,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_choice_1)))
                        except:
                            pass
                    elif 'reward_choice_taken' in str(string):
                        try:
                            self.Reward_Latency_choice_1 = time.time() - self.correct_choice_resp_time_1
                            self.reward_lat_choice_list_1.append(self.Reward_Latency_choice_1)
                            self.tableWidget.setItem(3, 52,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_choice_list_1)))
                            self.reward_A_choice_1 = [float(i) for i in self.reward_lat_choice_list_1]
                            self.reward_lat_choice_mean_1 = statistics.mean(self.reward_A_choice_1)
                            self.tableWidget.setItem(3, 35,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_choice_mean_1)))
                        except:
                            pass
                    elif "incorrect_choice_lit" in str(string):
                        self.incorrect_lit_choice_1 += 1
                        self.tableWidget.setItem(3, 33,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lit_choice_1)))
                    elif 'Incorrect_choice' in str(string):
                        self.Incorrect_choice_1 += 1
                        self.tableWidget.setItem(3, 32,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Incorrect_choice_1)))
                        try:
                            self.incorrect_latency_choice_1 = time.time() - self.choice_start_time_1
                            self.incorrect_choice_list_1.append(self.incorrect_latency_choice_1)
                            self.tableWidget.setItem(3, 54,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_choice_list_1)))
                            self.incorrect_A_choice_1 = [float(i) for i in self.incorrect_choice_list_1]
                            self.incorrect_lat_choice_mean_1 = statistics.mean(self.incorrect_A_choice_1)
                            self.tableWidget.setItem(3, 34,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lat_choice_mean_1)))
                        except:
                            pass
                    elif 'omission_choice' in str(string):
                        self.omission_choice_1 += 1
                        self.tableWidget.setItem(3, 37,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.omission_choice_1)))
                    elif 'Premature_choice_correct' in str(string):
                        self.Premature_choice_correct_1 += 1
                        self.tableWidget.setItem(3, 19,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_correct_1)))
                    elif "delay" in str(string):
                        self.delay_start_time_1 = time.time()
                        self.tableWidget.setItem(3, 64,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.delay_start_time_1)))
                    elif 'Premature_choice_incorrect' in str(string):
                        self.Premature_choice_incorrect_1 += 1
                        self.tableWidget.setItem(3, 43,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_incorrect_1)))
                        try:
                            self.Premature_Response_Latency_choice_1 = time.time() - self.delay_start_time_1
                            self.Premature_latancy_choice_list_1.append(self.Premature_Response_Latency_choice_1)
                            self.tableWidget.setItem(3, 56,
                                                     QtWidgets.QTableWidgetItem(
                                                         str(self.Premature_latancy_choice_list_1)))
                            self.premature_choice_1 = [float(i) for i in self.Premature_latancy_choice_list_1]
                            self.Premature_choice_mean_1 = statistics.mean(self.premature_choice_1)
                            self.tableWidget.setItem(3, 28,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_mean_1)))
                        except:
                            pass
                    elif 'perseverate_choice' in str(string):
                        self.perseverate_choice_1 += 1
                        self.tableWidget.setItem(3, 38,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.perseverate_choice_1)))
                    elif 'attempts_dur_penalty_choice' in str(string):
                        self.resp_timeout_1 += 1
                        self.tableWidget.setItem(3, 40,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.resp_timeout_1)))
                    elif 'receptacle_entries' in str(string):
                        self.Receptacle_entries_1 += 1
                        self.tableWidget.setItem(3, 41,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Receptacle_entries_1)))
                    elif '5_poke_entries' in str(string):
                        self.Nosepokes_5poke_1 += 1
                        self.tableWidget.setItem(3, 42,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Nosepokes_5poke_1)))
                    elif 'SP_reward' in str(string):
                        self.SP_reward_1 = value[2][12:]
                        self.tableWidget.setItem(3, 4,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.SP_reward_1)))
                    elif 'Event Closing' in str(string):
                        self.tableWidget.setItem(3, 0,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.date)))
                    try:
                        self.per_perseverate_sample_1 = (self.perseverate_sample_1 / self.Correct_sample_1) * 100
                        self.tableWidget.setItem(3, 30,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_perseverate_sample_1)))
                        self.per_omission_sample_1 = self.omission_sample_1 / (self.Correct_sample_1
                                                                               + self.Incorrect_sample_1
                                                                               + self.omission_sample_1) * 100
                        self.tableWidget.setItem(3, 9,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_omission_sample_1)))
                        self.per_accuracy_sample_1 = (self.Correct_sample_1 / (self.Correct_sample_1
                                                                               + self.Incorrect_sample_1)) * 100
                        self.tableWidget.setItem(3, 6,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_sample_1)))
                        self.per_correct_sample_1 = (self.Correct_sample_1 / (self.Correct_sample_1
                                                                              + self.Incorrect_sample_1
                                                                              + self.omission_sample_1)) * 100
                        self.tableWidget.setItem(3, 7,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_correct_sample_1)))

                        self.per_premature_sample_1 = self.Premature_sample_1 / (self.Correct_sample_1
                                                                                 + self.Incorrect_sample_1
                                                                                 + self.omission_sample_1) * 100
                        self.tableWidget.setItem(3, 24,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_premature_sample_1)))
                        self.trial_sample_1 = (self.Correct_sample_1 + self.Incorrect_sample_1 + self.omission_sample_1)
                        self.tableWidget.setItem(3, 22,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.trial_sample_1)))
                    except ZeroDivisionError:
                        pass
                    try:
                        self.per_perseverate_choice_1 = (self.perseverate_choice_1 / self.Correct_choice_1) * 100
                        self.tableWidget.setItem(3, 39,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_perseverate_choice_1)))
                        self.per_correct_choice_1 = (self.Correct_choice_1 / (self.Correct_choice_1
                                                                              + self.Incorrect_choice_1
                                                                              + self.incorrect_lit_choice_1
                                                                              + self.omission_choice_1)) * 100
                        self.tableWidget.setItem(3, 15,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_correct_choice_1)))

                        self.per_omission_choice_1 = (self.omission_choice_1 / (self.incorrect_lit_choice_1
                                                                                + self.Correct_choice_1
                                                                                + self.Incorrect_choice_1
                                                                                + self.omission_choice_1)) * 100
                        self.tableWidget.setItem(3, 17,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_omission_choice_1)))
                        self.per_accuracy_choice_1 = (self.Correct_choice_1 / (self.Correct_choice_1
                                                                               + self.incorrect_lit_choice_1
                                                                               + self.Incorrect_choice_1)) * 100
                        self.tableWidget.setItem(3, 14,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_choice_1)))
                        self.per_accuracy_lit_choice_1 = (self.Correct_choice_1 / (self.incorrect_lit_choice_1
                                                                                   + self.Correct_choice_1)) * 100
                        self.tableWidget.setItem(3, 13,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_lit_choice_1)))
                        self.trial_choice_1 = (self.incorrect_lit_choice_1 + self.Correct_choice_1
                                               + self.Incorrect_choice_1 + self.omission_choice_1)
                        self.tableWidget.setItem(3, 20,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.trial_choice_1)))
                    except ZeroDivisionError:
                        pass

    def update_data_table_2(self, new_data_2):
        if new_data_2:
            for value in new_data_2:
                for string in value:
                    self.tableWidget.setItem(4, 0,
                                             QtWidgets.QTableWidgetItem("{:.2f}".format(value[2])))
                    if "sample_phase" in str(string):
                        self.sample_start_time_2 = time.time()
                        self.tableWidget.setItem(4, 58,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.sample_start_time_2)))
                    elif "Correct_sample" in str(string):
                        self.Correct_sample_2 += 1
                        self.tableWidget.setItem(4, 8,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Correct_sample_2)))
                        try:
                            self.correct_latency_sample_2 = time.time() - self.sample_start_time_2
                            self.correct_cv_sample_list_2.append(self.correct_latency_sample_2)
                            self.tableWidget.setItem(4, 49,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_sample_list_2)))
                            self.correct_sample_resp_time_2 = time.time()
                            self.tableWidget.setItem(4, 59,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_sample_resp_time_2)))
                            self.correct_A_sample_2 = [float(i) for i in self.correct_cv_sample_list_2]
                            self.correct_stdev_sample_2 = statistics.stdev(self.correct_A_sample_2)
                            self.tableWidget.setItem(4, 47,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_stdev_sample_2)))
                            self.correct_mean_sample_2 = statistics.mean(self.correct_A_sample_2)
                            self.tableWidget.setItem(4, 11,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_mean_sample_2)))
                            self.correct_cv_sample_2 = self.correct_stdev_sample_2 / self.correct_mean_sample_2
                            self.tableWidget.setItem(4, 12,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_sample_2)))
                        except:
                            pass
                    elif 'Incorrect_sample' in str(string):
                        self.Incorrect_sample_2 += 1
                        self.tableWidget.setItem(4, 26,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Incorrect_sample_2)))
                        try:
                            self.incorrect_latency_sample_2 = time.time() - self.sample_start_time_2
                            self.incorrect_cv_sample_list_2.append(self.incorrect_latency_sample_2)
                            self.tableWidget.setItem(4, 53,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_cv_sample_list_2)))
                            self.incorrect_A_sample_2 = [float(i) for i in self.incorrect_cv_sample_list_2]
                            self.incorrect_lat_sample_mean_2 = statistics.mean(self.incorrect_A_sample_2)
                            self.tableWidget.setItem(4, 27,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lat_sample_mean_2)))
                        except:
                            pass
                    elif 'omission_sample' in str(string):
                        self.omission_sample_2 += 1
                        self.tableWidget.setItem(4, 25,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.omission_sample_2)))
                    elif 'reward_sample_taken' in str(string):
                        try:
                            self.Reward_Latency_sample_2 = time.time() - self.correct_sample_resp_time_2
                            self.reward_lat_sample_list_2.append(self.Reward_Latency_sample_2)
                            self.tableWidget.setItem(4, 51,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_sample_list_2)))
                            self.reward_A_sample_2 = [float(i) for i in self.reward_lat_sample_list_2]
                            self.reward_lat_sample_mean_2 = statistics.mean(self.reward_A_sample_2)
                            self.tableWidget.setItem(4, 10,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_sample_mean_2)))
                        except:
                            pass
                    elif "iti_sample" in str(string):
                        self.iti_start_time_2 = time.time()
                        self.tableWidget.setItem(4, 60,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.iti_start_time_2)))
                    elif 'Premature_response' in str(string):
                        self.Premature_sample_2 += 1
                        self.tableWidget.setItem(4, 23,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_sample_2)))
                        try:
                            self.Premature_Response_Latency_sample_2 = time.time() - self.iti_start_time_2
                            self.Premature_latancy_sample_list_2.append(self.Premature_Response_Latency_sample_2)
                            self.tableWidget.setItem(4, 56,
                                                     QtWidgets.QTableWidgetItem(
                                                         str(self.Premature_latancy_sample_list_2)))
                            self.premature_sample_2 = [float(i) for i in self.Premature_latancy_sample_list_2]
                            self.Premature_sample_mean_2 = statistics.mean(self.premature_sample_2)
                            self.tableWidget.setItem(4, 28,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_sample_mean_2)))
                        except:
                            pass
                    elif 'perseverate_sample' in str(string):
                        self.perseverate_sample_2 += 1
                        self.tableWidget.setItem(4, 29,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.perseverate_sample_2)))
                    elif 'attempts_dur_penalty_sample' in str(string):
                        self.resp_timeout_2 += 1
                        self.tableWidget.setItem(4, 31,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.resp_timeout_2)))
                    elif "choice_phase" in str(string):
                        self.choice_start_time_2 = time.time()
                        self.tableWidget.setItem(4, 61,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.choice_start_time_2)))
                    elif "Correct_choice" in str(string):
                        self.Correct_choice_2 += 1
                        self.tableWidget.setItem(4, 16,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Correct_choice_2)))
                        try:
                            self.correct_latency_choice_2 = time.time() - self.choice_start_time_2
                            self.correct_cv_choice_list_2.append(self.correct_latency_choice_2)
                            self.tableWidget.setItem(4, 50,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_choice_list_2)))
                            self.correct_choice_resp_time_2 = time.time()
                            self.tableWidget.setItem(4, 62,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_choice_resp_time_2)))
                            self.correct_A_choice_2 = [float(i) for i in self.correct_cv_choice_list_2]
                            self.correct_stdev_choice_2 = statistics.stdev(self.correct_A_choice_2)
                            self.tableWidget.setItem(4, 48,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_stdev_choice_2)))
                            self.correct_mean_choice_2 = statistics.mean(self.correct_A_choice_2)
                            self.tableWidget.setItem(4, 18,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_mean_choice_2)))
                            self.correct_cv_choice_2 = self.correct_stdev_choice_2 / self.correct_mean_choice_2
                            self.tableWidget.setItem(4, 21,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_choice_2)))
                        except:
                            pass
                    elif 'reward_choice_taken' in str(string):
                        try:
                            self.Reward_Latency_choice_2 = time.time() - self.correct_choice_resp_time_2
                            self.reward_lat_choice_list_2.append(self.Reward_Latency_choice_2)
                            self.tableWidget.setItem(4, 52,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_choice_list_2)))
                            self.reward_A_choice_2 = [float(i) for i in self.reward_lat_choice_list_2]
                            self.reward_lat_choice_mean_2 = statistics.mean(self.reward_A_choice_2)
                            self.tableWidget.setItem(4, 35,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_choice_mean_2)))
                        except:
                            pass
                    elif "incorrect_choice_lit" in str(string):
                        self.incorrect_lit_choice_2 += 1
                        self.tableWidget.setItem(4, 33,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lit_choice_2)))
                    elif 'Incorrect_choice' in str(string):
                        self.Incorrect_choice_2 += 1
                        self.tableWidget.setItem(4, 32,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Incorrect_choice_2)))
                        try:
                            self.incorrect_latency_choice_2 = time.time() - self.choice_start_time_2
                            self.incorrect_choice_list_2.append(self.incorrect_latency_choice_2)
                            self.tableWidget.setItem(4, 54,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_choice_list_2)))
                            self.incorrect_A_choice_2 = [float(i) for i in self.incorrect_choice_list_2]
                            self.incorrect_lat_choice_mean_2 = statistics.mean(self.incorrect_A_choice_2)
                            self.tableWidget.setItem(4, 34,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lat_choice_mean_2)))
                        except:
                            pass
                    elif 'omission_choice' in str(string):
                        self.omission_choice_2 += 1
                        self.tableWidget.setItem(4, 37,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.omission_choice_2)))
                    elif 'Premature_choice_correct' in str(string):
                        self.Premature_choice_correct_2 += 1
                        self.tableWidget.setItem(4, 19,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_correct_2)))
                    elif "delay" in str(string):
                        self.delay_start_time_2 = time.time()
                        self.tableWidget.setItem(4, 64,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.delay_start_time_2)))
                    elif 'Premature_choice_incorrect' in str(string):
                        self.Premature_choice_incorrect_2 += 1
                        self.tableWidget.setItem(4, 43,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_incorrect_2)))
                        try:
                            self.Premature_Response_Latency_choice_2 = time.time() - self.delay_start_time_2
                            self.Premature_latancy_choice_list_2.append(self.Premature_Response_Latency_choice_2)
                            self.tableWidget.setItem(4, 56,
                                                     QtWidgets.QTableWidgetItem(
                                                         str(self.Premature_latancy_choice_list_2)))
                            self.premature_choice_2 = [float(i) for i in self.Premature_latancy_choice_list_2]
                            self.Premature_choice_mean_2 = statistics.mean(self.premature_choice_2)
                            self.tableWidget.setItem(4, 28,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_mean_2)))
                        except:
                            pass
                    elif 'perseverate_choice' in str(string):
                        self.perseverate_choice_2 += 1
                        self.tableWidget.setItem(4, 38,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.perseverate_choice_2)))
                    elif 'attempts_dur_penalty_choice' in str(string):
                        self.resp_timeout_2 += 1
                        self.tableWidget.setItem(4, 40,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.resp_timeout_2)))
                    elif 'receptacle_entries' in str(string):
                        self.Receptacle_entries_2 += 1
                        self.tableWidget.setItem(4, 41,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Receptacle_entries_2)))
                    elif '5_poke_entries' in str(string):
                        self.Nosepokes_5poke_2 += 1
                        self.tableWidget.setItem(4, 42,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Nosepokes_5poke_2)))
                    elif 'SP_reward' in str(string):
                        self.SP_reward_2 = value[2][12:]
                        self.tableWidget.setItem(4, 4,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.SP_reward_2)))
                    elif 'Event Closing' in str(string):
                        self.tableWidget.setItem(4, 0,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.date)))
                    try:
                        self.per_perseverate_sample_2 = (self.perseverate_sample_2 / self.Correct_sample_2) * 100
                        self.tableWidget.setItem(4, 30,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_perseverate_sample_2)))
                        self.per_omission_sample_2 = self.omission_sample_2 / (self.Correct_sample_2
                                                                               + self.Incorrect_sample_2
                                                                               + self.omission_sample_2) * 100
                        self.tableWidget.setItem(4, 9,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_omission_sample_2)))
                        self.per_accuracy_sample_2 = (self.Correct_sample_2 / (self.Correct_sample_2
                                                                               + self.Incorrect_sample_2)) * 100
                        self.tableWidget.setItem(4, 6,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_sample_2)))
                        self.per_correct_sample_2 = (self.Correct_sample_2 / (self.Correct_sample_2
                                                                              + self.Incorrect_sample_2
                                                                              + self.omission_sample_2)) * 100
                        self.tableWidget.setItem(4, 7,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_correct_sample_2)))

                        self.per_premature_sample_2 = self.Premature_sample_2 / (self.Correct_sample_2
                                                                                 + self.Incorrect_sample_2
                                                                                 + self.omission_sample_2) * 100
                        self.tableWidget.setItem(4, 24,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_premature_sample_2)))
                        self.trial_sample_2 = (self.Correct_sample_2 + self.Incorrect_sample_2 + self.omission_sample_2)
                        self.tableWidget.setItem(4, 22,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.trial_sample_2)))
                    except ZeroDivisionError:
                        pass
                    try:
                        self.per_perseverate_choice_2 = (self.perseverate_choice_2 / self.Correct_choice_2) * 100
                        self.tableWidget.setItem(4, 39,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_perseverate_choice_2)))
                        self.per_correct_choice_2 = (self.Correct_choice_2 / (self.Correct_choice_2
                                                                              + self.Incorrect_choice_2
                                                                              + self.incorrect_lit_choice_2
                                                                              + self.omission_choice_2)) * 100
                        self.tableWidget.setItem(4, 15,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_correct_choice_2)))

                        self.per_omission_choice_2 = (self.omission_choice_2 / (self.incorrect_lit_choice_2
                                                                                + self.Correct_choice_2
                                                                                + self.Incorrect_choice_2
                                                                                + self.omission_choice_2)) * 100
                        self.tableWidget.setItem(4, 17,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_omission_choice_2)))
                        self.per_accuracy_choice_2 = (self.Correct_choice_2 / (self.Correct_choice_2
                                                                               + self.incorrect_lit_choice_2
                                                                               + self.Incorrect_choice_2)) * 100
                        self.tableWidget.setItem(4, 14,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_choice_2)))
                        self.per_accuracy_lit_choice_2 = (self.Correct_choice_2 / (self.incorrect_lit_choice_2
                                                                                   + self.Correct_choice_2)) * 100
                        self.tableWidget.setItem(4, 13,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_lit_choice_2)))
                        self.trial_choice_2 = (self.incorrect_lit_choice_2 + self.Correct_choice_2
                                               + self.Incorrect_choice_2 + self.omission_choice_2)
                        self.tableWidget.setItem(4, 20,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.trial_choice_2)))
                    except ZeroDivisionError:
                        pass

    def update_data_table_3(self, new_data_3):
        if new_data_3:
            for value in new_data_3:
                for string in value:
                    self.tableWidget.setItem(5, 0,
                                             QtWidgets.QTableWidgetItem("{:.2f}".format(value[2])))
                    if "sample_phase" in str(string):
                        self.sample_start_time_3 = time.time()
                        self.tableWidget.setItem(5, 58,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.sample_start_time_3)))
                    elif "Correct_sample" in str(string):
                        self.Correct_sample_3 += 1
                        self.tableWidget.setItem(5, 8,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Correct_sample_3)))
                        try:
                            self.correct_latency_sample_3 = time.time() - self.sample_start_time_3
                            self.correct_cv_sample_list_3.append(self.correct_latency_sample_3)
                            self.tableWidget.setItem(5, 49,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_sample_list_3)))
                            self.correct_sample_resp_time_3 = time.time()
                            self.tableWidget.setItem(5, 59,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_sample_resp_time_3)))
                            self.correct_A_sample_3 = [float(i) for i in self.correct_cv_sample_list_3]
                            self.correct_stdev_sample_3 = statistics.stdev(self.correct_A_sample_3)
                            self.tableWidget.setItem(5, 47,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_stdev_sample_3)))
                            self.correct_mean_sample_3 = statistics.mean(self.correct_A_sample_3)
                            self.tableWidget.setItem(5, 11,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_mean_sample_3)))
                            self.correct_cv_sample_3 = self.correct_stdev_sample_3 / self.correct_mean_sample_3
                            self.tableWidget.setItem(5, 12,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_sample_3)))
                        except:
                            pass
                    elif 'Incorrect_sample' in str(string):
                        self.Incorrect_sample_3 += 1
                        self.tableWidget.setItem(5, 26,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Incorrect_sample_3)))
                        try:
                            self.incorrect_latency_sample_3 = time.time() - self.sample_start_time_3
                            self.incorrect_cv_sample_list_3.append(self.incorrect_latency_sample_3)
                            self.tableWidget.setItem(5, 53,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_cv_sample_list_3)))
                            self.incorrect_A_sample_3 = [float(i) for i in self.incorrect_cv_sample_list_3]
                            self.incorrect_lat_sample_mean_3 = statistics.mean(self.incorrect_A_sample_3)
                            self.tableWidget.setItem(5, 27,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lat_sample_mean_3)))
                        except:
                            pass
                    elif 'omission_sample' in str(string):
                        self.omission_sample_3 += 1
                        self.tableWidget.setItem(5, 25,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.omission_sample_3)))
                    elif 'reward_sample_taken' in str(string):
                        try:
                            self.Reward_Latency_sample_3 = time.time() - self.correct_sample_resp_time_3
                            self.reward_lat_sample_list_3.append(self.Reward_Latency_sample_3)
                            self.tableWidget.setItem(5, 51,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_sample_list_3)))
                            self.reward_A_sample_3 = [float(i) for i in self.reward_lat_sample_list_3]
                            self.reward_lat_sample_mean_3 = statistics.mean(self.reward_A_sample_3)
                            self.tableWidget.setItem(5, 10,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_sample_mean_3)))
                        except:
                            pass
                    elif "iti_sample" in str(string):
                        self.iti_start_time_3 = time.time()
                        self.tableWidget.setItem(5, 60,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.iti_start_time_3)))
                    elif 'Premature_response' in str(string):
                        self.Premature_sample_3 += 1
                        self.tableWidget.setItem(5, 23,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_sample_3)))
                        try:
                            self.Premature_Response_Latency_sample_3 = time.time() - self.iti_start_time_3
                            self.Premature_latancy_sample_list_3.append(self.Premature_Response_Latency_sample_3)
                            self.tableWidget.setItem(5, 56,
                                                     QtWidgets.QTableWidgetItem(
                                                         str(self.Premature_latancy_sample_list_3)))
                            self.premature_sample_3 = [float(i) for i in self.Premature_latancy_sample_list_3]
                            self.Premature_sample_mean_3 = statistics.mean(self.premature_sample_3)
                            self.tableWidget.setItem(5, 28,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_sample_mean_3)))
                        except:
                            pass
                    elif 'perseverate_sample' in str(string):
                        self.perseverate_sample_3 += 1
                        self.tableWidget.setItem(5, 29,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.perseverate_sample_3)))
                    elif 'attempts_dur_penalty_sample' in str(string):
                        self.resp_timeout_3 += 1
                        self.tableWidget.setItem(5, 31,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.resp_timeout_3)))
                    elif "choice_phase" in str(string):
                        self.choice_start_time_3 = time.time()
                        self.tableWidget.setItem(5, 61,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.choice_start_time_3)))
                    elif "Correct_choice" in str(string):
                        self.Correct_choice_3 += 1
                        self.tableWidget.setItem(5, 16,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Correct_choice_3)))
                        try:
                            self.correct_latency_choice_3 = time.time() - self.choice_start_time_3
                            self.correct_cv_choice_list_3.append(self.correct_latency_choice_3)
                            self.tableWidget.setItem(5, 50,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_choice_list_3)))
                            self.correct_choice_resp_time_3 = time.time()
                            self.tableWidget.setItem(5, 62,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_choice_resp_time_3)))
                            self.correct_A_choice_3 = [float(i) for i in self.correct_cv_choice_list_3]
                            self.correct_stdev_choice_3 = statistics.stdev(self.correct_A_choice_3)
                            self.tableWidget.setItem(5, 48,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_stdev_choice_3)))
                            self.correct_mean_choice_3 = statistics.mean(self.correct_A_choice_3)
                            self.tableWidget.setItem(5, 18,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_mean_choice_3)))
                            self.correct_cv_choice_3 = self.correct_stdev_choice_3 / self.correct_mean_choice_3
                            self.tableWidget.setItem(5, 21,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_choice_3)))
                        except:
                            pass
                    elif 'reward_choice_taken' in str(string):
                        try:
                            self.Reward_Latency_choice_3 = time.time() - self.correct_choice_resp_time_3
                            self.reward_lat_choice_list_3.append(self.Reward_Latency_choice_3)
                            self.tableWidget.setItem(5, 52,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_choice_list_3)))
                            self.reward_A_choice_3 = [float(i) for i in self.reward_lat_choice_list_3]
                            self.reward_lat_choice_mean_3 = statistics.mean(self.reward_A_choice_3)
                            self.tableWidget.setItem(5, 35,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_choice_mean_3)))
                        except:
                            pass
                    elif "incorrect_choice_lit" in str(string):
                        self.incorrect_lit_choice_3 += 1
                        self.tableWidget.setItem(5, 33,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lit_choice_3)))
                    elif 'Incorrect_choice' in str(string):
                        self.Incorrect_choice_3 += 1
                        self.tableWidget.setItem(5, 32,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Incorrect_choice_3)))
                        try:
                            self.incorrect_latency_choice_3 = time.time() - self.choice_start_time_3
                            self.incorrect_choice_list_3.append(self.incorrect_latency_choice_3)
                            self.tableWidget.setItem(5, 54,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_choice_list_3)))
                            self.incorrect_A_choice_3 = [float(i) for i in self.incorrect_choice_list_3]
                            self.incorrect_lat_choice_mean_3 = statistics.mean(self.incorrect_A_choice_3)
                            self.tableWidget.setItem(5, 34,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lat_choice_mean_3)))
                        except:
                            pass
                    elif 'omission_choice' in str(string):
                        self.omission_choice_3 += 1
                        self.tableWidget.setItem(5, 37,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.omission_choice_3)))
                    elif 'Premature_choice_correct' in str(string):
                        self.Premature_choice_correct_3 += 1
                        self.tableWidget.setItem(5, 19,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_correct_3)))
                    elif "delay" in str(string):
                        self.delay_start_time_3 = time.time()
                        self.tableWidget.setItem(5, 64,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.delay_start_time_3)))
                    elif 'Premature_choice_incorrect' in str(string):
                        self.Premature_choice_incorrect_3 += 1
                        self.tableWidget.setItem(5, 43,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_incorrect_3)))
                        try:
                            self.Premature_Response_Latency_choice_3 = time.time() - self.delay_start_time_3
                            self.Premature_latancy_choice_list_3.append(self.Premature_Response_Latency_choice_3)
                            self.tableWidget.setItem(5, 56,
                                                     QtWidgets.QTableWidgetItem(
                                                         str(self.Premature_latancy_choice_list_3)))
                            self.premature_choice_3 = [float(i) for i in self.Premature_latancy_choice_list_3]
                            self.Premature_choice_mean_3 = statistics.mean(self.premature_choice_3)
                            self.tableWidget.setItem(5, 28,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_mean_3)))
                        except:
                            pass
                    elif 'perseverate_choice' in str(string):
                        self.perseverate_choice_3 += 1
                        self.tableWidget.setItem(5, 38,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.perseverate_choice_3)))
                    elif 'attempts_dur_penalty_choice' in str(string):
                        self.resp_timeout_3 += 1
                        self.tableWidget.setItem(5, 40,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.resp_timeout_3)))
                    elif 'receptacle_entries' in str(string):
                        self.Receptacle_entries_3 += 1
                        self.tableWidget.setItem(5, 41,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Receptacle_entries_3)))
                    elif '5_poke_entries' in str(string):
                        self.Nosepokes_5poke_3 += 1
                        self.tableWidget.setItem(5, 42,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Nosepokes_5poke_3)))
                    elif 'SP_reward' in str(string):
                        self.SP_reward_3 = value[2][12:]
                        self.tableWidget.setItem(5, 4,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.SP_reward_3)))
                    elif 'Event Closing' in str(string):
                        self.tableWidget.setItem(5, 0,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.date)))
                    try:
                        self.per_perseverate_sample_3 = (self.perseverate_sample_3 / self.Correct_sample_3) * 100
                        self.tableWidget.setItem(5, 30,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_perseverate_sample_3)))
                        self.per_omission_sample_3 = self.omission_sample_3 / (self.Correct_sample_3
                                                                               + self.Incorrect_sample_3
                                                                               + self.omission_sample_3) * 100
                        self.tableWidget.setItem(5, 9,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_omission_sample_3)))
                        self.per_accuracy_sample_3 = (self.Correct_sample_3 / (self.Correct_sample_3
                                                                               + self.Incorrect_sample_3)) * 100
                        self.tableWidget.setItem(5, 6,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_sample_3)))
                        self.per_correct_sample_3 = (self.Correct_sample_3 / (self.Correct_sample_3
                                                                              + self.Incorrect_sample_3
                                                                              + self.omission_sample_3)) * 100
                        self.tableWidget.setItem(5, 7,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_correct_sample_3)))

                        self.per_premature_sample_3 = self.Premature_sample_3 / (self.Correct_sample_3
                                                                                 + self.Incorrect_sample_3
                                                                                 + self.omission_sample_3) * 100
                        self.tableWidget.setItem(5, 24,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_premature_sample_3)))
                        self.trial_sample_3 = (self.Correct_sample_3 + self.Incorrect_sample_3 + self.omission_sample_3)
                        self.tableWidget.setItem(5, 22,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.trial_sample_3)))
                    except ZeroDivisionError:
                        pass
                    try:
                        self.per_perseverate_choice_3 = (self.perseverate_choice_3 / self.Correct_choice_3) * 100
                        self.tableWidget.setItem(5, 39,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_perseverate_choice_3)))
                        self.per_correct_choice_3 = (self.Correct_choice_3 / (self.Correct_choice_3
                                                                              + self.Incorrect_choice_3
                                                                              + self.incorrect_lit_choice_3
                                                                              + self.omission_choice_3)) * 100
                        self.tableWidget.setItem(5, 15,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_correct_choice_3)))

                        self.per_omission_choice_3 = (self.omission_choice_3 / (self.incorrect_lit_choice_3
                                                                                + self.Correct_choice_3
                                                                                + self.Incorrect_choice_3
                                                                                + self.omission_choice_3)) * 100
                        self.tableWidget.setItem(5, 17,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_omission_choice_3)))
                        self.per_accuracy_choice_3 = (self.Correct_choice_3 / (self.Correct_choice_3
                                                                               + self.incorrect_lit_choice_3
                                                                               + self.Incorrect_choice_3)) * 100
                        self.tableWidget.setItem(5, 14,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_choice_3)))
                        self.per_accuracy_lit_choice_3 = (self.Correct_choice_3 / (self.incorrect_lit_choice_3
                                                                                   + self.Correct_choice_3)) * 100
                        self.tableWidget.setItem(5, 13,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_lit_choice_3)))
                        self.trial_choice_3 = (self.incorrect_lit_choice_3 + self.Correct_choice_3
                                               + self.Incorrect_choice_3 + self.omission_choice_3)
                        self.tableWidget.setItem(5, 20,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.trial_choice_3)))
                    except ZeroDivisionError:
                        pass

    def update_data_table_4(self, new_data_4):
        if new_data_4:
            for value in new_data_4:
                for string in value:
                    self.tableWidget.setItem(6, 0,
                                             QtWidgets.QTableWidgetItem("{:.2f}".format(value[2])))
                    if "sample_phase" in str(string):
                        self.sample_start_time_4 = time.time()
                        self.tableWidget.setItem(6, 58,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.sample_start_time_4)))
                    elif "Correct_sample" in str(string):
                        self.Correct_sample_4 += 1
                        self.tableWidget.setItem(6, 8,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Correct_sample_4)))
                        try:
                            self.correct_latency_sample_4 = time.time() - self.sample_start_time_4
                            self.correct_cv_sample_list_4.append(self.correct_latency_sample_4)
                            self.tableWidget.setItem(6, 49,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_sample_list_4)))
                            self.correct_sample_resp_time_4 = time.time()
                            self.tableWidget.setItem(6, 59,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_sample_resp_time_4)))
                            self.correct_A_sample_4 = [float(i) for i in self.correct_cv_sample_list_4]
                            self.correct_stdev_sample_4 = statistics.stdev(self.correct_A_sample_4)
                            self.tableWidget.setItem(6, 47,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_stdev_sample_4)))
                            self.correct_mean_sample_4 = statistics.mean(self.correct_A_sample_4)
                            self.tableWidget.setItem(6, 11,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_mean_sample_4)))
                            self.correct_cv_sample_4 = self.correct_stdev_sample_4 / self.correct_mean_sample_4
                            self.tableWidget.setItem(6, 12,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_sample_4)))
                        except:
                            pass
                    elif 'Incorrect_sample' in str(string):
                        self.Incorrect_sample_4 += 1
                        self.tableWidget.setItem(6, 26,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Incorrect_sample_4)))
                        try:
                            self.incorrect_latency_sample_4 = time.time() - self.sample_start_time_4
                            self.incorrect_cv_sample_list_4.append(self.incorrect_latency_sample_4)
                            self.tableWidget.setItem(6, 53,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_cv_sample_list_4)))
                            self.incorrect_A_sample_4 = [float(i) for i in self.incorrect_cv_sample_list_4]
                            self.incorrect_lat_sample_mean_4 = statistics.mean(self.incorrect_A_sample_4)
                            self.tableWidget.setItem(6, 27,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lat_sample_mean_4)))
                        except:
                            pass
                    elif 'omission_sample' in str(string):
                        self.omission_sample_4 += 1
                        self.tableWidget.setItem(6, 25,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.omission_sample_4)))
                    elif 'reward_sample_taken' in str(string):
                        try:
                            self.Reward_Latency_sample_4 = time.time() - self.correct_sample_resp_time_4
                            self.reward_lat_sample_list_4.append(self.Reward_Latency_sample_4)
                            self.tableWidget.setItem(6, 51,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_sample_list_4)))
                            self.reward_A_sample_4 = [float(i) for i in self.reward_lat_sample_list_4]
                            self.reward_lat_sample_mean_4 = statistics.mean(self.reward_A_sample_4)
                            self.tableWidget.setItem(6, 10,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_sample_mean_4)))
                        except:
                            pass
                    elif "iti_sample" in str(string):
                        self.iti_start_time_4 = time.time()
                        self.tableWidget.setItem(6, 60,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.iti_start_time_4)))
                    elif 'Premature_response' in str(string):
                        self.Premature_sample_4 += 1
                        self.tableWidget.setItem(6, 23,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_sample_4)))
                        try:
                            self.Premature_Response_Latency_sample_4 = time.time() - self.iti_start_time_4
                            self.Premature_latancy_sample_list_4.append(self.Premature_Response_Latency_sample_4)
                            self.tableWidget.setItem(6, 56,
                                                     QtWidgets.QTableWidgetItem(
                                                         str(self.Premature_latancy_sample_list_4)))
                            self.premature_sample_4 = [float(i) for i in self.Premature_latancy_sample_list_4]
                            self.Premature_sample_mean_4 = statistics.mean(self.premature_sample_4)
                            self.tableWidget.setItem(6, 28,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_sample_mean_4)))
                        except:
                            pass
                    elif 'perseverate_sample' in str(string):
                        self.perseverate_sample_4 += 1
                        self.tableWidget.setItem(6, 29,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.perseverate_sample_4)))
                    elif 'attempts_dur_penalty_sample' in str(string):
                        self.resp_timeout_4 += 1
                        self.tableWidget.setItem(6, 31,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.resp_timeout_4)))
                    elif "choice_phase" in str(string):
                        self.choice_start_time_4 = time.time()
                        self.tableWidget.setItem(6, 61,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.choice_start_time_4)))
                    elif "Correct_choice" in str(string):
                        self.Correct_choice_4 += 1
                        self.tableWidget.setItem(6, 16,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Correct_choice_4)))
                        try:
                            self.correct_latency_choice_4 = time.time() - self.choice_start_time_4
                            self.correct_cv_choice_list_4.append(self.correct_latency_choice_4)
                            self.tableWidget.setItem(6, 50,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_choice_list_4)))
                            self.correct_choice_resp_time_4 = time.time()
                            self.tableWidget.setItem(6, 62,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_choice_resp_time_4)))
                            self.correct_A_choice_4 = [float(i) for i in self.correct_cv_choice_list_4]
                            self.correct_stdev_choice_4 = statistics.stdev(self.correct_A_choice_4)
                            self.tableWidget.setItem(6, 48,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_stdev_choice_4)))
                            self.correct_mean_choice_4 = statistics.mean(self.correct_A_choice_4)
                            self.tableWidget.setItem(6, 18,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_mean_choice_4)))
                            self.correct_cv_choice_4 = self.correct_stdev_choice_4 / self.correct_mean_choice_4
                            self.tableWidget.setItem(6, 21,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_choice_4)))
                        except:
                            pass
                    elif 'reward_choice_taken' in str(string):
                        try:
                            self.Reward_Latency_choice_4 = time.time() - self.correct_choice_resp_time_4
                            self.reward_lat_choice_list_4.append(self.Reward_Latency_choice_4)
                            self.tableWidget.setItem(6, 52,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_choice_list_4)))
                            self.reward_A_choice_4 = [float(i) for i in self.reward_lat_choice_list_4]
                            self.reward_lat_choice_mean_4 = statistics.mean(self.reward_A_choice_4)
                            self.tableWidget.setItem(6, 35,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_choice_mean_4)))
                        except:
                            pass
                    elif "incorrect_choice_lit" in str(string):
                        self.incorrect_lit_choice_4 += 1
                        self.tableWidget.setItem(6, 33,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lit_choice_4)))
                    elif 'Incorrect_choice' in str(string):
                        self.Incorrect_choice_4 += 1
                        self.tableWidget.setItem(6, 32,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Incorrect_choice_4)))
                        try:
                            self.incorrect_latency_choice_4 = time.time() - self.choice_start_time_4
                            self.incorrect_choice_list_4.append(self.incorrect_latency_choice_4)
                            self.tableWidget.setItem(6, 54,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_choice_list_4)))
                            self.incorrect_A_choice_4 = [float(i) for i in self.incorrect_choice_list_4]
                            self.incorrect_lat_choice_mean_4 = statistics.mean(self.incorrect_A_choice_4)
                            self.tableWidget.setItem(6, 34,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lat_choice_mean_4)))
                        except:
                            pass
                    elif 'omission_choice' in str(string):
                        self.omission_choice_4 += 1
                        self.tableWidget.setItem(6, 37,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.omission_choice_4)))
                    elif 'Premature_choice_correct' in str(string):
                        self.Premature_choice_correct_4 += 1
                        self.tableWidget.setItem(6, 19,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_correct_4)))
                    elif "delay" in str(string):
                        self.delay_start_time_4 = time.time()
                        self.tableWidget.setItem(6, 64,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.delay_start_time_4)))
                    elif 'Premature_choice_incorrect' in str(string):
                        self.Premature_choice_incorrect_4 += 1
                        self.tableWidget.setItem(6, 43,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_incorrect_4)))
                        try:
                            self.Premature_Response_Latency_choice_4 = time.time() - self.delay_start_time_4
                            self.Premature_latancy_choice_list_4.append(self.Premature_Response_Latency_choice_4)
                            self.tableWidget.setItem(6, 56,
                                                     QtWidgets.QTableWidgetItem(
                                                         str(self.Premature_latancy_choice_list_4)))
                            self.premature_choice_4 = [float(i) for i in self.Premature_latancy_choice_list_4]
                            self.Premature_choice_mean_4 = statistics.mean(self.premature_choice_4)
                            self.tableWidget.setItem(6, 28,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_mean_4)))
                        except:
                            pass
                    elif 'perseverate_choice' in str(string):
                        self.perseverate_choice_4 += 1
                        self.tableWidget.setItem(6, 38,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.perseverate_choice_4)))
                    elif 'attempts_dur_penalty_choice' in str(string):
                        self.resp_timeout_4 += 1
                        self.tableWidget.setItem(6, 40,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.resp_timeout_4)))
                    elif 'receptacle_entries' in str(string):
                        self.Receptacle_entries_4 += 1
                        self.tableWidget.setItem(6, 41,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Receptacle_entries_4)))
                    elif '5_poke_entries' in str(string):
                        self.Nosepokes_5poke_4 += 1
                        self.tableWidget.setItem(6, 42,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Nosepokes_5poke_4)))
                    elif 'SP_reward' in str(string):
                        self.SP_reward_4 = value[2][12:]
                        self.tableWidget.setItem(6, 4,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.SP_reward_4)))
                    elif 'Event Closing' in str(string):
                        self.tableWidget.setItem(6, 0,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.date)))
                    try:
                        self.per_perseverate_sample_4 = (self.perseverate_sample_4 / self.Correct_sample_4) * 100
                        self.tableWidget.setItem(6, 30,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_perseverate_sample_4)))
                        self.per_omission_sample_4 = self.omission_sample_4 / (self.Correct_sample_4
                                                                               + self.Incorrect_sample_4
                                                                               + self.omission_sample_4) * 100
                        self.tableWidget.setItem(6, 9,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_omission_sample_4)))
                        self.per_accuracy_sample_4 = (self.Correct_sample_4 / (self.Correct_sample_4
                                                                               + self.Incorrect_sample_4)) * 100
                        self.tableWidget.setItem(6, 6,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_sample_4)))
                        self.per_correct_sample_4 = (self.Correct_sample_4 / (self.Correct_sample_4
                                                                              + self.Incorrect_sample_4
                                                                              + self.omission_sample_4)) * 100
                        self.tableWidget.setItem(6, 7,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_correct_sample_4)))

                        self.per_premature_sample_4 = self.Premature_sample_4 / (self.Correct_sample_4
                                                                                 + self.Incorrect_sample_4
                                                                                 + self.omission_sample_4) * 100
                        self.tableWidget.setItem(6, 24,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_premature_sample_4)))
                        self.trial_sample_4 = (self.Correct_sample_4 + self.Incorrect_sample_4 + self.omission_sample_4)
                        self.tableWidget.setItem(6, 22,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.trial_sample_4)))
                    except ZeroDivisionError:
                        pass
                    try:
                        self.per_perseverate_choice_4 = (self.perseverate_choice_4 / self.Correct_choice_4) * 100
                        self.tableWidget.setItem(6, 39,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_perseverate_choice_4)))
                        self.per_correct_choice_4 = (self.Correct_choice_4 / (self.Correct_choice_4
                                                                              + self.Incorrect_choice_4
                                                                              + self.incorrect_lit_choice_4
                                                                              + self.omission_choice_4)) * 100
                        self.tableWidget.setItem(6, 15,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_correct_choice_4)))

                        self.per_omission_choice_4 = (self.omission_choice_4 / (self.incorrect_lit_choice_4
                                                                                + self.Correct_choice_4
                                                                                + self.Incorrect_choice_4
                                                                                + self.omission_choice_4)) * 100
                        self.tableWidget.setItem(6, 17,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_omission_choice_4)))
                        self.per_accuracy_choice_4 = (self.Correct_choice_4 / (self.Correct_choice_4
                                                                               + self.incorrect_lit_choice_4
                                                                               + self.Incorrect_choice_4)) * 100
                        self.tableWidget.setItem(6, 14,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_choice_4)))
                        self.per_accuracy_lit_choice_4 = (self.Correct_choice_4 / (self.incorrect_lit_choice_4
                                                                                   + self.Correct_choice_4)) * 100
                        self.tableWidget.setItem(6, 13,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_lit_choice_4)))
                        self.trial_choice_4 = (self.incorrect_lit_choice_4 + self.Correct_choice_4
                                               + self.Incorrect_choice_4 + self.omission_choice_4)
                        self.tableWidget.setItem(6, 20,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.trial_choice_4)))
                    except ZeroDivisionError:
                        pass

    def update_data_table_5(self, new_data_5):
        if new_data_5:
            for value in new_data_5:
                for string in value:
                    self.tableWidget.setItem(7, 0,
                                             QtWidgets.QTableWidgetItem("{:.2f}".format(value[2])))
                    if "sample_phase" in str(string):
                        self.sample_start_time_5 = time.time()
                        self.tableWidget.setItem(7, 58,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.sample_start_time_5)))
                    elif "Correct_sample" in str(string):
                        self.Correct_sample_5 += 1
                        self.tableWidget.setItem(7, 8,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Correct_sample_5)))
                        try:
                            self.correct_latency_sample_5 = time.time() - self.sample_start_time_5
                            self.correct_cv_sample_list_5.append(self.correct_latency_sample_5)
                            self.tableWidget.setItem(7, 49,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_sample_list_5)))
                            self.correct_sample_resp_time_5 = time.time()
                            self.tableWidget.setItem(7, 59,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_sample_resp_time_5)))
                            self.correct_A_sample_5 = [float(i) for i in self.correct_cv_sample_list_5]
                            self.correct_stdev_sample_5 = statistics.stdev(self.correct_A_sample_5)
                            self.tableWidget.setItem(7, 47,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_stdev_sample_5)))
                            self.correct_mean_sample_5 = statistics.mean(self.correct_A_sample_5)
                            self.tableWidget.setItem(7, 11,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_mean_sample_5)))
                            self.correct_cv_sample_5 = self.correct_stdev_sample_5 / self.correct_mean_sample_5
                            self.tableWidget.setItem(7, 12,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_sample_5)))
                        except:
                            pass
                    elif 'Incorrect_sample' in str(string):
                        self.Incorrect_sample_5 += 1
                        self.tableWidget.setItem(7, 26,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Incorrect_sample_5)))
                        try:
                            self.incorrect_latency_sample_5 = time.time() - self.sample_start_time_5
                            self.incorrect_cv_sample_list_5.append(self.incorrect_latency_sample_5)
                            self.tableWidget.setItem(7, 53,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_cv_sample_list_5)))
                            self.incorrect_A_sample_5 = [float(i) for i in self.incorrect_cv_sample_list_5]
                            self.incorrect_lat_sample_mean_5 = statistics.mean(self.incorrect_A_sample_5)
                            self.tableWidget.setItem(7, 27,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lat_sample_mean_5)))
                        except:
                            pass
                    elif 'omission_sample' in str(string):
                        self.omission_sample_5 += 1
                        self.tableWidget.setItem(7, 25,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.omission_sample_5)))
                    elif 'reward_sample_taken' in str(string):
                        try:
                            self.Reward_Latency_sample_5 = time.time() - self.correct_sample_resp_time_5
                            self.reward_lat_sample_list_5.append(self.Reward_Latency_sample_5)
                            self.tableWidget.setItem(7, 51,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_sample_list_5)))
                            self.reward_A_sample_5 = [float(i) for i in self.reward_lat_sample_list_5]
                            self.reward_lat_sample_mean_5 = statistics.mean(self.reward_A_sample_5)
                            self.tableWidget.setItem(7, 10,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_sample_mean_5)))
                        except:
                            pass
                    elif "iti_sample" in str(string):
                        self.iti_start_time_5 = time.time()
                        self.tableWidget.setItem(7, 60,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.iti_start_time_5)))
                    elif 'Premature_response' in str(string):
                        self.Premature_sample_5 += 1
                        self.tableWidget.setItem(7, 23,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_sample_5)))
                        try:
                            self.Premature_Response_Latency_sample_5 = time.time() - self.iti_start_time_5
                            self.Premature_latancy_sample_list_5.append(self.Premature_Response_Latency_sample_5)
                            self.tableWidget.setItem(7, 56,
                                                     QtWidgets.QTableWidgetItem(
                                                         str(self.Premature_latancy_sample_list_5)))
                            self.premature_sample_5 = [float(i) for i in self.Premature_latancy_sample_list_5]
                            self.Premature_sample_mean_5 = statistics.mean(self.premature_sample_5)
                            self.tableWidget.setItem(7, 28,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_sample_mean_5)))
                        except:
                            pass
                    elif 'perseverate_sample' in str(string):
                        self.perseverate_sample_5 += 1
                        self.tableWidget.setItem(7, 29,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.perseverate_sample_5)))
                    elif 'attempts_dur_penalty_sample' in str(string):
                        self.resp_timeout_5 += 1
                        self.tableWidget.setItem(7, 31,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.resp_timeout_5)))
                    elif "choice_phase" in str(string):
                        self.choice_start_time_5 = time.time()
                        self.tableWidget.setItem(7, 61,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.choice_start_time_5)))
                    elif "Correct_choice" in str(string):
                        self.Correct_choice_5 += 1
                        self.tableWidget.setItem(7, 16,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Correct_choice_5)))
                        try:
                            self.correct_latency_choice_5 = time.time() - self.choice_start_time_5
                            self.correct_cv_choice_list_5.append(self.correct_latency_choice_5)
                            self.tableWidget.setItem(7, 50,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_choice_list_5)))
                            self.correct_choice_resp_time_5 = time.time()
                            self.tableWidget.setItem(7, 62,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_choice_resp_time_5)))
                            self.correct_A_choice_5 = [float(i) for i in self.correct_cv_choice_list_5]
                            self.correct_stdev_choice_5 = statistics.stdev(self.correct_A_choice_5)
                            self.tableWidget.setItem(7, 48,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_stdev_choice_5)))
                            self.correct_mean_choice_5 = statistics.mean(self.correct_A_choice_5)
                            self.tableWidget.setItem(7, 18,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_mean_choice_5)))
                            self.correct_cv_choice_5 = self.correct_stdev_choice_5 / self.correct_mean_choice_5
                            self.tableWidget.setItem(7, 21,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_choice_5)))
                        except:
                            pass
                    elif 'reward_choice_taken' in str(string):
                        try:
                            self.Reward_Latency_choice_5 = time.time() - self.correct_choice_resp_time_5
                            self.reward_lat_choice_list_5.append(self.Reward_Latency_choice_5)
                            self.tableWidget.setItem(7, 52,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_choice_list_5)))
                            self.reward_A_choice_5 = [float(i) for i in self.reward_lat_choice_list_5]
                            self.reward_lat_choice_mean_5 = statistics.mean(self.reward_A_choice_5)
                            self.tableWidget.setItem(7, 35,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_choice_mean_5)))
                        except:
                            pass
                    elif "incorrect_choice_lit" in str(string):
                        self.incorrect_lit_choice_5 += 1
                        self.tableWidget.setItem(7, 33,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lit_choice_5)))
                    elif 'Incorrect_choice' in str(string):
                        self.Incorrect_choice_5 += 1
                        self.tableWidget.setItem(7, 32,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Incorrect_choice_5)))
                        try:
                            self.incorrect_latency_choice_5 = time.time() - self.choice_start_time_5
                            self.incorrect_choice_list_5.append(self.incorrect_latency_choice_5)
                            self.tableWidget.setItem(7, 54,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_choice_list_5)))
                            self.incorrect_A_choice_5 = [float(i) for i in self.incorrect_choice_list_5]
                            self.incorrect_lat_choice_mean_5 = statistics.mean(self.incorrect_A_choice_5)
                            self.tableWidget.setItem(7, 34,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lat_choice_mean_5)))
                        except:
                            pass
                    elif 'omission_choice' in str(string):
                        self.omission_choice_5 += 1
                        self.tableWidget.setItem(7, 37,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.omission_choice_5)))
                    elif 'Premature_choice_correct' in str(string):
                        self.Premature_choice_correct_5 += 1
                        self.tableWidget.setItem(7, 19,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_correct_5)))
                    elif "delay" in str(string):
                        self.delay_start_time_5 = time.time()
                        self.tableWidget.setItem(7, 64,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.delay_start_time_5)))
                    elif 'Premature_choice_incorrect' in str(string):
                        self.Premature_choice_incorrect_5 += 1
                        self.tableWidget.setItem(7, 43,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_incorrect_5)))
                        try:
                            self.Premature_Response_Latency_choice_5 = time.time() - self.delay_start_time_5
                            self.Premature_latancy_choice_list_5.append(self.Premature_Response_Latency_choice_5)
                            self.tableWidget.setItem(7, 56,
                                                     QtWidgets.QTableWidgetItem(
                                                         str(self.Premature_latancy_choice_list_5)))
                            self.premature_choice_5 = [float(i) for i in self.Premature_latancy_choice_list_5]
                            self.Premature_choice_mean_5 = statistics.mean(self.premature_choice_5)
                            self.tableWidget.setItem(7, 28,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_mean_5)))
                        except:
                            pass
                    elif 'perseverate_choice' in str(string):
                        self.perseverate_choice_5 += 1
                        self.tableWidget.setItem(7, 38,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.perseverate_choice_5)))
                    elif 'attempts_dur_penalty_choice' in str(string):
                        self.resp_timeout_5 += 1
                        self.tableWidget.setItem(7, 40,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.resp_timeout_5)))
                    elif 'receptacle_entries' in str(string):
                        self.Receptacle_entries_5 += 1
                        self.tableWidget.setItem(7, 41,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Receptacle_entries_5)))
                    elif '5_poke_entries' in str(string):
                        self.Nosepokes_5poke_5 += 1
                        self.tableWidget.setItem(7, 42,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Nosepokes_5poke_5)))
                    elif 'SP_reward' in str(string):
                        self.SP_reward_5 = value[2][12:]
                        self.tableWidget.setItem(7, 4,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.SP_reward_5)))
                    elif 'Event Closing' in str(string):
                        self.tableWidget.setItem(7, 0,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.date)))
                    try:
                        self.per_perseverate_sample_5 = (self.perseverate_sample_5 / self.Correct_sample_5) * 100
                        self.tableWidget.setItem(7, 30,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_perseverate_sample_5)))
                        self.per_omission_sample_5 = self.omission_sample_5 / (self.Correct_sample_5
                                                                               + self.Incorrect_sample_5
                                                                               + self.omission_sample_5) * 100
                        self.tableWidget.setItem(7, 9,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_omission_sample_5)))
                        self.per_accuracy_sample_5 = (self.Correct_sample_5 / (self.Correct_sample_5
                                                                               + self.Incorrect_sample_5)) * 100
                        self.tableWidget.setItem(7, 6,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_sample_5)))
                        self.per_correct_sample_5 = (self.Correct_sample_5 / (self.Correct_sample_5
                                                                              + self.Incorrect_sample_5
                                                                              + self.omission_sample_5)) * 100
                        self.tableWidget.setItem(7, 7,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_correct_sample_5)))

                        self.per_premature_sample_5 = self.Premature_sample_5 / (self.Correct_sample_5
                                                                                 + self.Incorrect_sample_5
                                                                                 + self.omission_sample_5) * 100
                        self.tableWidget.setItem(7, 24,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_premature_sample_5)))
                        self.trial_sample_5 = (self.Correct_sample_5 + self.Incorrect_sample_5 + self.omission_sample_5)
                        self.tableWidget.setItem(7, 22,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.trial_sample_5)))
                    except ZeroDivisionError:
                        pass
                    try:
                        self.per_perseverate_choice_5 = (self.perseverate_choice_5 / self.Correct_choice_5) * 100
                        self.tableWidget.setItem(7, 39,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_perseverate_choice_5)))
                        self.per_correct_choice_5 = (self.Correct_choice_5 / (self.Correct_choice_5
                                                                              + self.Incorrect_choice_5
                                                                              + self.incorrect_lit_choice_5
                                                                              + self.omission_choice_5)) * 100
                        self.tableWidget.setItem(7, 15,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_correct_choice_5)))

                        self.per_omission_choice_5 = (self.omission_choice_5 / (self.incorrect_lit_choice_5
                                                                                + self.Correct_choice_5
                                                                                + self.Incorrect_choice_5
                                                                                + self.omission_choice_5)) * 100
                        self.tableWidget.setItem(7, 17,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_omission_choice_5)))
                        self.per_accuracy_choice_5 = (self.Correct_choice_5 / (self.Correct_choice_5
                                                                               + self.incorrect_lit_choice_5
                                                                               + self.Incorrect_choice_5)) * 100
                        self.tableWidget.setItem(7, 14,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_choice_5)))
                        self.per_accuracy_lit_choice_5 = (self.Correct_choice_5 / (self.incorrect_lit_choice_5
                                                                                   + self.Correct_choice_5)) * 100
                        self.tableWidget.setItem(7, 13,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_lit_choice_5)))
                        self.trial_choice_5 = (self.incorrect_lit_choice_5 + self.Correct_choice_5
                                               + self.Incorrect_choice_5 + self.omission_choice_5)
                        self.tableWidget.setItem(7, 20,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.trial_choice_5)))
                    except ZeroDivisionError:
                        pass

    def update_data_table_6(self, new_data_6):
        if new_data_6:
            for value in new_data_6:
                for string in value:
                    self.tableWidget.setItem(8, 0,
                                             QtWidgets.QTableWidgetItem("{:.2f}".format(value[2])))
                    if "sample_phase" in str(string):
                        self.sample_start_time_6 = time.time()
                        self.tableWidget.setItem(8, 58,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.sample_start_time_6)))
                    elif "Correct_sample" in str(string):
                        self.Correct_sample_6 += 1
                        self.tableWidget.setItem(8, 8,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Correct_sample_6)))
                        try:
                            self.correct_latency_sample_6 = time.time() - self.sample_start_time_6
                            self.correct_cv_sample_list_6.append(self.correct_latency_sample_6)
                            self.tableWidget.setItem(8, 49,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_sample_list_6)))
                            self.correct_sample_resp_time_6 = time.time()
                            self.tableWidget.setItem(8, 59,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_sample_resp_time_6)))
                            self.correct_A_sample_6 = [float(i) for i in self.correct_cv_sample_list_6]
                            self.correct_stdev_sample_6 = statistics.stdev(self.correct_A_sample_6)
                            self.tableWidget.setItem(8, 47,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_stdev_sample_6)))
                            self.correct_mean_sample_6 = statistics.mean(self.correct_A_sample_6)
                            self.tableWidget.setItem(8, 11,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_mean_sample_6)))
                            self.correct_cv_sample_6 = self.correct_stdev_sample_6 / self.correct_mean_sample_6
                            self.tableWidget.setItem(8, 12,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_sample_6)))
                        except:
                            pass
                    elif 'Incorrect_sample' in str(string):
                        self.Incorrect_sample_6 += 1
                        self.tableWidget.setItem(8, 26,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Incorrect_sample_6)))
                        try:
                            self.incorrect_latency_sample_6 = time.time() - self.sample_start_time_6
                            self.incorrect_cv_sample_list_6.append(self.incorrect_latency_sample_6)
                            self.tableWidget.setItem(8, 53,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_cv_sample_list_6)))
                            self.incorrect_A_sample_6 = [float(i) for i in self.incorrect_cv_sample_list_6]
                            self.incorrect_lat_sample_mean_6 = statistics.mean(self.incorrect_A_sample_6)
                            self.tableWidget.setItem(8, 27,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lat_sample_mean_6)))
                        except:
                            pass
                    elif 'omission_sample' in str(string):
                        self.omission_sample_6 += 1
                        self.tableWidget.setItem(8, 25,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.omission_sample_6)))
                    elif 'reward_sample_taken' in str(string):
                        try:
                            self.Reward_Latency_sample_6 = time.time() - self.correct_sample_resp_time_6
                            self.reward_lat_sample_list_6.append(self.Reward_Latency_sample_6)
                            self.tableWidget.setItem(8, 51,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_sample_list_6)))
                            self.reward_A_sample_6 = [float(i) for i in self.reward_lat_sample_list_6]
                            self.reward_lat_sample_mean_6 = statistics.mean(self.reward_A_sample_6)
                            self.tableWidget.setItem(8, 10,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_sample_mean_6)))
                        except:
                            pass
                    elif "iti_sample" in str(string):
                        self.iti_start_time_6 = time.time()
                        self.tableWidget.setItem(8, 60,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.iti_start_time_6)))
                    elif 'Premature_response' in str(string):
                        self.Premature_sample_6 += 1
                        self.tableWidget.setItem(8, 23,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_sample_6)))
                        try:
                            self.Premature_Response_Latency_sample_6 = time.time() - self.iti_start_time_6
                            self.Premature_latancy_sample_list_6.append(self.Premature_Response_Latency_sample_6)
                            self.tableWidget.setItem(8, 56,
                                                     QtWidgets.QTableWidgetItem(
                                                         str(self.Premature_latancy_sample_list_6)))
                            self.premature_sample_6 = [float(i) for i in self.Premature_latancy_sample_list_6]
                            self.Premature_sample_mean_6 = statistics.mean(self.premature_sample_6)
                            self.tableWidget.setItem(8, 28,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_sample_mean_6)))
                        except:
                            pass
                    elif 'perseverate_sample' in str(string):
                        self.perseverate_sample_6 += 1
                        self.tableWidget.setItem(8, 29,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.perseverate_sample_6)))
                    elif 'attempts_dur_penalty_sample' in str(string):
                        self.resp_timeout_6 += 1
                        self.tableWidget.setItem(8, 31,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.resp_timeout_6)))
                    elif "choice_phase" in str(string):
                        self.choice_start_time_6 = time.time()
                        self.tableWidget.setItem(8, 61,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.choice_start_time_6)))
                    elif "Correct_choice" in str(string):
                        self.Correct_choice_6 += 1
                        self.tableWidget.setItem(8, 16,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Correct_choice_6)))
                        try:
                            self.correct_latency_choice_6 = time.time() - self.choice_start_time_6
                            self.correct_cv_choice_list_6.append(self.correct_latency_choice_6)
                            self.tableWidget.setItem(8, 50,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_choice_list_6)))
                            self.correct_choice_resp_time_6 = time.time()
                            self.tableWidget.setItem(8, 62,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_choice_resp_time_6)))
                            self.correct_A_choice_6 = [float(i) for i in self.correct_cv_choice_list_6]
                            self.correct_stdev_choice_6 = statistics.stdev(self.correct_A_choice_6)
                            self.tableWidget.setItem(8, 48,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_stdev_choice_6)))
                            self.correct_mean_choice_6 = statistics.mean(self.correct_A_choice_6)
                            self.tableWidget.setItem(8, 18,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_mean_choice_6)))
                            self.correct_cv_choice_6 = self.correct_stdev_choice_6 / self.correct_mean_choice_6
                            self.tableWidget.setItem(8, 21,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_choice_6)))
                        except:
                            pass
                    elif 'reward_choice_taken' in str(string):
                        try:
                            self.Reward_Latency_choice_6 = time.time() - self.correct_choice_resp_time_6
                            self.reward_lat_choice_list_6.append(self.Reward_Latency_choice_6)
                            self.tableWidget.setItem(8, 52,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_choice_list_6)))
                            self.reward_A_choice_6 = [float(i) for i in self.reward_lat_choice_list_6]
                            self.reward_lat_choice_mean_6 = statistics.mean(self.reward_A_choice_6)
                            self.tableWidget.setItem(8, 35,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_choice_mean_6)))
                        except:
                            pass
                    elif "incorrect_choice_lit" in str(string):
                        self.incorrect_lit_choice_6 += 1
                        self.tableWidget.setItem(8, 33,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lit_choice_6)))
                    elif 'Incorrect_choice' in str(string):
                        self.Incorrect_choice_6 += 1
                        self.tableWidget.setItem(8, 32,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Incorrect_choice_6)))
                        try:
                            self.incorrect_latency_choice_6 = time.time() - self.choice_start_time_6
                            self.incorrect_choice_list_6.append(self.incorrect_latency_choice_6)
                            self.tableWidget.setItem(8, 54,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_choice_list_6)))
                            self.incorrect_A_choice_6 = [float(i) for i in self.incorrect_choice_list_6]
                            self.incorrect_lat_choice_mean_6 = statistics.mean(self.incorrect_A_choice_6)
                            self.tableWidget.setItem(8, 34,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lat_choice_mean_6)))
                        except:
                            pass
                    elif 'omission_choice' in str(string):
                        self.omission_choice_6 += 1
                        self.tableWidget.setItem(8, 37,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.omission_choice_6)))
                    elif 'Premature_choice_correct' in str(string):
                        self.Premature_choice_correct_6 += 1
                        self.tableWidget.setItem(8, 19,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_correct_6)))
                    elif "delay" in str(string):
                        self.delay_start_time_6 = time.time()
                        self.tableWidget.setItem(8, 64,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.delay_start_time_6)))
                    elif 'Premature_choice_incorrect' in str(string):
                        self.Premature_choice_incorrect_6 += 1
                        self.tableWidget.setItem(8, 43,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_incorrect_6)))
                        try:
                            self.Premature_Response_Latency_choice_6 = time.time() - self.delay_start_time_6
                            self.Premature_latancy_choice_list_6.append(self.Premature_Response_Latency_choice_6)
                            self.tableWidget.setItem(8, 56,
                                                     QtWidgets.QTableWidgetItem(
                                                         str(self.Premature_latancy_choice_list_6)))
                            self.premature_choice_6 = [float(i) for i in self.Premature_latancy_choice_list_6]
                            self.Premature_choice_mean_6 = statistics.mean(self.premature_choice_6)
                            self.tableWidget.setItem(8, 28,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_mean_6)))
                        except:
                            pass
                    elif 'perseverate_choice' in str(string):
                        self.perseverate_choice_6 += 1
                        self.tableWidget.setItem(8, 38,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.perseverate_choice_6)))
                    elif 'attempts_dur_penalty_choice' in str(string):
                        self.resp_timeout_6 += 1
                        self.tableWidget.setItem(8, 40,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.resp_timeout_6)))
                    elif 'receptacle_entries' in str(string):
                        self.Receptacle_entries_6 += 1
                        self.tableWidget.setItem(8, 41,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Receptacle_entries_6)))
                    elif '5_poke_entries' in str(string):
                        self.Nosepokes_5poke_6 += 1
                        self.tableWidget.setItem(8, 42,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Nosepokes_5poke_6)))
                    elif 'SP_reward' in str(string):
                        self.SP_reward_6 = value[2][12:]
                        self.tableWidget.setItem(8, 4,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.SP_reward_6)))
                    elif 'Event Closing' in str(string):
                        self.tableWidget.setItem(8, 0,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.date)))
                    try:
                        self.per_perseverate_sample_6 = (self.perseverate_sample_6 / self.Correct_sample_6) * 100
                        self.tableWidget.setItem(8, 30,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_perseverate_sample_6)))
                        self.per_omission_sample_6 = self.omission_sample_6 / (self.Correct_sample_6
                                                                               + self.Incorrect_sample_6
                                                                               + self.omission_sample_6) * 100
                        self.tableWidget.setItem(8, 9,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_omission_sample_6)))
                        self.per_accuracy_sample_6 = (self.Correct_sample_6 / (self.Correct_sample_6
                                                                               + self.Incorrect_sample_6)) * 100
                        self.tableWidget.setItem(8, 6,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_sample_6)))
                        self.per_correct_sample_6 = (self.Correct_sample_6 / (self.Correct_sample_6
                                                                              + self.Incorrect_sample_6
                                                                              + self.omission_sample_6)) * 100
                        self.tableWidget.setItem(8, 7,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_correct_sample_6)))

                        self.per_premature_sample_6 = self.Premature_sample_6 / (self.Correct_sample_6
                                                                                 + self.Incorrect_sample_6
                                                                                 + self.omission_sample_6) * 100
                        self.tableWidget.setItem(8, 24,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_premature_sample_6)))
                        self.trial_sample_6 = (self.Correct_sample_6 + self.Incorrect_sample_6 + self.omission_sample_6)
                        self.tableWidget.setItem(8, 22,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.trial_sample_6)))
                    except ZeroDivisionError:
                        pass
                    try:
                        self.per_perseverate_choice_6 = (self.perseverate_choice_6 / self.Correct_choice_6) * 100
                        self.tableWidget.setItem(8, 39,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_perseverate_choice_6)))
                        self.per_correct_choice_6 = (self.Correct_choice_6 / (self.Correct_choice_6
                                                                              + self.Incorrect_choice_6
                                                                              + self.incorrect_lit_choice_6
                                                                              + self.omission_choice_6)) * 100
                        self.tableWidget.setItem(8, 15,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_correct_choice_6)))

                        self.per_omission_choice_6 = (self.omission_choice_6 / (self.incorrect_lit_choice_6
                                                                                + self.Correct_choice_6
                                                                                + self.Incorrect_choice_6
                                                                                + self.omission_choice_6)) * 100
                        self.tableWidget.setItem(8, 17,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_omission_choice_6)))
                        self.per_accuracy_choice_6 = (self.Correct_choice_6 / (self.Correct_choice_6
                                                                               + self.incorrect_lit_choice_6
                                                                               + self.Incorrect_choice_6)) * 100
                        self.tableWidget.setItem(8, 14,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_choice_6)))
                        self.per_accuracy_lit_choice_6 = (self.Correct_choice_6 / (self.incorrect_lit_choice_6
                                                                                   + self.Correct_choice_6)) * 100
                        self.tableWidget.setItem(8, 13,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_lit_choice_6)))
                        self.trial_choice_6 = (self.incorrect_lit_choice_6 + self.Correct_choice_6
                                               + self.Incorrect_choice_6 + self.omission_choice_6)
                        self.tableWidget.setItem(8, 20,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.trial_choice_6)))
                    except ZeroDivisionError:
                        pass

    def update_data_table_7(self, new_data_7):
        if new_data_7:
            for value in new_data_7:
                for string in value:
                    self.tableWidget.setItem(9, 0,
                                             QtWidgets.QTableWidgetItem("{:.2f}".format(value[2])))
                    if "sample_phase" in str(string):
                        self.sample_start_time_7 = time.time()
                        self.tableWidget.setItem(9, 58,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.sample_start_time_7)))
                    elif "Correct_sample" in str(string):
                        self.Correct_sample_7 += 1
                        self.tableWidget.setItem(9, 8,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Correct_sample_7)))
                        try:
                            self.correct_latency_sample_7 = time.time() - self.sample_start_time_7
                            self.correct_cv_sample_list_7.append(self.correct_latency_sample_7)
                            self.tableWidget.setItem(9, 49,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_sample_list_7)))
                            self.correct_sample_resp_time_7 = time.time()
                            self.tableWidget.setItem(9, 59,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_sample_resp_time_7)))
                            self.correct_A_sample_7 = [float(i) for i in self.correct_cv_sample_list_7]
                            self.correct_stdev_sample_7 = statistics.stdev(self.correct_A_sample_7)
                            self.tableWidget.setItem(9, 47,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_stdev_sample_7)))
                            self.correct_mean_sample_7 = statistics.mean(self.correct_A_sample_7)
                            self.tableWidget.setItem(9, 11,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_mean_sample_7)))
                            self.correct_cv_sample_7 = self.correct_stdev_sample_7 / self.correct_mean_sample_7
                            self.tableWidget.setItem(9, 12,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_sample_7)))
                        except:
                            pass
                    elif 'Incorrect_sample' in str(string):
                        self.Incorrect_sample_7 += 1
                        self.tableWidget.setItem(9, 26,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Incorrect_sample_7)))
                        try:
                            self.incorrect_latency_sample_7 = time.time() - self.sample_start_time_7
                            self.incorrect_cv_sample_list_7.append(self.incorrect_latency_sample_7)
                            self.tableWidget.setItem(9, 53,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_cv_sample_list_7)))
                            self.incorrect_A_sample_7 = [float(i) for i in self.incorrect_cv_sample_list_7]
                            self.incorrect_lat_sample_mean_7 = statistics.mean(self.incorrect_A_sample_7)
                            self.tableWidget.setItem(9, 27,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lat_sample_mean_7)))
                        except:
                            pass
                    elif 'omission_sample' in str(string):
                        self.omission_sample_7 += 1
                        self.tableWidget.setItem(9, 25,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.omission_sample_7)))
                    elif 'reward_sample_taken' in str(string):
                        try:
                            self.Reward_Latency_sample_7 = time.time() - self.correct_sample_resp_time_7
                            self.reward_lat_sample_list_7.append(self.Reward_Latency_sample_7)
                            self.tableWidget.setItem(9, 51,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_sample_list_7)))
                            self.reward_A_sample_7 = [float(i) for i in self.reward_lat_sample_list_7]
                            self.reward_lat_sample_mean_7 = statistics.mean(self.reward_A_sample_7)
                            self.tableWidget.setItem(9, 10,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_sample_mean_7)))
                        except:
                            pass
                    elif "iti_sample" in str(string):
                        self.iti_start_time_7 = time.time()
                        self.tableWidget.setItem(9, 60,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.iti_start_time_7)))
                    elif 'Premature_response' in str(string):
                        self.Premature_sample_7 += 1
                        self.tableWidget.setItem(9, 23,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_sample_7)))
                        try:
                            self.Premature_Response_Latency_sample_7 = time.time() - self.iti_start_time_7
                            self.Premature_latancy_sample_list_7.append(self.Premature_Response_Latency_sample_7)
                            self.tableWidget.setItem(9, 56,
                                                     QtWidgets.QTableWidgetItem(
                                                         str(self.Premature_latancy_sample_list_7)))
                            self.premature_sample_7 = [float(i) for i in self.Premature_latancy_sample_list_7]
                            self.Premature_sample_mean_7 = statistics.mean(self.premature_sample_7)
                            self.tableWidget.setItem(9, 28,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_sample_mean_7)))
                        except:
                            pass
                    elif 'perseverate_sample' in str(string):
                        self.perseverate_sample_7 += 1
                        self.tableWidget.setItem(9, 29,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.perseverate_sample_7)))
                    elif 'attempts_dur_penalty_sample' in str(string):
                        self.resp_timeout_7 += 1
                        self.tableWidget.setItem(9, 31,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.resp_timeout_7)))
                    elif "choice_phase" in str(string):
                        self.choice_start_time_7 = time.time()
                        self.tableWidget.setItem(9, 61,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.choice_start_time_7)))
                    elif "Correct_choice" in str(string):
                        self.Correct_choice_7 += 1
                        self.tableWidget.setItem(9, 16,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Correct_choice_7)))
                        try:
                            self.correct_latency_choice_7 = time.time() - self.choice_start_time_7
                            self.correct_cv_choice_list_7.append(self.correct_latency_choice_7)
                            self.tableWidget.setItem(9, 50,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_choice_list_7)))
                            self.correct_choice_resp_time_7 = time.time()
                            self.tableWidget.setItem(9, 62,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_choice_resp_time_7)))
                            self.correct_A_choice_7 = [float(i) for i in self.correct_cv_choice_list_7]
                            self.correct_stdev_choice_7 = statistics.stdev(self.correct_A_choice_7)
                            self.tableWidget.setItem(9, 48,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_stdev_choice_7)))
                            self.correct_mean_choice_7 = statistics.mean(self.correct_A_choice_7)
                            self.tableWidget.setItem(9, 18,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_mean_choice_7)))
                            self.correct_cv_choice_7 = self.correct_stdev_choice_7 / self.correct_mean_choice_7
                            self.tableWidget.setItem(9, 21,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_choice_7)))
                        except:
                            pass
                    elif 'reward_choice_taken' in str(string):
                        try:
                            self.Reward_Latency_choice_7 = time.time() - self.correct_choice_resp_time_7
                            self.reward_lat_choice_list_7.append(self.Reward_Latency_choice_7)
                            self.tableWidget.setItem(9, 52,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_choice_list_7)))
                            self.reward_A_choice_7 = [float(i) for i in self.reward_lat_choice_list_7]
                            self.reward_lat_choice_mean_7 = statistics.mean(self.reward_A_choice_7)
                            self.tableWidget.setItem(9, 35,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_choice_mean_7)))
                        except:
                            pass
                    elif "incorrect_choice_lit" in str(string):
                        self.incorrect_lit_choice_7 += 1
                        self.tableWidget.setItem(9, 33,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lit_choice_7)))
                    elif 'Incorrect_choice' in str(string):
                        self.Incorrect_choice_7 += 1
                        self.tableWidget.setItem(9, 32,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Incorrect_choice_7)))
                        try:
                            self.incorrect_latency_choice_7 = time.time() - self.choice_start_time_7
                            self.incorrect_choice_list_7.append(self.incorrect_latency_choice_7)
                            self.tableWidget.setItem(9, 54,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_choice_list_7)))
                            self.incorrect_A_choice_7 = [float(i) for i in self.incorrect_choice_list_7]
                            self.incorrect_lat_choice_mean_7 = statistics.mean(self.incorrect_A_choice_7)
                            self.tableWidget.setItem(9, 34,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lat_choice_mean_7)))
                        except:
                            pass
                    elif 'omission_choice' in str(string):
                        self.omission_choice_7 += 1
                        self.tableWidget.setItem(9, 37,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.omission_choice_7)))
                    elif 'Premature_choice_correct' in str(string):
                        self.Premature_choice_correct_7 += 1
                        self.tableWidget.setItem(9, 19,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_correct_7)))
                    elif "delay" in str(string):
                        self.delay_start_time_7 = time.time()
                        self.tableWidget.setItem(9, 64,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.delay_start_time_7)))
                    elif 'Premature_choice_incorrect' in str(string):
                        self.Premature_choice_incorrect_7 += 1
                        self.tableWidget.setItem(9, 43,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_incorrect_7)))
                        try:
                            self.Premature_Response_Latency_choice_7 = time.time() - self.delay_start_time_7
                            self.Premature_latancy_choice_list_7.append(self.Premature_Response_Latency_choice_7)
                            self.tableWidget.setItem(9, 56,
                                                     QtWidgets.QTableWidgetItem(
                                                         str(self.Premature_latancy_choice_list_7)))
                            self.premature_choice_7 = [float(i) for i in self.Premature_latancy_choice_list_7]
                            self.Premature_choice_mean_7 = statistics.mean(self.premature_choice_7)
                            self.tableWidget.setItem(9, 28,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_mean_7)))
                        except:
                            pass
                    elif 'perseverate_choice' in str(string):
                        self.perseverate_choice_7 += 1
                        self.tableWidget.setItem(9, 38,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.perseverate_choice_7)))
                    elif 'attempts_dur_penalty_choice' in str(string):
                        self.resp_timeout_7 += 1
                        self.tableWidget.setItem(9, 40,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.resp_timeout_7)))
                    elif 'receptacle_entries' in str(string):
                        self.Receptacle_entries_7 += 1
                        self.tableWidget.setItem(9, 41,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Receptacle_entries_7)))
                    elif '5_poke_entries' in str(string):
                        self.Nosepokes_5poke_7 += 1
                        self.tableWidget.setItem(9, 42,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Nosepokes_5poke_7)))
                    elif 'SP_reward' in str(string):
                        self.SP_reward_7 = value[2][12:]
                        self.tableWidget.setItem(9, 4,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.SP_reward_7)))
                    elif 'Event Closing' in str(string):
                        self.tableWidget.setItem(9, 0,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.date)))
                    try:
                        self.per_perseverate_sample_7 = (self.perseverate_sample_7 / self.Correct_sample_7) * 100
                        self.tableWidget.setItem(9, 30,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_perseverate_sample_7)))
                        self.per_omission_sample_7 = self.omission_sample_7 / (self.Correct_sample_7
                                                                               + self.Incorrect_sample_7
                                                                               + self.omission_sample_7) * 100
                        self.tableWidget.setItem(9, 9,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_omission_sample_7)))
                        self.per_accuracy_sample_7 = (self.Correct_sample_7 / (self.Correct_sample_7
                                                                               + self.Incorrect_sample_7)) * 100
                        self.tableWidget.setItem(9, 6,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_sample_7)))
                        self.per_correct_sample_7 = (self.Correct_sample_7 / (self.Correct_sample_7
                                                                              + self.Incorrect_sample_7
                                                                              + self.omission_sample_7)) * 100
                        self.tableWidget.setItem(9, 7,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_correct_sample_7)))

                        self.per_premature_sample_7 = self.Premature_sample_7 / (self.Correct_sample_7
                                                                                 + self.Incorrect_sample_7
                                                                                 + self.omission_sample_7) * 100
                        self.tableWidget.setItem(9, 24,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_premature_sample_7)))
                        self.trial_sample_7 = (self.Correct_sample_7 + self.Incorrect_sample_7 + self.omission_sample_7)
                        self.tableWidget.setItem(9, 22,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.trial_sample_7)))
                    except ZeroDivisionError:
                        pass
                    try:
                        self.per_perseverate_choice_7 = (self.perseverate_choice_7 / self.Correct_choice_7) * 100
                        self.tableWidget.setItem(9, 39,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_perseverate_choice_7)))
                        self.per_correct_choice_7 = (self.Correct_choice_7 / (self.Correct_choice_7
                                                                              + self.Incorrect_choice_7
                                                                              + self.incorrect_lit_choice_7
                                                                              + self.omission_choice_7)) * 100
                        self.tableWidget.setItem(9, 15,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_correct_choice_7)))

                        self.per_omission_choice_7 = (self.omission_choice_7 / (self.incorrect_lit_choice_7
                                                                                + self.Correct_choice_7
                                                                                + self.Incorrect_choice_7
                                                                                + self.omission_choice_7)) * 100
                        self.tableWidget.setItem(9, 17,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_omission_choice_7)))
                        self.per_accuracy_choice_7 = (self.Correct_choice_7 / (self.Correct_choice_7
                                                                               + self.incorrect_lit_choice_7
                                                                               + self.Incorrect_choice_7)) * 100
                        self.tableWidget.setItem(9, 14,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_choice_7)))
                        self.per_accuracy_lit_choice_7 = (self.Correct_choice_7 / (self.incorrect_lit_choice_7
                                                                                   + self.Correct_choice_7)) * 100
                        self.tableWidget.setItem(9, 13,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_lit_choice_7)))
                        self.trial_choice_7 = (self.incorrect_lit_choice_7 + self.Correct_choice_7
                                               + self.Incorrect_choice_7 + self.omission_choice_7)
                        self.tableWidget.setItem(9, 20,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.trial_choice_7)))
                    except ZeroDivisionError:
                        pass

    def update_data_table_8(self, new_data_8):
        if new_data_8:
            for value in new_data_8:
                for string in value:
                    self.tableWidget.setItem(10, 0,
                                             QtWidgets.QTableWidgetItem("{:.2f}".format(value[2])))
                    if "sample_phase" in str(string):
                        self.sample_start_time_8 = time.time()
                        self.tableWidget.setItem(10, 58,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.sample_start_time_8)))
                    elif "Correct_sample" in str(string):
                        self.Correct_sample_8 += 1
                        self.tableWidget.setItem(10, 8,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Correct_sample_8)))
                        try:
                            self.correct_latency_sample_8 = time.time() - self.sample_start_time_8
                            self.correct_cv_sample_list_8.append(self.correct_latency_sample_8)
                            self.tableWidget.setItem(10, 49,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_sample_list_8)))
                            self.correct_sample_resp_time_8 = time.time()
                            self.tableWidget.setItem(10, 59,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_sample_resp_time_8)))
                            self.correct_A_sample_8 = [float(i) for i in self.correct_cv_sample_list_8]
                            self.correct_stdev_sample_8 = statistics.stdev(self.correct_A_sample_8)
                            self.tableWidget.setItem(10, 47,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_stdev_sample_8)))
                            self.correct_mean_sample_8 = statistics.mean(self.correct_A_sample_8)
                            self.tableWidget.setItem(10, 11,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_mean_sample_8)))
                            self.correct_cv_sample_8 = self.correct_stdev_sample_8 / self.correct_mean_sample_8
                            self.tableWidget.setItem(10, 12,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_sample_8)))
                        except:
                            pass
                    elif 'Incorrect_sample' in str(string):
                        self.Incorrect_sample_8 += 1
                        self.tableWidget.setItem(10, 26,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Incorrect_sample_8)))
                        try:
                            self.incorrect_latency_sample_8 = time.time() - self.sample_start_time_8
                            self.incorrect_cv_sample_list_8.append(self.incorrect_latency_sample_8)
                            self.tableWidget.setItem(10, 53,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_cv_sample_list_8)))
                            self.incorrect_A_sample_8 = [float(i) for i in self.incorrect_cv_sample_list_8]
                            self.incorrect_lat_sample_mean_8 = statistics.mean(self.incorrect_A_sample_8)
                            self.tableWidget.setItem(10, 27,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lat_sample_mean_8)))
                        except:
                            pass
                    elif 'omission_sample' in str(string):
                        self.omission_sample_8 += 1
                        self.tableWidget.setItem(10, 25,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.omission_sample_8)))
                    elif 'reward_sample_taken' in str(string):
                        try:
                            self.Reward_Latency_sample_8 = time.time() - self.correct_sample_resp_time_8
                            self.reward_lat_sample_list_8.append(self.Reward_Latency_sample_8)
                            self.tableWidget.setItem(10, 51,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_sample_list_8)))
                            self.reward_A_sample_8 = [float(i) for i in self.reward_lat_sample_list_8]
                            self.reward_lat_sample_mean_8 = statistics.mean(self.reward_A_sample_8)
                            self.tableWidget.setItem(10, 10,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_sample_mean_8)))
                        except:
                            pass
                    elif "iti_sample" in str(string):
                        self.iti_start_time_8 = time.time()
                        self.tableWidget.setItem(10, 60,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.iti_start_time_8)))
                    elif 'Premature_response' in str(string):
                        self.Premature_sample_8 += 1
                        self.tableWidget.setItem(10, 23,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_sample_8)))
                        try:
                            self.Premature_Response_Latency_sample_8 = time.time() - self.iti_start_time_8
                            self.Premature_latancy_sample_list_8.append(self.Premature_Response_Latency_sample_8)
                            self.tableWidget.setItem(10, 56,
                                                     QtWidgets.QTableWidgetItem(
                                                         str(self.Premature_latancy_sample_list_8)))
                            self.premature_sample_8 = [float(i) for i in self.Premature_latancy_sample_list_8]
                            self.Premature_sample_mean_8 = statistics.mean(self.premature_sample_8)
                            self.tableWidget.setItem(10, 28,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_sample_mean_8)))
                        except:
                            pass
                    elif 'perseverate_sample' in str(string):
                        self.perseverate_sample_8 += 1
                        self.tableWidget.setItem(10, 29,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.perseverate_sample_8)))
                    elif 'attempts_dur_penalty_sample' in str(string):
                        self.resp_timeout_8 += 1
                        self.tableWidget.setItem(10, 31,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.resp_timeout_8)))
                    elif "choice_phase" in str(string):
                        self.choice_start_time_8 = time.time()
                        self.tableWidget.setItem(10, 61,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.choice_start_time_8)))
                    elif "Correct_choice" in str(string):
                        self.Correct_choice_8 += 1
                        self.tableWidget.setItem(10, 16,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Correct_choice_8)))
                        try:
                            self.correct_latency_choice_8 = time.time() - self.choice_start_time_8
                            self.correct_cv_choice_list_8.append(self.correct_latency_choice_8)
                            self.tableWidget.setItem(10, 50,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_choice_list_8)))
                            self.correct_choice_resp_time_8 = time.time()
                            self.tableWidget.setItem(10, 62,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_choice_resp_time_8)))
                            self.correct_A_choice_8 = [float(i) for i in self.correct_cv_choice_list_8]
                            self.correct_stdev_choice_8 = statistics.stdev(self.correct_A_choice_8)
                            self.tableWidget.setItem(10, 48,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_stdev_choice_8)))
                            self.correct_mean_choice_8 = statistics.mean(self.correct_A_choice_8)
                            self.tableWidget.setItem(10, 18,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_mean_choice_8)))
                            self.correct_cv_choice_8 = self.correct_stdev_choice_8 / self.correct_mean_choice_8
                            self.tableWidget.setItem(10, 21,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.correct_cv_choice_8)))
                        except:
                            pass
                    elif 'reward_choice_taken' in str(string):
                        try:
                            self.Reward_Latency_choice_8 = time.time() - self.correct_choice_resp_time_8
                            self.reward_lat_choice_list_8.append(self.Reward_Latency_choice_8)
                            self.tableWidget.setItem(10, 52,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_choice_list_8)))
                            self.reward_A_choice_8 = [float(i) for i in self.reward_lat_choice_list_8]
                            self.reward_lat_choice_mean_8 = statistics.mean(self.reward_A_choice_8)
                            self.tableWidget.setItem(10, 35,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.reward_lat_choice_mean_8)))
                        except:
                            pass
                    elif "incorrect_choice_lit" in str(string):
                        self.incorrect_lit_choice_8 += 1
                        self.tableWidget.setItem(10, 33,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lit_choice_8)))
                    elif 'Incorrect_choice' in str(string):
                        self.Incorrect_choice_8 += 1
                        self.tableWidget.setItem(10, 32,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Incorrect_choice_8)))
                        try:
                            self.incorrect_latency_choice_8 = time.time() - self.choice_start_time_8
                            self.incorrect_choice_list_8.append(self.incorrect_latency_choice_8)
                            self.tableWidget.setItem(10, 54,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_choice_list_8)))
                            self.incorrect_A_choice_8 = [float(i) for i in self.incorrect_choice_list_8]
                            self.incorrect_lat_choice_mean_8 = statistics.mean(self.incorrect_A_choice_8)
                            self.tableWidget.setItem(10, 34,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.incorrect_lat_choice_mean_8)))
                        except:
                            pass
                    elif 'omission_choice' in str(string):
                        self.omission_choice_8 += 1
                        self.tableWidget.setItem(10, 37,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.omission_choice_8)))
                    elif 'Premature_choice_correct' in str(string):
                        self.Premature_choice_correct_8 += 1
                        self.tableWidget.setItem(10, 19,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_correct_8)))
                    elif "delay" in str(string):
                        self.delay_start_time_8 = time.time()
                        self.tableWidget.setItem(10, 64,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.delay_start_time_8)))
                    elif 'Premature_choice_incorrect' in str(string):
                        self.Premature_choice_incorrect_8 += 1
                        self.tableWidget.setItem(10, 43,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_incorrect_8)))
                        try:
                            self.Premature_Response_Latency_choice_8 = time.time() - self.delay_start_time_8
                            self.Premature_latancy_choice_list_8.append(self.Premature_Response_Latency_choice_8)
                            self.tableWidget.setItem(10, 56,
                                                     QtWidgets.QTableWidgetItem(
                                                         str(self.Premature_latancy_choice_list_8)))
                            self.premature_choice_8 = [float(i) for i in self.Premature_latancy_choice_list_8]
                            self.Premature_choice_mean_8 = statistics.mean(self.premature_choice_8)
                            self.tableWidget.setItem(10, 28,
                                                     QtWidgets.QTableWidgetItem("{:.2f}".format(self.Premature_choice_mean_8)))
                        except:
                            pass
                    elif 'perseverate_choice' in str(string):
                        self.perseverate_choice_8 += 1
                        self.tableWidget.setItem(10, 38,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.perseverate_choice_8)))
                    elif 'attempts_dur_penalty_choice' in str(string):
                        self.resp_timeout_8 += 1
                        self.tableWidget.setItem(10, 40,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.resp_timeout_8)))
                    elif 'receptacle_entries' in str(string):
                        self.Receptacle_entries_8 += 1
                        self.tableWidget.setItem(10, 41,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Receptacle_entries_8)))
                    elif '5_poke_entries' in str(string):
                        self.Nosepokes_5poke_8 += 1
                        self.tableWidget.setItem(10, 42,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.Nosepokes_5poke_8)))
                    elif 'SP_reward' in str(string):
                        self.SP_reward_8 = value[2][12:]
                        self.tableWidget.setItem(10, 4,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.SP_reward_8)))
                    elif 'Event Closing' in str(string):
                        self.tableWidget.setItem(10, 0,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.date)))
                    try:
                        self.per_perseverate_sample_8 = (self.perseverate_sample_8 / self.Correct_sample_8) * 100
                        self.tableWidget.setItem(10, 30,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_perseverate_sample_8)))
                        self.per_omission_sample_8 = self.omission_sample_8 / (self.Correct_sample_8
                                                                               + self.Incorrect_sample_8
                                                                               + self.omission_sample_8) * 100
                        self.tableWidget.setItem(10, 9,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_omission_sample_8)))
                        self.per_accuracy_sample_8 = (self.Correct_sample_8 / (self.Correct_sample_8
                                                                               + self.Incorrect_sample_8)) * 100
                        self.tableWidget.setItem(10, 6,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_sample_8)))
                        self.per_correct_sample_8 = (self.Correct_sample_8 / (self.Correct_sample_8
                                                                              + self.Incorrect_sample_8
                                                                              + self.omission_sample_8)) * 100
                        self.tableWidget.setItem(10, 7,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_correct_sample_8)))

                        self.per_premature_sample_8 = self.Premature_sample_8 / (self.Correct_sample_8
                                                                                 + self.Incorrect_sample_8
                                                                                 + self.omission_sample_8) * 100
                        self.tableWidget.setItem(10, 24,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_premature_sample_8)))
                        self.trial_sample_8 = (self.Correct_sample_8 + self.Incorrect_sample_8 + self.omission_sample_8)
                        self.tableWidget.setItem(10, 22,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.trial_sample_8)))
                    except ZeroDivisionError:
                        pass
                    try:
                        self.per_perseverate_choice_8 = (self.perseverate_choice_8 / self.Correct_choice_8) * 100
                        self.tableWidget.setItem(10, 39,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_perseverate_choice_8)))
                        self.per_correct_choice_8 = (self.Correct_choice_8 / (self.Correct_choice_8
                                                                              + self.Incorrect_choice_8
                                                                              + self.incorrect_lit_choice_8
                                                                              + self.omission_choice_8)) * 100
                        self.tableWidget.setItem(10, 15,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_correct_choice_8)))

                        self.per_omission_choice_8 = (self.omission_choice_8 / (self.incorrect_lit_choice_8
                                                                                + self.Correct_choice_8
                                                                                + self.Incorrect_choice_8
                                                                                + self.omission_choice_8)) * 100
                        self.tableWidget.setItem(10, 17,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_omission_choice_8)))
                        self.per_accuracy_choice_8 = (self.Correct_choice_8 / (self.Correct_choice_8
                                                                               + self.incorrect_lit_choice_8
                                                                               + self.Incorrect_choice_8)) * 100
                        self.tableWidget.setItem(10, 14,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_choice_8)))
                        self.per_accuracy_lit_choice_8 = (self.Correct_choice_8 / (self.incorrect_lit_choice_8
                                                                                   + self.Correct_choice_8)) * 100
                        self.tableWidget.setItem(10, 13,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.per_accuracy_lit_choice_8)))
                        self.trial_choice_8 = (self.incorrect_lit_choice_8 + self.Correct_choice_8
                                               + self.Incorrect_choice_8 + self.omission_choice_8)
                        self.tableWidget.setItem(10, 20,
                                                 QtWidgets.QTableWidgetItem("{:.2f}".format(self.trial_choice_8)))
                    except ZeroDivisionError:
                        pass

    def items_clear(self):
        self.tableWidget.clearContents()
        self.lcdNumber_Timer_BOX1.display(0)
        self.lcdNumber_Timer_BOX2.display(0)
        self.lcdNumber_Timer_BOX3.display(0)
        self.lcdNumber_Timer_BOX4.display(0)
        self.lcdNumber_Timer_BOX5.display(0)
        self.lcdNumber_Timer_BOX6.display(0)
        self.lcdNumber_Timer_BOX7.display(0)
        self.lcdNumber_Timer_BOX8.display(0)
        self.sample_start_time_1 = 0
        self.correct_sample_resp_time_1 = 0
        self.iti_start_time_1 = 0
        self.choice_start_time_1 = 0
        self.correct_choice_resp_time_1 = 0
        self.delay_start_time_1 = 0
        self.sample_start_time_2 = 0
        self.correct_sample_resp_time_2 = 0
        self.iti_start_time_2 = 0
        self.choice_start_time_2 = 0
        self.correct_choice_resp_time_2 = 0
        self.delay_start_time_2 = 0
        self.sample_start_time_3 = 0
        self.correct_sample_resp_time_3 = 0
        self.iti_start_time_3 = 0
        self.choice_start_time_3 = 0
        self.correct_choice_resp_time_3 = 0
        self.delay_start_time_3 = 0
        self.sample_start_time_4 = 0
        self.correct_sample_resp_time_4 = 0
        self.iti_start_time_4 = 0
        self.choice_start_time_4 = 0
        self.correct_choice_resp_time_4 = 0
        self.delay_start_time_4 = 0
        self.sample_start_time_5 = 0
        self.correct_sample_resp_time_5 = 0
        self.iti_start_time_5 = 0
        self.choice_start_time_5 = 0
        self.correct_choice_resp_time_5 = 0
        self.delay_start_time_5 = 0
        self.sample_start_time_6 = 0
        self.correct_sample_resp_time_6 = 0
        self.iti_start_time_6 = 0
        self.choice_start_time_6 = 0
        self.correct_choice_resp_time_6 = 0
        self.delay_start_time_6 = 0
        self.sample_start_time_7 = 0
        self.correct_sample_resp_time_7 = 0
        self.iti_start_time_7 = 0
        self.choice_start_time_7 = 0
        self.correct_choice_resp_time_7 = 0
        self.delay_start_time_7 = 0
        self.sample_start_time_8 = 0
        self.correct_sample_resp_time_8 = 0
        self.iti_start_time_8 = 0
        self.choice_start_time_8 = 0
        self.correct_choice_resp_time_8 = 0
        self.delay_start_time_8 = 0
        self.Correct_sample_1 = 0
        self.Correct_sample_2 = 0
        self.Correct_sample_3 = 0
        self.Correct_sample_4 = 0
        self.Correct_sample_5 = 0
        self.Correct_sample_6 = 0
        self.Correct_sample_7 = 0
        self.Correct_sample_8 = 0
        self.Premature_Response_Latency_sample_1 = 0
        self.Premature_Response_Latency_sample_2 = 0
        self.Premature_Response_Latency_sample_3 = 0
        self.Premature_Response_Latency_sample_4 = 0
        self.Premature_Response_Latency_sample_5 = 0
        self.Premature_Response_Latency_sample_6 = 0
        self.Premature_Response_Latency_sample_7 = 0
        self.Premature_Response_Latency_sample_8 = 0
        self.premature_sample_1 = 0
        self.premature_sample_2 = 0
        self.premature_sample_3 = 0
        self.premature_sample_4 = 0
        self.premature_sample_5 = 0
        self.premature_sample_6 = 0
        self.premature_sample_7 = 0
        self.premature_sample_8 = 0
        self.Premature_sample_mean_1 = 0
        self.Premature_sample_mean_2 = 0
        self.Premature_sample_mean_3 = 0
        self.Premature_sample_mean_4 = 0
        self.Premature_sample_mean_5 = 0
        self.Premature_sample_mean_6 = 0
        self.Premature_sample_mean_7 = 0
        self.Premature_sample_mean_8 = 0
        self.Premature_Response_Latency_choice_1 = 0
        self.Premature_Response_Latency_choice_2 = 0
        self.Premature_Response_Latency_choice_3 = 0
        self.Premature_Response_Latency_choice_4 = 0
        self.Premature_Response_Latency_choice_5 = 0
        self.Premature_Response_Latency_choice_6 = 0
        self.Premature_Response_Latency_choice_7 = 0
        self.Premature_Response_Latency_choice_8 = 0
        self.Premature_latancy_sample_list_1 = []
        self.Premature_latancy_sample_list_2 = []
        self.Premature_latancy_sample_list_3 = []
        self.Premature_latancy_sample_list_4 = []
        self.Premature_latancy_sample_list_5 = []
        self.Premature_latancy_sample_list_6 = []
        self.Premature_latancy_sample_list_7 = []
        self.Premature_latancy_sample_list_8 = []
        self.Premature_latancy_choice_list_1 = []
        self.Premature_latancy_choice_list_2 = []
        self.Premature_latancy_choice_list_3 = []
        self.Premature_latancy_choice_list_4 = []
        self.Premature_latancy_choice_list_5 = []
        self.Premature_latancy_choice_list_6 = []
        self.Premature_latancy_choice_list_7 = []
        self.Premature_latancy_choice_list_8 = []
        self.premature_choice_1 = 0
        self.premature_choice_2 = 0
        self.premature_choice_3 = 0
        self.premature_choice_4 = 0
        self.premature_choice_5 = 0
        self.premature_choice_6 = 0
        self.premature_choice_7 = 0
        self.premature_choice_8 = 0
        self.Premature_choice_mean_1 = 0
        self.Premature_choice_mean_2 = 0
        self.Premature_choice_mean_3 = 0
        self.Premature_choice_mean_4 = 0
        self.Premature_choice_mean_5 = 0
        self.Premature_choice_mean_6 = 0
        self.Premature_choice_mean_7 = 0
        self.Premature_choice_mean_8 = 0
        self.omission_sample_1 = 0
        self.omission_sample_2 = 0
        self.omission_sample_3 = 0
        self.omission_sample_4 = 0
        self.omission_sample_5 = 0
        self.omission_sample_6 = 0
        self.omission_sample_7 = 0
        self.omission_sample_8 = 0
        self.Incorrect_sample_1 = 0
        self.Incorrect_sample_2 = 0
        self.Incorrect_sample_3 = 0
        self.Incorrect_sample_4 = 0
        self.Incorrect_sample_5 = 0
        self.Incorrect_sample_6 = 0
        self.Incorrect_sample_7 = 0
        self.Incorrect_sample_8 = 0
        self.Reward_Latency_sample_1 = 0
        self.Reward_Latency_sample_2 = 0
        self.Reward_Latency_sample_3 = 0
        self.Reward_Latency_sample_4 = 0
        self.Reward_Latency_sample_5 = 0
        self.Reward_Latency_sample_6 = 0
        self.Reward_Latency_sample_7 = 0
        self.Reward_Latency_sample_8 = 0
        self.Premature_sample_1 = 0
        self.Premature_sample_2 = 0
        self.Premature_sample_3 = 0
        self.Premature_sample_4 = 0
        self.Premature_sample_5 = 0
        self.Premature_sample_6 = 0
        self.Premature_sample_7 = 0
        self.Premature_sample_8 = 0
        self.perseverate_sample_1 = 0
        self.perseverate_sample_2 = 0
        self.perseverate_sample_3 = 0
        self.perseverate_sample_4 = 0
        self.perseverate_sample_5 = 0
        self.perseverate_sample_6 = 0
        self.perseverate_sample_7 = 0
        self.perseverate_sample_8 = 0
        self.Premature_Response_Latency_sample_Mean_1 = 0
        self.Premature_Response_Latency_sample_Mean_2 = 0
        self.Premature_Response_Latency_sample_Mean_3 = 0
        self.Premature_Response_Latency_sample_Mean_4 = 0
        self.Premature_Response_Latency_sample_Mean_5 = 0
        self.Premature_Response_Latency_sample_Mean_6 = 0
        self.Premature_Response_Latency_sample_Mean_7 = 0
        self.Premature_Response_Latency_sample_Mean_8 = 0
        self.incorrect_latency_sample_1 = 0
        self.incorrect_latency_sample_2 = 0
        self.incorrect_latency_sample_3 = 0
        self.incorrect_latency_sample_4 = 0
        self.incorrect_latency_sample_5 = 0
        self.incorrect_latency_sample_6 = 0
        self.incorrect_latency_sample_7 = 0
        self.incorrect_latency_sample_8 = 0
        self.incorrect_latency_choice_1 = 0
        self.incorrect_latency_choice_2 = 0
        self.incorrect_latency_choice_3 = 0
        self.incorrect_latency_choice_4 = 0
        self.incorrect_latency_choice_5 = 0
        self.incorrect_latency_choice_6 = 0
        self.incorrect_latency_choice_7 = 0
        self.incorrect_latency_choice_8 = 0
        self.incorrect_latency_choice_9 = 0
        self.correct_latency_sample_1 = 0
        self.correct_latency_sample_2 = 0
        self.correct_latency_sample_3 = 0
        self.correct_latency_sample_4 = 0
        self.correct_latency_sample_5 = 0
        self.correct_latency_sample_6 = 0
        self.correct_latency_sample_7 = 0
        self.correct_latency_sample_8 = 0
        self.correct_A_sample_1 = 0
        self.correct_A_sample_2 = 0
        self.correct_A_sample_3 = 0
        self.correct_A_sample_4 = 0
        self.correct_A_sample_5 = 0
        self.correct_A_sample_6 = 0
        self.correct_A_sample_7 = 0
        self.correct_A_sample_8 = 0
        self.correct_cv_sample_list_1 = []
        self.correct_cv_sample_list_2 = []
        self.correct_cv_sample_list_3 = []
        self.correct_cv_sample_list_4 = []
        self.correct_cv_sample_list_5 = []
        self.correct_cv_sample_list_6 = []
        self.correct_cv_sample_list_7 = []
        self.correct_cv_sample_list_8 = []
        self.correct_stdev_sample_1 = 0
        self.correct_stdev_sample_2 = 0
        self.correct_stdev_sample_3 = 0
        self.correct_stdev_sample_4 = 0
        self.correct_stdev_sample_5 = 0
        self.correct_stdev_sample_6 = 0
        self.correct_stdev_sample_7 = 0
        self.correct_stdev_sample_8 = 0
        self.correct_mean_sample_1 = 0
        self.correct_mean_sample_2 = 0
        self.correct_mean_sample_3 = 0
        self.correct_mean_sample_4 = 0
        self.correct_mean_sample_5 = 0
        self.correct_mean_sample_6 = 0
        self.correct_mean_sample_7 = 0
        self.correct_mean_sample_8 = 0
        self.correct_cv_sample_1 = 0
        self.correct_cv_sample_2 = 0
        self.correct_cv_sample_3 = 0
        self.correct_cv_sample_4 = 0
        self.correct_cv_sample_5 = 0
        self.correct_cv_sample_6 = 0
        self.correct_cv_sample_7 = 0
        self.correct_cv_sample_8 = 0
        self.reward_lat_sample_list_1 = []
        self.reward_lat_sample_list_2 = []
        self.reward_lat_sample_list_3 = []
        self.reward_lat_sample_list_4 = []
        self.reward_lat_sample_list_5 = []
        self.reward_lat_sample_list_6 = []
        self.reward_lat_sample_list_7 = []
        self.reward_lat_sample_list_8 = []
        self.reward_lat_choice_list_1 = []
        self.reward_lat_choice_list_2 = []
        self.reward_lat_choice_list_3 = []
        self.reward_lat_choice_list_4 = []
        self.reward_lat_choice_list_5 = []
        self.reward_lat_choice_list_6 = []
        self.reward_lat_choice_list_7 = []
        self.reward_lat_choice_list_8 = []
        self.reward_A_sample_1 = 0
        self.reward_A_sample_2 = 0
        self.reward_A_sample_3 = 0
        self.reward_A_sample_4 = 0
        self.reward_A_sample_5 = 0
        self.reward_A_sample_6 = 0
        self.reward_A_sample_7 = 0
        self.reward_A_sample_8 = 0
        self.reward_lat_sample_mean_1 = 0
        self.reward_lat_sample_mean_2 = 0
        self.reward_lat_sample_mean_3 = 0
        self.reward_lat_sample_mean_4 = 0
        self.reward_lat_sample_mean_5 = 0
        self.reward_lat_sample_mean_6 = 0
        self.reward_lat_sample_mean_7 = 0
        self.reward_lat_sample_mean_8 = 0
        self.reward_lat_choice_list_1 = []
        self.reward_lat_sample_list_2 = []
        self.reward_lat_sample_list_3 = []
        self.reward_lat_sample_list_4 = []
        self.reward_lat_sample_list_5 = []
        self.reward_lat_sample_list_6 = []
        self.reward_lat_sample_list_7 = []
        self.reward_lat_sample_list_8 = []
        self.incorrect_A_sample_1 = 0
        self.incorrect_A_sample_2 = 0
        self.incorrect_A_sample_3 = 0
        self.incorrect_A_sample_4 = 0
        self.incorrect_A_sample_5 = 0
        self.incorrect_A_sample_6 = 0
        self.incorrect_A_sample_7 = 0
        self.incorrect_A_sample_8 = 0
        self.incorrect_lat_sample_mean_1 = 0
        self.incorrect_lat_sample_mean_2 = 0
        self.incorrect_lat_sample_mean_3 = 0
        self.incorrect_lat_sample_mean_4 = 0
        self.incorrect_lat_sample_mean_5 = 0
        self.incorrect_lat_sample_mean_6 = 0
        self.incorrect_lat_sample_mean_7 = 0
        self.incorrect_lat_sample_mean_8 = 0
        self.incorrect_cv_sample_list_1 = []
        self.incorrect_cv_sample_list_2 = []
        self.incorrect_cv_sample_list_3 = []
        self.incorrect_cv_sample_list_4 = []
        self.incorrect_cv_sample_list_5 = []
        self.incorrect_cv_sample_list_6 = []
        self.incorrect_cv_sample_list_7 = []
        self.incorrect_cv_sample_list_8 = []
        self.incorrect_latency_sample_Mean_1 = 0
        self.incorrect_latency_sample_Mean_2 = 0
        self.incorrect_latency_sample_Mean_3 = 0
        self.incorrect_latency_sample_Mean_4 = 0
        self.incorrect_latency_sample_Mean_5 = 0
        self.incorrect_latency_sample_Mean_6 = 0
        self.incorrect_latency_sample_Mean_7 = 0
        self.incorrect_latency_sample_Mean_8 = 0
        self.trial_sample_1 = 0
        self.trial_sample_2 = 0
        self.trial_sample_3 = 0
        self.trial_sample_4 = 0
        self.trial_sample_5 = 0
        self.trial_sample_6 = 0
        self.trial_sample_7 = 0
        self.trial_sample_8 = 0
        self.per_omission_sample_1 = 0
        self.per_omission_sample_2 = 0
        self.per_omission_sample_3 = 0
        self.per_omission_sample_4 = 0
        self.per_omission_sample_5 = 0
        self.per_omission_sample_6 = 0
        self.per_omission_sample_7 = 0
        self.per_omission_sample_8 = 0
        self.per_accuracy_sample_1 = 0
        self.per_accuracy_sample_2 = 0
        self.per_accuracy_sample_3 = 0
        self.per_accuracy_sample_4 = 0
        self.per_accuracy_sample_5 = 0
        self.per_accuracy_sample_6 = 0
        self.per_accuracy_sample_7 = 0
        self.per_accuracy_sample_8 = 0
        self.per_correct_sample_1 = 0
        self.per_correct_sample_2 = 0
        self.per_correct_sample_3 = 0
        self.per_correct_sample_4 = 0
        self.per_correct_sample_5 = 0
        self.per_correct_sample_6 = 0
        self.per_correct_sample_7 = 0
        self.per_correct_sample_8 = 0
        self.per_premature_sample_1 = 0
        self.per_premature_sample_2 = 0
        self.per_premature_sample_3 = 0
        self.per_premature_sample_4 = 0
        self.per_premature_sample_5 = 0
        self.per_premature_sample_6 = 0
        self.per_premature_sample_7 = 0
        self.per_premature_sample_8 = 0
        self.per_perseverate_sample_1 = 0
        self.per_perseverate_sample_2 = 0
        self.per_perseverate_sample_3 = 0
        self.per_perseverate_sample_4 = 0
        self.per_perseverate_sample_5 = 0
        self.per_perseverate_sample_6 = 0
        self.per_perseverate_sample_7 = 0
        self.per_perseverate_sample_8 = 0
        self.Correct_choice_1 = 0
        self.Correct_choice_2 = 0
        self.Correct_choice_3 = 0
        self.Correct_choice_4 = 0
        self.Correct_choice_5 = 0
        self.Correct_choice_6 = 0
        self.Correct_choice_7 = 0
        self.Correct_choice_8 = 0
        self.Incorrect_choice_1 = 0
        self.Incorrect_choice_2 = 0
        self.Incorrect_choice_3 = 0
        self.Incorrect_choice_4 = 0
        self.Incorrect_choice_5 = 0
        self.Incorrect_choice_6 = 0
        self.Incorrect_choice_7 = 0
        self.Incorrect_choice_8 = 0
        self.omission_choice_1 = 0
        self.omission_choice_2 = 0
        self.omission_choice_3 = 0
        self.omission_choice_4 = 0
        self.omission_choice_5 = 0
        self.omission_choice_6 = 0
        self.omission_choice_7 = 0
        self.omission_choice_8 = 0
        self.Reward_Latency_choice_1 = 0
        self.Reward_Latency_choice_2 = 0
        self.Reward_Latency_choice_3 = 0
        self.Reward_Latency_choice_4 = 0
        self.Reward_Latency_choice_5 = 0
        self.Reward_Latency_choice_6 = 0
        self.Reward_Latency_choice_7 = 0
        self.Reward_Latency_choice_8 = 0
        self.Premature_choice_correct_1 = 0
        self.Premature_choice_correct_2 = 0
        self.Premature_choice_correct_3 = 0
        self.Premature_choice_correct_4 = 0
        self.Premature_choice_correct_5 = 0
        self.Premature_choice_correct_6 = 0
        self.Premature_choice_correct_7 = 0
        self.Premature_choice_correct_8 = 0
        self.Premature_choice_incorrect_1 = 0
        self.Premature_choice_incorrect_2 = 0
        self.Premature_choice_incorrect_3 = 0
        self.Premature_choice_incorrect_4 = 0
        self.Premature_choice_incorrect_5 = 0
        self.Premature_choice_incorrect_6 = 0
        self.Premature_choice_incorrect_7 = 0
        self.Premature_choice_incorrect_8 = 0
        self.perseverate_choice_1 = 0
        self.perseverate_choice_2 = 0
        self.perseverate_choice_3 = 0
        self.perseverate_choice_4 = 0
        self.perseverate_choice_5 = 0
        self.perseverate_choice_6 = 0
        self.perseverate_choice_7 = 0
        self.perseverate_choice_8 = 0
        self.resp_timeout_1 = 0
        self.resp_timeout_2 = 0
        self.resp_timeout_3 = 0
        self.resp_timeout_4 = 0
        self.resp_timeout_5 = 0
        self.resp_timeout_6 = 0
        self.resp_timeout_7 = 0
        self.resp_timeout_8 = 0
        self.Premature_Response_Latency_choice_Mean_1 = 0
        self.Premature_Response_Latency_choice_Mean_2 = 0
        self.Premature_Response_Latency_choice_Mean_3 = 0
        self.Premature_Response_Latency_choice_Mean_4 = 0
        self.Premature_Response_Latency_choice_Mean_5 = 0
        self.Premature_Response_Latency_choice_Mean_6 = 0
        self.Premature_Response_Latency_choice_Mean_7 = 0
        self.Premature_Response_Latency_choice_Mean_8 = 0
        self.correct_latency_choice_1 = 0
        self.correct_latency_choice_2 = 0
        self.correct_latency_choice_3 = 0
        self.correct_latency_choice_4 = 0
        self.correct_latency_choice_5 = 0
        self.correct_latency_choice_6 = 0
        self.correct_latency_choice_7 = 0
        self.correct_latency_choice_8 = 0
        self.incorrect_lit_choice_1 = 0
        self.incorrect_lit_choice_2 = 0
        self.incorrect_lit_choice_3 = 0
        self.incorrect_lit_choice_4 = 0
        self.incorrect_lit_choice_5 = 0
        self.incorrect_lit_choice_6 = 0
        self.incorrect_lit_choice_7 = 0
        self.incorrect_lit_choice_8 = 0
        self.Receptacle_entries_1 = 0
        self.Receptacle_entries_2 = 0
        self.Receptacle_entries_3 = 0
        self.Receptacle_entries_4 = 0
        self.Receptacle_entries_5 = 0
        self.Receptacle_entries_6 = 0
        self.Receptacle_entries_7 = 0
        self.Receptacle_entries_8 = 0
        self.Nosepokes_5poke_1 = 0
        self.Nosepokes_5poke_2 = 0
        self.Nosepokes_5poke_3 = 0
        self.Nosepokes_5poke_4 = 0
        self.Nosepokes_5poke_5 = 0
        self.Nosepokes_5poke_6 = 0
        self.Nosepokes_5poke_7 = 0
        self.Nosepokes_5poke_8 = 0
        self.SP_reward_1 = 0
        self.SP_reward_2 = 0
        self.SP_reward_3 = 0
        self.SP_reward_4 = 0
        self.SP_reward_5 = 0
        self.SP_reward_6 = 0
        self.SP_reward_7 = 0
        self.SP_reward_8 = 0
        self.correct_A_choice_1 = 0
        self.correct_A_choice_2 = 0
        self.correct_A_choice_3 = 0
        self.correct_A_choice_4 = 0
        self.correct_A_choice_5 = 0
        self.correct_A_choice_6 = 0
        self.correct_A_choice_7 = 0
        self.correct_A_choice_8 = 0
        self.correct_cv_choice_list_1 = []
        self.correct_cv_choice_list_2 = []
        self.correct_cv_choice_list_3 = []
        self.correct_cv_choice_list_4 = []
        self.correct_cv_choice_list_5 = []
        self.correct_cv_choice_list_6 = []
        self.correct_cv_choice_list_7 = []
        self.correct_cv_choice_list_8 = []
        self.correct_stdev_choice_1 = 0
        self.correct_stdev_choice_2 = 0
        self.correct_stdev_choice_3 = 0
        self.correct_stdev_choice_4 = 0
        self.correct_stdev_choice_5 = 0
        self.correct_stdev_choice_6 = 0
        self.correct_stdev_choice_7 = 0
        self.correct_stdev_choice_8 = 0
        self.correct_mean_choice_1 = 0
        self.correct_mean_choice_2 = 0
        self.correct_mean_choice_3 = 0
        self.correct_mean_choice_4 = 0
        self.correct_mean_choice_5 = 0
        self.correct_mean_choice_6 = 0
        self.correct_mean_choice_7 = 0
        self.correct_mean_choice_8 = 0
        self.correct_cv_choice_1 = 0
        self.correct_cv_choice_2 = 0
        self.correct_cv_choice_3 = 0
        self.correct_cv_choice_4 = 0
        self.correct_cv_choice_5 = 0
        self.correct_cv_choice_6 = 0
        self.correct_cv_choice_7 = 0
        self.correct_cv_choice_8 = 0
        self.reward_lat_choice_mean_1 = 0
        self.reward_lat_choice_mean_2 = 0
        self.reward_lat_choice_mean_3 = 0
        self.reward_lat_choice_mean_4 = 0
        self.reward_lat_choice_mean_5 = 0
        self.reward_lat_choice_mean_6 = 0
        self.reward_lat_choice_mean_7 = 0
        self.reward_lat_choice_mean_8 = 0
        self.incorrect_lat_choice_mean_1 = 0
        self.incorrect_lat_choice_mean_2 = 0
        self.incorrect_lat_choice_mean_3 = 0
        self.incorrect_lat_choice_mean_4 = 0
        self.incorrect_lat_choice_mean_5 = 0
        self.incorrect_lat_choice_mean_6 = 0
        self.incorrect_lat_choice_mean_7 = 0
        self.incorrect_lat_choice_mean_8 = 0
        self.reward_A_choice_1 = 0
        self.reward_A_choice_2 = 0
        self.reward_A_choice_3 = 0
        self.reward_A_choice_4 = 0
        self.reward_A_choice_5 = 0
        self.reward_A_choice_6 = 0
        self.reward_A_choice_7 = 0
        self.reward_A_choice_8 = 0
        self.incorrect_choice_list_1 = []
        self.incorrect_choice_list_2 = []
        self.incorrect_choice_list_3 = []
        self.incorrect_choice_list_4 = []
        self.incorrect_choice_list_5 = []
        self.incorrect_choice_list_6 = []
        self.incorrect_choice_list_7 = []
        self.incorrect_choice_list_8 = []
        self.incorrect_latency_choice_Mean_1 = 0
        self.incorrect_latency_choice_Mean_2 = 0
        self.incorrect_latency_choice_Mean_3 = 0
        self.incorrect_latency_choice_Mean_4 = 0
        self.incorrect_latency_choice_Mean_5 = 0
        self.incorrect_latency_choice_Mean_6 = 0
        self.incorrect_latency_choice_Mean_7 = 0
        self.incorrect_latency_choice_Mean_8 = 0
        self.trial_choice_1 = 0
        self.trial_choice_2 = 0
        self.trial_choice_3 = 0
        self.trial_choice_4 = 0
        self.trial_choice_5 = 0
        self.trial_choice_6 = 0
        self.trial_choice_7 = 0
        self.trial_choice_8 = 0
        self.per_correct_choice_1 = 0
        self.per_correct_choice_2 = 0
        self.per_correct_choice_3 = 0
        self.per_correct_choice_4 = 0
        self.per_correct_choice_5 = 0
        self.per_correct_choice_6 = 0
        self.per_correct_choice_7 = 0
        self.per_correct_choice_8 = 0
        self.per_omission_choice_1 = 0
        self.per_omission_choice_2 = 0
        self.per_omission_choice_3 = 0
        self.per_omission_choice_4 = 0
        self.per_omission_choice_5 = 0
        self.per_omission_choice_6 = 0
        self.per_omission_choice_7 = 0
        self.per_omission_choice_8 = 0
        self.per_accuracy_choice_1 = 0
        self.per_accuracy_choice_2 = 0
        self.per_accuracy_choice_3 = 0
        self.per_accuracy_choice_4 = 0
        self.per_accuracy_choice_5 = 0
        self.per_accuracy_choice_6 = 0
        self.per_accuracy_choice_7 = 0
        self.per_accuracy_choice_8 = 0
        self.per_accuracy_lit_choice_1 = 0
        self.per_accuracy_lit_choice_2 = 0
        self.per_accuracy_lit_choice_3 = 0
        self.per_accuracy_lit_choice_4 = 0
        self.per_accuracy_lit_choice_5 = 0
        self.per_accuracy_lit_choice_6 = 0
        self.per_accuracy_lit_choice_7 = 0
        self.per_accuracy_lit_choice_8 = 0
        self.per_perseverate_choice_1 = 0
        self.per_perseverate_choice_2 = 0
        self.per_perseverate_choice_3 = 0
        self.per_perseverate_choice_4 = 0
        self.per_perseverate_choice_5 = 0
        self.per_perseverate_choice_6 = 0
        self.per_perseverate_choice_7 = 0
        self.per_perseverate_choice_8 = 0
        self.incorrect_A_choice_1 = 0
        self.incorrect_A_choice_2 = 0
        self.incorrect_A_choice_3 = 0
        self.incorrect_A_choice_4 = 0
        self.incorrect_A_choice_5 = 0
        self.incorrect_A_choice_6 = 0
        self.incorrect_A_choice_7 = 0
        self.incorrect_A_choice_8 = 0
        self.lineEdit_subid1.clear()
        self.lineEdit_subid2.clear()
        self.lineEdit_subid3.clear()
        self.lineEdit_subid4.clear()
        self.lineEdit_subid5.clear()
        self.lineEdit_subid6.clear()
        self.lineEdit_subid7.clear()
        self.lineEdit_subid8.clear()

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
