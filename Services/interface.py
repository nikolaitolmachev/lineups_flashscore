# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from PyQt5 import QtCore, QtGui, QtWidgets
from Entities.match import Match, Sport, Team
from Entities.player import Player, Squad, Position, IHGoalkeeper
from Services.scraper import Scraper
import Services.consts as consts


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 1000)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1500, 1000))
        MainWindow.setMaximumSize(QtCore.QSize(1500, 1000))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Flags/icon_1.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(220, 10, 991, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 13, 55, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1230, 7, 93, 28))
        self.pushButton.setObjectName("pushButton")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(5, 50, 730, 991))
        self.groupBox.setStyleSheet("border: 0px")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(300, -10, 150, 80))
        self.label_2.setObjectName("label_2")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox)
        self.tableWidget.setGeometry(QtCore.QRect(5, 80, 721, 891))
        font = QtGui.QFont()
        font.setKerning(False)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.groupBox.setVisible(False)

        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(762, 50, 730, 991))
        self.groupBox_2.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.groupBox_2.setStatusTip("")
        self.groupBox_2.setAutoFillBackground(False)
        self.groupBox_2.setStyleSheet("border: 0px")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(300, -10, 150, 80))
        self.label_3.setObjectName("label_3")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget_2.setGeometry(QtCore.QRect(8, 80, 721, 891))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.groupBox_2.setVisible(False)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.__click_pushButton)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lineups"))
        self.label.setText(_translate("MainWindow", "URL"))
        self.pushButton.setText(_translate("MainWindow", "Chech lineups"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "TextLabel"))

    def __do_lineup(self, team: Team, sport: Sport, tableWidget: QtWidgets.QTableWidget, label: QtWidgets.QLabel):

        def get_nationality_for_image(nationality: str):
            if len(nationality.split(' ')) == 0:
                return nationality.lower()
            else:
                return nationality.replace(' ', '-').lower()

        label.clear()
        tableWidget.clear()

        # show team name
        label.setText(f'<div style="text-align: center"><img width="50" src="{team.logo}"><br/>{team.name}</div>')

        # set rows
        count_rows = len(team.players) + 1
        index_new_players = count_rows
        if len(team.new_players) != 0:
            count_rows += len(team.new_players) + 2
        index_empty_row_best_players = consts.INTERFACE_THE_BEST_PLAYERS_COUNT_FOOTBALL if sport == Sport.football \
                                        else consts.INTERFACE_THE_BEST_PLAYERS_COUNT_HOCKEY

        tableWidget.setRowCount(count_rows)
        for i in range(0, count_rows):
            if i == index_empty_row_best_players or i == index_new_players:
                tableWidget.setRowHeight(i, 1)
            else:
                tableWidget.setRowHeight(i, 12)

        # set columns
        WIDTH_COLUMN = 8
        COUNT_COLUMN = 12
        tableWidget.setColumnCount(COUNT_COLUMN)
        for i in range(0, COUNT_COLUMN):
            if i == 1:
                tableWidget.setColumnWidth(i, 180)
            else:
                tableWidget.setColumnWidth(i, WIDTH_COLUMN)

        # set style of grid
        tableWidget.setShowGrid(False)
        tableWidget.setStyleSheet('QTableView::item { border-top : 1px solid black;}')

        # set column headers
        tableWidget.setHorizontalHeaderLabels(['#', 'Name', '', 'Age', 'Pos', 'MP', 'G', 'SV', 'GAA', 'SO', 'Last XI',
                                               'Today'])
        # hide row headers
        tableWidget.verticalHeader().hide()

        # sort players list by matches played
        team.players = sorted(team.players, key=lambda pl: (pl.matches_played, pl.goals_scored), reverse=True)

        # fill a table of list of players
        j = 0
        for player in team.players:
            if j == index_empty_row_best_players:
                j += 1
            for i in range(0, COUNT_COLUMN):
                if i == 0:
                    value = player.number if player.number != None else ''
                elif i == 1:
                    tableWidget.setCellWidget(j, i, QtWidgets.QLabel(f'<a href="{player.url}">{player.name}</a>',
                                                                          openExternalLinks=True))
                    continue
                elif i == 2:
                    value = get_nationality_for_image(player.nationality)
                    tags = f'<div style="text-align: center;"><img width="15" src="Flags/{value}.png"></div>'
                    tableWidget.setCellWidget(j, i, QtWidgets.QLabel(tags))
                    continue
                elif i == 3:
                    value = player.age if player.age != None else '?'
                elif i == 4:
                    value = player.position.value
                elif i == 5:
                    value = player.matches_played
                elif i == 6:
                    if isinstance(player, IHGoalkeeper):
                        continue
                    else:
                        value = player.goals_scored
                elif i == 7:
                    if isinstance(player, IHGoalkeeper):
                        value = player.sv if player.sv != -1 else ''
                    else:
                        continue
                elif i == 8:
                    if isinstance(player, IHGoalkeeper):
                        value = player.gaa if player.gaa != -1 else ''
                    else:
                        continue
                elif i == 9:
                    if isinstance(player, IHGoalkeeper):
                        value = player.so if player.so != -1 else ''
                    else:
                        continue
                elif i == 10:
                    if player.info_squad_last_match == Squad.in_XI:
                        color = 'green'
                    elif player.info_squad_last_match == Squad.on_bench:
                        color = 'yellow'
                    else:
                        color = 'red'

                    tags = f'<div style="text-align: center; background-color: {color};"></div>'
                    tableWidget.setCellWidget(j, i, QtWidgets.QLabel(tags))
                    continue
                elif i == 11:
                    if player.info_squad == Squad.in_XI:
                        color = 'green'
                    elif player.info_squad == Squad.on_bench:
                        color = 'yellow'
                    else:
                        color = 'red'

                    tags = f'<div style="text-align: center; background-color: {color};"></div>'
                    tableWidget.setCellWidget(j, i, QtWidgets.QLabel(tags))
                    continue
                else:
                    value = ''
                item = QtWidgets.QTableWidgetItem(str(value))
                if i != 1:
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                tableWidget.setItem(j, i, item)

            j += 1

        # fill players which couldn't check (new_players)
        tableWidget.setItem(j, 1, QtWidgets.QTableWidgetItem('Can\'t mark the next:'))
        j += 1

        for player in team.new_players:
            if isinstance(player, Player):
                tableWidget.setCellWidget(j, 1, QtWidgets.QLabel(f'<a href="{player.url}">{player.name}</a>',
                                                             openExternalLinks=True))
            else:
                tableWidget.setCellWidget(j, 1, QtWidgets.QLabel(f'{player}'))
            j += 1

    def __click_pushButton(self):
        self.label_3.setText('')
        self.label_2.setText('')
        self.tableWidget.clear()
        self.tableWidget_2.clear()
        self.groupBox.setVisible(False)
        self.groupBox_2.setVisible(False)
        self.pushButton.setEnabled(False)

        if consts.FLASHSCORE_MAIN in self.lineEdit.text().strip():
            try:
                match = Scraper.get_match(self.lineEdit.text().strip())
            except KeyError:
                message = consts.ERROR_PATH_DRIVER
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(message)
                msg.setWindowTitle("Lineup")
                msg.setWindowIcon(QtGui.QIcon('Flags/icon_1.ico'))
                msg.exec_()
            else:
                if match == None or (len(match.team_a.players) == 0 and len(match.team_b.players) == 0):
                    if match == None:
                        message = consts.ERROR_WRONG_SPORT
                    else:
                        message = consts.ERROR_LINEUPS_NOT_READY
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setText(message)
                    msg.setWindowTitle("Lineup")
                    msg.setWindowIcon(QtGui.QIcon('Flags/icon_1.ico'))
                    msg.exec_()
                    self.lineEdit.setText('')
                else:
                    self.__do_lineup(match.team_a, match.sport, self.tableWidget, self.label_2)
                    self.__do_lineup(match.team_b, match.sport, self.tableWidget_2, self.label_3)
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText(consts.ERROR_WRONG_URL)
            msg.setWindowTitle("Lineup")
            msg.setWindowIcon(QtGui.QIcon('Flags/icon_1.ico'))
            msg.exec_()
            self.lineEdit.setText('')

        self.groupBox.setVisible(True)
        self.groupBox_2.setVisible(True)
        self.pushButton.setEnabled(True)
