import os
from pyqtgraph.Qt import QtGui, QtCore
from config.paths import config_dir

# Settings_dialog -------------------------------------------------------

class Settings_dialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(QtGui.QDialog, self).__init__(parent)
        self.setWindowTitle('GUI settings')
        # Create widgets.
        self.s_len_label = QtGui.QLabel('State history length')
        self.s_len_text  = QtGui.QLineEdit(str(100))
        self.e_len_label = QtGui.QLabel('Event hisory length')
        self.e_len_text  = QtGui.QLineEdit(str(100))
        self.a_len_label = QtGui.QLabel('Analog history duration (s)')
        self.a_len_text  = QtGui.QLineEdit(str(5))
        # Layout
        self.grid_layout = QtGui.QGridLayout()
        self.grid_layout.addWidget(self.s_len_label, 1, 1)
        self.grid_layout.addWidget(self.s_len_text , 1, 2)
        self.grid_layout.addWidget(self.e_len_label, 2, 1)
        self.grid_layout.addWidget(self.e_len_text , 2, 2)
        self.grid_layout.addWidget(self.a_len_label, 3, 1)
        self.grid_layout.addWidget(self.a_len_text , 3, 2)
        self.setLayout(self.grid_layout)
# Board_config_dialog -------------------------------------------------

class Board_config_dialog_1(QtGui.QDialog):
    def __init__(self, parent=None):
        super(QtGui.QDialog, self).__init__(parent)
        self.setWindowTitle('Configure pyboard')
        # Create widgets.
        self.load_fw_button = QtGui.QPushButton('Load framework')
        self.load_hw_button = QtGui.QPushButton('Load hardware definition')
        self.DFU_button = QtGui.QPushButton('Device Firmware Update (DFU) mode')
        self.flashdrive_button = QtGui.QPushButton()
        # Layout.
        self.vertical_layout = QtGui.QVBoxLayout()
        self.setLayout(self.vertical_layout)
        self.vertical_layout.addWidget(self.load_fw_button)
        self.vertical_layout.addWidget(self.load_hw_button)
        self.vertical_layout.addWidget(self.DFU_button)
        self.vertical_layout.addWidget(self.flashdrive_button)
        # Connect widgets.
        self.load_fw_button.clicked.connect(self.load_framework)
        self.load_hw_button.clicked.connect(self.load_hardware_definition)
        self.DFU_button.clicked.connect(self.DFU_mode)
        self.flashdrive_button.clicked.connect(self.flashdrive)
    def exec_(self):
        self.flashdrive_enabled = 'MSC' in self.parent().board_1.status['usb_mode']
        self.flashdrive_button.setText('{} USB flash drive'
            .format('Disable' if self.flashdrive_enabled else 'Enable'))
        return QtGui.QDialog.exec_(self)
    def load_framework(self):
        self.accept()
        self.parent().board_1.load_framework()
        self.parent().task_changed_1()
    def load_hardware_definition(self):
        hwd_path = QtGui.QFileDialog.getOpenFileName(self, 'Select hardware definition:',
                    os.path.join(config_dir, 'hardware_definition.py'), filter='*.py')[0]
        self.accept()
        self.parent().board_1.load_hardware_definition(hwd_path)
        self.parent().task_changed_1()
    def DFU_mode(self):
        self.accept()
        self.parent().board_1.DFU_mode()
        self.parent().disconnect()
        QtCore.QTimer.singleShot(500, self.parent().refresh)
    def flashdrive(self):
        self.accept()
        if self.flashdrive_enabled:
            self.parent().board_1.disable_mass_storage()
        else:
            self.parent().board_1.enable_mass_storage()
        self.parent().disconnect()
        QtCore.QTimer.singleShot(500, self.parent().refresh)

