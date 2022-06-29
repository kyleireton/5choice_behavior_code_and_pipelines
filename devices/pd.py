        self.tableWidget.setItem(0, 0,
                                 QtWidgets.QTableWidgetItem(str('Experimenter_name:')))
        self.exp_name = str(self.lineEdit_exp.text())
        self.tableWidget.setItem(0, 1,
                                 QtWidgets.QTableWidgetItem(str(self.exp_name)))
        self.tableWidget.setItem(0, 4,
                                 QtWidgets.QTableWidgetItem(str('Project:')))
        self.project = str(self.lineEdit_prj.text())
        self.tableWidget.setItem(0, 5,
                                 QtWidgets.QTableWidgetItem(str(self.project)))
        self.tableWidget.setItem(1, 0,
                                 QtWidgets.QTableWidgetItem(str('SUB_ID')))
        self.tableWidget.setItem(1, 1,
                                 QtWidgets.QTableWidgetItem(str('TASK')))
        self.tableWidget.setItem(1, 2,
                                 QtWidgets.QTableWidgetItem(str('DATA_online')))
        self.tableWidget.setItem(1, 3,
                                 QtWidgets.QTableWidgetItem(str('Accuracy(%)')))
        self.tableWidget.setItem(1, 4,
                                 QtWidgets.QTableWidgetItem(str('Omission(%)')))
        self.tableWidget.setItem(1, 5,
                                 QtWidgets.QTableWidgetItem(str('Correct(%)')))
        self.tableWidget.setItem(1, 6,
                                 QtWidgets.QTableWidgetItem(str('#Correct')))
        self.tableWidget.setItem(1, 7,
                                 QtWidgets.QTableWidgetItem(str('Premature(%)')))
        self.tableWidget.setItem(1, 8,
                                 QtWidgets.QTableWidgetItem(str('Rew. Lat.')))
        self.tableWidget.setItem(1, 9,
                                 QtWidgets.QTableWidgetItem(str('#Trials')))
        self.tableWidget.setItem(1, 10,
                                 QtWidgets.QTableWidgetItem(str('Perseverative(%)')))
        self.tableWidget.setItem(1, 11,
                                 QtWidgets.QTableWidgetItem(str('# Prematures')))
        self.tableWidget.setItem(1, 12,
                                 QtWidgets.QTableWidgetItem(str('#Omision')))
        self.tableWidget.setItem(1, 13,
                                 QtWidgets.QTableWidgetItem(str('#Incorrect')))
        self.tableWidget.setItem(1, 14,
                                 QtWidgets.QTableWidgetItem(str('Mean IL(sec)')))
        self.tableWidget.setItem(1, 15,
                                 QtWidgets.QTableWidgetItem(str('Mean PRT (sec)')))
        self.tableWidget.setItem(1, 16,
                                 QtWidgets.QTableWidgetItem(str('#Perseveratives')))
        self.tableWidget.setItem(1, 17,
                                 QtWidgets.QTableWidgetItem(str('#Receptacle_entries')))
        self.tableWidget.setItem(1, 18,
                                 QtWidgets.QTableWidgetItem(str('#Nosepokes_5poke')))
        self.tableWidget.setItem(1, 19,
                                 QtWidgets.QTableWidgetItem(str('#Resp_timeouts')))
        self.tableWidget.setItem(1, 20,
                                 QtWidgets.QTableWidgetItem(str('REMARKS')))