class Board_config_dialog_2(QtGui.QDialog):
    def __init__(self, parent=None):
        super(QtGui.QDialog, self).__init__(parent)
        self.setWindowTitle('Configure pyboard')
        # Create widgets.
        self.load_fw_button = QtGui.QPushButton('Load framework')
        self.load_hw_button = QtGui.QPushButton('Load hardware definition')
        self.DFU_button = QtGui.QPushButton('Device Firmware Update (DFU) mode')
        self.flashdrive_button = QtGui.QPushButton()
        # Layout.
        self.vertical_layout = QtGui.QVBoxLayout()
        self.setLayout(self.vertical_layout)
        self.vertical_layout.addWidget(self.load_fw_button)
        self.vertical_layout.addWidget(self.load_hw_button)
        self.vertical_layout.addWidget(self.DFU_button)
        self.vertical_layout.addWidget(self.flashdrive_button)
        # Connect widgets.
        self.load_fw_button.clicked.connect(self.load_framework)
        self.load_hw_button.clicked.connect(self.load_hardware_definition)
        self.DFU_button.clicked.connect(self.DFU_mode)
        self.flashdrive_button.clicked.connect(self.flashdrive)
    def exec_(self):
        self.flashdrive_enabled = 'MSC' in self.parent().board_2.status['usb_mode']
        self.flashdrive_button.setText('{} USB flash drive'
            .format('Disable' if self.flashdrive_enabled else 'Enable'))
        return QtGui.QDialog.exec_(self)
    def load_framework(self):
        self.accept()
        self.parent().board_2.load_framework()
        self.parent().task_changed_2()
    def load_hardware_definition(self):
        hwd_path = QtGui.QFileDialog.getOpenFileName(self, 'Select hardware definition:',
                    os.path.join(config_dir, 'hardware_definition.py'), filter='*.py')[0]
        self.accept()
        self.parent().board_2.load_hardware_definition(hwd_path)
        self.parent().task_changed_2()
    def DFU_mode(self):
        self.accept()
        self.parent().board_2.DFU_mode()
        self.parent().disconnect()
        QtCore.QTimer.singleShot(500, self.parent().refresh)
    def flashdrive(self):
        self.accept()
        if self.flashdrive_enabled:
            self.parent().board_2.disable_mass_storage()
        else:
            self.parent().board_2.enable_mass_storage()
        self.parent().disconnect()
        QtCore.QTimer.singleShot(500, self.parent().refresh)

class Board_config_dialog_3(QtGui.QDialog):
    def __init__(self, parent=None):
        super(QtGui.QDialog, self).__init__(parent)
        self.setWindowTitle('Configure pyboard')
        # Create widgets.
        self.load_fw_button = QtGui.QPushButton('Load framework')
        self.load_hw_button = QtGui.QPushButton('Load hardware definition')
        self.DFU_button = QtGui.QPushButton('Device Firmware Update (DFU) mode')
        self.flashdrive_button = QtGui.QPushButton()
        # Layout.
        self.vertical_layout = QtGui.QVBoxLayout()
        self.setLayout(self.vertical_layout)
        self.vertical_layout.addWidget(self.load_fw_button)
        self.vertical_layout.addWidget(self.load_hw_button)
        self.vertical_layout.addWidget(self.DFU_button)
        self.vertical_layout.addWidget(self.flashdrive_button)
        # Connect widgets.
        self.load_fw_button.clicked.connect(self.load_framework)
        self.load_hw_button.clicked.connect(self.load_hardware_definition)
        self.DFU_button.clicked.connect(self.DFU_mode)
        self.flashdrive_button.clicked.connect(self.flashdrive)
    def exec_(self):
        self.flashdrive_enabled = 'MSC' in self.parent().board_3.status['usb_mode']
        self.flashdrive_button.setText('{} USB flash drive'
            .format('Disable' if self.flashdrive_enabled else 'Enable'))
        return QtGui.QDialog.exec_(self)
    def load_framework(self):
        self.accept()
        self.parent().board_3.load_framework()
        self.parent().task_changed_3()
    def load_hardware_definition(self):
        hwd_path = QtGui.QFileDialog.getOpenFileName(self, 'Select hardware definition:',
                    os.path.join(config_dir, 'hardware_definition.py'), filter='*.py')[0]
        self.accept()
        self.parent().board_3.load_hardware_definition(hwd_path)
        self.parent().task_changed_3()
    def DFU_mode(self):
        self.accept()
        self.parent().board_3.DFU_mode()
        self.parent().disconnect()
        QtCore.QTimer.singleShot(500, self.parent().refresh)
    def flashdrive(self):
        self.accept()
        if self.flashdrive_enabled:
            self.parent().board_3.disable_mass_storage()
        else:
            self.parent().board_3.enable_mass_storage()
        self.parent().disconnect()
        QtCore.QTimer.singleShot(500, self.parent().refresh)

class Board_config_dialog_4(QtGui.QDialog):
    def __init__(self, parent=None):
        super(QtGui.QDialog, self).__init__(parent)
        self.setWindowTitle('Configure pyboard')
        # Create widgets.
        self.load_fw_button = QtGui.QPushButton('Load framework')
        self.load_hw_button = QtGui.QPushButton('Load hardware definition')
        self.DFU_button = QtGui.QPushButton('Device Firmware Update (DFU) mode')
        self.flashdrive_button = QtGui.QPushButton()
        # Layout.
        self.vertical_layout = QtGui.QVBoxLayout()
        self.setLayout(self.vertical_layout)
        self.vertical_layout.addWidget(self.load_fw_button)
        self.vertical_layout.addWidget(self.load_hw_button)
        self.vertical_layout.addWidget(self.DFU_button)
        self.vertical_layout.addWidget(self.flashdrive_button)
        # Connect widgets.
        self.load_fw_button.clicked.connect(self.load_framework)
        self.load_hw_button.clicked.connect(self.load_hardware_definition)
        self.DFU_button.clicked.connect(self.DFU_mode)
        self.flashdrive_button.clicked.connect(self.flashdrive)
    def exec_(self):
        self.flashdrive_enabled = 'MSC' in self.parent().board_4.status['usb_mode']
        self.flashdrive_button.setText('{} USB flash drive'
            .format('Disable' if self.flashdrive_enabled else 'Enable'))
        return QtGui.QDialog.exec_(self)
    def load_framework(self):
        self.accept()
        self.parent().board_4.load_framework()
        self.parent().task_changed_4()
    def load_hardware_definition(self):
        hwd_path = QtGui.QFileDialog.getOpenFileName(self, 'Select hardware definition:',
                    os.path.join(config_dir, 'hardware_definition.py'), filter='*.py')[0]
        self.accept()
        self.parent().board_4.load_hardware_definition(hwd_path)
        self.parent().task_changed_4()
    def DFU_mode(self):
        self.accept()
        self.parent().board_4.DFU_mode()
        self.parent().disconnect()
        QtCore.QTimer.singleShot(500, self.parent().refresh)
    def flashdrive(self):
        self.accept()
        if self.flashdrive_enabled:
            self.parent().board_4.disable_mass_storage()
        else:
            self.parent().board_4.enable_mass_storage()
        self.parent().disconnect()
        QtCore.QTimer.singleShot(500, self.parent().refresh)