if new_data_1:
    self.tableWidget.setItem(2, 2,
                             QtWidgets.QTableWidgetItem(str(new_data_1)))
    for value in new_data_1:
        for string in value:
            if "Correct_response" in str(string):
                self.Correct_response_1 += 1
                self.tableWidget.setItem(2, 6,
                                         QtWidgets.QTableWidgetItem(str(self.Correct_response_1)))
            elif 'Incorrect_response' in str(string):
                self.Incorrect_response_1 += 1
                self.tableWidget.setItem(2, 13,
                                         QtWidgets.QTableWidgetItem(str(self.Incorrect_response_1)))
            elif 'Premature_response' in str(string):
                self.Premature_response_1 += 1
                self.tableWidget.setItem(2, 11,
                                         QtWidgets.QTableWidgetItem(str(self.Premature_response_1)))
            elif 'omission' in str(string):
                self.omission_1 += 1
                self.tableWidget.setItem(2, 12,
                                         QtWidgets.QTableWidgetItem(str(self.omission_1)))
            elif 'perseverate' in str(string):
                self.perseverate_1 += 1
                self.tableWidget.setItem(2, 16,
                                         QtWidgets.QTableWidgetItem(str(self.perseverate_1)))
            elif 'poke_6' in str(string):
                self.receptical_entry_1 += 1
                self.tableWidget.setItem(2, 17,
                                         QtWidgets.QTableWidgetItem(str(self.receptical_entry_1)))
            elif 'poke_1' in str(string):
                self.nose_poke_1 += 1
                self.tableWidget.setItem(2, 18,
                                         QtWidgets.QTableWidgetItem(str(self.nose_poke_1)))
            elif 'poke_2' in str(string):
                self.nose_poke_1 += 1
                self.tableWidget.setItem(2, 18,
                                         QtWidgets.QTableWidgetItem(str(self.nose_poke_1)))
            elif 'poke_3' in str(string):
                self.nose_poke_1 += 1
                self.tableWidget.setItem(2, 18,
                                         QtWidgets.QTableWidgetItem(str(self.nose_poke_1)))
            elif 'poke_4' in str(string):
                self.nose_poke_1 += 1
                self.tableWidget.setItem(2, 18,
                                         QtWidgets.QTableWidgetItem(str(self.nose_poke_1)))
            elif 'poke_5' in str(string):
                self.nose_poke_1 += 1
                self.tableWidget.setItem(2, 18,
                                         QtWidgets.QTableWidgetItem(str(self.nose_poke_1)))
            elif 'attempts_dur_penalty' in str(string):
                self.resp_timeout_1 += 1
                self.tableWidget.setItem(2, 19,
                                         QtWidgets.QTableWidgetItem(str(self.resp_timeout_1)))

    else:
        try:
            self.Choice_state_1 = self.omission_1 + self.Correct_response_1 \
                                  + self.Incorrect_response_1 + self.Premature_response_1
            self.tableWidget.setItem(2, 9,
                                     QtWidgets.QTableWidgetItem(str(self.Choice_state_1)))
            self.per_omission_1 = (self.omission_1 / (self.omission_1 + self.Correct_response_1
                                                      + self.Incorrect_response_1)) * 100
            self.tableWidget.setItem(2, 4,
                                     QtWidgets.QTableWidgetItem(str(self.per_omission_1)))
            self.per_accuracy_1 = (self.Correct_response_1 / (self.Correct_response_1
                                                              + self.Incorrect_response_1)) * 100
            self.tableWidget.setItem(2, 3,
                                     QtWidgets.QTableWidgetItem(str(self.per_accuracy_1)))
            self.per_correct_1 = (self.Correct_response_1 / (self.Correct_response_1 + self.Incorrect_response_1
                                                             + self.omission_1)) * 100
            self.tableWidget.setItem(2, 5,
                                     QtWidgets.QTableWidgetItem(str(self.per_correct_1)))
            self.per_premature_1 = (self.Premature_response_1 / self.Choice_state_1) * 100
            self.tableWidget.setItem(2, 7,
                                     QtWidgets.QTableWidgetItem(str(self.per_premature_1)))
            self.per_perseverate_1 = (self.perseverate_1 / self.Correct_response_1) * 100
            self.tableWidget.setItem(2, 10,
                                     QtWidgets.QTableWidgetItem(str(self.per_perseverate_1)))
        except ZeroDivisionError:
            pass