class Board_config_dialog_5(QtGui.QDialog):
    def __init__(self, parent=None):
        super(QtGui.QDialog, self).__init__(parent)
        self.setWindowTitle('Configure pyboard')
        # Create widgets.
        self.load_fw_button = QtGui.QPushButton('Load framework')
        self.load_hw_button = QtGui.QPushButton('Load hardware definition')
        self.DFU_button = QtGui.QPushButton('Device Firmware Update (DFU) mode')
        self.flashdrive_button = QtGui.QPushButton()
        # Layout.
        self.vertical_layout = QtGui.QVBoxLayout()
        self.setLayout(self.vertical_layout)
        self.vertical_layout.addWidget(self.load_fw_button)
        self.vertical_layout.addWidget(self.load_hw_button)
        self.vertical_layout.addWidget(self.DFU_button)
        self.vertical_layout.addWidget(self.flashdrive_button)
        # Connect widgets.
        self.load_fw_button.clicked.connect(self.load_framework)
        self.load_hw_button.clicked.connect(self.load_hardware_definition)
        self.DFU_button.clicked.connect(self.DFU_mode)
        self.flashdrive_button.clicked.connect(self.flashdrive)
    def exec_(self):
        self.flashdrive_enabled = 'MSC' in self.parent().board_5.status['usb_mode']
        self.flashdrive_button.setText('{} USB flash drive'
            .format('Disable' if self.flashdrive_enabled else 'Enable'))
        return QtGui.QDialog.exec_(self)
    def load_framework(self):
        self.accept()
        self.parent().board_5.load_framework()
        self.parent().task_changed_5()
    def load_hardware_definition(self):
        hwd_path = QtGui.QFileDialog.getOpenFileName(self, 'Select hardware definition:',
                    os.path.join(config_dir, 'hardware_definition.py'), filter='*.py')[0]
        self.accept()
        self.parent().board_5.load_hardware_definition(hwd_path)
        self.parent().task_changed_5()
    def DFU_mode(self):
        self.accept()
        self.parent().board_5.DFU_mode()
        self.parent().disconnect()
        QtCore.QTimer.singleShot(500, self.parent().refresh)
    def flashdrive(self):
        self.accept()
        if self.flashdrive_enabled:
            self.parent().board_5.disable_mass_storage()
        else:
            self.parent().board_5.enable_mass_storage()
        self.parent().disconnect()
        QtCore.QTimer.singleShot(500, self.parent().refresh)

class Board_config_dialog_6(QtGui.QDialog):
    def __init__(self, parent=None):
        super(QtGui.QDialog, self).__init__(parent)
        self.setWindowTitle('Configure pyboard')
        # Create widgets.
        self.load_fw_button = QtGui.QPushButton('Load framework')
        self.load_hw_button = QtGui.QPushButton('Load hardware definition')
        self.DFU_button = QtGui.QPushButton('Device Firmware Update (DFU) mode')
        self.flashdrive_button = QtGui.QPushButton()
        # Layout.
        self.vertical_layout = QtGui.QVBoxLayout()
        self.setLayout(self.vertical_layout)
        self.vertical_layout.addWidget(self.load_fw_button)
        self.vertical_layout.addWidget(self.load_hw_button)
        self.vertical_layout.addWidget(self.DFU_button)
        self.vertical_layout.addWidget(self.flashdrive_button)
        # Connect widgets.
        self.load_fw_button.clicked.connect(self.load_framework)
        self.load_hw_button.clicked.connect(self.load_hardware_definition)
        self.DFU_button.clicked.connect(self.DFU_mode)
        self.flashdrive_button.clicked.connect(self.flashdrive)
    def exec_(self):
        self.flashdrive_enabled = 'MSC' in self.parent().board_6.status['usb_mode']
        self.flashdrive_button.setText('{} USB flash drive'
            .format('Disable' if self.flashdrive_enabled else 'Enable'))
        return QtGui.QDialog.exec_(self)
    def load_framework(self):
        self.accept()
        self.parent().board_6.load_framework()
        self.parent().task_changed_6()
    def load_hardware_definition(self):
        hwd_path = QtGui.QFileDialog.getOpenFileName(self, 'Select hardware definition:',
                    os.path.join(config_dir, 'hardware_definition.py'), filter='*.py')[0]
        self.accept()
        self.parent().board_6.load_hardware_definition(hwd_path)
        self.parent().task_changed_6()
    def DFU_mode(self):
        self.accept()
        self.parent().board_6.DFU_mode()
        self.parent().disconnect()
        QtCore.QTimer.singleShot(500, self.parent().refresh)
    def flashdrive(self):
        self.accept()
        if self.flashdrive_enabled:
            self.parent().board_6.disable_mass_storage()
        else:
            self.parent().board_6.enable_mass_storage()
        self.parent().disconnect()
        QtCore.QTimer.singleShot(500, self.parent().refresh)

class Board_config_dialog_7(QtGui.QDialog):
    def __init__(self, parent=None):
        super(QtGui.QDialog, self).__init__(parent)
        self.setWindowTitle('Configure pyboard')
        # Create widgets.
        self.load_fw_button = QtGui.QPushButton('Load framework')
        self.load_hw_button = QtGui.QPushButton('Load hardware definition')
        self.DFU_button = QtGui.QPushButton('Device Firmware Update (DFU) mode')
        self.flashdrive_button = QtGui.QPushButton()
        # Layout.
        self.vertical_layout = QtGui.QVBoxLayout()
        self.setLayout(self.vertical_layout)
        self.vertical_layout.addWidget(self.load_fw_button)
        self.vertical_layout.addWidget(self.load_hw_button)
        self.vertical_layout.addWidget(self.DFU_button)
        self.vertical_layout.addWidget(self.flashdrive_button)
        # Connect widgets.
        self.load_fw_button.clicked.connect(self.load_framework)
        self.load_hw_button.clicked.connect(self.load_hardware_definition)
        self.DFU_button.clicked.connect(self.DFU_mode)
        self.flashdrive_button.clicked.connect(self.flashdrive)
    def exec_(self):
        self.flashdrive_enabled = 'MSC' in self.parent().board_7.status['usb_mode']
        self.flashdrive_button.setText('{} USB flash drive'
            .format('Disable' if self.flashdrive_enabled else 'Enable'))
        return QtGui.QDialog.exec_(self)
    def load_framework(self):
        self.accept()
        self.parent().board_7.load_framework()
        self.parent().task_changed_7()
    def load_hardware_definition(self):
        hwd_path = QtGui.QFileDialog.getOpenFileName(self, 'Select hardware definition:',
                    os.path.join(config_dir, 'hardware_definition.py'), filter='*.py')[0]
        self.accept()
        self.parent().board_7.load_hardware_definition(hwd_path)
        self.parent().task_changed_7()
    def DFU_mode(self):
        self.accept()
        self.parent().board_7.DFU_mode()
        self.parent().disconnect()
        QtCore.QTimer.singleShot(500, self.parent().refresh)
    def flashdrive(self):
        self.accept()
        if self.flashdrive_enabled:
            self.parent().board_7.disable_mass_storage()
        else:
            self.parent().board_7.enable_mass_storage()
        self.parent().disconnect()
        QtCore.QTimer.singleShot(500, self.parent().refresh)

class Board_config_dialog_8(QtGui.QDialog):
    def __init__(self, parent=None):
        super(QtGui.QDialog, self).__init__(parent)
        self.setWindowTitle('Configure pyboard')
        # Create widgets.
        self.load_fw_button = QtGui.QPushButton('Load framework')
        self.load_hw_button = QtGui.QPushButton('Load hardware definition')
        self.DFU_button = QtGui.QPushButton('Device Firmware Update (DFU) mode')
        self.flashdrive_button = QtGui.QPushButton()
        # Layout.
        self.vertical_layout = QtGui.QVBoxLayout()
        self.setLayout(self.vertical_layout)
        self.vertical_layout.addWidget(self.load_fw_button)
        self.vertical_layout.addWidget(self.load_hw_button)
        self.vertical_layout.addWidget(self.DFU_button)
        self.vertical_layout.addWidget(self.flashdrive_button)
        # Connect widgets.
        self.load_fw_button.clicked.connect(self.load_framework)
        self.load_hw_button.clicked.connect(self.load_hardware_definition)
        self.DFU_button.clicked.connect(self.DFU_mode)
        self.flashdrive_button.clicked.connect(self.flashdrive)
    def exec_(self):
        self.flashdrive_enabled = 'MSC' in self.parent().board_8.status['usb_mode']
        self.flashdrive_button.setText('{} USB flash drive'
            .format('Disable' if self.flashdrive_enabled else 'Enable'))
        return QtGui.QDialog.exec_(self)
    def load_framework(self):
        self.accept()
        self.parent().board_8.load_framework()
        self.parent().task_changed_8()
    def load_hardware_definition(self):
        hwd_path = QtGui.QFileDialog.getOpenFileName(self, 'Select hardware definition:',
                    os.path.join(config_dir, 'hardware_definition.py'), filter='*.py')[0]
        self.accept()
        self.parent().board_8.load_hardware_definition(hwd_path)
        self.parent().task_changed_8()
    def DFU_mode(self):
        self.accept()
        self.parent().board_8.DFU_mode()
        self.parent().disconnect()
        QtCore.QTimer.singleShot(500, self.parent().refresh)
    def flashdrive(self):
        self.accept()
        if self.flashdrive_enabled:
            self.parent().board_8.disable_mass_storage()
        else:
            self.parent().board_8.enable_mass_storage()
        self.parent().disconnect()
        QtCore.QTimer.singleShot(500, self.parent().refresh)
# Variables_dialog ---------------------------------------------------------------------
class Variables_dialog(QtGui.QDialog):
    # Dialog for setting and getting task variables.
    def __init__(self, variable=None, parent=None):  # Should split into separate init and provide info.
        super(Variables_dialog, self).__init__(parent)
        self.setWindowTitle('Set variables')
        self.scroll_area = QtGui.QScrollArea(parent=self)
        self.scroll_area.setWidgetResizable(True)
        self.variables_grid = Variables_grid(parent=self.scroll_area, variable=variable)
        self.scroll_area.setWidget(self.variables_grid)
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)


class Variables_grid(QtGui.QWidget):
    # Grid of variables to set/get, displayed within qcross area of dialog.
    def __init__(self, variable=None, parent=None):
        super(Variables_grid, self).__init__(parent)
        if variable == 1:
            variables_1 = self.parent().parent().parent().sm_info_1['variables']
            self.grid_layout_1 = QtGui.QGridLayout()
            for i, (v_name, v_value_str) in enumerate(sorted(variables_1.items())):
                Variable_setter(v_name, v_value_str, self.grid_layout_1, i, board=1, parent=self)
            self.setLayout(self.grid_layout_1)
        if variable == 2:
            variables_2 = self.parent().parent().parent().sm_info_2['variables']
            self.grid_layout_2 = QtGui.QGridLayout()
            for i, (v_name, v_value_str) in enumerate(sorted(variables_2.items())):
                Variable_setter(v_name, v_value_str, self.grid_layout_2, i, board=2, parent=self)
            self.setLayout(self.grid_layout_2)
        if variable == 3:
            variables_3 = self.parent().parent().parent().sm_info_3['variables']
            self.grid_layout_3 = QtGui.QGridLayout()
            for i, (v_name, v_value_str) in enumerate(sorted(variables_3.items())):
                Variable_setter(v_name, v_value_str, self.grid_layout_3, i, board=3, parent=self)
            self.setLayout(self.grid_layout_3)
        if variable == 4:
            variables_4 = self.parent().parent().parent().sm_info_4['variables']
            self.grid_layout_4 = QtGui.QGridLayout()
            for i, (v_name, v_value_str) in enumerate(sorted(variables_4.items())):
                Variable_setter(v_name, v_value_str, self.grid_layout_4, i, board=4, parent=self)
            self.setLayout(self.grid_layout_4)
        if variable == 5:
            variables_5 = self.parent().parent().parent().sm_info_5['variables']
            self.grid_layout_5 = QtGui.QGridLayout()
            for i, (v_name, v_value_str) in enumerate(sorted(variables_5.items())):
                Variable_setter(v_name, v_value_str, self.grid_layout_5, i, board=5, parent=self)
            self.setLayout(self.grid_layout_5)
        if variable == 6:
            variables_6 = self.parent().parent().parent().sm_info_6['variables']
            self.grid_layout_6 = QtGui.QGridLayout()
            for i, (v_name, v_value_str) in enumerate(sorted(variables_6.items())):
                Variable_setter(v_name, v_value_str, self.grid_layout_6, i, board=6, parent=self)
            self.setLayout(self.grid_layout_6)
        if variable == 7:
            variables_7 = self.parent().parent().parent().sm_info_7['variables']
            self.grid_layout_7 = QtGui.QGridLayout()
            for i, (v_name, v_value_str) in enumerate(sorted(variables_7.items())):
                Variable_setter(v_name, v_value_str, self.grid_layout_7, i, board=7, parent=self)
            self.setLayout(self.grid_layout_7)
        if variable == 8:
            variables_8 = self.parent().parent().parent().sm_info_8['variables']
            self.grid_layout_8 = QtGui.QGridLayout()
            for i, (v_name, v_value_str) in enumerate(sorted(variables_8.items())):
                Variable_setter(v_name, v_value_str, self.grid_layout_8, i, board=8, parent=self)
            self.setLayout(self.grid_layout_8)


class Variable_setter(QtGui.QWidget):
    # For setting and getting a single variable.
    def __init__(self, v_name, v_value_str, grid_layout, i, board, parent=None): # Should split into seperate init and provide info.
        super(QtGui.QWidget, self).__init__(parent)
        if board == 1:
            self.board = self.parent().parent().parent().parent().board_1
        elif board == 2:
            self.board = self.parent().parent().parent().parent().board_2
        elif board == 3:
            self.board = self.parent().parent().parent().parent().board_3
        elif board == 4:
            self.board = self.parent().parent().parent().parent().board_4
        elif board == 5:
            self.board = self.parent().parent().parent().parent().board_5
        elif board == 6:
            self.board = self.parent().parent().parent().parent().board_6
        elif board == 7:
            self.board = self.parent().parent().parent().parent().board_7
        elif board == 8:
            self.board = self.parent().parent().parent().parent().board_8
        self.v_name = v_name
        self.label = QtGui.QLabel(v_name)
        self.get_button = QtGui.QPushButton('Get value')
        self.set_button = QtGui.QPushButton('Set value')
        self.value_str = QtGui.QLineEdit(v_value_str)
        if v_value_str[0] == '<': # Variable is a complex object that cannot be modifed.
            self.value_str.setText('<complex object>')
            self.set_button.setEnabled(False)
            self.get_button.setEnabled(False)
        self.value_text_colour('gray')
        self.get_button.clicked.connect(self.get)
        self.set_button.clicked.connect(self.set)
        self.value_str.textChanged.connect(lambda x: self.value_text_colour('black'))
        self.value_str.returnPressed.connect(self.set)
        self.get_button.setDefault(False)
        self.get_button.setAutoDefault(False)
        self.set_button.setDefault(False)
        self.set_button.setAutoDefault(False)
        grid_layout.addWidget(self.label     , i, 1)
        grid_layout.addWidget(self.value_str , i, 2)
        grid_layout.addWidget(self.get_button, i, 3)
        grid_layout.addWidget(self.set_button, i, 4)

    def value_text_colour(self, color='gray'):
        self.value_str.setStyleSheet("color: {};".format(color))

    def get(self):
        if self.board.framework_running: # Value returned later.
            self.board.get_variable(self.v_name)
            self.value_str.setText('getting..')
            QtCore.QTimer.singleShot(200, self.reload)
        else: # Value returned immediately.
            self.value_str.setText(str(self.board.get_variable(self.v_name))) 
            QtCore.QTimer.singleShot(1000, self.value_text_colour)

    def set(self):
        try:
            v_value = eval(self.value_str.text())
        except Exception:
            self.value_str.setText('Invalid value')
            return
        if self.board.framework_running: # Value returned later if set OK.
            self.board.set_variable(self.v_name, v_value)
            self.value_str.setText('setting..')
            QtCore.QTimer.singleShot(200, self.reload)
        else: # Set OK returned immediately.
            if self.board.set_variable(self.v_name, v_value):
                self.value_text_colour('gray')
            else:
                self.value_str.setText('Set failed')
                
    def reload(self):
        '''Reload value from sm_info.  sm_info is updated when variables are output
        during framework run due to get/set.'''
        self.value_text_colour('black')
        self.value_str.setText(str(self.board.sm_info['variables'][self.v_name]))
        QtCore.QTimer.singleShot(1000, self.value_text_colour)