#### Data collection script #### mlong 16/01/2019
import tkinter as tk
from tkinter import messagebox

import ctypes

from tkinter import filedialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QTableWidget,QTableWidgetItem
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
import numpy as np
from numpy import *
import numpy.ma as ma
import cv2
import pypylon.pylon as py
import time
from datetime import datetime
import argparse
import qimage2ndarray
import pandas
import math
import re

import matplotlib
from matplotlib import style
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import pygame
import urllib
import json
import itertools
import pprint

import subprocess

import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
import glob, os
from xlrd import open_workbook
from scipy import signal
from scipy.signal import butter, lfilter, freqz, filtfilt
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d
from scipy.interpolate import CubicSpline


from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Image
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.colors import PCMYKColor, PCMYKColorSep, Color, black, blue, red, white

# import MQTT package        
import paho.mqtt.client as mqtt 
import ssl
import requests

# host = "192.168.160.43"
host ="10.0.0.254"
port = 1883
topic = "tagsLive"

class Point:
#'"' "Just a simple container for XY points"""
    def __init__(self, x,y):
         self.x = x
         self.y = y


# Create a class that will save the positions of individual tags, convert them to pixels, as well as visualise them in pygame
class PozyxTag():
#"""Pozyx tags have both an ID, a position, and a small history of their positions"""
    def __init__(self, id_, max_path_size=1):             # tag. something
        self.id = id_
        self.position = Point(0, 0)        
        self.max_path_size = max_path_size
        self.saved_positions = [] 
    def set_position( self, x, y):
        self.position = Point(int(x), int(y))
    def calculate_pixel_position( self, position):
        pixel_x = (position.x - MINIMUM_COORDINATES.x) / PIXEL_RATIO_X
        pixel_y = (position.y - MINIMUM_COORDINATES.y) / PIXEL_RATIO_Y
      #  print(pixel_x,pixel_y)        
        return [pixel_x, pixel_y]

    @property
    def pixel_position(self):
        return self.calculate_pixel_position(self.position) 
    def draw_history(self):
        for saved_position in self.saved_positions:
            pixel_position=self.calculate_pixel_position(saved_position)
         
            
        pygame.draw.circle(game_display,TAG_HISTORY_MAIN_COLOR,[int(pixel_position[0]),int(pixel_position[1])],4,1)
        pygame.draw.circle(game_display, TAG_HISTORY_SECONDARY_COLOR,[int(pixel_position[0]), int( pixel_position[1])],3,0)
        
    def draw_tag_position(self):
        global game_display2; global text2;global Graphic; global Track_graphic;global Drills_Graphic; global display_counter; 
        display_counter+=1
        remainder=display_counter%10
      #  print("D",display_counter)
        text3=str(display_counter)
        fontname = 'freesansbold.ttf'
        fontsize = 10
        fontsize2=20
        fontsize3=20
        font_error=0
        surface_error=0
        pygame.font.init()
        time.sleep(.01)
        font_int=0
        font_int=pygame.font.get_init()
        if font_int ==1:
            try:
                font = pygame.font.Font(fontname, fontsize)
                font2 = pygame.font.Font(fontname, fontsize2)
                font3 = pygame.font.Font(fontname, fontsize3)
            except RuntimeError:
                print("font error")
                font_error=1
        else:     
            font_error=1
            
        antialias = True
        colour = 0,0,0
        Ui_Dialog().score()
        
        if font_error==0: 
            try:
                textSurf = font.render(text, antialias, colour) # tag number
                textSurf1 = font2.render(text2, antialias, colour) #score
                textSurf2 = font3.render(text3, antialias, colour) #score
            except RuntimeError:
                print ("no text Surface")
                surface_error=1
        else:
            surface_error=1
        
        pixel_position = self.calculate_pixel_position(self.position)

        if font_error==0 and surface_error==0: 
                game_display.blit(textSurf1,[400,10])
                game_display.blit(floorplan_image2,[750,10])
                game_display.blit(textSurf2,[750,10])                   
        else:
            pass
        

        if self.id<=7:        
            pygame.draw.circle(game_display, TAG_SECONDARY_COLOR, [ int(pixel_position[0]),
            int(pixel_position[1])], 10, 0)
 #           print(self.id,pixel_position[1])
        else:
            pygame.draw.circle(game_display, TAG_MAIN_COLOR_2, [ int(pixel_position[0]),
            int(pixel_position[1])], 10, 0)
                 
        if font_error==0 and surface_error==0:
            game_display.blit(textSurf, [int(pixel_position[0]-5),
            int(pixel_position[1]-5)])
        else:
            pass

        #image conversion # 
        game_display1=game_display.get_buffer().raw        
        game_display2=QImage(game_display1,Graphic.width(),Graphic.height(),QImage.Format_RGB32) ##works
        Ui_Dialog().screen_update(Graphic,1)
     
        
    def display(self):
        global display_counter;global Picture_Display;global end_Tag_counter        
        self.saved_positions.append(self.position) 
        # If enough data has been collected, plot the path of the tag
        if len( self.saved_positions) > self.max_path_size:
        # eliminate first element of the array so it does not become too Large
            self.saved_positions.pop(0)
            self.draw_history()
        self.draw_tag_position()

        

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        global save;global b;global img;global video;global board;global file_1; global close_1; global topic1;global New_Trial; global New_Trial_1;
        global counter; global topic1; global record; global row; global column; global connected; global graph; global connect; global topic2;
        global topic3; global flag; global file_2;global file;global new_trial_count; global data_exists;global Red_team_counter; global Blue_team_counter;
        global game_display; global Graphic; global Track_graphic; global Drills_Graphic; global output_value; global display_counter; global record_counter
        display_counter=0
        record_counter=0
        
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(1300, 650)

        ## General Variables ##
        video=0
        save=1
        close_1=0         
        counter = 0
        topic1 = 0
        record = 0
        row = 0
        column = 0
        connected = 0
        graph = 0 
        connect = 0
        New_trial = 0
        New_Trial_1 = 0
        topic2 = 0
        topic3 = 0
        flag = 0
        new_trial_count=0
        data_exists=0
        Red_team_counter=0
        Blue_team_counter=0
        output_value=0
        
############################################# Tab creation ###########################################################
        self.parent_tabWidget = QtWidgets.QTabWidget(Dialog)
        self.parent_tabWidget.setGeometry(QtCore.QRect(10, 10, 1266, 620))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.parent_tabWidget.setFont(font)
        self.parent_tabWidget.setObjectName("parent_tabWidget")

        self.Tab_Game = QtWidgets.QWidget()
        self.Tab_Game.setObjectName("Tab_Game")
        self.parent_tabWidget.addTab(self.Tab_Game, "")

        self.Tab_Drills = QtWidgets.QWidget()
        self.Tab_Drills.setObjectName("Tab_Drills")
        self.parent_tabWidget.addTab(self.Tab_Drills, "")

        self.Tab_Results = QtWidgets.QWidget()
        self.Tab_Results.setObjectName("Tab_Results")
        self.parent_tabWidget.addTab(self.Tab_Results, "")
        
######################################################################################################################
        
                                     # Tab_Game
                                     
##########################################   Track graphic ###########################################################
  
        self.Track_graphic = QtWidgets.QLabel(self.Tab_Game)
        self.Track_graphic.setGeometry(QtCore.QRect(200, 150, 819, 412))
        self.Track_graphic.setAutoFillBackground(False)
        self.Track_graphic.setStyleSheet("background-color: rgb(43, 43, 43);")
        self.Track_graphic.setPixmap(QPixmap('netball court3.JPG'))
        self.Track_graphic.setObjectName("Track_graphic")
        Track_graphic=self.Track_graphic
        
######################################################################################################################

##########################################   Save File Button ########################################################
        
        self.Save_location_button = QtWidgets.QPushButton(self.Tab_Game)
        self.Save_location_button.setGeometry(QtCore.QRect(400, 10, 90, 23))
        self.Save_location_button.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.Save_location_button.setObjectName("Save_location_button")
        self.Save_location_button.clicked.connect(self.Set_Output_location)
        
######################################################################################################################
##########################################   Save File Location  #####################################################
        
        self.Race_Save_location = QtWidgets.QLineEdit(self.Tab_Game)
        self.Race_Save_location.setGeometry(QtCore.QRect(500, 10, 220, 20))
        self.Race_Save_location.setStyleSheet("background-color: rgb(240, 240, 240);\n"
                                              "border-color: rgb(0, 0, 0);")
        self.Race_Save_location.setClearButtonEnabled(False)
        self.Race_Save_location.setObjectName("Race_Save_location")
######################################################################################################################

##########################################   Close button ############################################################
        
        self.Close_button = QtWidgets.QPushButton(self.Tab_Game)
        self.Close_button.setGeometry(QtCore.QRect(900, 50, 171, 70))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Close_button.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.Close_button.setFlat(False)
        self.Close_button.setObjectName("Close_button")
        self.Close_button.clicked.connect(self.Close)
        
######################################################################################################################

############################################   Data colleciton button ################################################
        self.Arm_button = QtWidgets.QPushButton(self.Tab_Game)
        self.Arm_button.setGeometry(QtCore.QRect(450, 50, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Arm_button.setFont(font)
        self.Arm_button.setStyleSheet("background-color: rgb(85, 255, 0);")
        self.Arm_button.setObjectName("Arm_button")
        self.Arm_button.setCheckable(True)
        self.Arm_button.clicked.connect(self.Save_Active)
        
######################################################################################################################

############################################   New File button ################################################
        self.New_File_button = QtWidgets.QPushButton(self.Tab_Game)
        self.New_File_button.setGeometry(QtCore.QRect(650, 50, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.New_File_button.setFont(font)
        self.New_File_button.setFlat(False)
        self.New_File_button.setObjectName("New_File_button")
        self.New_File_button.clicked.connect(self.New_Trial)
        
######################################################################################################################

############################################   Team 1 score button ################################################
        self.T1_Score_button = QtWidgets.QPushButton(self.Tab_Game)
        self.T1_Score_button.setGeometry(QtCore.QRect(400, 100, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.T1_Score_button.setFont(font)
        self.T1_Score_button.setFlat(False)       
        self.T1_Score_button.setObjectName("T1_Score_button")
        self.T1_Score_button.clicked.connect(self.T1_score)
        
        
######################################################################################################################

############################################   Team 2 score button ################################################
        self.T2_Score_button = QtWidgets.QPushButton(self.Tab_Game)
        self.T2_Score_button.setGeometry(QtCore.QRect(700, 100, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.T2_Score_button.setFont(font)
        self.T2_Score_button.setFlat(False)        
        self.T2_Score_button.setObjectName("T2_Score_button")
        self.T2_Score_button.clicked.connect(self.T2_score)
        
######################################################################################################################

############################################   POZYX connect button ################################################
        self.Connect_button = QtWidgets.QPushButton(self.Tab_Game)
        self.Connect_button.setGeometry(QtCore.QRect(30, 50, 170, 70))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Connect_button.setFont(font)
        self.Connect_button.setFlat(False)
        self.Connect_button.setObjectName("Connect_button")
        self.Connect_button.clicked.connect(self.POZYX_connect)
        
######################################################################################################################
############################################   POZYX disconnect button ################################################
        self.DisConnect_button = QtWidgets.QPushButton(self.Tab_Game)
        self.DisConnect_button.setGeometry(QtCore.QRect(210, 50, 170, 70))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.DisConnect_button.setFont(font)
        self.DisConnect_button.setFlat(False)
        self.DisConnect_button.setObjectName("Diconnect_button")
        self.DisConnect_button.clicked.connect(self.POZYX_Disconnect)
        
######################################################################################################################
        
##########################################   T1_Score box ############################################################
        
        self.T1_number_box = QtWidgets.QLineEdit(self.Tab_Game)
        self.T1_number_box.setGeometry(QtCore.QRect(550, 100, 51, 30))
        self.T1_number_box.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.T1_number_box.setClearButtonEnabled(False)
        self.T1_number_box.setText("0")
        self.T1_number_box.setObjectName("T1_number_box")

        
######################################################################################################################
##########################################   T2_Score box ############################################################
        
        self.T2_number_box = QtWidgets.QLineEdit(self.Tab_Game)
        self.T2_number_box.setGeometry(QtCore.QRect(620, 100, 51, 30))
        self.T2_number_box.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.T2_number_box.setClearButtonEnabled(False)
        self.T2_number_box.setText("0")
        self.T2_number_box.setObjectName("T2_number_box")

        
######################################################################################################################
##########################################   Tag update ############################################################
        
        self.Tag_update = QtWidgets.QPushButton(self.Tab_Game)
        self.Tag_update.setGeometry(QtCore.QRect(1100, 470, 150, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Tag_update.setFont(font)
        self.Tag_update.setFlat(False)
        self.Tag_update.setObjectName("Tag_update")
        self.Tag_update.clicked.connect(self.tag_check)

######################################################################################################################
##########################################   Tag Set ############################################################
        
        self.Tag_Set = QtWidgets.QPushButton(self.Tab_Game)
        self.Tag_Set.setGeometry(QtCore.QRect(1100, 420, 150, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Tag_Set.setFont(font)
        self.Tag_Set.setFlat(False)
        self.Tag_Set.setObjectName("Tag_set")
        self.Tag_Set.clicked.connect(self.Tag_Set1)
##########################################   Sub choice #############################################################
        
        self.Sub_Choice = QtWidgets.QComboBox(self.Tab_Game)
        self.Sub_Choice.setGeometry(QtCore.QRect(30, 410, 141, 22))
        self.Sub_Choice.setObjectName("Position_Box")
        self.Sub_Choice.addItem("")
        self.Sub_Choice.addItem("")
        self.Sub_Choice.addItem("")
        self.Sub_Choice.addItem("")
        self.Sub_Choice.addItem("")
        self.Sub_Choice.addItem("")
        self.Sub_Choice.addItem("")
        self.Sub_Choice.addItem("")
        self.Sub_Choice.addItem("")
        self.Sub_Choice.addItem("")
        self.Sub_Choice.addItem("")
        self.Sub_Choice.addItem("")
        self.Sub_Choice.addItem("")
        self.Sub_Choice.addItem("")
        self.Sub_Choice.addItem("")
        
##########################################   Sub Button ########################################################
        
        self.Substitution_button = QtWidgets.QPushButton(self.Tab_Game)
        self.Substitution_button.setGeometry(QtCore.QRect(60, 450, 90, 23))
        self.Substitution_button.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.Substitution_button.setObjectName("Save_location_button")
        self.Substitution_button.clicked.connect(self.Substitution)
        
######################################################################################################################        
######################################################################################################################
####################################  Tag Active check box   #########################################################
        self.Athlete_1_checkbox = QtWidgets.QCheckBox(self.Tab_Game)
        self.Athlete_1_checkbox.setGeometry(QtCore.QRect(30, 200, 21, 17))
        self.Athlete_1_checkbox.setText("")
        self.Athlete_1_checkbox.setObjectName("Athlete_1_checkbox")
        
        
        self.Athlete_2_checkbox = QtWidgets.QCheckBox(self.Tab_Game)
        self.Athlete_2_checkbox.setGeometry(QtCore.QRect(30, 230, 21, 17))
        self.Athlete_2_checkbox.setText("")
        self.Athlete_2_checkbox.setObjectName("Athlete_2_checkbox")
        
        self.Athlete_3_checkbox = QtWidgets.QCheckBox(self.Tab_Game)
        self.Athlete_3_checkbox.setGeometry(QtCore.QRect(30, 260, 21, 17))
        self.Athlete_3_checkbox.setText("")
        self.Athlete_3_checkbox.setObjectName("Athlete_3_checkbox")
        
        self.Athlete_4_checkbox = QtWidgets.QCheckBox(self.Tab_Game)
        self.Athlete_4_checkbox.setGeometry(QtCore.QRect(30, 290, 21, 17))
        self.Athlete_4_checkbox.setText("")
        self.Athlete_4_checkbox.setObjectName("Athlete_4_checkbox")
        
        self.Athlete_5_checkbox = QtWidgets.QCheckBox(self.Tab_Game)
        self.Athlete_5_checkbox.setGeometry(QtCore.QRect(30, 320, 21, 17))
        self.Athlete_5_checkbox.setText("")
        self.Athlete_5_checkbox.setObjectName("Athlete_5_checkbox")
        
        self.Athlete_6_checkbox = QtWidgets.QCheckBox(self.Tab_Game)
        self.Athlete_6_checkbox.setGeometry(QtCore.QRect(30, 350, 21, 17))
        self.Athlete_6_checkbox.setText("")
        self.Athlete_6_checkbox.setObjectName("Athlete_6_checkbox")
        
        self.Athlete_7_checkbox = QtWidgets.QCheckBox(self.Tab_Game)
        self.Athlete_7_checkbox.setGeometry(QtCore.QRect(30, 380, 21, 17))
        self.Athlete_7_checkbox.setText("")
        self.Athlete_7_checkbox.setObjectName("Athlete_7_checkbox")
        
        self.Athlete_11_checkbox = QtWidgets.QCheckBox(self.Tab_Game)
        self.Athlete_11_checkbox.setGeometry(QtCore.QRect(1100, 200, 21, 17))
        self.Athlete_11_checkbox.setText("")
        self.Athlete_11_checkbox.setObjectName("Athlete_11_checkbox")
        
        self.Athlete_12_checkbox = QtWidgets.QCheckBox(self.Tab_Game)
        self.Athlete_12_checkbox.setGeometry(QtCore.QRect(1100, 230, 21, 17))
        self.Athlete_12_checkbox.setText("")
        self.Athlete_12_checkbox.setObjectName("Athlete_12_checkbox")
        
        self.Athlete_13_checkbox = QtWidgets.QCheckBox(self.Tab_Game)
        self.Athlete_13_checkbox.setGeometry(QtCore.QRect(1100, 260, 21, 17))
        self.Athlete_13_checkbox.setText("")
        self.Athlete_13_checkbox.setObjectName("Athlete_13_checkbox")
        
        self.Athlete_14_checkbox = QtWidgets.QCheckBox(self.Tab_Game)
        self.Athlete_14_checkbox.setGeometry(QtCore.QRect(1100, 290, 21, 17))
        self.Athlete_14_checkbox.setText("")
        self.Athlete_14_checkbox.setObjectName("Athlete_14_checkbox")
        
        self.Athlete_15_checkbox = QtWidgets.QCheckBox(self.Tab_Game)
        self.Athlete_15_checkbox.setGeometry(QtCore.QRect(1100, 320, 21, 17))
        self.Athlete_15_checkbox.setText("")
        self.Athlete_15_checkbox.setObjectName("Athlete_15_checkbox")
        
        self.Athlete_16_checkbox = QtWidgets.QCheckBox(self.Tab_Game)
        self.Athlete_16_checkbox.setGeometry(QtCore.QRect(1100, 350, 21, 17))
        self.Athlete_16_checkbox.setText("")
        self.Athlete_16_checkbox.setObjectName("Athlete_16_checkbox")
        
        self.Athlete_17_checkbox = QtWidgets.QCheckBox(self.Tab_Game)
        self.Athlete_17_checkbox.setGeometry(QtCore.QRect(1100, 380, 21, 17))
        self.Athlete_17_checkbox.setText("")
        self.Athlete_17_checkbox.setObjectName("Athlete_17_checkbox")
        
######################################Labels #################################################################

        self.Team1_label = QtWidgets.QLabel(self.Tab_Game)
        self.Team1_label.setGeometry(QtCore.QRect(30, 150, 101, 21))
        self.Team1_label.setObjectName("Team 1 (Red)")

        self.GK_1_label = QtWidgets.QLabel(self.Tab_Game)
        self.GK_1_label.setGeometry(QtCore.QRect(50, 200, 71, 21))
        self.GK_1_label.setObjectName("GK1")
        
        self.WD_1_label = QtWidgets.QLabel(self.Tab_Game)
        self.WD_1_label.setGeometry(QtCore.QRect(50, 230, 71, 21))
        self.WD_1_label.setObjectName("WD1")

        self.GD_1_label = QtWidgets.QLabel(self.Tab_Game)
        self.GD_1_label.setGeometry(QtCore.QRect(50, 260, 71, 21))
        self.GD_1_label.setObjectName("GD1")

        self.C_1_label = QtWidgets.QLabel(self.Tab_Game)
        self.C_1_label.setGeometry(QtCore.QRect(50, 290, 71, 21))
        self.C_1_label.setObjectName("C1")

        self.GA_1_label = QtWidgets.QLabel(self.Tab_Game)
        self.GA_1_label.setGeometry(QtCore.QRect(50, 320, 71, 21))
        self.GA_1_label.setObjectName("GA1")

        self.WA_1_label = QtWidgets.QLabel(self.Tab_Game)
        self.WA_1_label.setGeometry(QtCore.QRect(50, 350, 71, 21))
        self.WA_1_label.setObjectName("WA1")

        self.GS_1_label = QtWidgets.QLabel(self.Tab_Game)
        self.GS_1_label.setGeometry(QtCore.QRect(50, 380, 71, 21))
        self.GS_1_label.setObjectName("GS1")

        self.Team2_label = QtWidgets.QLabel(self.Tab_Game)
        self.Team2_label.setGeometry(QtCore.QRect(1100, 150, 101, 21))
        self.Team2_label.setObjectName("Team 2 (Blue)")

        self.GK_2_label = QtWidgets.QLabel(self.Tab_Game)
        self.GK_2_label.setGeometry(QtCore.QRect(1120, 200, 71, 21))
        self.GK_2_label.setObjectName("GK2")
        
        self.WD_2_label = QtWidgets.QLabel(self.Tab_Game)
        self.WD_2_label.setGeometry(QtCore.QRect(1120, 230, 71, 21))
        self.WD_2_label.setObjectName("WD2")

        self.GD_2_label = QtWidgets.QLabel(self.Tab_Game)
        self.GD_2_label.setGeometry(QtCore.QRect(1120, 260, 71, 21))
        self.GD_2_label.setObjectName("GD2")

        self.C_2_label = QtWidgets.QLabel(self.Tab_Game)
        self.C_2_label.setGeometry(QtCore.QRect(1120, 290, 71, 21))
        self.C_2_label.setObjectName("C2")

        self.GA_2_label = QtWidgets.QLabel(self.Tab_Game)
        self.GA_2_label.setGeometry(QtCore.QRect(1120, 320, 71, 21))
        self.GA_2_label.setObjectName("GA2")

        self.WA_2_label = QtWidgets.QLabel(self.Tab_Game)
        self.WA_2_label.setGeometry(QtCore.QRect(1120, 350, 71, 21))
        self.WA_2_label.setObjectName("WA2")

        self.GS_2_label = QtWidgets.QLabel(self.Tab_Game)
        self.GS_2_label.setGeometry(QtCore.QRect(1120, 380, 71, 21))
        self.GS_2_label.setObjectName("GS2")
        
        
#####################################################################################################################################################################
#####################################################################################################################################################################
        
                            # Tab_Drills

######################################################################################################################

##########################################   Save File Button ########################################################
        
        self.Save_location_Drills_button = QtWidgets.QPushButton(self.Tab_Drills)
        self.Save_location_Drills_button.setGeometry(QtCore.QRect(250, 10, 90, 23))
        self.Save_location_Drills_button.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.Save_location_Drills_button.setObjectName("Save_location_button")
        self.Save_location_Drills_button.clicked.connect(self.Set_Output_location)
        
######################################################################################################################
##########################################   Save File Location  #####################################################
        
        self.Race_Save_Drills_location = QtWidgets.QLineEdit(self.Tab_Drills)
        self.Race_Save_Drills_location.setGeometry(QtCore.QRect(10, 10, 220, 20))
        self.Race_Save_Drills_location.setStyleSheet("background-color: rgb(240, 240, 240);\n"
                                              "border-color: rgb(0, 0, 0);")
        self.Race_Save_Drills_location.setClearButtonEnabled(False)
        self.Race_Save_Drills_location.setObjectName("Race_Save_location")
######################################################################################################################
        
######################################################################################################################
##########################################   Drill choice #############################################################
        
        self.Drill_Choice = QtWidgets.QComboBox(self.Tab_Drills)
        self.Drill_Choice.setGeometry(QtCore.QRect(10, 50, 141, 22))
        self.Drill_Choice.setObjectName("Drill_box")
        self.Drill_Choice.addItem("")
        self.Drill_Choice.addItem("")
        self.Drill_Choice.addItem("")
        self.Drill_Choice.addItem("")

######################################################################################################################

##########################################   Tag choice #############################################################
        
        self.Position_Choice = QtWidgets.QComboBox(self.Tab_Drills)
        self.Position_Choice.setGeometry(QtCore.QRect(10, 90, 141, 22))
        self.Position_Choice.setObjectName("Position_Box")
        self.Position_Choice.addItem("")
        self.Position_Choice.addItem("")
        self.Position_Choice.addItem("")
        self.Position_Choice.addItem("")
        self.Position_Choice.addItem("")
        self.Position_Choice.addItem("")
        self.Position_Choice.addItem("")
        self.Position_Choice.addItem("")
        self.Position_Choice.addItem("")
        self.Position_Choice.addItem("")
        self.Position_Choice.addItem("")
        self.Position_Choice.addItem("")
        self.Position_Choice.addItem("")
        self.Position_Choice.addItem("")
        self.Position_Choice.addItem("")

######################################################################################################################
###############################    Graphic   #########################################################################
        
        self.Drills_Graphic = QtWidgets.QLabel(self.Tab_Drills)
        self.Drills_Graphic.setGeometry(QtCore.QRect(600, 10, 662, 548))
        self.Drills_Graphic.setAutoFillBackground(False)
        self.Drills_Graphic.setStyleSheet("background-color: rgb(43, 43, 43);")
      #  self.Drills_Graphic.setPixmap(QPixmap('20m sprint.PNG'))
        self.Drills_Graphic.setObjectName("Drills_graphic")
        Drills_Graphic=self.Drills_Graphic
        
######################################################################################################################
###############################    Drill set button   ################################################################

        self.Set_Drill = QtWidgets.QPushButton(self.Tab_Drills)
        self.Set_Drill.setGeometry(QtCore.QRect(170, 50, 81, 23))
        self.Set_Drill.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.Set_Drill.setObjectName("Save_location_button")
        self.Set_Drill.clicked.connect(self.Set_Drill_method)
        
######################################################################################################################
###############################    Tag set button   ################################################################
        self.Set_Tag = QtWidgets.QPushButton(self.Tab_Drills)
        self.Set_Tag.setGeometry(QtCore.QRect(170, 90, 150, 23))
        self.Set_Tag.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.Set_Tag.setObjectName("Save_location_button")
        self.Set_Tag.clicked.connect(self.Set_Tag_method)

############################################   POZYX connect button ################################################
        self.Connect_button_Drills = QtWidgets.QPushButton(self.Tab_Drills)
        self.Connect_button_Drills.setGeometry(QtCore.QRect(10, 140, 170, 70))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Connect_button_Drills.setFont(font)
        self.Connect_button_Drills.setFlat(False)
        self.Connect_button_Drills.setObjectName("Connect_button_Drills")
        self.Connect_button_Drills.clicked.connect(self.POZYX_connect)
        
############################################   POZYX disconnect button ################################################
        self.DisConnect_button_Drills = QtWidgets.QPushButton(self.Tab_Drills)
        self.DisConnect_button_Drills.setGeometry(QtCore.QRect(190, 140, 170, 70))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.DisConnect_button_Drills.setFont(font)
        self.DisConnect_button_Drills.setFlat(False)
        self.DisConnect_button_Drills.setObjectName("Diconnect_button")
        self.DisConnect_button_Drills.clicked.connect(self.POZYX_Disconnect)
        
######################################################################################################################        
############################################   Data colleciton button ################################################
        self.Arm_button_Drills = QtWidgets.QPushButton(self.Tab_Drills)
        self.Arm_button_Drills.setGeometry(QtCore.QRect(10, 230, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Arm_button_Drills.setFont(font)
        self.Arm_button_Drills.setStyleSheet("background-color: rgb(85, 255, 0);")
        self.Arm_button_Drills.setObjectName("Arm_button")
        self.Arm_button_Drills.setCheckable(True)
        self.Arm_button_Drills.clicked.connect(self.Save_Active_Drills)                                                                # do work with button
        

######################################################################################################################
##########################################   Tag set ############################################################
        
        self.Tag_set_Drills = QtWidgets.QPushButton(self.Tab_Drills)
        self.Tag_set_Drills.setGeometry(QtCore.QRect(400, 240, 150, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Tag_set_Drills.setFont(font)
        self.Tag_set_Drills.setFlat(False)
        self.Tag_set_Drills.setObjectName("tag set drills")
        self.Tag_set_Drills.clicked.connect(self.Tag_Set1)
        self.Tag_set_Drills.setDisabled(True)
######################################################################################################################
##########################################   Tag update ############################################################
        
        self.Tag_update_Drills = QtWidgets.QPushButton(self.Tab_Drills)
        self.Tag_update_Drills.setGeometry(QtCore.QRect(400, 270, 150, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Tag_update_Drills.setFont(font)
        self.Tag_update_Drills.setFlat(False)
        self.Tag_update_Drills.setObjectName("New_File_button")
        self.Tag_update_Drills.clicked.connect(self.tag_check)
        self.Tag_update_Drills.setDisabled(True)

############################# load all files###############################################################################
        self.Load_Files_Button = QtWidgets.QPushButton(self.Tab_Drills)
        self.Load_Files_Button.setGeometry(QtCore.QRect(10, 300, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.Load_Files_Button.setFont(font)
        self.Load_Files_Button.setAutoDefault(False)
        self.Load_Files_Button.setDefault(True)
        self.Load_Files_Button.setFlat(False)
        self.Load_Files_Button.setObjectName("Load_Files_Button")
        self.Load_Files_Button.clicked.connect(self.Load_All_Files)

######################################################################################################################
        self.File_List_Text = QtWidgets.QListWidget(self.Tab_Drills)
        self.File_List_Text.setGeometry(QtCore.QRect(10, 350,171, 201))
        self.File_List_Text.setObjectName("File_List_Text")

##########################################   Close button ############################################################
        
        self.Close_button_Drills = QtWidgets.QPushButton(self.Tab_Drills)
        self.Close_button_Drills.setGeometry(QtCore.QRect(10, 560, 75, 23))
        self.Close_button_Drills.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.Close_button_Drills.setFlat(False)
        self.Close_button_Drills.setObjectName("Close_button")
        self.Close_button_Drills.clicked.connect(self.Close_Drills)

##################### processing button ########################################################################### 
        self.Process_File_Button = QtWidgets.QPushButton(self.Tab_Drills)
        self.Process_File_Button.setGeometry(QtCore.QRect(200, 520, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.Process_File_Button.setFont(font)
        self.Process_File_Button.setAutoDefault(False)
        self.Process_File_Button.setDefault(True)
        self.Process_File_Button.setFlat(False)
        self.Process_File_Button.setObjectName("Process_File_Button")
        self.Process_File_Button.clicked.connect(self.Process)

##########################################   File number choice #############################################################
        
        self.Filenumber_Choice = QtWidgets.QComboBox(self.Tab_Drills)
        self.Filenumber_Choice.setGeometry(QtCore.QRect(300, 55, 50, 22))
        self.Filenumber_Choice.setObjectName("Position_Box")
        self.Filenumber_Choice.addItem("")
        self.Filenumber_Choice.addItem("")
        self.Filenumber_Choice.addItem("")
        self.Filenumber_Choice.addItem("")
        self.Filenumber_Choice.addItem("")
        self.Filenumber_Choice.addItem("")
        self.Filenumber_Choice.addItem("")
        self.Filenumber_Choice.addItem("")
        self.Filenumber_Choice.addItem("")
        self.Filenumber_Choice.addItem("")

        self.Filenumber_label = QtWidgets.QLabel(self.Tab_Drills)
        self.Filenumber_label.setGeometry(QtCore.QRect(300, 35, 100, 22))
        self.Filenumber_label.setObjectName("File_label")
        
################################# Progress bar #######################################################################
        self.progressBar = QtWidgets.QProgressBar(self.Tab_Drills)
        self.progressBar.setGeometry(QtCore.QRect(350, 525, 221, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
#######################################################################################################################     
        
####################################  Illinois check box   #########################################################
        
        self.Athlete_1_Drillcheckbox = QtWidgets.QCheckBox(self.Tab_Drills)
        self.Athlete_1_Drillcheckbox.setGeometry(QtCore.QRect(400, 30, 21, 17))
        self.Athlete_1_Drillcheckbox.setText("")
        self.Athlete_1_Drillcheckbox.setObjectName("Athlete_1_Drillcheckbox")
        self.Athlete_1_Drillcheckbox.setDisabled(True)
        
        self.Athlete_2_Drillcheckbox = QtWidgets.QCheckBox(self.Tab_Drills)
        self.Athlete_2_Drillcheckbox.setGeometry(QtCore.QRect(400, 60, 21, 17))
        self.Athlete_2_Drillcheckbox.setText("")
        self.Athlete_2_Drillcheckbox.setObjectName("Athlete_2_Drillcheckbox")
        self.Athlete_2_Drillcheckbox.setDisabled(True)
        
        self.Athlete_3_Drillcheckbox = QtWidgets.QCheckBox(self.Tab_Drills)
        self.Athlete_3_Drillcheckbox.setGeometry(QtCore.QRect(400, 90, 21, 17))
        self.Athlete_3_Drillcheckbox.setText("")
        self.Athlete_3_Drillcheckbox.setObjectName("Athlete_3_Drillcheckbox")
        self.Athlete_3_Drillcheckbox.setDisabled(True)
        
        self.Athlete_4_Drillcheckbox = QtWidgets.QCheckBox(self.Tab_Drills)
        self.Athlete_4_Drillcheckbox.setGeometry(QtCore.QRect(400, 120, 21, 17))
        self.Athlete_4_Drillcheckbox.setText("")
        self.Athlete_4_Drillcheckbox.setObjectName("Athlete_4_Drillcheckbox")
        self.Athlete_4_Drillcheckbox.setDisabled(True)
        
        self.Athlete_5_Drillcheckbox = QtWidgets.QCheckBox(self.Tab_Drills)
        self.Athlete_5_Drillcheckbox.setGeometry(QtCore.QRect(400, 150, 21, 17))
        self.Athlete_5_Drillcheckbox.setText("")
        self.Athlete_5_Drillcheckbox.setObjectName("Athlete_5_Drillcheckbox")
        self.Athlete_5_Drillcheckbox.setDisabled(True)
        
        self.Athlete_6_Drillcheckbox = QtWidgets.QCheckBox(self.Tab_Drills)
        self.Athlete_6_Drillcheckbox.setGeometry(QtCore.QRect(400, 180, 21, 17))
        self.Athlete_6_Drillcheckbox.setText("")
        self.Athlete_6_Drillcheckbox.setObjectName("Athlete_6_Drillcheckbox")
        self.Athlete_6_Drillcheckbox.setDisabled(True)
        
        self.Athlete_7_Drillcheckbox = QtWidgets.QCheckBox(self.Tab_Drills)
        self.Athlete_7_Drillcheckbox.setGeometry(QtCore.QRect(400, 210, 21, 17))
        self.Athlete_7_Drillcheckbox.setText("")
        self.Athlete_7_Drillcheckbox.setObjectName("Athlete_7_Drillcheckbox")
        self.Athlete_7_Drillcheckbox.setDisabled(True)
        
        self.Athlete_8_Drillcheckbox = QtWidgets.QCheckBox(self.Tab_Drills)
        self.Athlete_8_Drillcheckbox.setGeometry(QtCore.QRect(480, 30, 21, 17))
        self.Athlete_8_Drillcheckbox.setText("")
        self.Athlete_8_Drillcheckbox.setObjectName("Athlete_8_Drillcheckbox")
        self.Athlete_8_Drillcheckbox.setDisabled(True)
        
        self.Athlete_9_Drillcheckbox = QtWidgets.QCheckBox(self.Tab_Drills)
        self.Athlete_9_Drillcheckbox.setGeometry(QtCore.QRect(480, 60, 21, 17))
        self.Athlete_9_Drillcheckbox.setText("")
        self.Athlete_9_Drillcheckbox.setObjectName("Athlete_9_Drillcheckbox")
        self.Athlete_9_Drillcheckbox.setDisabled(True)
        
        self.Athlete_10_Drillcheckbox = QtWidgets.QCheckBox(self.Tab_Drills)
        self.Athlete_10_Drillcheckbox.setGeometry(QtCore.QRect(480, 90, 21, 17))
        self.Athlete_10_Drillcheckbox.setText("")
        self.Athlete_10_Drillcheckbox.setObjectName("Athlete_10_Drillcheckbox")
        self.Athlete_10_Drillcheckbox.setDisabled(True)
        
        self.Athlete_11_Drillcheckbox = QtWidgets.QCheckBox(self.Tab_Drills)
        self.Athlete_11_Drillcheckbox.setGeometry(QtCore.QRect(480, 120, 21, 17))
        self.Athlete_11_Drillcheckbox.setText("")
        self.Athlete_11_Drillcheckbox.setObjectName("Athlete_11_Drillcheckbox")
        self.Athlete_11_Drillcheckbox.setDisabled(True)
        
        self.Athlete_12_Drillcheckbox = QtWidgets.QCheckBox(self.Tab_Drills)
        self.Athlete_12_Drillcheckbox.setGeometry(QtCore.QRect(480, 150, 21, 17))
        self.Athlete_12_Drillcheckbox.setText("")
        self.Athlete_12_Drillcheckbox.setObjectName("Athlete_12_Drillcheckbox")
        self.Athlete_12_Drillcheckbox.setDisabled(True)
        
        self.Athlete_13_Drillcheckbox = QtWidgets.QCheckBox(self.Tab_Drills)
        self.Athlete_13_Drillcheckbox.setGeometry(QtCore.QRect(480, 180, 21, 17))
        self.Athlete_13_Drillcheckbox.setText("")
        self.Athlete_13_Drillcheckbox.setObjectName("Athlete_13_Drillcheckbox")
        self.Athlete_13_Drillcheckbox.setDisabled(True)
        
        self.Athlete_14_Drillcheckbox = QtWidgets.QCheckBox(self.Tab_Drills)
        self.Athlete_14_Drillcheckbox.setGeometry(QtCore.QRect(480, 210, 21, 17))
        self.Athlete_14_Drillcheckbox.setText("")
        self.Athlete_14_Drillcheckbox.setObjectName("Athlete_14_Drillcheckbox")
        self.Athlete_14_Drillcheckbox.setDisabled(True)
        
######################################Labels #################################################################
        self.Illinois = QtWidgets.QLabel(self.Tab_Drills)
        self.Illinois.setGeometry(QtCore.QRect(420, 10, 71, 21))
        self.Illinois.setObjectName("Illinois Test")
       

        self.GK_1_label_Drills = QtWidgets.QLabel(self.Tab_Drills)
        self.GK_1_label_Drills.setGeometry(QtCore.QRect(420, 30, 71, 21))
        self.GK_1_label_Drills.setObjectName("GK1")
        
        self.WD_1_label_Drills = QtWidgets.QLabel(self.Tab_Drills)
        self.WD_1_label_Drills.setGeometry(QtCore.QRect(420, 60, 71, 21))
        self.WD_1_label_Drills.setObjectName("WD1")

        self.GD_1_label_Drills = QtWidgets.QLabel(self.Tab_Drills)
        self.GD_1_label_Drills.setGeometry(QtCore.QRect(420, 90, 71, 21))
        self.GD_1_label_Drills.setObjectName("GD1")

        self.C_1_label_Drills = QtWidgets.QLabel(self.Tab_Drills)
        self.C_1_label_Drills.setGeometry(QtCore.QRect(420, 120, 71, 21))
        self.C_1_label_Drills.setObjectName("C1")

        self.GA_1_label_Drills = QtWidgets.QLabel(self.Tab_Drills)
        self.GA_1_label_Drills.setGeometry(QtCore.QRect(420, 150, 71, 21))
        self.GA_1_label_Drills.setObjectName("GA1")

        self.WA_1_label_Drills = QtWidgets.QLabel(self.Tab_Drills)
        self.WA_1_label_Drills.setGeometry(QtCore.QRect(420, 180, 71, 21))
        self.WA_1_label_Drills.setObjectName("WA1")

        self.GS_1_label_Drills = QtWidgets.QLabel(self.Tab_Drills)
        self.GS_1_label_Drills.setGeometry(QtCore.QRect(420, 210, 71, 21))
        self.GS_1_label_Drills.setObjectName("GS1")

        self.GK_2_label_Drills = QtWidgets.QLabel(self.Tab_Drills)
        self.GK_2_label_Drills.setGeometry(QtCore.QRect(500, 30, 71, 21))
        self.GK_2_label_Drills.setObjectName("GK2")
        
        self.WD_2_label_Drills = QtWidgets.QLabel(self.Tab_Drills)
        self.WD_2_label_Drills.setGeometry(QtCore.QRect(500, 60, 71, 21))
        self.WD_2_label_Drills.setObjectName("WD2")

        self.GD_2_label_Drills = QtWidgets.QLabel(self.Tab_Drills)
        self.GD_2_label_Drills.setGeometry(QtCore.QRect(500, 90, 71, 21))
        self.GD_2_label_Drills.setObjectName("GD2")

        self.C_2_label_Drills = QtWidgets.QLabel(self.Tab_Drills)
        self.C_2_label_Drills.setGeometry(QtCore.QRect(500, 120, 71, 21))
        self.C_2_label_Drills.setObjectName("C2")

        self.GA_2_label_Drills = QtWidgets.QLabel(self.Tab_Drills)
        self.GA_2_label_Drills.setGeometry(QtCore.QRect(500, 150, 71, 21))
        self.GA_2_label_Drills.setObjectName("GA2")

        self.WA_2_label_Drills = QtWidgets.QLabel(self.Tab_Drills)
        self.WA_2_label_Drills.setGeometry(QtCore.QRect(500, 180, 71, 21))
        self.WA_2_label_Drills.setObjectName("WA2")

        self.GS_2_label_Drills = QtWidgets.QLabel(self.Tab_Drills)
        self.GS_2_label_Drills.setGeometry(QtCore.QRect(500, 210, 71, 21))
        self.GS_2_label_Drills.setObjectName("GS2")

#######################################Save PDF ################################################################################################################        
        self.Save_PDF_checkbox = QtWidgets.QCheckBox(self.Tab_Drills)
        self.Save_PDF_checkbox.setGeometry(QtCore.QRect(200, 490, 30, 31))
        self.Save_PDF_checkbox.setText("")
        self.Save_PDF_checkbox.setObjectName("Save_PDF")

        self.Save_PDF_label_Drills = QtWidgets.QLabel(self.Tab_Drills)
        self.Save_PDF_label_Drills.setGeometry(QtCore.QRect(225, 490, 160, 31))
        self.Save_PDF_label_Drills.setObjectName("Save_pdf_label")
        
#####################################################################################################################################################################
#####################################################################################################################################################################        
                                     # Tab_Results
                                     
######################################################################################################################
        self.File_List_Text_Results = QtWidgets.QListWidget(self.Tab_Results)
        self.File_List_Text_Results.setGeometry(QtCore.QRect(10,10,171, 201))
        self.File_List_Text_Results.setObjectName("File_List_Text")

######################################################################################################################
##################### View Data button ########################################################################### 
        self.View_Data_Button = QtWidgets.QPushButton(self.Tab_Results)
        self.View_Data_Button.setGeometry(QtCore.QRect(190, 175, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.View_Data_Button.setFont(font)
        self.View_Data_Button.setAutoDefault(False)
        self.View_Data_Button.setDefault(True)
        self.View_Data_Button.setFlat(False)
        self.View_Data_Button.setObjectName("Process_File_Button")
        self.View_Data_Button.clicked.connect(self.View_Data)
      
######################################################################################################################
      
##################### View Data button ########################################################################### 
        self.Open_Data_Button = QtWidgets.QPushButton(self.Tab_Results)
        self.Open_Data_Button.setGeometry(QtCore.QRect(10, 220, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.Open_Data_Button.setFont(font)
        self.Open_Data_Button.setAutoDefault(False)
        self.Open_Data_Button.setDefault(True)
        self.Open_Data_Button.setFlat(False)
        self.Open_Data_Button.setObjectName("Open_File_Button")
        self.Open_Data_Button.clicked.connect(self.Load_All_Files2)
      
######################################################################################################################
      
        self.Drill_twenty_checkbox = QtWidgets.QCheckBox(self.Tab_Results)
        self.Drill_twenty_checkbox.setGeometry(QtCore.QRect(190, 50, 21, 17))
        self.Drill_twenty_checkbox.setText("")
        self.Drill_twenty_checkbox.setObjectName("Drill_twenty_checkbox")
        
        
        self.illinois_checkbox = QtWidgets.QCheckBox(self.Tab_Results)
        self.illinois_checkbox.setGeometry(QtCore.QRect(190, 70, 21, 17))
        self.illinois_checkbox.setText("")
        self.illinois_checkbox.setObjectName("illinois_checkbox")
        
        self.YoYo_checkbox = QtWidgets.QCheckBox(self.Tab_Results)
        self.YoYo_checkbox.setGeometry(QtCore.QRect(190, 90, 21, 17))
        self.YoYo_checkbox.setText("")
        self.YoYo_checkbox.setObjectName("YoYo_checkbox")
        
        self.twenty_label = QtWidgets.QLabel(self.Tab_Results)
        self.twenty_label.setGeometry(QtCore.QRect(210, 50, 101, 21))
        self.twenty_label.setObjectName("20 m ")

        self.illinois_label = QtWidgets.QLabel(self.Tab_Results)
        self.illinois_label.setGeometry(QtCore.QRect(210, 70, 71, 21))
        self.illinois_label.setObjectName("Illinois_test")
        
        self.YoYo_label = QtWidgets.QLabel(self.Tab_Results)
        self.YoYo_label.setGeometry(QtCore.QRect(210, 90, 71, 21))
        self.YoYo_label.setObjectName("Yo-Yo")

        self.Drill_select_label = QtWidgets.QLabel(self.Tab_Results)
        self.Drill_select_label.setGeometry(QtCore.QRect(200, 10, 71, 21))
        self.Drill_select_label.setObjectName("Yo-Yo")
###################################################################################################################### 
        self.figure = plt.figure(figsize=(8,6))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.Tab_Results)
        self.canvas.move(400,1)
        self.toolbar = NavigationToolbar(self.canvas, self.Tab_Results)
        self.toolbar.move(100,550)

############################### Table creation ############################################################################        
        self.tableWidget = QtWidgets.QTableWidget(self.Tab_Results)
        self.tableWidget.setGeometry(QtCore.QRect(10, 270, 350, 280))
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(5)

##########################################   Close button ############################################################
        
        self.Close_button_Results = QtWidgets.QPushButton(self.Tab_Results)
        self.Close_button_Results.setGeometry(QtCore.QRect(10, 560, 75, 23))
        self.Close_button_Results.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.Close_button_Results.setFlat(False)
        self.Close_button_Results.setObjectName("Close_button")
        self.Close_button_Results.clicked.connect(self.Close_Results)
######################################################################################################################        
        self.Athlete_7_Drillcheckbox.raise_()
        self.Athlete_8_Drillcheckbox.raise_()
        self.Athlete_9_Drillcheckbox.raise_()
        self.Athlete_10_Drillcheckbox.raise_()
        self.Athlete_11_Drillcheckbox.raise_()
        self.Athlete_12_Drillcheckbox.raise_()
        self.Athlete_13_Drillcheckbox.raise_()
        self.Athlete_14_Drillcheckbox.raise_()
        self.retranslateUi(Dialog)
        self.parent_tabWidget.setCurrentIndex(0)
       
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.displayImage()       

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Save_location_button.setText(_translate("Dialog", "Save Location"))
        self.Save_location_Drills_button.setText(_translate("Dialog", "Save Location"))
        self.Close_button.setText(_translate("Dialog", "Close"))
        self.Arm_button.setText(_translate("Dialog", "Record/Stop"))
        self.New_File_button.setText(_translate("Dialog","New File"))
        self.T1_Score_button.setText(_translate("Dialog","T1 Score"))
        self.T2_Score_button.setText(_translate("Dialog","T2 Score"))
        self.Connect_button.setText(_translate("Dialog","POZYX connect"))
        self.GK_1_label.setText(_translate("Dialog","GK1"))
        self.WD_1_label.setText(_translate("Dialog","WD1"))
        self.GD_1_label.setText(_translate("Dialog","GD1"))
        self.C_1_label.setText(_translate("Dialog","C1"))
        self.GA_1_label.setText(_translate("Dialog","GA1"))
        self.WA_1_label.setText(_translate("Dialog","WA1"))
        self.GS_1_label.setText(_translate("Dialog","GS1"))
        self.GK_2_label.setText(_translate("Dialog","GK2"))
        self.WD_2_label.setText(_translate("Dialog","WD2"))
        self.GD_2_label.setText(_translate("Dialog","GD2"))
        self.C_2_label.setText(_translate("Dialog","C2"))
        self.GA_2_label.setText(_translate("Dialog","GA2"))
        self.WA_2_label.setText(_translate("Dialog","WA2"))
        self.GS_2_label.setText(_translate("Dialog","GS2"))
        self.Team1_label.setText(_translate("Dialog","Team 1 (Red)"))
        self.Team2_label.setText(_translate("Dialog","Team 2 (Blue)"))
        self.Tag_update.setText(_translate("Dialog","Update Tags"))
        self.DisConnect_button.setText(_translate("Dialog","POZYX Disconnect"))        
        self.Sub_Choice.setItemText(0, _translate("Dialog", "Choose Player"))
        self.Sub_Choice.setItemText(1, _translate("Dialog", "GK1"))
        self.Sub_Choice.setItemText(2, _translate("Dialog", "WD1"))
        self.Sub_Choice.setItemText(3, _translate("Dialog", "GD1"))
        self.Sub_Choice.setItemText(4, _translate("Dialog", "C1"))
        self.Sub_Choice.setItemText(5, _translate("Dialog", "GA1"))
        self.Sub_Choice.setItemText(6, _translate("Dialog", "WA1"))
        self.Sub_Choice.setItemText(7, _translate("Dialog", "GS1"))
        self.Sub_Choice.setItemText(8, _translate("Dialog", "GK2"))
        self.Sub_Choice.setItemText(9, _translate("Dialog", "WD2"))
        self.Sub_Choice.setItemText(10, _translate("Dialog", "GD2"))
        self.Sub_Choice.setItemText(11, _translate("Dialog", "C2"))
        self.Sub_Choice.setItemText(12, _translate("Dialog", "GA2"))
        self.Sub_Choice.setItemText(13, _translate("Dialog", "WA2"))
        self.Sub_Choice.setItemText(14, _translate("Dialog", "GS2"))
        self.Substitution_button.setText(_translate("Dialog","Substitution"))
        self.Tag_Set.setText(_translate("Dialog","Set Tags"))
        self.parent_tabWidget.setTabText(self.parent_tabWidget.indexOf(self.Tab_Game), _translate("Dialog", "Game"))
        self.parent_tabWidget.setTabText(self.parent_tabWidget.indexOf(self.Tab_Drills), _translate("Dialog", "Drills"))
        self.parent_tabWidget.setTabText(self.parent_tabWidget.indexOf(self.Tab_Results), _translate("Dialog", "Results"))
        self.Drill_Choice.setItemText(0, _translate("Dialog", "Choose Drill"))
        self.Drill_Choice.setItemText(1, _translate("Dialog", "20m Sprints"))
        self.Drill_Choice.setItemText(2, _translate("Dialog", "Illinos"))
        self.Drill_Choice.setItemText(3, _translate("Dialog", "Yo-Yo"))
        self.Position_Choice.setItemText(0, _translate("Dialog", "Choose Player"))
        self.Position_Choice.setItemText(1, _translate("Dialog", "GK1"))
        self.Position_Choice.setItemText(2, _translate("Dialog", "WD1"))
        self.Position_Choice.setItemText(3, _translate("Dialog", "GD1"))
        self.Position_Choice.setItemText(4, _translate("Dialog", "C1"))
        self.Position_Choice.setItemText(5, _translate("Dialog", "GA1"))
        self.Position_Choice.setItemText(6, _translate("Dialog", "WA1"))
        self.Position_Choice.setItemText(7, _translate("Dialog", "GS1"))
        self.Position_Choice.setItemText(8, _translate("Dialog", "GK2"))
        self.Position_Choice.setItemText(9, _translate("Dialog", "WD2"))
        self.Position_Choice.setItemText(10, _translate("Dialog", "GD2"))
        self.Position_Choice.setItemText(11, _translate("Dialog", "C2"))
        self.Position_Choice.setItemText(12, _translate("Dialog", "GA2"))
        self.Position_Choice.setItemText(13, _translate("Dialog", "WA2"))
        self.Position_Choice.setItemText(14, _translate("Dialog", "GS2"))
        self.Set_Tag.setText(_translate("Dialog","Set player/file number"))
        self.Set_Drill.setText(_translate("Dialog","Set Drill"))
        self.Connect_button_Drills.setText(_translate("Dialog","POZYX connect"))
        self.GK_1_label_Drills.setText(_translate("Dialog","GK1"))
        self.WD_1_label_Drills.setText(_translate("Dialog","WD1"))
        self.GD_1_label_Drills.setText(_translate("Dialog","GD1"))
        self.C_1_label_Drills.setText(_translate("Dialog","C1"))
        self.GA_1_label_Drills.setText(_translate("Dialog","GA1"))
        self.WA_1_label_Drills.setText(_translate("Dialog","WA1"))
        self.GS_1_label_Drills.setText(_translate("Dialog","GS1"))
        self.GK_2_label_Drills.setText(_translate("Dialog","GK2"))
        self.WD_2_label_Drills.setText(_translate("Dialog","WD2"))
        self.GD_2_label_Drills.setText(_translate("Dialog","GD2"))
        self.C_2_label_Drills.setText(_translate("Dialog","C2"))
        self.GA_2_label_Drills.setText(_translate("Dialog","GA2"))
        self.WA_2_label_Drills.setText(_translate("Dialog","WA2"))
        self.GS_2_label_Drills.setText(_translate("Dialog","GS2"))
        self.Illinois.setText(_translate("Dialog","Yo-Yo Test"))
        self.Arm_button_Drills.setText(_translate("Dialog", "Record/Stop"))
        self.Tag_update_Drills.setText(_translate("Dialog", "Update Tags"))
        self.Load_Files_Button.setText(_translate("Dialog", "Load Files"))
        self.Close_button_Drills.setText(_translate("Dialog", "Close"))
        self.Process_File_Button.setText(_translate("Dialog", "Process"))
        self.DisConnect_button_Drills.setText(_translate("Dialog", "POZYX Disconnect"))
        self.Filenumber_Choice.setItemText(0, _translate("Dialog", "1"))
        self.Filenumber_Choice.setItemText(1, _translate("Dialog", "2"))
        self.Filenumber_Choice.setItemText(2, _translate("Dialog", "3"))
        self.Filenumber_Choice.setItemText(3, _translate("Dialog", "4"))
        self.Filenumber_Choice.setItemText(4, _translate("Dialog", "5"))
        self.Filenumber_Choice.setItemText(5, _translate("Dialog", "6"))
        self.Filenumber_Choice.setItemText(6, _translate("Dialog", "7"))
        self.Filenumber_Choice.setItemText(7, _translate("Dialog", "8"))
        self.Filenumber_Choice.setItemText(8, _translate("Dialog", "9"))
        self.Filenumber_Choice.setItemText(9, _translate("Dialog", "10"))
        self.Filenumber_label.setText(_translate("Dialog","File Number"))
        self.Tag_set_Drills.setText(_translate("Dialog","Set Tags"))
        self.Save_PDF_label_Drills.setText(_translate("Dialog","Export Game to PDF"))

        self.twenty_label.setText(_translate("Dialog","20 metre sprint"))
        self.illinois_label.setText(_translate("Dialog","Illinois"))
        self.YoYo_label.setText(_translate("Dialog","Yo-Yo"))
        self.Drill_select_label.setText(_translate("Dialog","Select Drill"))
        self.View_Data_Button.setText(_translate("Dialog","View Data"))
        self.Open_Data_Button.setText(_translate("Dialog","Set Folder"))
        self.Close_button_Results.setText(_translate("Dialog","Close"))
    
    def tag_check(self):
        global topic1;global connected;global tags;global game_display;global Athlete_1_checkbox;
        global Athlete_2_checkbox;global Athlete_3_checkbox;global Athlete_4_checkbox;
        global Athlete_5_checkbox;global Athlete_6_checkbox;global Athlete_7_checkbox;
        global Athlete_11_checkbox;global Athlete_12_checkbox;global Athlete_13_checkbox;
        global Athlete_14_checkbox;global Athlete_15_checkbox;global Athlete_16_checkbox;
        global Athlete_17_checkbox;
        global coordinates_x;global coordinates_y; global coordinates_z
        global coordinates_x_Tag1;global coordinates_y_Tag1; global coordinates_z_Tag1
        global coordinates_x_Tag2; global coordinates_y_Tag2; global coordinates_z_Tag2
        global coordinates_x_Tag3; global coordinates_y_Tag3; global coordinates_z_Tag3
        global coordinates_x_Tag4; global coordinates_y_Tag4; global coordinates_z_Tag4
        global coordinates_x_Tag5; global coordinates_y_Tag5; global coordinates_z_Tag5
        global coordinates_x_Tag6; global coordinates_y_Tag6; global coordinates_z_Tag6
        global coordinates_x_Tag7; global coordinates_y_Tag7; global coordinates_z_Tag7
        global coordinates_x_Tag8; global coordinates_y_Tag8; global coordinates_z_Tag8
        global coordinates_x_Tag9; global coordinates_y_Tag9; global coordinates_z_Tag9
        global coordinates_x_Tag10; global coordinates_y_Tag10; global coordinates_z_Tag10
        global coordinates_x_Tag11; global coordinates_y_Tag11; global coordinates_z_Tag11
        global coordinates_x_Tag12; global coordinates_y_Tag12; global coordinates_z_Tag12
        global coordinates_x_Tag13; global coordinates_y_Tag13; global coordinates_z_Tag13
        global coordinates_x_Tag14; global coordinates_y_Tag14; global coordinates_z_Tag14
        global coordinates_x_Tag15; global coordinates_y_Tag15; global coordinates_z_Tag15
        global GK1_Game;global GK1_Drill;global WD1_Game;global WD1_Drill;
        global GD1_Game;global GD1_Drill;global C1_Game;global C1_Drill;
        global GA1_Game;global GA1_Drill;global WA1_Game;global WA1_Drill;
        global GS1_Game;global GS1_Drill;global GK2_Game;global GK2_Drill;
        global WD2_Game;global WD2_Drill;global GD2_Game;global GD2_Drill;
        global C2_Game;global C2_Drill;global GA2_Game;global GA2_Drill;
        global WA2_Game;global WA2_Drill;global GS2_Game;global GS2_Drill; global tags; global tag_ids;
        global worksheet_Coordinates;global worksheet_Coordinates_Tag1;global worksheet_Coordinates_Tag2;global worksheet_Coordinates_Tag3;
        global worksheet_Coordinates_Tag4;global worksheet_Coordinates_Tag5;global worksheet_Coordinates_Tag6;global worksheet_Coordinates_Tag7;
        global worksheet_Coordinates_Tag8;global worksheet_Coordinates_Tag9;global worksheet_Coordinates_Tag10;global worksheet_Coordinates_Tag11;
        global worksheet_Coordinates_Tag12;global worksheet_Coordinates_Tag13;global worksheet_Coordinates_Tag14;global worksheet_Coordinates_Tag15;
        global outputfile;global game_display; global Graphic; global Track_graphic; global Drills_Graphic; global output_value

        
        if self.parent_tabWidget.currentIndex()==0:
            Athlete_1_checkbox =self.Athlete_1_checkbox.isChecked()
            Athlete_2_checkbox =self.Athlete_2_checkbox.isChecked()
            Athlete_3_checkbox =self.Athlete_3_checkbox.isChecked()
            Athlete_4_checkbox =self.Athlete_4_checkbox.isChecked()
            Athlete_5_checkbox =self.Athlete_5_checkbox.isChecked()
            Athlete_6_checkbox =self.Athlete_6_checkbox.isChecked()
            Athlete_7_checkbox =self.Athlete_7_checkbox.isChecked()
            Athlete_11_checkbox =self.Athlete_11_checkbox.isChecked()
            Athlete_12_checkbox =self.Athlete_12_checkbox.isChecked()
            Athlete_13_checkbox =self.Athlete_13_checkbox.isChecked()
            Athlete_14_checkbox =self.Athlete_14_checkbox.isChecked()
            Athlete_15_checkbox =self.Athlete_15_checkbox.isChecked()
            Athlete_16_checkbox =self.Athlete_16_checkbox.isChecked()
            Athlete_17_checkbox =self.Athlete_17_checkbox.isChecked()
            if Athlete_1_checkbox is True:
                GK1_Game=1
            else:
                GK1_Game=0
            if Athlete_2_checkbox is True:
                WD1_Game=2
            else:
                WD1_Game=0
            if Athlete_3_checkbox is True:
               GD1_Game =3
            else:
                GD1_Game=0
            if Athlete_4_checkbox is True:
                C1_Game=4
            else:
                C1_Game=0
            if Athlete_5_checkbox is True:
                GA1_Game=5
            else:
                GA1_Game=0
            if Athlete_6_checkbox is True:
                WA1_Game=6
            else:
                WA1_Game=0
            if Athlete_7_checkbox is True:
                GS1_Game=7
            else:
                GS1_Game=0
            if Athlete_11_checkbox is True:
                GK2_Game=8
            else:
                GK2_Game=0
            if Athlete_12_checkbox is True:
                WD2_Game=9
            else:
                WD2_Game=0
            if Athlete_13_checkbox is True:
                GD2_Game=10
            else:
                GD2_Game=0
            if Athlete_14_checkbox is True:
                C2_Game=11
            else:
                C2_Game=0
            if Athlete_15_checkbox is True:
                GA2_Game=12
            else:
                GA2_Game=0
            if Athlete_16_checkbox is True:
                WA2_Game=13
            else:
                WA2_Game=0
            if Athlete_17_checkbox is True:
                GS2_Game=14
            else:
                GS2_Game=0
            tag_ids=[GK1_Game,WD1_Game,GD1_Game,C1_Game,GA1_Game,WA1_Game,GS1_Game,GK2_Game,WD2_Game,GD2_Game,C2_Game,GA2_Game,WA2_Game,GS2_Game]
            tag_ids[:] = (value for value in tag_ids if value != 0)
            tags = [PozyxTag(tag_id) for tag_id in tag_ids]
            print(tag_ids)
                
        elif self.parent_tabWidget.currentIndex()==1:
            Athlete_1_Drill_checkbox =self.Athlete_1_Drillcheckbox.isChecked()
            Athlete_2_Drill_checkbox =self.Athlete_2_Drillcheckbox.isChecked()
            Athlete_3_Drill_checkbox =self.Athlete_3_Drillcheckbox.isChecked()
            Athlete_4_Drill_checkbox =self.Athlete_4_Drillcheckbox.isChecked()
            Athlete_5_Drill_checkbox =self.Athlete_5_Drillcheckbox.isChecked()
            Athlete_6_Drill_checkbox =self.Athlete_6_Drillcheckbox.isChecked()
            Athlete_7_Drill_checkbox =self.Athlete_7_Drillcheckbox.isChecked()
            Athlete_8_Drill_checkbox =self.Athlete_8_Drillcheckbox.isChecked()
            Athlete_9_Drill_checkbox =self.Athlete_9_Drillcheckbox.isChecked()
            Athlete_10_Drill_checkbox =self.Athlete_10_Drillcheckbox.isChecked()
            Athlete_11_Drill_checkbox =self.Athlete_11_Drillcheckbox.isChecked()
            Athlete_12_Drill_checkbox =self.Athlete_12_Drillcheckbox.isChecked()
            Athlete_13_Drill_checkbox =self.Athlete_13_Drillcheckbox.isChecked()
            Athlete_14_Drill_checkbox =self.Athlete_14_Drillcheckbox.isChecked()
            if Athlete_1_Drill_checkbox is True:
                GK1_Drill=1
            else:
                GK1_Drill=0
            if Athlete_2_Drill_checkbox is True:
                WD1_Drill=2
            else:
                WD1_Drill=0
            if Athlete_3_Drill_checkbox is True:
                GD1_Drill=3
            else:
                GD1_Drill=0
            if Athlete_4_Drill_checkbox is True:
                C1_Drill=4
            else:
                C1_Drill=0
            if Athlete_5_Drill_checkbox is True:
                GA1_Drill=5
            else:
                GA1_Drill=0
            if Athlete_6_Drill_checkbox is True:
                WA1_Drill=6
            else:
                WA1_Drill=0
            if Athlete_7_Drill_checkbox is True:
                GS1_Drill=7
            else:
                GS1_Drill=0
            if Athlete_8_Drill_checkbox is True:
                GK2_Drill=8
            else:
                GK2_Drill=0
            if Athlete_9_Drill_checkbox is True:
                WD2_Drill=9
            else:
                WD2_Drill=0
            if Athlete_10_Drill_checkbox is True:
                GD2_Drill=10
            else:
                GD2_Drill=0
            if Athlete_11_Drill_checkbox is True:
                C2_Drill=11
            else:
                C2_Drill=0
            if Athlete_12_Drill_checkbox is True:
                GA2_Drill=12
            else:
                GA2_Drill=0
            if Athlete_13_Drill_checkbox is True:
                WA2_Drill=13
            else:
                WA2_Drill=0
            if Athlete_14_Drill_checkbox is True:
                GS2_Drill=14
            else:
                GS2_Drill=0
            if self.Drill_Choice.currentIndex()==3:
                tag_ids=[GK1_Drill,WD1_Drill,GD1_Drill,C1_Drill,GA1_Drill,WA1_Drill,GS1_Drill,GK2_Drill,WD2_Drill,GD2_Drill,C2_Drill,GA2_Drill,WA2_Drill,GS2_Drill]
                tag_ids[:] = (value for value in tag_ids if value != 0)
                tags = [PozyxTag(tag_id) for tag_id in tag_ids]
                print(tag_ids)
                

            messagebox.showinfo('success', 'Updated')
          
############################################################################################################################################

############################################################################################################################################
############################################################################################################################################

                 
    def POZYX_connect(self):
        global topic1;global connected;global tags;global game_display;global Athlete_1_checkbox;
        global Athlete_2_checkbox;global Athlete_3_checkbox;global Athlete_4_checkbox;
        global Athlete_5_checkbox;global Athlete_6_checkbox;global Athlete_7_checkbox;
        global Athlete_11_checkbox;global Athlete_12_checkbox;global Athlete_13_checkbox;
        global Athlete_14_checkbox;global Athlete_15_checkbox;global Athlete_16_checkbox;
        global Athlete_17_checkbox; global update_count;
        global GK1_Game;global GK1_Drill;global WD1_Game;global WD1_Drill;
        global GD1_Game;global GD1_Drill;global C1_Game;global C1_Drill;
        global GA1_Game;global GA1_Drill;global WA1_Game;global WA1_Drill;
        global GS1_Game;global GS1_Drill;global GK2_Game;global GK2_Drill;
        global WD2_Game;global WD2_Drill;global GD2_Game;global GD2_Drill;
        global C2_Game;global C2_Drill;global GA2_Game;global GA2_Drill;
        global WA2_Game;global WA2_Drill;global GS2_Game;global GS2_Drill;
        global Graphic; global Drills_Graphic; global Track_graphic; global tab_Game; global tag_ids; global tags
        global Athlete_1_Drill_checkbox; global Athlete_2_Drill_checkbox; global Athlete_3_Drill_checkbox; global Athlete_4_Drill_checkbox;
        global Athlete_5_Drill_checkbox; global Athlete_6_Drill_checkbox; global Athlete_7_Drill_checkbox; global Athlete_8_Drill_checkbox;
        global Athlete_9_Drill_checkbox; global Athlete_10_Drill_checkbox; global Athlete_11_Drill_checkbox; global Athlete_12_Drill_checkbox;
        global Athlete_13_Drill_checkbox; global Athlete_14_Drill_checkbox;
        global Output_file_directory;global Out_img;global out1;global img; global outputfile
        global fourcc;global video;global file;global file_1; global close_1;global New_Trial_1;
        global game_display; global Graphic; global Track_graphic; global Drills_Graphic; global output_value;global reconnect;global remainder3;
        global remainder2
        clientloop=0
        update_count=0
        reconnect=0
        remainder3=0
        remainder2=0
        
        if self.parent_tabWidget.currentIndex()==0:
            tab_Game=1
            Athlete_1_checkbox =self.Athlete_1_checkbox.isChecked()           
            Athlete_2_checkbox =self.Athlete_2_checkbox.isChecked()
            Athlete_3_checkbox =self.Athlete_3_checkbox.isChecked()
            Athlete_4_checkbox =self.Athlete_4_checkbox.isChecked()
            Athlete_5_checkbox =self.Athlete_5_checkbox.isChecked()
            Athlete_6_checkbox =self.Athlete_6_checkbox.isChecked()
            Athlete_7_checkbox =self.Athlete_7_checkbox.isChecked()
            Athlete_11_checkbox =self.Athlete_11_checkbox.isChecked()
            Athlete_12_checkbox =self.Athlete_12_checkbox.isChecked()
            Athlete_13_checkbox =self.Athlete_13_checkbox.isChecked()
            Athlete_14_checkbox =self.Athlete_14_checkbox.isChecked()
            Athlete_15_checkbox =self.Athlete_15_checkbox.isChecked()
            Athlete_16_checkbox =self.Athlete_16_checkbox.isChecked()
            Athlete_17_checkbox =self.Athlete_17_checkbox.isChecked()
            if Athlete_1_checkbox is True:
                GK1_Game=1
            if Athlete_2_checkbox is True:
                WD1_Game=2
            if Athlete_3_checkbox is True:
                GD1_Game=3
            if Athlete_4_checkbox is True:
                C1_Game=4
            if Athlete_5_checkbox is True:
                GA1_Game=5
            if Athlete_6_checkbox is True:
                WA1_Game=6
            if Athlete_7_checkbox is True:
                GS1_Game=7
            if Athlete_11_checkbox is True:
                GK2_Game=8
            if Athlete_12_checkbox is True:
                WD2_Game=9
            if Athlete_13_checkbox is True:
                GD2_Game=10
            if Athlete_14_checkbox is True:
                C2_Game=11
            if Athlete_15_checkbox is True:
                GA2_Game=12
            if Athlete_16_checkbox is True:
                WA2_Game=13
            if Athlete_17_checkbox is True:
                GS2_Game=14            
            tag_ids=[GK1_Game,WD1_Game,GD1_Game,C1_Game,GA1_Game,WA1_Game,GS1_Game,GK2_Game,WD2_Game,GD2_Game,C2_Game,GA2_Game,WA2_Game,GS2_Game]
            tag_ids[:] = (value for value in tag_ids if value != 0)
            tags = [PozyxTag(tag_id) for tag_id in tag_ids]
            print(tag_ids)
                       
            
            Graphic=Track_graphic
            self.client.loop_start()
            
            time.sleep(.5)   
                 
            while topic1 is 1:
                    connected = 1
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showinfo('success', 'POZYX connected')
                    clientloop=1
                    break;
#            self.client.loop_forever()
            
        elif self.parent_tabWidget.currentIndex()==1:
            tab_Game=2
            Athlete_1_Drill_checkbox =self.Athlete_1_Drillcheckbox.isChecked()
            Athlete_2_Drill_checkbox =self.Athlete_2_Drillcheckbox.isChecked()
            Athlete_3_Drill_checkbox =self.Athlete_3_Drillcheckbox.isChecked()
            Athlete_4_Drill_checkbox =self.Athlete_4_Drillcheckbox.isChecked()
            Athlete_5_Drill_checkbox =self.Athlete_5_Drillcheckbox.isChecked()
            Athlete_6_Drill_checkbox =self.Athlete_6_Drillcheckbox.isChecked()
            Athlete_7_Drill_checkbox =self.Athlete_7_Drillcheckbox.isChecked()
            Athlete_8_Drill_checkbox =self.Athlete_8_Drillcheckbox.isChecked()
            Athlete_9_Drill_checkbox =self.Athlete_9_Drillcheckbox.isChecked()
            Athlete_10_Drill_checkbox =self.Athlete_10_Drillcheckbox.isChecked()
            Athlete_11_Drill_checkbox =self.Athlete_11_Drillcheckbox.isChecked()
            Athlete_12_Drill_checkbox =self.Athlete_12_Drillcheckbox.isChecked()
            Athlete_13_Drill_checkbox =self.Athlete_13_Drillcheckbox.isChecked()
            Athlete_14_Drill_checkbox =self.Athlete_14_Drillcheckbox.isChecked()
            
            if Athlete_1_Drill_checkbox is True:
                GK1_Drill=1
            if Athlete_2_Drill_checkbox is True:
                WD1_Drill=2
            if Athlete_3_Drill_checkbox is True:
                GD1_Drill=3
            if Athlete_4_Drill_checkbox is True:
                C1_Drill=4
            if Athlete_5_Drill_checkbox is True:
                GA1_Drill=5
            if Athlete_6_Drill_checkbox is True:
                WA1_Drill=6
            if Athlete_7_Drill_checkbox is True:
                GS1_Drill=7
            if Athlete_8_Drill_checkbox is True:
                GK2_Drill=8
            if Athlete_9_Drill_checkbox is True:
                WD2_Drill=9
            if Athlete_10_Drill_checkbox is True:
                GD2_Drill=10
            if Athlete_11_Drill_checkbox is True:
                C2_Drill=11
            if Athlete_12_Drill_checkbox is True:
                GA2_Drill=12
            if Athlete_13_Drill_checkbox is True:
                WA2_Drill=13
            if Athlete_14_Drill_checkbox is True:
                GS2_Drill=14
            if self.Drill_Choice.currentIndex()==3:
                tag_ids=[GK1_Drill,WD1_Drill,GD1_Drill,C1_Drill,GA1_Drill,WA1_Drill,GS1_Drill,GK2_Drill,WD2_Drill,GD2_Drill,C2_Drill,GA2_Drill,WA2_Drill,GS2_Drill]
                tag_ids[:] = (value for value in tag_ids if value != 0)
                tags = [PozyxTag(tag_id) for tag_id in tag_ids]
                print(tag_ids)
                
            Graphic=Drills_Graphic
            self.client.loop_start()
            
            time.sleep(.5)   
                 
            while topic1 is 1:
                    connected = 1
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showinfo('success', 'POZYX connected')
                    break;
    #        self.client.loop_forever()

            

    def on_message(client, userdata, msg):
        global coordinates_x;global coordinates_y; global coordinates_z;
        global coordinates_x_Tag2; global coordinates_y_Tag2; global coordinates_z_Tag2;
        global coordinates_x_Tag3; global coordinates_y_Tag3; global coordinates_z_Tag3;
        global coordinates_x_Tag4; global coordinates_y_Tag4; global coordinates_z_Tag4;
        global coordinates_x_Tag5; global coordinates_y_Tag5; global coordinates_z_Tag5;
        global coordinates_x_Tag6; global coordinates_y_Tag6; global coordinates_z_Tag6;
        global coordinates_x_Tag7; global coordinates_y_Tag7; global coordinates_z_Tag7;
        global coordinates_x_Tag8; global coordinates_y_Tag8; global coordinates_z_Tag8;
        global coordinates_x_Tag9; global coordinates_y_Tag9; global coordinates_z_Tag9;
        global coordinates_x_Tag10; global coordinates_y_Tag10; global coordinates_z_Tag10;
        global coordinates_x_Tag11; global coordinates_y_Tag11; global coordinates_z_Tag11;
        global coordinates_x_Tag12; global coordinates_y_Tag12; global coordinates_z_Tag12;
        global coordinates_x_Tag13; global coordinates_y_Tag13; global coordinates_z_Tag13;
        global coordinates_x_Tag14; global coordinates_y_Tag14; global coordinates_z_Tag14;
        global coordinates_x_Tag15; global coordinates_y_Tag15; global coordinates_z_Tag15;
        global worksheet_Coordinates;global worksheet_Coordinates_Tag1;global worksheet_Coordinates_Tag2;global worksheet_Coordinates_Tag3;
        global worksheet_Coordinates_Tag4;global worksheet_Coordinates_Tag5;global worksheet_Coordinates_Tag6;global worksheet_Coordinates_Tag7;
        global worksheet_Coordinates_Tag8;global worksheet_Coordinates_Tag9;global worksheet_Coordinates_Tag10;global worksheet_Coordinates_Tag11;
        global worksheet_Coordinates_Tag12;global worksheet_Coordinates_Tag13;global worksheet_Coordinates_Tag14;global worksheet_Coordinates_Tag15;
        global Tag1; global Tag2; global Tag3; global Tag4;global Tag5;global Tag6;global Tag7;global Tag8;global Tag9;global Tag10;global Tag11;global Tag12;
        global Tag13;global Tag14;global Tag15;
        global Tag_1_visible; global Tag_2_visible; global Tag_3_visible; global Tag_4_visible;global Tag_5_visible;global Tag_6_visible;global Tag_7_visible
        global Tag_8_visible;global Tag_9_visible;global Tag_10_visible;global Tag_11_visible;global Tag_12_visible;global Tag_13_visible;global Tag_14_visible;
        global Tag_15_visible;
        global second;global timestamp2;global counter;global record;global row;global column;global connected;global coordinates_exists
        global flag;global b;global a;global Filter_type;global tags;global data_exists;
        global Athlete_1_checkbox;global Athlete_2_checkbox;global Athlete_3_checkbox;global Athlete_4_checkbox;
        global Athlete_5_checkbox;global Athlete_6_checkbox;global Athlete_7_checkbox;
        global Athlete_11_checkbox;global Athlete_12_checkbox;global Athlete_13_checkbox;
        global Athlete_14_checkbox;global Athlete_15_checkbox;global Athlete_16_checkbox;
        global Athlete_17_checkbox; global outputfile;global file_1;global file_2;global New_trial; global New_trial_1; global file; global output_value;
        global pygame; global game_display; global clock; global SCREEN_WIDTH; global SCREEN_HEIGHT; global tag_ids; global tag_data; global tags; global clock;
        global coordinates_x_plot; global coordinates_y_plot;global x; global y; global floorplan; global update_count; global text; global game_display2; global t3;
        global out1; global videosave; global tab_Game; global player;
        global Athlete_1_Drill_checkbox; global Athlete_2_Drill_checkbox; global Athlete_3_Drill_checkbox; global Athlete_4_Drill_checkbox;
        global Athlete_5_Drill_checkbox; global Athlete_6_Drill_checkbox; global Athlete_7_Drill_checkbox; global Athlete_8_Drill_checkbox;
        global Athlete_9_Drill_checkbox; global Athlete_10_Drill_checkbox; global Athlete_11_Drill_checkbox; global Athlete_12_Drill_checkbox; global save;
        global Athlete_13_Drill_checkbox; global Athlete_14_Drill_checkbox;
        global GK1_Game;global GK1_Drill;global WD1_Game;global WD1_Drill;
        global GD1_Game;global GD1_Drill;global C1_Game;global C1_Drill;
        global GA1_Game;global GA1_Drill;global WA1_Game;global WA1_Drill;
        global GS1_Game;global GS1_Drill;global GK2_Game;global GK2_Drill;
        global WD2_Game;global WD2_Drill;global GD2_Game;global GD2_Drill;
        global C2_Game;global C2_Drill;global GA2_Game;global GA2_Drill;
        global WA2_Game;global WA2_Drill;global GS2_Game;global GS2_Drill;
        global Graphic; global Track_graphic; global Drills_Graphic; global record_counter; global Picture_Display; global end_Tag_counter;
        global remainder3; global remainder2; global data_record

        
    ############ Json Data #######################
        tag_data = json.loads(msg.payload.decode())
    #    print (tag_data)
        try:
            tagId = tag_data["tagId"]
            tagId=int(tagId)
            data = tag_data["data"]["coordinates"]
            data_exists = 1
        except KeyError:
            data_exists = 0
          
        dt = datetime.now()
        second = dt.second
        microseond = dt.microsecond        
        
       # remainder3=0
    
    ## Data ##
        if data_record==1: # first tab                         # second tab
            for tag in tags:
                if data_exists == 1:
                    update_count=update_count+1
                    coordinates_plot=data
                    while tagId == tag.id: 
                            coordinates_x_plot =(coordinates_plot["x"])
                            coordinates_y_plot =(coordinates_plot["y"])
                            text=str(tag.id)
                            tag.set_position(coordinates_x_plot,coordinates_y_plot)
                            tag.display()
                            break;
                    if update_count==50:
                       game_display.blit(floorplan, [0, 0])
                       update_count=0
                else:
                    pass

            record_counter +=1

#        print("R",record_counter)
        
    ## Coordinates ##
        if data_exists is 1:   
              if tab_Game==1:
                  if Athlete_1_checkbox is True:
                    while tagId == 1:
                        coordinates =data
                        coordinates_x =(coordinates["x"])
                        coordinates_y =(coordinates["y"])
                        coordinates_z =(coordinates["z"])
                  #      print (tagId,coordinates_x,coordinates_y)
                        break;
                  if Athlete_2_checkbox is True:
                    while tagId == 2:
                        coordinates_Tag2 =data
                        coordinates_x_Tag2 =(coordinates_Tag2["x"])
                        coordinates_y_Tag2 =(coordinates_Tag2["y"])
                        coordinates_z_Tag2 =(coordinates_Tag2["z"])
                        #print (coordinates_x_Tag2)
                        break;    
                  if Athlete_3_checkbox is True:
                    while tagId == 3:
                        coordinates_Tag3 =data
                        coordinates_x_Tag3 =(coordinates_Tag3["x"])
                        coordinates_y_Tag3 =(coordinates_Tag3["y"])
                        coordinates_z_Tag3 =(coordinates_Tag3["z"])
                        #print (coordinates_x_Tag3)
                        break;
                   
                  if Athlete_4_checkbox is True:
                    while tagId == 4:
                        coordinates_Tag4 =data
                        coordinates_x_Tag4 =(coordinates_Tag4["x"])
                        coordinates_y_Tag4 =(coordinates_Tag4["y"])
                        coordinates_z_Tag4 =(coordinates_Tag4["z"])
                        #print (coordinates_x_Tag4)
                        break;

                  if Athlete_5_checkbox is True:
                    while tagId == 5:
                        coordinates_Tag5 =data
                        coordinates_x_Tag5 =(coordinates_Tag5["x"])
                        coordinates_y_Tag5 =(coordinates_Tag5["y"])
                        coordinates_z_Tag5 =(coordinates_Tag5["z"])
                        #print (coordinates_x_Tag5)
                        break;   

                  if Athlete_6_checkbox is True:
                    while tagId == 6:
                        coordinates_Tag6 =data
                        coordinates_x_Tag6 =(coordinates_Tag6["x"])
                        coordinates_y_Tag6 =(coordinates_Tag6["y"])
                        coordinates_z_Tag6 =(coordinates_Tag6["z"])
                        #print (coordinates_x_Tag6)
                        break;   

                  if Athlete_7_checkbox is True:
                    while tagId == 7:                        
                        coordinates_Tag7 =data
                        coordinates_x_Tag7 =(coordinates_Tag7["x"])
                        coordinates_y_Tag7 =(coordinates_Tag7["y"])
                        coordinates_z_Tag7 =(coordinates_Tag7["z"])
                        #print (coordinates_x_Tag7)
                        break;   

                  if Athlete_11_checkbox is True:                   
                    while tagId == 8:  
                        coordinates_Tag8 =data
                        coordinates_x_Tag8 =(coordinates_Tag8["x"])
                        coordinates_y_Tag8 =(coordinates_Tag8["y"])
                        coordinates_z_Tag8 =(coordinates_Tag8["z"])
                        #print (coordinates_x_Tag8)
                        break;   

                  if Athlete_12_checkbox is True:
                    while tagId == 9:
                        coordinates_Tag9 =data
                        coordinates_x_Tag9 =(coordinates_Tag9["x"])
                        coordinates_y_Tag9 =(coordinates_Tag9["y"])
                        coordinates_z_Tag9 =(coordinates_Tag9["z"])
                        #print (coordinates_x_Tag9)
                        break;   

                  if Athlete_13_checkbox is True:
                    while tagId == 10:
                        coordinates_Tag10 =data
                        coordinates_x_Tag10 =(coordinates_Tag10["x"])
                        coordinates_y_Tag10 =(coordinates_Tag10["y"])
                        coordinates_z_Tag10 =(coordinates_Tag10["z"])
                        #print (coordinates_x_Tag10)
                        break;   

                  if Athlete_14_checkbox is True:
                    while tagId == 11:
                        coordinates_Tag11 =data
                        coordinates_x_Tag11 =(coordinates_Tag11["x"])
                        coordinates_y_Tag11 =(coordinates_Tag11["y"])
                        coordinates_z_Tag11 =(coordinates_Tag11["z"])
                        #print (coordinates_x_Tag11)
                        break;   

                  if Athlete_15_checkbox is True:
                    while tagId == 12:
                        coordinates_Tag12 =data
                        coordinates_x_Tag12 =(coordinates_Tag12["x"])
                        coordinates_y_Tag12 =(coordinates_Tag12["y"])
                        coordinates_z_Tag12 =(coordinates_Tag12["z"])
                        #print (coordinates_x_Tag12)
                        break;   

                  if Athlete_16_checkbox is True:
                    while tagId == 13:
                        coordinates_Tag13 =data
                        coordinates_x_Tag13 =(coordinates_Tag13["x"])
                        coordinates_y_Tag13 =(coordinates_Tag13["y"])
                        coordinates_z_Tag13 =(coordinates_Tag13["z"])
                        #print (coordinates_x_Tag13)
                        break;   

                  if Athlete_17_checkbox is True:
                    while tagId == 14:
                        coordinates_Tag14 =data
                        coordinates_x_Tag14 =(coordinates_Tag14["x"])
                        coordinates_y_Tag14 =(coordinates_Tag14["y"])
                        coordinates_z_Tag14 =(coordinates_Tag14["z"])
                        #print (coordinates_x_Tag14)
                        break;
                    
                  counter = counter +1

              elif tab_Game==2:    
                  if Athlete_1_Drill_checkbox is True or player==1:
                    while tagId == 1:
                        coordinates =data
                        coordinates_x =(coordinates["x"])
                        coordinates_y =(coordinates["y"])
                        coordinates_z =(coordinates["z"])
                  #      print (tagId,coordinates_x,coordinates_y,coordinates_z)
                        break;
                  if Athlete_2_Drill_checkbox is True or player==2:
                    while tagId == 2:
                        coordinates_Tag2 =data
                        coordinates_x_Tag2 =(coordinates_Tag2["x"])
                        coordinates_y_Tag2 =(coordinates_Tag2["y"])
                        coordinates_z_Tag2 =(coordinates_Tag2["z"])
                        #print (coordinates_x_Tag2)
                        break;    
                  if Athlete_3_Drill_checkbox is True or player==3:
                    while tagId == 3:                        
                        coordinates_Tag3 =data
                        coordinates_x_Tag3 =(coordinates_Tag3["x"])
                        coordinates_y_Tag3 =(coordinates_Tag3["y"])
                        coordinates_z_Tag3 =(coordinates_Tag3["z"])
                        #print (coordinates_x_Tag3)
                        break;
                   
                  if Athlete_4_Drill_checkbox is True or player==4:
                    while tagId == 4:
                        coordinates_Tag4 =data
                        coordinates_x_Tag4 =(coordinates_Tag4["x"])
                        coordinates_y_Tag4 =(coordinates_Tag4["y"])
                        coordinates_z_Tag4 =(coordinates_Tag4["z"])
                        #print (coordinates_x_Tag4)
                        break;

                  if Athlete_5_Drill_checkbox is True or player==5:
                    while tagId == 5:
                        coordinates_Tag5 =data
                        coordinates_x_Tag5 =(coordinates_Tag5["x"])
                        coordinates_y_Tag5 =(coordinates_Tag5["y"])
                        coordinates_z_Tag5 =(coordinates_Tag5["z"])
                        #print (coordinates_x_Tag5)
                        break;   

                  if Athlete_6_Drill_checkbox is True or player==6:
                    while tagId == 6:
                        coordinates_Tag6 =data
                        coordinates_x_Tag6 =(coordinates_Tag6["x"])
                        coordinates_y_Tag6 =(coordinates_Tag6["y"])
                        coordinates_z_Tag6 =(coordinates_Tag6["z"])
                        #print (coordinates_x_Tag6)
                        break;   

                  if Athlete_7_Drill_checkbox is True or player==7:
                    while tagId == 7:
                        coordinates_Tag7 =data
                        coordinates_x_Tag7 =(coordinates_Tag7["x"])
                        coordinates_y_Tag7 =(coordinates_Tag7["y"])
                        coordinates_z_Tag7 =(coordinates_Tag7["z"])
                        #print (coordinates_x_Tag7)
                        break;   

                  if Athlete_8_Drill_checkbox is True or player==8:
                    while tagId == 8:  
                        coordinates_Tag8 =data
                        coordinates_x_Tag8 =(coordinates_Tag8["x"])
                        coordinates_y_Tag8 =(coordinates_Tag8["y"])
                        coordinates_z_Tag8 =(coordinates_Tag8["z"])
                        #print (coordinates_x_Tag8)
                        break;   

                  if Athlete_9_Drill_checkbox is True or player==9:
                    while tagId == 9:
                        coordinates_Tag9 =data
                        coordinates_x_Tag9 =(coordinates_Tag9["x"])
                        coordinates_y_Tag9 =(coordinates_Tag9["y"])
                        coordinates_z_Tag9 =(coordinates_Tag9["z"])
                        #print (coordinates_x_Tag9)
                        break;   

                  if Athlete_10_Drill_checkbox is True or player==10:
                    while tagId == 10:
                        coordinates_Tag10 =data
                        coordinates_x_Tag10 =(coordinates_Tag10["x"])
                        coordinates_y_Tag10 =(coordinates_Tag10["y"])
                        coordinates_z_Tag10 =(coordinates_Tag10["z"])
                        #print (coordinates_x_Tag10)
                        break;   

                  if Athlete_11_Drill_checkbox is True or player==11:
                    while tagId == 11:
                        coordinates_Tag11 =data
                        coordinates_x_Tag11 =(coordinates_Tag11["x"])
                        coordinates_y_Tag11 =(coordinates_Tag11["y"])
                        coordinates_z_Tag11 =(coordinates_Tag11["z"])
                        #print (coordinates_x_Tag11)
                        break;   

                  if Athlete_12_Drill_checkbox is True or player==12:
                    while tagId == 12:
                        coordinates_Tag12 =data
                        coordinates_x_Tag12 =(coordinates_Tag12["x"])
                        coordinates_y_Tag12 =(coordinates_Tag12["y"])
                        coordinates_z_Tag12 =(coordinates_Tag12["z"])
                        #print (coordinates_x_Tag12)
                        break;   

                  if Athlete_13_Drill_checkbox is True or player==13:
                    while tagId == 13:
                        coordinates_Tag13 =data
                        coordinates_x_Tag13 =(coordinates_Tag13["x"])
                        coordinates_y_Tag13 =(coordinates_Tag13["y"])
                        coordinates_z_Tag13 =(coordinates_Tag13["z"])
                        #print (coordinates_x_Tag13)
                        break;   

                  if Athlete_14_Drill_checkbox is True or player==14:                    
                    while tagId == 14:
                        coordinates_Tag14 =data
                        coordinates_x_Tag14 =(coordinates_Tag14["x"])
                        coordinates_y_Tag14 =(coordinates_Tag14["y"])
                        coordinates_z_Tag14 =(coordinates_Tag14["z"])
                        #print (coordinates_x_Tag14)
                        break;
                    
                  counter = counter +1
              end_Tag_counter=0
              
        elif data_exists is 0:
            if update_count ==50:
               text=00 
               game_display.blit(floorplan, [0, 0])
               update_count=0
              # record_counter=0
       

    #################################################################################        
         
    ## loop into excel save file ###
        
       
        while save==2:
                  row = row + 1
                  exit_game = False
                  if data_exists is 1:                          
                          output_value=1
                          if tab_Game==1:

                              if Athlete_1_checkbox is True: 
                                      worksheet_Coordinates_Tag1.write(row, column,second)  
                                      worksheet_Coordinates_Tag1.write(row, column+1,coordinates_x)
                                      worksheet_Coordinates_Tag1.write(row, column+2,coordinates_y)
                                      worksheet_Coordinates_Tag1.write(row, column+3,coordinates_z)
                                      print(row)
                              if Athlete_2_checkbox is True:
                                      worksheet_Coordinates_Tag2.write(row, column,second)  
                                      worksheet_Coordinates_Tag2.write(row, column+1,coordinates_x_Tag2)
                                      worksheet_Coordinates_Tag2.write(row, column+2,coordinates_y_Tag2)
                                      worksheet_Coordinates_Tag2.write(row, column+3,coordinates_z_Tag2)

                          
                              if Athlete_3_checkbox is True:
                                      worksheet_Coordinates_Tag3.write(row, column,second)  
                                      worksheet_Coordinates_Tag3.write(row, column+1,coordinates_x_Tag3)
                                      worksheet_Coordinates_Tag3.write(row, column+2,coordinates_y_Tag3)
                                      worksheet_Coordinates_Tag3.write(row, column+3,coordinates_z_Tag3)

                          
                              if Athlete_4_checkbox is True:
                                      worksheet_Coordinates_Tag4.write(row, column,second)  
                                      worksheet_Coordinates_Tag4.write(row, column+1,coordinates_x_Tag4)
                                      worksheet_Coordinates_Tag4.write(row, column+2,coordinates_y_Tag4)
                                      worksheet_Coordinates_Tag4.write(row, column+3,coordinates_z_Tag4)

                              if Athlete_5_checkbox is True:
                                      worksheet_Coordinates_Tag5.write(row, column,second)  
                                      worksheet_Coordinates_Tag5.write(row, column+1,coordinates_x_Tag5)
                                      worksheet_Coordinates_Tag5.write(row, column+2,coordinates_y_Tag5)
                                      worksheet_Coordinates_Tag5.write(row, column+3,coordinates_z_Tag5)

                              if Athlete_6_checkbox is True:
                                      worksheet_Coordinates_Tag6.write(row, column,second)  
                                      worksheet_Coordinates_Tag6.write(row, column+1,coordinates_x_Tag6)
                                      worksheet_Coordinates_Tag6.write(row, column+2,coordinates_y_Tag6)
                                      worksheet_Coordinates_Tag6.write(row, column+3,coordinates_z_Tag6)

                              if Athlete_7_checkbox is True:
                                      worksheet_Coordinates_Tag7.write(row, column,second)  
                                      worksheet_Coordinates_Tag7.write(row, column+1,coordinates_x_Tag7)
                                      worksheet_Coordinates_Tag7.write(row, column+2,coordinates_y_Tag7)
                                      worksheet_Coordinates_Tag7.write(row, column+3,coordinates_z_Tag7)

                              if Athlete_11_checkbox is True:
                                      worksheet_Coordinates_Tag8.write(row, column,second)  
                                      worksheet_Coordinates_Tag8.write(row, column+1,coordinates_x_Tag8)
                                      worksheet_Coordinates_Tag8.write(row, column+2,coordinates_y_Tag8)
                                      worksheet_Coordinates_Tag8.write(row, column+3,coordinates_z_Tag8)

                              if Athlete_12_checkbox is True:
                                      worksheet_Coordinates_Tag9.write(row, column,second)  
                                      worksheet_Coordinates_Tag9.write(row, column+1,coordinates_x_Tag9)
                                      worksheet_Coordinates_Tag9.write(row, column+2,coordinates_y_Tag9)
                                      worksheet_Coordinates_Tag9.write(row, column+3,coordinates_z_Tag9)

                              if Athlete_13_checkbox is True:
                                      worksheet_Coordinates_Tag10.write(row, column,second)  
                                      worksheet_Coordinates_Tag10.write(row, column+1,coordinates_x_Tag10)
                                      worksheet_Coordinates_Tag10.write(row, column+2,coordinates_y_Tag10)
                                      worksheet_Coordinates_Tag10.write(row, column+3,coordinates_z_Tag10)

                              if Athlete_14_checkbox is True:
                                      worksheet_Coordinates_Tag11.write(row, column,second)  
                                      worksheet_Coordinates_Tag11.write(row, column+1,coordinates_x_Tag11)
                                      worksheet_Coordinates_Tag11.write(row, column+2,coordinates_y_Tag11)
                                      worksheet_Coordinates_Tag11.write(row, column+3,coordinates_z_Tag11)

                              if Athlete_15_checkbox is True:
                                      worksheet_Coordinates_Tag12.write(row, column,second)  
                                      worksheet_Coordinates_Tag12.write(row, column+1,coordinates_x_Tag12)
                                      worksheet_Coordinates_Tag12.write(row, column+2,coordinates_y_Tag12)
                                      worksheet_Coordinates_Tag12.write(row, column+3,coordinates_z_Tag12)

                              if Athlete_16_checkbox is True:
                                      worksheet_Coordinates_Tag13.write(row, column,second)  
                                      worksheet_Coordinates_Tag13.write(row, column+1,coordinates_x_Tag13)
                                      worksheet_Coordinates_Tag13.write(row, column+2,coordinates_y_Tag13)
                                      worksheet_Coordinates_Tag13.write(row, column+3,coordinates_z_Tag13)

                              if Athlete_17_checkbox is True:
                                      worksheet_Coordinates_Tag14.write(row, column,second)  
                                      worksheet_Coordinates_Tag14.write(row, column+1,coordinates_x_Tag14)
                                      worksheet_Coordinates_Tag14.write(row, column+2,coordinates_y_Tag14)
                                      worksheet_Coordinates_Tag14.write(row, column+3,coordinates_z_Tag14)
                                      
                          elif tab_Game==2:
                              if GK1_Drill==1 or player==1:
                                      worksheet_Coordinates_Tag1.write(row, column,second)  
                                      worksheet_Coordinates_Tag1.write(row, column+1,coordinates_x)
                                      worksheet_Coordinates_Tag1.write(row, column+2,coordinates_y)
                                      worksheet_Coordinates_Tag1.write(row, column+3,coordinates_z)
                              if WD1_Drill==2 or player==2:
                                      worksheet_Coordinates_Tag2.write(row, column,second)  
                                      worksheet_Coordinates_Tag2.write(row, column+1,coordinates_x_Tag2)
                                      worksheet_Coordinates_Tag2.write(row, column+2,coordinates_y_Tag2)
                                      worksheet_Coordinates_Tag2.write(row, column+3,coordinates_z_Tag2)
                              if GD1_Drill==3 or player==3:
                                      worksheet_Coordinates_Tag3.write(row, column,second)  
                                      worksheet_Coordinates_Tag3.write(row, column+1,coordinates_x_Tag3)
                                      worksheet_Coordinates_Tag3.write(row, column+2,coordinates_y_Tag3)
                                      worksheet_Coordinates_Tag3.write(row, column+3,coordinates_z_Tag3)
                              if C1_Drill==4 or player==4:
                                      worksheet_Coordinates_Tag4.write(row, column,second)  
                                      worksheet_Coordinates_Tag4.write(row, column+1,coordinates_x_Tag4)
                                      worksheet_Coordinates_Tag4.write(row, column+2,coordinates_y_Tag4)
                                      worksheet_Coordinates_Tag4.write(row, column+3,coordinates_z_Tag4)
                              if GA1_Drill ==5 or player==5:
                                      worksheet_Coordinates_Tag5.write(row, column,second)  
                                      worksheet_Coordinates_Tag5.write(row, column+1,coordinates_x_Tag5)
                                      worksheet_Coordinates_Tag5.write(row, column+2,coordinates_y_Tag5)
                                      worksheet_Coordinates_Tag5.write(row, column+3,coordinates_z_Tag5)
                              if WA1_Drill==6 or player==6:
                                      worksheet_Coordinates_Tag6.write(row, column,second)  
                                      worksheet_Coordinates_Tag6.write(row, column+1,coordinates_x_Tag6)
                                      worksheet_Coordinates_Tag6.write(row, column+2,coordinates_y_Tag6)
                                      worksheet_Coordinates_Tag6.write(row, column+3,coordinates_z_Tag6)
                              if GS1_Drill==7 or player==7:
                                      worksheet_Coordinates_Tag7.write(row, column,second)  
                                      worksheet_Coordinates_Tag7.write(row, column+1,coordinates_x_Tag7)
                                      worksheet_Coordinates_Tag7.write(row, column+2,coordinates_y_Tag7)
                                      worksheet_Coordinates_Tag7.write(row, column+3,coordinates_z_Tag7)
                              if GK2_Drill==8 or player==8:
                                      worksheet_Coordinates_Tag8.write(row, column,second)  
                                      worksheet_Coordinates_Tag8.write(row, column+1,coordinates_x_Tag8)
                                      worksheet_Coordinates_Tag8.write(row, column+2,coordinates_y_Tag8)
                                      worksheet_Coordinates_Tag8.write(row, column+3,coordinates_z_Tag8)
                              if WD2_Drill==9 or player==9:
                                      worksheet_Coordinates_Tag9.write(row, column,second)  
                                      worksheet_Coordinates_Tag9.write(row, column+1,coordinates_x_Tag9)
                                      worksheet_Coordinates_Tag9.write(row, column+2,coordinates_y_Tag9)
                                      worksheet_Coordinates_Tag9.write(row, column+3,coordinates_z_Tag9)
                              if GD2_Drill==10 or player==10:
                                      worksheet_Coordinates_Tag10.write(row, column,second)  
                                      worksheet_Coordinates_Tag10.write(row, column+1,coordinates_x_Tag10)
                                      worksheet_Coordinates_Tag10.write(row, column+2,coordinates_y_Tag10)
                                      worksheet_Coordinates_Tag10.write(row, column+3,coordinates_z_Tag10)
                              if C2_Drill==11 or player==11:
                                      worksheet_Coordinates_Tag11.write(row, column,second)  
                                      worksheet_Coordinates_Tag11.write(row, column+1,coordinates_x_Tag11)
                                      worksheet_Coordinates_Tag11.write(row, column+2,coordinates_y_Tag11)
                                      worksheet_Coordinates_Tag11.write(row, column+3,coordinates_z_Tag11)
                              if GA2_Drill==12 or player==12:
                                      worksheet_Coordinates_Tag12.write(row, column,second)  
                                      worksheet_Coordinates_Tag12.write(row, column+1,coordinates_x_Tag12)
                                      worksheet_Coordinates_Tag12.write(row, column+2,coordinates_y_Tag12)
                                      worksheet_Coordinates_Tag12.write(row, column+3,coordinates_z_Tag12)
                              if WA2_Drill==13 or player==13:
                                      worksheet_Coordinates_Tag13.write(row, column,second)  
                                      worksheet_Coordinates_Tag13.write(row, column+1,coordinates_x_Tag13)
                                      worksheet_Coordinates_Tag13.write(row, column+2,coordinates_y_Tag13)
                                      worksheet_Coordinates_Tag13.write(row, column+3,coordinates_z_Tag13)
                              if GS2_Drill==14 or player==14:
                                      worksheet_Coordinates_Tag14.write(row, column,second)  
                                      worksheet_Coordinates_Tag14.write(row, column+1,coordinates_x_Tag14)
                                      worksheet_Coordinates_Tag14.write(row, column+2,coordinates_y_Tag14)
                                      worksheet_Coordinates_Tag14.write(row, column+3,coordinates_z_Tag14)
                                  
                      
                              width=game_display2.width()
                              height=game_display2.height()
                              ptr =game_display2.constBits()
                              ptr.setsize(game_display2.byteCount())
                              arr = np.array(ptr).reshape(height,width,4)
                              arr2=arr[:,:,:3]
                              
                  if data_exists is 0:
                    pass
                  break;
            ##Connecting to MQTT ##
    def on_connect(client, userdata, flags, rc):
       global topic3;global reconnect
       print(rc)
       if rc==0:
           print(mqtt.connack_string(rc))
           topic3 = 1 + topic3
       else:         
            print("bad connection")            
  
    def on_subscribe(client, userdata, mid, granted_qos):
        global topic1;global topic2;global topic3; global clientloop
        topic1 = 1
        print("Subscribed to topic!")
        

############################################################################################################################################
    ret_val=ctypes.windll.user32.MessageBoxW(0, "Are You Collecting Data?", "Indoor Positioning", 4)
    clientloop=0
    if ret_val ==6:
            client = mqtt.Client()
            client.connect(host, port=port,keepalive=10000)        ###uncomment when in connected locally
            client.subscribe(topic)
            client.on_connect = on_connect
            client.on_subscribe = on_subscribe                        
            client.on_message = on_message
        
    def Set_Output_location(self):
        global Output_file_directory;global Out_img;global out1;global img; global outputfile
        global fourcc;global video;global file;global file_1; global close_1;global New_Trial_1; global SCREEN_WIDTH; global SCREEN_HEIGHT; global videosave; global file_directory;
        global worksheet_Coordinates_Tag1;global worksheet_Coordinates_Tag2;global worksheet_Coordinates_Tag3;global worksheet_Coordinates_Tag4;global worksheet_Coordinates_Tag5;
        global worksheet_Coordinates_Tag6;global worksheet_Coordinates_Tag7;global worksheet_Coordinates_Tag8;global worksheet_Coordinates_Tag9;global worksheet_Coordinates_Tag10;
        global worksheet_Coordinates_Tag11;global worksheet_Coordinates_Tag12;global worksheet_Coordinates_Tag13;global worksheet_Coordinates_Tag14; global data_record

        videosave =0
        root = tk.Tk()
        root.withdraw()    
        #sets output directory and file names
        if self.parent_tabWidget.currentIndex()==0:
            file =filedialog.asksaveasfilename(initialdir = "/",title = "Save file",filetypes = (("xlsx files","*.xlsx"),("all files","*.*")))
            file_1=file +'.xlsx'
            self.Race_Save_location.setText(file_1)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            size=(847,425)
            FPS_output=210
           # out1 = cv2.VideoWriter(file +'.avi', fourcc, FPS_output, size) #filename,codec,fps,(width,height)
            close_1=1            
            outputfile= xlsxwriter.Workbook(file_1) ##create excel file
            key=cv2.waitKey(1)
            data_record=0
        elif self.parent_tabWidget.currentIndex()==1:            
            file_directory = str(QFileDialog.getExistingDirectory())
            self.Race_Save_Drills_location.setText(file_directory)
            data_record=1


        ###### Generates a new trial ########
    def New_Trial(self):
        global New_trial;global file_2;global New_Trial_1;global row;global counter;global topic2;global topic3;global save_counter;global file;
        global new_trial_count;global outputfile;
        global worksheet_Coordinates_Tag1;global worksheet_Coordinates_Tag2;global worksheet_Coordinates_Tag3;global worksheet_Coordinates_Tag4;global worksheet_Coordinates_Tag5;
        global worksheet_Coordinates_Tag6;global worksheet_Coordinates_Tag7;global worksheet_Coordinates_Tag8;global worksheet_Coordinates_Tag9;global worksheet_Coordinates_Tag10;
        global worksheet_Coordinates_Tag11;global worksheet_Coordinates_Tag12;global worksheet_Coordinates_Tag13;global worksheet_Coordinates_Tag14;
        global game_display; global Graphic; global Track_graphic; global Drills_Graphic; global output_value

        outputfile.close()
        new_trial_count+=1
        New_Trial_1 = 1        
        New_trial = new_trial_count
        New_trial=str(New_trial)
        row = 0
        counter = 0
        file_2 = file + '_' + New_trial + '.xlsx'
        messagebox.showinfo('File', 'New Trial')
        New_trial=int(New_trial)
        record = 2
        #self.Record_Video()
        outputfile= xlsxwriter.Workbook(file_2)
        if self.parent_tabWidget.currentIndex()==0:
            Athlete_1_checkbox =self.Athlete_1_checkbox.isChecked()           
            Athlete_2_checkbox =self.Athlete_2_checkbox.isChecked()
            Athlete_3_checkbox =self.Athlete_3_checkbox.isChecked()
            Athlete_4_checkbox =self.Athlete_4_checkbox.isChecked()
            Athlete_5_checkbox =self.Athlete_5_checkbox.isChecked()
            Athlete_6_checkbox =self.Athlete_6_checkbox.isChecked()
            Athlete_7_checkbox =self.Athlete_7_checkbox.isChecked()
            Athlete_11_checkbox =self.Athlete_11_checkbox.isChecked()
            Athlete_12_checkbox =self.Athlete_12_checkbox.isChecked()
            Athlete_13_checkbox =self.Athlete_13_checkbox.isChecked()
            Athlete_14_checkbox =self.Athlete_14_checkbox.isChecked()
            Athlete_15_checkbox =self.Athlete_15_checkbox.isChecked()
            Athlete_16_checkbox =self.Athlete_16_checkbox.isChecked()
            Athlete_17_checkbox =self.Athlete_17_checkbox.isChecked()
            if Athlete_1_checkbox is True:
                worksheet_Coordinates_Tag1=outputfile.add_worksheet('Coordinates_Tag1')
                worksheet_Coordinates_Tag1.write("A1","Time")   
                worksheet_Coordinates_Tag1.write("B1","X")
                worksheet_Coordinates_Tag1.write("C1","Y")
                worksheet_Coordinates_Tag1.write("D1","Z")
                worksheet_Coordinates_Tag1.write("E1","T1")
                worksheet_Coordinates_Tag1.write("F1","T2")
                worksheet_Coordinates_Tag1.write("G1","Sub")
                worksheet_Coordinates_Tag1.write("H1","Tag")
                worksheet_Coordinates_Tag1.write("H2","GK")
            if Athlete_2_checkbox is True:
                worksheet_Coordinates_Tag2=outputfile.add_worksheet('Coordinates_Tag2')
                worksheet_Coordinates_Tag2.write("A1","Time")   
                worksheet_Coordinates_Tag2.write("B1","X")
                worksheet_Coordinates_Tag2.write("C1","Y")
                worksheet_Coordinates_Tag2.write("D1","Z")
                worksheet_Coordinates_Tag2.write("E1","T1")
                worksheet_Coordinates_Tag2.write("F1","T2")
                worksheet_Coordinates_Tag2.write("G1","Sub")
                worksheet_Coordinates_Tag2.write("H1","Tag")
                worksheet_Coordinates_Tag2.write("H2","WD")
            if Athlete_3_checkbox is True:
                worksheet_Coordinates_Tag3=outputfile.add_worksheet('Coordinates_Tag3')
                worksheet_Coordinates_Tag3.write("A1","Time")   
                worksheet_Coordinates_Tag3.write("B1","X")
                worksheet_Coordinates_Tag3.write("C1","Y")
                worksheet_Coordinates_Tag3.write("D1","Z")
                worksheet_Coordinates_Tag3.write("E1","T1")
                worksheet_Coordinates_Tag3.write("F1","T2")
                worksheet_Coordinates_Tag3.write("G1","Sub")
                worksheet_Coordinates_Tag3.write("H1","Tag")
                worksheet_Coordinates_Tag3.write("H2","GD")
            if Athlete_4_checkbox is True:
                worksheet_Coordinates_Tag4=outputfile.add_worksheet('Coordinates_Tag4')
                worksheet_Coordinates_Tag4.write("A1","Time")   
                worksheet_Coordinates_Tag4.write("B1","X")
                worksheet_Coordinates_Tag4.write("C1","Y")
                worksheet_Coordinates_Tag4.write("D1","Z")
                worksheet_Coordinates_Tag4.write("E1","T1")
                worksheet_Coordinates_Tag4.write("F1","T2")
                worksheet_Coordinates_Tag4.write("G1","Sub")
                worksheet_Coordinates_Tag4.write("H1","Tag")
                worksheet_Coordinates_Tag4.write("H2","C")
            if Athlete_5_checkbox is True:
                worksheet_Coordinates_Tag5=outputfile.add_worksheet('Coordinates_Tag5')
                worksheet_Coordinates_Tag5.write("A1","Time")   
                worksheet_Coordinates_Tag5.write("B1","X")
                worksheet_Coordinates_Tag5.write("C1","Y")
                worksheet_Coordinates_Tag5.write("D1","Z")
                worksheet_Coordinates_Tag5.write("E1","T1")
                worksheet_Coordinates_Tag5.write("F1","T2")
                worksheet_Coordinates_Tag5.write("G1","Sub")
                worksheet_Coordinates_Tag5.write("H1","Tag")
                worksheet_Coordinates_Tag5.write("H2","GA")
            if Athlete_6_checkbox is True:
                worksheet_Coordinates_Tag6=outputfile.add_worksheet('Coordinates_Tag6')
                worksheet_Coordinates_Tag6.write("A1","Time")   
                worksheet_Coordinates_Tag6.write("B1","X")
                worksheet_Coordinates_Tag6.write("C1","Y")
                worksheet_Coordinates_Tag6.write("D1","Z")
                worksheet_Coordinates_Tag6.write("E1","T1")
                worksheet_Coordinates_Tag6.write("F1","T2")
                worksheet_Coordinates_Tag6.write("G1","Sub")
                worksheet_Coordinates_Tag6.write("H1","Tag")
                worksheet_Coordinates_Tag6.write("H2","WA")
            if Athlete_7_checkbox is True:
                worksheet_Coordinates_Tag7=outputfile.add_worksheet('Coordinates_Tag7')
                worksheet_Coordinates_Tag7.write("A1","Time")   
                worksheet_Coordinates_Tag7.write("B1","X")
                worksheet_Coordinates_Tag7.write("C1","Y")
                worksheet_Coordinates_Tag7.write("D1","Z")
                worksheet_Coordinates_Tag7.write("E1","T1")
                worksheet_Coordinates_Tag7.write("F1","T2")
                worksheet_Coordinates_Tag7.write("G1","Sub")
                worksheet_Coordinates_Tag7.write("H1","Tag")
                worksheet_Coordinates_Tag7.write("H2","GS")
            if Athlete_11_checkbox is True:
                worksheet_Coordinates_Tag8=outputfile.add_worksheet('Coordinates_Tag8')
                worksheet_Coordinates_Tag8.write("A1","Time")   
                worksheet_Coordinates_Tag8.write("B1","X")
                worksheet_Coordinates_Tag8.write("C1","Y")
                worksheet_Coordinates_Tag8.write("D1","Z")
                worksheet_Coordinates_Tag8.write("E1","T1")
                worksheet_Coordinates_Tag8.write("F1","T2")
                worksheet_Coordinates_Tag8.write("G1","Sub")
                worksheet_Coordinates_Tag8.write("H1","Tag")
                worksheet_Coordinates_Tag8.write("H2","GK_2")
            if Athlete_12_checkbox is True:
                worksheet_Coordinates_Tag9=outputfile.add_worksheet('Coordinates_Tag9')
                worksheet_Coordinates_Tag9.write("A1","Time")   
                worksheet_Coordinates_Tag9.write("B1","X")
                worksheet_Coordinates_Tag9.write("C1","Y")
                worksheet_Coordinates_Tag9.write("D1","Z")
                worksheet_Coordinates_Tag9.write("E1","T1")
                worksheet_Coordinates_Tag9.write("F1","T2")
                worksheet_Coordinates_Tag9.write("G1","Sub")
                worksheet_Coordinates_Tag9.write("H1","Tag")
                worksheet_Coordinates_Tag9.write("H2","WD_2")
            if Athlete_13_checkbox is True:
                worksheet_Coordinates_Tag10=outputfile.add_worksheet('Coordinates_Tag10')
                worksheet_Coordinates_Tag10.write("A1","Time")   
                worksheet_Coordinates_Tag10.write("B1","X")
                worksheet_Coordinates_Tag10.write("C1","Y")
                worksheet_Coordinates_Tag10.write("D1","Z")
                worksheet_Coordinates_Tag10.write("E1","T1")
                worksheet_Coordinates_Tag10.write("F1","T2")
                worksheet_Coordinates_Tag10.write("G1","Sub")
                worksheet_Coordinates_Tag10.write("H1","Tag")
                worksheet_Coordinates_Tag10.write("H2","GD_2")
            if Athlete_14_checkbox is True:
                worksheet_Coordinates_Tag11=outputfile.add_worksheet('Coordinates_Tag11')
                worksheet_Coordinates_Tag11.write("A1","Time")   
                worksheet_Coordinates_Tag11.write("B1","X")
                worksheet_Coordinates_Tag11.write("C1","Y")
                worksheet_Coordinates_Tag11.write("D1","Z")
                worksheet_Coordinates_Tag11.write("E1","T1")
                worksheet_Coordinates_Tag11.write("F1","T2")
                worksheet_Coordinates_Tag11.write("G1","Sub")
                worksheet_Coordinates_Tag11.write("H1","Tag")
                worksheet_Coordinates_Tag11.write("H2","C_2")
            if Athlete_15_checkbox is True:
                worksheet_Coordinates_Tag12=outputfile.add_worksheet('Coordinates_Tag12')
                worksheet_Coordinates_Tag12.write("A1","Time")   
                worksheet_Coordinates_Tag12.write("B1","X")
                worksheet_Coordinates_Tag12.write("C1","Y")
                worksheet_Coordinates_Tag12.write("D1","Z")
                worksheet_Coordinates_Tag12.write("E1","T1")
                worksheet_Coordinates_Tag12.write("F1","T2")
                worksheet_Coordinates_Tag12.write("G1","Sub")
                worksheet_Coordinates_Tag12.write("H1","Tag")
                worksheet_Coordinates_Tag12.write("H2","GA_2")
            if Athlete_16_checkbox is True:
                worksheet_Coordinates_Tag13=outputfile.add_worksheet('Coordinates_Tag13')
                worksheet_Coordinates_Tag13.write("A1","Time")   
                worksheet_Coordinates_Tag13.write("B1","X")
                worksheet_Coordinates_Tag13.write("C1","Y")
                worksheet_Coordinates_Tag13.write("D1","Z")
                worksheet_Coordinates_Tag13.write("E1","T1")
                worksheet_Coordinates_Tag13.write("F1","T2")
                worksheet_Coordinates_Tag13.write("G1","Sub")
                worksheet_Coordinates_Tag13.write("H1","Tag")
                worksheet_Coordinates_Tag13.write("H2","WA_2")
            if Athlete_17_checkbox is True:
                worksheet_Coordinates_Tag14=outputfile.add_worksheet('Coordinates_Tag14')
                worksheet_Coordinates_Tag14.write("A1","Time")   
                worksheet_Coordinates_Tag14.write("B1","X")
                worksheet_Coordinates_Tag14.write("C1","Y")
                worksheet_Coordinates_Tag14.write("D1","Z")
                worksheet_Coordinates_Tag14.write("E1","T1")
                worksheet_Coordinates_Tag14.write("F1","T2")
                worksheet_Coordinates_Tag14.write("G1","Sub")
                worksheet_Coordinates_Tag14.write("H1","Tag")
                worksheet_Coordinates_Tag14.write("H2","GS_2")
        
        
        if self.parent_tabWidget.currentIndex()==1:
            Athlete_1_Drill_checkbox =self.Athlete_1_Drillcheckbox.isChecked()
            Athlete_2_Drill_checkbox =self.Athlete_2_Drillcheckbox.isChecked()
            Athlete_3_Drill_checkbox =self.Athlete_3_Drillcheckbox.isChecked()
            Athlete_4_Drill_checkbox =self.Athlete_4_Drillcheckbox.isChecked()
            Athlete_5_Drill_checkbox =self.Athlete_5_Drillcheckbox.isChecked()
            Athlete_6_Drill_checkbox =self.Athlete_6_Drillcheckbox.isChecked()
            Athlete_7_Drill_checkbox =self.Athlete_7_Drillcheckbox.isChecked()
            Athlete_8_Drill_checkbox =self.Athlete_8_Drillcheckbox.isChecked()
            Athlete_9_Drill_checkbox =self.Athlete_9_Drillcheckbox.isChecked()
            Athlete_10_Drill_checkbox =self.Athlete_10_Drillcheckbox.isChecked()
            Athlete_11_Drill_checkbox =self.Athlete_11_Drillcheckbox.isChecked()
            Athlete_12_Drill_checkbox =self.Athlete_12_Drillcheckbox.isChecked()
            Athlete_13_Drill_checkbox =self.Athlete_13_Drillcheckbox.isChecked()
            Athlete_14_Drill_checkbox =self.Athlete_14_Drillcheckbox.isChecked()
            
            if Athlete_1_Drill_checkbox is True:            
                worksheet_Coordinates_Tag1=outputfile.add_worksheet('Coordinates_Tag1')
                worksheet_Coordinates_Tag1.write("A1","Time")   
                worksheet_Coordinates_Tag1.write("B1","X")
                worksheet_Coordinates_Tag1.write("C1","Y")
                worksheet_Coordinates_Tag1.write("D1","Z")
            if Athlete_2_Drill_checkbox is True:   
                worksheet_Coordinates_Tag2=outputfile.add_worksheet('Coordinates_Tag2')
                worksheet_Coordinates_Tag2.write("A1","Time")   
                worksheet_Coordinates_Tag2.write("B1","X")
                worksheet_Coordinates_Tag2.write("C1","Y")
                worksheet_Coordinates_Tag2.write("D1","Z")
            if Athlete_3_Drill_checkbox is True:   
                worksheet_Coordinates_Tag3=outputfile.add_worksheet('Coordinates_Tag3')
                worksheet_Coordinates_Tag3.write("A1","Time")   
                worksheet_Coordinates_Tag3.write("B1","X")
                worksheet_Coordinates_Tag3.write("C1","Y")
                worksheet_Coordinates_Tag3.write("D1","Z")
            if Athlete_4_Drill_checkbox is True:   
                worksheet_Coordinates_Tag4=outputfile.add_worksheet('Coordinates_Tag4')
                worksheet_Coordinates_Tag4.write("A1","Time")   
                worksheet_Coordinates_Tag4.write("B1","X")
                worksheet_Coordinates_Tag4.write("C1","Y")
                worksheet_Coordinates_Tag4.write("D1","Z")
            if Athlete_5_Drill_checkbox is True:   
                worksheet_Coordinates_Tag5=outputfile.add_worksheet('Coordinates_Tag5')
                worksheet_Coordinates_Tag5.write("A1","Time")   
                worksheet_Coordinates_Tag5.write("B1","X")
                worksheet_Coordinates_Tag5.write("C1","Y")
                worksheet_Coordinates_Tag5.write("D1","Z")
            if Athlete_6_Drill_checkbox is True:   
                worksheet_Coordinates_Tag6=outputfile.add_worksheet('Coordinates_Tag6')
                worksheet_Coordinates_Tag6.write("A1","Time")   
                worksheet_Coordinates_Tag6.write("B1","X")
                worksheet_Coordinates_Tag6.write("C1","Y")
                worksheet_Coordinates_Tag6.write("D1","Z")
            if Athlete_7_Drill_checkbox is True:  
                worksheet_Coordinates_Tag7=outputfile.add_worksheet('Coordinates_Tag7')
                worksheet_Coordinates_Tag7.write("A1","Time")   
                worksheet_Coordinates_Tag7.write("B1","X")
                worksheet_Coordinates_Tag7.write("C1","Y")
                worksheet_Coordinates_Tag7.write("D1","Z")
            if Athlete_8_Drill_checkbox is True:   
                worksheet_Coordinates_Tag8=outputfile.add_worksheet('Coordinates_Tag8')
                worksheet_Coordinates_Tag8.write("A1","Time")   
                worksheet_Coordinates_Tag8.write("B1","X")
                worksheet_Coordinates_Tag8.write("C1","Y")
                worksheet_Coordinates_Tag8.write("D1","Z")
            if Athlete_9_Drill_checkbox is True:   
                worksheet_Coordinates_Tag9=outputfile.add_worksheet('Coordinates_Tag9')
                worksheet_Coordinates_Tag9.write("A1","Time")   
                worksheet_Coordinates_Tag9.write("B1","X")
                worksheet_Coordinates_Tag9.write("C1","Y")
                worksheet_Coordinates_Tag9.write("D1","Z")
            if Athlete_10_Drill_checkbox is True:   
                worksheet_Coordinates_Tag10=outputfile.add_worksheet('Coordinates_Tag10')
                worksheet_Coordinates_Tag10.write("A1","Time")   
                worksheet_Coordinates_Tag10.write("B1","X")
                worksheet_Coordinates_Tag10.write("C1","Y")
                worksheet_Coordinates_Tag10.write("D1","Z")
            if Athlete_11_Drill_checkbox is True:   
                worksheet_Coordinates_Tag11=outputfile.add_worksheet('Coordinates_Tag11')
                worksheet_Coordinates_Tag11.write("A1","Time")   
                worksheet_Coordinates_Tag11.write("B1","X")
                worksheet_Coordinates_Tag11.write("C1","Y")
                worksheet_Coordinates_Tag11.write("D1","Z")
            if Athlete_12_Drill_checkbox is True:   
                worksheet_Coordinates_Tag12=outputfile.add_worksheet('Coordinates_Tag12')
                worksheet_Coordinates_Tag12.write("A1","Time")   
                worksheet_Coordinates_Tag12.write("B1","X")
                worksheet_Coordinates_Tag12.write("C1","Y")
                worksheet_Coordinates_Tag12.write("D1","Z")
            if Athlete_13_Drill_checkbox is True:   
                worksheet_Coordinates_Tag13=outputfile.add_worksheet('Coordinates_Tag13')
                worksheet_Coordinates_Tag13.write("A1","Time")   
                worksheet_Coordinates_Tag13.write("B1","X")
                worksheet_Coordinates_Tag13.write("C1","Y")
                worksheet_Coordinates_Tag13.write("D1","Z")
            if Athlete_14_Drill_checkbox is True:   
                worksheet_Coordinates_Tag14=outputfile.add_worksheet('Coordinates_Tag14')
                worksheet_Coordinates_Tag14.write("A1","Time")   
                worksheet_Coordinates_Tag14.write("B1","X")
                worksheet_Coordinates_Tag14.write("C1","Y")
                worksheet_Coordinates_Tag14.write("D1","Z")


        key=cv2.waitKey(1)

        return
       
    def T1_score(self):
        global second;global counter;global coordinates;global flag;global row;global data_exists; global Red_team_counter;global Blue_team_counter;
        global Athlete_1_checkbox;global Athlete_2_checkbox;global Athlete_3_checkbox;global Athlete_4_checkbox;
        global Athlete_5_checkbox;global Athlete_6_checkbox;global Athlete_7_checkbox;
        global Athlete_11_checkbox;global Athlete_12_checkbox;global Athlete_13_checkbox;
        global Athlete_14_checkbox;global Athlete_15_checkbox;global Athlete_16_checkbox;
        global Athlete_17_checkbox; global text2
        flag= 1


        Red_team_counter+=1
        Red_team_counter1=str(Red_team_counter)
        self.T1_number_box.setText(Red_team_counter1)

        if data_exists is 1:
            if Athlete_1_checkbox is True:
                worksheet_Coordinates_Tag1.write(row, column+4,Red_team_counter)
            if Athlete_2_checkbox is True:
                worksheet_Coordinates_Tag2.write(row, column+4,Red_team_counter)
            if Athlete_3_checkbox is True:
                worksheet_Coordinates_Tag3.write(row, column+4,Red_team_counter)
            if Athlete_4_checkbox is True:
                worksheet_Coordinates_Tag4.write(row, column+4,Red_team_counter)
            if Athlete_5_checkbox is True:
                worksheet_Coordinates_Tag5.write(row, column+4,Red_team_counter)
            if Athlete_6_checkbox is True:
                worksheet_Coordinates_Tag6.write(row, column+4,Red_team_counter)
            if Athlete_7_checkbox is True:
                worksheet_Coordinates_Tag7.write(row, column+4,Red_team_counter)
            if Athlete_11_checkbox is True:
                worksheet_Coordinates_Tag8.write(row, column+4,Red_team_counter)
            if Athlete_12_checkbox is True:
                worksheet_Coordinates_Tag9.write(row, column+4,Red_team_counter)
            if Athlete_13_checkbox is True:
                worksheet_Coordinates_Tag10.write(row, column+4,Red_team_counter)
            if Athlete_14_checkbox is True:
                worksheet_Coordinates_Tag11.write(row, column+4,Red_team_counter)
            if Athlete_15_checkbox is True:
                worksheet_Coordinates_Tag12.write(row, column+4,Red_team_counter)
            if Athlete_16_checkbox is True:
                worksheet_Coordinates_Tag13.write(row, column+4,Red_team_counter)
            if Athlete_17_checkbox is True:
                worksheet_Coordinates_Tag14.write(row, column+4,Red_team_counter)
        


    def T2_score(self):
        global second;global counter;global coordinates;global flag;global row;global data_exists; global Red_team_counter;global Blue_team_counter;
        global Athlete_1_checkbox;global Athlete_2_checkbox;global Athlete_3_checkbox;global Athlete_4_checkbox;
        global Athlete_5_checkbox;global Athlete_6_checkbox;global Athlete_7_checkbox;
        global Athlete_11_checkbox;global Athlete_12_checkbox;global Athlete_13_checkbox;
        global Athlete_14_checkbox;global Athlete_15_checkbox;global Athlete_16_checkbox;
        global Athlete_17_checkbox; global text2
        flag= 1
        
        Blue_team_counter+=1
        Blue_team_counter1=str(Blue_team_counter)
        self.T2_number_box.setText(Blue_team_counter1)

        if data_exists is 1:
            if Athlete_1_checkbox is True:
                worksheet_Coordinates_Tag1.write(row, column+5,Blue_team_counter)
            if Athlete_2_checkbox is True:
                worksheet_Coordinates_Tag2.write(row, column+5,Blue_team_counter)
            if Athlete_3_checkbox is True:
                worksheet_Coordinates_Tag3.write(row, column+5,Blue_team_counter)
            if Athlete_4_checkbox is True:
                worksheet_Coordinates_Tag4.write(row, column+5,Blue_team_counter)
            if Athlete_5_checkbox is True:
                worksheet_Coordinates_Tag5.write(row, column+5,Blue_team_counter)
            if Athlete_6_checkbox is True:
                worksheet_Coordinates_Tag6.write(row, column+5,Blue_team_counter)
            if Athlete_7_checkbox is True:
                worksheet_Coordinates_Tag7.write(row, column+5,Blue_team_counter)
            if Athlete_11_checkbox is True:
                worksheet_Coordinates_Tag8.write(row, column+5,Blue_team_counter)
            if Athlete_12_checkbox is True:
                worksheet_Coordinates_Tag9.write(row, column+5,Blue_team_counter)
            if Athlete_13_checkbox is True:
                worksheet_Coordinates_Tag10.write(row, column+5,Blue_team_counter)
            if Athlete_14_checkbox is True:
                worksheet_Coordinates_Tag11.write(row, column+5,Blue_team_counter)
            if Athlete_15_checkbox is True:
                worksheet_Coordinates_Tag12.write(row, column+5,Blue_team_counter)
            if Athlete_16_checkbox is True:
                worksheet_Coordinates_Tag13.write(row, column+5,Blue_team_counter)
            if Athlete_17_checkbox is True:
                worksheet_Coordinates_Tag14.write(row, column+5,Blue_team_counter)
        
    def Substitution(self):
        global second;global counter;global coordinates;global flag;global row;global data_exists;
        global game_display; global Graphic; global Track_graphic; global Drills_Graphic; global output_value
        flag= 1
        if data_exists is 1:
            if self.Sub_Choice.currentIndex()==1:
                worksheet_Coordinates_Tag1.write(row, column+6,flag)
            if self.Sub_Choice.currentIndex()==2:
                worksheet_Coordinates_Tag2.write(row, column+6,flag)
            if self.Sub_Choice.currentIndex()==3:
                worksheet_Coordinates_Tag3.write(row, column+6,flag)
            if self.Sub_Choice.currentIndex()==4:
                worksheet_Coordinates_Tag4.write(row, column+6,flag)
            if self.Sub_Choice.currentIndex()==5:
                worksheet_Coordinates_Tag5.write(row, column+6,flag)
            if self.Sub_Choice.currentIndex()==6:
                worksheet_Coordinates_Tag6.write(row, column+6,flag)
            if self.Sub_Choice.currentIndex()==7:
                worksheet_Coordinates_Tag7.write(row, column+6,flag)
            if self.Sub_Choice.currentIndex()==8:
                worksheet_Coordinates_Tag8.write(row, column+6,flag)
            if self.Sub_Choice.currentIndex()==9:
                worksheet_Coordinates_Tag9.write(row, column+6,flag)
            if self.Sub_Choice.currentIndex()==10:
                worksheet_Coordinates_Tag10.write(row, column+6,flag)
            if self.Sub_Choice.currentIndex()==11:
                worksheet_Coordinates_Tag11.write(row, column+6,flag)
            if self.Sub_Choice.currentIndex()==12:
                worksheet_Coordinates_Tag12.write(row, column+6,flag)
            if self.Sub_Choice.currentIndex()==13:
                worksheet_Coordinates_Tag13.write(row, column+6,flag)
            if self.Sub_Choice.currentIndex()==13:
                worksheet_Coordinates_Tag14.write(row, column+6,flag)
        
 
    def Save_Active(self):
        global coordinates_x;global coordinates_y; global coordinates_z
        global coordinates_x_Tag2; global coordinates_y_Tag2; global coordinates_z_Tag2
        global coordinates_x_Tag3; global coordinates_y_Tag3; global coordinates_z_Tag3
        global coordinates_x_Tag4; global coordinates_y_Tag4; global coordinates_z_Tag4
        global coordinates_x_Tag5; global coordinates_y_Tag5; global coordinates_z_Tag5
        global coordinates_x_Tag6; global coordinates_y_Tag6; global coordinates_z_Tag6
        global coordinates_x_Tag7; global coordinates_y_Tag7; global coordinates_z_Tag7
        global coordinates_x_Tag8; global coordinates_y_Tag8; global coordinates_z_Tag8
        global coordinates_x_Tag9; global coordinates_y_Tag9; global coordinates_z_Tag9
        global coordinates_x_Tag10; global coordinates_y_Tag10; global coordinates_z_Tag10
        global coordinates_x_Tag11; global coordinates_y_Tag11; global coordinates_z_Tag11
        global coordinates_x_Tag12; global coordinates_y_Tag12; global coordinates_z_Tag12
        global coordinates_x_Tag13; global coordinates_y_Tag13; global coordinates_z_Tag13
        global coordinates_x_Tag14; global coordinates_y_Tag14; global coordinates_z_Tag14
        global coordinates_x_Tag15; global coordinates_y_Tag15; global coordinates_z_Tag15
        global worksheet_Coordinates;global worksheet_Coordinates_Tag1;global worksheet_Coordinates_Tag2;global worksheet_Coordinates_Tag3;
        global worksheet_Coordinates_Tag4;global worksheet_Coordinates_Tag5;global worksheet_Coordinates_Tag6;global worksheet_Coordinates_Tag7;
        global worksheet_Coordinates_Tag8;global worksheet_Coordinates_Tag9;global worksheet_Coordinates_Tag10;global worksheet_Coordinates_Tag11;
        global worksheet_Coordinates_Tag12;global worksheet_Coordinates_Tag13;global worksheet_Coordinates_Tag14;global worksheet_Coordinates_Tag15;
        global Tag1; global Tag2; global Tag3; global Tag4;global Tag5;global Tag6;global Tag7;global Tag8;global Tag9;global Tag10;global Tag11;global Tag12
        global Tag13;global Tag14;global Tag15
        global Tag_1_visible; global Tag_2_visible; global Tag_3_visible; global Tag_4_visible;global Tag_5_visible;global Tag_6_visible;global Tag_7_visible
        global Tag_8_visible;global Tag_9_visible;global Tag_10_visible;global Tag_11_visible;global Tag_12_visible;global Tag_13_visible;global Tag_14_visible;
        global Tag_15_visible;
        global second;global timestamp2;global counter;global record;global row;global column;global connected;global coordinates_exists
        global flag;global b;global a;global Filter_type;global tags;global data_exists;
        global Athlete_1_checkbox;global Athlete_2_checkbox;global Athlete_3_checkbox;global Athlete_4_checkbox;
        global Athlete_5_checkbox;global Athlete_6_checkbox;global Athlete_7_checkbox;
        global Athlete_11_checkbox;global Athlete_12_checkbox;global Athlete_13_checkbox;
        global Athlete_14_checkbox;global Athlete_15_checkbox;global Athlete_16_checkbox;
        global Athlete_17_checkbox; global outputfile;global file_1;global file_2;global New_trial; global New_trial_1; global file;global save;
        global game_display; global Graphic; global Track_graphic; global Drills_Graphic; global output_value
 
        if save==2:  #button up = 2
            save=1
            record = 2
            self.Tag_Set.setDisabled(False)
            outputfile.close()

        elif save==1: #button down =1
            save=2
            save_counter =0
            record = 1
            self.Tag_Set.setDisabled(True)
            #row=0
            
    def Save_Active_Drills(self):
        global coordinates_x;global coordinates_y; global coordinates_z
        global coordinates_x_Tag2; global coordinates_y_Tag2; global coordinates_z_Tag2
        global coordinates_x_Tag3; global coordinates_y_Tag3; global coordinates_z_Tag3
        global coordinates_x_Tag4; global coordinates_y_Tag4; global coordinates_z_Tag4
        global coordinates_x_Tag5; global coordinates_y_Tag5; global coordinates_z_Tag5
        global coordinates_x_Tag6; global coordinates_y_Tag6; global coordinates_z_Tag6
        global coordinates_x_Tag7; global coordinates_y_Tag7; global coordinates_z_Tag7
        global coordinates_x_Tag8; global coordinates_y_Tag8; global coordinates_z_Tag8
        global coordinates_x_Tag9; global coordinates_y_Tag9; global coordinates_z_Tag9
        global coordinates_x_Tag10; global coordinates_y_Tag10; global coordinates_z_Tag10
        global coordinates_x_Tag11; global coordinates_y_Tag11; global coordinates_z_Tag11
        global coordinates_x_Tag12; global coordinates_y_Tag12; global coordinates_z_Tag12
        global coordinates_x_Tag13; global coordinates_y_Tag13; global coordinates_z_Tag13
        global coordinates_x_Tag14; global coordinates_y_Tag14; global coordinates_z_Tag14
        global coordinates_x_Tag15; global coordinates_y_Tag15; global coordinates_z_Tag15
        global worksheet_Coordinates;global worksheet_Coordinates_Tag1;global worksheet_Coordinates_Tag2;global worksheet_Coordinates_Tag3;
        global worksheet_Coordinates_Tag4;global worksheet_Coordinates_Tag5;global worksheet_Coordinates_Tag6;global worksheet_Coordinates_Tag7;
        global worksheet_Coordinates_Tag8;global worksheet_Coordinates_Tag9;global worksheet_Coordinates_Tag10;global worksheet_Coordinates_Tag11;
        global worksheet_Coordinates_Tag12;global worksheet_Coordinates_Tag13;global worksheet_Coordinates_Tag14;global worksheet_Coordinates_Tag15;
        global Tag1; global Tag2; global Tag3; global Tag4;global Tag5;global Tag6;global Tag7;global Tag8;global Tag9;global Tag10;global Tag11;global Tag12
        global Tag13;global Tag14;global Tag15
        global Tag_1_visible; global Tag_2_visible; global Tag_3_visible; global Tag_4_visible;global Tag_5_visible;global Tag_6_visible;global Tag_7_visible
        global Tag_8_visible;global Tag_9_visible;global Tag_10_visible;global Tag_11_visible;global Tag_12_visible;global Tag_13_visible;global Tag_14_visible;
        global Tag_15_visible;
        global second;global timestamp2;global counter;global record;global row;global column;global connected;global coordinates_exists
        global flag;global b;global a;global Filter_type;global tags;global data_exists;
        global Athlete_1_checkbox;global Athlete_2_checkbox;global Athlete_3_checkbox;global Athlete_4_checkbox;
        global Athlete_5_checkbox;global Athlete_6_checkbox;global Athlete_7_checkbox;
        global Athlete_11_checkbox;global Athlete_12_checkbox;global Athlete_13_checkbox;
        global Athlete_14_checkbox;global Athlete_15_checkbox;global Athlete_16_checkbox;
        global Athlete_17_checkbox; global outputfile;global file_1;global file_2;global New_trial; global New_trial_1; global file;global save;
        global file_directory; global player;
        global GK1_Game;global GK1_Drill;global WD1_Game;global WD1_Drill;
        global GD1_Game;global GD1_Drill;global C1_Game;global C1_Drill;
        global GA1_Game;global GA1_Drill;global WA1_Game;global WA1_Drill;
        global GS1_Game;global GS1_Drill;global GK2_Game;global GK2_Drill;
        global WD2_Game;global WD2_Drill;global GD2_Game;global GD2_Drill;
        global C2_Game;global C2_Drill;global GA2_Game;global GA2_Drill;
        global WA2_Game;global WA2_Drill;global GS2_Game;global GS2_Drill;
        global game_display; global Graphic; global Track_graphic; global Drills_Graphic; global output_value
        
        if save==2:  #button up = 2
            save=1
            record = 2
            if self.Drill_Choice.currentIndex()==3:
                self.Tag_set_Drills.setDisabled(False)
            outputfile.close()
        
        elif save==1: #button down =1
            save=2
            save_counter =0
            record = 1
            row = 0
            self.Tag_set_Drills.setDisabled(True)

                
        
    def Close(self):
        global out1; global close_1;global pygaame;global outputfile; global output_value; global pygame

        if output_value == 1:
            outputfile.close()
        Dialog.close()

    def displayImage(self):
        global pygame; global game_display; global clock; global SCREEN_WIDTH; global SCREEN_HEIGHT; global tag_ids; global MINIMUM_COORDINATES;
        global MAXIMUM_COORDINATES; global PIXEL_RATIO_X;global PIXEL_RATIO_Y; global TAG_MAIN_COLOR_1; global TAG_MAIN_COLOR_2;global TAG_SECONDARY_COLOR
        global TAG_HISTORY_MAIN_COLOR; global TAG_HISTORY_SECONDARY_COLOR; global tags; global clock; global floorplan;
        global Graphic; global Track_graphic; global Drills_Graphic; global output_value; global floorplan_image2
      # Create instances of the PozyxTag class from the IDs you used earlier.
        pygame.init()
        ######## PYGAME SETUP##############
        # Enter the IDS of the tags you will use here. Edit that the tag ID is on the back of your tag written in HEX. - EDIT ME!
     #   tag_ids = tag_ids
        # Enter the dimensions in mm of your area here. Only positive numbers. Notice that e,e is the upper Left corner in graphics programming. - EDIT ME!
        MINIMUM_COORDINATES= Point(0, 0)
        MAXIMUM_COORDINATES = Point(32790, 18232)
        # COLORS
        # define the colours to be used for visualisation in RGB format
        WHITE = (255, 255, 255)
        BLACK = ( 0, 0, 0 )
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        LIGHT_PURPLE = (126, 38, 119)
        GREY = (20, 20, 20)
        GREEN = (42, 89, 59)

        TAG_MAIN_COLOR_1 = BLACK
        TAG_MAIN_COLOR_2= BLUE
        TAG_SECONDARY_COLOR = RED
        TAG_HISTORY_MAIN_COLOR = GREY
        TAG_HISTORY_SECONDARY_COLOR  = GREEN

                #  initialise pygame       
        clock = pygame.time.Clock()
        if self.parent_tabWidget.currentIndex()==0:
            floorplan_image = pygame.image.load('netball court2.JPG')
            floorplan_image2 = pygame.image.load('court fill.PNG')
            SCREEN_WIDTH = 847
            SCREEN_HEIGHT = 425 
        if self.parent_tabWidget.currentIndex()==1:
            if self.Drill_Choice.currentIndex()==1:
               floorplan_image = pygame.image.load('20m sprint.PNG')
               SCREEN_WIDTH = 662
               SCREEN_HEIGHT = 548
            elif self.Drill_Choice.currentIndex()==2:
               floorplan_image = pygame.image.load('Illinois test.PNG')
               SCREEN_WIDTH = 662
               SCREEN_HEIGHT = 548
            elif self.Drill_Choice.currentIndex()==3:
               floorplan_image = pygame.image.load('YO-YO test.PNG')
               SCREEN_WIDTH = 662
               SCREEN_HEIGHT = 548

        PIXEL_RATIO_X = (MAXIMUM_COORDINATES.x - MINIMUM_COORDINATES.x) / SCREEN_WIDTH
        PIXEL_RATIO_Y = (MAXIMUM_COORDINATES.y - MINIMUM_COORDINATES.y) / SCREEN_HEIGHT
        game_display = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
 
        game_display.fill(WHITE)
        floorplan = pygame.transform.rotate(floorplan_image,0)

        game_display.blit(floorplan, [0, 0])

    ## Callback triggered by a new Pozyx data packet ##

    def screen_update(self, Graphic, window=1):
        global game_display2; global t3; global tab_Game; global pygame;
        if window==1:
            if tab_Game==1:
                Track_graphic.setPixmap(QPixmap.fromImage(game_display2)) ############ look more
                Track_graphic.setScaledContents(True)
               
            elif tab_Game==2:
                Drills_Graphic.setPixmap(QPixmap.fromImage(game_display2)) ############ look more
                Drills_Graphic.setScaledContents(True)
    def score(self):
       global text2; global tab_Game
       if tab_Game==1:  
           Red_team_counter2=Red_team_counter
           Blue_team_counter2=Blue_team_counter
           text1=[str(Red_team_counter2),"-",str(Blue_team_counter2)]
           text2=''.join(text1)
       else:
           text2=''

    def Tag_Set1(self):
        global Output_file_directory;global Out_img;global out1;global img; global outputfile
        global fourcc;global video;global file;global file_1; global close_1;global New_Trial_1; global SCREEN_WIDTH; global SCREEN_HEIGHT; global videosave; global file_directory;
        global worksheet_Coordinates_Tag1;global worksheet_Coordinates_Tag2;global worksheet_Coordinates_Tag3;global worksheet_Coordinates_Tag4;global worksheet_Coordinates_Tag5;
        global worksheet_Coordinates_Tag6;global worksheet_Coordinates_Tag7;global worksheet_Coordinates_Tag8;global worksheet_Coordinates_Tag9;global worksheet_Coordinates_Tag10;
        global worksheet_Coordinates_Tag11;global worksheet_Coordinates_Tag12;global worksheet_Coordinates_Tag13;global worksheet_Coordinates_Tag14;
        global GK1_Game;global GK1_Drill;global WD1_Game;global WD1_Drill;
        global GD1_Game;global GD1_Drill;global C1_Game;global C1_Drill;
        global GA1_Game;global GA1_Drill;global WA1_Game;global WA1_Drill;
        global GS1_Game;global GS1_Drill;global GK2_Game;global GK2_Drill;
        global WD2_Game;global WD2_Drill;global GD2_Game;global GD2_Drill;
        global C2_Game;global C2_Drill;global GA2_Game;global GA2_Drill;
        global WA2_Game;global WA2_Drill;global GS2_Game;global GS2_Drill; global tags; global tag_ids;
        global Athlete_1_checkbox;
        global Athlete_2_checkbox;global Athlete_3_checkbox;global Athlete_4_checkbox;
        global Athlete_5_checkbox;global Athlete_6_checkbox;global Athlete_7_checkbox;
        global Athlete_11_checkbox;global Athlete_12_checkbox;global Athlete_13_checkbox;
        global Athlete_14_checkbox;global Athlete_15_checkbox;global Athlete_16_checkbox;
        global Athlete_17_checkbox;
        global Athlete_1_Drill_checkbox; global Athlete_2_Drill_checkbox; global Athlete_3_Drill_checkbox; global Athlete_4_Drill_checkbox;
        global Athlete_5_Drill_checkbox; global Athlete_6_Drill_checkbox; global Athlete_7_Drill_checkbox; global Athlete_8_Drill_checkbox;
        global Athlete_9_Drill_checkbox; global Athlete_10_Drill_checkbox; global Athlete_11_Drill_checkbox; global Athlete_12_Drill_checkbox;
        global Athlete_13_Drill_checkbox; global Athlete_14_Drill_checkbox;
        global game_display; global Graphic; global Track_graphic; global Drills_Graphic; global output_value

        GK1_Game=0;GK1_Drill=0;
        WD1_Game=0;WD1_Drill=0;
        GD1_Game=0;GD1_Drill=0;
        C1_Game=0;C1_Drill=0;
        GA1_Game=0;GA1_Drill=0;
        WA1_Game=0;WA1_Drill=0;
        GS1_Game=0;GS1_Drill=0;
        GK2_Game=0;GK2_Drill=0;
        WD2_Game=0;WD2_Drill=0;
        GD2_Game=0;GD2_Drill=0;
        C2_Game=0;C2_Drill=0;
        GA2_Game=0;GA2_Drill=0;
        WA2_Game=0;WA2_Drill=0;
        GS2_Game=0;GS2_Drill=0;


        if self.parent_tabWidget.currentIndex()==0:
            Athlete_1_checkbox =self.Athlete_1_checkbox.isChecked()           
            Athlete_2_checkbox =self.Athlete_2_checkbox.isChecked()
            Athlete_3_checkbox =self.Athlete_3_checkbox.isChecked()
            Athlete_4_checkbox =self.Athlete_4_checkbox.isChecked()
            Athlete_5_checkbox =self.Athlete_5_checkbox.isChecked()
            Athlete_6_checkbox =self.Athlete_6_checkbox.isChecked()
            Athlete_7_checkbox =self.Athlete_7_checkbox.isChecked()
            Athlete_11_checkbox =self.Athlete_11_checkbox.isChecked()
            Athlete_12_checkbox =self.Athlete_12_checkbox.isChecked()
            Athlete_13_checkbox =self.Athlete_13_checkbox.isChecked()
            Athlete_14_checkbox =self.Athlete_14_checkbox.isChecked()
            Athlete_15_checkbox =self.Athlete_15_checkbox.isChecked()
            Athlete_16_checkbox =self.Athlete_16_checkbox.isChecked()
            Athlete_17_checkbox =self.Athlete_17_checkbox.isChecked()
            if Athlete_1_checkbox is True:
                GK1_Game=1
                worksheet_Coordinates_Tag1=outputfile.add_worksheet('Coordinates_Tag1')
                worksheet_Coordinates_Tag1.write("A1","Time")   
                worksheet_Coordinates_Tag1.write("B1","X")
                worksheet_Coordinates_Tag1.write("C1","Y")
                worksheet_Coordinates_Tag1.write("D1","Z")
                worksheet_Coordinates_Tag1.write("E1","T1")
                worksheet_Coordinates_Tag1.write("F1","T2")
                worksheet_Coordinates_Tag1.write("G1","Sub")
                worksheet_Coordinates_Tag1.write("H1","Tag")
                worksheet_Coordinates_Tag1.write("H2","GK")
                
            else:
                GK1_Game=0    
            if Athlete_2_checkbox is True:
                WD1_Game=2 
                worksheet_Coordinates_Tag2=outputfile.add_worksheet('Coordinates_Tag2')
                worksheet_Coordinates_Tag2.write("A1","Time")   
                worksheet_Coordinates_Tag2.write("B1","X")
                worksheet_Coordinates_Tag2.write("C1","Y")
                worksheet_Coordinates_Tag2.write("D1","Z")
                worksheet_Coordinates_Tag2.write("E1","T1")
                worksheet_Coordinates_Tag2.write("F1","T2")
                worksheet_Coordinates_Tag2.write("G1","Sub")
                worksheet_Coordinates_Tag2.write("H1","Tag")
                worksheet_Coordinates_Tag2.write("H2","WD")
            else:
                WD1_Game=0
            if Athlete_3_checkbox is True:
                GD1_Game=3
                worksheet_Coordinates_Tag3=outputfile.add_worksheet('Coordinates_Tag3')
                worksheet_Coordinates_Tag3.write("A1","Time")   
                worksheet_Coordinates_Tag3.write("B1","X")
                worksheet_Coordinates_Tag3.write("C1","Y")
                worksheet_Coordinates_Tag3.write("D1","Z")
                worksheet_Coordinates_Tag3.write("E1","T1")
                worksheet_Coordinates_Tag3.write("F1","T2")
                worksheet_Coordinates_Tag3.write("G1","Sub")
                worksheet_Coordinates_Tag3.write("H1","Tag")
                worksheet_Coordinates_Tag3.write("H2","GD")
            else:
                GD1_Game=0
            if Athlete_4_checkbox is True:
                C1_Game=4                
                worksheet_Coordinates_Tag4=outputfile.add_worksheet('Coordinates_Tag4')
                worksheet_Coordinates_Tag4.write("A1","Time")   
                worksheet_Coordinates_Tag4.write("B1","X")
                worksheet_Coordinates_Tag4.write("C1","Y")
                worksheet_Coordinates_Tag4.write("D1","Z")
                worksheet_Coordinates_Tag4.write("E1","T1")
                worksheet_Coordinates_Tag4.write("F1","T2")
                worksheet_Coordinates_Tag4.write("G1","Sub")
                worksheet_Coordinates_Tag4.write("H1","Tag")
                worksheet_Coordinates_Tag4.write("H2","C")
            else:
                C1_Game=0
            if Athlete_5_checkbox is True:
                GA1_Game=5               
                worksheet_Coordinates_Tag5=outputfile.add_worksheet('Coordinates_Tag5')
                worksheet_Coordinates_Tag5.write("A1","Time")   
                worksheet_Coordinates_Tag5.write("B1","X")
                worksheet_Coordinates_Tag5.write("C1","Y")
                worksheet_Coordinates_Tag5.write("D1","Z")
                worksheet_Coordinates_Tag5.write("E1","T1")
                worksheet_Coordinates_Tag5.write("F1","T2")
                worksheet_Coordinates_Tag5.write("G1","Sub")
                worksheet_Coordinates_Tag5.write("H1","Tag")
                worksheet_Coordinates_Tag5.write("H2","GA")
            else:
                GA1_Game=0
            if Athlete_6_checkbox is True:
                WA1_Game=6
                worksheet_Coordinates_Tag6=outputfile.add_worksheet('Coordinates_Tag6')
                worksheet_Coordinates_Tag6.write("A1","Time")   
                worksheet_Coordinates_Tag6.write("B1","X")
                worksheet_Coordinates_Tag6.write("C1","Y")
                worksheet_Coordinates_Tag6.write("D1","Z")
                worksheet_Coordinates_Tag6.write("E1","T1")
                worksheet_Coordinates_Tag6.write("F1","T2")
                worksheet_Coordinates_Tag6.write("G1","Sub")
                worksheet_Coordinates_Tag6.write("H1","Tag")
                worksheet_Coordinates_Tag6.write("H2","WA")
            else:
                WA1_Game=0
            if Athlete_7_checkbox is True:
                GS1_Game=7
                worksheet_Coordinates_Tag7=outputfile.add_worksheet('Coordinates_Tag7')
                worksheet_Coordinates_Tag7.write("A1","Time")   
                worksheet_Coordinates_Tag7.write("B1","X")
                worksheet_Coordinates_Tag7.write("C1","Y")
                worksheet_Coordinates_Tag7.write("D1","Z")
                worksheet_Coordinates_Tag7.write("E1","T1")
                worksheet_Coordinates_Tag7.write("F1","T2")
                worksheet_Coordinates_Tag7.write("G1","Sub")
                worksheet_Coordinates_Tag7.write("H1","Tag")
                worksheet_Coordinates_Tag7.write("H2","GS")
            else:                
                GS1_Game=0
            if Athlete_11_checkbox is True:
                GK2_Game=8 
                worksheet_Coordinates_Tag8=outputfile.add_worksheet('Coordinates_Tag8')
                worksheet_Coordinates_Tag8.write("A1","Time")   
                worksheet_Coordinates_Tag8.write("B1","X")
                worksheet_Coordinates_Tag8.write("C1","Y")
                worksheet_Coordinates_Tag8.write("D1","Z")
                worksheet_Coordinates_Tag8.write("E1","T1")
                worksheet_Coordinates_Tag8.write("F1","T2")
                worksheet_Coordinates_Tag8.write("G1","Sub")
                worksheet_Coordinates_Tag8.write("H1","Tag")
                worksheet_Coordinates_Tag8.write("H2","GK_2")
            else:        
                GK2_Game=0
            if Athlete_12_checkbox is True:
                WD2_Game=9               
                worksheet_Coordinates_Tag9=outputfile.add_worksheet('Coordinates_Tag9')
                worksheet_Coordinates_Tag9.write("A1","Time")   
                worksheet_Coordinates_Tag9.write("B1","X")
                worksheet_Coordinates_Tag9.write("C1","Y")
                worksheet_Coordinates_Tag9.write("D1","Z")
                worksheet_Coordinates_Tag9.write("E1","T1")
                worksheet_Coordinates_Tag9.write("F1","T2")
                worksheet_Coordinates_Tag9.write("G1","Sub")
                worksheet_Coordinates_Tag9.write("H1","Tag")
                worksheet_Coordinates_Tag9.write("H2","WD_2")
            else: 
                WD2_Game=0
            if Athlete_13_checkbox is True:
                GD2_Game=10
                worksheet_Coordinates_Tag10=outputfile.add_worksheet('Coordinates_Tag10')
                worksheet_Coordinates_Tag10.write("A1","Time")   
                worksheet_Coordinates_Tag10.write("B1","X")
                worksheet_Coordinates_Tag10.write("C1","Y")
                worksheet_Coordinates_Tag10.write("D1","Z")
                worksheet_Coordinates_Tag10.write("E1","T1")
                worksheet_Coordinates_Tag10.write("F1","T2")
                worksheet_Coordinates_Tag10.write("G1","Sub")
                worksheet_Coordinates_Tag10.write("H1","Tag")
                worksheet_Coordinates_Tag10.write("H2","GD_2")
            else:                
                GD2_Game=0
            if Athlete_14_checkbox is True:
                C2_Game=11
                worksheet_Coordinates_Tag11=outputfile.add_worksheet('Coordinates_Tag11')
                worksheet_Coordinates_Tag11.write("A1","Time")   
                worksheet_Coordinates_Tag11.write("B1","X")
                worksheet_Coordinates_Tag11.write("C1","Y")
                worksheet_Coordinates_Tag11.write("D1","Z")
                worksheet_Coordinates_Tag11.write("E1","T1")
                worksheet_Coordinates_Tag11.write("F1","T2")
                worksheet_Coordinates_Tag11.write("G1","Sub")
                worksheet_Coordinates_Tag11.write("H1","Tag")
                worksheet_Coordinates_Tag11.write("H2","C_2")
            else:                
                C2_Game=0
            if Athlete_15_checkbox is True:                
                GA2_Game=12
                worksheet_Coordinates_Tag12=outputfile.add_worksheet('Coordinates_Tag12')
                worksheet_Coordinates_Tag12.write("A1","Time")   
                worksheet_Coordinates_Tag12.write("B1","X")
                worksheet_Coordinates_Tag12.write("C1","Y")
                worksheet_Coordinates_Tag12.write("D1","Z")
                worksheet_Coordinates_Tag12.write("E1","T1")
                worksheet_Coordinates_Tag12.write("F1","T2")
                worksheet_Coordinates_Tag12.write("G1","Sub")
                worksheet_Coordinates_Tag12.write("H1","Tag")
                worksheet_Coordinates_Tag12.write("H2","GA_2")
            else:                
                GA2_Game=0
            if Athlete_16_checkbox is True:
                WA2_Game=13
                worksheet_Coordinates_Tag13=outputfile.add_worksheet('Coordinates_Tag13')
                worksheet_Coordinates_Tag13.write("A1","Time")   
                worksheet_Coordinates_Tag13.write("B1","X")
                worksheet_Coordinates_Tag13.write("C1","Y")
                worksheet_Coordinates_Tag13.write("D1","Z")
                worksheet_Coordinates_Tag13.write("E1","T1")
                worksheet_Coordinates_Tag13.write("F1","T2")
                worksheet_Coordinates_Tag13.write("G1","Sub")
                worksheet_Coordinates_Tag13.write("H1","Tag")
                worksheet_Coordinates_Tag13.write("H2","WA_2")
            else:
                WA2_Game=0
            if Athlete_17_checkbox is True:
                GS2_Game=14                
                worksheet_Coordinates_Tag14=outputfile.add_worksheet('Coordinates_Tag14')
                worksheet_Coordinates_Tag14.write("A1","Time")   
                worksheet_Coordinates_Tag14.write("B1","X")
                worksheet_Coordinates_Tag14.write("C1","Y")
                worksheet_Coordinates_Tag14.write("D1","Z")
                worksheet_Coordinates_Tag14.write("E1","T1")
                worksheet_Coordinates_Tag14.write("F1","T2")
                worksheet_Coordinates_Tag14.write("G1","Sub")
                worksheet_Coordinates_Tag14.write("H1","Tag")
                worksheet_Coordinates_Tag14.write("H2","GS_2")
            else:
                GS2_Game=0
      
            tag_ids=[GK1_Game,WD1_Game,GD1_Game,C1_Game,GA1_Game,WA1_Game,GS1_Game,GK2_Game,WD2_Game,GD2_Game,C2_Game,GA2_Game,WA2_Game,GS2_Game]
            tag_ids[:] = (value for value in tag_ids if value != 0)
            tags = [PozyxTag(tag_id) for tag_id in tag_ids]
            print(tag_ids)
            messagebox.showinfo('Tags', 'Tags Set')
        
        if self.parent_tabWidget.currentIndex()==1:
            if self.Drill_Choice.currentIndex()==3:
                File_number=str(self.Filenumber_Choice.currentText())
                Drill = str(self.Drill_Choice.currentText())
                file =file_directory+ '/' + Drill + '_'+'Team' +'_'+ File_number + '.xlsx'
                outputfile= xlsxwriter.Workbook(file)
            Athlete_1_Drill_checkbox =self.Athlete_1_Drillcheckbox.isChecked()
            Athlete_2_Drill_checkbox =self.Athlete_2_Drillcheckbox.isChecked()
            Athlete_3_Drill_checkbox =self.Athlete_3_Drillcheckbox.isChecked()
            Athlete_4_Drill_checkbox =self.Athlete_4_Drillcheckbox.isChecked()
            Athlete_5_Drill_checkbox =self.Athlete_5_Drillcheckbox.isChecked()
            Athlete_6_Drill_checkbox =self.Athlete_6_Drillcheckbox.isChecked()
            Athlete_7_Drill_checkbox =self.Athlete_7_Drillcheckbox.isChecked()
            Athlete_8_Drill_checkbox =self.Athlete_8_Drillcheckbox.isChecked()
            Athlete_9_Drill_checkbox =self.Athlete_9_Drillcheckbox.isChecked()
            Athlete_10_Drill_checkbox =self.Athlete_10_Drillcheckbox.isChecked()
            Athlete_11_Drill_checkbox =self.Athlete_11_Drillcheckbox.isChecked()
            Athlete_12_Drill_checkbox =self.Athlete_12_Drillcheckbox.isChecked()
            Athlete_13_Drill_checkbox =self.Athlete_13_Drillcheckbox.isChecked()
            Athlete_14_Drill_checkbox =self.Athlete_14_Drillcheckbox.isChecked()
            
            if Athlete_1_Drill_checkbox is True:
                GK1_Drill=1
                worksheet_Coordinates_Tag1=outputfile.add_worksheet('Coordinates_Tag1')
                worksheet_Coordinates_Tag1.write("A1","Time")   
                worksheet_Coordinates_Tag1.write("B1","X")
                worksheet_Coordinates_Tag1.write("C1","Y")
                worksheet_Coordinates_Tag1.write("D1","Z")
            else:
                GK1_Drill=0
            if Athlete_2_Drill_checkbox is True:
                WD1_Drill=2
                worksheet_Coordinates_Tag2=outputfile.add_worksheet('Coordinates_Tag2')
                worksheet_Coordinates_Tag2.write("A1","Time")   
                worksheet_Coordinates_Tag2.write("B1","X")
                worksheet_Coordinates_Tag2.write("C1","Y")
                worksheet_Coordinates_Tag2.write("D1","Z")
            else:
                WD1_Drill=0
            if Athlete_3_Drill_checkbox is True:
                GD1_Drill=3
                worksheet_Coordinates_Tag3=outputfile.add_worksheet('Coordinates_Tag3')
                worksheet_Coordinates_Tag3.write("A1","Time")   
                worksheet_Coordinates_Tag3.write("B1","X")
                worksheet_Coordinates_Tag3.write("C1","Y")
                worksheet_Coordinates_Tag3.write("D1","Z")
            else:
                GD1_Drill=0
            if Athlete_4_Drill_checkbox is True:
                C1_Drill=4
                worksheet_Coordinates_Tag4=outputfile.add_worksheet('Coordinates_Tag4')
                worksheet_Coordinates_Tag4.write("A1","Time")   
                worksheet_Coordinates_Tag4.write("B1","X")
                worksheet_Coordinates_Tag4.write("C1","Y")
                worksheet_Coordinates_Tag4.write("D1","Z")
            else:
                C1_Drill=0
            if Athlete_5_Drill_checkbox is True:
                GA1_Drill=5
                worksheet_Coordinates_Tag5=outputfile.add_worksheet('Coordinates_Tag5')
                worksheet_Coordinates_Tag5.write("A1","Time")   
                worksheet_Coordinates_Tag5.write("B1","X")
                worksheet_Coordinates_Tag5.write("C1","Y")
                worksheet_Coordinates_Tag5.write("D1","Z")
            else:
                GA1_Drill=0
            if Athlete_6_Drill_checkbox is True:
                WA1_Drill=6
                worksheet_Coordinates_Tag6=outputfile.add_worksheet('Coordinates_Tag6')
                worksheet_Coordinates_Tag6.write("A1","Time")   
                worksheet_Coordinates_Tag6.write("B1","X")
                worksheet_Coordinates_Tag6.write("C1","Y")
                worksheet_Coordinates_Tag6.write("D1","Z")
            else:
                WA1_Drill=0
            if Athlete_7_Drill_checkbox is True:
                GS1_Drill=7
                worksheet_Coordinates_Tag7=outputfile.add_worksheet('Coordinates_Tag7')
                worksheet_Coordinates_Tag7.write("A1","Time")   
                worksheet_Coordinates_Tag7.write("B1","X")
                worksheet_Coordinates_Tag7.write("C1","Y")
                worksheet_Coordinates_Tag7.write("D1","Z")
            else:
                GS1_Drill=0
            if Athlete_8_Drill_checkbox is True:
                GK2_Drill=8
                worksheet_Coordinates_Tag8=outputfile.add_worksheet('Coordinates_Tag8')
                worksheet_Coordinates_Tag8.write("A1","Time")   
                worksheet_Coordinates_Tag8.write("B1","X")
                worksheet_Coordinates_Tag8.write("C1","Y")
                worksheet_Coordinates_Tag8.write("D1","Z")
            else:
                GK2_Drill=0
            if Athlete_9_Drill_checkbox is True:
                WD2_Drill=9
                worksheet_Coordinates_Tag9=outputfile.add_worksheet('Coordinates_Tag9')
                worksheet_Coordinates_Tag9.write("A1","Time")   
                worksheet_Coordinates_Tag9.write("B1","X")
                worksheet_Coordinates_Tag9.write("C1","Y")
                worksheet_Coordinates_Tag9.write("D1","Z")
            else:
                WD2_Drill=0
            if Athlete_10_Drill_checkbox is True:
                GD2_Drill=10
                worksheet_Coordinates_Tag10=outputfile.add_worksheet('Coordinates_Tag10')
                worksheet_Coordinates_Tag10.write("A1","Time")   
                worksheet_Coordinates_Tag10.write("B1","X")
                worksheet_Coordinates_Tag10.write("C1","Y")
                worksheet_Coordinates_Tag10.write("D1","Z")
            else:
                GD2_Drill=0
            if Athlete_11_Drill_checkbox is True:
                C2_Drill=11
                worksheet_Coordinates_Tag11=outputfile.add_worksheet('Coordinates_Tag11')
                worksheet_Coordinates_Tag11.write("A1","Time")   
                worksheet_Coordinates_Tag11.write("B1","X")
                worksheet_Coordinates_Tag11.write("C1","Y")
                worksheet_Coordinates_Tag11.write("D1","Z")
            else:
                C2_Drill=0
            if Athlete_12_Drill_checkbox is True:
                GA2_Drill=12
                worksheet_Coordinates_Tag12=outputfile.add_worksheet('Coordinates_Tag12')
                worksheet_Coordinates_Tag12.write("A1","Time")   
                worksheet_Coordinates_Tag12.write("B1","X")
                worksheet_Coordinates_Tag12.write("C1","Y")
                worksheet_Coordinates_Tag12.write("D1","Z")
            else:
                GA2_Drill=0
            if Athlete_13_Drill_checkbox is True:
                WA2_Drill=13
                worksheet_Coordinates_Tag13=outputfile.add_worksheet('Coordinates_Tag13')
                worksheet_Coordinates_Tag13.write("A1","Time")   
                worksheet_Coordinates_Tag13.write("B1","X")
                worksheet_Coordinates_Tag13.write("C1","Y")
                worksheet_Coordinates_Tag13.write("D1","Z")
            else:
                WA2_Drill=0
            if Athlete_14_Drill_checkbox is True:
                GS2_Drill=14
                worksheet_Coordinates_Tag14=outputfile.add_worksheet('Coordinates_Tag14')
                worksheet_Coordinates_Tag14.write("A1","Time")   
                worksheet_Coordinates_Tag14.write("B1","X")
                worksheet_Coordinates_Tag14.write("C1","Y")
                worksheet_Coordinates_Tag14.write("D1","Z")
            else:
                GS2_Drill=0       
                
            if self.Drill_Choice.currentIndex()==3:
                tag_ids=[GK1_Drill,WD1_Drill,GD1_Drill,C1_Drill,GA1_Drill,WA1_Drill,GS1_Drill,GK2_Drill,WD2_Drill,GD2_Drill,C2_Drill,GA2_Drill,WA2_Drill,GS2_Drill]
                tag_ids[:] = (value for value in tag_ids if value != 0)
                tags = [PozyxTag(tag_id) for tag_id in tag_ids]
                print(tag_ids)    
            messagebox.showinfo('Tags', 'Tags Set')

    
########################################### drills            
    def Set_Tag_method(self):
        global player; global tag_ids; global tags; global outputfile; global file;
        global worksheet_Coordinates;global worksheet_Coordinates_Tag1;global worksheet_Coordinates_Tag2;global worksheet_Coordinates_Tag3;
        global worksheet_Coordinates_Tag4;global worksheet_Coordinates_Tag5;global worksheet_Coordinates_Tag6;global worksheet_Coordinates_Tag7;
        global worksheet_Coordinates_Tag8;global worksheet_Coordinates_Tag9;global worksheet_Coordinates_Tag10;global worksheet_Coordinates_Tag11;
        global worksheet_Coordinates_Tag12;global worksheet_Coordinates_Tag13;global worksheet_Coordinates_Tag14;global worksheet_Coordinates_Tag15;
        global Athlete_1_checkbox;
        global Athlete_2_checkbox;global Athlete_3_checkbox;global Athlete_4_checkbox;
        global Athlete_5_checkbox;global Athlete_6_checkbox;global Athlete_7_checkbox;
        global Athlete_11_checkbox;global Athlete_12_checkbox;global Athlete_13_checkbox;
        global Athlete_14_checkbox;global Athlete_15_checkbox;global Athlete_16_checkbox;
        global Athlete_17_checkbox;
        global Athlete_1_Drill_checkbox; global Athlete_2_Drill_checkbox; global Athlete_3_Drill_checkbox; global Athlete_4_Drill_checkbox;
        global Athlete_5_Drill_checkbox; global Athlete_6_Drill_checkbox; global Athlete_7_Drill_checkbox; global Athlete_8_Drill_checkbox;
        global Athlete_9_Drill_checkbox; global Athlete_10_Drill_checkbox; global Athlete_11_Drill_checkbox; global Athlete_12_Drill_checkbox;
        global Athlete_13_Drill_checkbox; global Athlete_14_Drill_checkbox;

        File_number=str(self.Filenumber_Choice.currentText())
        Drill = str(self.Drill_Choice.currentText())
        Player = str(self.Position_Choice.currentText())
        file =file_directory+ '/' + Player + '_' + Drill +'_'+ File_number +'.xlsx'
        outputfile= xlsxwriter.Workbook(file)
        if self.Position_Choice.currentIndex()==1:
            player=1
            worksheet_Coordinates_Tag1=outputfile.add_worksheet('Coordinates_Tag1')
            worksheet_Coordinates_Tag1.write("A1","Time")   
            worksheet_Coordinates_Tag1.write("B1","X")
            worksheet_Coordinates_Tag1.write("C1","Y")
            worksheet_Coordinates_Tag1.write("D1","Z")
        if self.Position_Choice.currentIndex()==2:
            player=2
            worksheet_Coordinates_Tag2=outputfile.add_worksheet('Coordinates_Tag2')
            worksheet_Coordinates_Tag2.write("A1","Time")   
            worksheet_Coordinates_Tag2.write("B1","X")
            worksheet_Coordinates_Tag2.write("C1","Y")
            worksheet_Coordinates_Tag2.write("D1","Z")
        if self.Position_Choice.currentIndex()==3:
            player=3
            worksheet_Coordinates_Tag3=outputfile.add_worksheet('Coordinates_Tag3')
            worksheet_Coordinates_Tag3.write("A1","Time")   
            worksheet_Coordinates_Tag3.write("B1","X")
            worksheet_Coordinates_Tag3.write("C1","Y")
            worksheet_Coordinates_Tag3.write("D1","Z")
        if self.Position_Choice.currentIndex()==4:
            player=4
            worksheet_Coordinates_Tag4=outputfile.add_worksheet('Coordinates_Tag4')
            worksheet_Coordinates_Tag4.write("A1","Time")   
            worksheet_Coordinates_Tag4.write("B1","X")
            worksheet_Coordinates_Tag4.write("C1","Y")
            worksheet_Coordinates_Tag4.write("D1","Z")
        if self.Position_Choice.currentIndex()==5:
            player=5
            worksheet_Coordinates_Tag5=outputfile.add_worksheet('Coordinates_Tag5')
            worksheet_Coordinates_Tag5.write("A1","Time")   
            worksheet_Coordinates_Tag5.write("B1","X")
            worksheet_Coordinates_Tag5.write("C1","Y")
            worksheet_Coordinates_Tag5.write("D1","Z")
        if self.Position_Choice.currentIndex()==6:
            player=6
            worksheet_Coordinates_Tag6=outputfile.add_worksheet('Coordinates_Tag6')
            worksheet_Coordinates_Tag6.write("A1","Time")   
            worksheet_Coordinates_Tag6.write("B1","X")
            worksheet_Coordinates_Tag6.write("C1","Y")
            worksheet_Coordinates_Tag6.write("D1","Z")
        if self.Position_Choice.currentIndex()==7:
            player=7
            worksheet_Coordinates_Tag7=outputfile.add_worksheet('Coordinates_Tag7')
            worksheet_Coordinates_Tag7.write("A1","Time")   
            worksheet_Coordinates_Tag7.write("B1","X")
            worksheet_Coordinates_Tag7.write("C1","Y")
            worksheet_Coordinates_Tag7.write("D1","Z")
        if self.Position_Choice.currentIndex()==8:
            player=8
            worksheet_Coordinates_Tag8=outputfile.add_worksheet('Coordinates_Tag8')
            worksheet_Coordinates_Tag8.write("A1","Time")   
            worksheet_Coordinates_Tag8.write("B1","X")
            worksheet_Coordinates_Tag8.write("C1","Y")
            worksheet_Coordinates_Tag8.write("D1","Z")
        if self.Position_Choice.currentIndex()==9:
            player=9
            worksheet_Coordinates_Tag9=outputfile.add_worksheet('Coordinates_Tag9')
            worksheet_Coordinates_Tag9.write("A1","Time")   
            worksheet_Coordinates_Tag9.write("B1","X")
            worksheet_Coordinates_Tag9.write("C1","Y")
            worksheet_Coordinates_Tag9.write("D1","Z")
        if self.Position_Choice.currentIndex()==10:
            player=10
            worksheet_Coordinates_Tag10=outputfile.add_worksheet('Coordinates_Tag10')
            worksheet_Coordinates_Tag10.write("A1","Time")   
            worksheet_Coordinates_Tag10.write("B1","X")
            worksheet_Coordinates_Tag10.write("C1","Y")
            worksheet_Coordinates_Tag10.write("D1","Z")
        if self.Position_Choice.currentIndex()==11:
            player=11
            worksheet_Coordinates_Tag11=outputfile.add_worksheet('Coordinates_Tag11')
            worksheet_Coordinates_Tag11.write("A1","Time")   
            worksheet_Coordinates_Tag11.write("B1","X")
            worksheet_Coordinates_Tag11.write("C1","Y")
            worksheet_Coordinates_Tag11.write("D1","Z")
        if self.Position_Choice.currentIndex()==12:
            player=12
            worksheet_Coordinates_Tag12=outputfile.add_worksheet('Coordinates_Tag12')
            worksheet_Coordinates_Tag12.write("A1","Time")   
            worksheet_Coordinates_Tag12.write("B1","X")
            worksheet_Coordinates_Tag12.write("C1","Y")
            worksheet_Coordinates_Tag12.write("D1","Z")
        if self.Position_Choice.currentIndex()==13:
            player=13
            worksheet_Coordinates_Tag13=outputfile.add_worksheet('Coordinates_Tag13')
            worksheet_Coordinates_Tag13.write("A1","Time")   
            worksheet_Coordinates_Tag13.write("B1","X")
            worksheet_Coordinates_Tag13.write("C1","Y")
            worksheet_Coordinates_Tag13.write("D1","Z")
        if self.Position_Choice.currentIndex()==14:
            player=14
            worksheet_Coordinates_Tag14=outputfile.add_worksheet('Coordinates_Tag14')
            worksheet_Coordinates_Tag14.write("A1","Time")   
            worksheet_Coordinates_Tag14.write("B1","X")
            worksheet_Coordinates_Tag14.write("C1","Y")
            worksheet_Coordinates_Tag14.write("D1","Z")
        tag_ids=[player]
        tags = [PozyxTag(tag_id) for tag_id in tag_ids]
        print(tag_ids)
        messagebox.showinfo('File', 'File Set')

        
    def Set_Drill_method(self):
        global player;global pygame; global outputfile;
        global worksheet_Coordinates;global worksheet_Coordinates_Tag1;global worksheet_Coordinates_Tag2;global worksheet_Coordinates_Tag3;
        global worksheet_Coordinates_Tag4;global worksheet_Coordinates_Tag5;global worksheet_Coordinates_Tag6;global worksheet_Coordinates_Tag7;
        global worksheet_Coordinates_Tag8;global worksheet_Coordinates_Tag9;global worksheet_Coordinates_Tag10;global worksheet_Coordinates_Tag11;
        global worksheet_Coordinates_Tag12;global worksheet_Coordinates_Tag13;global worksheet_Coordinates_Tag14;global worksheet_Coordinates_Tag15;
        global GK1_Game;global GK1_Drill;global WD1_Game;global WD1_Drill;
        global GD1_Game;global GD1_Drill;global C1_Game;global C1_Drill;
        global GA1_Game;global GA1_Drill;global WA1_Game;global WA1_Drill;
        global GS1_Game;global GS1_Drill;global GK2_Game;global GK2_Drill;
        global WD2_Game;global WD2_Drill;global GD2_Game;global GD2_Drill;
        global C2_Game;global C2_Drill;global GA2_Game;global GA2_Drill;
        global WA2_Game;global WA2_Drill;global GS2_Game;global GS2_Drill; global tags; global tag_ids;
        global game_display; global Graphic; global Track_graphic; global Drills_Graphic; global output_value
        
        player = 0
        GK1_Game=0;GK1_Drill=0;
        WD1_Game=0;WD1_Drill=0;
        GD1_Game=0;GD1_Drill=0;
        C1_Game=0;C1_Drill=0;
        GA1_Game=0;GA1_Drill=0;
        WA1_Game=0;WA1_Drill=0;
        GS1_Game=0;GS1_Drill=0;
        GK2_Game=0;GK2_Drill=0;
        WD2_Game=0;WD2_Drill=0;
        GD2_Game=0;GD2_Drill=0;
        C2_Game=0;C2_Drill=0;
        GA2_Game=0;GA2_Drill=0;
        WA2_Game=0;WA2_Drill=0;
        GS2_Game=0;GS2_Drill=0;
    #    print(self.Drill_Choice.currentIndex())
        if self.Drill_Choice.currentIndex()==1:
           self.Athlete_1_Drillcheckbox.setChecked(False)
           self.Athlete_2_Drillcheckbox.setChecked(False)
           self.Athlete_3_Drillcheckbox.setChecked(False)
           self.Athlete_4_Drillcheckbox.setChecked(False)
           self.Athlete_5_Drillcheckbox.setChecked(False)
           self.Athlete_6_Drillcheckbox.setChecked(False)
           self.Athlete_7_Drillcheckbox.setChecked(False)
           self.Athlete_8_Drillcheckbox.setChecked(False)
           self.Athlete_9_Drillcheckbox.setChecked(False)
           self.Athlete_10_Drillcheckbox.setChecked(False)
           self.Athlete_11_Drillcheckbox.setChecked(False)
           self.Athlete_12_Drillcheckbox.setChecked(False)
           self.Athlete_13_Drillcheckbox.setChecked(False)
           self.Athlete_14_Drillcheckbox.setChecked(False)
           self.Drills_Graphic.setPixmap(QPixmap('20m sprint.PNG'))
           self.displayImage()
        if self.Drill_Choice.currentIndex()==2:
           self.Athlete_1_Drillcheckbox.setChecked(False)
           self.Athlete_2_Drillcheckbox.setChecked(False)
           self.Athlete_3_Drillcheckbox.setChecked(False)
           self.Athlete_4_Drillcheckbox.setChecked(False)
           self.Athlete_5_Drillcheckbox.setChecked(False)
           self.Athlete_6_Drillcheckbox.setChecked(False)
           self.Athlete_7_Drillcheckbox.setChecked(False)
           self.Athlete_8_Drillcheckbox.setChecked(False)
           self.Athlete_9_Drillcheckbox.setChecked(False)
           self.Athlete_10_Drillcheckbox.setChecked(False)
           self.Athlete_11_Drillcheckbox.setChecked(False)
           self.Athlete_12_Drillcheckbox.setChecked(False)
           self.Athlete_13_Drillcheckbox.setChecked(False)
           self.Athlete_14_Drillcheckbox.setChecked(False)
           self.Drills_Graphic.setPixmap(QPixmap('Illinois test.PNG'))
           self.displayImage()
        if self.Drill_Choice.currentIndex()==3:
            self.Athlete_1_Drillcheckbox.setDisabled(False)
            self.Athlete_2_Drillcheckbox.setDisabled(False)
            self.Athlete_3_Drillcheckbox.setDisabled(False)
            self.Athlete_4_Drillcheckbox.setDisabled(False)
            self.Athlete_5_Drillcheckbox.setDisabled(False)
            self.Athlete_6_Drillcheckbox.setDisabled(False)
            self.Athlete_7_Drillcheckbox.setDisabled(False)
            self.Athlete_8_Drillcheckbox.setDisabled(False)
            self.Athlete_9_Drillcheckbox.setDisabled(False)
            self.Athlete_10_Drillcheckbox.setDisabled(False)
            self.Athlete_11_Drillcheckbox.setDisabled(False)
            self.Athlete_12_Drillcheckbox.setDisabled(False)
            self.Athlete_13_Drillcheckbox.setDisabled(False)
            self.Athlete_14_Drillcheckbox.setDisabled(False)
            self.Tag_update_Drills.setDisabled(False)
            self.Tag_set_Drills.setDisabled(False)
            self.Set_Tag.setDisabled(True)
            self.Position_Choice.setDisabled(True)
            self.Position_Choice.setCurrentIndex(0)
            self.Drills_Graphic.setPixmap(QPixmap('YO-YO test.PNG'))
            self.displayImage()
        else:
            self.Athlete_1_Drillcheckbox.setDisabled(True)
            self.Athlete_2_Drillcheckbox.setDisabled(True)
            self.Athlete_3_Drillcheckbox.setDisabled(True)
            self.Athlete_4_Drillcheckbox.setDisabled(True)
            self.Athlete_5_Drillcheckbox.setDisabled(True)
            self.Athlete_6_Drillcheckbox.setDisabled(True)
            self.Athlete_7_Drillcheckbox.setDisabled(True)
            self.Athlete_8_Drillcheckbox.setDisabled(True)
            self.Athlete_9_Drillcheckbox.setDisabled(True)
            self.Athlete_10_Drillcheckbox.setDisabled(True)
            self.Athlete_11_Drillcheckbox.setDisabled(True)
            self.Athlete_12_Drillcheckbox.setDisabled(True)
            self.Athlete_13_Drillcheckbox.setDisabled(True)
            self.Athlete_14_Drillcheckbox.setDisabled(True)
            self.Tag_update_Drills.setDisabled(True)
            self.Tag_set_Drills.setDisabled(True)
            self.Position_Choice.setDisabled(False)
            self.Set_Tag.setDisabled(False)
            

                     
    def Load_All_Files(self):
        global file_directory;global Position_G;global Speed_G;global Distance_G;global Acceleration_G;global Metrics_G;global Work_G
        global Output_file_directory
        Output_file_directory = str(QFileDialog.getExistingDirectory())        
        Position_G=0
        Speed_G=0
        Distance_G=0
        Acceleration_G = 0
        Work_G=0
        QListWidgetItem=0
        Metrics_G=0
        self.File_List_Text.clear()
        all_files=os.listdir(Output_file_directory)        
               
        for index in range(len(all_files)):
           File_list=all_files[index]
           self.File_List_Text.addItem(File_list)
    def Load_All_Files2(self):
        global Output_file_directory2; global file_directory; global Output_file_directory;
        global file_directory;global Output_file_directory; global outputfile;global File_list;global File_list_2; global all_files_2; global all_files
        
        Output_file_directory2 = str(QFileDialog.getExistingDirectory())        
        self.File_List_Text_Results.clear()
        self.File_List_Text_Results.clear()
        all_files_2=os.listdir(Output_file_directory2)          
        for index in range(len(all_files_2)):
           File_list_2=all_files_2[index]
           self.File_List_Text_Results.addItem(File_list_2)
           
    def Close_Drills(self):
        global out1; global close_1;global pygaame;global outputfile; global output_value; global pygame

        if output_value == 1:
            outputfile.close()
        Dialog.close()    
    def Close_Results(self):
        global out1; global close_1;global pygaame;global outputfile; global output_value; global pygame

        if output_value == 1:
            outputfile.close()
            
        Dialog.close()
        
    def POZYX_Disconnect(self):
       self.client.loop_stop()
       
############################# Processing #####################################################
    def Process(self):
         global Output_file_directory2; global file_directory; global Output_file_directory; global outputfile; global Frames_persecond_round; global players_ids
         self.completed= 0
         self.start=30
         self.half=50
         self.almost = 80
         count=0
         count2=0
         count3=0
         Hertz=0
         Distance=0
         Distance_prev=0
         count5=0
         row=0
         Frames_persecond=0
         Tag=0
         Team =0
         Tag1=-1
         Tag2=-1
         Tag3=-1
         Tag4=-1
         Tag5=-1
         Tag6=-1
         Tag7=-1
         Tag8=-1
         Tag9=-1
         Tag10=-1
         Tag11=-1
         Tag12=-1
         Tag13=-1
         Tag14=-1

         ###         
         moving_count=0
         work_count = 0
         filtercount=0
         Resultant_1=[]
         Resultant_2=[]
         Resultant_3=[]
         average=[]
         cordinates2=[]
         average1=[]      
         Velocity_persecond=[]
         Acceleration_persecond=[]
         Speed_persecond=[]
         Velocity_persecond1=[]
         Acceleration_persecond1=[]
         Speed_persecond1=[]
         Resultant_diff_persecond=[]
         Resultant_diff_persecond1=[]
         cumsum_time=[]

         Time=[]
         Tag_X=[]          
         Tag_Y=[]
         Player_Tag=[]
         Tag_X_filtered=[]
         Tag_Y_filtered=[]
         b=[]
         a=[]
         Speed=[]
         count_all = []
         Total_Work=[]
        
                     
         if self.Save_PDF_checkbox.isChecked():
             save_PDF=1
         else:
             save_PDF=0
                 
         Output_file_directory2 = str(QFileDialog.getExistingDirectory())
     
         Process_File=self.File_List_Text.selectedIndexes()[0]
         open_file=Output_file_directory + "/" + Process_File.data()
         if save_PDF ==0:
             
             outputfile= xlsxwriter.Workbook(Output_file_directory2 + "/" + "Processed_" + Process_File.data())
             worksheet_Data=outputfile.add_worksheet('Data') ##create excel sheets
             worksheet_Data.write("A1","Time")   
        
             worksheet_Data.write("C1","Total Distance (m)")
    
             worksheet_Data.write("E1","Velocity (m/s)")
             worksheet_Data.write("F1","Acceleration (m/s)")
             
             worksheet_Data.write("H1","Metrics")
             worksheet_Data.write("H3","Velocity")
             worksheet_Data.write("H4","Acceleration")
             worksheet_Data.write("H5","Time")
             worksheet_Data.write("I1","5m")
             worksheet_Data.write("J1","10m")
             worksheet_Data.write("K1","15m")
             worksheet_Data.write("L1","20m")
             worksheet_Data.write("M1","25m")
             worksheet_Data.write("N1","30m")
             worksheet_Data.write("O1","35m")
             worksheet_Data.write("P1","40m")
             worksheet_Data.write("Q1","45m")
             worksheet_Data.write("R1","50m")
             worksheet_Data.write("S1","55m")
             worksheet_Data.write("T1","60m")
             worksheet_Data.write("U1","65m")
             worksheet_Data.write("V1","70m")
             worksheet_Data.write("W1","75m")
             worksheet_Data.write("X1","80m")
             worksheet_Data.write("Y1","85m")
             worksheet_Data.write("Z1","90m")
             worksheet_Data.write("AA1","95m")
             worksheet_Data.write("AB1","100m")
             worksheet_Data.write("AC1","Total Time")
             worksheet_Data.write("AD1","Max")
             worksheet_Data.write("AE1","Mean")
         
         while self.completed <31:
               self.completed += 1
         self.progressBar.setValue (self.completed)
         self.progressBar.setValue (self.start)
         excelfile=pandas.ExcelFile(open_file)
            
         excel_sheetnames=excelfile.sheet_names
         numbers = []
         for item in excel_sheetnames:
            for subitem in item.split("g"):
                if(subitem.isdigit()):
                    numbers.append(subitem)

         numbers=np.array(numbers,dtype=np.float64)
         Number_Tags=numbers.size
         for i in numbers:
             if i ==1:
                 Tag1=0
                 GK='GK'
             elif i ==2:
                 Tag2=1
                 WD='WD'
             elif i ==3:
                 Tag3=2
                 GD='GD'
             elif i ==4:
                 Tag4=3
                 C='C'
             elif i ==5:
                 Tag5=4
                 GA='GA'
             elif i ==6:
                 Tag6=5
                 WA='WA'
             elif i ==7:
                 Tag7=6
                 GS='GS'
             elif i ==8:
                 Tag8=7
                 GK2='GK2'
             elif i ==9:
                 Tag9=8
                 WD2='WD2'
             elif i ==10:
                 Tag10=9
                 GD2='GD2'
             elif i ==11:
                 Tag11=10
                 C2='C2'
             elif i ==12:
                 Tag12=11
                 GA2='GA2'
             elif i ==13:
                 Tag13=12
                 WA2='WA2'
             elif i ==14:
                 Tag14=13
                 GS2='GS2'    
             

         Tag_sheet_map = pandas.read_excel(open_file, sheet_name=None) ####long time for operation
         Tag_dict=list(Tag_sheet_map.items())

    


         for i in range (len(Tag_dict)):
            Time.append(Tag_dict[i][1]["Time"])   #(Time=column, Time[0]=row)
            Time[i].fillna(method='ffill', inplace =True)
            Tag_X.append(Tag_dict[i][1]["X"])
            Tag_X[i].fillna(method='ffill', inplace =True)
            Tag_Y.append(Tag_dict[i][1]["Y"])
            Tag_Y[i].fillna(method='ffill', inplace =True)
            if save_PDF==1:
                Player_Tag.append(Tag_dict[i][1]["Tag"])
                Player_Tag[i].fillna(method='ffill', inplace =True)
            
###   
         Player_Tag=np.array(Player_Tag) # np = (column, row)
         Time=np.array(Time,dtype=np.float64) # np = (column, row)  
         Time_diff=np.diff(Time[0])
         Time_diff1=Time_diff
         Time_diff1=np.array(Time_diff1,dtype=np.float64)
         Time_diff1=np.pad(Time_diff1,(1,0),'reflect')
         Time_diff1=np.transpose(Time_diff1)
         time_plus=0
         Time_new=[]
         Time_length=len(Time[0])
###        
         for i in range(Time_length-1):            
             Time_start=Time[0][i]
             Time_end=Time[0][i+1]
             Time_frame=Time_end-Time_start
             time_plus+=1
             if Time_frame!=0:
                 Time_new.append(time_plus)
                 time_plus=0
###
         Time_new=np.array(Time_new,dtype=np.float64)
         Time_one=np.where(Time_diff==1)
         Time_one=np.array(Time_one,dtype=np.float64)
         Time_one=np.pad(Time_one,[(0,0),(0,1)],'reflect')
         time_count=len(Time[0])
         count_all=list(range(1,time_count+1,1))
         count_all=np.array(count_all,dtype=np.float64)
         unique_elements, counts_elements = np.unique(Time[0], return_counts=True)
         Frames_persecond=np.mean(Time_new) #average FPR
         print("frames:",count_all.size,"seconds:",Time_one.size,"framesP/S:",Frames_persecond)
###
         Tag_X=np.array(Tag_X,dtype=np.float64)         
         Tag_Y=np.array(Tag_Y,dtype=np.float64)
         Resultant_X = sqrt(Tag_X**2)                                                                                        
         Resultant_Y= sqrt(Tag_Y**2)         
         Resultant=Resultant_X-Resultant_Y
         Trial_seconds=count_all/Frames_persecond        
         Trial_seconds=np.round(Trial_seconds,decimals=2)      

###
         print(Number_Tags)
         Frames_persecond=np.mean(Frames_persecond)
         Window_slider=921
         N = Window_slider
         Window_slider=np.array(Window_slider,dtype=np.float64)
         padd=np.round(Window_slider/2,decimals=0)
         padd=int(padd)

         for i in range (len(Tag_dict)):                                                                        #### for each tag pad array
          Resultant_1=np.pad(Resultant,[(0,0),(padd,padd)],'reflect')
###         
         cordinates2=savgol_filter(Resultant_1, N, 3, axis = 1)# window size 101, polynomial order 3
         cordinates2=np.array(cordinates2,dtype=np.float64)
         coordinates_Data=cordinates2[:,padd:-padd]
         coordinates_Data=coordinates_Data/1000 #change fro mm into meters
###      
         Resultant_diff2=np.pad(coordinates_Data,[(0,0),(0,1)],'reflect')
         Resultant_diff=np.diff(Resultant_diff2,axis=1)
         Resultant_diff=np.absolute(Resultant_diff)
         Resultant_diff=np.round(Resultant_diff, decimals = 3)          ###Resultant difference
         
         ###
         if len(Tag_dict) ==1:
             second_length=len(Resultant_diff[0])
             second_length2=list(range(1,second_length+1,1))
             
         else:
             second_length=len(Resultant_diff[1])                                                                    # length of tags recording
             second_length2=list(range(1,second_length+1,1)) 
         
### outlier detection and correction##
         if len(Tag_dict) ==1:
             Resultant_diff[Resultant_diff>=0.015]=np.nan
             idx_finite = np.isfinite(Resultant_diff)
             x = np.linspace(0, second_length, num=second_length, endpoint=True)
             y = Resultant_diff
             f2 = interp1d(x[idx_finite], y[idx_finite], kind='linear')
             xnew = np.linspace(0, second_length, num=second_length, endpoint=True)
             new_res_dif=f2(xnew)
         else:
             new_res_dif=[]
             for i in range (len(Tag_dict)):
                 Resultant_diff[i,:][Resultant_diff[i,:]>=0.015]=np.nan
                 idx_finite = np.isfinite(Resultant_diff[i,:])
                 x = np.linspace(0, second_length, num=second_length, endpoint=True)
                 y = Resultant_diff[i,:]
                 f2 = interp1d(x[idx_finite], y[idx_finite], kind='linear')
                 xnew = np.linspace(0, second_length, num=second_length, endpoint=True)
                 new_res_dif.append(f2(xnew))
             new_res_dif=np.vstack(new_res_dif)
                 
         if len(Tag_dict) ==1:
             Displacement=np.cumsum(new_res_dif)                    ###Displacement
         else:
             Displacement=np.cumsum(new_res_dif,axis=1)
###                                                            # length of tags recording 1:end#
             
         Second_period=count_all.size/Frames_persecond         
         Frames_persecond_round=np.round(Frames_persecond,decimals=0)
         All_frames=second_length2/Frames_persecond_round
###
         
         if len(Tag_dict) ==1:
             Resultant_Velocity2=[]
             Resultant_Acceleration2=[]
             for i in range(second_length):
                 velocity=Displacement/All_frames
                 acceleration=velocity/All_frames
                 Resultant_Velocity2.append(velocity)
                 Resultant_Acceleration2.append(acceleration)
             Resultant_Velocity2=np.array(Resultant_Velocity2,dtype=np.float64)
             Resultant_Acceleration2=np.array(Resultant_Acceleration2,dtype=np.float64)
             Resultant_Velocity=Resultant_Velocity2[0]
             Resultant_Acceleration=Resultant_Acceleration2[0]
               
##         plt.plot(Displacement[4,:])
##         plt.plot(Displacement[5,:])
##         plt.plot(Displacement[6,:])
##         plt.plot(Displacement[7,:])
##         plt.plot(Displacement[8,:])
##         plt.plot(Displacement[9,:])
##         plt.plot(Displacement[10,:])
##         plt.plot(Displacement[11,:])
##         plt.plot(Displacement[12,:])
##         plt.plot(Displacement[13,:])
##         plt.show()
                     
        
         while self.completed <51:
            self.completed += 1
         self.progressBar.setValue (self.completed)
         self.progressBar.setValue (self.half)


#################### one tag a.ka. - sprint or illinois ###############
          
         Tag_A=0;Tag_B=0;Tag_C=0;Tag_D=0;Tag_E=0;Tag_F=0;Tag_G=0;Tag_H=0;Tag_I=0;Tag_J=0;Tag_K=0;Tag_L=0;Tag_M=0;Tag_N=0
         for i in numbers:
             if i ==1:
                 Tag_A = 1 
             if i==2:
                 Tag_B=1
             if i==3:
                 Tag_C=1
             if i==4:
                 Tag_D=1                
             if i==5:
                 Tag_E=1                 
             if i==6:
                 Tag_F=1                 
             if i==7:
                 Tag_G=1               
             if i==8:
                 Tag_H=1                
             if i==9:
                 Tag_I=1               
             if i==10:
                 Tag_J=1                 
             if i==11:
                 Tag_K=1
             if i==12:
                 Tag_L=1
             if i==13:
                 Tag_M=1
             if i==14:
                 Tag_N=1

         players_ids=[]
         players=([Tag_A,Tag_B,Tag_C,Tag_D,Tag_E,Tag_F,Tag_G,Tag_H,Tag_I,Tag_J,Tag_K,Tag_L,Tag_M,Tag_N]) #accessc via[0][#]
         players_ids[:] = (value for value in players if value != 0)
###  
         if Number_Tags ==1 and save_PDF ==0:            # write 1 persons tag         
             second_count=0
             speed=[]
             row4=2
             row5=3
             row6=4
             column3=0
                     
             Distance=Displacement            
             Distance3=Distance
             Distance3=np.round(Distance3, decimals = 0)
             Distance=np.round(Distance, decimals = 2)
             Resultant_Velocity_filt_ms_abs1=Resultant_Velocity
             Resultant_Velocity_filt_ms_abs1=np.round(Resultant_Velocity_filt_ms_abs1, decimals = 2)
             Resultant_Acceleration_abs1=Resultant_Acceleration
             Resultant_Acceleration_abs1=np.round(Resultant_Acceleration_abs1, decimals = 2)
             All_frames_1=np.round(All_frames, decimals = 1)

###

########## Write metrics #############################
           #  print(Distance)     
             dist5=1;dist10=1;dist15=1;dist20=1;dist25=1;dist30=1;dist35=1;dist40=1;dist45=1;dist50=1;dist55=1;dist60=1;dist65=1;dist70=1;dist75=1;
             dist80=1;dist85=1;dist90=1;dist95=1;dist100=1
             for i in range(second_length):
                 if Distance3[i] == 5:
                         if dist5==1:
                             Distance_5_vel=Resultant_Velocity_filt_ms_abs1[i]
                             Distance_5_Acc=Resultant_Acceleration_abs1[i]
                             Second_5m=All_frames_1[i]
                             worksheet_Data.write(row4, column3+8,Distance_5_vel)  ##
                             worksheet_Data.write(row5, column3+8,Distance_5_Acc)#####
                             worksheet_Data.write(row6, column3+8,Second_5m)
                             dist5=0
                         else:
                             pass
                 elif Distance3[i] == 10:
                         if dist10==1:
                             Distance_10_vel=Resultant_Velocity_filt_ms_abs1[i]
                             Distance_10_Acc=Resultant_Acceleration_abs1[i]
                             Second_10m=All_frames_1[i]
                             worksheet_Data.write(row4, column3+9,Distance_10_vel)  ##
                             worksheet_Data.write(row5, column3+9,Distance_10_Acc)#####
                             worksheet_Data.write(row6, column3+9,Second_10m)
                             dist10=0
                         else:
                             pass
                 elif Distance3[i] == 15:
                     if dist15==1:
                         Distance_15_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_15_Acc=Resultant_Acceleration_abs1[i]
                         Second_15m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+10,Distance_15_vel)  ##
                         worksheet_Data.write(row5, column3+10,Distance_15_Acc)#####
                         worksheet_Data.write(row6, column3+10,Second_15m)
                         dist15=0
                     else:
                         pass
                 elif Distance3[i] == 20:
                     if dist20==1:
                         Distance_20_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_20_Acc=Resultant_Acceleration_abs1[i]
                         Second_20m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+11,Distance_20_vel)  ##
                         worksheet_Data.write(row5, column3+11,Distance_20_Acc)#####
                         worksheet_Data.write(row6, column3+11,Second_20m)
                         dist20=0
                     else:
                         pass
                 elif Distance3[i] == 25:
                     if dist25==1:
                         Distance_25_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_25_Acc=Resultant_Acceleration_abs1[i]
                         Second_25m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+12,Distance_25_vel)  ##
                         worksheet_Data.write(row5, column3+12,Distance_25_Acc)#####
                         worksheet_Data.write(row6, column3+12,Second_25m)
                         dist25=0
                     else:
                         pass
                 elif Distance3[i] == 30:
                     if dist30==1:
                         Distance_30_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_30_Acc=Resultant_Acceleration_abs1[i]
                         Second_30m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+13,Distance_30_vel)  ##
                         worksheet_Data.write(row5, column3+13,Distance_30_Acc)#####
                         worksheet_Data.write(row6, column3+13,Second_30m)
                         dist30=0
                     else:
                         pass
                 elif Distance3[i] == 35:
                     if dist35==1:
                         Distance_35_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_35_Acc=Resultant_Acceleration_abs1[i]
                         Second_35m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+14,Distance_35_vel)  ##
                         worksheet_Data.write(row5, column3+14,Distance_35_Acc)#####
                         worksheet_Data.write(row6, column3+14,Second_35m)
                         dist35=0
                     else:
                         pass
                 elif Distance3[i] == 40:
                     if dist40==1:
                         Distance_40_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_40_Acc=Resultant_Acceleration_abs1[i]
                         Second_40m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+15,Distance_40_vel)  ##
                         worksheet_Data.write(row5, column3+15,Distance_40_Acc)#####
                         worksheet_Data.write(row6, column3+15,Second_40m)
                         dist40=0
                     else:
                         pass
                 elif Distance3[i] == 45:
                     if dist45==1:
                         Distance_45_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_45_Acc=Resultant_Acceleration_abs1[i]
                         Second_45m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+16,Distance_45_vel)  ##
                         worksheet_Data.write(row5, column3+16,Distance_45_Acc)#####
                         worksheet_Data.write(row6, column3+16,Second_45m)
                         dist45=0
                     else:
                         pass
                 elif Distance3[i] == 50:
                     if dist50==1:
                         Distance_50_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_50_Acc=Resultant_Acceleration_abs1[i]
                         Second_50m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+17,Distance_50_vel)  ##
                         worksheet_Data.write(row5, column3+17,Distance_50_Acc)#####
                         worksheet_Data.write(row6, column3+17,Second_50m)
                         dist50=0
                     else:
                         pass
                 elif Distance3[i] == 55:
                     if dist55==1:
                         Distance_55_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_55_Acc=Resultant_Acceleration_abs1[i]
                         Second_55m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+18,Distance_55_vel)  ##
                         worksheet_Data.write(row5, column3+18,Distance_55_Acc)#####
                         worksheet_Data.write(row6, column3+18,Second_55m)
                         dist55=0
                     else:
                         pass
                 elif Distance3[i] == 60:
                     if dist60==1:
                         Distance_60_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_60_Acc=Resultant_Acceleration_abs1[i]
                         Second_60m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+19,Distance_60_vel)  ##
                         worksheet_Data.write(row5, column3+19,Distance_60_Acc)#####
                         worksheet_Data.write(row6, column3+19,Second_60m)
                         dist60=0
                     else:
                         pass
                 elif Distance3[i] == 65:
                     if dist65==1:
                         Distance_65_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_65_Acc=Resultant_Acceleration_abs1[i]
                         Second_65m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+20,Distance_65_vel)  ##
                         worksheet_Data.write(row5, column3+20,Distance_65_Acc)#####
                         worksheet_Data.write(row6, column3+20,Second_65m)
                         dist65=0
                     else:
                         pass
                 elif Distance3[i] == 70:
                     if dist70==1:
                         Distance_70_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_70_Acc=Resultant_Acceleration_abs1[i]
                         Second_70m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+21,Distance_70_vel)  ##
                         worksheet_Data.write(row5, column3+21,Distance_70_Acc)#####
                         worksheet_Data.write(row6, column3+21,Second_70m)
                         dist70=0
                     else:
                         pass
                 elif Distance3[i] == 75:
                     if dist75==1:
                         Distance_75_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_75_Acc=Resultant_Acceleration_abs1[i]
                         Second_75m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+22,Distance_75_vel)  ##
                         worksheet_Data.write(row5, column3+22,Distance_75_Acc)#####
                         worksheet_Data.write(row6, column3+22,Second_75m)
                         dist75=0
                     else:
                         pass
                 elif Distance3[i] == 80:
                     if dist80==1:
                         Distance_80_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_80_Acc=Resultant_Acceleration_abs1[i]
                         Second_80m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+23,Distance_80_vel)  ##
                         worksheet_Data.write(row5, column3+23,Distance_80_Acc)#####
                         worksheet_Data.write(row6, column3+23,Second_80m)
                         dist80=0
                     else:
                         pass
                 elif Distance3[i] == 85:
                     if dist85==1:
                         Distance_85_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_85_Acc=Resultant_Acceleration_abs1[i]
                         Second_85m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+24,Distance_85_vel)  ##
                         worksheet_Data.write(row5, column3+24,Distance_85_Acc)#####
                         worksheet_Data.write(row6, column3+24,Second_85m)
                         dist85=0
                     else:
                         pass
                 elif Distance3[i] == 90:
                     if dist90==1:
                         Distance_90_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_90_Acc=Resultant_Acceleration_abs1[i]
                         Second_90m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+25,Distance_90_vel)  ##
                         worksheet_Data.write(row5, column3+25,Distance_90_Acc)#####
                         worksheet_Data.write(row6, column3+25,Second_90m)
                         dist90=0
                     else:
                         pass
                 elif Distance3[i] == 95:
                     if dist95==1:
                         Distance_95_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_95_Acc=Resultant_Acceleration_abs1[i]
                         Second_95m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+26,Distance_95_vel)  ##
                         worksheet_Data.write(row5, column3+26,Distance_95_Acc)#####
                         worksheet_Data.write(row6, column3+26,Second_95m)
                         dist95=0
                     else:
                         pass
                 elif Distance3[i] == 100:
                     if dist100==1:
                         Distance_100_vel=Resultant_Velocity_filt_ms_abs1[i]
                         Distance_100_Acc=Resultant_Acceleration_abs1[i]
                         Second_100m=All_frames_1[i]
                         worksheet_Data.write(row4, column3+27,Distance_100_vel)  ##
                         worksheet_Data.write(row5, column3+27,Distance_100_Acc)#####
                         worksheet_Data.write(row6, column3+27,Second_100m)
                         dist100=0
                     else:
                         pass
  
             worksheet_Data.write(row6, column3+28,Time_one.size)#####
             Resultant_Velocity_max=Resultant_Velocity_filt_ms_abs1.max()
             Resultant_Velocity_mean=Resultant_Velocity_filt_ms_abs1.mean();
             Resultant_Velocity_max=np.round(Resultant_Velocity_max, decimals = 2)
             Resultant_Velocity_mean=np.round(Resultant_Velocity_mean, decimals = 2)
             Resultant_Acceleration_max=Resultant_Acceleration_abs1.max()
             Resultant_Acceleration_mean=Resultant_Acceleration_abs1.mean()
             Resultant_Acceleration_max=np.round(Resultant_Acceleration_max, decimals = 2)
             Resultant_Acceleration_mean=np.round(Resultant_Acceleration_mean, decimals = 2)
             worksheet_Data.write(row4, column3+29,Resultant_Velocity_max)  ##
             worksheet_Data.write(row4, column3+30,Resultant_Velocity_mean)#####
             worksheet_Data.write(row5, column3+29,Resultant_Acceleration_max)  ##
             worksheet_Data.write(row5, column3+30,Resultant_Acceleration_mean)#####

             
             

    
###################################################################################

##### write waveform data ############
             
             Loop_count=Resultant_Velocity_filt_ms_abs1.size
   
             
             row2=0
             column2=0
             row3=0

             for i in range(second_length):
                 worksheet_Data.write(row2+1, column2,Trial_seconds[i])  
                 worksheet_Data.write(row2+1, column2+2,Distance[i]) #distance
                 worksheet_Data.write(row2+1, column2+4,Resultant_Velocity_filt_ms_abs1[i]) #velocity
                 worksheet_Data.write(row2+1, column2+5,Resultant_Acceleration_abs1[i]) #acceleration
                 row2=row2+1

             outputfile.close()
             self.Load_All_Files_Results()
             
                
         while self.completed <81:
            self.completed += 1
         self.progressBar.setValue (self.completed)
         self.progressBar.setValue (self.almost)

####################################################################################################################################################################
####################################################################################################################################################################
####################################################################################################################################################################
####################################################################################################################################################################
####################################################################################################################################################################
###############################################################################################################################################################
####################################################################################################################################################################
####################################################################################################################################################################
####################################################################################################################################################################
####################################################################################################################################################################


                     
                  #   Resultant_Velocity2=np.array(Resultant_Velocity2,dtype=np.float64)                                  
                   #  Resultant_Acceleration2=np.array(Resultant_Acceleration2,dtype=np.float64)    
         # multiple tag processing
         if save_PDF==1:

             
             Tag_A_Velocity_persecond =[];Tag_B_Velocity_persecond =[];Tag_C_Velocity_persecond =[];Tag_D_Velocity_persecond =[];Tag_E_Velocity_persecond =[];
             Tag_F_Velocity_persecond =[];Tag_G_Velocity_persecond =[];Tag_H_Velocity_persecond =[];Tag_I_Velocity_persecond =[];Tag_J_Velocity_persecond =[];
             Tag_K_Velocity_persecond =[];Tag_L_Velocity_persecond =[];Tag_M_Velocity_persecond =[];Tag_N_Velocity_persecond =[];
             
             Tag_A_Acceleration_persecond =[];Tag_B_Acceleration_persecond =[];Tag_C_Acceleration_persecond =[];Tag_D_Acceleration_persecond =[];Tag_E_Acceleration_persecond =[];
             Tag_F_Acceleration_persecond =[];Tag_G_Acceleration_persecond =[];Tag_H_Acceleration_persecond =[];Tag_I_Acceleration_persecond =[];Tag_J_Acceleration_persecond =[];
             Tag_K_Acceleration_persecond =[];Tag_L_Acceleration_persecond =[];Tag_M_Acceleration_persecond =[];Tag_N_Acceleration_persecond =[];
             
             Tag_A_Speed_persecond =[];Tag_B_Speed_persecond =[];Tag_C_Speed_persecond =[];Tag_D_Speed_persecond =[];Tag_E_Speed_persecond =[];
             Tag_F_Speed_persecond =[];Tag_G_Speed_persecond =[];Tag_H_Speed_persecond =[];Tag_I_Speed_persecond =[];Tag_J_Speed_persecond =[];
             Tag_K_Speed_persecond =[];Tag_L_Speed_persecond =[];Tag_M_Speed_persecond =[];Tag_N_Speed_persecond =[];

             Tag_A_Resultant_diff_persecond =[];Tag_B_Resultant_diff_persecond =[];Tag_C_Resultant_diff_persecond =[];Tag_D_Resultant_diff_persecond =[];Tag_E_Resultant_diff_persecond =[];
             Tag_F_Resultant_diff_persecond =[];Tag_G_Resultant_diff_persecond =[];Tag_H_Resultant_diff_persecond =[];Tag_I_Resultant_diff_persecond =[];Tag_J_Resultant_diff_persecond =[];
             Tag_K_Resultant_diff_persecond =[];Tag_L_Resultant_diff_persecond =[];Tag_M_Resultant_diff_persecond =[];Tag_N_Resultant_diff_persecond =[];
             
             for j in range (len(Tag_dict)):
                 work_count=0
                 Tag_Count=0
                 for i in range(second_length):                                                                         # for length of seconds
                     work_count +=1
                     if work_count == Frames_persecond_round:           
                         work_count=-1
                         while j ==0:
                             Tag_Count=Tag_Count+1
                             Tag_A_Velocity_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_A_Velocity_persecond2=Displacement[j,i]/All_frames[i]
                             Tag_A_Acceleration_persecond.append(Tag_A_Velocity_persecond2/All_frames[i])                   
                             Tag_A_Speed_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_A_Resultant_diff_persecond.append(Displacement[j,i])
                             break;                
                         while j ==1:
                             Tag_Count=Tag_Count+1
                             Tag_B_Velocity_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_B_Velocity_persecond2=Displacement[j,i]/All_frames[i]
                             Tag_B_Acceleration_persecond.append(Tag_B_Velocity_persecond2/All_frames[i])                   
                             Tag_B_Speed_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_B_Resultant_diff_persecond.append(Displacement[j,i])                       
                             break;
                         while j ==2:
                             Tag_Count=Tag_Count+1
                             Tag_C_Velocity_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_C_Velocity_persecond2=Displacement[j,i]/All_frames[i]
                             Tag_C_Acceleration_persecond.append(Tag_C_Velocity_persecond2/All_frames[i])                   
                             Tag_C_Speed_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_C_Resultant_diff_persecond.append(Displacement[j,i])                         
                             break;
                         while j ==3:
                             Tag_Count=Tag_Count+1
                             Tag_D_Velocity_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_D_Velocity_persecond2=Displacement[j,i]/All_frames[i]
                             Tag_D_Acceleration_persecond.append(Tag_D_Velocity_persecond2/All_frames[i])                   
                             Tag_D_Speed_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_D_Resultant_diff_persecond.append(Displacement[j,i])                        
                             break;
                         while j ==4:
                             Tag_Count=Tag_Count+1
                             Tag_E_Velocity_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_E_Velocity_persecond2=Displacement[j,i]/All_frames[i]
                             Tag_E_Acceleration_persecond.append(Tag_E_Velocity_persecond2/All_frames[i])                   
                             Tag_E_Speed_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_E_Resultant_diff_persecond.append(Displacement[j,i])                        
                             break;
                         while j ==5:
                             Tag_Count=Tag_Count+1
                             Tag_F_Velocity_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_F_Velocity_persecond2=Displacement[j,i]/All_frames[i]
                             Tag_F_Acceleration_persecond.append(Tag_F_Velocity_persecond2/All_frames[i])                   
                             Tag_F_Speed_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_F_Resultant_diff_persecond.append(Displacement[j,i])                         
                             break;
                         while j ==6:
                             Tag_Count=Tag_Count+1
                             Tag_G_Velocity_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_G_Velocity_persecond2=Displacement[j,i]/All_frames[i]
                             Tag_G_Acceleration_persecond.append(Tag_G_Velocity_persecond2/All_frames[i])                   
                             Tag_G_Speed_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_G_Resultant_diff_persecond.append(Displacement[j,i])                      
                             break;
                         while j ==7:
                             Tag_Count=Tag_Count+1
                             Tag_H_Velocity_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_H_Velocity_persecond2=Displacement[j,i]/All_frames[i]
                             Tag_H_Acceleration_persecond.append(Tag_H_Velocity_persecond2/All_frames[i])                   
                             Tag_H_Speed_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_H_Resultant_diff_persecond.append(Displacement[j,i])                         
                             break;
                         while j ==8:
                             Tag_Count=Tag_Count+1
                             Tag_I_Velocity_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_I_Velocity_persecond2=Displacement[j,i]/All_frames[i]
                             Tag_I_Acceleration_persecond.append(Tag_I_Velocity_persecond2/All_frames[i])                   
                             Tag_I_Speed_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_I_Resultant_diff_persecond.append(Displacement[j,i])                        
                             break;
                         while j ==9:
                             Tag_Count=Tag_Count+1
                             Tag_J_Velocity_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_J_Velocity_persecond2=Displacement[j,i]/All_frames[i]
                             Tag_J_Acceleration_persecond.append(Tag_J_Velocity_persecond2/All_frames[i])                   
                             Tag_J_Speed_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_J_Resultant_diff_persecond.append(Displacement[j,i])                         
                             break;
                         while j ==10:
                             Tag_Count=Tag_Count+1
                             Tag_K_Velocity_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_K_Velocity_persecond2=Displacement[j,i]/All_frames[i]
                             Tag_K_Acceleration_persecond.append(Tag_K_Velocity_persecond2/All_frames[i])                   
                             Tag_K_Speed_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_K_Resultant_diff_persecond.append(Displacement[j,i])                        
                             break; 
                         while j ==11:
                             Tag_Count=Tag_Count+1
                             Tag_L_Velocity_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_L_Velocity_persecond2=Displacement[j,i]/All_frames[i]
                             Tag_L_Acceleration_persecond.append(Tag_L_Velocity_persecond2/All_frames[i])                   
                             Tag_L_Speed_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_L_Resultant_diff_persecond.append(Displacement[j,i])                         
                             break;
                         while j ==12:
                             Tag_Count=Tag_Count+1
                             Tag_M_Velocity_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_M_Velocity_persecond2=Displacement[j,i]/All_frames[i]
                             Tag_M_Acceleration_persecond.append(Tag_M_Velocity_persecond2/All_frames[i])                   
                             Tag_M_Speed_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_M_Resultant_diff_persecond.append(Displacement[j,i])                         
                             break;
                         while j ==13:                         
                             Tag_Count=Tag_Count+1
                             Tag_N_Velocity_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_N_Velocity_persecond2=Displacement[j,i]/All_frames[i]
                             Tag_N_Acceleration_persecond.append(Tag_N_Velocity_persecond2/All_frames[i])                   
                             Tag_N_Speed_persecond.append(Displacement[j,i]/All_frames[i])
                             Tag_N_Resultant_diff_persecond.append(Displacement[j,i])
                             break;

### all of this dependant on correct calculation above~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#######################################################
             print("WORKS")               
    ###velocity transforms ###
             
             Tag_A_Velocity_persecond=np.array(Tag_A_Velocity_persecond,dtype=np.float64);Tag_A_Velocity_persecond=np.transpose(Tag_A_Velocity_persecond);
             Tag_B_Velocity_persecond=np.array(Tag_B_Velocity_persecond,dtype=np.float64);Tag_B_Velocity_persecond=np.transpose(Tag_B_Velocity_persecond);
             Tag_C_Velocity_persecond=np.array(Tag_C_Velocity_persecond,dtype=np.float64);Tag_C_Velocity_persecond=np.transpose(Tag_C_Velocity_persecond);
             Tag_D_Velocity_persecond=np.array(Tag_D_Velocity_persecond,dtype=np.float64);Tag_D_Velocity_persecond=np.transpose(Tag_D_Velocity_persecond);             
             Tag_E_Velocity_persecond=np.array(Tag_E_Velocity_persecond,dtype=np.float64);Tag_E_Velocity_persecond=np.transpose(Tag_E_Velocity_persecond);             
             Tag_F_Velocity_persecond=np.array(Tag_F_Velocity_persecond,dtype=np.float64);Tag_F_Velocity_persecond=np.transpose(Tag_F_Velocity_persecond);
             Tag_G_Velocity_persecond=np.array(Tag_G_Velocity_persecond,dtype=np.float64);Tag_G_Velocity_persecond=np.transpose(Tag_G_Velocity_persecond);             
             Tag_H_Velocity_persecond=np.array(Tag_H_Velocity_persecond,dtype=np.float64);Tag_H_Velocity_persecond=np.transpose(Tag_H_Velocity_persecond);             
             Tag_I_Velocity_persecond=np.array(Tag_I_Velocity_persecond,dtype=np.float64);Tag_I_Velocity_persecond=np.transpose(Tag_I_Velocity_persecond);
             Tag_J_Velocity_persecond=np.array(Tag_J_Velocity_persecond,dtype=np.float64);Tag_J_Velocity_persecond=np.transpose(Tag_J_Velocity_persecond);             
             Tag_K_Velocity_persecond=np.array(Tag_K_Velocity_persecond,dtype=np.float64);Tag_K_Velocity_persecond=np.transpose(Tag_K_Velocity_persecond);             
             Tag_L_Velocity_persecond=np.array(Tag_L_Velocity_persecond,dtype=np.float64);Tag_L_Velocity_persecond=np.transpose(Tag_L_Velocity_persecond);
             Tag_M_Velocity_persecond=np.array(Tag_M_Velocity_persecond,dtype=np.float64);Tag_M_Velocity_persecond=np.transpose(Tag_M_Velocity_persecond);             
             Tag_N_Velocity_persecond=np.array(Tag_N_Velocity_persecond,dtype=np.float64);Tag_N_Velocity_persecond=np.transpose(Tag_N_Velocity_persecond);             
       
             Velocity_persecond=Tag_A_Velocity_persecond
             Tag_A_Resultant_Velocity_max=Velocity_persecond.max()
             Tag_A_Resultant_Velocity_mean=Velocity_persecond.mean()
             Resultant_Velocity_max=Tag_A_Resultant_Velocity_max
             Resultant_Velocity_mean=Tag_A_Resultant_Velocity_mean

             if len(Tag_B_Velocity_persecond)>0:
                    Velocity_persecond=[]
                    Resultant_Velocity_max=[]
                    Resultant_Velocity_mean=[]
                    Velocity_persecond=np.vstack([Tag_A_Velocity_persecond,Tag_B_Velocity_persecond])    
                    Tag_B_Resultant_Velocity_max=(Velocity_persecond[1,:].max())
                    Tag_B_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean())
                    Resultant_Velocity_max=np.vstack([Tag_A_Resultant_Velocity_max,Tag_B_Resultant_Velocity_max])
                    Resultant_Velocity_mean=np.vstack([Tag_A_Resultant_Velocity_mean,Tag_B_Resultant_Velocity_mean])
             else:
                    pass

             if len(Tag_C_Velocity_persecond)>0:
                    Velocity_persecond=[]
                    Resultant_Velocity_max=[]
                    Resultant_Velocity_mean=[]
                    Velocity_persecond=np.vstack([Tag_A_Velocity_persecond,Tag_B_Velocity_persecond,Tag_C_Velocity_persecond])
                    Tag_B_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_B_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                    Tag_C_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_C_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                    Resultant_Velocity_max=np.vstack([Tag_A_Resultant_Velocity_max,Tag_B_Resultant_Velocity_max,Tag_C_Resultant_Velocity_max])
                    Resultant_Velocity_mean=np.vstack([Tag_A_Resultant_Velocity_mean,Tag_B_Resultant_Velocity_mean,Tag_C_Resultant_Velocity_mean])
             else:
                    pass
             if len(Tag_D_Velocity_persecond)>0:
                    Velocity_persecond=[]
                    Resultant_Velocity_max=[]
                    Resultant_Velocity_mean=[]
                    Velocity_persecond=np.vstack([Tag_A_Velocity_persecond,Tag_B_Velocity_persecond,Tag_C_Velocity_persecond,Tag_D_Velocity_persecond])
                    Tag_B_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_B_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                    Tag_C_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_C_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                    Tag_D_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_D_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                    Resultant_Velocity_max=np.vstack([Tag_A_Resultant_Velocity_max,Tag_B_Resultant_Velocity_max,Tag_C_Resultant_Velocity_max,Tag_D_Resultant_Velocity_max])
                    Resultant_Velocity_mean=np.vstack([Tag_A_Resultant_Velocity_mean,Tag_B_Resultant_Velocity_mean,Tag_C_Resultant_Velocity_mean,Tag_D_Resultant_Velocity_mean])
             else:
                    pass
             if len(Tag_E_Velocity_persecond)>0:
                    Velocity_persecond=[]
                    Resultant_Velocity_max=[]
                    Resultant_Velocity_mean=[]
                    Velocity_persecond=np.vstack([Tag_A_Velocity_persecond,Tag_B_Velocity_persecond,Tag_C_Velocity_persecond,Tag_D_Velocity_persecond,
                                                     Tag_E_Velocity_persecond])
                    Tag_B_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_B_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                    Tag_C_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_C_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                    Tag_D_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_D_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                    Tag_E_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_E_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                    Resultant_Velocity_max=np.vstack([Tag_A_Resultant_Velocity_max,Tag_B_Resultant_Velocity_max,Tag_C_Resultant_Velocity_max,Tag_D_Resultant_Velocity_max,
                                                     Tag_E_Resultant_Velocity_max])
                    Resultant_Velocity_mean=np.vstack([Tag_A_Resultant_Velocity_mean,Tag_B_Resultant_Velocity_mean,Tag_C_Resultant_Velocity_mean,Tag_D_Resultant_Velocity_mean,
                                                     Tag_E_Resultant_Velocity_mean])
             else:
                    pass
             if len(Tag_F_Velocity_persecond)>0:
                    Velocity_persecond=[]
                    Resultant_Velocity_max=[]
                    Resultant_Velocity_mean=[]
                    Velocity_persecond=np.vstack([Tag_A_Velocity_persecond,Tag_B_Velocity_persecond,Tag_C_Velocity_persecond,Tag_D_Velocity_persecond,
                                                     Tag_E_Velocity_persecond,Tag_F_Velocity_persecond])
                    Tag_B_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_B_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                    Tag_C_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_C_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                    Tag_D_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_D_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                    Tag_E_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_E_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                    Tag_F_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_F_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                    Resultant_Velocity_max=np.vstack([Tag_A_Resultant_Velocity_max,Tag_B_Resultant_Velocity_max,Tag_C_Resultant_Velocity_max,Tag_D_Resultant_Velocity_max,
                                                     Tag_E_Resultant_Velocity_max,Tag_F_Resultant_Velocity_max])
                    Resultant_Velocity_mean=np.vstack([Tag_A_Resultant_Velocity_mean,Tag_B_Resultant_Velocity_mean,Tag_C_Resultant_Velocity_mean,Tag_D_Resultant_Velocity_mean,
                                                     Tag_E_Resultant_Velocity_mean,Tag_F_Resultant_Velocity_mean])
             else:
                    pass
             if len(Tag_G_Velocity_persecond)>0:
                    Velocity_persecond=[]
                    Resultant_Velocity_max=[]
                    Resultant_Velocity_mean=[]
                    Velocity_persecond=np.vstack([Tag_A_Velocity_persecond,Tag_B_Velocity_persecond,Tag_C_Velocity_persecond,Tag_D_Velocity_persecond,
                                                     Tag_E_Velocity_persecond,Tag_F_Velocity_persecond,Tag_G_Velocity_persecond])
                    Tag_B_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_B_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                    Tag_C_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_C_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                    Tag_D_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_D_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                    Tag_E_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_E_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                    Tag_F_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_F_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                    Tag_G_Resultant_Velocity_max=(Velocity_persecond[6,:].max());Tag_G_Resultant_Velocity_mean=(Velocity_persecond[6,:].mean());
                    Resultant_Velocity_max=np.vstack([Tag_A_Resultant_Velocity_max,Tag_B_Resultant_Velocity_max,Tag_C_Resultant_Velocity_max,Tag_D_Resultant_Velocity_max,
                                                     Tag_E_Resultant_Velocity_max,Tag_F_Resultant_Velocity_max,Tag_G_Resultant_Velocity_max])
                    Resultant_Velocity_mean=np.vstack([Tag_A_Resultant_Velocity_mean,Tag_B_Resultant_Velocity_mean,Tag_C_Resultant_Velocity_mean,Tag_D_Resultant_Velocity_mean,
                                                     Tag_E_Resultant_Velocity_mean,Tag_F_Resultant_Velocity_mean,Tag_G_Resultant_Velocity_mean])
     
             else:
                    pass
             if len(Tag_H_Velocity_persecond)>0:
                    Velocity_persecond=[]
                    Resultant_Velocity_max=[]
                    Resultant_Velocity_mean=[]
                    Velocity_persecond=np.vstack([Tag_A_Velocity_persecond,Tag_B_Velocity_persecond,Tag_C_Velocity_persecond,Tag_D_Velocity_persecond,
                                                     Tag_E_Velocity_persecond,Tag_F_Velocity_persecond,Tag_G_Velocity_persecond,Tag_H_Velocity_persecond])
                    Tag_B_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_B_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                    Tag_C_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_C_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                    Tag_D_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_D_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                    Tag_E_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_E_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                    Tag_F_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_F_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                    Tag_G_Resultant_Velocity_max=(Velocity_persecond[6,:].max());Tag_G_Resultant_Velocity_mean=(Velocity_persecond[6,:].mean());
                    Tag_H_Resultant_Velocity_max=(Velocity_persecond[7,:].max());Tag_H_Resultant_Velocity_mean=(Velocity_persecond[7,:].mean());
                    Resultant_Velocity_max=np.vstack([Tag_A_Resultant_Velocity_max,Tag_B_Resultant_Velocity_max,Tag_C_Resultant_Velocity_max,Tag_D_Resultant_Velocity_max,
                                                     Tag_E_Resultant_Velocity_max,Tag_F_Resultant_Velocity_max,Tag_G_Resultant_Velocity_max,Tag_H_Resultant_Velocity_max])
                    Resultant_Velocity_mean=np.vstack([Tag_A_Resultant_Velocity_mean,Tag_B_Resultant_Velocity_mean,Tag_C_Resultant_Velocity_mean,Tag_D_Resultant_Velocity_mean,
                                                     Tag_E_Resultant_Velocity_mean,Tag_F_Resultant_Velocity_mean,Tag_G_Resultant_Velocity_mean,Tag_H_Resultant_Velocity_mean])
             else:
                    pass
             if len(Tag_I_Velocity_persecond)>0:
                    Velocity_persecond=[]
                    Resultant_Velocity_max=[]
                    Resultant_Velocity_mean=[]
                    Velocity_persecond=np.vstack([Tag_A_Velocity_persecond,Tag_B_Velocity_persecond,Tag_C_Velocity_persecond,Tag_D_Velocity_persecond,
                                                     Tag_E_Velocity_persecond,Tag_F_Velocity_persecond,Tag_G_Velocity_persecond,Tag_H_Velocity_persecond,
                                                     Tag_I_Velocity_persecond])
                    Tag_B_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_B_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                    Tag_C_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_C_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                    Tag_D_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_D_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                    Tag_E_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_E_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                    Tag_F_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_F_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                    Tag_G_Resultant_Velocity_max=(Velocity_persecond[6,:].max());Tag_G_Resultant_Velocity_mean=(Velocity_persecond[6,:].mean());
                    Tag_H_Resultant_Velocity_max=(Velocity_persecond[7,:].max());Tag_H_Resultant_Velocity_mean=(Velocity_persecond[7,:].mean());
                    Tag_I_Resultant_Velocity_max=(Velocity_persecond[8,:].max());Tag_I_Resultant_Velocity_mean=(Velocity_persecond[8,:].mean());
                    Resultant_Velocity_max=np.vstack([Tag_A_Resultant_Velocity_max,Tag_B_Resultant_Velocity_max,Tag_C_Resultant_Velocity_max,Tag_D_Resultant_Velocity_max,
                                                     Tag_E_Resultant_Velocity_max,Tag_F_Resultant_Velocity_max,Tag_G_Resultant_Velocity_max,Tag_H_Resultant_Velocity_max,
                                                     Tag_I_Resultant_Velocity_max])
                    Resultant_Velocity_mean=np.vstack([Tag_A_Resultant_Velocity_mean,Tag_B_Resultant_Velocity_mean,Tag_C_Resultant_Velocity_mean,Tag_D_Resultant_Velocity_mean,
                                                     Tag_E_Resultant_Velocity_mean,Tag_F_Resultant_Velocity_mean,Tag_G_Resultant_Velocity_mean,Tag_H_Resultant_Velocity_mean,
                                                     Tag_I_Resultant_Velocity_mean])
             else:
                    pass
             if len(Tag_J_Velocity_persecond)>0:
                    Velocity_persecond=[]
                    Resultant_Velocity_max=[]
                    Resultant_Velocity_mean=[]
                    Velocity_persecond=np.vstack([Tag_A_Velocity_persecond,Tag_B_Velocity_persecond,Tag_C_Velocity_persecond,Tag_D_Velocity_persecond,
                                                     Tag_E_Velocity_persecond,Tag_F_Velocity_persecond,Tag_G_Velocity_persecond,Tag_H_Velocity_persecond,
                                                     Tag_I_Velocity_persecond,Tag_J_Velocity_persecond])
                    Tag_B_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_B_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                    Tag_C_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_C_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                    Tag_D_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_D_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                    Tag_E_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_E_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                    Tag_F_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_F_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                    Tag_G_Resultant_Velocity_max=(Velocity_persecond[6,:].max());Tag_G_Resultant_Velocity_mean=(Velocity_persecond[6,:].mean());
                    Tag_H_Resultant_Velocity_max=(Velocity_persecond[7,:].max());Tag_H_Resultant_Velocity_mean=(Velocity_persecond[7,:].mean());
                    Tag_I_Resultant_Velocity_max=(Velocity_persecond[8,:].max());Tag_I_Resultant_Velocity_mean=(Velocity_persecond[8,:].mean());
                    Tag_J_Resultant_Velocity_max=(Velocity_persecond[9,:].max());Tag_J_Resultant_Velocity_mean=(Velocity_persecond[9,:].mean());
                    Resultant_Velocity_max=np.vstack([Tag_A_Resultant_Velocity_max,Tag_B_Resultant_Velocity_max,Tag_C_Resultant_Velocity_max,Tag_D_Resultant_Velocity_max,
                                                     Tag_E_Resultant_Velocity_max,Tag_F_Resultant_Velocity_max,Tag_G_Resultant_Velocity_max,Tag_H_Resultant_Velocity_max,
                                                     Tag_I_Resultant_Velocity_max,Tag_J_Resultant_Velocity_max])
                    Resultant_Velocity_mean=np.vstack([Tag_A_Resultant_Velocity_mean,Tag_B_Resultant_Velocity_mean,Tag_C_Resultant_Velocity_mean,Tag_D_Resultant_Velocity_mean,
                                                     Tag_E_Resultant_Velocity_mean,Tag_F_Resultant_Velocity_mean,Tag_G_Resultant_Velocity_mean,Tag_H_Resultant_Velocity_mean,
                                                     Tag_I_Resultant_Velocity_mean,Tag_J_Resultant_Velocity_mean])         
            
             else:
                    pass
             if len(Tag_K_Velocity_persecond)>0:
                    Velocity_persecond=[]
                    Resultant_Velocity_max=[]
                    Resultant_Velocity_mean=[]

                    Velocity_persecond=np.vstack([Tag_A_Velocity_persecond,Tag_B_Velocity_persecond,Tag_C_Velocity_persecond,Tag_D_Velocity_persecond,
                                                     Tag_E_Velocity_persecond,Tag_F_Velocity_persecond,Tag_G_Velocity_persecond,Tag_H_Velocity_persecond,
                                                     Tag_I_Velocity_persecond,Tag_J_Velocity_persecond,Tag_K_Velocity_persecond])
                    Tag_B_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_B_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                    Tag_C_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_C_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                    Tag_D_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_D_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                    Tag_E_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_E_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                    Tag_F_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_F_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                    Tag_G_Resultant_Velocity_max=(Velocity_persecond[6,:].max());Tag_G_Resultant_Velocity_mean=(Velocity_persecond[6,:].mean());
                    Tag_H_Resultant_Velocity_max=(Velocity_persecond[7,:].max());Tag_H_Resultant_Velocity_mean=(Velocity_persecond[7,:].mean());
                    Tag_I_Resultant_Velocity_max=(Velocity_persecond[8,:].max());Tag_I_Resultant_Velocity_mean=(Velocity_persecond[8,:].mean());
                    Tag_J_Resultant_Velocity_max=(Velocity_persecond[9,:].max());Tag_J_Resultant_Velocity_mean=(Velocity_persecond[9,:].mean());
                    Tag_K_Resultant_Velocity_max=(Velocity_persecond[10,:].max());Tag_K_Resultant_Velocity_mean=(Velocity_persecond[10,:].mean());
                    Resultant_Velocity_max=np.vstack([Tag_A_Resultant_Velocity_max,Tag_B_Resultant_Velocity_max,Tag_C_Resultant_Velocity_max,Tag_D_Resultant_Velocity_max,
                                                     Tag_E_Resultant_Velocity_max,Tag_F_Resultant_Velocity_max,Tag_G_Resultant_Velocity_max,Tag_H_Resultant_Velocity_max,
                                                     Tag_I_Resultant_Velocity_max,Tag_J_Resultant_Velocity_max,Tag_K_Resultant_Velocity_max])
                    Resultant_Velocity_mean=np.vstack([Tag_A_Resultant_Velocity_mean,Tag_B_Resultant_Velocity_mean,Tag_C_Resultant_Velocity_mean,Tag_D_Resultant_Velocity_mean,
                                                     Tag_E_Resultant_Velocity_mean,Tag_F_Resultant_Velocity_mean,Tag_G_Resultant_Velocity_mean,Tag_H_Resultant_Velocity_mean,
                                                     Tag_I_Resultant_Velocity_mean,Tag_J_Resultant_Velocity_mean,Tag_K_Resultant_Velocity_mean])         
             else:
                    pass
             if len(Tag_L_Velocity_persecond)>0:
                    Velocity_persecond=[]
                    Resultant_Velocity_max=[]
                    Resultant_Velocity_mean=[]

                    Velocity_persecond=np.vstack([Tag_A_Velocity_persecond,Tag_B_Velocity_persecond,Tag_C_Velocity_persecond,Tag_D_Velocity_persecond,
                                                     Tag_E_Velocity_persecond,Tag_F_Velocity_persecond,Tag_G_Velocity_persecond,Tag_H_Velocity_persecond,
                                                     Tag_I_Velocity_persecond,Tag_J_Velocity_persecond,Tag_K_Velocity_persecond,Tag_L_Velocity_persecond])
                    Tag_B_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_B_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                    Tag_C_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_C_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                    Tag_D_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_D_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                    Tag_E_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_E_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                    Tag_F_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_F_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                    Tag_G_Resultant_Velocity_max=(Velocity_persecond[6,:].max());Tag_G_Resultant_Velocity_mean=(Velocity_persecond[6,:].mean());
                    Tag_H_Resultant_Velocity_max=(Velocity_persecond[7,:].max());Tag_H_Resultant_Velocity_mean=(Velocity_persecond[7,:].mean());
                    Tag_I_Resultant_Velocity_max=(Velocity_persecond[8,:].max());Tag_I_Resultant_Velocity_mean=(Velocity_persecond[8,:].mean());
                    Tag_J_Resultant_Velocity_max=(Velocity_persecond[9,:].max());Tag_J_Resultant_Velocity_mean=(Velocity_persecond[9,:].mean());
                    Tag_K_Resultant_Velocity_max=(Velocity_persecond[10,:].max());Tag_K_Resultant_Velocity_mean=(Velocity_persecond[10,:].mean());
                    Tag_L_Resultant_Velocity_max=(Velocity_persecond[11,:].max());Tag_L_Resultant_Velocity_mean=(Velocity_persecond[11,:].mean());
                    Resultant_Velocity_max=np.vstack([Tag_A_Resultant_Velocity_max,Tag_B_Resultant_Velocity_max,Tag_C_Resultant_Velocity_max,Tag_D_Resultant_Velocity_max,
                                                     Tag_E_Resultant_Velocity_max,Tag_F_Resultant_Velocity_max,Tag_G_Resultant_Velocity_max,Tag_H_Resultant_Velocity_max,
                                                     Tag_I_Resultant_Velocity_max,Tag_J_Resultant_Velocity_max,Tag_K_Resultant_Velocity_max,Tag_L_Resultant_Velocity_max])
                    Resultant_Velocity_mean=np.vstack([Tag_A_Resultant_Velocity_mean,Tag_B_Resultant_Velocity_mean,Tag_C_Resultant_Velocity_mean,Tag_D_Resultant_Velocity_mean,
                                                     Tag_E_Resultant_Velocity_mean,Tag_F_Resultant_Velocity_mean,Tag_G_Resultant_Velocity_mean,Tag_H_Resultant_Velocity_mean,
                                                     Tag_I_Resultant_Velocity_mean,Tag_J_Resultant_Velocity_mean,Tag_K_Resultant_Velocity_mean,Tag_L_Resultant_Velocity_mean])
             else:
                    pass
             if len(Tag_M_Velocity_persecond)>0:
                    Velocity_persecond=[]
                    Resultant_Velocity_max=[]
                    Resultant_Velocity_mean=[]

                    Velocity_persecond=np.vstack([Tag_A_Velocity_persecond,Tag_B_Velocity_persecond,Tag_C_Velocity_persecond,Tag_D_Velocity_persecond,
                                                     Tag_E_Velocity_persecond,Tag_F_Velocity_persecond,Tag_G_Velocity_persecond,Tag_H_Velocity_persecond,
                                                     Tag_I_Velocity_persecond,Tag_J_Velocity_persecond,Tag_K_Velocity_persecond,Tag_L_Velocity_persecond,
                                                     Tag_M_Velocity_persecond])
                    Tag_B_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_B_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                    Tag_C_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_C_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                    Tag_D_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_D_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                    Tag_E_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_E_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                    Tag_F_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_F_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                    Tag_G_Resultant_Velocity_max=(Velocity_persecond[6,:].max());Tag_G_Resultant_Velocity_mean=(Velocity_persecond[6,:].mean());
                    Tag_H_Resultant_Velocity_max=(Velocity_persecond[7,:].max());Tag_H_Resultant_Velocity_mean=(Velocity_persecond[7,:].mean());
                    Tag_I_Resultant_Velocity_max=(Velocity_persecond[8,:].max());Tag_I_Resultant_Velocity_mean=(Velocity_persecond[8,:].mean());
                    Tag_J_Resultant_Velocity_max=(Velocity_persecond[9,:].max());Tag_J_Resultant_Velocity_mean=(Velocity_persecond[9,:].mean());
                    Tag_K_Resultant_Velocity_max=(Velocity_persecond[10,:].max());Tag_K_Resultant_Velocity_mean=(Velocity_persecond[10,:].mean());
                    Tag_L_Resultant_Velocity_max=(Velocity_persecond[11,:].max());Tag_L_Resultant_Velocity_mean=(Velocity_persecond[11,:].mean());
                    Tag_M_Resultant_Velocity_max=(Velocity_persecond[12,:].max());Tag_M_Resultant_Velocity_mean=(Velocity_persecond[12,:].mean());
                    Resultant_Velocity_max=np.vstack([Tag_A_Resultant_Velocity_max,Tag_B_Resultant_Velocity_max,Tag_C_Resultant_Velocity_max,Tag_D_Resultant_Velocity_max,
                                                     Tag_E_Resultant_Velocity_max,Tag_F_Resultant_Velocity_max,Tag_G_Resultant_Velocity_max,Tag_H_Resultant_Velocity_max,
                                                     Tag_I_Resultant_Velocity_max,Tag_J_Resultant_Velocity_max,Tag_K_Resultant_Velocity_max,Tag_L_Resultant_Velocity_max,
                                                     Tag_M_Resultant_Velocity_max])
                    Resultant_Velocity_mean=np.vstack([Tag_A_Resultant_Velocity_mean,Tag_B_Resultant_Velocity_mean,Tag_C_Resultant_Velocity_mean,Tag_D_Resultant_Velocity_mean,
                                                     Tag_E_Resultant_Velocity_mean,Tag_F_Resultant_Velocity_mean,Tag_G_Resultant_Velocity_mean,Tag_H_Resultant_Velocity_mean,
                                                     Tag_I_Resultant_Velocity_mean,Tag_J_Resultant_Velocity_mean,Tag_K_Resultant_Velocity_mean,Tag_L_Resultant_Velocity_mean,
                                                     Tag_M_Resultant_Velocity_mean])
             else:
                    pass
             if len(Tag_N_Velocity_persecond)>0:
                    Velocity_persecond=[]
                    Resultant_Velocity_max=[]
                    Resultant_Velocity_mean=[]
                    Velocity_persecond=np.vstack([Tag_A_Velocity_persecond,Tag_B_Velocity_persecond,Tag_C_Velocity_persecond,Tag_D_Velocity_persecond,
                                                     Tag_E_Velocity_persecond,Tag_F_Velocity_persecond,Tag_G_Velocity_persecond,Tag_H_Velocity_persecond,
                                                     Tag_I_Velocity_persecond,Tag_J_Velocity_persecond,Tag_K_Velocity_persecond,Tag_L_Velocity_persecond,
                                                     Tag_M_Velocity_persecond,Tag_N_Velocity_persecond])
                    
                    Tag_B_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_B_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                    Tag_C_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_C_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                    Tag_D_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_D_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                    Tag_E_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_E_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                    Tag_F_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_F_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                    Tag_G_Resultant_Velocity_max=(Velocity_persecond[6,:].max());Tag_G_Resultant_Velocity_mean=(Velocity_persecond[6,:].mean());
                    Tag_H_Resultant_Velocity_max=(Velocity_persecond[7,:].max());Tag_H_Resultant_Velocity_mean=(Velocity_persecond[7,:].mean());
                    Tag_I_Resultant_Velocity_max=(Velocity_persecond[8,:].max());Tag_I_Resultant_Velocity_mean=(Velocity_persecond[8,:].mean());
                    Tag_J_Resultant_Velocity_max=(Velocity_persecond[9,:].max());Tag_J_Resultant_Velocity_mean=(Velocity_persecond[9,:].mean());
                    Tag_K_Resultant_Velocity_max=(Velocity_persecond[10,:].max());Tag_K_Resultant_Velocity_mean=(Velocity_persecond[10,:].mean());
                    Tag_L_Resultant_Velocity_max=(Velocity_persecond[11,:].max());Tag_L_Resultant_Velocity_mean=(Velocity_persecond[11,:].mean());
                    Tag_M_Resultant_Velocity_max=(Velocity_persecond[12,:].max());Tag_M_Resultant_Velocity_mean=(Velocity_persecond[12,:].mean());
                    Tag_N_Resultant_Velocity_max=(Velocity_persecond[13,:].max());Tag_N_Resultant_Velocity_mean=(Velocity_persecond[13,:].mean());
                    
                    Resultant_Velocity_max=np.vstack([Tag_A_Resultant_Velocity_max,Tag_B_Resultant_Velocity_max,Tag_C_Resultant_Velocity_max,Tag_D_Resultant_Velocity_max,
                                                     Tag_E_Resultant_Velocity_max,Tag_F_Resultant_Velocity_max,Tag_G_Resultant_Velocity_max,Tag_H_Resultant_Velocity_max,
                                                     Tag_I_Resultant_Velocity_max,Tag_J_Resultant_Velocity_max,Tag_K_Resultant_Velocity_max,Tag_L_Resultant_Velocity_max,
                                                     Tag_M_Resultant_Velocity_max,Tag_N_Resultant_Velocity_max])
                    Resultant_Velocity_mean=np.vstack([Tag_A_Resultant_Velocity_mean,Tag_B_Resultant_Velocity_mean,Tag_C_Resultant_Velocity_mean,Tag_D_Resultant_Velocity_mean,
                                                     Tag_E_Resultant_Velocity_mean,Tag_F_Resultant_Velocity_mean,Tag_G_Resultant_Velocity_mean,Tag_H_Resultant_Velocity_mean,
                                                     Tag_I_Resultant_Velocity_mean,Tag_J_Resultant_Velocity_mean,Tag_K_Resultant_Velocity_mean,Tag_L_Resultant_Velocity_mean,
                                                     Tag_M_Resultant_Velocity_mean,Tag_N_Resultant_Velocity_mean])
             else:
                    pass
     ###Acceleration transforms ###
          
             Tag_A_Acceleration_persecond=np.array(Tag_A_Acceleration_persecond,dtype=np.float64);Tag_A_Acceleration_persecond=np.transpose(Tag_A_Acceleration_persecond);
             Tag_B_Acceleration_persecond=np.array(Tag_B_Acceleration_persecond,dtype=np.float64);Tag_B_Acceleration_persecond=np.transpose(Tag_B_Acceleration_persecond);             
             Tag_C_Acceleration_persecond=np.array(Tag_C_Acceleration_persecond,dtype=np.float64);Tag_C_Acceleration_persecond=np.transpose(Tag_C_Acceleration_persecond);
             Tag_D_Acceleration_persecond=np.array(Tag_D_Acceleration_persecond,dtype=np.float64);Tag_D_Acceleration_persecond=np.transpose(Tag_D_Acceleration_persecond);             
             Tag_E_Acceleration_persecond=np.array(Tag_E_Acceleration_persecond,dtype=np.float64);Tag_E_Acceleration_persecond=np.transpose(Tag_E_Acceleration_persecond);             
             Tag_F_Acceleration_persecond=np.array(Tag_F_Acceleration_persecond,dtype=np.float64);Tag_F_Acceleration_persecond=np.transpose(Tag_F_Acceleration_persecond);
             Tag_G_Acceleration_persecond=np.array(Tag_G_Acceleration_persecond,dtype=np.float64);Tag_G_Acceleration_persecond=np.transpose(Tag_G_Acceleration_persecond);             
             Tag_H_Acceleration_persecond=np.array(Tag_H_Acceleration_persecond,dtype=np.float64);Tag_H_Acceleration_persecond=np.transpose(Tag_H_Acceleration_persecond);             
             Tag_I_Acceleration_persecond=np.array(Tag_I_Acceleration_persecond,dtype=np.float64);Tag_I_Acceleration_persecond=np.transpose(Tag_I_Acceleration_persecond);
             Tag_J_Acceleration_persecond=np.array(Tag_J_Acceleration_persecond,dtype=np.float64);Tag_J_Acceleration_persecond=np.transpose(Tag_J_Acceleration_persecond);             
             Tag_K_Acceleration_persecond=np.array(Tag_K_Acceleration_persecond,dtype=np.float64);Tag_K_Acceleration_persecond=np.transpose(Tag_K_Acceleration_persecond);             
             Tag_L_Acceleration_persecond=np.array(Tag_L_Acceleration_persecond,dtype=np.float64);Tag_L_Acceleration_persecond=np.transpose(Tag_L_Acceleration_persecond);
             Tag_M_Acceleration_persecond=np.array(Tag_M_Acceleration_persecond,dtype=np.float64);Tag_M_Acceleration_persecond=np.transpose(Tag_M_Acceleration_persecond);             
             Tag_N_Acceleration_persecond=np.array(Tag_N_Acceleration_persecond,dtype=np.float64);Tag_N_Acceleration_persecond=np.transpose(Tag_N_Acceleration_persecond);             


             Acceleration_persecond=Tag_A_Acceleration_persecond
             Tag_A_Resultant_Acceleration_max=Acceleration_persecond.max()
             Tag_A_Resultant_Acceleration_mean=Acceleration_persecond.mean()
             Resultant_Acceleration_max=Tag_A_Resultant_Acceleration_max
             Resultant_Acceleration_mean=Tag_A_Resultant_Acceleration_mean
                
             if len(Tag_B_Acceleration_persecond)>0:
                    Acceleration_persecond=np.vstack([Tag_A_Acceleration_persecond,Tag_B_Acceleration_persecond])
                    Tag_B_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max())
                    Tag_B_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean())
                    Resultant_Acceleration_max=np.vstack([Tag_A_Resultant_Acceleration_max,Tag_B_Resultant_Acceleration_max])
                    Resultant_Acceleration_mean=np.vstack([Tag_A_Resultant_Acceleration_mean,Tag_B_Resultant_Acceleration_mean])
             else:
                    pass
             if len(Tag_C_Acceleration_persecond)>0:
                    Acceleration_persecond=np.vstack([Tag_A_Acceleration_persecond,Tag_B_Acceleration_persecond,Tag_C_Acceleration_persecond])
                    Tag_B_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_B_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                    Tag_C_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_C_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                    Resultant_Acceleration_max=np.vstack([Tag_A_Resultant_Acceleration_max,Tag_B_Resultant_Acceleration_max,Tag_C_Resultant_Acceleration_max])
                    Resultant_Acceleration_mean=np.vstack([Tag_A_Resultant_Acceleration_mean,Tag_B_Resultant_Acceleration_mean,Tag_C_Resultant_Acceleration_mean])
             else:
                    pass
             if len(Tag_D_Acceleration_persecond)>0:
                    Acceleration_persecond=np.vstack([Tag_A_Acceleration_persecond,Tag_B_Acceleration_persecond,Tag_C_Acceleration_persecond,Tag_D_Acceleration_persecond])
                    Tag_B_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_B_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                    Tag_C_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_C_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                    Tag_D_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_D_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                    Resultant_Acceleration_max=np.vstack([Tag_A_Resultant_Acceleration_max,Tag_B_Resultant_Acceleration_max,Tag_C_Resultant_Acceleration_max,Tag_D_Resultant_Acceleration_max])
                    Resultant_Acceleration_mean=np.vstack([Tag_A_Resultant_Acceleration_mean,Tag_B_Resultant_Acceleration_mean,Tag_C_Resultant_Acceleration_mean,Tag_D_Resultant_Acceleration_mean])
             else:
                    pass
             if len(Tag_E_Acceleration_persecond)>0:
                    Acceleration_persecond=np.vstack([Tag_A_Acceleration_persecond,Tag_B_Acceleration_persecond,Tag_C_Acceleration_persecond,Tag_D_Acceleration_persecond,
                                                     Tag_E_Acceleration_persecond])
                    Tag_B_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_B_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                    Tag_C_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_C_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                    Tag_D_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_D_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                    Tag_E_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_E_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                    Resultant_Acceleration_max=np.vstack([Tag_A_Resultant_Acceleration_max,Tag_B_Resultant_Acceleration_max,Tag_C_Resultant_Acceleration_max,Tag_D_Resultant_Acceleration_max,
                                                     Tag_E_Resultant_Acceleration_max])
                    Resultant_Acceleration_mean=np.vstack([Tag_A_Resultant_Acceleration_mean,Tag_B_Resultant_Acceleration_mean,Tag_C_Resultant_Acceleration_mean,Tag_D_Resultant_Acceleration_mean,
                                                     Tag_E_Resultant_Acceleration_mean])
             else:
                    pass
             if len(Tag_F_Acceleration_persecond)>0:
                    Acceleration_persecond=np.vstack([Tag_A_Acceleration_persecond,Tag_B_Acceleration_persecond,Tag_C_Acceleration_persecond,Tag_D_Acceleration_persecond,
                                                     Tag_E_Acceleration_persecond,Tag_F_Acceleration_persecond])
                    Tag_B_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_B_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                    Tag_C_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_C_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                    Tag_D_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_D_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                    Tag_E_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_E_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                    Tag_F_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_F_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                    Resultant_Acceleration_max=np.vstack([Tag_A_Resultant_Acceleration_max,Tag_B_Resultant_Acceleration_max,Tag_C_Resultant_Acceleration_max,Tag_D_Resultant_Acceleration_max,
                                                     Tag_E_Resultant_Acceleration_max,Tag_F_Resultant_Acceleration_max])
                    Resultant_Acceleration_mean=np.vstack([Tag_A_Resultant_Acceleration_mean,Tag_B_Resultant_Acceleration_mean,Tag_C_Resultant_Acceleration_mean,Tag_D_Resultant_Acceleration_mean,
                                                     Tag_E_Resultant_Acceleration_mean,Tag_F_Resultant_Acceleration_mean])
             else:
                    pass
             if len(Tag_G_Acceleration_persecond)>0:
                    Acceleration_persecond=np.vstack([Tag_A_Acceleration_persecond,Tag_B_Acceleration_persecond,Tag_C_Acceleration_persecond,Tag_D_Acceleration_persecond,
                                                     Tag_E_Acceleration_persecond,Tag_F_Acceleration_persecond,Tag_G_Acceleration_persecond])
                    Tag_B_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_B_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                    Tag_C_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_C_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                    Tag_D_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_D_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                    Tag_E_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_E_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                    Tag_F_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_F_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                    Tag_G_Resultant_Acceleration_max=(Acceleration_persecond[6,:].max());Tag_G_Resultant_Acceleration_mean=(Acceleration_persecond[6,:].mean());
                    Resultant_Acceleration_max=np.vstack([Tag_A_Resultant_Acceleration_max,Tag_B_Resultant_Acceleration_max,Tag_C_Resultant_Acceleration_max,Tag_D_Resultant_Acceleration_max,
                                                     Tag_E_Resultant_Acceleration_max,Tag_F_Resultant_Acceleration_max,Tag_G_Resultant_Acceleration_max])
                    Resultant_Acceleration_mean=np.vstack([Tag_A_Resultant_Acceleration_mean,Tag_B_Resultant_Acceleration_mean,Tag_C_Resultant_Acceleration_mean,Tag_D_Resultant_Acceleration_mean,
                                                     Tag_E_Resultant_Acceleration_mean,Tag_F_Resultant_Acceleration_mean,Tag_G_Resultant_Acceleration_mean])
     
             else:
                    pass
             if len(Tag_H_Acceleration_persecond)>0:
                    Acceleration_persecond=np.vstack([Tag_A_Acceleration_persecond,Tag_B_Acceleration_persecond,Tag_C_Acceleration_persecond,Tag_D_Acceleration_persecond,
                                                     Tag_E_Acceleration_persecond,Tag_F_Acceleration_persecond,Tag_G_Acceleration_persecond,Tag_H_Acceleration_persecond])
                    Tag_B_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_B_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                    Tag_C_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_C_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                    Tag_D_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_D_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                    Tag_E_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_E_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                    Tag_F_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_F_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                    Tag_G_Resultant_Acceleration_max=(Acceleration_persecond[6,:].max());Tag_G_Resultant_Acceleration_mean=(Acceleration_persecond[6,:].mean());
                    Tag_H_Resultant_Acceleration_max=(Acceleration_persecond[7,:].max());Tag_H_Resultant_Acceleration_mean=(Acceleration_persecond[7,:].mean());
                    Resultant_Acceleration_max=np.vstack([Tag_A_Resultant_Acceleration_max,Tag_B_Resultant_Acceleration_max,Tag_C_Resultant_Acceleration_max,Tag_D_Resultant_Acceleration_max,
                                                     Tag_E_Resultant_Acceleration_max,Tag_F_Resultant_Acceleration_max,Tag_G_Resultant_Acceleration_max,Tag_H_Resultant_Acceleration_max])
                    Resultant_Acceleration_mean=np.vstack([Tag_A_Resultant_Acceleration_mean,Tag_B_Resultant_Acceleration_mean,Tag_C_Resultant_Acceleration_mean,Tag_D_Resultant_Acceleration_mean,
                                                     Tag_E_Resultant_Acceleration_mean,Tag_F_Resultant_Acceleration_mean,Tag_G_Resultant_Acceleration_mean,Tag_H_Resultant_Acceleration_mean])
             else:
                    pass
             if len(Tag_I_Acceleration_persecond)>0:
                    Acceleration_persecond=np.vstack([Tag_A_Acceleration_persecond,Tag_B_Acceleration_persecond,Tag_C_Acceleration_persecond,Tag_D_Acceleration_persecond,
                                                     Tag_E_Acceleration_persecond,Tag_F_Acceleration_persecond,Tag_G_Acceleration_persecond,Tag_H_Acceleration_persecond,
                                                     Tag_I_Acceleration_persecond])
                    Tag_B_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_B_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                    Tag_C_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_C_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                    Tag_D_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_D_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                    Tag_E_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_E_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                    Tag_F_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_F_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                    Tag_G_Resultant_Acceleration_max=(Acceleration_persecond[6,:].max());Tag_G_Resultant_Acceleration_mean=(Acceleration_persecond[6,:].mean());
                    Tag_H_Resultant_Acceleration_max=(Acceleration_persecond[7,:].max());Tag_H_Resultant_Acceleration_mean=(Acceleration_persecond[7,:].mean());
                    Tag_I_Resultant_Acceleration_max=(Acceleration_persecond[8,:].max());Tag_I_Resultant_Acceleration_mean=(Acceleration_persecond[8,:].mean());
                    Resultant_Acceleration_max=np.vstack([Tag_A_Resultant_Acceleration_max,Tag_B_Resultant_Acceleration_max,Tag_C_Resultant_Acceleration_max,Tag_D_Resultant_Acceleration_max,
                                                     Tag_E_Resultant_Acceleration_max,Tag_F_Resultant_Acceleration_max,Tag_G_Resultant_Acceleration_max,Tag_H_Resultant_Acceleration_max,
                                                     Tag_I_Resultant_Acceleration_max])
                    Resultant_Acceleration_mean=np.vstack([Tag_A_Resultant_Acceleration_mean,Tag_B_Resultant_Acceleration_mean,Tag_C_Resultant_Acceleration_mean,Tag_D_Resultant_Acceleration_mean,
                                                     Tag_E_Resultant_Acceleration_mean,Tag_F_Resultant_Acceleration_mean,Tag_G_Resultant_Acceleration_mean,Tag_H_Resultant_Acceleration_mean,
                                                     Tag_I_Resultant_Acceleration_mean])
             else:
                    pass
             if len(Tag_J_Acceleration_persecond)>0:
                    Acceleration_persecond=np.vstack([Tag_A_Acceleration_persecond,Tag_B_Acceleration_persecond,Tag_C_Acceleration_persecond,Tag_D_Acceleration_persecond,
                                                     Tag_E_Acceleration_persecond,Tag_F_Acceleration_persecond,Tag_G_Acceleration_persecond,Tag_H_Acceleration_persecond,
                                                     Tag_I_Acceleration_persecond,Tag_J_Acceleration_persecond])
                    Tag_B_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_B_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                    Tag_C_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_C_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                    Tag_D_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_D_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                    Tag_E_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_E_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                    Tag_F_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_F_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                    Tag_G_Resultant_Acceleration_max=(Acceleration_persecond[6,:].max());Tag_G_Resultant_Acceleration_mean=(Acceleration_persecond[6,:].mean());
                    Tag_H_Resultant_Acceleration_max=(Acceleration_persecond[7,:].max());Tag_H_Resultant_Acceleration_mean=(Acceleration_persecond[7,:].mean());
                    Tag_I_Resultant_Acceleration_max=(Acceleration_persecond[8,:].max());Tag_I_Resultant_Acceleration_mean=(Acceleration_persecond[8,:].mean());
                    Tag_J_Resultant_Acceleration_max=(Acceleration_persecond[9,:].max());Tag_J_Resultant_Acceleration_mean=(Acceleration_persecond[9,:].mean());
                    Resultant_Acceleration_max=np.vstack([Tag_A_Resultant_Acceleration_max,Tag_B_Resultant_Acceleration_max,Tag_C_Resultant_Acceleration_max,Tag_D_Resultant_Acceleration_max,
                                                     Tag_E_Resultant_Acceleration_max,Tag_F_Resultant_Acceleration_max,Tag_G_Resultant_Acceleration_max,Tag_H_Resultant_Acceleration_max,
                                                     Tag_I_Resultant_Acceleration_max,Tag_J_Resultant_Acceleration_max])
                    Resultant_Acceleration_mean=np.vstack([Tag_A_Resultant_Acceleration_mean,Tag_B_Resultant_Acceleration_mean,Tag_C_Resultant_Acceleration_mean,Tag_D_Resultant_Acceleration_mean,
                                                     Tag_E_Resultant_Acceleration_mean,Tag_F_Resultant_Acceleration_mean,Tag_G_Resultant_Acceleration_mean,Tag_H_Resultant_Acceleration_mean,
                                                     Tag_I_Resultant_Acceleration_mean,Tag_J_Resultant_Acceleration_mean])         
            
             else:
                    pass
             if len(Tag_K_Acceleration_persecond)>0:
                    Acceleration_persecond=np.vstack([Tag_A_Acceleration_persecond,Tag_B_Acceleration_persecond,Tag_C_Acceleration_persecond,Tag_D_Acceleration_persecond,
                                                     Tag_E_Acceleration_persecond,Tag_F_Acceleration_persecond,Tag_G_Acceleration_persecond,Tag_H_Acceleration_persecond,
                                                     Tag_I_Acceleration_persecond,Tag_J_Acceleration_persecond,Tag_K_Acceleration_persecond])
                    Tag_B_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_B_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                    Tag_C_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_C_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                    Tag_D_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_D_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                    Tag_E_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_E_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                    Tag_F_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_F_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                    Tag_G_Resultant_Acceleration_max=(Acceleration_persecond[6,:].max());Tag_G_Resultant_Acceleration_mean=(Acceleration_persecond[6,:].mean());
                    Tag_H_Resultant_Acceleration_max=(Acceleration_persecond[7,:].max());Tag_H_Resultant_Acceleration_mean=(Acceleration_persecond[7,:].mean());
                    Tag_I_Resultant_Acceleration_max=(Acceleration_persecond[8,:].max());Tag_I_Resultant_Acceleration_mean=(Acceleration_persecond[8,:].mean());
                    Tag_J_Resultant_Acceleration_max=(Acceleration_persecond[9,:].max());Tag_J_Resultant_Acceleration_mean=(Acceleration_persecond[9,:].mean());
                    Tag_K_Resultant_Acceleration_max=(Acceleration_persecond[10,:].max());Tag_K_Resultant_Acceleration_mean=(Acceleration_persecond[10,:].mean());
                    Resultant_Acceleration_max=np.vstack([Tag_A_Resultant_Acceleration_max,Tag_B_Resultant_Acceleration_max,Tag_C_Resultant_Acceleration_max,Tag_D_Resultant_Acceleration_max,
                                                     Tag_E_Resultant_Acceleration_max,Tag_F_Resultant_Acceleration_max,Tag_G_Resultant_Acceleration_max,Tag_H_Resultant_Acceleration_max,
                                                     Tag_I_Resultant_Acceleration_max,Tag_J_Resultant_Acceleration_max,Tag_K_Resultant_Acceleration_max])
                    Resultant_Acceleration_mean=np.vstack([Tag_A_Resultant_Acceleration_mean,Tag_B_Resultant_Acceleration_mean,Tag_C_Resultant_Acceleration_mean,Tag_D_Resultant_Acceleration_mean,
                                                     Tag_E_Resultant_Acceleration_mean,Tag_F_Resultant_Acceleration_mean,Tag_G_Resultant_Acceleration_mean,Tag_H_Resultant_Acceleration_mean,
                                                     Tag_I_Resultant_Acceleration_mean,Tag_J_Resultant_Acceleration_mean,Tag_K_Resultant_Acceleration_mean])         
             else:
                    pass
             if len(Tag_L_Acceleration_persecond)>0:
                    Acceleration_persecond=np.vstack([Tag_A_Acceleration_persecond,Tag_B_Acceleration_persecond,Tag_C_Acceleration_persecond,Tag_D_Acceleration_persecond,
                                                     Tag_E_Acceleration_persecond,Tag_F_Acceleration_persecond,Tag_G_Acceleration_persecond,Tag_H_Acceleration_persecond,
                                                     Tag_I_Acceleration_persecond,Tag_J_Acceleration_persecond,Tag_K_Acceleration_persecond,Tag_L_Acceleration_persecond])
                    Tag_B_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_B_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                    Tag_C_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_C_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                    Tag_D_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_D_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                    Tag_E_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_E_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                    Tag_F_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_F_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                    Tag_G_Resultant_Acceleration_max=(Acceleration_persecond[6,:].max());Tag_G_Resultant_Acceleration_mean=(Acceleration_persecond[6,:].mean());
                    Tag_H_Resultant_Acceleration_max=(Acceleration_persecond[7,:].max());Tag_H_Resultant_Acceleration_mean=(Acceleration_persecond[7,:].mean());
                    Tag_I_Resultant_Acceleration_max=(Acceleration_persecond[8,:].max());Tag_I_Resultant_Acceleration_mean=(Acceleration_persecond[8,:].mean());
                    Tag_J_Resultant_Acceleration_max=(Acceleration_persecond[9,:].max());Tag_J_Resultant_Acceleration_mean=(Acceleration_persecond[9,:].mean());
                    Tag_K_Resultant_Acceleration_max=(Acceleration_persecond[10,:].max());Tag_K_Resultant_Acceleration_mean=(Acceleration_persecond[10,:].mean());
                    Tag_L_Resultant_Acceleration_max=(Acceleration_persecond[11,:].max());Tag_L_Resultant_Acceleration_mean=(Acceleration_persecond[11,:].mean());
                    Resultant_Acceleration_max=np.vstack([Tag_A_Resultant_Acceleration_max,Tag_B_Resultant_Acceleration_max,Tag_C_Resultant_Acceleration_max,Tag_D_Resultant_Acceleration_max,
                                                     Tag_E_Resultant_Acceleration_max,Tag_F_Resultant_Acceleration_max,Tag_G_Resultant_Acceleration_max,Tag_H_Resultant_Acceleration_max,
                                                     Tag_I_Resultant_Acceleration_max,Tag_J_Resultant_Acceleration_max,Tag_K_Resultant_Acceleration_max,Tag_L_Resultant_Acceleration_max])
                    Resultant_Acceleration_mean=np.vstack([Tag_A_Resultant_Acceleration_mean,Tag_B_Resultant_Acceleration_mean,Tag_C_Resultant_Acceleration_mean,Tag_D_Resultant_Acceleration_mean,
                                                     Tag_E_Resultant_Acceleration_mean,Tag_F_Resultant_Acceleration_mean,Tag_G_Resultant_Acceleration_mean,Tag_H_Resultant_Acceleration_mean,
                                                     Tag_I_Resultant_Acceleration_mean,Tag_J_Resultant_Acceleration_mean,Tag_K_Resultant_Acceleration_mean,Tag_L_Resultant_Acceleration_mean])
             else:
                    pass
             if len(Tag_M_Acceleration_persecond)>0:
                    Acceleration_persecond=np.vstack([Tag_A_Acceleration_persecond,Tag_B_Acceleration_persecond,Tag_C_Acceleration_persecond,Tag_D_Acceleration_persecond,
                                                     Tag_E_Acceleration_persecond,Tag_F_Acceleration_persecond,Tag_G_Acceleration_persecond,Tag_H_Acceleration_persecond,
                                                     Tag_I_Acceleration_persecond,Tag_J_Acceleration_persecond,Tag_K_Acceleration_persecond,Tag_L_Acceleration_persecond,
                                                     Tag_M_Acceleration_persecond])
                    Tag_B_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_B_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                    Tag_C_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_C_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                    Tag_D_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_D_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                    Tag_E_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_E_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                    Tag_F_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_F_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                    Tag_G_Resultant_Acceleration_max=(Acceleration_persecond[6,:].max());Tag_G_Resultant_Acceleration_mean=(Acceleration_persecond[6,:].mean());
                    Tag_H_Resultant_Acceleration_max=(Acceleration_persecond[7,:].max());Tag_H_Resultant_Acceleration_mean=(Acceleration_persecond[7,:].mean());
                    Tag_I_Resultant_Acceleration_max=(Acceleration_persecond[8,:].max());Tag_I_Resultant_Acceleration_mean=(Acceleration_persecond[8,:].mean());
                    Tag_J_Resultant_Acceleration_max=(Acceleration_persecond[9,:].max());Tag_J_Resultant_Acceleration_mean=(Acceleration_persecond[9,:].mean());
                    Tag_K_Resultant_Acceleration_max=(Acceleration_persecond[10,:].max());Tag_K_Resultant_Acceleration_mean=(Acceleration_persecond[10,:].mean());
                    Tag_L_Resultant_Acceleration_max=(Acceleration_persecond[11,:].max());Tag_L_Resultant_Acceleration_mean=(Acceleration_persecond[11,:].mean());
                    Tag_M_Resultant_Acceleration_max=(Acceleration_persecond[12,:].max());Tag_M_Resultant_Acceleration_mean=(Acceleration_persecond[12,:].mean());
                    Resultant_Acceleration_max=np.vstack([Tag_A_Resultant_Acceleration_max,Tag_B_Resultant_Acceleration_max,Tag_C_Resultant_Acceleration_max,Tag_D_Resultant_Acceleration_max,
                                                     Tag_E_Resultant_Acceleration_max,Tag_F_Resultant_Acceleration_max,Tag_G_Resultant_Acceleration_max,Tag_H_Resultant_Acceleration_max,
                                                     Tag_I_Resultant_Acceleration_max,Tag_J_Resultant_Acceleration_max,Tag_K_Resultant_Acceleration_max,Tag_L_Resultant_Acceleration_max,
                                                     Tag_M_Resultant_Acceleration_max])
                    Resultant_Acceleration_mean=np.vstack([Tag_A_Resultant_Acceleration_mean,Tag_B_Resultant_Acceleration_mean,Tag_C_Resultant_Acceleration_mean,Tag_D_Resultant_Acceleration_mean,
                                                     Tag_E_Resultant_Acceleration_mean,Tag_F_Resultant_Acceleration_mean,Tag_G_Resultant_Acceleration_mean,Tag_H_Resultant_Acceleration_mean,
                                                     Tag_I_Resultant_Acceleration_mean,Tag_J_Resultant_Acceleration_mean,Tag_K_Resultant_Acceleration_mean,Tag_L_Resultant_Acceleration_mean,
                                                     Tag_M_Resultant_Acceleration_mean])
             else:
                    pass
             if len(Tag_N_Acceleration_persecond)>0:
                    Acceleration_persecond=np.vstack([Tag_A_Acceleration_persecond,Tag_B_Acceleration_persecond,Tag_C_Acceleration_persecond,Tag_D_Acceleration_persecond,
                                                     Tag_E_Acceleration_persecond,Tag_F_Acceleration_persecond,Tag_G_Acceleration_persecond,Tag_H_Acceleration_persecond,
                                                     Tag_I_Acceleration_persecond,Tag_J_Acceleration_persecond,Tag_K_Acceleration_persecond,Tag_L_Acceleration_persecond,
                                                     Tag_M_Acceleration_persecond,Tag_N_Acceleration_persecond])
                    Tag_B_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_B_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                    Tag_C_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_C_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                    Tag_D_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_D_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                    Tag_E_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_E_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                    Tag_F_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_F_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                    Tag_G_Resultant_Acceleration_max=(Acceleration_persecond[6,:].max());Tag_G_Resultant_Acceleration_mean=(Acceleration_persecond[6,:].mean());
                    Tag_H_Resultant_Acceleration_max=(Acceleration_persecond[7,:].max());Tag_H_Resultant_Acceleration_mean=(Acceleration_persecond[7,:].mean());
                    Tag_I_Resultant_Acceleration_max=(Acceleration_persecond[8,:].max());Tag_I_Resultant_Acceleration_mean=(Acceleration_persecond[8,:].mean());
                    Tag_J_Resultant_Acceleration_max=(Acceleration_persecond[9,:].max());Tag_J_Resultant_Acceleration_mean=(Acceleration_persecond[9,:].mean());
                    Tag_K_Resultant_Acceleration_max=(Acceleration_persecond[10,:].max());Tag_K_Resultant_Acceleration_mean=(Acceleration_persecond[10,:].mean());
                    Tag_L_Resultant_Acceleration_max=(Acceleration_persecond[11,:].max());Tag_L_Resultant_Acceleration_mean=(Acceleration_persecond[11,:].mean());
                    Tag_M_Resultant_Acceleration_max=(Acceleration_persecond[12,:].max());Tag_M_Resultant_Acceleration_mean=(Acceleration_persecond[12,:].mean());
                    Tag_N_Resultant_Acceleration_max=(Acceleration_persecond[13,:].max());Tag_N_Resultant_Acceleration_mean=(Acceleration_persecond[13,:].mean());
                    Resultant_Acceleration_max=np.vstack([Tag_A_Resultant_Acceleration_max,Tag_B_Resultant_Acceleration_max,Tag_C_Resultant_Acceleration_max,Tag_D_Resultant_Acceleration_max,
                                                     Tag_E_Resultant_Acceleration_max,Tag_F_Resultant_Acceleration_max,Tag_G_Resultant_Acceleration_max,Tag_H_Resultant_Acceleration_max,
                                                     Tag_I_Resultant_Acceleration_max,Tag_J_Resultant_Acceleration_max,Tag_K_Resultant_Acceleration_max,Tag_L_Resultant_Acceleration_max,
                                                     Tag_M_Resultant_Acceleration_max,Tag_N_Resultant_Acceleration_max])
                    Resultant_Acceleration_mean=np.vstack([Tag_A_Resultant_Acceleration_mean,Tag_B_Resultant_Acceleration_mean,Tag_C_Resultant_Acceleration_mean,Tag_D_Resultant_Acceleration_mean,
                                                     Tag_E_Resultant_Acceleration_mean,Tag_F_Resultant_Acceleration_mean,Tag_G_Resultant_Acceleration_mean,Tag_H_Resultant_Acceleration_mean,
                                                     Tag_I_Resultant_Acceleration_mean,Tag_J_Resultant_Acceleration_mean,Tag_K_Resultant_Acceleration_mean,Tag_L_Resultant_Acceleration_mean,
                                                     Tag_M_Resultant_Acceleration_mean,Tag_N_Resultant_Acceleration_mean])
             else:
                    pass
         
    ###speed transforms ###
             Tag_A_Speed_persecond=np.array(Tag_A_Speed_persecond,dtype=np.float64);Tag_A_Speed_persecond=np.transpose(Tag_A_Speed_persecond);
             Tag_B_Speed_persecond=np.array(Tag_B_Speed_persecond,dtype=np.float64);Tag_B_Speed_persecond=np.transpose(Tag_B_Speed_persecond);             
             Tag_C_Speed_persecond=np.array(Tag_C_Speed_persecond,dtype=np.float64);Tag_C_Speed_persecond=np.transpose(Tag_C_Speed_persecond);
             Tag_D_Speed_persecond=np.array(Tag_D_Speed_persecond,dtype=np.float64);Tag_D_Speed_persecond=np.transpose(Tag_D_Speed_persecond);             
             Tag_E_Speed_persecond=np.array(Tag_E_Speed_persecond,dtype=np.float64);Tag_E_Speed_persecond=np.transpose(Tag_E_Speed_persecond);             
             Tag_F_Speed_persecond=np.array(Tag_F_Speed_persecond,dtype=np.float64);Tag_F_Speed_persecond=np.transpose(Tag_F_Speed_persecond);
             Tag_G_Speed_persecond=np.array(Tag_G_Speed_persecond,dtype=np.float64);Tag_G_Speed_persecond=np.transpose(Tag_G_Speed_persecond);             
             Tag_H_Speed_persecond=np.array(Tag_H_Speed_persecond,dtype=np.float64);Tag_H_Speed_persecond=np.transpose(Tag_H_Speed_persecond);             
             Tag_I_Speed_persecond=np.array(Tag_I_Speed_persecond,dtype=np.float64);Tag_I_Speed_persecond=np.transpose(Tag_I_Speed_persecond);
             Tag_J_Speed_persecond=np.array(Tag_J_Speed_persecond,dtype=np.float64);Tag_J_Speed_persecond=np.transpose(Tag_J_Speed_persecond);             
             Tag_K_Speed_persecond=np.array(Tag_K_Speed_persecond,dtype=np.float64);Tag_K_Speed_persecond=np.transpose(Tag_K_Speed_persecond);             
             Tag_L_Speed_persecond=np.array(Tag_L_Speed_persecond,dtype=np.float64);Tag_L_Speed_persecond=np.transpose(Tag_L_Speed_persecond);
             Tag_M_Speed_persecond=np.array(Tag_M_Speed_persecond,dtype=np.float64);Tag_M_Speed_persecond=np.transpose(Tag_M_Speed_persecond);             
             Tag_N_Speed_persecond=np.array(Tag_N_Speed_persecond,dtype=np.float64);Tag_N_Speed_persecond=np.transpose(Tag_N_Speed_persecond);             

             Speed_persecond=Tag_A_Speed_persecond
             Tag_A_Resultant_Speed_max=(Speed_persecond.max())
             Tag_A_Resultant_Speed_mean=(Speed_persecond.mean())
             Resultant_Speed_max=Tag_A_Resultant_Speed_max
             Resultant_Speed_mean=Tag_A_Resultant_Speed_mean
                
             if len(Tag_B_Speed_persecond)>0:
                    Speed_persecond=np.vstack([Tag_A_Speed_persecond,Tag_B_Speed_persecond])
                    Tag_B_Resultant_Speed_max=(Speed_persecond[1,:].max())
                    Tag_B_Resultant_Speed_mean=(Speed_persecond[1,:].mean())
                    Resultant_Speed_max=np.vstack([Tag_A_Resultant_Speed_max,Tag_B_Resultant_Speed_max])
                    Resultant_Speed_mean=np.vstack([Tag_A_Resultant_Speed_mean,Tag_B_Resultant_Speed_mean])
             else:
                    pass
             if len(Tag_C_Speed_persecond)>0:
                    Speed_persecond=np.vstack([Tag_A_Speed_persecond,Tag_B_Speed_persecond,Tag_C_Speed_persecond])
                    Tag_B_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_B_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                    Tag_C_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_C_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                    Resultant_Speed_max=np.vstack([Tag_A_Resultant_Speed_max,Tag_B_Resultant_Speed_max,Tag_C_Resultant_Speed_max])
                    Resultant_Speed_mean=np.vstack([Tag_A_Resultant_Speed_mean,Tag_B_Resultant_Speed_mean,Tag_C_Resultant_Speed_mean])
             else:
                    pass
             if len(Tag_D_Speed_persecond)>0:
                    Speed_persecond=np.vstack([Tag_A_Speed_persecond,Tag_B_Speed_persecond,Tag_C_Speed_persecond,Tag_D_Speed_persecond])
                    Tag_B_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_B_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                    Tag_C_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_C_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                    Tag_D_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_D_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                    Resultant_Speed_max=np.vstack([Tag_A_Resultant_Speed_max,Tag_B_Resultant_Speed_max,Tag_C_Resultant_Speed_max,Tag_D_Resultant_Speed_max])
                    Resultant_Speed_mean=np.vstack([Tag_A_Resultant_Speed_mean,Tag_B_Resultant_Speed_mean,Tag_C_Resultant_Speed_mean,Tag_D_Resultant_Speed_mean])
             else:
                    pass
             if len(Tag_E_Speed_persecond)>0:
                    Speed_persecond=np.vstack([Tag_A_Speed_persecond,Tag_B_Speed_persecond,Tag_C_Speed_persecond,Tag_D_Speed_persecond,
                                                     Tag_E_Speed_persecond])
                    Tag_B_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_B_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                    Tag_C_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_C_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                    Tag_D_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_D_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                    Tag_E_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_E_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                    Resultant_Speed_max=np.vstack([Tag_A_Resultant_Speed_max,Tag_B_Resultant_Speed_max,Tag_C_Resultant_Speed_max,Tag_D_Resultant_Speed_max,
                                                     Tag_E_Resultant_Speed_max])
                    Resultant_Speed_mean=np.vstack([Tag_A_Resultant_Speed_mean,Tag_B_Resultant_Speed_mean,Tag_C_Resultant_Speed_mean,Tag_D_Resultant_Speed_mean,
                                                     Tag_E_Resultant_Speed_mean])
             else:
                    pass
             if len(Tag_F_Speed_persecond)>0:
                    Speed_persecond=np.vstack([Tag_A_Speed_persecond,Tag_B_Speed_persecond,Tag_C_Speed_persecond,Tag_D_Speed_persecond,
                                                     Tag_E_Speed_persecond,Tag_F_Speed_persecond])
                    Tag_B_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_B_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                    Tag_C_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_C_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                    Tag_D_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_D_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                    Tag_E_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_E_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                    Tag_F_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_F_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                    Resultant_Speed_max=np.vstack([Tag_A_Resultant_Speed_max,Tag_B_Resultant_Speed_max,Tag_C_Resultant_Speed_max,Tag_D_Resultant_Speed_max,
                                                     Tag_E_Resultant_Speed_max,Tag_F_Resultant_Speed_max])
                    Resultant_Speed_mean=np.vstack([Tag_A_Resultant_Speed_mean,Tag_B_Resultant_Speed_mean,Tag_C_Resultant_Speed_mean,Tag_D_Resultant_Speed_mean,
                                                     Tag_E_Resultant_Speed_mean,Tag_F_Resultant_Speed_mean])
             else:
                    pass
             if len(Tag_G_Speed_persecond)>0:
                    Speed_persecond=np.vstack([Tag_A_Speed_persecond,Tag_B_Speed_persecond,Tag_C_Speed_persecond,Tag_D_Speed_persecond,
                                                     Tag_E_Speed_persecond,Tag_F_Speed_persecond,Tag_G_Speed_persecond])
                    Tag_B_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_B_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                    Tag_C_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_C_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                    Tag_D_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_D_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                    Tag_E_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_E_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                    Tag_F_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_F_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                    Tag_G_Resultant_Speed_max=(Speed_persecond[6,:].max());Tag_G_Resultant_Speed_mean=(Speed_persecond[6,:].mean());
                    Resultant_Speed_max=np.vstack([Tag_A_Resultant_Speed_max,Tag_B_Resultant_Speed_max,Tag_C_Resultant_Speed_max,Tag_D_Resultant_Speed_max,
                                                     Tag_E_Resultant_Speed_max,Tag_F_Resultant_Speed_max,Tag_G_Resultant_Speed_max])
                    Resultant_Speed_mean=np.vstack([Tag_A_Resultant_Speed_mean,Tag_B_Resultant_Speed_mean,Tag_C_Resultant_Speed_mean,Tag_D_Resultant_Speed_mean,
                                                     Tag_E_Resultant_Speed_mean,Tag_F_Resultant_Speed_mean,Tag_G_Resultant_Speed_mean])
     
             else:
                    pass
             if len(Tag_H_Speed_persecond)>0:
                    Speed_persecond=np.vstack([Tag_A_Speed_persecond,Tag_B_Speed_persecond,Tag_C_Speed_persecond,Tag_D_Speed_persecond,
                                                     Tag_E_Speed_persecond,Tag_F_Speed_persecond,Tag_G_Speed_persecond,Tag_H_Speed_persecond])
                    Tag_B_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_B_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                    Tag_C_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_C_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                    Tag_D_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_D_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                    Tag_E_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_E_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                    Tag_F_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_F_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                    Tag_G_Resultant_Speed_max=(Speed_persecond[6,:].max());Tag_G_Resultant_Speed_mean=(Speed_persecond[6,:].mean());
                    Tag_H_Resultant_Speed_max=(Speed_persecond[7,:].max());Tag_H_Resultant_Speed_mean=(Speed_persecond[7,:].mean());
                    Resultant_Speed_max=np.vstack([Tag_A_Resultant_Speed_max,Tag_B_Resultant_Speed_max,Tag_C_Resultant_Speed_max,Tag_D_Resultant_Speed_max,
                                                     Tag_E_Resultant_Speed_max,Tag_F_Resultant_Speed_max,Tag_G_Resultant_Speed_max,Tag_H_Resultant_Speed_max])
                    Resultant_Speed_mean=np.vstack([Tag_A_Resultant_Speed_mean,Tag_B_Resultant_Speed_mean,Tag_C_Resultant_Speed_mean,Tag_D_Resultant_Speed_mean,
                                                     Tag_E_Resultant_Speed_mean,Tag_F_Resultant_Speed_mean,Tag_G_Resultant_Speed_mean,Tag_H_Resultant_Speed_mean])
             else:
                    pass
             if len(Tag_I_Speed_persecond)>0:
                    Speed_persecond=np.vstack([Tag_A_Speed_persecond,Tag_B_Speed_persecond,Tag_C_Speed_persecond,Tag_D_Speed_persecond,
                                                     Tag_E_Speed_persecond,Tag_F_Speed_persecond,Tag_G_Speed_persecond,Tag_H_Speed_persecond,
                                                     Tag_I_Speed_persecond])
                    Tag_B_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_B_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                    Tag_C_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_C_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                    Tag_D_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_D_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                    Tag_E_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_E_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                    Tag_F_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_F_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                    Tag_G_Resultant_Speed_max=(Speed_persecond[6,:].max());Tag_G_Resultant_Speed_mean=(Speed_persecond[6,:].mean());
                    Tag_H_Resultant_Speed_max=(Speed_persecond[7,:].max());Tag_H_Resultant_Speed_mean=(Speed_persecond[7,:].mean());
                    Tag_I_Resultant_Speed_max=(Speed_persecond[8,:].max());Tag_I_Resultant_Speed_mean=(Speed_persecond[8,:].mean());
                    Resultant_Speed_max=np.vstack([Tag_A_Resultant_Speed_max,Tag_B_Resultant_Speed_max,Tag_C_Resultant_Speed_max,Tag_D_Resultant_Speed_max,
                                                     Tag_E_Resultant_Speed_max,Tag_F_Resultant_Speed_max,Tag_G_Resultant_Speed_max,Tag_H_Resultant_Speed_max,
                                                     Tag_I_Resultant_Speed_max])
                    Resultant_Speed_mean=np.vstack([Tag_A_Resultant_Speed_mean,Tag_B_Resultant_Speed_mean,Tag_C_Resultant_Speed_mean,Tag_D_Resultant_Speed_mean,
                                                     Tag_E_Resultant_Speed_mean,Tag_F_Resultant_Speed_mean,Tag_G_Resultant_Speed_mean,Tag_H_Resultant_Speed_mean,
                                                     Tag_I_Resultant_Speed_mean])
             else:
                    pass
             if len(Tag_J_Speed_persecond)>0:
                    Speed_persecond=np.vstack([Tag_A_Speed_persecond,Tag_B_Speed_persecond,Tag_C_Speed_persecond,Tag_D_Speed_persecond,
                                                     Tag_E_Speed_persecond,Tag_F_Speed_persecond,Tag_G_Speed_persecond,Tag_H_Speed_persecond,
                                                     Tag_I_Speed_persecond,Tag_J_Speed_persecond])
                    Tag_B_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_B_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                    Tag_C_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_C_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                    Tag_D_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_D_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                    Tag_E_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_E_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                    Tag_F_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_F_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                    Tag_G_Resultant_Speed_max=(Speed_persecond[6,:].max());Tag_G_Resultant_Speed_mean=(Speed_persecond[6,:].mean());
                    Tag_H_Resultant_Speed_max=(Speed_persecond[7,:].max());Tag_H_Resultant_Speed_mean=(Speed_persecond[7,:].mean());
                    Tag_I_Resultant_Speed_max=(Speed_persecond[8,:].max());Tag_I_Resultant_Speed_mean=(Speed_persecond[8,:].mean());
                    Tag_J_Resultant_Speed_max=(Speed_persecond[9,:].max());Tag_J_Resultant_Speed_mean=(Speed_persecond[9,:].mean());
                    Resultant_Speed_max=np.vstack([Tag_A_Resultant_Speed_max,Tag_B_Resultant_Speed_max,Tag_C_Resultant_Speed_max,Tag_D_Resultant_Speed_max,
                                                     Tag_E_Resultant_Speed_max,Tag_F_Resultant_Speed_max,Tag_G_Resultant_Speed_max,Tag_H_Resultant_Speed_max,
                                                     Tag_I_Resultant_Speed_max,Tag_J_Resultant_Speed_max])
                    Resultant_Speed_mean=np.vstack([Tag_A_Resultant_Speed_mean,Tag_B_Resultant_Speed_mean,Tag_C_Resultant_Speed_mean,Tag_D_Resultant_Speed_mean,
                                                     Tag_E_Resultant_Speed_mean,Tag_F_Resultant_Speed_mean,Tag_G_Resultant_Speed_mean,Tag_H_Resultant_Speed_mean,
                                                     Tag_I_Resultant_Speed_mean,Tag_J_Resultant_Speed_mean])         
            
             else:
                    pass
             if len(Tag_K_Speed_persecond)>0:
                    Speed_persecond=np.vstack([Tag_A_Speed_persecond,Tag_B_Speed_persecond,Tag_C_Speed_persecond,Tag_D_Speed_persecond,
                                                     Tag_E_Speed_persecond,Tag_F_Speed_persecond,Tag_G_Speed_persecond,Tag_H_Speed_persecond,
                                                     Tag_I_Speed_persecond,Tag_J_Speed_persecond,Tag_K_Speed_persecond])
                    Tag_B_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_B_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                    Tag_C_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_C_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                    Tag_D_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_D_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                    Tag_E_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_E_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                    Tag_F_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_F_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                    Tag_G_Resultant_Speed_max=(Speed_persecond[6,:].max());Tag_G_Resultant_Speed_mean=(Speed_persecond[6,:].mean());
                    Tag_H_Resultant_Speed_max=(Speed_persecond[7,:].max());Tag_H_Resultant_Speed_mean=(Speed_persecond[7,:].mean());
                    Tag_I_Resultant_Speed_max=(Speed_persecond[8,:].max());Tag_I_Resultant_Speed_mean=(Speed_persecond[8,:].mean());
                    Tag_J_Resultant_Speed_max=(Speed_persecond[9,:].max());Tag_J_Resultant_Speed_mean=(Speed_persecond[9,:].mean());
                    Tag_K_Resultant_Speed_max=(Speed_persecond[10,:].max());Tag_K_Resultant_Speed_mean=(Speed_persecond[10,:].mean());
                    Resultant_Speed_max=np.vstack([Tag_A_Resultant_Speed_max,Tag_B_Resultant_Speed_max,Tag_C_Resultant_Speed_max,Tag_D_Resultant_Speed_max,
                                                     Tag_E_Resultant_Speed_max,Tag_F_Resultant_Speed_max,Tag_G_Resultant_Speed_max,Tag_H_Resultant_Speed_max,
                                                     Tag_I_Resultant_Speed_max,Tag_J_Resultant_Speed_max,Tag_K_Resultant_Speed_max])
                    Resultant_Speed_mean=np.vstack([Tag_A_Resultant_Speed_mean,Tag_B_Resultant_Speed_mean,Tag_C_Resultant_Speed_mean,Tag_D_Resultant_Speed_mean,
                                                     Tag_E_Resultant_Speed_mean,Tag_F_Resultant_Speed_mean,Tag_G_Resultant_Speed_mean,Tag_H_Resultant_Speed_mean,
                                                     Tag_I_Resultant_Speed_mean,Tag_J_Resultant_Speed_mean,Tag_K_Resultant_Speed_mean])         
             else:
                    pass
             if len(Tag_L_Speed_persecond)>0:
                    Speed_persecond=np.vstack([Tag_A_Speed_persecond,Tag_B_Speed_persecond,Tag_C_Speed_persecond,Tag_D_Speed_persecond,
                                                     Tag_E_Speed_persecond,Tag_F_Speed_persecond,Tag_G_Speed_persecond,Tag_H_Speed_persecond,
                                                     Tag_I_Speed_persecond,Tag_J_Speed_persecond,Tag_K_Speed_persecond,Tag_L_Speed_persecond])
                    Tag_B_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_B_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                    Tag_C_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_C_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                    Tag_D_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_D_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                    Tag_E_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_E_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                    Tag_F_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_F_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                    Tag_G_Resultant_Speed_max=(Speed_persecond[6,:].max());Tag_G_Resultant_Speed_mean=(Speed_persecond[6,:].mean());
                    Tag_H_Resultant_Speed_max=(Speed_persecond[7,:].max());Tag_H_Resultant_Speed_mean=(Speed_persecond[7,:].mean());
                    Tag_I_Resultant_Speed_max=(Speed_persecond[8,:].max());Tag_I_Resultant_Speed_mean=(Speed_persecond[8,:].mean());
                    Tag_J_Resultant_Speed_max=(Speed_persecond[9,:].max());Tag_J_Resultant_Speed_mean=(Speed_persecond[9,:].mean());
                    Tag_K_Resultant_Speed_max=(Speed_persecond[10,:].max());Tag_K_Resultant_Speed_mean=(Speed_persecond[10,:].mean());
                    Tag_L_Resultant_Speed_max=(Speed_persecond[11,:].max());Tag_L_Resultant_Speed_mean=(Speed_persecond[11,:].mean());
                    Resultant_Speed_max=np.vstack([Tag_A_Resultant_Speed_max,Tag_B_Resultant_Speed_max,Tag_C_Resultant_Speed_max,Tag_D_Resultant_Speed_max,
                                                     Tag_E_Resultant_Speed_max,Tag_F_Resultant_Speed_max,Tag_G_Resultant_Speed_max,Tag_H_Resultant_Speed_max,
                                                     Tag_I_Resultant_Speed_max,Tag_J_Resultant_Speed_max,Tag_K_Resultant_Speed_max,Tag_L_Resultant_Speed_max])
                    Resultant_Speed_mean=np.vstack([Tag_A_Resultant_Speed_mean,Tag_B_Resultant_Speed_mean,Tag_C_Resultant_Speed_mean,Tag_D_Resultant_Speed_mean,
                                                     Tag_E_Resultant_Speed_mean,Tag_F_Resultant_Speed_mean,Tag_G_Resultant_Speed_mean,Tag_H_Resultant_Speed_mean,
                                                     Tag_I_Resultant_Speed_mean,Tag_J_Resultant_Speed_mean,Tag_K_Resultant_Speed_mean,Tag_L_Resultant_Speed_mean])
             else:
                    pass
             if len(Tag_M_Speed_persecond)>0:
                    Speed_persecond=np.vstack([Tag_A_Speed_persecond,Tag_B_Speed_persecond,Tag_C_Speed_persecond,Tag_D_Speed_persecond,
                                                     Tag_E_Speed_persecond,Tag_F_Speed_persecond,Tag_G_Speed_persecond,Tag_H_Speed_persecond,
                                                     Tag_I_Speed_persecond,Tag_J_Speed_persecond,Tag_K_Speed_persecond,Tag_L_Speed_persecond,
                                                     Tag_M_Speed_persecond])
                    Tag_B_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_B_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                    Tag_C_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_C_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                    Tag_D_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_D_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                    Tag_E_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_E_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                    Tag_F_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_F_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                    Tag_G_Resultant_Speed_max=(Speed_persecond[6,:].max());Tag_G_Resultant_Speed_mean=(Speed_persecond[6,:].mean());
                    Tag_H_Resultant_Speed_max=(Speed_persecond[7,:].max());Tag_H_Resultant_Speed_mean=(Speed_persecond[7,:].mean());
                    Tag_I_Resultant_Speed_max=(Speed_persecond[8,:].max());Tag_I_Resultant_Speed_mean=(Speed_persecond[8,:].mean());
                    Tag_J_Resultant_Speed_max=(Speed_persecond[9,:].max());Tag_J_Resultant_Speed_mean=(Speed_persecond[9,:].mean());
                    Tag_K_Resultant_Speed_max=(Speed_persecond[10,:].max());Tag_K_Resultant_Speed_mean=(Speed_persecond[10,:].mean());
                    Tag_L_Resultant_Speed_max=(Speed_persecond[11,:].max());Tag_L_Resultant_Speed_mean=(Speed_persecond[11,:].mean());
                    Tag_M_Resultant_Speed_max=(Speed_persecond[12,:].max());Tag_M_Resultant_Speed_mean=(Speed_persecond[12,:].mean());
                    Resultant_Speed_max=np.vstack([Tag_A_Resultant_Speed_max,Tag_B_Resultant_Speed_max,Tag_C_Resultant_Speed_max,Tag_D_Resultant_Speed_max,
                                                     Tag_E_Resultant_Speed_max,Tag_F_Resultant_Speed_max,Tag_G_Resultant_Speed_max,Tag_H_Resultant_Speed_max,
                                                     Tag_I_Resultant_Speed_max,Tag_J_Resultant_Speed_max,Tag_K_Resultant_Speed_max,Tag_L_Resultant_Speed_max,
                                                     Tag_M_Resultant_Speed_max])
                    Resultant_Speed_mean=np.vstack([Tag_A_Resultant_Speed_mean,Tag_B_Resultant_Speed_mean,Tag_C_Resultant_Speed_mean,Tag_D_Resultant_Speed_mean,
                                                     Tag_E_Resultant_Speed_mean,Tag_F_Resultant_Speed_mean,Tag_G_Resultant_Speed_mean,Tag_H_Resultant_Speed_mean,
                                                     Tag_I_Resultant_Speed_mean,Tag_J_Resultant_Speed_mean,Tag_K_Resultant_Speed_mean,Tag_L_Resultant_Speed_mean,
                                                     Tag_M_Resultant_Speed_mean])
             else:
                    pass
             if len(Tag_N_Speed_persecond)>0:
                    Speed_persecond=np.vstack([Tag_A_Speed_persecond,Tag_B_Speed_persecond,Tag_C_Speed_persecond,Tag_D_Speed_persecond,
                                                     Tag_E_Speed_persecond,Tag_F_Speed_persecond,Tag_G_Speed_persecond,Tag_H_Speed_persecond,
                                                     Tag_I_Speed_persecond,Tag_J_Speed_persecond,Tag_K_Speed_persecond,Tag_L_Speed_persecond,
                                                     Tag_M_Speed_persecond,Tag_N_Speed_persecond])
                    Tag_B_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_B_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                    Tag_C_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_C_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                    Tag_D_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_D_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                    Tag_E_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_E_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                    Tag_F_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_F_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                    Tag_G_Resultant_Speed_max=(Speed_persecond[6,:].max());Tag_G_Resultant_Speed_mean=(Speed_persecond[6,:].mean());
                    Tag_H_Resultant_Speed_max=(Speed_persecond[7,:].max());Tag_H_Resultant_Speed_mean=(Speed_persecond[7,:].mean());
                    Tag_I_Resultant_Speed_max=(Speed_persecond[8,:].max());Tag_I_Resultant_Speed_mean=(Speed_persecond[8,:].mean());
                    Tag_J_Resultant_Speed_max=(Speed_persecond[9,:].max());Tag_J_Resultant_Speed_mean=(Speed_persecond[9,:].mean());
                    Tag_K_Resultant_Speed_max=(Speed_persecond[10,:].max());Tag_K_Resultant_Speed_mean=(Speed_persecond[10,:].mean());
                    Tag_L_Resultant_Speed_max=(Speed_persecond[11,:].max());Tag_L_Resultant_Speed_mean=(Speed_persecond[11,:].mean());
                    Tag_M_Resultant_Speed_max=(Speed_persecond[12,:].max());Tag_M_Resultant_Speed_mean=(Speed_persecond[12,:].mean());
                    Tag_N_Resultant_Speed_max=(Speed_persecond[13,:].max());Tag_N_Resultant_Speed_mean=(Speed_persecond[13,:].mean());
                    Resultant_Speed_max=np.vstack([Tag_A_Resultant_Speed_max,Tag_B_Resultant_Speed_max,Tag_C_Resultant_Speed_max,Tag_D_Resultant_Speed_max,
                                                     Tag_E_Resultant_Speed_max,Tag_F_Resultant_Speed_max,Tag_G_Resultant_Speed_max,Tag_H_Resultant_Speed_max,
                                                     Tag_I_Resultant_Speed_max,Tag_J_Resultant_Speed_max,Tag_K_Resultant_Speed_max,Tag_L_Resultant_Speed_max,
                                                     Tag_M_Resultant_Speed_max,Tag_N_Resultant_Speed_max])
                    Resultant_Speed_mean=np.vstack([Tag_A_Resultant_Speed_mean,Tag_B_Resultant_Speed_mean,Tag_C_Resultant_Speed_mean,Tag_D_Resultant_Speed_mean,
                                                     Tag_E_Resultant_Speed_mean,Tag_F_Resultant_Speed_mean,Tag_G_Resultant_Speed_mean,Tag_H_Resultant_Speed_mean,
                                                     Tag_I_Resultant_Speed_mean,Tag_J_Resultant_Speed_mean,Tag_K_Resultant_Speed_mean,Tag_L_Resultant_Speed_mean,
                                                     Tag_M_Resultant_Speed_mean,Tag_N_Resultant_Speed_mean])
             else:
                    pass
####Distance transforms ###

             Tag_A_Resultant_diff_persecond=np.array(Tag_A_Resultant_diff_persecond,dtype=np.float64);Tag_A_Resultant_diff_persecond=np.transpose(Tag_A_Resultant_diff_persecond);
             Tag_B_Resultant_diff_persecond=np.array(Tag_B_Resultant_diff_persecond,dtype=np.float64);Tag_B_Resultant_diff_persecond=np.transpose(Tag_B_Resultant_diff_persecond);             
             Tag_C_Resultant_diff_persecond=np.array(Tag_C_Resultant_diff_persecond,dtype=np.float64);Tag_C_Resultant_diff_persecond=np.transpose(Tag_C_Resultant_diff_persecond);
             Tag_D_Resultant_diff_persecond=np.array(Tag_D_Resultant_diff_persecond,dtype=np.float64);Tag_D_Resultant_diff_persecond=np.transpose(Tag_D_Resultant_diff_persecond);             
             Tag_E_Resultant_diff_persecond=np.array(Tag_E_Resultant_diff_persecond,dtype=np.float64);Tag_E_Resultant_diff_persecond=np.transpose(Tag_E_Resultant_diff_persecond);             
             Tag_F_Resultant_diff_persecond=np.array(Tag_F_Resultant_diff_persecond,dtype=np.float64);Tag_F_Resultant_diff_persecond=np.transpose(Tag_F_Resultant_diff_persecond);
             Tag_G_Resultant_diff_persecond=np.array(Tag_G_Resultant_diff_persecond,dtype=np.float64);Tag_G_Resultant_diff_persecond=np.transpose(Tag_G_Resultant_diff_persecond);             
             Tag_H_Resultant_diff_persecond=np.array(Tag_H_Resultant_diff_persecond,dtype=np.float64);Tag_H_Resultant_diff_persecond=np.transpose(Tag_H_Resultant_diff_persecond);             
             Tag_I_Resultant_diff_persecond=np.array(Tag_I_Resultant_diff_persecond,dtype=np.float64);Tag_I_Resultant_diff_persecond=np.transpose(Tag_I_Resultant_diff_persecond);
             Tag_J_Resultant_diff_persecond=np.array(Tag_J_Resultant_diff_persecond,dtype=np.float64);Tag_J_Resultant_diff_persecond=np.transpose(Tag_J_Resultant_diff_persecond);             
             Tag_K_Resultant_diff_persecond=np.array(Tag_K_Resultant_diff_persecond,dtype=np.float64);Tag_K_Resultant_diff_persecond=np.transpose(Tag_K_Resultant_diff_persecond);             
             Tag_L_Resultant_diff_persecond=np.array(Tag_L_Resultant_diff_persecond,dtype=np.float64);Tag_L_Resultant_diff_persecond=np.transpose(Tag_L_Resultant_diff_persecond);
             Tag_M_Resultant_diff_persecond=np.array(Tag_M_Resultant_diff_persecond,dtype=np.float64);Tag_M_Resultant_diff_persecond=np.transpose(Tag_M_Resultant_diff_persecond);             
             Tag_N_Resultant_diff_persecond=np.array(Tag_N_Resultant_diff_persecond,dtype=np.float64);Tag_N_Resultant_diff_persecond=np.transpose(Tag_N_Resultant_diff_persecond);             

             Resultant_diff_persecond=Tag_A_Resultant_diff_persecond
             Tag_A_Distance_max=(Tag_A_Resultant_diff_persecond.max())
             Tag_A_Distance_mean=(Tag_A_Resultant_diff_persecond.mean())
             Distance_max=Tag_A_Distance_max
             Distance_mean=Tag_A_Distance_mean
             
             if len(Tag_B_Resultant_diff_persecond)>0:
                    Tag_B_Distance_max=(Tag_B_Resultant_diff_persecond.max())
                    Tag_B_Distance_mean=(Tag_B_Resultant_diff_persecond.mean())
                    Distance_max=np.vstack([Tag_A_Distance_max,Tag_B_Distance_max])
                    Distance_mean=np.vstack([Tag_A_Distance_mean,Tag_B_Distance_mean])
             else:
                    pass
             if len(Tag_C_Resultant_diff_persecond)>0:
                    Tag_B_Distance_max=(Tag_B_Resultant_diff_persecond.max());Tag_B_Distance_mean=(Tag_B_Resultant_diff_persecond.mean())
                    Tag_C_Distance_max=(Tag_C_Resultant_diff_persecond.max());Tag_C_Distance_mean=(Tag_C_Resultant_diff_persecond.mean())
                    Distance_max=np.vstack([Tag_A_Distance_max,Tag_B_Distance_max,Tag_C_Distance_max])
                    Distance_mean=np.vstack([Tag_A_Distance_mean,Tag_B_Distance_mean,Tag_C_Distance_mean])
             else:
                    pass
          
             if len(Tag_D_Resultant_diff_persecond)>0:
                    Tag_B_Distance_max=(Tag_B_Resultant_diff_persecond.max());Tag_B_Distance_mean=(Tag_B_Resultant_diff_persecond.mean())
                    Tag_C_Distance_max=(Tag_C_Resultant_diff_persecond.max());Tag_C_Distance_mean=(Tag_C_Resultant_diff_persecond.mean())
                    Tag_D_Distance_max=(Tag_D_Resultant_diff_persecond.max());Tag_D_Distance_mean=(Tag_D_Resultant_diff_persecond.mean())
                    Distance_max=np.vstack([Tag_A_Distance_max,Tag_B_Distance_max,Tag_C_Distance_max,Tag_D_Distance_max])
                    Distance_mean=np.vstack([Tag_A_Distance_mean,Tag_B_Distance_mean,Tag_C_Distance_mean,Tag_D_Distance_mean])
             else:
                    pass
             if len(Tag_E_Resultant_diff_persecond)>0:
                    Tag_B_Distance_max=(Tag_B_Resultant_diff_persecond.max());Tag_B_Distance_mean=(Tag_B_Resultant_diff_persecond.mean())
                    Tag_C_Distance_max=(Tag_C_Resultant_diff_persecond.max());Tag_C_Distance_mean=(Tag_C_Resultant_diff_persecond.mean())
                    Tag_D_Distance_max=(Tag_D_Resultant_diff_persecond.max());Tag_D_Distance_mean=(Tag_D_Resultant_diff_persecond.mean())
                    Tag_E_Distance_max=(Tag_E_Resultant_diff_persecond.max());Tag_E_Distance_mean=(Tag_E_Resultant_diff_persecond.mean())
                    Distance_max=np.vstack([Tag_A_Distance_max,Tag_B_Distance_max,Tag_C_Distance_max,Tag_D_Distance_max,
                                                     Tag_E_Distance_max])
                    Distance_mean=np.vstack([Tag_A_Distance_mean,Tag_B_Distance_mean,Tag_C_Distance_mean,Tag_D_Distance_mean,
                                                     Tag_E_Distance_mean])
             else:
                    pass
             if len(Tag_F_Resultant_diff_persecond)>0:
                    Tag_B_Distance_max=(Tag_B_Resultant_diff_persecond.max());Tag_B_Distance_mean=(Tag_B_Resultant_diff_persecond.mean())
                    Tag_C_Distance_max=(Tag_C_Resultant_diff_persecond.max());Tag_C_Distance_mean=(Tag_C_Resultant_diff_persecond.mean())
                    Tag_D_Distance_max=(Tag_D_Resultant_diff_persecond.max());Tag_D_Distance_mean=(Tag_D_Resultant_diff_persecond.mean())
                    Tag_E_Distance_max=(Tag_E_Resultant_diff_persecond.max());Tag_E_Distance_mean=(Tag_E_Resultant_diff_persecond.mean())
                    Tag_F_Distance_max=(Tag_F_Resultant_diff_persecond.max());Tag_F_Distance_mean=(Tag_F_Resultant_diff_persecond.mean())
                    Distance_max=np.vstack([Tag_A_Distance_max,Tag_B_Distance_max,Tag_C_Distance_max,Tag_D_Distance_max,
                                                     Tag_E_Distance_max,Tag_F_Distance_max])
                    Distance_mean=np.vstack([Tag_A_Distance_mean,Tag_B_Distance_mean,Tag_C_Distance_mean,Tag_D_Distance_mean,
                                                     Tag_E_Distance_mean,Tag_F_Distance_mean])
             else:
                    pass
          
             if len(Tag_G_Resultant_diff_persecond)>0:
                    Tag_B_Distance_max=(Tag_B_Resultant_diff_persecond.max());Tag_B_Distance_mean=(Tag_B_Resultant_diff_persecond.mean())
                    Tag_C_Distance_max=(Tag_C_Resultant_diff_persecond.max());Tag_C_Distance_mean=(Tag_C_Resultant_diff_persecond.mean())
                    Tag_D_Distance_max=(Tag_D_Resultant_diff_persecond.max());Tag_D_Distance_mean=(Tag_D_Resultant_diff_persecond.mean())
                    Tag_E_Distance_max=(Tag_E_Resultant_diff_persecond.max());Tag_E_Distance_mean=(Tag_E_Resultant_diff_persecond.mean())
                    Tag_F_Distance_max=(Tag_F_Resultant_diff_persecond.max());Tag_F_Distance_mean=(Tag_F_Resultant_diff_persecond.mean())
                    Tag_G_Distance_max=(Tag_G_Resultant_diff_persecond.max());Tag_G_Distance_mean=(Tag_G_Resultant_diff_persecond.mean())
                    Distance_max=np.vstack([Tag_A_Distance_max,Tag_B_Distance_max,Tag_C_Distance_max,Tag_D_Distance_max,
                                                     Tag_E_Distance_max,Tag_F_Distance_max,Tag_G_Distance_max])
                    Distance_mean=np.vstack([Tag_A_Distance_mean,Tag_B_Distance_mean,Tag_C_Distance_mean,Tag_D_Distance_mean,
                                                     Tag_E_Distance_mean,Tag_F_Distance_mean,Tag_G_Distance_mean])
     
             else:
                    pass
             if len(Tag_H_Resultant_diff_persecond)>0:
                    Tag_B_Distance_max=(Tag_B_Resultant_diff_persecond.max());Tag_B_Distance_mean=(Tag_B_Resultant_diff_persecond.mean())
                    Tag_C_Distance_max=(Tag_C_Resultant_diff_persecond.max());Tag_C_Distance_mean=(Tag_C_Resultant_diff_persecond.mean())
                    Tag_D_Distance_max=(Tag_D_Resultant_diff_persecond.max());Tag_D_Distance_mean=(Tag_D_Resultant_diff_persecond.mean())
                    Tag_E_Distance_max=(Tag_E_Resultant_diff_persecond.max());Tag_E_Distance_mean=(Tag_E_Resultant_diff_persecond.mean())
                    Tag_F_Distance_max=(Tag_F_Resultant_diff_persecond.max());Tag_F_Distance_mean=(Tag_F_Resultant_diff_persecond.mean())
                    Tag_G_Distance_max=(Tag_G_Resultant_diff_persecond.max());Tag_G_Distance_mean=(Tag_G_Resultant_diff_persecond.mean())
                    Tag_H_Distance_max=(Tag_H_Resultant_diff_persecond.max());Tag_H_Distance_mean=(Tag_H_Resultant_diff_persecond.mean())
                    Distance_max=np.vstack([Tag_A_Distance_max,Tag_B_Distance_max,Tag_C_Distance_max,Tag_D_Distance_max,
                                                     Tag_E_Distance_max,Tag_F_Distance_max,Tag_G_Distance_max,Tag_H_Distance_max])
                    Distance_mean=np.vstack([Tag_A_Distance_mean,Tag_B_Distance_mean,Tag_C_Distance_mean,Tag_D_Distance_mean,
                                                     Tag_E_Distance_mean,Tag_F_Distance_mean,Tag_G_Distance_mean,Tag_H_Distance_mean])
             else:
                    pass
             if len(Tag_I_Resultant_diff_persecond)>0:
                    Tag_B_Distance_max=(Tag_B_Resultant_diff_persecond.max());Tag_B_Distance_mean=(Tag_B_Resultant_diff_persecond.mean())
                    Tag_C_Distance_max=(Tag_C_Resultant_diff_persecond.max());Tag_C_Distance_mean=(Tag_C_Resultant_diff_persecond.mean())
                    Tag_D_Distance_max=(Tag_D_Resultant_diff_persecond.max());Tag_D_Distance_mean=(Tag_D_Resultant_diff_persecond.mean())
                    Tag_E_Distance_max=(Tag_E_Resultant_diff_persecond.max());Tag_E_Distance_mean=(Tag_E_Resultant_diff_persecond.mean())
                    Tag_F_Distance_max=(Tag_F_Resultant_diff_persecond.max());Tag_F_Distance_mean=(Tag_F_Resultant_diff_persecond.mean())
                    Tag_G_Distance_max=(Tag_G_Resultant_diff_persecond.max());Tag_G_Distance_mean=(Tag_G_Resultant_diff_persecond.mean())
                    Tag_H_Distance_max=(Tag_H_Resultant_diff_persecond.max());Tag_H_Distance_mean=(Tag_H_Resultant_diff_persecond.mean())
                    Tag_I_Distance_max=(Tag_I_Resultant_diff_persecond.max());Tag_I_Distance_mean=(Tag_I_Resultant_diff_persecond.mean())
                    Distance_max=np.vstack([Tag_A_Distance_max,Tag_B_Distance_max,Tag_C_Distance_max,Tag_D_Distance_max,
                                                     Tag_E_Distance_max,Tag_F_Distance_max,Tag_G_Distance_max,Tag_H_Distance_max,
                                                     Tag_I_Distance_max])
                    Distance_mean=np.vstack([Tag_A_Distance_mean,Tag_B_Distance_mean,Tag_C_Distance_mean,Tag_D_Distance_mean,
                                                     Tag_E_Distance_mean,Tag_F_Distance_mean,Tag_G_Distance_mean,Tag_H_Distance_mean,
                                                     Tag_I_Distance_mean])
             else:
                    pass
       
             if len(Tag_J_Resultant_diff_persecond)>0:
                    Tag_B_Distance_max=(Tag_B_Resultant_diff_persecond.max());Tag_B_Distance_mean=(Tag_B_Resultant_diff_persecond.mean())
                    Tag_C_Distance_max=(Tag_C_Resultant_diff_persecond.max());Tag_C_Distance_mean=(Tag_C_Resultant_diff_persecond.mean())
                    Tag_D_Distance_max=(Tag_D_Resultant_diff_persecond.max());Tag_D_Distance_mean=(Tag_D_Resultant_diff_persecond.mean())
                    Tag_E_Distance_max=(Tag_E_Resultant_diff_persecond.max());Tag_E_Distance_mean=(Tag_E_Resultant_diff_persecond.mean())
                    Tag_F_Distance_max=(Tag_F_Resultant_diff_persecond.max());Tag_F_Distance_mean=(Tag_F_Resultant_diff_persecond.mean())
                    Tag_G_Distance_max=(Tag_G_Resultant_diff_persecond.max());Tag_G_Distance_mean=(Tag_G_Resultant_diff_persecond.mean())
                    Tag_H_Distance_max=(Tag_H_Resultant_diff_persecond.max());Tag_H_Distance_mean=(Tag_H_Resultant_diff_persecond.mean())
                    Tag_I_Distance_max=(Tag_I_Resultant_diff_persecond.max());Tag_I_Distance_mean=(Tag_I_Resultant_diff_persecond.mean())
                    Tag_J_Distance_max=(Tag_J_Resultant_diff_persecond.max());Tag_J_Distance_mean=(Tag_J_Resultant_diff_persecond.mean())
                    Distance_max=np.vstack([Tag_A_Distance_max,Tag_B_Distance_max,Tag_C_Distance_max,Tag_D_Distance_max,
                                                     Tag_E_Distance_max,Tag_F_Distance_max,Tag_G_Distance_max,Tag_H_Distance_max,
                                                     Tag_I_Distance_max,Tag_J_Distance_max])
                    Distance_mean=np.vstack([Tag_A_Distance_mean,Tag_B_Distance_mean,Tag_C_Distance_mean,Tag_D_Distance_mean,
                                                     Tag_E_Distance_mean,Tag_F_Distance_mean,Tag_G_Distance_mean,Tag_H_Distance_mean,
                                                     Tag_I_Distance_mean,Tag_J_Distance_mean])         
            
             else:
                    pass
             if len(Tag_K_Resultant_diff_persecond)>0:
                    Tag_B_Distance_max=(Tag_B_Resultant_diff_persecond.max());Tag_B_Distance_mean=(Tag_B_Resultant_diff_persecond.mean())
                    Tag_C_Distance_max=(Tag_C_Resultant_diff_persecond.max());Tag_C_Distance_mean=(Tag_C_Resultant_diff_persecond.mean())
                    Tag_D_Distance_max=(Tag_D_Resultant_diff_persecond.max());Tag_D_Distance_mean=(Tag_D_Resultant_diff_persecond.mean())
                    Tag_E_Distance_max=(Tag_E_Resultant_diff_persecond.max());Tag_E_Distance_mean=(Tag_E_Resultant_diff_persecond.mean())
                    Tag_F_Distance_max=(Tag_F_Resultant_diff_persecond.max());Tag_F_Distance_mean=(Tag_F_Resultant_diff_persecond.mean())
                    Tag_G_Distance_max=(Tag_G_Resultant_diff_persecond.max());Tag_G_Distance_mean=(Tag_G_Resultant_diff_persecond.mean())
                    Tag_H_Distance_max=(Tag_H_Resultant_diff_persecond.max());Tag_H_Distance_mean=(Tag_H_Resultant_diff_persecond.mean())
                    Tag_I_Distance_max=(Tag_I_Resultant_diff_persecond.max());Tag_I_Distance_mean=(Tag_I_Resultant_diff_persecond.mean())
                    Tag_J_Distance_max=(Tag_J_Resultant_diff_persecond.max());Tag_J_Distance_mean=(Tag_J_Resultant_diff_persecond.mean())
                    Tag_K_Distance_max=(Tag_K_Resultant_diff_persecond.max());Tag_K_Distance_mean=(Tag_K_Resultant_diff_persecond.mean())
                    Distance_max=np.vstack([Tag_A_Distance_max,Tag_B_Distance_max,Tag_C_Distance_max,Tag_D_Distance_max,
                                                     Tag_E_Distance_max,Tag_F_Distance_max,Tag_G_Distance_max,Tag_H_Distance_max,
                                                     Tag_I_Distance_max,Tag_J_Distance_max,Tag_K_Distance_max])
                    Distance_mean=np.vstack([Tag_A_Distance_mean,Tag_B_Distance_mean,Tag_C_Distance_mean,Tag_D_Distance_mean,
                                                     Tag_E_Distance_mean,Tag_F_Distance_mean,Tag_G_Distance_mean,Tag_H_Distance_mean,
                                                     Tag_I_Distance_mean,Tag_J_Distance_mean,Tag_K_Distance_mean])         
             else:
                    pass
             if len(Tag_L_Resultant_diff_persecond)>0:
                    Tag_B_Distance_max=(Tag_B_Resultant_diff_persecond.max());Tag_B_Distance_mean=(Tag_B_Resultant_diff_persecond.mean())
                    Tag_C_Distance_max=(Tag_C_Resultant_diff_persecond.max());Tag_C_Distance_mean=(Tag_C_Resultant_diff_persecond.mean())
                    Tag_D_Distance_max=(Tag_D_Resultant_diff_persecond.max());Tag_D_Distance_mean=(Tag_D_Resultant_diff_persecond.mean())
                    Tag_E_Distance_max=(Tag_E_Resultant_diff_persecond.max());Tag_E_Distance_mean=(Tag_E_Resultant_diff_persecond.mean())
                    Tag_F_Distance_max=(Tag_F_Resultant_diff_persecond.max());Tag_F_Distance_mean=(Tag_F_Resultant_diff_persecond.mean())
                    Tag_G_Distance_max=(Tag_G_Resultant_diff_persecond.max());Tag_G_Distance_mean=(Tag_G_Resultant_diff_persecond.mean())
                    Tag_H_Distance_max=(Tag_H_Resultant_diff_persecond.max());Tag_H_Distance_mean=(Tag_H_Resultant_diff_persecond.mean())
                    Tag_I_Distance_max=(Tag_I_Resultant_diff_persecond.max());Tag_I_Distance_mean=(Tag_I_Resultant_diff_persecond.mean())
                    Tag_J_Distance_max=(Tag_J_Resultant_diff_persecond.max());Tag_J_Distance_mean=(Tag_J_Resultant_diff_persecond.mean())
                    Tag_K_Distance_max=(Tag_K_Resultant_diff_persecond.max());Tag_K_Distance_mean=(Tag_K_Resultant_diff_persecond.mean())
                    Tag_L_Distance_max=(Tag_L_Resultant_diff_persecond.max());Tag_L_Distance_mean=(Tag_L_Resultant_diff_persecond.mean())
                    Distance_max=np.vstack([Tag_A_Distance_max,Tag_B_Distance_max,Tag_C_Distance_max,Tag_D_Distance_max,
                                                     Tag_E_Distance_max,Tag_F_Distance_max,Tag_G_Distance_max,Tag_H_Distance_max,
                                                     Tag_I_Distance_max,Tag_J_Distance_max,Tag_K_Distance_max,Tag_L_Distance_max])
                    Distance_mean=np.vstack([Tag_A_Distance_mean,Tag_B_Distance_mean,Tag_C_Distance_mean,Tag_D_Distance_mean,
                                                     Tag_E_Distance_mean,Tag_F_Distance_mean,Tag_G_Distance_mean,Tag_H_Distance_mean,
                                                     Tag_I_Distance_mean,Tag_J_Distance_mean,Tag_K_Distance_mean,Tag_L_Distance_mean])
             else:
                    pass
             if len(Tag_M_Resultant_diff_persecond)>0:
                    Tag_B_Distance_max=(Tag_B_Resultant_diff_persecond.max());Tag_B_Distance_mean=(Tag_B_Resultant_diff_persecond.mean())
                    Tag_C_Distance_max=(Tag_C_Resultant_diff_persecond.max());Tag_C_Distance_mean=(Tag_C_Resultant_diff_persecond.mean())
                    Tag_D_Distance_max=(Tag_D_Resultant_diff_persecond.max());Tag_D_Distance_mean=(Tag_D_Resultant_diff_persecond.mean())
                    Tag_E_Distance_max=(Tag_E_Resultant_diff_persecond.max());Tag_E_Distance_mean=(Tag_E_Resultant_diff_persecond.mean())
                    Tag_F_Distance_max=(Tag_F_Resultant_diff_persecond.max());Tag_F_Distance_mean=(Tag_F_Resultant_diff_persecond.mean())
                    Tag_G_Distance_max=(Tag_G_Resultant_diff_persecond.max());Tag_G_Distance_mean=(Tag_G_Resultant_diff_persecond.mean())
                    Tag_H_Distance_max=(Tag_H_Resultant_diff_persecond.max());Tag_H_Distance_mean=(Tag_H_Resultant_diff_persecond.mean())
                    Tag_I_Distance_max=(Tag_I_Resultant_diff_persecond.max());Tag_I_Distance_mean=(Tag_I_Resultant_diff_persecond.mean())
                    Tag_J_Distance_max=(Tag_J_Resultant_diff_persecond.max());Tag_J_Distance_mean=(Tag_J_Resultant_diff_persecond.mean())
                    Tag_K_Distance_max=(Tag_K_Resultant_diff_persecond.max());Tag_K_Distance_mean=(Tag_K_Resultant_diff_persecond.mean())
                    Tag_L_Distance_max=(Tag_L_Resultant_diff_persecond.max());Tag_L_Distance_mean=(Tag_L_Resultant_diff_persecond.mean())
                    Tag_M_Distance_max=(Tag_M_Resultant_diff_persecond.max());Tag_M_Distance_mean=(Tag_M_Resultant_diff_persecond.mean())
                    Distance_max=np.vstack([Tag_A_Distance_max,Tag_B_Distance_max,Tag_C_Distance_max,Tag_D_Distance_max,
                                                     Tag_E_Distance_max,Tag_F_Distance_max,Tag_G_Distance_max,Tag_H_Distance_max,
                                                     Tag_I_Distance_max,Tag_J_Distance_max,Tag_K_Distance_max,Tag_L_Distance_max,
                                                     Tag_M_Distance_max])
                    Distance_mean=np.vstack([Tag_A_Distance_mean,Tag_B_Distance_mean,Tag_C_Distance_mean,Tag_D_Distance_mean,
                                                     Tag_E_Distance_mean,Tag_F_Distance_mean,Tag_G_Distance_mean,Tag_H_Distance_mean,
                                                     Tag_I_Distance_mean,Tag_J_Distance_mean,Tag_K_Distance_mean,Tag_L_Distance_mean,
                                                     Tag_M_Distance_mean])
             else:
                    pass
             if len(Tag_N_Resultant_diff_persecond)>0:
                    Tag_B_Distance_max=(Tag_B_Resultant_diff_persecond.max());Tag_B_Distance_mean=(Tag_B_Resultant_diff_persecond.mean())
                    Tag_C_Distance_max=(Tag_C_Resultant_diff_persecond.max());Tag_C_Distance_mean=(Tag_C_Resultant_diff_persecond.mean())
                    Tag_D_Distance_max=(Tag_D_Resultant_diff_persecond.max());Tag_D_Distance_mean=(Tag_D_Resultant_diff_persecond.mean())
                    Tag_E_Distance_max=(Tag_E_Resultant_diff_persecond.max());Tag_E_Distance_mean=(Tag_E_Resultant_diff_persecond.mean())
                    Tag_F_Distance_max=(Tag_F_Resultant_diff_persecond.max());Tag_F_Distance_mean=(Tag_F_Resultant_diff_persecond.mean())
                    Tag_G_Distance_max=(Tag_G_Resultant_diff_persecond.max());Tag_G_Distance_mean=(Tag_G_Resultant_diff_persecond.mean())
                    Tag_H_Distance_max=(Tag_H_Resultant_diff_persecond.max());Tag_H_Distance_mean=(Tag_H_Resultant_diff_persecond.mean())
                    Tag_I_Distance_max=(Tag_I_Resultant_diff_persecond.max());Tag_I_Distance_mean=(Tag_I_Resultant_diff_persecond.mean())
                    Tag_J_Distance_max=(Tag_J_Resultant_diff_persecond.max());Tag_J_Distance_mean=(Tag_J_Resultant_diff_persecond.mean())
                    Tag_K_Distance_max=(Tag_K_Resultant_diff_persecond.max());Tag_K_Distance_mean=(Tag_K_Resultant_diff_persecond.mean())
                    Tag_L_Distance_max=(Tag_L_Resultant_diff_persecond.max());Tag_L_Distance_mean=(Tag_L_Resultant_diff_persecond.mean())
                    Tag_M_Distance_max=(Tag_M_Resultant_diff_persecond.max());Tag_M_Distance_mean=(Tag_M_Resultant_diff_persecond.mean())
                    Tag_N_Distance_max=(Tag_N_Resultant_diff_persecond.max());Tag_N_Distance_mean=(Tag_N_Resultant_diff_persecond.mean())
                    Distance_max=np.vstack([Tag_A_Distance_max,Tag_B_Distance_max,Tag_C_Distance_max,Tag_D_Distance_max,
                                                     Tag_E_Distance_max,Tag_F_Distance_max,Tag_G_Distance_max,Tag_H_Distance_max,
                                                     Tag_I_Distance_max,Tag_J_Distance_max,Tag_K_Distance_max,Tag_L_Distance_max,
                                                     Tag_M_Distance_max,Tag_N_Distance_max])
                    Distance_mean=np.vstack([Tag_A_Distance_mean,Tag_B_Distance_mean,Tag_C_Distance_mean,Tag_D_Distance_mean,
                                                     Tag_E_Distance_mean,Tag_F_Distance_mean,Tag_G_Distance_mean,Tag_H_Distance_mean,
                                                     Tag_I_Distance_mean,Tag_J_Distance_mean,Tag_K_Distance_mean,Tag_L_Distance_mean,
                                                     Tag_M_Distance_mean,Tag_N_Distance_mean])
             else:
                    pass
                
           
             Velocity_persecond=np.array(Velocity_persecond,dtype=np.float64)
             Velocity_persecond=Velocity_persecond
             Acceleration_persecond=np.array(Acceleration_persecond,dtype=np.float64)
             Acceleration_persecond=Acceleration_persecond
             Speed_persecond=np.array(Speed_persecond,dtype=np.float64)   
             Speed_persecond=Speed_persecond/Time_one.size
             Speed_persecond=Speed_persecond
             Metric_length=Speed_persecond.shape[1]
             Metric_length2=list(range(1,Metric_length+1,1))
             
             Speed_max=np.array(Resultant_Speed_max,dtype=np.float64)
             Speed_mean=np.array(Resultant_Speed_mean,dtype=np.float64)
             Speed_max=Speed_max
             Speed_mean=Speed_mean
             Resultant_Acceleration_max=np.array(Resultant_Acceleration_max,dtype=np.float64)
             Resultant_Acceleration_mean=np.array(Resultant_Acceleration_mean,dtype=np.float64)
             Resultant_Acceleration_max=Resultant_Acceleration_max
             Resultant_Acceleration_mean=Resultant_Acceleration_mean
             Distance_max=np.array(Distance_max,dtype=np.float64)
             Distance_max=np.round(Distance_max, decimals = 0)
             Distance_mean=np.array(Distance_mean,dtype=np.float64)

             Resultant_Velocity_max=Resultant_Velocity_max
             Resultant_Velocity_mean=Resultant_Velocity_mean
             Resultant_Velocity_max=Resultant_Velocity_max.flatten()
             Resultant_Velocity_mean=Resultant_Velocity_mean.flatten()
             Speed_max=Speed_max.flatten()
             Speed_mean=Speed_mean.flatten()
             Resultant_Acceleration_max=Resultant_Acceleration_max.flatten()
             Resultant_Acceleration_mean=Resultant_Acceleration_mean.flatten()
             Distance_max=Distance_max.flatten()
             Distance_mean=Distance_mean.flatten()
             
  #           print("dis",Tag_A_Resultant_diff_persecond)
  #           print("vel",Velocity_persecond)
  #           print("acc",Acceleration_persecond)
 #            print("speed",Speed_persecond)             
  #           print("res vel max",Resultant_Velocity_max)
   #          print("res vel mean",Resultant_Velocity_mean)
    #         print("res acc max",Resultant_Acceleration_max)
     #        print("res acc mean",Resultant_Acceleration_mean)
      #       print("speed max",Speed_max)
       #      print("speed mean",Speed_mean)
        #     print("dis max",Distance_max)
         #    print("dis mean",Distance_mean)
             
    ######################### W_R_ratios ##########################################       
             work_count = 0
             Work_Rest=[]
             Work_Rest1=[]
             Work_percent=[]
             Work_percent1=[]
             Velocity_Percentages_PS=[]
             Velocity_Percentages_PS1=[]
             length=(Tag_A_Velocity_persecond.size)
             WtagA=[];WtagB=[];WtagC=[];WtagD=[];WtagE=[];WtagF=[];WtagG=[];WtagH=[];WtagI=[];WtagJ=[];WtagK=[];WtagL=[];WtagM=[];WtagN=[]
             RtagA=[];RtagB=[];RtagC=[];RtagD=[];RtagE=[];RtagF=[];RtagG=[];RtagH=[];RtagI=[];RtagJ=[];RtagK=[];RtagL=[];RtagM=[];RtagN=[]   
             for i in range (len(Tag_dict)):                   
                     for j in range(length):
                         while i ==0:
                           if Velocity_persecond[i][j]>=2:
                                 WtagA.append(j)
                           else:
                                 RtagA.append(j)                         
                           break;                
                         while i ==1:
                           if Velocity_persecond[i][j]>=2:
                                 WtagB.append(j)
                           else:
                                 RtagB.append(j)                         
                           break;
                         while i ==2:
                           if Velocity_persecond[i][j]>=2:
                                 WtagC.append(j)
                           else:
                                 RtagC.append(j)                         
                           break;
                         while i ==3:
                           if Velocity_persecond[i][j]>=2:
                                 WtagD.append(j)
                           else:
                                 RtagD.append(j)                         
                           break;
                         while i ==4:
                           if Velocity_persecond[i][j]>=2:
                                 WtagE.append(j)
                           else:
                                 RtagE.append(j)                         
                           break;
                         while i ==5:
                           if Velocity_persecond[i][j]>=2:
                                 WtagF.append(j)
                           else:
                                 RtagF.append(j)                         
                           break;
                         while i ==6:
                           if Velocity_persecond[i][j]>=2:
                                 WtagG.append(j)
                           else:
                                 RtagG.append(j)                         
                           break;
                         while i ==7:
                           if Velocity_persecond[i][j]>=2:
                                 WtagH.append(j)
                           else:
                                 RtagH.append(j)                         
                           break;
                         while i ==8:
                           if Velocity_persecond[i][j]>=2:
                                 WtagI.append(j)
                           else:
                                 RtagI.append(j)                         
                           break;
                         while i ==9:
                           if Velocity_persecond[i][j]>=2:
                                 WtagJ.append(j)
                           else:
                                 RtagJ.append(j)                         
                           break;
                         while i ==10:
                           if Velocity_persecond[i][j]>=2:
                                 WtagK.append(j)
                           else:
                                 RtagK.append(j)                         
                           break; 
                         while i ==11:
                           if Velocity_persecond[i][j]>=2:
                                 WtagL.append(j)
                           else:
                                 RtagL.append(j)                         
                           break;
                         while i ==12:
                           if Velocity_persecond[i][j]>=2:
                                 WtagM.append(j)
                           else:
                                 RtagM.append(j)                         
                           break;
                         while i ==13:
                           if Velocity_persecond[i][j]>=2:
                                 WtagN.append(j)                
                           else:
                                 RtagN.append(j)
                           break;
             
    ############################################# work durations ################################################################        
             # minute 1              
             WtagA_min1=sum(i <60 for i in WtagA);WtagB_min1=sum(i <60 for i in WtagB);WtagC_min1=sum(i <60 for i in WtagC);
             WtagD_min1=sum(i <60 for i in WtagD);WtagE_min1=sum(i <60 for i in WtagE);WtagF_min1=sum(i <60 for i in WtagF);
             WtagG_min1=sum(i <60 for i in WtagG);WtagH_min1=sum(i <60 for i in WtagH);WtagI_min1=sum(i <60 for i in WtagI);
             WtagJ_min1=sum(i <60 for i in WtagJ);WtagK_min1=sum(i <60 for i in WtagK);WtagL_min1=sum(i <60 for i in WtagL);
             WtagM_min1=sum(i <60 for i in WtagM);WtagN_min1=sum(i <60 for i in WtagN)
             
             # minute 2
             WtagA_min2=sum((i >=60) and (i <120) for i in WtagA);WtagB_min2=sum((i >=60) and (i <120) for i in WtagB);
             WtagC_min2=sum((i >=60) and (i <120) for i in WtagC);WtagD_min2=sum((i >=60) and (i <120) for i in WtagD);
             WtagE_min2=sum((i >=60) and (i <120) for i in WtagE);WtagF_min2=sum((i >=60) and (i <120) for i in WtagF);
             WtagG_min2=sum((i >=60) and (i <120) for i in WtagG);WtagH_min2=sum((i >=60) and (i <120) for i in WtagH);
             WtagI_min2=sum((i >=60) and (i <120) for i in WtagI);WtagJ_min2=sum((i >=60) and (i <120) for i in WtagJ);
             WtagK_min2=sum((i >=60) and (i <120) for i in WtagK);WtagL_min2=sum((i >=60) and (i <120) for i in WtagL);
             WtagM_min2=sum((i >=60) and (i <120) for i in WtagM);WtagN_min2=sum((i >=60) and (i <120) for i in WtagN)

             # minute 3
             WtagA_min3=sum((i>=120) and (i<180) for i in WtagA);WtagB_min3=sum((i>=120) and (i<180) for i in WtagB);
             WtagC_min3=sum((i>=120) and (i<180) for i in WtagC);WtagD_min3=sum((i>=120) and (i<180) for i in WtagD);
             WtagE_min3=sum((i>=120) and (i<180) for i in WtagE);WtagF_min3=sum((i>=120) and (i<180) for i in WtagF);
             WtagG_min3=sum((i>=120) and (i<180) for i in WtagG);WtagH_min3=sum((i>=120) and (i<180) for i in WtagH);
             WtagI_min3=sum((i>=120) and (i<180) for i in WtagI);WtagJ_min3=sum((i>=120) and (i<180) for i in WtagJ);
             WtagK_min3=sum((i>=120) and (i<180) for i in WtagK);WtagL_min3=sum((i>=120) and (i<180) for i in WtagL);
             WtagM_min3=sum((i>=120) and (i<180) for i in WtagM);WtagN_min3=sum((i>=120) and (i<180) for i in WtagN)
             
             # minute 4
             WtagA_min4=sum((i>=180) and (i<240) for i in WtagA);WtagB_min4=sum((i>=180) and (i<240) for i in WtagB);
             WtagC_min4=sum((i>=180) and (i<240) for i in WtagC);WtagD_min4=sum((i>=180) and (i<240) for i in WtagD);
             WtagE_min4=sum((i>=180) and (i<240) for i in WtagE);WtagF_min4=sum((i>=180) and (i<240) for i in WtagF);
             WtagG_min4=sum((i>=180) and (i<240) for i in WtagG);WtagH_min4=sum((i>=180) and (i<240) for i in WtagH);
             WtagI_min4=sum((i>=180) and (i<240) for i in WtagI);WtagJ_min4=sum((i>=180) and (i<240) for i in WtagJ);
             WtagK_min4=sum((i>=180) and (i<240) for i in WtagK);WtagL_min4=sum((i>=180) and (i<240) for i in WtagL);
             WtagM_min4=sum((i>=180) and (i<240) for i in WtagM);WtagN_min4=sum((i>=180) and (i<240) for i in WtagN)
             
             # minute 5
             WtagA_min5=sum((i>=240) and (i<300) for i in WtagA);WtagB_min5=sum((i>=240) and (i<300) for i in WtagB);
             WtagC_min5=sum((i>=240) and (i<300) for i in WtagC);WtagD_min5=sum((i>=240) and (i<300) for i in WtagD);
             WtagE_min5=sum((i>=240) and (i<300) for i in WtagE);WtagF_min5=sum((i>=240) and (i<300) for i in WtagF);
             WtagG_min5=sum((i>=240) and (i<300) for i in WtagG);WtagH_min5=sum((i>=240) and (i<300) for i in WtagH);
             WtagI_min5=sum((i>=240) and (i<300) for i in WtagI);WtagJ_min5=sum((i>=240) and (i<300) for i in WtagJ);
             WtagK_min5=sum((i>=240) and (i<300) for i in WtagK);WtagL_min5=sum((i>=240) and (i<300) for i in WtagL);
             WtagM_min5=sum((i>=240) and (i<300) for i in WtagM);WtagN_min5=sum((i>=240) and (i<300) for i in WtagN)
             
             # minute 6
             WtagA_min6=sum((i>=300) and (i<360) for i in WtagA);WtagB_min6=sum((i>=300) and (i<360) for i in WtagB);
             WtagC_min6=sum((i>=300) and (i<360) for i in WtagC);WtagD_min6=sum((i>=300) and (i<360) for i in WtagD);
             WtagE_min6=sum((i>=300) and (i<360) for i in WtagE);WtagF_min6=sum((i>=300) and (i<360) for i in WtagF);
             WtagG_min6=sum((i>=300) and (i<360) for i in WtagG);WtagH_min6=sum((i>=300) and (i<360) for i in WtagH);
             WtagI_min6=sum((i>=300) and (i<360) for i in WtagI);WtagJ_min6=sum((i>=300) and (i<360)for i in WtagJ);
             WtagK_min6=sum((i>=300) and (i<360) for i in WtagK);WtagL_min6=sum((i>=300) and (i<360) for i in WtagL);
             WtagM_min6=sum((i>=300) and (i<360) for i in WtagM);WtagN_min6=sum((i>=300) and (i<360) for i in WtagN)
             
             # minute 7
             WtagA_min7=sum((i>=360) and (i<420) for i in WtagA);WtagB_min7=sum((i>=360) and (i<420) for i in WtagB);
             WtagC_min7=sum((i>=360) and (i<420) for i in WtagC);WtagD_min7=sum((i>=360) and (i<420) for i in WtagD);
             WtagE_min7=sum((i>=360) and (i<420) for i in WtagE);WtagF_min7=sum((i>=360) and (i<420) for i in WtagF);
             WtagG_min7=sum((i>=360) and (i<420) for i in WtagG);WtagH_min7=sum((i>=360) and (i<420) for i in WtagH);
             WtagI_min7=sum((i>=360) and (i<420) for i in WtagI);WtagJ_min7=sum((i>=360) and (i<420)for i in WtagJ);
             WtagK_min7=sum((i>=360) and (i<420) for i in WtagK);WtagL_min7=sum((i>=360) and (i<420) for i in WtagL);
             WtagM_min7=sum((i>=360) and (i<420) for i in WtagM);WtagN_min7=sum((i>=360) and (i<420) for i in WtagN)
             
             # minute 8
             WtagA_min8=sum((i>=420) and (i<480) for i in WtagA);WtagB_min8=sum((i>=420) and (i<480) for i in WtagB);
             WtagC_min8=sum((i>=420) and (i<480) for i in WtagC);WtagD_min8=sum((i>=420) and (i<480) for i in WtagD);
             WtagE_min8=sum((i>=420) and (i<480) for i in WtagE);WtagF_min8=sum((i>=420) and (i<480) for i in WtagF);
             WtagG_min8=sum((i>=420) and (i<480) for i in WtagG);WtagH_min8=sum((i>=420) and (i<480)for i in WtagH);
             WtagI_min8=sum((i>=420) and (i<480) for i in WtagI);WtagJ_min8=sum((i>=420) and (i<480)for i in WtagJ);
             WtagK_min8=sum((i>=420) and (i<480) for i in WtagK);WtagL_min8=sum((i>=420) and (i<480) for i in WtagL);
             WtagM_min8=sum((i>=420) and (i<480) for i in WtagM);WtagN_min8=sum((i>=420) and (i<480) for i in WtagN)
             
             # minute 9
             WtagA_min9=sum((i>=480) and (i<540) for i in WtagA);WtagB_min9=sum((i>=480) and (i<540) for i in WtagB);
             WtagC_min9=sum((i>=480) and (i<540) for i in WtagC);WtagD_min9=sum((i>=480) and (i<540) for i in WtagD);
             WtagE_min9=sum((i>=480) and (i<540) for i in WtagE);WtagF_min9=sum((i>=480) and (i<540) for i in WtagF);
             WtagG_min9=sum((i>=480) and (i<540) for i in WtagG);WtagH_min9=sum((i>=480) and (i<540) for i in WtagH);
             WtagI_min9=sum((i>=480) and (i<540) for i in WtagI);WtagJ_min9=sum((i>=480) and (i<540) for i in WtagJ);
             WtagK_min9=sum((i>=480) and (i<540) for i in WtagK);WtagL_min9=sum((i>=480) and (i<540) for i in WtagL);
             WtagM_min9=sum((i>=480) and (i<540) for i in WtagM);WtagN_min9=sum((i>=480) and (i<540) for i in WtagN)
             
             # minute 10
             WtagA_min10=sum((i>=540) and (i<600) for i in WtagA);WtagB_min10=sum((i>=540) and (i<600) for i in WtagB);
             WtagC_min10=sum((i>=540) and (i<600) for i in WtagC);WtagD_min10=sum((i>=540) and (i<600) for i in WtagD);
             WtagE_min10=sum((i>=540) and (i<600) for i in WtagE);WtagF_min10=sum((i>=540) and (i<600) for i in WtagF);
             WtagG_min10=sum((i>=540) and (i<600) for i in WtagG);WtagH_min10=sum((i>=540) and (i<600) for i in WtagH);
             WtagI_min10=sum((i>=540) and (i<600) for i in WtagI);WtagJ_min10=sum((i>=540) and (i<600) for i in WtagJ);
             WtagK_min10=sum((i>=540) and (i<600) for i in WtagK);WtagL_min10=sum((i>=540) and (i<600) for i in WtagL);
             WtagM_min10=sum((i>=540) and (i<600) for i in WtagM);WtagN_min10=sum((i>=540) and (i<600) for i in WtagN)
             
             # minute 11
             WtagA_min11=sum((i>=600) and (i<660) for i in WtagA);WtagB_min11=sum((i>=600) and (i<660) for i in WtagB);
             WtagC_min11=sum((i>=600) and (i<660) for i in WtagC);WtagD_min11=sum((i>=600) and (i<660) for i in WtagD);
             WtagE_min11=sum((i>=600) and (i<660) for i in WtagE);WtagF_min11=sum((i>=600) and (i<660) for i in WtagF);
             WtagG_min11=sum((i>=600) and (i<660) for i in WtagG);WtagH_min11=sum((i>=600) and (i<660) for i in WtagH);
             WtagI_min11=sum((i>=600) and (i<660) for i in WtagI);WtagJ_min11=sum((i>=600) and (i<660) for i in WtagJ);
             WtagK_min11=sum((i>=600) and (i<660) for i in WtagK);WtagL_min11=sum((i>=600) and (i<660) for i in WtagL);
             WtagM_min11=sum((i>=600) and (i<660) for i in WtagM);WtagN_min11=sum((i>=600) and (i<660) for i in WtagN)
             
             # minute 12
             WtagA_min12=sum((i>=660) and (i<720) for i in WtagA);WtagB_min12=sum((i>=660) and (i<720) for i in WtagB);
             WtagC_min12=sum((i>=660) and (i<720) for i in WtagC);WtagD_min12=sum((i>=660) and (i<720) for i in WtagD);
             WtagE_min12=sum((i>=660) and (i<720) for i in WtagE);WtagF_min12=sum((i>=660) and (i<720) for i in WtagF);
             WtagG_min12=sum((i>=660) and (i<720) for i in WtagG);WtagH_min12=sum((i>=660) and (i<720) for i in WtagH);
             WtagI_min12=sum((i>=660) and (i<720) for i in WtagI);WtagJ_min12=sum((i>=660) and (i<720) for i in WtagJ);
             WtagK_min12=sum((i>=660) and (i<720) for i in WtagK);WtagL_min12=sum((i>=660) and (i<720) for i in WtagL);
             WtagM_min12=sum((i>=660) and (i<720) for i in WtagM);WtagN_min12=sum((i>=660) and (i<720) for i in WtagN)
             
             # minute 13
             WtagA_min13=sum((i>=720) and (i<780) for i in WtagA);WtagB_min13=sum((i>=720) and (i<780)for i in WtagB);
             WtagC_min13=sum((i>=720) and (i<780) for i in WtagC);WtagD_min13=sum((i>=720) and (i<780) for i in WtagD);
             WtagE_min13=sum((i>=720) and (i<780) for i in WtagE);WtagF_min13=sum((i>=720) and (i<780) for i in WtagF);
             WtagG_min13=sum((i>=720) and (i<780) for i in WtagG);WtagH_min13=sum((i>=720) and (i<780) for i in WtagH);
             WtagI_min13=sum((i>=720) and (i<780) for i in WtagI);WtagJ_min13=sum((i>=720) and (i<780) for i in WtagJ);
             WtagK_min13=sum((i>=720) and (i<780) for i in WtagK);WtagL_min13=sum((i>=720) and (i<780) for i in WtagL);
             WtagM_min13=sum((i>=720) and (i<780) for i in WtagM);WtagN_min13=sum((i>=720) and (i<780) for i in WtagN)
             
             # minute 14
             WtagA_min14=sum((i>=780) and (i<840) for i in WtagA);WtagB_min14=sum((i>=780) and (i<840) for i in WtagB);
             WtagC_min14=sum((i>=780) and (i<840) for i in WtagC);WtagD_min14=sum((i>=780) and (i<840) for i in WtagD);
             WtagE_min14=sum((i>=780) and (i<840) for i in WtagE);WtagF_min14=sum((i>=780) and (i<840) for i in WtagF);
             WtagG_min14=sum((i>=780) and (i<840) for i in WtagG);WtagH_min14=sum((i>=780) and (i<840) for i in WtagH);
             WtagI_min14=sum((i>=780) and (i<840) for i in WtagI);WtagJ_min14=sum((i>=780) and (i<840) for i in WtagJ);
             WtagK_min14=sum((i>=780) and (i<840)for i in WtagK);WtagL_min14=sum((i>=780) and (i<840) for i in WtagL);
             WtagM_min14=sum((i>=780) and (i<840) for i in WtagM);WtagN_min14=sum((i>=780) and (i<840) for i in WtagN)
             
             # minute 15
             WtagA_min15=sum((i>=840) and (i<=900) for i in WtagA);WtagB_min15=sum((i>=840) and (i<=900) for i in WtagB);
             WtagC_min15=sum((i>=840) and (i<=900) for i in WtagC);WtagD_min15=sum((i>=840) and (i<=900) for i in WtagD);
             WtagE_min15=sum((i>=840) and (i<=900) for i in WtagE);WtagF_min15=sum((i>=840) and (i<=900) for i in WtagF);
             WtagG_min15=sum((i>=840) and (i<=900) for i in WtagG);WtagH_min15=sum((i>=840) and (i<=900) for i in WtagH);
             WtagI_min15=sum((i>=840) and (i<=900) for i in WtagI);WtagJ_min15=sum((i>=840) and (i<=900) for i in WtagJ);
             WtagK_min15=sum((i>=840) and (i<=900) for i in WtagK);WtagL_min15=sum((i>=840) and (i<=900) for i in WtagL);
             WtagM_min15=sum((i>=840) and (i<=900) for i in WtagM);WtagN_min15=sum((i>=840) and (i<=900) for i in WtagN)


             
             WtagA_Work_mins=[];WtagB_Work_mins=[];WtagC_Work_mins=[];WtagD_Work_mins=[];WtagE_Work_mins=[];WtagF_Work_mins=[];WtagG_Work_mins=[];
             WtagH_Work_mins=[];WtagI_Work_mins=[];WtagJ_Work_mins=[];WtagK_Work_mins=[];WtagL_Work_mins=[];WtagM_Work_mins=[];WtagN_Work_mins=[]
             
             WtagA_Work_mins.append([WtagA_min1,WtagA_min2,WtagA_min3,WtagA_min4,WtagA_min5,WtagA_min6,WtagA_min7,WtagA_min8,WtagA_min9,
                                     WtagA_min10,WtagA_min11,WtagA_min12,WtagA_min13,WtagA_min14,WtagA_min15])
             
             WtagB_Work_mins.append([WtagB_min1,WtagB_min2,WtagB_min3,WtagB_min4,WtagB_min5,WtagB_min6,WtagB_min7,WtagB_min8,WtagB_min9,
                                     WtagB_min10,WtagB_min11,WtagB_min12,WtagB_min13,WtagB_min14,WtagB_min15])
             
             WtagC_Work_mins.append([WtagC_min1,WtagA_min2,WtagC_min3,WtagC_min4,WtagC_min5,WtagC_min6,WtagC_min7,WtagC_min8,WtagC_min9,
                                     WtagC_min10,WtagC_min11,WtagC_min12,WtagC_min13,WtagC_min14,WtagC_min15])
             
             WtagD_Work_mins.append([WtagD_min1,WtagD_min2,WtagD_min3,WtagD_min4,WtagD_min5,WtagD_min6,WtagD_min7,WtagD_min8,WtagD_min9,
                                     WtagD_min10,WtagD_min11,WtagD_min12,WtagD_min13,WtagD_min14,WtagD_min15])
             
             WtagE_Work_mins.append([WtagE_min1,WtagE_min2,WtagE_min3,WtagE_min4,WtagE_min5,WtagE_min6,WtagE_min7,WtagE_min8,WtagE_min9,
                                     WtagE_min10,WtagE_min11,WtagE_min12,WtagE_min13,WtagE_min14,WtagE_min15])
             
             WtagF_Work_mins.append([WtagF_min1,WtagF_min2,WtagF_min3,WtagF_min4,WtagF_min5,WtagF_min6,WtagF_min7,WtagF_min8,WtagF_min9,
                                     WtagF_min10,WtagF_min11,WtagF_min12,WtagF_min13,WtagF_min14,WtagF_min15])
             
             WtagG_Work_mins.append([WtagG_min1,WtagG_min2,WtagG_min3,WtagG_min4,WtagG_min5,WtagG_min6,WtagG_min7,WtagG_min8,WtagG_min9,
                                     WtagG_min10,WtagG_min11,WtagG_min12,WtagG_min13,WtagG_min14,WtagG_min15])
             
             WtagH_Work_mins.append([WtagH_min1,WtagH_min2,WtagH_min3,WtagH_min4,WtagH_min5,WtagH_min6,WtagH_min7,WtagH_min8,WtagH_min9,
                                   WtagH_min10,WtagH_min11,WtagH_min12,WtagH_min13,WtagH_min14,WtagH_min15])
             
             WtagI_Work_mins.append([WtagI_min1,WtagI_min2,WtagI_min3,WtagI_min4,WtagI_min5,WtagI_min6,WtagI_min7,WtagI_min8,WtagI_min9,
                                     WtagI_min10,WtagI_min11,WtagI_min12,WtagI_min13,WtagI_min14,WtagI_min15])
             
             WtagJ_Work_mins.append([WtagJ_min1,WtagJ_min2,WtagJ_min3,WtagJ_min4,WtagJ_min5,WtagJ_min6,WtagJ_min7,WtagJ_min8,WtagJ_min9,
                                     WtagJ_min10,WtagJ_min11,WtagJ_min12,WtagJ_min13,WtagJ_min14,WtagJ_min15])
             
             WtagK_Work_mins.append([WtagK_min1,WtagK_min2,WtagK_min3,WtagK_min4,WtagK_min5,WtagK_min6,WtagK_min7,WtagK_min8,WtagK_min9,
                                     WtagK_min10,WtagK_min11,WtagK_min12,WtagK_min13,WtagK_min14,WtagK_min15])
             
             WtagL_Work_mins.append([WtagL_min1,WtagL_min2,WtagL_min3,WtagL_min4,WtagL_min5,WtagL_min6,WtagL_min7,WtagL_min8,WtagL_min9,
                                     WtagL_min10,WtagL_min11,WtagL_min12,WtagL_min13,WtagL_min14,WtagL_min15])
             
             WtagM_Work_mins.append([WtagM_min1,WtagM_min2,WtagM_min3,WtagM_min4,WtagM_min5,WtagM_min6,WtagM_min7,WtagM_min8,WtagM_min9,
                                     WtagM_min10,WtagM_min11,WtagM_min12,WtagM_min13,WtagM_min14,WtagM_min15])
             
             WtagN_Work_mins.append([WtagN_min1,WtagN_min2,WtagN_min3,WtagN_min4,WtagN_min5,WtagN_min6,WtagN_min7,WtagN_min8,WtagN_min9,
                                     WtagN_min10,WtagN_min11,WtagN_min12,WtagN_min13,WtagN_min14,WtagN_min15])
             
    ############################################# Rest durations ################################################################
             # minute 1              
             RtagA_min1=sum(i <60 for i in RtagA);RtagB_min1=sum(i <60 for i in RtagB);RtagC_min1=sum(i <60 for i in RtagC);
             RtagD_min1=sum(i <60 for i in RtagD);RtagE_min1=sum(i <60 for i in RtagE);RtagF_min1=sum(i <60 for i in RtagF);
             RtagG_min1=sum(i <60 for i in RtagG);RtagH_min1=sum(i <60 for i in RtagH);RtagI_min1=sum(i <60 for i in RtagI);
             RtagJ_min1=sum(i <60 for i in RtagJ);RtagK_min1=sum(i <60 for i in RtagK);RtagL_min1=sum(i <60 for i in RtagL);
             RtagM_min1=sum(i <60 for i in RtagM);RtagN_min1=sum(i <60 for i in RtagN)

             # minute 2
             RtagA_min2=sum((i >=60) and (i <120) for i in RtagA);RtagB_min2=sum((i >=60) and (i <120) for i in RtagB);
             RtagC_min2=sum((i >=60) and (i <120) for i in RtagC);RtagD_min2=sum((i >=60) and (i <120) for i in RtagD);
             RtagE_min2=sum((i >=60) and (i <120) for i in RtagE);RtagF_min2=sum((i >=60) and (i <120) for i in RtagF);
             RtagG_min2=sum((i >=60) and (i <120) for i in RtagG);RtagH_min2=sum((i >=60) and (i <120) for i in RtagH);
             RtagI_min2=sum((i >=60) and (i <120) for i in RtagI);RtagJ_min2=sum((i >=60) and (i <120) for i in RtagJ);
             RtagK_min2=sum((i >=60) and (i <120) for i in RtagK);RtagL_min2=sum((i >=60) and (i <120) for i in RtagL);
             RtagM_min2=sum((i >=60) and (i <120) for i in RtagM);RtagN_min2=sum((i >=60) and (i <120) for i in RtagN)

             # minute 3
             RtagA_min3=sum((i>=120) and (i<180) for i in RtagA);RtagB_min3=sum((i>=120) and (i<180) for i in RtagB);
             RtagC_min3=sum((i>=120) and (i<180) for i in RtagC);RtagD_min3=sum((i>=120) and (i<180) for i in RtagD);
             RtagE_min3=sum((i>=120) and (i<180) for i in RtagE);RtagF_min3=sum((i>=120) and (i<180) for i in RtagF);
             RtagG_min3=sum((i>=120) and (i<180) for i in RtagG);RtagH_min3=sum((i>=120) and (i<180) for i in RtagH);
             RtagI_min3=sum((i>=120) and (i<180) for i in RtagI);RtagJ_min3=sum((i>=120) and (i<180) for i in RtagJ);
             RtagK_min3=sum((i>=120) and (i<180) for i in RtagK);RtagL_min3=sum((i>=120) and (i<180) for i in RtagL);
             RtagM_min3=sum((i>=120) and (i<180) for i in RtagM);RtagN_min3=sum((i>=120) and (i<180) for i in RtagN)
             
             # minute 4
             RtagA_min4=sum((i>=180) and (i<240) for i in RtagA);RtagB_min4=sum((i>=180) and (i<240) for i in RtagB);
             RtagC_min4=sum((i>=180) and (i<240) for i in RtagC);RtagD_min4=sum((i>=180) and (i<240) for i in RtagD);
             RtagE_min4=sum((i>=180) and (i<240) for i in RtagE);RtagF_min4=sum((i>=180) and (i<240) for i in RtagF);
             RtagG_min4=sum((i>=180) and (i<240) for i in RtagG);RtagH_min4=sum((i>=180) and (i<240) for i in RtagH);
             RtagI_min4=sum((i>=180) and (i<240) for i in RtagI);RtagJ_min4=sum((i>=180) and (i<240) for i in RtagJ);
             RtagK_min4=sum((i>=180) and (i<240) for i in RtagK);RtagL_min4=sum((i>=180) and (i<240) for i in RtagL);
             RtagM_min4=sum((i>=180) and (i<240) for i in RtagM);RtagN_min4=sum((i>=180) and (i<240) for i in RtagN)
             
             # minute 5
             RtagA_min5=sum((i>=240) and (i<300) for i in RtagA);RtagB_min5=sum((i>=240) and (i<300) for i in RtagB);
             RtagC_min5=sum((i>=240) and (i<300) for i in RtagC);RtagD_min5=sum((i>=240) and (i<300) for i in RtagD);
             RtagE_min5=sum((i>=240) and (i<300) for i in RtagE);RtagF_min5=sum((i>=240) and (i<300) for i in RtagF);
             RtagG_min5=sum((i>=240) and (i<300) for i in RtagG);RtagH_min5=sum((i>=240) and (i<300) for i in RtagH);
             RtagI_min5=sum((i>=240) and (i<300) for i in RtagI);RtagJ_min5=sum((i>=240) and (i<300) for i in RtagJ);
             RtagK_min5=sum((i>=240) and (i<300) for i in RtagK);RtagL_min5=sum((i>=240) and (i<300) for i in RtagL);
             RtagM_min5=sum((i>=240) and (i<300) for i in RtagM);RtagN_min5=sum((i>=240) and (i<300) for i in RtagN)
             
             # minute 6
             RtagA_min6=sum((i>=300) and (i<360) for i in RtagA);RtagB_min6=sum((i>=300) and (i<360) for i in RtagB);
             RtagC_min6=sum((i>=300) and (i<360) for i in RtagC);RtagD_min6=sum((i>=300) and (i<360) for i in RtagD);
             RtagE_min6=sum((i>=300) and (i<360) for i in RtagE);RtagF_min6=sum((i>=300) and (i<360) for i in RtagF);
             RtagG_min6=sum((i>=300) and (i<360) for i in RtagG);RtagH_min6=sum((i>=300) and (i<360) for i in RtagH);
             RtagI_min6=sum((i>=300) and (i<360) for i in RtagI);RtagJ_min6=sum((i>=300) and (i<360)for i in RtagJ);
             RtagK_min6=sum((i>=300) and (i<360) for i in RtagK);RtagL_min6=sum((i>=300) and (i<360) for i in RtagL);
             RtagM_min6=sum((i>=300) and (i<360) for i in RtagM);RtagN_min6=sum((i>=300) and (i<360) for i in RtagN)
             
             # minute 7
             RtagA_min7=sum((i>=360) and (i<420) for i in RtagA);RtagB_min7=sum((i>=360) and (i<420) for i in RtagB);
             RtagC_min7=sum((i>=360) and (i<420) for i in RtagC);RtagD_min7=sum((i>=360) and (i<420) for i in RtagD);
             RtagE_min7=sum((i>=360) and (i<420) for i in RtagE);RtagF_min7=sum((i>=360) and (i<420) for i in RtagF);
             RtagG_min7=sum((i>=360) and (i<420) for i in RtagG);RtagH_min7=sum((i>=360) and (i<420) for i in RtagH);
             RtagI_min7=sum((i>=360) and (i<420) for i in RtagI);RtagJ_min7=sum((i>=360) and (i<420)for i in RtagJ);
             RtagK_min7=sum((i>=360) and (i<420) for i in RtagK);RtagL_min7=sum((i>=360) and (i<420) for i in RtagL);
             RtagM_min7=sum((i>=360) and (i<420) for i in RtagM);RtagN_min7=sum((i>=360) and (i<420) for i in RtagN)
             
             # minute 8
             RtagA_min8=sum((i>=420) and (i<480) for i in RtagA);RtagB_min8=sum((i>=420) and (i<480) for i in RtagB);
             RtagC_min8=sum((i>=420) and (i<480) for i in RtagC);RtagD_min8=sum((i>=420) and (i<480) for i in RtagD);
             RtagE_min8=sum((i>=420) and (i<480) for i in RtagE);RtagF_min8=sum((i>=420) and (i<480) for i in RtagF);
             RtagG_min8=sum((i>=420) and (i<480) for i in RtagG);RtagH_min8=sum((i>=420) and (i<480)for i in RtagH);
             RtagI_min8=sum((i>=420) and (i<480) for i in RtagI);RtagJ_min8=sum((i>=420) and (i<480)for i in RtagJ);
             RtagK_min8=sum((i>=420) and (i<480) for i in RtagK);RtagL_min8=sum((i>=420) and (i<480) for i in RtagL);
             RtagM_min8=sum((i>=420) and (i<480) for i in RtagM);RtagN_min8=sum((i>=420) and (i<480) for i in RtagN)
             
             # minute 9
             RtagA_min9=sum((i>=480) and (i<540) for i in RtagA);RtagB_min9=sum((i>=480) and (i<540) for i in RtagB);
             RtagC_min9=sum((i>=480) and (i<540) for i in RtagC);RtagD_min9=sum((i>=480) and (i<540) for i in RtagD);
             RtagE_min9=sum((i>=480) and (i<540) for i in RtagE);RtagF_min9=sum((i>=480) and (i<540) for i in RtagF);
             RtagG_min9=sum((i>=480) and (i<540) for i in RtagG);RtagH_min9=sum((i>=480) and (i<540) for i in RtagH);
             RtagI_min9=sum((i>=480) and (i<540) for i in RtagI);RtagJ_min9=sum((i>=480) and (i<540) for i in RtagJ);
             RtagK_min9=sum((i>=480) and (i<540) for i in RtagK);RtagL_min9=sum((i>=480) and (i<540) for i in RtagL);
             RtagM_min9=sum((i>=480) and (i<540) for i in RtagM);RtagN_min9=sum((i>=480) and (i<540) for i in RtagN)        

             # minute 10
             RtagA_min10=sum((i>=540) and (i<600) for i in RtagA);RtagB_min10=sum((i>=540) and (i<600) for i in RtagB);
             RtagC_min10=sum((i>=540) and (i<600) for i in RtagC);RtagD_min10=sum((i>=540) and (i<600) for i in RtagD);
             RtagE_min10=sum((i>=540) and (i<600) for i in RtagE);RtagF_min10=sum((i>=540) and (i<600) for i in RtagF);
             RtagG_min10=sum((i>=540) and (i<600) for i in RtagG);RtagH_min10=sum((i>=540) and (i<600) for i in RtagH);
             RtagI_min10=sum((i>=540) and (i<600) for i in RtagI);RtagJ_min10=sum((i>=540) and (i<600) for i in RtagJ);
             RtagK_min10=sum((i>=540) and (i<600) for i in RtagK);RtagL_min10=sum((i>=540) and (i<600) for i in RtagL);
             RtagM_min10=sum((i>=540) and (i<600) for i in RtagM);RtagN_min10=sum((i>=540) and (i<600) for i in RtagN)
             
             # minute 11
             RtagA_min11=sum((i>=600) and (i<660) for i in RtagA);RtagB_min11=sum((i>=600) and (i<660) for i in RtagB);
             RtagC_min11=sum((i>=600) and (i<660) for i in RtagC);RtagD_min11=sum((i>=600) and (i<660) for i in RtagD);
             RtagE_min11=sum((i>=600) and (i<660) for i in RtagE);RtagF_min11=sum((i>=600) and (i<660) for i in RtagF);
             RtagG_min11=sum((i>=600) and (i<660) for i in RtagG);RtagH_min11=sum((i>=600) and (i<660) for i in RtagH);
             RtagI_min11=sum((i>=600) and (i<660) for i in RtagI);RtagJ_min11=sum((i>=600) and (i<660) for i in RtagJ);
             RtagK_min11=sum((i>=600) and (i<660) for i in RtagK);RtagL_min11=sum((i>=600) and (i<660) for i in RtagL);
             RtagM_min11=sum((i>=600) and (i<660) for i in RtagM);RtagN_min11=sum((i>=600) and (i<660) for i in RtagN)
             
             # minute 12
             RtagA_min12=sum((i>=660) and (i<720) for i in RtagA);RtagB_min12=sum((i>=660) and (i<720) for i in RtagB);
             RtagC_min12=sum((i>=660) and (i<720) for i in RtagC);RtagD_min12=sum((i>=660) and (i<720) for i in RtagD);
             RtagE_min12=sum((i>=660) and (i<720) for i in RtagE);RtagF_min12=sum((i>=660) and (i<720) for i in RtagF);
             RtagG_min12=sum((i>=660) and (i<720) for i in RtagG);RtagH_min12=sum((i>=660) and (i<720) for i in RtagH);
             RtagI_min12=sum((i>=660) and (i<720) for i in RtagI);RtagJ_min12=sum((i>=660) and (i<720) for i in RtagJ);
             RtagK_min12=sum((i>=660) and (i<720) for i in RtagK);RtagL_min12=sum((i>=660) and (i<720) for i in RtagL);
             RtagM_min12=sum((i>=660) and (i<720) for i in RtagM);RtagN_min12=sum((i>=660) and (i<720) for i in RtagN)
             
             # minute 13
             RtagA_min13=sum((i>=720) and (i<780) for i in RtagA);RtagB_min13=sum((i>=720) and (i<780)for i in RtagB);
             RtagC_min13=sum((i>=720) and (i<780) for i in RtagC);RtagD_min13=sum((i>=720) and (i<780) for i in RtagD);
             RtagE_min13=sum((i>=720) and (i<780) for i in RtagE);RtagF_min13=sum((i>=720) and (i<780) for i in RtagF);
             RtagG_min13=sum((i>=720) and (i<780) for i in RtagG);RtagH_min13=sum((i>=720) and (i<780) for i in RtagH);
             RtagI_min13=sum((i>=720) and (i<780) for i in RtagI);RtagJ_min13=sum((i>=720) and (i<780) for i in RtagJ);
             RtagK_min13=sum((i>=720) and (i<780) for i in RtagK);RtagL_min13=sum((i>=720) and (i<780) for i in RtagL);
             RtagM_min13=sum((i>=720) and (i<780) for i in RtagM);RtagN_min13=sum((i>=720) and (i<780) for i in RtagN)
             
             # minute 14
             RtagA_min14=sum((i>=780) and (i<840) for i in RtagA);RtagB_min14=sum((i>=780) and (i<840) for i in RtagB);
             RtagC_min14=sum((i>=780) and (i<840) for i in RtagC);RtagD_min14=sum((i>=780) and (i<840) for i in RtagD);
             RtagE_min14=sum((i>=780) and (i<840) for i in RtagE);RtagF_min14=sum((i>=780) and (i<840) for i in RtagF);
             RtagG_min14=sum((i>=780) and (i<840) for i in RtagG);RtagH_min14=sum((i>=780) and (i<840) for i in RtagH);
             RtagI_min14=sum((i>=780) and (i<840) for i in RtagI);RtagJ_min14=sum((i>=780) and (i<840) for i in RtagJ);
             RtagK_min14=sum((i>=780) and (i<840)for i in RtagK);RtagL_min14=sum((i>=780) and (i<840) for i in RtagL);
             RtagM_min14=sum((i>=780) and (i<840) for i in RtagM);RtagN_min14=sum((i>=780) and (i<840) for i in RtagN)
             
             # minute 15
             RtagA_min15=sum((i>=840) and (i<=900) for i in RtagA);RtagB_min15=sum((i>=840) and (i<=900) for i in RtagB);
             RtagC_min15=sum((i>=840) and (i<=900) for i in RtagC);RtagD_min15=sum((i>=840) and (i<=900) for i in RtagD);
             RtagE_min15=sum((i>=840) and (i<=900) for i in RtagE);RtagF_min15=sum((i>=840) and (i<=900) for i in RtagF);
             RtagG_min15=sum((i>=840) and (i<=900) for i in RtagG);RtagH_min15=sum((i>=840) and (i<=900) for i in RtagH);
             RtagI_min15=sum((i>=840) and (i<=900) for i in RtagI);RtagJ_min15=sum((i>=840) and (i<=900) for i in RtagJ);
             RtagK_min15=sum((i>=840) and (i<=900) for i in RtagK);RtagL_min15=sum((i>=840) and (i<=900) for i in RtagL);
             RtagM_min15=sum((i>=840) and (i<=900) for i in RtagM);RtagN_min15=sum((i>=840) and (i<=900) for i in RtagN)
          
             RtagA_Work_mins=[];RtagB_Work_mins=[];RtagC_Work_mins=[];RtagD_Work_mins=[];RtagE_Work_mins=[];RtagF_Work_mins=[];RtagG_Work_mins=[];
             RtagH_Work_mins=[];RtagI_Work_mins=[];RtagJ_Work_mins=[];RtagK_Work_mins=[];RtagL_Work_mins=[];RtagM_Work_mins=[];RtagN_Work_mins=[]
             
             RtagA_Work_mins.append([RtagA_min1,RtagA_min2,RtagA_min3,RtagA_min4,RtagA_min5,RtagA_min6,RtagA_min7,RtagA_min8,RtagA_min9,
                                     RtagA_min10,RtagA_min11,RtagA_min12,RtagA_min13,RtagA_min14,RtagA_min15])
             
             RtagB_Work_mins.append([RtagB_min1,RtagB_min2,RtagB_min3,RtagB_min4,RtagB_min5,RtagB_min6,RtagB_min7,RtagB_min8,RtagB_min9,
                                     RtagB_min10,RtagB_min11,RtagB_min12,RtagB_min13,RtagB_min14,RtagB_min15])
             
             RtagC_Work_mins.append([RtagC_min1,RtagA_min2,RtagC_min3,RtagC_min4,RtagC_min5,RtagC_min6,RtagC_min7,RtagC_min8,RtagC_min9,
                                     RtagC_min10,RtagC_min11,RtagC_min12,RtagC_min13,RtagC_min14,RtagC_min15])
             
             RtagD_Work_mins.append([RtagD_min1,RtagD_min2,RtagD_min3,RtagD_min4,RtagD_min5,RtagD_min6,RtagD_min7,RtagD_min8,RtagD_min9,
                                     RtagD_min10,RtagD_min11,RtagD_min12,RtagD_min13,RtagD_min14,RtagD_min15])
             
             RtagE_Work_mins.append([RtagE_min1,RtagE_min2,RtagE_min3,RtagE_min4,RtagE_min5,RtagE_min6,RtagE_min7,RtagE_min8,RtagE_min9,
                                     RtagE_min10,RtagE_min11,RtagE_min12,RtagE_min13,RtagE_min14,RtagE_min15])
             
             RtagF_Work_mins.append([RtagF_min1,RtagF_min2,RtagF_min3,RtagF_min4,RtagF_min5,RtagF_min6,RtagF_min7,RtagF_min8,RtagF_min9,
                                     RtagF_min10,RtagF_min11,RtagF_min12,RtagF_min13,RtagF_min14,RtagF_min15])
             
             RtagG_Work_mins.append([RtagG_min1,RtagG_min2,RtagG_min3,RtagG_min4,RtagG_min5,RtagG_min6,RtagG_min7,RtagG_min8,RtagG_min9,
                                     RtagG_min10,RtagG_min11,RtagG_min12,RtagG_min13,RtagG_min14,RtagG_min15])
             
             RtagH_Work_mins.append([RtagH_min1,RtagH_min2,RtagH_min3,RtagH_min4,RtagH_min5,RtagH_min6,RtagH_min7,RtagH_min8,RtagH_min9,
                                   RtagH_min10,RtagH_min11,RtagH_min12,RtagH_min13,RtagH_min14,RtagH_min15])
             
             RtagI_Work_mins.append([RtagI_min1,RtagI_min2,RtagI_min3,RtagI_min4,RtagI_min5,RtagI_min6,RtagI_min7,RtagI_min8,RtagI_min9,
                                     RtagI_min10,RtagI_min11,RtagI_min12,RtagI_min13,RtagI_min14,RtagI_min15])
             
             RtagJ_Work_mins.append([RtagJ_min1,RtagJ_min2,RtagJ_min3,RtagJ_min4,RtagJ_min5,RtagJ_min6,RtagJ_min7,RtagJ_min8,RtagJ_min9,
                                     RtagJ_min10,RtagJ_min11,RtagJ_min12,RtagJ_min13,RtagJ_min14,RtagJ_min15])
             
             RtagK_Work_mins.append([RtagK_min1,RtagK_min2,RtagK_min3,RtagK_min4,RtagK_min5,RtagK_min6,RtagK_min7,RtagK_min8,RtagK_min9,
                                     RtagK_min10,RtagK_min11,RtagK_min12,RtagK_min13,RtagK_min14,RtagK_min15])
             
             RtagL_Work_mins.append([RtagL_min1,RtagL_min2,RtagL_min3,RtagL_min4,RtagL_min5,RtagL_min6,RtagL_min7,RtagL_min8,RtagL_min9,
                                     RtagL_min10,RtagL_min11,RtagL_min12,RtagL_min13,RtagL_min14,RtagL_min15])
             
             RtagM_Work_mins.append([RtagM_min1,RtagM_min2,RtagM_min3,RtagM_min4,RtagM_min5,RtagM_min6,RtagM_min7,RtagM_min8,RtagM_min9,
                                     RtagM_min10,RtagM_min11,RtagM_min12,RtagM_min13,RtagM_min14,RtagM_min15])
             
             RtagN_Work_mins.append([RtagN_min1,RtagN_min2,RtagN_min3,RtagN_min4,RtagN_min5,RtagN_min6,RtagN_min7,RtagN_min8,RtagN_min9,
                                     RtagN_min10,RtagN_min11,RtagN_min12,RtagN_min13,RtagN_min14,RtagN_min15])

             Work_Percent=[]
             Rest_Percent=[]
             
             Work_Percent.append([WtagA_Work_mins,WtagB_Work_mins,WtagC_Work_mins,WtagD_Work_mins,WtagE_Work_mins,WtagF_Work_mins,
                                  WtagG_Work_mins,WtagH_Work_mins,WtagI_Work_mins,WtagJ_Work_mins,WtagK_Work_mins,WtagL_Work_mins,WtagM_Work_mins,
                                  WtagN_Work_mins])
                                  
             Rest_Percent.append([RtagA_Work_mins,RtagB_Work_mins,RtagC_Work_mins,RtagD_Work_mins,RtagE_Work_mins,RtagF_Work_mins,
                                  RtagG_Work_mins,RtagH_Work_mins,RtagI_Work_mins,RtagJ_Work_mins,RtagK_Work_mins,RtagL_Work_mins,RtagM_Work_mins,
                                  RtagN_Work_mins])
             
             Work_Percent=np.array(Work_Percent,dtype=np.float64)
             Rest_Percent=np.array(Rest_Percent,dtype=np.float64)
     
#             Work_Percent=np.round((Work_Percent/60)*100, decimals = 0)
 #            Rest_Percent=np.round((Rest_Percent/60)*100, decimals = 0) #[0] = ignore,[#]= tag column,[0]=ignore,[#] = minute column
             Average_Work=[]
             Average_Rest=[]

             for i in range(len(Resultant_diff)):
                 Average_Work.append(np.round(np.mean(Work_Percent[0][i][:][:]),decimals = 0))
                 Average_Rest.append(np.round(np.mean(Rest_Percent[0][i][:][:]),decimals = 0))
                       
    ################################################Work percentages ###################################################################################
             VP_Z1_TagA=[]; VP_Z1_TagB=[]; VP_Z1_TagC=[]; VP_Z1_TagD=[]; VP_Z1_TagE=[]; VP_Z1_TagF=[]; VP_Z1_TagG=[]; VP_Z1_TagH=[]; VP_Z1_TagI=[]; VP_Z1_TagJ=[]; VP_Z1_TagK=[];
             VP_Z1_TagL=[]; VP_Z1_TagM=[]; VP_Z1_TagN=[];

             VP_Z2_TagA=[]; VP_Z2_TagB=[]; VP_Z2_TagC=[]; VP_Z2_TagD=[]; VP_Z2_TagE=[]; VP_Z2_TagF=[]; VP_Z2_TagG=[]; VP_Z2_TagH=[]; VP_Z2_TagI=[]; VP_Z2_TagJ=[]; VP_Z2_TagK=[];
             VP_Z2_TagL=[]; VP_Z2_TagM=[]; VP_Z2_TagN=[];

             VP_Z3_TagA=[]; VP_Z3_TagB=[]; VP_Z3_TagC=[]; VP_Z3_TagD=[]; VP_Z3_TagE=[]; VP_Z3_TagF=[]; VP_Z3_TagG=[]; VP_Z3_TagH=[]; VP_Z3_TagI=[]; VP_Z3_TagJ=[]; VP_Z3_TagK=[];
             VP_Z3_TagL=[]; VP_Z3_TagM=[]; VP_Z3_TagN=[];

             VP_Z4_TagA=[]; VP_Z4_TagB=[]; VP_Z4_TagC=[]; VP_Z4_TagD=[]; VP_Z4_TagE=[]; VP_Z4_TagF=[]; VP_Z4_TagG=[]; VP_Z4_TagH=[]; VP_Z4_TagI=[]; VP_Z4_TagJ=[]; VP_Z4_TagK=[];
             VP_Z4_TagL=[]; VP_Z4_TagM=[]; VP_Z4_TagN=[];

             VP_Z5_TagA=[]; VP_Z5_TagB=[]; VP_Z5_TagC=[]; VP_Z5_TagD=[]; VP_Z5_TagE=[]; VP_Z5_TagF=[]; VP_Z5_TagG=[]; VP_Z5_TagH=[]; VP_Z5_TagI=[]; VP_Z5_TagJ=[]; VP_Z5_TagK=[];
             VP_Z5_TagL=[]; VP_Z5_TagM=[]; VP_Z5_TagN=[];
             for i in range (len(Tag_dict)): 
                 for j in range(length):
                      if i==0:
                          if Velocity_persecond[i][j]<2:
                              VP_Z1_TagA.append(j)                       
                          elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                              VP_Z2_TagA.append(j)
                          elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                              VP_Z3_TagA.append(j)
                          elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                              VP_Z4_TagA.append(j)
                          elif Velocity_persecond[i][j]>=8:
                              VP_Z5_TagA.append(j)
                      if i==1: 
                          if Velocity_persecond[i][j]<2:
                              VP_Z1_TagB.append(j)
                          elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                              VP_Z2_TagB.append(j)
                          elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                              VP_Z3_TagB.append(j)
                          elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                              VP_Z4_TagB.append(j)
                          elif Velocity_persecond[i][j]>=8:
                              VP_Z5_TagB.append(j)                          
                      if i==2:
                          if Velocity_persecond[i][j]<2:
                              VP_Z1_TagC.append(j)
                          elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                              VP_Z2_TagC.append(j)
                          elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                              VP_Z3_TagC.append(j)
                          elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                              VP_Z4_TagC.append(j)
                          elif Velocity_persecond[i][j]>=8:
                              VP_Z5_TagC.append(j)                          
                      if i==3:
                          if Velocity_persecond[i][j]<2:
                              VP_Z1_TagD.append(j)
                          elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                              VP_Z2_TagD.append(j)
                          elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                              VP_Z3_TagD.append(j)
                          elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                              VP_Z4_TagD.append(j)
                          elif Velocity_persecond[i][j]>=8:
                              VP_Z5_TagD.append(j)                          
                      if i==4:
                          if Velocity_persecond[i][j]<2:
                              VP_Z1_TagE.append(j)   
                          elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                              VP_Z2_TagE.append(j) 
                          elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                              VP_Z3_TagE.append(j) 
                          elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                              VP_Z4_TagE.append(j) 
                          elif Velocity_persecond[i][j]>=8:
                              VP_Z5_TagE.append(j) 
                      if i==5:
                          if Velocity_persecond[i][j]<2:
                              VP_Z1_TagF.append(j)    
                          elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                              VP_Z2_TagF.append(j)
                          elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                              VP_Z3_TagF.append(j)
                          elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                              VP_Z4_TagF.append(j)
                          elif Velocity_persecond[i][j]>=8:
                              VP_Z5_TagF.append(j)
                      if i==6:
                          if Velocity_persecond[i][j]<2:
                              VP_Z1_TagG.append(j)    
                          elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:                          
                              VP_Z2_TagG.append(j) 
                          elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                              VP_Z3_TagG.append(j) 
                          elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                              VP_Z4_TagG.append(j) 
                          elif Velocity_persecond[i][j]>=8:
                              VP_Z5_TagG.append(j) 
                      if i==7:
                          if Velocity_persecond[i][j]<2:
                              VP_Z1_TagH.append(j)    
                          elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                              VP_Z2_TagH.append(j) 
                          elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                              VP_Z3_TagH.append(j) 
                          elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                              VP_Z4_TagH.append(j) 
                          elif Velocity_persecond[i][j]>=8:
                              VP_Z5_TagH.append(j) 
                      if i==8:
                          if Velocity_persecond[i][j]<2:
                              VP_Z1_TagI.append(j)    
                          elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                              VP_Z2_TagI.append(j)
                          elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                              VP_Z3_TagI.append(j)
                          elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                              VP_Z4_TagI.append(j)
                          elif Velocity_persecond[i][j]>=8:
                              VP_Z5_TagI.append(j)
                      if i==9:
                          if Velocity_persecond[i][j]<2:
                              VP_Z1_TagJ.append(j)    
                          elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                              VP_Z2_TagJ.append(j)
                          elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                              VP_Z3_TagJ.append(j)
                          elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                              VP_Z4_TagJ.append(j)
                          elif Velocity_persecond[i][j]>=8:
                              VP_Z5_TagJ.append(j)
                      if i==10:
                          if Velocity_persecond[i][j]<2:
                              VP_Z1_TagK.append(j)    
                          elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                              VP_Z2_TagK.append(j)  
                          elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                              VP_Z3_TagK.append(j)  
                          elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                              VP_Z4_TagK.append(j)  
                          elif Velocity_persecond[i][j]>=8:
                              VP_Z5_TagK.append(j)  
                      if i==11:
                          if Velocity_persecond[i][j]<2:
                              VP_Z1_TagL.append(j)    
                          elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                              VP_Z2_TagL.append(j) 
                          elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                              VP_Z3_TagL.append(j) 
                          elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                              VP_Z4_TagL.append(j) 
                          elif Velocity_persecond[i][j]>=8:
                              VP_Z5_TagL.append(j) 
                      if i==12:
                          if Velocity_persecond[i][j]<2:
                              VP_Z1_TagM.append(j)    
                          elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                              VP_Z2_TagM.append(j) 
                          elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                              VP_Z3_TagM.append(j) 
                          elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                              VP_Z4_TagM.append(j) 
                          elif Velocity_persecond[i][j]>=8:
                              VP_Z5_TagM.append(j) 
                      if i==13:
                          if Velocity_persecond[i][j]<2:
                              VP_Z1_TagN.append(j)
                          elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                              VP_Z2_TagN.append(j)
                          elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                              VP_Z3_TagN.append(j)
                          elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                              VP_Z4_TagN.append(j)
                          elif Velocity_persecond[i][j]>=8:
                              VP_Z5_TagN.append(j)
                    

             ########################################## VP zone durations ################################################################
    # Zone 1         
             while self.completed <51:
                self.completed += 1
             self.progressBar.setValue (self.completed)
             self.progressBar.setValue (self.half)
             
             Z1_VPtagA_mins=[];Z1_VPtagB_mins=[];Z1_VPtagC_mins=[];Z1_VPtagD_mins=[];Z1_VPtagE_mins=[];Z1_VPtagF_mins=[];Z1_VPtagG_mins=[];
             Z1_VPtagH_mins=[];Z1_VPtagI_mins=[];Z1_VPtagJ_mins=[];Z1_VPtagK_mins=[];Z1_VPtagL_mins=[];Z1_VPtagM_mins=[];Z1_VPtagN_mins=[]

             
             # minute 1              
             Z1_VPtagA_min1=sum(i <60 for i in VP_Z1_TagA);Z1_VPtagB_min1=sum(i <60 for i in VP_Z1_TagB);Z1_VPtagC_min1=sum(i <60 for i in VP_Z1_TagC);
             Z1_VPtagD_min1=sum(i <60 for i in VP_Z1_TagD);Z1_VPtagE_min1=sum(i <60 for i in VP_Z1_TagE);Z1_VPtagF_min1=sum(i <60 for i in VP_Z1_TagF);
             Z1_VPtagG_min1=sum(i <60 for i in VP_Z1_TagG);Z1_VPtagH_min1=sum(i <60 for i in VP_Z1_TagH);Z1_VPtagI_min1=sum(i <60 for i in VP_Z1_TagI);
             Z1_VPtagJ_min1=sum(i <60 for i in VP_Z1_TagJ);Z1_VPtagK_min1=sum(i <60 for i in VP_Z1_TagK);Z1_VPtagL_min1=sum(i <60 for i in VP_Z1_TagL);
             Z1_VPtagM_min1=sum(i <60 for i in VP_Z1_TagM);Z1_VPtagN_min1=sum(i <60 for i in VP_Z1_TagN);
             
             # minute 2
             Z1_VPtagA_min2=sum((i >=60) and (i <120) for i in VP_Z1_TagA);Z1_VPtagB_min2=sum((i >=60) and (i <120) for i in VP_Z1_TagB);
             Z1_VPtagC_min2=sum((i >=60) and (i <120) for i in VP_Z1_TagC);Z1_VPtagD_min2=sum((i >=60) and (i <120) for i in VP_Z1_TagD);
             Z1_VPtagE_min2=sum((i >=60) and (i <120) for i in VP_Z1_TagE);Z1_VPtagF_min2=sum((i >=60) and (i <120) for i in VP_Z1_TagF);
             Z1_VPtagG_min2=sum((i >=60) and (i <120) for i in VP_Z1_TagG);Z1_VPtagH_min2=sum((i >=60) and (i <120) for i in VP_Z1_TagH);
             Z1_VPtagI_min2=sum((i >=60) and (i <120) for i in VP_Z1_TagI);Z1_VPtagJ_min2=sum((i >=60) and (i <120) for i in VP_Z1_TagJ);
             Z1_VPtagK_min2=sum((i >=60) and (i <120) for i in VP_Z1_TagK);Z1_VPtagL_min2=sum((i >=60) and (i <120) for i in VP_Z1_TagL);
             Z1_VPtagM_min2=sum((i >=60) and (i <120) for i in VP_Z1_TagM);Z1_VPtagN_min2=sum((i >=60) and (i <120) for i in VP_Z1_TagN)

             # minute 3
             Z1_VPtagA_min3=sum((i>=120) and (i<180) for i in VP_Z1_TagA);Z1_VPtagB_min3=sum((i>=120) and (i<180) for i in VP_Z1_TagB);
             Z1_VPtagC_min3=sum((i>=120) and (i<180) for i in VP_Z1_TagC);Z1_VPtagD_min3=sum((i>=120) and (i<180) for i in VP_Z1_TagD);
             Z1_VPtagE_min3=sum((i>=120) and (i<180) for i in VP_Z1_TagE);Z1_VPtagF_min3=sum((i>=120) and (i<180) for i in VP_Z1_TagF);
             Z1_VPtagG_min3=sum((i>=120) and (i<180) for i in VP_Z1_TagG);Z1_VPtagH_min3=sum((i>=120) and (i<180) for i in VP_Z1_TagH);
             Z1_VPtagI_min3=sum((i>=120) and (i<180) for i in VP_Z1_TagI);Z1_VPtagJ_min3=sum((i>=120) and (i<180) for i in VP_Z1_TagJ);
             Z1_VPtagK_min3=sum((i>=120) and (i<180) for i in VP_Z1_TagK);Z1_VPtagL_min3=sum((i>=120) and (i<180) for i in VP_Z1_TagL);
             Z1_VPtagM_min3=sum((i>=120) and (i<180) for i in VP_Z1_TagM);Z1_VPtagN_min3=sum((i>=120) and (i<180) for i in VP_Z1_TagN)
             
             # minute 4
             Z1_VPtagA_min4=sum((i>=180) and (i<240) for i in VP_Z1_TagA);Z1_VPtagB_min4=sum((i>=180) and (i<240) for i in VP_Z1_TagB);
             Z1_VPtagC_min4=sum((i>=180) and (i<240) for i in VP_Z1_TagC);Z1_VPtagD_min4=sum((i>=180) and (i<240) for i in VP_Z1_TagD);
             Z1_VPtagE_min4=sum((i>=180) and (i<240) for i in VP_Z1_TagE);Z1_VPtagF_min4=sum((i>=180) and (i<240) for i in VP_Z1_TagF);
             Z1_VPtagG_min4=sum((i>=180) and (i<240) for i in VP_Z1_TagG);Z1_VPtagH_min4=sum((i>=180) and (i<240) for i in VP_Z1_TagH);
             Z1_VPtagI_min4=sum((i>=180) and (i<240) for i in VP_Z1_TagI);Z1_VPtagJ_min4=sum((i>=180) and (i<240) for i in VP_Z1_TagJ);
             Z1_VPtagK_min4=sum((i>=180) and (i<240) for i in VP_Z1_TagK);Z1_VPtagL_min4=sum((i>=180) and (i<240) for i in VP_Z1_TagL);
             Z1_VPtagM_min4=sum((i>=180) and (i<240) for i in VP_Z1_TagM);Z1_VPtagN_min4=sum((i>=180) and (i<240) for i in VP_Z1_TagN)
             
             # minute 5
             Z1_VPtagA_min5=sum((i>=240) and (i<300) for i in VP_Z1_TagA);Z1_VPtagB_min5=sum((i>=240) and (i<300) for i in VP_Z1_TagB);
             Z1_VPtagC_min5=sum((i>=240) and (i<300) for i in VP_Z1_TagC);Z1_VPtagD_min5=sum((i>=240) and (i<300) for i in VP_Z1_TagD);
             Z1_VPtagE_min5=sum((i>=240) and (i<300) for i in VP_Z1_TagE);Z1_VPtagF_min5=sum((i>=240) and (i<300) for i in VP_Z1_TagF);
             Z1_VPtagG_min5=sum((i>=240) and (i<300) for i in VP_Z1_TagG);Z1_VPtagH_min5=sum((i>=240) and (i<300) for i in VP_Z1_TagH);
             Z1_VPtagI_min5=sum((i>=240) and (i<300) for i in VP_Z1_TagI);Z1_VPtagJ_min5=sum((i>=240) and (i<300) for i in VP_Z1_TagJ);
             Z1_VPtagK_min5=sum((i>=240) and (i<300) for i in VP_Z1_TagK);Z1_VPtagL_min5=sum((i>=240) and (i<300) for i in VP_Z1_TagL);
             Z1_VPtagM_min5=sum((i>=240) and (i<300) for i in VP_Z1_TagM);Z1_VPtagN_min5=sum((i>=240) and (i<300) for i in VP_Z1_TagN)
             
             # minute 6
             Z1_VPtagA_min6=sum((i>=300) and (i<360) for i in VP_Z1_TagA);Z1_VPtagB_min6=sum((i>=300) and (i<360) for i in VP_Z1_TagB);
             Z1_VPtagC_min6=sum((i>=300) and (i<360) for i in VP_Z1_TagC);Z1_VPtagD_min6=sum((i>=300) and (i<360) for i in VP_Z1_TagD);
             Z1_VPtagE_min6=sum((i>=300) and (i<360) for i in VP_Z1_TagE);Z1_VPtagF_min6=sum((i>=300) and (i<360) for i in VP_Z1_TagF);
             Z1_VPtagG_min6=sum((i>=300) and (i<360) for i in VP_Z1_TagG);Z1_VPtagH_min6=sum((i>=300) and (i<360) for i in VP_Z1_TagH);
             Z1_VPtagI_min6=sum((i>=300) and (i<360) for i in VP_Z1_TagI);Z1_VPtagJ_min6=sum((i>=300) and (i<360)for i in VP_Z1_TagJ);
             Z1_VPtagK_min6=sum((i>=300) and (i<360) for i in VP_Z1_TagK);Z1_VPtagL_min6=sum((i>=300) and (i<360) for i in VP_Z1_TagL);
             Z1_VPtagM_min6=sum((i>=300) and (i<360) for i in VP_Z1_TagM);Z1_VPtagN_min6=sum((i>=300) and (i<360) for i in VP_Z1_TagN)
             
             # minute 7
             Z1_VPtagA_min7=sum((i>=360) and (i<420) for i in VP_Z1_TagA);Z1_VPtagB_min7=sum((i>=360) and (i<420) for i in VP_Z1_TagB);
             Z1_VPtagC_min7=sum((i>=360) and (i<420) for i in VP_Z1_TagC);Z1_VPtagD_min7=sum((i>=360) and (i<420) for i in VP_Z1_TagD);
             Z1_VPtagE_min7=sum((i>=360) and (i<420) for i in VP_Z1_TagE);Z1_VPtagF_min7=sum((i>=360) and (i<420) for i in VP_Z1_TagF);
             Z1_VPtagG_min7=sum((i>=360) and (i<420) for i in VP_Z1_TagG);Z1_VPtagH_min7=sum((i>=360) and (i<420) for i in VP_Z1_TagH);
             Z1_VPtagI_min7=sum((i>=360) and (i<420) for i in VP_Z1_TagI);Z1_VPtagJ_min7=sum((i>=360) and (i<420)for i in VP_Z1_TagJ);
             Z1_VPtagK_min7=sum((i>=360) and (i<420) for i in VP_Z1_TagK);Z1_VPtagL_min7=sum((i>=360) and (i<420) for i in VP_Z1_TagL);
             Z1_VPtagM_min7=sum((i>=360) and (i<420) for i in VP_Z1_TagM);Z1_VPtagN_min7=sum((i>=360) and (i<420) for i in VP_Z1_TagN)
             
             # minute 8
             Z1_VPtagA_min8=sum((i>=420) and (i<480) for i in VP_Z1_TagA);Z1_VPtagB_min8=sum((i>=420) and (i<480) for i in VP_Z1_TagB);
             Z1_VPtagC_min8=sum((i>=420) and (i<480) for i in VP_Z1_TagC);Z1_VPtagD_min8=sum((i>=420) and (i<480) for i in VP_Z1_TagD);
             Z1_VPtagE_min8=sum((i>=420) and (i<480) for i in VP_Z1_TagE);Z1_VPtagF_min8=sum((i>=420) and (i<480) for i in VP_Z1_TagF);
             Z1_VPtagG_min8=sum((i>=420) and (i<480) for i in VP_Z1_TagG);Z1_VPtagH_min8=sum((i>=420) and (i<480)for i in VP_Z1_TagH);
             Z1_VPtagI_min8=sum((i>=420) and (i<480) for i in VP_Z1_TagI);Z1_VPtagJ_min8=sum((i>=420) and (i<480)for i in VP_Z1_TagJ);
             Z1_VPtagK_min8=sum((i>=420) and (i<480) for i in VP_Z1_TagK);Z1_VPtagL_min8=sum((i>=420) and (i<480) for i in VP_Z1_TagL);
             Z1_VPtagM_min8=sum((i>=420) and (i<480) for i in VP_Z1_TagM);Z1_VPtagN_min8=sum((i>=420) and (i<480) for i in VP_Z1_TagN)
             
             # minute 9
             Z1_VPtagA_min9=sum((i>=480) and (i<540) for i in VP_Z1_TagA);Z1_VPtagB_min9=sum((i>=480) and (i<540) for i in VP_Z1_TagB);
             Z1_VPtagC_min9=sum((i>=480) and (i<540) for i in VP_Z1_TagC);Z1_VPtagD_min9=sum((i>=480) and (i<540) for i in VP_Z1_TagD);
             Z1_VPtagE_min9=sum((i>=480) and (i<540) for i in VP_Z1_TagE);Z1_VPtagF_min9=sum((i>=480) and (i<540) for i in VP_Z1_TagF);
             Z1_VPtagG_min9=sum((i>=480) and (i<540) for i in VP_Z1_TagG);Z1_VPtagH_min9=sum((i>=480) and (i<540) for i in VP_Z1_TagH);
             Z1_VPtagI_min9=sum((i>=480) and (i<540) for i in VP_Z1_TagI);Z1_VPtagJ_min9=sum((i>=480) and (i<540) for i in VP_Z1_TagJ);
             Z1_VPtagK_min9=sum((i>=480) and (i<540) for i in VP_Z1_TagK);Z1_VPtagL_min9=sum((i>=480) and (i<540) for i in VP_Z1_TagL);
             Z1_VPtagM_min9=sum((i>=480) and (i<540) for i in VP_Z1_TagM);Z1_VPtagN_min9=sum((i>=480) and (i<540) for i in VP_Z1_TagN)        

             # minute 10
             Z1_VPtagA_min10=sum((i>=540) and (i<600) for i in VP_Z1_TagA);Z1_VPtagB_min10=sum((i>=540) and (i<600) for i in VP_Z1_TagB);
             Z1_VPtagC_min10=sum((i>=540) and (i<600) for i in VP_Z1_TagC);Z1_VPtagD_min10=sum((i>=540) and (i<600) for i in VP_Z1_TagD);
             Z1_VPtagE_min10=sum((i>=540) and (i<600) for i in VP_Z1_TagE);Z1_VPtagF_min10=sum((i>=540) and (i<600) for i in VP_Z1_TagF);
             Z1_VPtagG_min10=sum((i>=540) and (i<600) for i in VP_Z1_TagG);Z1_VPtagH_min10=sum((i>=540) and (i<600) for i in VP_Z1_TagH);
             Z1_VPtagI_min10=sum((i>=540) and (i<600) for i in VP_Z1_TagI);Z1_VPtagJ_min10=sum((i>=540) and (i<600) for i in VP_Z1_TagJ);
             Z1_VPtagK_min10=sum((i>=540) and (i<600) for i in VP_Z1_TagK);Z1_VPtagL_min10=sum((i>=540) and (i<600) for i in VP_Z1_TagL);
             Z1_VPtagM_min10=sum((i>=540) and (i<600) for i in VP_Z1_TagM);Z1_VPtagN_min10=sum((i>=540) and (i<600) for i in VP_Z1_TagN)
             
             # minute 11
             Z1_VPtagA_min11=sum((i>=600) and (i<660) for i in VP_Z1_TagA);Z1_VPtagB_min11=sum((i>=600) and (i<660) for i in VP_Z1_TagB);
             Z1_VPtagC_min11=sum((i>=600) and (i<660) for i in VP_Z1_TagC);Z1_VPtagD_min11=sum((i>=600) and (i<660) for i in VP_Z1_TagD);
             Z1_VPtagE_min11=sum((i>=600) and (i<660) for i in VP_Z1_TagE);Z1_VPtagF_min11=sum((i>=600) and (i<660) for i in VP_Z1_TagF);
             Z1_VPtagG_min11=sum((i>=600) and (i<660) for i in VP_Z1_TagG);Z1_VPtagH_min11=sum((i>=600) and (i<660) for i in VP_Z1_TagH);
             Z1_VPtagI_min11=sum((i>=600) and (i<660) for i in VP_Z1_TagI);Z1_VPtagJ_min11=sum((i>=600) and (i<660) for i in VP_Z1_TagJ);
             Z1_VPtagK_min11=sum((i>=600) and (i<660) for i in VP_Z1_TagK);Z1_VPtagL_min11=sum((i>=600) and (i<660) for i in VP_Z1_TagL);
             Z1_VPtagM_min11=sum((i>=600) and (i<660) for i in VP_Z1_TagM);Z1_VPtagN_min11=sum((i>=600) and (i<660) for i in VP_Z1_TagN)
             
             # minute 12
             Z1_VPtagA_min12=sum((i>=660) and (i<720) for i in VP_Z1_TagA);Z1_VPtagB_min12=sum((i>=660) and (i<720) for i in VP_Z1_TagB);
             Z1_VPtagC_min12=sum((i>=660) and (i<720) for i in VP_Z1_TagC);Z1_VPtagD_min12=sum((i>=660) and (i<720) for i in VP_Z1_TagD);
             Z1_VPtagE_min12=sum((i>=660) and (i<720) for i in VP_Z1_TagE);Z1_VPtagF_min12=sum((i>=660) and (i<720) for i in VP_Z1_TagF);
             Z1_VPtagG_min12=sum((i>=660) and (i<720) for i in VP_Z1_TagG);Z1_VPtagH_min12=sum((i>=660) and (i<720) for i in VP_Z1_TagH);
             Z1_VPtagI_min12=sum((i>=660) and (i<720) for i in VP_Z1_TagI);Z1_VPtagJ_min12=sum((i>=660) and (i<720) for i in VP_Z1_TagJ);
             Z1_VPtagK_min12=sum((i>=660) and (i<720) for i in VP_Z1_TagK);Z1_VPtagL_min12=sum((i>=660) and (i<720) for i in VP_Z1_TagL);
             Z1_VPtagM_min12=sum((i>=660) and (i<720) for i in VP_Z1_TagM);Z1_VPtagN_min12=sum((i>=660) and (i<720) for i in VP_Z1_TagN)
             
             # minute 13
             Z1_VPtagA_min13=sum((i>=720) and (i<780) for i in VP_Z1_TagA);Z1_VPtagB_min13=sum((i>=720) and (i<780)for i in VP_Z1_TagB);
             Z1_VPtagC_min13=sum((i>=720) and (i<780) for i in VP_Z1_TagC);Z1_VPtagD_min13=sum((i>=720) and (i<780) for i in VP_Z1_TagD);
             Z1_VPtagE_min13=sum((i>=720) and (i<780) for i in VP_Z1_TagE);Z1_VPtagF_min13=sum((i>=720) and (i<780) for i in VP_Z1_TagF);
             Z1_VPtagG_min13=sum((i>=720) and (i<780) for i in VP_Z1_TagG);Z1_VPtagH_min13=sum((i>=720) and (i<780) for i in VP_Z1_TagH);
             Z1_VPtagI_min13=sum((i>=720) and (i<780) for i in VP_Z1_TagI);Z1_VPtagJ_min13=sum((i>=720) and (i<780) for i in VP_Z1_TagJ);
             Z1_VPtagK_min13=sum((i>=720) and (i<780) for i in VP_Z1_TagK);Z1_VPtagL_min13=sum((i>=720) and (i<780) for i in VP_Z1_TagL);
             Z1_VPtagM_min13=sum((i>=720) and (i<780) for i in VP_Z1_TagM);Z1_VPtagN_min13=sum((i>=720) and (i<780) for i in VP_Z1_TagN)
             
             # minute 14
             Z1_VPtagA_min14=sum((i>=780) and (i<840) for i in VP_Z1_TagA);Z1_VPtagB_min14=sum((i>=780) and (i<840) for i in VP_Z1_TagB);
             Z1_VPtagC_min14=sum((i>=780) and (i<840) for i in VP_Z1_TagC);Z1_VPtagD_min14=sum((i>=780) and (i<840) for i in VP_Z1_TagD);
             Z1_VPtagE_min14=sum((i>=780) and (i<840) for i in VP_Z1_TagE);Z1_VPtagF_min14=sum((i>=780) and (i<840) for i in VP_Z1_TagF);
             Z1_VPtagG_min14=sum((i>=780) and (i<840) for i in VP_Z1_TagG);Z1_VPtagH_min14=sum((i>=780) and (i<840) for i in VP_Z1_TagH);
             Z1_VPtagI_min14=sum((i>=780) and (i<840) for i in VP_Z1_TagI);Z1_VPtagJ_min14=sum((i>=780) and (i<840) for i in VP_Z1_TagJ);
             Z1_VPtagK_min14=sum((i>=780) and (i<840)for i in VP_Z1_TagK);Z1_VPtagL_min14=sum((i>=780) and (i<840) for i in VP_Z1_TagL);
             Z1_VPtagM_min14=sum((i>=780) and (i<840) for i in VP_Z1_TagM);Z1_VPtagN_min14=sum((i>=780) and (i<840) for i in VP_Z1_TagN)
             
             # minute 15
             Z1_VPtagA_min15=sum((i>=840) and (i<=900) for i in VP_Z1_TagA);Z1_VPtagB_min15=sum((i>=840) and (i<=900) for i in VP_Z1_TagB);
             Z1_VPtagC_min15=sum((i>=840) and (i<=900) for i in VP_Z1_TagC);Z1_VPtagD_min15=sum((i>=840) and (i<=900) for i in VP_Z1_TagD);
             Z1_VPtagE_min15=sum((i>=840) and (i<=900) for i in VP_Z1_TagE);Z1_VPtagF_min15=sum((i>=840) and (i<=900) for i in VP_Z1_TagF);
             Z1_VPtagG_min15=sum((i>=840) and (i<=900) for i in VP_Z1_TagG);Z1_VPtagH_min15=sum((i>=840) and (i<=900) for i in VP_Z1_TagH);
             Z1_VPtagI_min15=sum((i>=840) and (i<=900) for i in VP_Z1_TagI);Z1_VPtagJ_min15=sum((i>=840) and (i<=900) for i in VP_Z1_TagJ);
             Z1_VPtagK_min15=sum((i>=840) and (i<=900) for i in VP_Z1_TagK);Z1_VPtagL_min15=sum((i>=840) and (i<=900) for i in VP_Z1_TagL);
             Z1_VPtagM_min15=sum((i>=840) and (i<=900) for i in VP_Z1_TagM);Z1_VPtagN_min15=sum((i>=840) and (i<=900) for i in VP_Z1_TagN)
    ##############################################################################################################################
    # Zone 2

             Z2_VPtagA_mins=[];Z2_VPtagB_mins=[];Z2_VPtagC_mins=[];Z2_VPtagD_mins=[];Z2_VPtagE_mins=[];Z2_VPtagF_mins=[];Z2_VPtagG_mins=[];
             Z2_VPtagH_mins=[];Z2_VPtagI_mins=[];Z2_VPtagJ_mins=[];Z2_VPtagK_mins=[];Z2_VPtagL_mins=[];Z2_VPtagM_mins=[];Z2_VPtagN_mins=[]
             # minute 1              
             Z2_VPtagA_min1=sum(i <60 for i in VP_Z2_TagA);Z2_VPtagB_min1=sum(i <60 for i in VP_Z2_TagB);Z2_VPtagC_min1=sum(i <60 for i in VP_Z2_TagC);
             Z2_VPtagD_min1=sum(i <60 for i in VP_Z2_TagD);Z2_VPtagE_min1=sum(i <60 for i in VP_Z2_TagE);Z2_VPtagF_min1=sum(i <60 for i in VP_Z2_TagF);
             Z2_VPtagG_min1=sum(i <60 for i in VP_Z2_TagG);Z2_VPtagH_min1=sum(i <60 for i in VP_Z2_TagH);Z2_VPtagI_min1=sum(i <60 for i in VP_Z2_TagI);
             Z2_VPtagJ_min1=sum(i <60 for i in VP_Z2_TagJ);Z2_VPtagK_min1=sum(i <60 for i in VP_Z2_TagK);Z2_VPtagL_min1=sum(i <60 for i in VP_Z2_TagL);
             Z2_VPtagM_min1=sum(i <60 for i in VP_Z2_TagM);Z2_VPtagN_min1=sum(i <60 for i in VP_Z2_TagN)

             # minute 2
             Z2_VPtagA_min2=sum((i >=60) and (i <120) for i in VP_Z2_TagA);Z2_VPtagB_min2=sum((i >=60) and (i <120) for i in VP_Z2_TagB);
             Z2_VPtagC_min2=sum((i >=60) and (i <120) for i in VP_Z2_TagC);Z2_VPtagD_min2=sum((i >=60) and (i <120) for i in VP_Z2_TagD);
             Z2_VPtagE_min2=sum((i >=60) and (i <120) for i in VP_Z2_TagE);Z2_VPtagF_min2=sum((i >=60) and (i <120) for i in VP_Z2_TagF);
             Z2_VPtagG_min2=sum((i >=60) and (i <120) for i in VP_Z2_TagG);Z2_VPtagH_min2=sum((i >=60) and (i <120) for i in VP_Z2_TagH);
             Z2_VPtagI_min2=sum((i >=60) and (i <120) for i in VP_Z2_TagI);Z2_VPtagJ_min2=sum((i >=60) and (i <120) for i in VP_Z2_TagJ);
             Z2_VPtagK_min2=sum((i >=60) and (i <120) for i in VP_Z2_TagK);Z2_VPtagL_min2=sum((i >=60) and (i <120) for i in VP_Z2_TagL);
             Z2_VPtagM_min2=sum((i >=60) and (i <120) for i in VP_Z2_TagM);Z2_VPtagN_min2=sum((i >=60) and (i <120) for i in VP_Z2_TagN)

             # minute 3
             Z2_VPtagA_min3=sum((i>=120) and (i<180) for i in VP_Z2_TagA);Z2_VPtagB_min3=sum((i>=120) and (i<180) for i in VP_Z2_TagB);
             Z2_VPtagC_min3=sum((i>=120) and (i<180) for i in VP_Z2_TagC);Z2_VPtagD_min3=sum((i>=120) and (i<180) for i in VP_Z2_TagD);
             Z2_VPtagE_min3=sum((i>=120) and (i<180) for i in VP_Z2_TagE);Z2_VPtagF_min3=sum((i>=120) and (i<180) for i in VP_Z2_TagF);
             Z2_VPtagG_min3=sum((i>=120) and (i<180) for i in VP_Z2_TagG);Z2_VPtagH_min3=sum((i>=120) and (i<180) for i in VP_Z2_TagH);
             Z2_VPtagI_min3=sum((i>=120) and (i<180) for i in VP_Z2_TagI);Z2_VPtagJ_min3=sum((i>=120) and (i<180) for i in VP_Z2_TagJ);
             Z2_VPtagK_min3=sum((i>=120) and (i<180) for i in VP_Z2_TagK);Z2_VPtagL_min3=sum((i>=120) and (i<180) for i in VP_Z2_TagL);
             Z2_VPtagM_min3=sum((i>=120) and (i<180) for i in VP_Z2_TagM);Z2_VPtagN_min3=sum((i>=120) and (i<180) for i in VP_Z2_TagN)
             
             # minute 4
             Z2_VPtagA_min4=sum((i>=180) and (i<240) for i in VP_Z2_TagA);Z2_VPtagB_min4=sum((i>=180) and (i<240) for i in VP_Z2_TagB);
             Z2_VPtagC_min4=sum((i>=180) and (i<240) for i in VP_Z2_TagC);Z2_VPtagD_min4=sum((i>=180) and (i<240) for i in VP_Z2_TagD);
             Z2_VPtagE_min4=sum((i>=180) and (i<240) for i in VP_Z2_TagE);Z2_VPtagF_min4=sum((i>=180) and (i<240) for i in VP_Z2_TagF);
             Z2_VPtagG_min4=sum((i>=180) and (i<240) for i in VP_Z2_TagG);Z2_VPtagH_min4=sum((i>=180) and (i<240) for i in VP_Z2_TagH);
             Z2_VPtagI_min4=sum((i>=180) and (i<240) for i in VP_Z2_TagI);Z2_VPtagJ_min4=sum((i>=180) and (i<240) for i in VP_Z2_TagJ);
             Z2_VPtagK_min4=sum((i>=180) and (i<240) for i in VP_Z2_TagK);Z2_VPtagL_min4=sum((i>=180) and (i<240) for i in VP_Z2_TagL);
             Z2_VPtagM_min4=sum((i>=180) and (i<240) for i in VP_Z2_TagM);Z2_VPtagN_min4=sum((i>=180) and (i<240) for i in VP_Z2_TagN)
             
             # minute 5
             Z2_VPtagA_min5=sum((i>=240) and (i<300) for i in VP_Z2_TagA);Z2_VPtagB_min5=sum((i>=240) and (i<300) for i in VP_Z2_TagB);
             Z2_VPtagC_min5=sum((i>=240) and (i<300) for i in VP_Z2_TagC);Z2_VPtagD_min5=sum((i>=240) and (i<300) for i in VP_Z2_TagD);
             Z2_VPtagE_min5=sum((i>=240) and (i<300) for i in VP_Z2_TagE);Z2_VPtagF_min5=sum((i>=240) and (i<300) for i in VP_Z2_TagF);
             Z2_VPtagG_min5=sum((i>=240) and (i<300) for i in VP_Z2_TagG);Z2_VPtagH_min5=sum((i>=240) and (i<300) for i in VP_Z2_TagH);
             Z2_VPtagI_min5=sum((i>=240) and (i<300) for i in VP_Z2_TagI);Z2_VPtagJ_min5=sum((i>=240) and (i<300) for i in VP_Z2_TagJ);
             Z2_VPtagK_min5=sum((i>=240) and (i<300) for i in VP_Z2_TagK);Z2_VPtagL_min5=sum((i>=240) and (i<300) for i in VP_Z2_TagL);
             Z2_VPtagM_min5=sum((i>=240) and (i<300) for i in VP_Z2_TagM);Z2_VPtagN_min5=sum((i>=240) and (i<300) for i in VP_Z2_TagN)
             
             # minute 6
             Z2_VPtagA_min6=sum((i>=300) and (i<360) for i in VP_Z2_TagA);Z2_VPtagB_min6=sum((i>=300) and (i<360) for i in VP_Z2_TagB);
             Z2_VPtagC_min6=sum((i>=300) and (i<360) for i in VP_Z2_TagC);Z2_VPtagD_min6=sum((i>=300) and (i<360) for i in VP_Z2_TagD);
             Z2_VPtagE_min6=sum((i>=300) and (i<360) for i in VP_Z2_TagE);Z2_VPtagF_min6=sum((i>=300) and (i<360) for i in VP_Z2_TagF);
             Z2_VPtagG_min6=sum((i>=300) and (i<360) for i in VP_Z2_TagG);Z2_VPtagH_min6=sum((i>=300) and (i<360) for i in VP_Z2_TagH);
             Z2_VPtagI_min6=sum((i>=300) and (i<360) for i in VP_Z2_TagI);Z2_VPtagJ_min6=sum((i>=300) and (i<360)for i in VP_Z2_TagJ);
             Z2_VPtagK_min6=sum((i>=300) and (i<360) for i in VP_Z2_TagK);Z2_VPtagL_min6=sum((i>=300) and (i<360) for i in VP_Z2_TagL);
             Z2_VPtagM_min6=sum((i>=300) and (i<360) for i in VP_Z2_TagM);Z2_VPtagN_min6=sum((i>=300) and (i<360) for i in VP_Z2_TagN)
             
             # minute 7
             Z2_VPtagA_min7=sum((i>=360) and (i<420) for i in VP_Z2_TagA);Z2_VPtagB_min7=sum((i>=360) and (i<420) for i in VP_Z2_TagB);
             Z2_VPtagC_min7=sum((i>=360) and (i<420) for i in VP_Z2_TagC);Z2_VPtagD_min7=sum((i>=360) and (i<420) for i in VP_Z2_TagD);
             Z2_VPtagE_min7=sum((i>=360) and (i<420) for i in VP_Z2_TagE);Z2_VPtagF_min7=sum((i>=360) and (i<420) for i in VP_Z2_TagF);
             Z2_VPtagG_min7=sum((i>=360) and (i<420) for i in VP_Z2_TagG);Z2_VPtagH_min7=sum((i>=360) and (i<420) for i in VP_Z2_TagH);
             Z2_VPtagI_min7=sum((i>=360) and (i<420) for i in VP_Z2_TagI);Z2_VPtagJ_min7=sum((i>=360) and (i<420)for i in VP_Z2_TagJ);
             Z2_VPtagK_min7=sum((i>=360) and (i<420) for i in VP_Z2_TagK);Z2_VPtagL_min7=sum((i>=360) and (i<420) for i in VP_Z2_TagL);
             Z2_VPtagM_min7=sum((i>=360) and (i<420) for i in VP_Z2_TagM);Z2_VPtagN_min7=sum((i>=360) and (i<420) for i in VP_Z2_TagN)
             
             # minute 8
             Z2_VPtagA_min8=sum((i>=420) and (i<480) for i in VP_Z2_TagA);Z2_VPtagB_min8=sum((i>=420) and (i<480) for i in VP_Z2_TagB);
             Z2_VPtagC_min8=sum((i>=420) and (i<480) for i in VP_Z2_TagC);Z2_VPtagD_min8=sum((i>=420) and (i<480) for i in VP_Z2_TagD);
             Z2_VPtagE_min8=sum((i>=420) and (i<480) for i in VP_Z2_TagE);Z2_VPtagF_min8=sum((i>=420) and (i<480) for i in VP_Z2_TagF);
             Z2_VPtagG_min8=sum((i>=420) and (i<480) for i in VP_Z2_TagG);Z2_VPtagH_min8=sum((i>=420) and (i<480)for i in VP_Z2_TagH);
             Z2_VPtagI_min8=sum((i>=420) and (i<480) for i in VP_Z2_TagI);Z2_VPtagJ_min8=sum((i>=420) and (i<480)for i in VP_Z2_TagJ);
             Z2_VPtagK_min8=sum((i>=420) and (i<480) for i in VP_Z2_TagK);Z2_VPtagL_min8=sum((i>=420) and (i<480) for i in VP_Z2_TagL);
             Z2_VPtagM_min8=sum((i>=420) and (i<480) for i in VP_Z2_TagM);Z2_VPtagN_min8=sum((i>=420) and (i<480) for i in VP_Z2_TagN)
             
             # minute 9
             Z2_VPtagA_min9=sum((i>=480) and (i<540) for i in VP_Z2_TagA);Z2_VPtagB_min9=sum((i>=480) and (i<540) for i in VP_Z2_TagB);
             Z2_VPtagC_min9=sum((i>=480) and (i<540) for i in VP_Z2_TagC);Z2_VPtagD_min9=sum((i>=480) and (i<540) for i in VP_Z2_TagD);
             Z2_VPtagE_min9=sum((i>=480) and (i<540) for i in VP_Z2_TagE);Z2_VPtagF_min9=sum((i>=480) and (i<540) for i in VP_Z2_TagF);
             Z2_VPtagG_min9=sum((i>=480) and (i<540) for i in VP_Z2_TagG);Z2_VPtagH_min9=sum((i>=480) and (i<540) for i in VP_Z2_TagH);
             Z2_VPtagI_min9=sum((i>=480) and (i<540) for i in VP_Z2_TagI);Z2_VPtagJ_min9=sum((i>=480) and (i<540) for i in VP_Z2_TagJ);
             Z2_VPtagK_min9=sum((i>=480) and (i<540) for i in VP_Z2_TagK);Z2_VPtagL_min9=sum((i>=480) and (i<540) for i in VP_Z2_TagL);
             Z2_VPtagM_min9=sum((i>=480) and (i<540) for i in VP_Z2_TagM);Z2_VPtagN_min9=sum((i>=480) and (i<540) for i in VP_Z2_TagN)        

             # minute 10
             Z2_VPtagA_min10=sum((i>=540) and (i<600) for i in VP_Z2_TagA);Z2_VPtagB_min10=sum((i>=540) and (i<600) for i in VP_Z2_TagB);
             Z2_VPtagC_min10=sum((i>=540) and (i<600) for i in VP_Z2_TagC);Z2_VPtagD_min10=sum((i>=540) and (i<600) for i in VP_Z2_TagD);
             Z2_VPtagE_min10=sum((i>=540) and (i<600) for i in VP_Z2_TagE);Z2_VPtagF_min10=sum((i>=540) and (i<600) for i in VP_Z2_TagF);
             Z2_VPtagG_min10=sum((i>=540) and (i<600) for i in VP_Z2_TagG);Z2_VPtagH_min10=sum((i>=540) and (i<600) for i in VP_Z2_TagH);
             Z2_VPtagI_min10=sum((i>=540) and (i<600) for i in VP_Z2_TagI);Z2_VPtagJ_min10=sum((i>=540) and (i<600) for i in VP_Z2_TagJ);
             Z2_VPtagK_min10=sum((i>=540) and (i<600) for i in VP_Z2_TagK);Z2_VPtagL_min10=sum((i>=540) and (i<600) for i in VP_Z2_TagL);
             Z2_VPtagM_min10=sum((i>=540) and (i<600) for i in VP_Z2_TagM);Z2_VPtagN_min10=sum((i>=540) and (i<600) for i in VP_Z2_TagN)
             
             # minute 11
             Z2_VPtagA_min11=sum((i>=600) and (i<660) for i in VP_Z2_TagA);Z2_VPtagB_min11=sum((i>=600) and (i<660) for i in VP_Z2_TagB);
             Z2_VPtagC_min11=sum((i>=600) and (i<660) for i in VP_Z2_TagC);Z2_VPtagD_min11=sum((i>=600) and (i<660) for i in VP_Z2_TagD);
             Z2_VPtagE_min11=sum((i>=600) and (i<660) for i in VP_Z2_TagE);Z2_VPtagF_min11=sum((i>=600) and (i<660) for i in VP_Z2_TagF);
             Z2_VPtagG_min11=sum((i>=600) and (i<660) for i in VP_Z2_TagG);Z2_VPtagH_min11=sum((i>=600) and (i<660) for i in VP_Z2_TagH);
             Z2_VPtagI_min11=sum((i>=600) and (i<660) for i in VP_Z2_TagI);Z2_VPtagJ_min11=sum((i>=600) and (i<660) for i in VP_Z2_TagJ);
             Z2_VPtagK_min11=sum((i>=600) and (i<660) for i in VP_Z2_TagK);Z2_VPtagL_min11=sum((i>=600) and (i<660) for i in VP_Z2_TagL);
             Z2_VPtagM_min11=sum((i>=600) and (i<660) for i in VP_Z2_TagM);Z2_VPtagN_min11=sum((i>=600) and (i<660) for i in VP_Z2_TagN)
             
             # minute 12
             Z2_VPtagA_min12=sum((i>=660) and (i<720) for i in VP_Z2_TagA);Z2_VPtagB_min12=sum((i>=660) and (i<720) for i in VP_Z2_TagB);
             Z2_VPtagC_min12=sum((i>=660) and (i<720) for i in VP_Z2_TagC);Z2_VPtagD_min12=sum((i>=660) and (i<720) for i in VP_Z2_TagD);
             Z2_VPtagE_min12=sum((i>=660) and (i<720) for i in VP_Z2_TagE);Z2_VPtagF_min12=sum((i>=660) and (i<720) for i in VP_Z2_TagF);
             Z2_VPtagG_min12=sum((i>=660) and (i<720) for i in VP_Z2_TagG);Z2_VPtagH_min12=sum((i>=660) and (i<720) for i in VP_Z2_TagH);
             Z2_VPtagI_min12=sum((i>=660) and (i<720) for i in VP_Z2_TagI);Z2_VPtagJ_min12=sum((i>=660) and (i<720) for i in VP_Z2_TagJ);
             Z2_VPtagK_min12=sum((i>=660) and (i<720) for i in VP_Z2_TagK);Z2_VPtagL_min12=sum((i>=660) and (i<720) for i in VP_Z2_TagL);
             Z2_VPtagM_min12=sum((i>=660) and (i<720) for i in VP_Z2_TagM);Z2_VPtagN_min12=sum((i>=660) and (i<720) for i in VP_Z2_TagN)
             
             # minute 13
             Z2_VPtagA_min13=sum((i>=720) and (i<780) for i in VP_Z2_TagA);Z2_VPtagB_min13=sum((i>=720) and (i<780)for i in VP_Z2_TagB);
             Z2_VPtagC_min13=sum((i>=720) and (i<780) for i in VP_Z2_TagC);Z2_VPtagD_min13=sum((i>=720) and (i<780) for i in VP_Z2_TagD);
             Z2_VPtagE_min13=sum((i>=720) and (i<780) for i in VP_Z2_TagE);Z2_VPtagF_min13=sum((i>=720) and (i<780) for i in VP_Z2_TagF);
             Z2_VPtagG_min13=sum((i>=720) and (i<780) for i in VP_Z2_TagG);Z2_VPtagH_min13=sum((i>=720) and (i<780) for i in VP_Z2_TagH);
             Z2_VPtagI_min13=sum((i>=720) and (i<780) for i in VP_Z2_TagI);Z2_VPtagJ_min13=sum((i>=720) and (i<780) for i in VP_Z2_TagJ);
             Z2_VPtagK_min13=sum((i>=720) and (i<780) for i in VP_Z2_TagK);Z2_VPtagL_min13=sum((i>=720) and (i<780) for i in VP_Z2_TagL);
             Z2_VPtagM_min13=sum((i>=720) and (i<780) for i in VP_Z2_TagM);Z2_VPtagN_min13=sum((i>=720) and (i<780) for i in VP_Z2_TagN)
             
             # minute 14
             Z2_VPtagA_min14=sum((i>=780) and (i<840) for i in VP_Z2_TagA);Z2_VPtagB_min14=sum((i>=780) and (i<840) for i in VP_Z2_TagB);
             Z2_VPtagC_min14=sum((i>=780) and (i<840) for i in VP_Z2_TagC);Z2_VPtagD_min14=sum((i>=780) and (i<840) for i in VP_Z2_TagD);
             Z2_VPtagE_min14=sum((i>=780) and (i<840) for i in VP_Z2_TagE);Z2_VPtagF_min14=sum((i>=780) and (i<840) for i in VP_Z2_TagF);
             Z2_VPtagG_min14=sum((i>=780) and (i<840) for i in VP_Z2_TagG);Z2_VPtagH_min14=sum((i>=780) and (i<840) for i in VP_Z2_TagH);
             Z2_VPtagI_min14=sum((i>=780) and (i<840) for i in VP_Z2_TagI);Z2_VPtagJ_min14=sum((i>=780) and (i<840) for i in VP_Z2_TagJ);
             Z2_VPtagK_min14=sum((i>=780) and (i<840)for i in VP_Z2_TagK);Z2_VPtagL_min14=sum((i>=780) and (i<840) for i in VP_Z2_TagL);
             Z2_VPtagM_min14=sum((i>=780) and (i<840) for i in VP_Z2_TagM);Z2_VPtagN_min14=sum((i>=780) and (i<840) for i in VP_Z2_TagN)
             
             # minute 15
             Z2_VPtagA_min15=sum((i>=840) and (i<=900) for i in VP_Z2_TagA);Z2_VPtagB_min15=sum((i>=840) and (i<=900) for i in VP_Z2_TagB);
             Z2_VPtagC_min15=sum((i>=840) and (i<=900) for i in VP_Z2_TagC);Z2_VPtagD_min15=sum((i>=840) and (i<=900) for i in VP_Z2_TagD);
             Z2_VPtagE_min15=sum((i>=840) and (i<=900) for i in VP_Z2_TagE);Z2_VPtagF_min15=sum((i>=840) and (i<=900) for i in VP_Z2_TagF);
             Z2_VPtagG_min15=sum((i>=840) and (i<=900) for i in VP_Z2_TagG);Z2_VPtagH_min15=sum((i>=840) and (i<=900) for i in VP_Z2_TagH);
             Z2_VPtagI_min15=sum((i>=840) and (i<=900) for i in VP_Z2_TagI);Z2_VPtagJ_min15=sum((i>=840) and (i<=900) for i in VP_Z2_TagJ);
             Z2_VPtagK_min15=sum((i>=840) and (i<=900) for i in VP_Z2_TagK);Z2_VPtagL_min15=sum((i>=840) and (i<=900) for i in VP_Z2_TagL);
             Z2_VPtagM_min15=sum((i>=840) and (i<=900) for i in VP_Z2_TagM);Z2_VPtagN_min15=sum((i>=840) and (i<=900) for i in VP_Z2_TagN)

    ##############################################################################################################################
    # Zone 3

             Z3_VPtagA_mins=[];Z3_VPtagB_mins=[];Z3_VPtagC_mins=[];Z3_VPtagD_mins=[];Z3_VPtagE_mins=[];Z3_VPtagF_mins=[];Z3_VPtagG_mins=[];
             Z3_VPtagH_mins=[];Z3_VPtagI_mins=[];Z3_VPtagJ_mins=[];Z3_VPtagK_mins=[];Z3_VPtagL_mins=[];Z3_VPtagM_mins=[];Z3_VPtagN_mins=[]
             # minute 1              
             Z3_VPtagA_min1=sum(i <60 for i in VP_Z3_TagA);Z3_VPtagB_min1=sum(i <60 for i in VP_Z3_TagB);Z3_VPtagC_min1=sum(i <60 for i in VP_Z3_TagC);
             Z3_VPtagD_min1=sum(i <60 for i in VP_Z3_TagD);Z3_VPtagE_min1=sum(i <60 for i in VP_Z3_TagE);Z3_VPtagF_min1=sum(i <60 for i in VP_Z3_TagF);
             Z3_VPtagG_min1=sum(i <60 for i in VP_Z3_TagG);Z3_VPtagH_min1=sum(i <60 for i in VP_Z3_TagH);Z3_VPtagI_min1=sum(i <60 for i in VP_Z3_TagI);
             Z3_VPtagJ_min1=sum(i <60 for i in VP_Z3_TagJ);Z3_VPtagK_min1=sum(i <60 for i in VP_Z3_TagK);Z3_VPtagL_min1=sum(i <60 for i in VP_Z3_TagL);
             Z3_VPtagM_min1=sum(i <60 for i in VP_Z3_TagM);Z3_VPtagN_min1=sum(i <60 for i in VP_Z3_TagN)

             # minute 2
             Z3_VPtagA_min2=sum((i >=60) and (i <120) for i in VP_Z3_TagA);Z3_VPtagB_min2=sum((i >=60) and (i <120) for i in VP_Z3_TagB);
             Z3_VPtagC_min2=sum((i >=60) and (i <120) for i in VP_Z3_TagC);Z3_VPtagD_min2=sum((i >=60) and (i <120) for i in VP_Z3_TagD);
             Z3_VPtagE_min2=sum((i >=60) and (i <120) for i in VP_Z3_TagE);Z3_VPtagF_min2=sum((i >=60) and (i <120) for i in VP_Z3_TagF);
             Z3_VPtagG_min2=sum((i >=60) and (i <120) for i in VP_Z3_TagG);Z3_VPtagH_min2=sum((i >=60) and (i <120) for i in VP_Z3_TagH);
             Z3_VPtagI_min2=sum((i >=60) and (i <120) for i in VP_Z3_TagI);Z3_VPtagJ_min2=sum((i >=60) and (i <120) for i in VP_Z3_TagJ);
             Z3_VPtagK_min2=sum((i >=60) and (i <120) for i in VP_Z3_TagK);Z3_VPtagL_min2=sum((i >=60) and (i <120) for i in VP_Z3_TagL);
             Z3_VPtagM_min2=sum((i >=60) and (i <120) for i in VP_Z3_TagM);Z3_VPtagN_min2=sum((i >=60) and (i <120) for i in VP_Z3_TagN)

             # minute 3
             Z3_VPtagA_min3=sum((i>=120) and (i<180) for i in VP_Z3_TagA);Z3_VPtagB_min3=sum((i>=120) and (i<180) for i in VP_Z3_TagB);
             Z3_VPtagC_min3=sum((i>=120) and (i<180) for i in VP_Z3_TagC);Z3_VPtagD_min3=sum((i>=120) and (i<180) for i in VP_Z3_TagD);
             Z3_VPtagE_min3=sum((i>=120) and (i<180) for i in VP_Z3_TagE);Z3_VPtagF_min3=sum((i>=120) and (i<180) for i in VP_Z3_TagF);
             Z3_VPtagG_min3=sum((i>=120) and (i<180) for i in VP_Z3_TagG);Z3_VPtagH_min3=sum((i>=120) and (i<180) for i in VP_Z3_TagH);
             Z3_VPtagI_min3=sum((i>=120) and (i<180) for i in VP_Z3_TagI);Z3_VPtagJ_min3=sum((i>=120) and (i<180) for i in VP_Z3_TagJ);
             Z3_VPtagK_min3=sum((i>=120) and (i<180) for i in VP_Z3_TagK);Z3_VPtagL_min3=sum((i>=120) and (i<180) for i in VP_Z3_TagL);
             Z3_VPtagM_min3=sum((i>=120) and (i<180) for i in VP_Z3_TagM);Z3_VPtagN_min3=sum((i>=120) and (i<180) for i in VP_Z3_TagN)
             
             # minute 4
             Z3_VPtagA_min4=sum((i>=180) and (i<240) for i in VP_Z3_TagA);Z3_VPtagB_min4=sum((i>=180) and (i<240) for i in VP_Z3_TagB);
             Z3_VPtagC_min4=sum((i>=180) and (i<240) for i in VP_Z3_TagC);Z3_VPtagD_min4=sum((i>=180) and (i<240) for i in VP_Z3_TagD);
             Z3_VPtagE_min4=sum((i>=180) and (i<240) for i in VP_Z3_TagE);Z3_VPtagF_min4=sum((i>=180) and (i<240) for i in VP_Z3_TagF);
             Z3_VPtagG_min4=sum((i>=180) and (i<240) for i in VP_Z3_TagG);Z3_VPtagH_min4=sum((i>=180) and (i<240) for i in VP_Z3_TagH);
             Z3_VPtagI_min4=sum((i>=180) and (i<240) for i in VP_Z3_TagI);Z3_VPtagJ_min4=sum((i>=180) and (i<240) for i in VP_Z3_TagJ);
             Z3_VPtagK_min4=sum((i>=180) and (i<240) for i in VP_Z3_TagK);Z3_VPtagL_min4=sum((i>=180) and (i<240) for i in VP_Z3_TagL);
             Z3_VPtagM_min4=sum((i>=180) and (i<240) for i in VP_Z3_TagM);Z3_VPtagN_min4=sum((i>=180) and (i<240) for i in VP_Z3_TagN)
             
             # minute 5
             Z3_VPtagA_min5=sum((i>=240) and (i<300) for i in VP_Z3_TagA);Z3_VPtagB_min5=sum((i>=240) and (i<300) for i in VP_Z3_TagB);
             Z3_VPtagC_min5=sum((i>=240) and (i<300) for i in VP_Z3_TagC);Z3_VPtagD_min5=sum((i>=240) and (i<300) for i in VP_Z3_TagD);
             Z3_VPtagE_min5=sum((i>=240) and (i<300) for i in VP_Z3_TagE);Z3_VPtagF_min5=sum((i>=240) and (i<300) for i in VP_Z3_TagF);
             Z3_VPtagG_min5=sum((i>=240) and (i<300) for i in VP_Z3_TagG);Z3_VPtagH_min5=sum((i>=240) and (i<300) for i in VP_Z3_TagH);
             Z3_VPtagI_min5=sum((i>=240) and (i<300) for i in VP_Z3_TagI);Z3_VPtagJ_min5=sum((i>=240) and (i<300) for i in VP_Z3_TagJ);
             Z3_VPtagK_min5=sum((i>=240) and (i<300) for i in VP_Z3_TagK);Z3_VPtagL_min5=sum((i>=240) and (i<300) for i in VP_Z3_TagL);
             Z3_VPtagM_min5=sum((i>=240) and (i<300) for i in VP_Z3_TagM);Z3_VPtagN_min5=sum((i>=240) and (i<300) for i in VP_Z3_TagN)
             
             # minute 6
             Z3_VPtagA_min6=sum((i>=300) and (i<360) for i in VP_Z3_TagA);Z3_VPtagB_min6=sum((i>=300) and (i<360) for i in VP_Z3_TagB);
             Z3_VPtagC_min6=sum((i>=300) and (i<360) for i in VP_Z3_TagC);Z3_VPtagD_min6=sum((i>=300) and (i<360) for i in VP_Z3_TagD);
             Z3_VPtagE_min6=sum((i>=300) and (i<360) for i in VP_Z3_TagE);Z3_VPtagF_min6=sum((i>=300) and (i<360) for i in VP_Z3_TagF);
             Z3_VPtagG_min6=sum((i>=300) and (i<360) for i in VP_Z3_TagG);Z3_VPtagH_min6=sum((i>=300) and (i<360) for i in VP_Z3_TagH);
             Z3_VPtagI_min6=sum((i>=300) and (i<360) for i in VP_Z3_TagI);Z3_VPtagJ_min6=sum((i>=300) and (i<360)for i in VP_Z3_TagJ);
             Z3_VPtagK_min6=sum((i>=300) and (i<360) for i in VP_Z3_TagK);Z3_VPtagL_min6=sum((i>=300) and (i<360) for i in VP_Z3_TagL);
             Z3_VPtagM_min6=sum((i>=300) and (i<360) for i in VP_Z3_TagM);Z3_VPtagN_min6=sum((i>=300) and (i<360) for i in VP_Z3_TagN)
             
             # minute 7
             Z3_VPtagA_min7=sum((i>=360) and (i<420) for i in VP_Z3_TagA);Z3_VPtagB_min7=sum((i>=360) and (i<420) for i in VP_Z3_TagB);
             Z3_VPtagC_min7=sum((i>=360) and (i<420) for i in VP_Z3_TagC);Z3_VPtagD_min7=sum((i>=360) and (i<420) for i in VP_Z3_TagD);
             Z3_VPtagE_min7=sum((i>=360) and (i<420) for i in VP_Z3_TagE);Z3_VPtagF_min7=sum((i>=360) and (i<420) for i in VP_Z3_TagF);
             Z3_VPtagG_min7=sum((i>=360) and (i<420) for i in VP_Z3_TagG);Z3_VPtagH_min7=sum((i>=360) and (i<420) for i in VP_Z3_TagH);
             Z3_VPtagI_min7=sum((i>=360) and (i<420) for i in VP_Z3_TagI);Z3_VPtagJ_min7=sum((i>=360) and (i<420)for i in VP_Z3_TagJ);
             Z3_VPtagK_min7=sum((i>=360) and (i<420) for i in VP_Z3_TagK);Z3_VPtagL_min7=sum((i>=360) and (i<420) for i in VP_Z3_TagL);
             Z3_VPtagM_min7=sum((i>=360) and (i<420) for i in VP_Z3_TagM);Z3_VPtagN_min7=sum((i>=360) and (i<420) for i in VP_Z3_TagN)
             
             # minute 8
             Z3_VPtagA_min8=sum((i>=420) and (i<480) for i in VP_Z3_TagA);Z3_VPtagB_min8=sum((i>=420) and (i<480) for i in VP_Z3_TagB);
             Z3_VPtagC_min8=sum((i>=420) and (i<480) for i in VP_Z3_TagC);Z3_VPtagD_min8=sum((i>=420) and (i<480) for i in VP_Z3_TagD);
             Z3_VPtagE_min8=sum((i>=420) and (i<480) for i in VP_Z3_TagE);Z3_VPtagF_min8=sum((i>=420) and (i<480) for i in VP_Z3_TagF);
             Z3_VPtagG_min8=sum((i>=420) and (i<480) for i in VP_Z3_TagG);Z3_VPtagH_min8=sum((i>=420) and (i<480)for i in VP_Z3_TagH);
             Z3_VPtagI_min8=sum((i>=420) and (i<480) for i in VP_Z3_TagI);Z3_VPtagJ_min8=sum((i>=420) and (i<480)for i in VP_Z3_TagJ);
             Z3_VPtagK_min8=sum((i>=420) and (i<480) for i in VP_Z3_TagK);Z3_VPtagL_min8=sum((i>=420) and (i<480) for i in VP_Z3_TagL);
             Z3_VPtagM_min8=sum((i>=420) and (i<480) for i in VP_Z3_TagM);Z3_VPtagN_min8=sum((i>=420) and (i<480) for i in VP_Z3_TagN)
             
             # minute 9
             Z3_VPtagA_min9=sum((i>=480) and (i<540) for i in VP_Z3_TagA);Z3_VPtagB_min9=sum((i>=480) and (i<540) for i in VP_Z3_TagB);
             Z3_VPtagC_min9=sum((i>=480) and (i<540) for i in VP_Z3_TagC);Z3_VPtagD_min9=sum((i>=480) and (i<540) for i in VP_Z3_TagD);
             Z3_VPtagE_min9=sum((i>=480) and (i<540) for i in VP_Z3_TagE);Z3_VPtagF_min9=sum((i>=480) and (i<540) for i in VP_Z3_TagF);
             Z3_VPtagG_min9=sum((i>=480) and (i<540) for i in VP_Z3_TagG);Z3_VPtagH_min9=sum((i>=480) and (i<540) for i in VP_Z3_TagH);
             Z3_VPtagI_min9=sum((i>=480) and (i<540) for i in VP_Z3_TagI);Z3_VPtagJ_min9=sum((i>=480) and (i<540) for i in VP_Z3_TagJ);
             Z3_VPtagK_min9=sum((i>=480) and (i<540) for i in VP_Z3_TagK);Z3_VPtagL_min9=sum((i>=480) and (i<540) for i in VP_Z3_TagL);
             Z3_VPtagM_min9=sum((i>=480) and (i<540) for i in VP_Z3_TagM);Z3_VPtagN_min9=sum((i>=480) and (i<540) for i in VP_Z3_TagN)        

             # minute 10
             Z3_VPtagA_min10=sum((i>=540) and (i<600) for i in VP_Z3_TagA);Z3_VPtagB_min10=sum((i>=540) and (i<600) for i in VP_Z3_TagB);
             Z3_VPtagC_min10=sum((i>=540) and (i<600) for i in VP_Z3_TagC);Z3_VPtagD_min10=sum((i>=540) and (i<600) for i in VP_Z3_TagD);
             Z3_VPtagE_min10=sum((i>=540) and (i<600) for i in VP_Z3_TagE);Z3_VPtagF_min10=sum((i>=540) and (i<600) for i in VP_Z3_TagF);
             Z3_VPtagG_min10=sum((i>=540) and (i<600) for i in VP_Z3_TagG);Z3_VPtagH_min10=sum((i>=540) and (i<600) for i in VP_Z3_TagH);
             Z3_VPtagI_min10=sum((i>=540) and (i<600) for i in VP_Z3_TagI);Z3_VPtagJ_min10=sum((i>=540) and (i<600) for i in VP_Z3_TagJ);
             Z3_VPtagK_min10=sum((i>=540) and (i<600) for i in VP_Z3_TagK);Z3_VPtagL_min10=sum((i>=540) and (i<600) for i in VP_Z3_TagL);
             Z3_VPtagM_min10=sum((i>=540) and (i<600) for i in VP_Z3_TagM);Z3_VPtagN_min10=sum((i>=540) and (i<600) for i in VP_Z3_TagN)
             
             # minute 11
             Z3_VPtagA_min11=sum((i>=600) and (i<660) for i in VP_Z3_TagA);Z3_VPtagB_min11=sum((i>=600) and (i<660) for i in VP_Z3_TagB);
             Z3_VPtagC_min11=sum((i>=600) and (i<660) for i in VP_Z3_TagC);Z3_VPtagD_min11=sum((i>=600) and (i<660) for i in VP_Z3_TagD);
             Z3_VPtagE_min11=sum((i>=600) and (i<660) for i in VP_Z3_TagE);Z3_VPtagF_min11=sum((i>=600) and (i<660) for i in VP_Z3_TagF);
             Z3_VPtagG_min11=sum((i>=600) and (i<660) for i in VP_Z3_TagG);Z3_VPtagH_min11=sum((i>=600) and (i<660) for i in VP_Z3_TagH);
             Z3_VPtagI_min11=sum((i>=600) and (i<660) for i in VP_Z3_TagI);Z3_VPtagJ_min11=sum((i>=600) and (i<660) for i in VP_Z3_TagJ);
             Z3_VPtagK_min11=sum((i>=600) and (i<660) for i in VP_Z3_TagK);Z3_VPtagL_min11=sum((i>=600) and (i<660) for i in VP_Z3_TagL);
             Z3_VPtagM_min11=sum((i>=600) and (i<660) for i in VP_Z3_TagM);Z3_VPtagN_min11=sum((i>=600) and (i<660) for i in VP_Z3_TagN)
             
             # minute 12
             Z3_VPtagA_min12=sum((i>=660) and (i<720) for i in VP_Z3_TagA);Z3_VPtagB_min12=sum((i>=660) and (i<720) for i in VP_Z3_TagB);
             Z3_VPtagC_min12=sum((i>=660) and (i<720) for i in VP_Z3_TagC);Z3_VPtagD_min12=sum((i>=660) and (i<720) for i in VP_Z3_TagD);
             Z3_VPtagE_min12=sum((i>=660) and (i<720) for i in VP_Z3_TagE);Z3_VPtagF_min12=sum((i>=660) and (i<720) for i in VP_Z3_TagF);
             Z3_VPtagG_min12=sum((i>=660) and (i<720) for i in VP_Z3_TagG);Z3_VPtagH_min12=sum((i>=660) and (i<720) for i in VP_Z3_TagH);
             Z3_VPtagI_min12=sum((i>=660) and (i<720) for i in VP_Z3_TagI);Z3_VPtagJ_min12=sum((i>=660) and (i<720) for i in VP_Z3_TagJ);
             Z3_VPtagK_min12=sum((i>=660) and (i<720) for i in VP_Z3_TagK);Z3_VPtagL_min12=sum((i>=660) and (i<720) for i in VP_Z3_TagL);
             Z3_VPtagM_min12=sum((i>=660) and (i<720) for i in VP_Z3_TagM);Z3_VPtagN_min12=sum((i>=660) and (i<720) for i in VP_Z3_TagN)
             
             # minute 13
             Z3_VPtagA_min13=sum((i>=720) and (i<780) for i in VP_Z3_TagA);Z3_VPtagB_min13=sum((i>=720) and (i<780)for i in VP_Z3_TagB);
             Z3_VPtagC_min13=sum((i>=720) and (i<780) for i in VP_Z3_TagC);Z3_VPtagD_min13=sum((i>=720) and (i<780) for i in VP_Z3_TagD);
             Z3_VPtagE_min13=sum((i>=720) and (i<780) for i in VP_Z3_TagE);Z3_VPtagF_min13=sum((i>=720) and (i<780) for i in VP_Z3_TagF);
             Z3_VPtagG_min13=sum((i>=720) and (i<780) for i in VP_Z3_TagG);Z3_VPtagH_min13=sum((i>=720) and (i<780) for i in VP_Z3_TagH);
             Z3_VPtagI_min13=sum((i>=720) and (i<780) for i in VP_Z3_TagI);Z3_VPtagJ_min13=sum((i>=720) and (i<780) for i in VP_Z3_TagJ);
             Z3_VPtagK_min13=sum((i>=720) and (i<780) for i in VP_Z3_TagK);Z3_VPtagL_min13=sum((i>=720) and (i<780) for i in VP_Z3_TagL);
             Z3_VPtagM_min13=sum((i>=720) and (i<780) for i in VP_Z3_TagM);Z3_VPtagN_min13=sum((i>=720) and (i<780) for i in VP_Z3_TagN)
             
             # minute 14
             Z3_VPtagA_min14=sum((i>=780) and (i<840) for i in VP_Z3_TagA);Z3_VPtagB_min14=sum((i>=780) and (i<840) for i in VP_Z3_TagB);
             Z3_VPtagC_min14=sum((i>=780) and (i<840) for i in VP_Z3_TagC);Z3_VPtagD_min14=sum((i>=780) and (i<840) for i in VP_Z3_TagD);
             Z3_VPtagE_min14=sum((i>=780) and (i<840) for i in VP_Z3_TagE);Z3_VPtagF_min14=sum((i>=780) and (i<840) for i in VP_Z3_TagF);
             Z3_VPtagG_min14=sum((i>=780) and (i<840) for i in VP_Z3_TagG);Z3_VPtagH_min14=sum((i>=780) and (i<840) for i in VP_Z3_TagH);
             Z3_VPtagI_min14=sum((i>=780) and (i<840) for i in VP_Z3_TagI);Z3_VPtagJ_min14=sum((i>=780) and (i<840) for i in VP_Z3_TagJ);
             Z3_VPtagK_min14=sum((i>=780) and (i<840)for i in VP_Z3_TagK);Z3_VPtagL_min14=sum((i>=780) and (i<840) for i in VP_Z3_TagL);
             Z3_VPtagM_min14=sum((i>=780) and (i<840) for i in VP_Z3_TagM);Z3_VPtagN_min14=sum((i>=780) and (i<840) for i in VP_Z3_TagN)
             
             # minute 15
             Z3_VPtagA_min15=sum((i>=840) and (i<=900) for i in VP_Z3_TagA);Z3_VPtagB_min15=sum((i>=840) and (i<=900) for i in VP_Z3_TagB);
             Z3_VPtagC_min15=sum((i>=840) and (i<=900) for i in VP_Z3_TagC);Z3_VPtagD_min15=sum((i>=840) and (i<=900) for i in VP_Z3_TagD);
             Z3_VPtagE_min15=sum((i>=840) and (i<=900) for i in VP_Z3_TagE);Z3_VPtagF_min15=sum((i>=840) and (i<=900) for i in VP_Z3_TagF);
             Z3_VPtagG_min15=sum((i>=840) and (i<=900) for i in VP_Z3_TagG);Z3_VPtagH_min15=sum((i>=840) and (i<=900) for i in VP_Z3_TagH);
             Z3_VPtagI_min15=sum((i>=840) and (i<=900) for i in VP_Z3_TagI);Z3_VPtagJ_min15=sum((i>=840) and (i<=900) for i in VP_Z3_TagJ);
             Z3_VPtagK_min15=sum((i>=840) and (i<=900) for i in VP_Z3_TagK);Z3_VPtagL_min15=sum((i>=840) and (i<=900) for i in VP_Z3_TagL);
             Z3_VPtagM_min15=sum((i>=840) and (i<=900) for i in VP_Z3_TagM);Z3_VPtagN_min15=sum((i>=840) and (i<=900) for i in VP_Z3_TagN)
             
    ##############################################################################################################################
    # Zone 4

             Z4_VPtagA_mins=[];Z4_VPtagB_mins=[];Z4_VPtagC_mins=[];Z4_VPtagD_mins=[];Z4_VPtagE_mins=[];Z4_VPtagF_mins=[];Z4_VPtagG_mins=[];
             Z4_VPtagH_mins=[];Z4_VPtagI_mins=[];Z4_VPtagJ_mins=[];Z4_VPtagK_mins=[];Z4_VPtagL_mins=[];Z4_VPtagM_mins=[];Z4_VPtagN_mins=[]
             # minute 1              
             Z4_VPtagA_min1=sum(i <60 for i in VP_Z4_TagA);Z4_VPtagB_min1=sum(i <60 for i in VP_Z4_TagB);Z4_VPtagC_min1=sum(i <60 for i in VP_Z4_TagC);
             Z4_VPtagD_min1=sum(i <60 for i in VP_Z4_TagD);Z4_VPtagE_min1=sum(i <60 for i in VP_Z4_TagE);Z4_VPtagF_min1=sum(i <60 for i in VP_Z4_TagF);
             Z4_VPtagG_min1=sum(i <60 for i in VP_Z4_TagG);Z4_VPtagH_min1=sum(i <60 for i in VP_Z4_TagH);Z4_VPtagI_min1=sum(i <60 for i in VP_Z4_TagI);
             Z4_VPtagJ_min1=sum(i <60 for i in VP_Z4_TagJ);Z4_VPtagK_min1=sum(i <60 for i in VP_Z4_TagK);Z4_VPtagL_min1=sum(i <60 for i in VP_Z4_TagL);
             Z4_VPtagM_min1=sum(i <60 for i in VP_Z4_TagM);Z4_VPtagN_min1=sum(i <60 for i in VP_Z4_TagN)

             # minute 2
             Z4_VPtagA_min2=sum((i >=60) and (i <120) for i in VP_Z4_TagA);Z4_VPtagB_min2=sum((i >=60) and (i <120) for i in VP_Z4_TagB);
             Z4_VPtagC_min2=sum((i >=60) and (i <120) for i in VP_Z4_TagC);Z4_VPtagD_min2=sum((i >=60) and (i <120) for i in VP_Z4_TagD);
             Z4_VPtagE_min2=sum((i >=60) and (i <120) for i in VP_Z4_TagE);Z4_VPtagF_min2=sum((i >=60) and (i <120) for i in VP_Z4_TagF);
             Z4_VPtagG_min2=sum((i >=60) and (i <120) for i in VP_Z4_TagG);Z4_VPtagH_min2=sum((i >=60) and (i <120) for i in VP_Z4_TagH);
             Z4_VPtagI_min2=sum((i >=60) and (i <120) for i in VP_Z4_TagI);Z4_VPtagJ_min2=sum((i >=60) and (i <120) for i in VP_Z4_TagJ);
             Z4_VPtagK_min2=sum((i >=60) and (i <120) for i in VP_Z4_TagK);Z4_VPtagL_min2=sum((i >=60) and (i <120) for i in VP_Z4_TagL);
             Z4_VPtagM_min2=sum((i >=60) and (i <120) for i in VP_Z4_TagM);Z4_VPtagN_min2=sum((i >=60) and (i <120) for i in VP_Z4_TagN)

             # minute 3
             Z4_VPtagA_min3=sum((i>=120) and (i<180) for i in VP_Z4_TagA);Z4_VPtagB_min3=sum((i>=120) and (i<180) for i in VP_Z4_TagB);
             Z4_VPtagC_min3=sum((i>=120) and (i<180) for i in VP_Z4_TagC);Z4_VPtagD_min3=sum((i>=120) and (i<180) for i in VP_Z4_TagD);
             Z4_VPtagE_min3=sum((i>=120) and (i<180) for i in VP_Z4_TagE);Z4_VPtagF_min3=sum((i>=120) and (i<180) for i in VP_Z4_TagF);
             Z4_VPtagG_min3=sum((i>=120) and (i<180) for i in VP_Z4_TagG);Z4_VPtagH_min3=sum((i>=120) and (i<180) for i in VP_Z4_TagH);
             Z4_VPtagI_min3=sum((i>=120) and (i<180) for i in VP_Z4_TagI);Z4_VPtagJ_min3=sum((i>=120) and (i<180) for i in VP_Z4_TagJ);
             Z4_VPtagK_min3=sum((i>=120) and (i<180) for i in VP_Z4_TagK);Z4_VPtagL_min3=sum((i>=120) and (i<180) for i in VP_Z4_TagL);
             Z4_VPtagM_min3=sum((i>=120) and (i<180) for i in VP_Z4_TagM);Z4_VPtagN_min3=sum((i>=120) and (i<180) for i in VP_Z4_TagN)
             
             # minute 4
             Z4_VPtagA_min4=sum((i>=180) and (i<240) for i in VP_Z4_TagA);Z4_VPtagB_min4=sum((i>=180) and (i<240) for i in VP_Z4_TagB);
             Z4_VPtagC_min4=sum((i>=180) and (i<240) for i in VP_Z4_TagC);Z4_VPtagD_min4=sum((i>=180) and (i<240) for i in VP_Z4_TagD);
             Z4_VPtagE_min4=sum((i>=180) and (i<240) for i in VP_Z4_TagE);Z4_VPtagF_min4=sum((i>=180) and (i<240) for i in VP_Z4_TagF);
             Z4_VPtagG_min4=sum((i>=180) and (i<240) for i in VP_Z4_TagG);Z4_VPtagH_min4=sum((i>=180) and (i<240) for i in VP_Z4_TagH);
             Z4_VPtagI_min4=sum((i>=180) and (i<240) for i in VP_Z4_TagI);Z4_VPtagJ_min4=sum((i>=180) and (i<240) for i in VP_Z4_TagJ);
             Z4_VPtagK_min4=sum((i>=180) and (i<240) for i in VP_Z4_TagK);Z4_VPtagL_min4=sum((i>=180) and (i<240) for i in VP_Z4_TagL);
             Z4_VPtagM_min4=sum((i>=180) and (i<240) for i in VP_Z4_TagM);Z4_VPtagN_min4=sum((i>=180) and (i<240) for i in VP_Z4_TagN)
             
             # minute 5
             Z4_VPtagA_min5=sum((i>=240) and (i<300) for i in VP_Z4_TagA);Z4_VPtagB_min5=sum((i>=240) and (i<300) for i in VP_Z4_TagB);
             Z4_VPtagC_min5=sum((i>=240) and (i<300) for i in VP_Z4_TagC);Z4_VPtagD_min5=sum((i>=240) and (i<300) for i in VP_Z4_TagD);
             Z4_VPtagE_min5=sum((i>=240) and (i<300) for i in VP_Z4_TagE);Z4_VPtagF_min5=sum((i>=240) and (i<300) for i in VP_Z4_TagF);
             Z4_VPtagG_min5=sum((i>=240) and (i<300) for i in VP_Z4_TagG);Z4_VPtagH_min5=sum((i>=240) and (i<300) for i in VP_Z4_TagH);
             Z4_VPtagI_min5=sum((i>=240) and (i<300) for i in VP_Z4_TagI);Z4_VPtagJ_min5=sum((i>=240) and (i<300) for i in VP_Z4_TagJ);
             Z4_VPtagK_min5=sum((i>=240) and (i<300) for i in VP_Z4_TagK);Z4_VPtagL_min5=sum((i>=240) and (i<300) for i in VP_Z4_TagL);
             Z4_VPtagM_min5=sum((i>=240) and (i<300) for i in VP_Z4_TagM);Z4_VPtagN_min5=sum((i>=240) and (i<300) for i in VP_Z4_TagN)
             
             # minute 6
             Z4_VPtagA_min6=sum((i>=300) and (i<360) for i in VP_Z4_TagA);Z4_VPtagB_min6=sum((i>=300) and (i<360) for i in VP_Z4_TagB);
             Z4_VPtagC_min6=sum((i>=300) and (i<360) for i in VP_Z4_TagC);Z4_VPtagD_min6=sum((i>=300) and (i<360) for i in VP_Z4_TagD);
             Z4_VPtagE_min6=sum((i>=300) and (i<360) for i in VP_Z4_TagE);Z4_VPtagF_min6=sum((i>=300) and (i<360) for i in VP_Z4_TagF);
             Z4_VPtagG_min6=sum((i>=300) and (i<360) for i in VP_Z4_TagG);Z4_VPtagH_min6=sum((i>=300) and (i<360) for i in VP_Z4_TagH);
             Z4_VPtagI_min6=sum((i>=300) and (i<360) for i in VP_Z4_TagI);Z4_VPtagJ_min6=sum((i>=300) and (i<360)for i in VP_Z4_TagJ);
             Z4_VPtagK_min6=sum((i>=300) and (i<360) for i in VP_Z4_TagK);Z4_VPtagL_min6=sum((i>=300) and (i<360) for i in VP_Z4_TagL);
             Z4_VPtagM_min6=sum((i>=300) and (i<360) for i in VP_Z4_TagM);Z4_VPtagN_min6=sum((i>=300) and (i<360) for i in VP_Z4_TagN)
             
             # minute 7
             Z4_VPtagA_min7=sum((i>=360) and (i<420) for i in VP_Z4_TagA);Z4_VPtagB_min7=sum((i>=360) and (i<420) for i in VP_Z4_TagB);
             Z4_VPtagC_min7=sum((i>=360) and (i<420) for i in VP_Z4_TagC);Z4_VPtagD_min7=sum((i>=360) and (i<420) for i in VP_Z4_TagD);
             Z4_VPtagE_min7=sum((i>=360) and (i<420) for i in VP_Z4_TagE);Z4_VPtagF_min7=sum((i>=360) and (i<420) for i in VP_Z4_TagF);
             Z4_VPtagG_min7=sum((i>=360) and (i<420) for i in VP_Z4_TagG);Z4_VPtagH_min7=sum((i>=360) and (i<420) for i in VP_Z4_TagH);
             Z4_VPtagI_min7=sum((i>=360) and (i<420) for i in VP_Z4_TagI);Z4_VPtagJ_min7=sum((i>=360) and (i<420)for i in VP_Z4_TagJ);
             Z4_VPtagK_min7=sum((i>=360) and (i<420) for i in VP_Z4_TagK);Z4_VPtagL_min7=sum((i>=360) and (i<420) for i in VP_Z4_TagL);
             Z4_VPtagM_min7=sum((i>=360) and (i<420) for i in VP_Z4_TagM);Z4_VPtagN_min7=sum((i>=360) and (i<420) for i in VP_Z4_TagN)
             
             # minute 8
             Z4_VPtagA_min8=sum((i>=420) and (i<480) for i in VP_Z4_TagA);Z4_VPtagB_min8=sum((i>=420) and (i<480) for i in VP_Z4_TagB);
             Z4_VPtagC_min8=sum((i>=420) and (i<480) for i in VP_Z4_TagC);Z4_VPtagD_min8=sum((i>=420) and (i<480) for i in VP_Z4_TagD);
             Z4_VPtagE_min8=sum((i>=420) and (i<480) for i in VP_Z4_TagE);Z4_VPtagF_min8=sum((i>=420) and (i<480) for i in VP_Z4_TagF);
             Z4_VPtagG_min8=sum((i>=420) and (i<480) for i in VP_Z4_TagG);Z4_VPtagH_min8=sum((i>=420) and (i<480)for i in VP_Z4_TagH);
             Z4_VPtagI_min8=sum((i>=420) and (i<480) for i in VP_Z4_TagI);Z4_VPtagJ_min8=sum((i>=420) and (i<480)for i in VP_Z4_TagJ);
             Z4_VPtagK_min8=sum((i>=420) and (i<480) for i in VP_Z4_TagK);Z4_VPtagL_min8=sum((i>=420) and (i<480) for i in VP_Z4_TagL);
             Z4_VPtagM_min8=sum((i>=420) and (i<480) for i in VP_Z4_TagM);Z4_VPtagN_min8=sum((i>=420) and (i<480) for i in VP_Z4_TagN)
             
             # minute 9
             Z4_VPtagA_min9=sum((i>=480) and (i<540) for i in VP_Z4_TagA);Z4_VPtagB_min9=sum((i>=480) and (i<540) for i in VP_Z4_TagB);
             Z4_VPtagC_min9=sum((i>=480) and (i<540) for i in VP_Z4_TagC);Z4_VPtagD_min9=sum((i>=480) and (i<540) for i in VP_Z4_TagD);
             Z4_VPtagE_min9=sum((i>=480) and (i<540) for i in VP_Z4_TagE);Z4_VPtagF_min9=sum((i>=480) and (i<540) for i in VP_Z4_TagF);
             Z4_VPtagG_min9=sum((i>=480) and (i<540) for i in VP_Z4_TagG);Z4_VPtagH_min9=sum((i>=480) and (i<540) for i in VP_Z4_TagH);
             Z4_VPtagI_min9=sum((i>=480) and (i<540) for i in VP_Z4_TagI);Z4_VPtagJ_min9=sum((i>=480) and (i<540) for i in VP_Z4_TagJ);
             Z4_VPtagK_min9=sum((i>=480) and (i<540) for i in VP_Z4_TagK);Z4_VPtagL_min9=sum((i>=480) and (i<540) for i in VP_Z4_TagL);
             Z4_VPtagM_min9=sum((i>=480) and (i<540) for i in VP_Z4_TagM);Z4_VPtagN_min9=sum((i>=480) and (i<540) for i in VP_Z4_TagN)        

             # minute 10
             Z4_VPtagA_min10=sum((i>=540) and (i<600) for i in VP_Z4_TagA);Z4_VPtagB_min10=sum((i>=540) and (i<600) for i in VP_Z4_TagB);
             Z4_VPtagC_min10=sum((i>=540) and (i<600) for i in VP_Z4_TagC);Z4_VPtagD_min10=sum((i>=540) and (i<600) for i in VP_Z4_TagD);
             Z4_VPtagE_min10=sum((i>=540) and (i<600) for i in VP_Z4_TagE);Z4_VPtagF_min10=sum((i>=540) and (i<600) for i in VP_Z4_TagF);
             Z4_VPtagG_min10=sum((i>=540) and (i<600) for i in VP_Z4_TagG);Z4_VPtagH_min10=sum((i>=540) and (i<600) for i in VP_Z4_TagH);
             Z4_VPtagI_min10=sum((i>=540) and (i<600) for i in VP_Z4_TagI);Z4_VPtagJ_min10=sum((i>=540) and (i<600) for i in VP_Z4_TagJ);
             Z4_VPtagK_min10=sum((i>=540) and (i<600) for i in VP_Z4_TagK);Z4_VPtagL_min10=sum((i>=540) and (i<600) for i in VP_Z4_TagL);
             Z4_VPtagM_min10=sum((i>=540) and (i<600) for i in VP_Z4_TagM);Z4_VPtagN_min10=sum((i>=540) and (i<600) for i in VP_Z4_TagN)
             
             # minute 11
             Z4_VPtagA_min11=sum((i>=600) and (i<660) for i in VP_Z4_TagA);Z4_VPtagB_min11=sum((i>=600) and (i<660) for i in VP_Z4_TagB);
             Z4_VPtagC_min11=sum((i>=600) and (i<660) for i in VP_Z4_TagC);Z4_VPtagD_min11=sum((i>=600) and (i<660) for i in VP_Z4_TagD);
             Z4_VPtagE_min11=sum((i>=600) and (i<660) for i in VP_Z4_TagE);Z4_VPtagF_min11=sum((i>=600) and (i<660) for i in VP_Z4_TagF);
             Z4_VPtagG_min11=sum((i>=600) and (i<660) for i in VP_Z4_TagG);Z4_VPtagH_min11=sum((i>=600) and (i<660) for i in VP_Z4_TagH);
             Z4_VPtagI_min11=sum((i>=600) and (i<660) for i in VP_Z4_TagI);Z4_VPtagJ_min11=sum((i>=600) and (i<660) for i in VP_Z4_TagJ);
             Z4_VPtagK_min11=sum((i>=600) and (i<660) for i in VP_Z4_TagK);Z4_VPtagL_min11=sum((i>=600) and (i<660) for i in VP_Z4_TagL);
             Z4_VPtagM_min11=sum((i>=600) and (i<660) for i in VP_Z4_TagM);Z4_VPtagN_min11=sum((i>=600) and (i<660) for i in VP_Z4_TagN)
             
             # minute 12
             Z4_VPtagA_min12=sum((i>=660) and (i<720) for i in VP_Z4_TagA);Z4_VPtagB_min12=sum((i>=660) and (i<720) for i in VP_Z4_TagB);
             Z4_VPtagC_min12=sum((i>=660) and (i<720) for i in VP_Z4_TagC);Z4_VPtagD_min12=sum((i>=660) and (i<720) for i in VP_Z4_TagD);
             Z4_VPtagE_min12=sum((i>=660) and (i<720) for i in VP_Z4_TagE);Z4_VPtagF_min12=sum((i>=660) and (i<720) for i in VP_Z4_TagF);
             Z4_VPtagG_min12=sum((i>=660) and (i<720) for i in VP_Z4_TagG);Z4_VPtagH_min12=sum((i>=660) and (i<720) for i in VP_Z4_TagH);
             Z4_VPtagI_min12=sum((i>=660) and (i<720) for i in VP_Z4_TagI);Z4_VPtagJ_min12=sum((i>=660) and (i<720) for i in VP_Z4_TagJ);
             Z4_VPtagK_min12=sum((i>=660) and (i<720) for i in VP_Z4_TagK);Z4_VPtagL_min12=sum((i>=660) and (i<720) for i in VP_Z4_TagL);
             Z4_VPtagM_min12=sum((i>=660) and (i<720) for i in VP_Z4_TagM);Z4_VPtagN_min12=sum((i>=660) and (i<720) for i in VP_Z4_TagN)
             
             # minute 13
             Z4_VPtagA_min13=sum((i>=720) and (i<780) for i in VP_Z4_TagA);Z4_VPtagB_min13=sum((i>=720) and (i<780)for i in VP_Z4_TagB);
             Z4_VPtagC_min13=sum((i>=720) and (i<780) for i in VP_Z4_TagC);Z4_VPtagD_min13=sum((i>=720) and (i<780) for i in VP_Z4_TagD);
             Z4_VPtagE_min13=sum((i>=720) and (i<780) for i in VP_Z4_TagE);Z4_VPtagF_min13=sum((i>=720) and (i<780) for i in VP_Z4_TagF);
             Z4_VPtagG_min13=sum((i>=720) and (i<780) for i in VP_Z4_TagG);Z4_VPtagH_min13=sum((i>=720) and (i<780) for i in VP_Z4_TagH);
             Z4_VPtagI_min13=sum((i>=720) and (i<780) for i in VP_Z4_TagI);Z4_VPtagJ_min13=sum((i>=720) and (i<780) for i in VP_Z4_TagJ);
             Z4_VPtagK_min13=sum((i>=720) and (i<780) for i in VP_Z4_TagK);Z4_VPtagL_min13=sum((i>=720) and (i<780) for i in VP_Z4_TagL);
             Z4_VPtagM_min13=sum((i>=720) and (i<780) for i in VP_Z4_TagM);Z4_VPtagN_min13=sum((i>=720) and (i<780) for i in VP_Z4_TagN)
             
             # minute 14
             Z4_VPtagA_min14=sum((i>=780) and (i<840) for i in VP_Z4_TagA);Z4_VPtagB_min14=sum((i>=780) and (i<840) for i in VP_Z4_TagB);
             Z4_VPtagC_min14=sum((i>=780) and (i<840) for i in VP_Z4_TagC);Z4_VPtagD_min14=sum((i>=780) and (i<840) for i in VP_Z4_TagD);
             Z4_VPtagE_min14=sum((i>=780) and (i<840) for i in VP_Z4_TagE);Z4_VPtagF_min14=sum((i>=780) and (i<840) for i in VP_Z4_TagF);
             Z4_VPtagG_min14=sum((i>=780) and (i<840) for i in VP_Z4_TagG);Z4_VPtagH_min14=sum((i>=780) and (i<840) for i in VP_Z4_TagH);
             Z4_VPtagI_min14=sum((i>=780) and (i<840) for i in VP_Z4_TagI);Z4_VPtagJ_min14=sum((i>=780) and (i<840) for i in VP_Z4_TagJ);
             Z4_VPtagK_min14=sum((i>=780) and (i<840)for i in VP_Z4_TagK);Z4_VPtagL_min14=sum((i>=780) and (i<840) for i in VP_Z4_TagL);
             Z4_VPtagM_min14=sum((i>=780) and (i<840) for i in VP_Z4_TagM);Z4_VPtagN_min14=sum((i>=780) and (i<840) for i in VP_Z4_TagN)
             
             # minute 15
             Z4_VPtagA_min15=sum((i>=840) and (i<=900) for i in VP_Z4_TagA);Z4_VPtagB_min15=sum((i>=840) and (i<=900) for i in VP_Z4_TagB);
             Z4_VPtagC_min15=sum((i>=840) and (i<=900) for i in VP_Z4_TagC);Z4_VPtagD_min15=sum((i>=840) and (i<=900) for i in VP_Z4_TagD);
             Z4_VPtagE_min15=sum((i>=840) and (i<=900) for i in VP_Z4_TagE);Z4_VPtagF_min15=sum((i>=840) and (i<=900) for i in VP_Z4_TagF);
             Z4_VPtagG_min15=sum((i>=840) and (i<=900) for i in VP_Z4_TagG);Z4_VPtagH_min15=sum((i>=840) and (i<=900) for i in VP_Z4_TagH);
             Z4_VPtagI_min15=sum((i>=840) and (i<=900) for i in VP_Z4_TagI);Z4_VPtagJ_min15=sum((i>=840) and (i<=900) for i in VP_Z4_TagJ);
             Z4_VPtagK_min15=sum((i>=840) and (i<=900) for i in VP_Z4_TagK);Z4_VPtagL_min15=sum((i>=840) and (i<=900) for i in VP_Z4_TagL);
             Z4_VPtagM_min15=sum((i>=840) and (i<=900) for i in VP_Z4_TagM);Z4_VPtagN_min15=sum((i>=840) and (i<=900) for i in VP_Z4_TagN)
             
    ##############################################################################################################################
    # Zone 5

             Z5_VPtagA_mins=[];Z5_VPtagB_mins=[];Z5_VPtagC_mins=[];Z5_VPtagD_mins=[];Z5_VPtagE_mins=[];Z5_VPtagF_mins=[];Z5_VPtagG_mins=[];
             Z5_VPtagH_mins=[];Z5_VPtagI_mins=[];Z5_VPtagJ_mins=[];Z5_VPtagK_mins=[];Z5_VPtagL_mins=[];Z5_VPtagM_mins=[];Z5_VPtagN_mins=[]
             # minute 1              
             Z5_VPtagA_min1=sum(i <60 for i in VP_Z5_TagA);Z5_VPtagB_min1=sum(i <60 for i in VP_Z5_TagB);Z5_VPtagC_min1=sum(i <60 for i in VP_Z5_TagC);
             Z5_VPtagD_min1=sum(i <60 for i in VP_Z5_TagD);Z5_VPtagE_min1=sum(i <60 for i in VP_Z5_TagE);Z5_VPtagF_min1=sum(i <60 for i in VP_Z5_TagF);
             Z5_VPtagG_min1=sum(i <60 for i in VP_Z5_TagG);Z5_VPtagH_min1=sum(i <60 for i in VP_Z5_TagH);Z5_VPtagI_min1=sum(i <60 for i in VP_Z5_TagI);
             Z5_VPtagJ_min1=sum(i <60 for i in VP_Z5_TagJ);Z5_VPtagK_min1=sum(i <60 for i in VP_Z5_TagK);Z5_VPtagL_min1=sum(i <60 for i in VP_Z5_TagL);
             Z5_VPtagM_min1=sum(i <60 for i in VP_Z5_TagM);Z5_VPtagN_min1=sum(i <60 for i in VP_Z5_TagN)
       
             # minute 2
             Z5_VPtagA_min2=sum((i >=60) and (i <120) for i in VP_Z5_TagA);Z5_VPtagB_min2=sum((i >=60) and (i <120) for i in VP_Z5_TagB);
             Z5_VPtagC_min2=sum((i >=60) and (i <120) for i in VP_Z5_TagC);Z5_VPtagD_min2=sum((i >=60) and (i <120) for i in VP_Z5_TagD);
             Z5_VPtagE_min2=sum((i >=60) and (i <120) for i in VP_Z5_TagE);Z5_VPtagF_min2=sum((i >=60) and (i <120) for i in VP_Z5_TagF);
             Z5_VPtagG_min2=sum((i >=60) and (i <120) for i in VP_Z5_TagG);Z5_VPtagH_min2=sum((i >=60) and (i <120) for i in VP_Z5_TagH);
             Z5_VPtagI_min2=sum((i >=60) and (i <120) for i in VP_Z5_TagI);Z5_VPtagJ_min2=sum((i >=60) and (i <120) for i in VP_Z5_TagJ);
             Z5_VPtagK_min2=sum((i >=60) and (i <120) for i in VP_Z5_TagK);Z5_VPtagL_min2=sum((i >=60) and (i <120) for i in VP_Z5_TagL);
             Z5_VPtagM_min2=sum((i >=60) and (i <120) for i in VP_Z5_TagM);Z5_VPtagN_min2=sum((i >=60) and (i <120) for i in VP_Z5_TagN)
                
             # minute 3
             Z5_VPtagA_min3=sum((i>=120) and (i<180) for i in VP_Z5_TagA);Z5_VPtagB_min3=sum((i>=120) and (i<180) for i in VP_Z5_TagB);
             Z5_VPtagC_min3=sum((i>=120) and (i<180) for i in VP_Z5_TagC);Z5_VPtagD_min3=sum((i>=120) and (i<180) for i in VP_Z5_TagD);
             Z5_VPtagE_min3=sum((i>=120) and (i<180) for i in VP_Z5_TagE);Z5_VPtagF_min3=sum((i>=120) and (i<180) for i in VP_Z5_TagF);
             Z5_VPtagG_min3=sum((i>=120) and (i<180) for i in VP_Z5_TagG);Z5_VPtagH_min3=sum((i>=120) and (i<180) for i in VP_Z5_TagH);
             Z5_VPtagI_min3=sum((i>=120) and (i<180) for i in VP_Z5_TagI);Z5_VPtagJ_min3=sum((i>=120) and (i<180) for i in VP_Z5_TagJ);
             Z5_VPtagK_min3=sum((i>=120) and (i<180) for i in VP_Z5_TagK);Z5_VPtagL_min3=sum((i>=120) and (i<180) for i in VP_Z5_TagL);
             Z5_VPtagM_min3=sum((i>=120) and (i<180) for i in VP_Z5_TagM);Z5_VPtagN_min3=sum((i>=120) and (i<180) for i in VP_Z5_TagN)
             
             # minute 4
             Z5_VPtagA_min4=sum((i>=180) and (i<240) for i in VP_Z5_TagA);Z5_VPtagB_min4=sum((i>=180) and (i<240) for i in VP_Z5_TagB);
             Z5_VPtagC_min4=sum((i>=180) and (i<240) for i in VP_Z5_TagC);Z5_VPtagD_min4=sum((i>=180) and (i<240) for i in VP_Z5_TagD);
             Z5_VPtagE_min4=sum((i>=180) and (i<240) for i in VP_Z5_TagE);Z5_VPtagF_min4=sum((i>=180) and (i<240) for i in VP_Z5_TagF);
             Z5_VPtagG_min4=sum((i>=180) and (i<240) for i in VP_Z5_TagG);Z5_VPtagH_min4=sum((i>=180) and (i<240) for i in VP_Z5_TagH);
             Z5_VPtagI_min4=sum((i>=180) and (i<240) for i in VP_Z5_TagI);Z5_VPtagJ_min4=sum((i>=180) and (i<240) for i in VP_Z5_TagJ);
             Z5_VPtagK_min4=sum((i>=180) and (i<240) for i in VP_Z5_TagK);Z5_VPtagL_min4=sum((i>=180) and (i<240) for i in VP_Z5_TagL);
             Z5_VPtagM_min4=sum((i>=180) and (i<240) for i in VP_Z5_TagM);Z5_VPtagN_min4=sum((i>=180) and (i<240) for i in VP_Z5_TagN)
             
             # minute 5
             Z5_VPtagA_min5=sum((i>=240) and (i<300) for i in VP_Z5_TagA);Z5_VPtagB_min5=sum((i>=240) and (i<300) for i in VP_Z5_TagB);
             Z5_VPtagC_min5=sum((i>=240) and (i<300) for i in VP_Z5_TagC);Z5_VPtagD_min5=sum((i>=240) and (i<300) for i in VP_Z5_TagD);
             Z5_VPtagE_min5=sum((i>=240) and (i<300) for i in VP_Z5_TagE);Z5_VPtagF_min5=sum((i>=240) and (i<300) for i in VP_Z5_TagF);
             Z5_VPtagG_min5=sum((i>=240) and (i<300) for i in VP_Z5_TagG);Z5_VPtagH_min5=sum((i>=240) and (i<300) for i in VP_Z5_TagH);
             Z5_VPtagI_min5=sum((i>=240) and (i<300) for i in VP_Z5_TagI);Z5_VPtagJ_min5=sum((i>=240) and (i<300) for i in VP_Z5_TagJ);
             Z5_VPtagK_min5=sum((i>=240) and (i<300) for i in VP_Z5_TagK);Z5_VPtagL_min5=sum((i>=240) and (i<300) for i in VP_Z5_TagL);
             Z5_VPtagM_min5=sum((i>=240) and (i<300) for i in VP_Z5_TagM);Z5_VPtagN_min5=sum((i>=240) and (i<300) for i in VP_Z5_TagN)
             
             # minute 6
             Z5_VPtagA_min6=sum((i>=300) and (i<360) for i in VP_Z5_TagA);Z5_VPtagB_min6=sum((i>=300) and (i<360) for i in VP_Z5_TagB);
             Z5_VPtagC_min6=sum((i>=300) and (i<360) for i in VP_Z5_TagC);Z5_VPtagD_min6=sum((i>=300) and (i<360) for i in VP_Z5_TagD);
             Z5_VPtagE_min6=sum((i>=300) and (i<360) for i in VP_Z5_TagE);Z5_VPtagF_min6=sum((i>=300) and (i<360) for i in VP_Z5_TagF);
             Z5_VPtagG_min6=sum((i>=300) and (i<360) for i in VP_Z5_TagG);Z5_VPtagH_min6=sum((i>=300) and (i<360) for i in VP_Z5_TagH);
             Z5_VPtagI_min6=sum((i>=300) and (i<360) for i in VP_Z5_TagI);Z5_VPtagJ_min6=sum((i>=300) and (i<360)for i in VP_Z5_TagJ);
             Z5_VPtagK_min6=sum((i>=300) and (i<360) for i in VP_Z5_TagK);Z5_VPtagL_min6=sum((i>=300) and (i<360) for i in VP_Z5_TagL);
             Z5_VPtagM_min6=sum((i>=300) and (i<360) for i in VP_Z5_TagM);Z5_VPtagN_min6=sum((i>=300) and (i<360) for i in VP_Z5_TagN)
             
             # minute 7
             Z5_VPtagA_min7=sum((i>=360) and (i<420) for i in VP_Z5_TagA);Z5_VPtagB_min7=sum((i>=360) and (i<420) for i in VP_Z5_TagB);
             Z5_VPtagC_min7=sum((i>=360) and (i<420) for i in VP_Z5_TagC);Z5_VPtagD_min7=sum((i>=360) and (i<420) for i in VP_Z5_TagD);
             Z5_VPtagE_min7=sum((i>=360) and (i<420) for i in VP_Z5_TagE);Z5_VPtagF_min7=sum((i>=360) and (i<420) for i in VP_Z5_TagF);
             Z5_VPtagG_min7=sum((i>=360) and (i<420) for i in VP_Z5_TagG);Z5_VPtagH_min7=sum((i>=360) and (i<420) for i in VP_Z5_TagH);
             Z5_VPtagI_min7=sum((i>=360) and (i<420) for i in VP_Z5_TagI);Z5_VPtagJ_min7=sum((i>=360) and (i<420)for i in VP_Z5_TagJ);
             Z5_VPtagK_min7=sum((i>=360) and (i<420) for i in VP_Z5_TagK);Z5_VPtagL_min7=sum((i>=360) and (i<420) for i in VP_Z5_TagL);
             Z5_VPtagM_min7=sum((i>=360) and (i<420) for i in VP_Z5_TagM);Z5_VPtagN_min7=sum((i>=360) and (i<420) for i in VP_Z5_TagN)
             
             # minute 8
             Z5_VPtagA_min8=sum((i>=420) and (i<480) for i in VP_Z5_TagA);Z5_VPtagB_min8=sum((i>=420) and (i<480) for i in VP_Z5_TagB);
             Z5_VPtagC_min8=sum((i>=420) and (i<480) for i in VP_Z5_TagC);Z5_VPtagD_min8=sum((i>=420) and (i<480) for i in VP_Z5_TagD);
             Z5_VPtagE_min8=sum((i>=420) and (i<480) for i in VP_Z5_TagE);Z5_VPtagF_min8=sum((i>=420) and (i<480) for i in VP_Z5_TagF);
             Z5_VPtagG_min8=sum((i>=420) and (i<480) for i in VP_Z5_TagG);Z5_VPtagH_min8=sum((i>=420) and (i<480)for i in VP_Z5_TagH);
             Z5_VPtagI_min8=sum((i>=420) and (i<480) for i in VP_Z5_TagI);Z5_VPtagJ_min8=sum((i>=420) and (i<480)for i in VP_Z5_TagJ);
             Z5_VPtagK_min8=sum((i>=420) and (i<480) for i in VP_Z5_TagK);Z5_VPtagL_min8=sum((i>=420) and (i<480) for i in VP_Z5_TagL);
             Z5_VPtagM_min8=sum((i>=420) and (i<480) for i in VP_Z5_TagM);Z5_VPtagN_min8=sum((i>=420) and (i<480) for i in VP_Z5_TagN)
             
             # minute 9
             Z5_VPtagA_min9=sum((i>=480) and (i<540) for i in VP_Z5_TagA);Z5_VPtagB_min9=sum((i>=480) and (i<540) for i in VP_Z5_TagB);
             Z5_VPtagC_min9=sum((i>=480) and (i<540) for i in VP_Z5_TagC);Z5_VPtagD_min9=sum((i>=480) and (i<540) for i in VP_Z5_TagD);
             Z5_VPtagE_min9=sum((i>=480) and (i<540) for i in VP_Z5_TagE);Z5_VPtagF_min9=sum((i>=480) and (i<540) for i in VP_Z5_TagF);
             Z5_VPtagG_min9=sum((i>=480) and (i<540) for i in VP_Z5_TagG);Z5_VPtagH_min9=sum((i>=480) and (i<540) for i in VP_Z5_TagH);
             Z5_VPtagI_min9=sum((i>=480) and (i<540) for i in VP_Z5_TagI);Z5_VPtagJ_min9=sum((i>=480) and (i<540) for i in VP_Z5_TagJ);
             Z5_VPtagK_min9=sum((i>=480) and (i<540) for i in VP_Z5_TagK);Z5_VPtagL_min9=sum((i>=480) and (i<540) for i in VP_Z5_TagL);
             Z5_VPtagM_min9=sum((i>=480) and (i<540) for i in VP_Z5_TagM);Z5_VPtagN_min9=sum((i>=480) and (i<540) for i in VP_Z5_TagN)        

             # minute 10
             Z5_VPtagA_min10=sum((i>=540) and (i<600) for i in VP_Z5_TagA);Z5_VPtagB_min10=sum((i>=540) and (i<600) for i in VP_Z5_TagB);
             Z5_VPtagC_min10=sum((i>=540) and (i<600) for i in VP_Z5_TagC);Z5_VPtagD_min10=sum((i>=540) and (i<600) for i in VP_Z5_TagD);
             Z5_VPtagE_min10=sum((i>=540) and (i<600) for i in VP_Z5_TagE);Z5_VPtagF_min10=sum((i>=540) and (i<600) for i in VP_Z5_TagF);
             Z5_VPtagG_min10=sum((i>=540) and (i<600) for i in VP_Z5_TagG);Z5_VPtagH_min10=sum((i>=540) and (i<600) for i in VP_Z5_TagH);
             Z5_VPtagI_min10=sum((i>=540) and (i<600) for i in VP_Z5_TagI);Z5_VPtagJ_min10=sum((i>=540) and (i<600) for i in VP_Z5_TagJ);
             Z5_VPtagK_min10=sum((i>=540) and (i<600) for i in VP_Z5_TagK);Z5_VPtagL_min10=sum((i>=540) and (i<600) for i in VP_Z5_TagL);
             Z5_VPtagM_min10=sum((i>=540) and (i<600) for i in VP_Z5_TagM);Z5_VPtagN_min10=sum((i>=540) and (i<600) for i in VP_Z5_TagN)
             
             # minute 11
             Z5_VPtagA_min11=sum((i>=600) and (i<660) for i in VP_Z5_TagA);Z5_VPtagB_min11=sum((i>=600) and (i<660) for i in VP_Z5_TagB);
             Z5_VPtagC_min11=sum((i>=600) and (i<660) for i in VP_Z5_TagC);Z5_VPtagD_min11=sum((i>=600) and (i<660) for i in VP_Z5_TagD);
             Z5_VPtagE_min11=sum((i>=600) and (i<660) for i in VP_Z5_TagE);Z5_VPtagF_min11=sum((i>=600) and (i<660) for i in VP_Z5_TagF);
             Z5_VPtagG_min11=sum((i>=600) and (i<660) for i in VP_Z5_TagG);Z5_VPtagH_min11=sum((i>=600) and (i<660) for i in VP_Z5_TagH);
             Z5_VPtagI_min11=sum((i>=600) and (i<660) for i in VP_Z5_TagI);Z5_VPtagJ_min11=sum((i>=600) and (i<660) for i in VP_Z5_TagJ);
             Z5_VPtagK_min11=sum((i>=600) and (i<660) for i in VP_Z5_TagK);Z5_VPtagL_min11=sum((i>=600) and (i<660) for i in VP_Z5_TagL);
             Z5_VPtagM_min11=sum((i>=600) and (i<660) for i in VP_Z5_TagM);Z5_VPtagN_min11=sum((i>=600) and (i<660) for i in VP_Z5_TagN)
             
             # minute 12
             Z5_VPtagA_min12=sum((i>=660) and (i<720) for i in VP_Z5_TagA);Z5_VPtagB_min12=sum((i>=660) and (i<720) for i in VP_Z5_TagB);
             Z5_VPtagC_min12=sum((i>=660) and (i<720) for i in VP_Z5_TagC);Z5_VPtagD_min12=sum((i>=660) and (i<720) for i in VP_Z5_TagD);
             Z5_VPtagE_min12=sum((i>=660) and (i<720) for i in VP_Z5_TagE);Z5_VPtagF_min12=sum((i>=660) and (i<720) for i in VP_Z5_TagF);
             Z5_VPtagG_min12=sum((i>=660) and (i<720) for i in VP_Z5_TagG);Z5_VPtagH_min12=sum((i>=660) and (i<720) for i in VP_Z5_TagH);
             Z5_VPtagI_min12=sum((i>=660) and (i<720) for i in VP_Z5_TagI);Z5_VPtagJ_min12=sum((i>=660) and (i<720) for i in VP_Z5_TagJ);
             Z5_VPtagK_min12=sum((i>=660) and (i<720) for i in VP_Z5_TagK);Z5_VPtagL_min12=sum((i>=660) and (i<720) for i in VP_Z5_TagL);
             Z5_VPtagM_min12=sum((i>=660) and (i<720) for i in VP_Z5_TagM);Z5_VPtagN_min12=sum((i>=660) and (i<720) for i in VP_Z5_TagN)
             
             # minute 13
             Z5_VPtagA_min13=sum((i>=720) and (i<780) for i in VP_Z5_TagA);Z5_VPtagB_min13=sum((i>=720) and (i<780)for i in VP_Z5_TagB);
             Z5_VPtagC_min13=sum((i>=720) and (i<780) for i in VP_Z5_TagC);Z5_VPtagD_min13=sum((i>=720) and (i<780) for i in VP_Z5_TagD);
             Z5_VPtagE_min13=sum((i>=720) and (i<780) for i in VP_Z5_TagE);Z5_VPtagF_min13=sum((i>=720) and (i<780) for i in VP_Z5_TagF);
             Z5_VPtagG_min13=sum((i>=720) and (i<780) for i in VP_Z5_TagG);Z5_VPtagH_min13=sum((i>=720) and (i<780) for i in VP_Z5_TagH);
             Z5_VPtagI_min13=sum((i>=720) and (i<780) for i in VP_Z5_TagI);Z5_VPtagJ_min13=sum((i>=720) and (i<780) for i in VP_Z5_TagJ);
             Z5_VPtagK_min13=sum((i>=720) and (i<780) for i in VP_Z5_TagK);Z5_VPtagL_min13=sum((i>=720) and (i<780) for i in VP_Z5_TagL);
             Z5_VPtagM_min13=sum((i>=720) and (i<780) for i in VP_Z5_TagM);Z5_VPtagN_min13=sum((i>=720) and (i<780) for i in VP_Z5_TagN)
             
             # minute 14
             Z5_VPtagA_min14=sum((i>=780) and (i<840) for i in VP_Z5_TagA);Z5_VPtagB_min14=sum((i>=780) and (i<840) for i in VP_Z5_TagB);
             Z5_VPtagC_min14=sum((i>=780) and (i<840) for i in VP_Z5_TagC);Z5_VPtagD_min14=sum((i>=780) and (i<840) for i in VP_Z5_TagD);
             Z5_VPtagE_min14=sum((i>=780) and (i<840) for i in VP_Z5_TagE);Z5_VPtagF_min14=sum((i>=780) and (i<840) for i in VP_Z5_TagF);
             Z5_VPtagG_min14=sum((i>=780) and (i<840) for i in VP_Z5_TagG);Z5_VPtagH_min14=sum((i>=780) and (i<840) for i in VP_Z5_TagH);
             Z5_VPtagI_min14=sum((i>=780) and (i<840) for i in VP_Z5_TagI);Z5_VPtagJ_min14=sum((i>=780) and (i<840) for i in VP_Z5_TagJ);
             Z5_VPtagK_min14=sum((i>=780) and (i<840)for i in VP_Z5_TagK);Z5_VPtagL_min14=sum((i>=780) and (i<840) for i in VP_Z5_TagL);
             Z5_VPtagM_min14=sum((i>=780) and (i<840) for i in VP_Z5_TagM);Z5_VPtagN_min14=sum((i>=780) and (i<840) for i in VP_Z5_TagN)
             
             # minute 15
             Z5_VPtagA_min15=sum((i>=840) and (i<=900) for i in VP_Z5_TagA);Z5_VPtagB_min15=sum((i>=840) and (i<=900) for i in VP_Z5_TagB);
             Z5_VPtagC_min15=sum((i>=840) and (i<=900) for i in VP_Z5_TagC);Z5_VPtagD_min15=sum((i>=840) and (i<=900) for i in VP_Z5_TagD);
             Z5_VPtagE_min15=sum((i>=840) and (i<=900) for i in VP_Z5_TagE);Z5_VPtagF_min15=sum((i>=840) and (i<=900) for i in VP_Z5_TagF);
             Z5_VPtagG_min15=sum((i>=840) and (i<=900) for i in VP_Z5_TagG);Z5_VPtagH_min15=sum((i>=840) and (i<=900) for i in VP_Z5_TagH);
             Z5_VPtagI_min15=sum((i>=840) and (i<=900) for i in VP_Z5_TagI);Z5_VPtagJ_min15=sum((i>=840) and (i<=900) for i in VP_Z5_TagJ);
             Z5_VPtagK_min15=sum((i>=840) and (i<=900) for i in VP_Z5_TagK);Z5_VPtagL_min15=sum((i>=840) and (i<=900) for i in VP_Z5_TagL);
             Z5_VPtagM_min15=sum((i>=840) and (i<=900) for i in VP_Z5_TagM);Z5_VPtagN_min15=sum((i>=840) and (i<=900) for i in VP_Z5_TagN)

             Z1_VPtagA_mins.append([Z1_VPtagA_min1,Z1_VPtagA_min2,Z1_VPtagA_min3,Z1_VPtagA_min4,Z1_VPtagA_min5,Z1_VPtagA_min6,Z1_VPtagA_min7,Z1_VPtagA_min8,
                                    Z1_VPtagA_min9,Z1_VPtagA_min10,Z1_VPtagA_min11,Z1_VPtagA_min12,Z1_VPtagA_min13,Z1_VPtagA_min14,Z1_VPtagA_min15])
             Z1_VPtagB_mins.append([Z1_VPtagB_min1,Z1_VPtagB_min2,Z1_VPtagB_min3,Z1_VPtagB_min4,Z1_VPtagB_min5,Z1_VPtagB_min6,Z1_VPtagB_min7,Z1_VPtagB_min8,
                                    Z1_VPtagB_min9,Z1_VPtagB_min10,Z1_VPtagB_min11,Z1_VPtagB_min12,Z1_VPtagB_min13,Z1_VPtagB_min14,Z1_VPtagB_min15])
             Z1_VPtagC_mins.append([Z1_VPtagC_min1,Z1_VPtagC_min2,Z1_VPtagC_min3,Z1_VPtagC_min4,Z1_VPtagC_min5,Z1_VPtagC_min6,Z1_VPtagC_min7,Z1_VPtagC_min8,
                                    Z1_VPtagC_min9,Z1_VPtagC_min10,Z1_VPtagC_min11,Z1_VPtagC_min12,Z1_VPtagC_min13,Z1_VPtagC_min14,Z1_VPtagC_min15])
             Z1_VPtagD_mins.append([Z1_VPtagD_min1,Z1_VPtagD_min2,Z1_VPtagD_min3,Z1_VPtagD_min4,Z1_VPtagD_min5,Z1_VPtagD_min6,Z1_VPtagD_min7,Z1_VPtagD_min8,
                                    Z1_VPtagD_min9,Z1_VPtagD_min10,Z1_VPtagD_min11,Z1_VPtagD_min12,Z1_VPtagD_min13,Z1_VPtagD_min14,Z1_VPtagD_min15])
             Z1_VPtagE_mins.append([Z1_VPtagE_min1,Z1_VPtagE_min2,Z1_VPtagE_min3,Z1_VPtagE_min4,Z1_VPtagE_min5,Z1_VPtagE_min6,Z1_VPtagE_min7,Z1_VPtagE_min8,
                                    Z1_VPtagE_min9,Z1_VPtagE_min10,Z1_VPtagE_min11,Z1_VPtagE_min12,Z1_VPtagE_min13,Z1_VPtagE_min14,Z1_VPtagE_min15])
             Z1_VPtagF_mins.append([Z1_VPtagF_min1,Z1_VPtagF_min2,Z1_VPtagF_min3,Z1_VPtagF_min4,Z1_VPtagF_min5,Z1_VPtagF_min6,Z1_VPtagF_min7,Z1_VPtagF_min8,
                                    Z1_VPtagF_min9,Z1_VPtagF_min10,Z1_VPtagF_min11,Z1_VPtagF_min12,Z1_VPtagF_min13,Z1_VPtagF_min14,Z1_VPtagF_min15])
             Z1_VPtagG_mins.append([Z1_VPtagG_min1,Z1_VPtagG_min2,Z1_VPtagG_min3,Z1_VPtagG_min4,Z1_VPtagG_min5,Z1_VPtagG_min6,Z1_VPtagG_min7,Z1_VPtagG_min8,
                                    Z1_VPtagG_min9,Z1_VPtagG_min10,Z1_VPtagG_min11,Z1_VPtagG_min12,Z1_VPtagG_min13,Z1_VPtagG_min14,Z1_VPtagG_min15])
             Z1_VPtagH_mins.append([Z1_VPtagH_min1,Z1_VPtagH_min2,Z1_VPtagH_min3,Z1_VPtagH_min4,Z1_VPtagH_min5,Z1_VPtagH_min6,Z1_VPtagH_min7,Z1_VPtagH_min8,
                                    Z1_VPtagH_min9,Z1_VPtagH_min10,Z1_VPtagH_min11,Z1_VPtagH_min12,Z1_VPtagH_min13,Z1_VPtagH_min14,Z1_VPtagH_min15])
             Z1_VPtagI_mins.append([Z1_VPtagI_min1,Z1_VPtagI_min2,Z1_VPtagI_min3,Z1_VPtagI_min4,Z1_VPtagI_min5,Z1_VPtagI_min6,Z1_VPtagI_min7,Z1_VPtagI_min8,
                                    Z1_VPtagI_min9,Z1_VPtagI_min10,Z1_VPtagI_min11,Z1_VPtagI_min12,Z1_VPtagI_min13,Z1_VPtagI_min14,Z1_VPtagI_min15])
             Z1_VPtagJ_mins.append([Z1_VPtagJ_min1,Z1_VPtagJ_min2,Z1_VPtagJ_min3,Z1_VPtagJ_min4,Z1_VPtagJ_min5,Z1_VPtagJ_min6,Z1_VPtagJ_min7,Z1_VPtagJ_min8,
                                    Z1_VPtagJ_min9,Z1_VPtagJ_min10,Z1_VPtagJ_min11,Z1_VPtagJ_min12,Z1_VPtagJ_min13,Z1_VPtagJ_min14,Z1_VPtagJ_min15])
             Z1_VPtagK_mins.append([Z1_VPtagK_min1,Z1_VPtagK_min2,Z1_VPtagK_min3,Z1_VPtagK_min4,Z1_VPtagK_min5,Z1_VPtagK_min6,Z1_VPtagK_min7,Z1_VPtagK_min8,
                                    Z1_VPtagK_min9,Z1_VPtagK_min10,Z1_VPtagK_min11,Z1_VPtagK_min12,Z1_VPtagK_min13,Z1_VPtagK_min14,Z1_VPtagK_min15])
             Z1_VPtagL_mins.append([Z1_VPtagL_min1,Z1_VPtagL_min2,Z1_VPtagL_min3,Z1_VPtagL_min4,Z1_VPtagL_min5,Z1_VPtagL_min6,Z1_VPtagL_min7,Z1_VPtagL_min8,
                                    Z1_VPtagL_min9,Z1_VPtagL_min10,Z1_VPtagL_min11,Z1_VPtagL_min12,Z1_VPtagL_min13,Z1_VPtagL_min14,Z1_VPtagL_min15])
             Z1_VPtagM_mins.append([Z1_VPtagM_min1,Z1_VPtagM_min2,Z1_VPtagM_min3,Z1_VPtagM_min4,Z1_VPtagM_min5,Z1_VPtagM_min6,Z1_VPtagM_min7,Z1_VPtagM_min8,
                                    Z1_VPtagM_min9,Z1_VPtagM_min10,Z1_VPtagM_min11,Z1_VPtagM_min12,Z1_VPtagM_min13,Z1_VPtagM_min14,Z1_VPtagM_min15])
             Z1_VPtagN_mins.append([Z1_VPtagN_min1,Z1_VPtagN_min2,Z1_VPtagN_min3,Z1_VPtagN_min4,Z1_VPtagN_min5,Z1_VPtagN_min6,Z1_VPtagN_min7,Z1_VPtagN_min8,
                                    Z1_VPtagN_min9,Z1_VPtagN_min10,Z1_VPtagN_min11,Z1_VPtagN_min12,Z1_VPtagN_min13,Z1_VPtagN_min14,Z1_VPtagN_min15])

             Z2_VPtagA_mins.append([Z2_VPtagA_min1,Z2_VPtagA_min2,Z2_VPtagA_min3,Z2_VPtagA_min4,Z2_VPtagA_min5,Z2_VPtagA_min6,Z2_VPtagA_min7,Z2_VPtagA_min8,
                                    Z2_VPtagA_min9,Z2_VPtagA_min10,Z2_VPtagA_min11,Z2_VPtagA_min12,Z2_VPtagA_min13,Z2_VPtagA_min14,Z2_VPtagA_min15])
             Z2_VPtagB_mins.append([Z2_VPtagB_min1,Z2_VPtagB_min2,Z2_VPtagB_min3,Z2_VPtagB_min4,Z2_VPtagB_min5,Z2_VPtagB_min6,Z2_VPtagB_min7,Z2_VPtagB_min8,
                                    Z2_VPtagB_min9,Z2_VPtagB_min10,Z2_VPtagB_min11,Z2_VPtagB_min12,Z2_VPtagB_min13,Z2_VPtagB_min14,Z2_VPtagB_min15])
             Z2_VPtagC_mins.append([Z2_VPtagC_min1,Z2_VPtagC_min2,Z2_VPtagC_min3,Z2_VPtagC_min4,Z2_VPtagC_min5,Z2_VPtagC_min6,Z2_VPtagC_min7,Z2_VPtagC_min8,
                                    Z2_VPtagC_min9,Z2_VPtagC_min10,Z2_VPtagC_min11,Z2_VPtagC_min12,Z2_VPtagC_min13,Z2_VPtagC_min14,Z2_VPtagC_min15])
             Z2_VPtagD_mins.append([Z2_VPtagD_min1,Z2_VPtagD_min2,Z2_VPtagD_min3,Z2_VPtagD_min4,Z2_VPtagD_min5,Z2_VPtagD_min6,Z2_VPtagD_min7,Z2_VPtagD_min8,
                                    Z2_VPtagD_min9,Z2_VPtagD_min10,Z2_VPtagD_min11,Z2_VPtagD_min12,Z2_VPtagD_min13,Z2_VPtagD_min14,Z2_VPtagD_min15])
             Z2_VPtagE_mins.append([Z2_VPtagE_min1,Z2_VPtagE_min2,Z2_VPtagE_min3,Z2_VPtagE_min4,Z2_VPtagE_min5,Z2_VPtagE_min6,Z2_VPtagE_min7,Z2_VPtagE_min8,
                                    Z2_VPtagE_min9,Z2_VPtagE_min10,Z2_VPtagE_min11,Z2_VPtagE_min12,Z2_VPtagE_min13,Z2_VPtagE_min14,Z2_VPtagE_min15])
             Z2_VPtagF_mins.append([Z2_VPtagF_min1,Z2_VPtagF_min2,Z2_VPtagF_min3,Z2_VPtagF_min4,Z2_VPtagF_min5,Z2_VPtagF_min6,Z2_VPtagF_min7,Z2_VPtagF_min8,
                                    Z2_VPtagF_min9,Z2_VPtagF_min10,Z2_VPtagF_min11,Z2_VPtagF_min12,Z2_VPtagF_min13,Z2_VPtagF_min14,Z2_VPtagF_min15])
             Z2_VPtagG_mins.append([Z2_VPtagG_min1,Z2_VPtagG_min2,Z2_VPtagG_min3,Z2_VPtagG_min4,Z2_VPtagG_min5,Z2_VPtagG_min6,Z2_VPtagG_min7,Z2_VPtagG_min8,
                                    Z2_VPtagG_min9,Z2_VPtagG_min10,Z2_VPtagG_min11,Z2_VPtagG_min12,Z2_VPtagG_min13,Z2_VPtagG_min14,Z2_VPtagG_min15])
             Z2_VPtagH_mins.append([Z2_VPtagH_min1,Z2_VPtagH_min2,Z2_VPtagH_min3,Z2_VPtagH_min4,Z2_VPtagH_min5,Z2_VPtagH_min6,Z2_VPtagH_min7,Z2_VPtagH_min8,
                                    Z2_VPtagH_min9,Z2_VPtagH_min10,Z2_VPtagH_min11,Z2_VPtagH_min12,Z2_VPtagH_min13,Z2_VPtagH_min14,Z2_VPtagH_min15])
             Z2_VPtagI_mins.append([Z2_VPtagI_min1,Z2_VPtagI_min2,Z2_VPtagI_min3,Z2_VPtagI_min4,Z2_VPtagI_min5,Z2_VPtagI_min6,Z2_VPtagI_min7,Z2_VPtagI_min8,
                                    Z2_VPtagI_min9,Z2_VPtagI_min10,Z2_VPtagI_min11,Z2_VPtagI_min12,Z2_VPtagI_min13,Z2_VPtagI_min14,Z2_VPtagI_min15])
             Z2_VPtagJ_mins.append([Z2_VPtagJ_min1,Z2_VPtagJ_min2,Z2_VPtagJ_min3,Z2_VPtagJ_min4,Z2_VPtagJ_min5,Z2_VPtagJ_min6,Z2_VPtagJ_min7,Z2_VPtagJ_min8,
                                    Z2_VPtagJ_min9,Z2_VPtagJ_min10,Z2_VPtagJ_min11,Z2_VPtagJ_min12,Z2_VPtagJ_min13,Z2_VPtagJ_min14,Z2_VPtagJ_min15])
             Z2_VPtagK_mins.append([Z2_VPtagK_min1,Z2_VPtagK_min2,Z2_VPtagK_min3,Z2_VPtagK_min4,Z2_VPtagK_min5,Z2_VPtagK_min6,Z2_VPtagK_min7,Z2_VPtagK_min8,
                                    Z2_VPtagK_min9,Z2_VPtagK_min10,Z2_VPtagK_min11,Z2_VPtagK_min12,Z2_VPtagK_min13,Z2_VPtagK_min14,Z2_VPtagK_min15])
             Z2_VPtagL_mins.append([Z2_VPtagL_min1,Z2_VPtagL_min2,Z2_VPtagL_min3,Z2_VPtagL_min4,Z2_VPtagL_min5,Z2_VPtagL_min6,Z2_VPtagL_min7,Z2_VPtagL_min8,
                                    Z2_VPtagL_min9,Z2_VPtagL_min10,Z2_VPtagL_min11,Z2_VPtagL_min12,Z2_VPtagL_min13,Z2_VPtagL_min14,Z2_VPtagL_min15])
             Z2_VPtagM_mins.append([Z2_VPtagM_min1,Z2_VPtagM_min2,Z2_VPtagM_min3,Z2_VPtagM_min4,Z2_VPtagM_min5,Z2_VPtagM_min6,Z2_VPtagM_min7,Z2_VPtagM_min8,
                                    Z2_VPtagM_min9,Z2_VPtagM_min10,Z2_VPtagM_min11,Z2_VPtagM_min12,Z2_VPtagM_min13,Z2_VPtagM_min14,Z2_VPtagM_min15])
             Z2_VPtagN_mins.append([Z2_VPtagN_min1,Z2_VPtagN_min2,Z2_VPtagN_min3,Z2_VPtagN_min4,Z2_VPtagN_min5,Z2_VPtagN_min6,Z2_VPtagN_min7,Z2_VPtagN_min8,
                                    Z2_VPtagN_min9,Z2_VPtagN_min10,Z2_VPtagN_min11,Z2_VPtagN_min12,Z2_VPtagN_min13,Z2_VPtagN_min14,Z2_VPtagN_min15])
             
             Z3_VPtagA_mins.append([Z3_VPtagA_min1,Z3_VPtagA_min2,Z3_VPtagA_min3,Z3_VPtagA_min4,Z3_VPtagA_min5,Z3_VPtagA_min6,Z3_VPtagA_min7,Z3_VPtagA_min8,
                                    Z3_VPtagA_min9,Z3_VPtagA_min10,Z3_VPtagA_min11,Z3_VPtagA_min12,Z3_VPtagA_min13,Z3_VPtagA_min14,Z3_VPtagA_min15])
             Z3_VPtagB_mins.append([Z3_VPtagB_min1,Z3_VPtagB_min2,Z3_VPtagB_min3,Z3_VPtagB_min4,Z3_VPtagB_min5,Z3_VPtagB_min6,Z3_VPtagB_min7,Z3_VPtagB_min8,
                                    Z3_VPtagB_min9,Z3_VPtagB_min10,Z3_VPtagB_min11,Z3_VPtagB_min12,Z3_VPtagB_min13,Z3_VPtagB_min14,Z3_VPtagB_min15])
             Z3_VPtagC_mins.append([Z3_VPtagC_min1,Z3_VPtagC_min2,Z3_VPtagC_min3,Z3_VPtagC_min4,Z3_VPtagC_min5,Z3_VPtagC_min6,Z3_VPtagC_min7,Z3_VPtagC_min8,
                                    Z3_VPtagC_min9,Z3_VPtagC_min10,Z3_VPtagC_min11,Z3_VPtagC_min12,Z3_VPtagC_min13,Z3_VPtagC_min14,Z3_VPtagC_min15])
             Z3_VPtagD_mins.append([Z3_VPtagD_min1,Z3_VPtagD_min2,Z3_VPtagD_min3,Z3_VPtagD_min4,Z3_VPtagD_min5,Z3_VPtagD_min6,Z3_VPtagD_min7,Z3_VPtagD_min8,
                                    Z3_VPtagD_min9,Z3_VPtagD_min10,Z3_VPtagD_min11,Z3_VPtagD_min12,Z3_VPtagD_min13,Z3_VPtagD_min14,Z3_VPtagD_min15])
             Z3_VPtagE_mins.append([Z3_VPtagE_min1,Z3_VPtagE_min2,Z3_VPtagE_min3,Z3_VPtagE_min4,Z3_VPtagE_min5,Z3_VPtagE_min6,Z3_VPtagE_min7,Z3_VPtagE_min8,
                                    Z3_VPtagE_min9,Z3_VPtagE_min10,Z3_VPtagE_min11,Z3_VPtagE_min12,Z3_VPtagE_min13,Z3_VPtagE_min14,Z3_VPtagE_min15])
             Z3_VPtagF_mins.append([Z3_VPtagF_min1,Z3_VPtagF_min2,Z3_VPtagF_min3,Z3_VPtagF_min4,Z3_VPtagF_min5,Z3_VPtagF_min6,Z3_VPtagF_min7,Z3_VPtagF_min8,
                                    Z3_VPtagF_min9,Z3_VPtagF_min10,Z3_VPtagF_min11,Z3_VPtagF_min12,Z3_VPtagF_min13,Z3_VPtagF_min14,Z3_VPtagF_min15])
             Z3_VPtagG_mins.append([Z3_VPtagG_min1,Z3_VPtagG_min2,Z3_VPtagG_min3,Z3_VPtagG_min4,Z3_VPtagG_min5,Z3_VPtagG_min6,Z3_VPtagG_min7,Z3_VPtagG_min8,
                                    Z3_VPtagG_min9,Z3_VPtagG_min10,Z3_VPtagG_min11,Z3_VPtagG_min12,Z3_VPtagG_min13,Z3_VPtagG_min14,Z3_VPtagG_min15])
             Z3_VPtagH_mins.append([Z3_VPtagH_min1,Z3_VPtagH_min2,Z3_VPtagH_min3,Z3_VPtagH_min4,Z3_VPtagH_min5,Z3_VPtagH_min6,Z3_VPtagH_min7,Z3_VPtagH_min8,
                                    Z3_VPtagH_min9,Z3_VPtagH_min10,Z3_VPtagH_min11,Z3_VPtagH_min12,Z3_VPtagH_min13,Z3_VPtagH_min14,Z3_VPtagH_min15])
             Z3_VPtagI_mins.append([Z3_VPtagI_min1,Z3_VPtagI_min2,Z3_VPtagI_min3,Z3_VPtagI_min4,Z3_VPtagI_min5,Z3_VPtagI_min6,Z3_VPtagI_min7,Z3_VPtagI_min8,
                                    Z3_VPtagI_min9,Z3_VPtagI_min10,Z3_VPtagI_min11,Z3_VPtagI_min12,Z3_VPtagI_min13,Z3_VPtagI_min14,Z3_VPtagI_min15])
             Z3_VPtagJ_mins.append([Z3_VPtagJ_min1,Z3_VPtagJ_min2,Z3_VPtagJ_min3,Z3_VPtagJ_min4,Z3_VPtagJ_min5,Z3_VPtagJ_min6,Z3_VPtagJ_min7,Z3_VPtagJ_min8,
                                    Z3_VPtagJ_min9,Z3_VPtagJ_min10,Z3_VPtagJ_min11,Z3_VPtagJ_min12,Z3_VPtagJ_min13,Z3_VPtagJ_min14,Z3_VPtagJ_min15])
             Z3_VPtagK_mins.append([Z3_VPtagK_min1,Z3_VPtagK_min2,Z3_VPtagK_min3,Z3_VPtagK_min4,Z3_VPtagK_min5,Z3_VPtagK_min6,Z3_VPtagK_min7,Z3_VPtagK_min8,
                                    Z3_VPtagK_min9,Z3_VPtagK_min10,Z3_VPtagK_min11,Z3_VPtagK_min12,Z3_VPtagK_min13,Z3_VPtagK_min14,Z3_VPtagK_min15])
             Z3_VPtagL_mins.append([Z3_VPtagL_min1,Z3_VPtagL_min2,Z3_VPtagL_min3,Z3_VPtagL_min4,Z3_VPtagL_min5,Z3_VPtagL_min6,Z3_VPtagL_min7,Z3_VPtagL_min8,
                                    Z3_VPtagL_min9,Z3_VPtagL_min10,Z3_VPtagL_min11,Z3_VPtagL_min12,Z3_VPtagL_min13,Z3_VPtagL_min14,Z3_VPtagL_min15])
             Z3_VPtagM_mins.append([Z3_VPtagM_min1,Z3_VPtagM_min2,Z3_VPtagM_min3,Z3_VPtagM_min4,Z3_VPtagM_min5,Z3_VPtagM_min6,Z3_VPtagM_min7,Z3_VPtagM_min8,
                                    Z3_VPtagM_min9,Z3_VPtagM_min10,Z3_VPtagM_min11,Z3_VPtagM_min12,Z3_VPtagM_min13,Z3_VPtagM_min14,Z3_VPtagM_min15])
             Z3_VPtagN_mins.append([Z3_VPtagN_min1,Z3_VPtagN_min2,Z3_VPtagN_min3,Z3_VPtagN_min4,Z3_VPtagN_min5,Z3_VPtagN_min6,Z3_VPtagN_min7,Z3_VPtagN_min8,
                                    Z3_VPtagN_min9,Z3_VPtagN_min10,Z3_VPtagN_min11,Z3_VPtagN_min12,Z3_VPtagN_min13,Z3_VPtagN_min14,Z3_VPtagN_min15])

             Z4_VPtagA_mins.append([Z4_VPtagA_min1,Z4_VPtagA_min2,Z4_VPtagA_min3,Z4_VPtagA_min4,Z4_VPtagA_min5,Z4_VPtagA_min6,Z4_VPtagA_min7,Z4_VPtagA_min8,
                                    Z4_VPtagA_min9,Z4_VPtagA_min10,Z4_VPtagA_min11,Z4_VPtagA_min12,Z4_VPtagA_min13,Z4_VPtagA_min14,Z4_VPtagA_min15])
             Z4_VPtagB_mins.append([Z4_VPtagB_min1,Z4_VPtagB_min2,Z4_VPtagB_min3,Z4_VPtagB_min4,Z4_VPtagB_min5,Z4_VPtagB_min6,Z4_VPtagB_min7,Z4_VPtagB_min8,
                                    Z4_VPtagB_min9,Z4_VPtagB_min10,Z4_VPtagB_min11,Z4_VPtagB_min12,Z4_VPtagB_min13,Z4_VPtagB_min14,Z4_VPtagB_min15])
             Z4_VPtagC_mins.append([Z4_VPtagC_min1,Z4_VPtagC_min2,Z4_VPtagC_min3,Z4_VPtagC_min4,Z4_VPtagC_min5,Z4_VPtagC_min6,Z4_VPtagC_min7,Z4_VPtagC_min8,
                                    Z4_VPtagC_min9,Z4_VPtagC_min10,Z4_VPtagC_min11,Z4_VPtagC_min12,Z4_VPtagC_min13,Z4_VPtagC_min14,Z4_VPtagC_min15])
             Z4_VPtagD_mins.append([Z4_VPtagD_min1,Z4_VPtagD_min2,Z4_VPtagD_min3,Z4_VPtagD_min4,Z4_VPtagD_min5,Z4_VPtagD_min6,Z4_VPtagD_min7,Z4_VPtagD_min8,
                                    Z4_VPtagD_min9,Z4_VPtagD_min10,Z4_VPtagD_min11,Z4_VPtagD_min12,Z4_VPtagD_min13,Z4_VPtagD_min14,Z4_VPtagD_min15])
             Z4_VPtagE_mins.append([Z4_VPtagE_min1,Z4_VPtagE_min2,Z4_VPtagE_min3,Z4_VPtagE_min4,Z4_VPtagE_min5,Z4_VPtagE_min6,Z4_VPtagE_min7,Z4_VPtagE_min8,
                                    Z4_VPtagE_min9,Z4_VPtagE_min10,Z4_VPtagE_min11,Z4_VPtagE_min12,Z4_VPtagE_min13,Z4_VPtagE_min14,Z4_VPtagE_min15])
             Z4_VPtagF_mins.append([Z4_VPtagF_min1,Z4_VPtagF_min2,Z4_VPtagF_min3,Z4_VPtagF_min4,Z4_VPtagF_min5,Z4_VPtagF_min6,Z4_VPtagF_min7,Z4_VPtagF_min8,
                                    Z4_VPtagF_min9,Z4_VPtagF_min10,Z4_VPtagF_min11,Z4_VPtagF_min12,Z4_VPtagF_min13,Z4_VPtagF_min14,Z4_VPtagF_min15])
             Z4_VPtagG_mins.append([Z4_VPtagG_min1,Z4_VPtagG_min2,Z4_VPtagG_min3,Z4_VPtagG_min4,Z4_VPtagG_min5,Z4_VPtagG_min6,Z4_VPtagG_min7,Z4_VPtagG_min8,
                                    Z4_VPtagG_min9,Z4_VPtagG_min10,Z4_VPtagG_min11,Z4_VPtagG_min12,Z4_VPtagG_min13,Z4_VPtagG_min14,Z4_VPtagG_min15])
             Z4_VPtagH_mins.append([Z4_VPtagH_min1,Z4_VPtagH_min2,Z4_VPtagH_min3,Z4_VPtagH_min4,Z4_VPtagH_min5,Z4_VPtagH_min6,Z4_VPtagH_min7,Z4_VPtagH_min8,
                                    Z4_VPtagH_min9,Z4_VPtagH_min10,Z4_VPtagH_min11,Z4_VPtagH_min12,Z4_VPtagH_min13,Z4_VPtagH_min14,Z4_VPtagH_min15])
             Z4_VPtagI_mins.append([Z4_VPtagI_min1,Z4_VPtagI_min2,Z4_VPtagI_min3,Z4_VPtagI_min4,Z4_VPtagI_min5,Z4_VPtagI_min6,Z4_VPtagI_min7,Z4_VPtagI_min8,
                                    Z4_VPtagI_min9,Z4_VPtagI_min10,Z4_VPtagI_min11,Z4_VPtagI_min12,Z4_VPtagI_min13,Z4_VPtagI_min14,Z4_VPtagI_min15])
             Z4_VPtagJ_mins.append([Z4_VPtagJ_min1,Z4_VPtagJ_min2,Z4_VPtagJ_min3,Z4_VPtagJ_min4,Z4_VPtagJ_min5,Z4_VPtagJ_min6,Z4_VPtagJ_min7,Z4_VPtagJ_min8,
                                    Z4_VPtagJ_min9,Z4_VPtagJ_min10,Z4_VPtagJ_min11,Z4_VPtagJ_min12,Z4_VPtagJ_min13,Z4_VPtagJ_min14,Z4_VPtagJ_min15])
             Z4_VPtagK_mins.append([Z4_VPtagK_min1,Z4_VPtagK_min2,Z4_VPtagK_min3,Z4_VPtagK_min4,Z4_VPtagK_min5,Z4_VPtagK_min6,Z4_VPtagK_min7,Z4_VPtagK_min8,
                                    Z4_VPtagK_min9,Z4_VPtagK_min10,Z4_VPtagK_min11,Z4_VPtagK_min12,Z4_VPtagK_min13,Z4_VPtagK_min14,Z4_VPtagK_min15])
             Z4_VPtagL_mins.append([Z4_VPtagL_min1,Z4_VPtagL_min2,Z4_VPtagL_min3,Z4_VPtagL_min4,Z4_VPtagL_min5,Z4_VPtagL_min6,Z4_VPtagL_min7,Z4_VPtagL_min8,
                                    Z4_VPtagL_min9,Z4_VPtagL_min10,Z4_VPtagL_min11,Z4_VPtagL_min12,Z4_VPtagL_min13,Z4_VPtagL_min14,Z4_VPtagL_min15])
             Z4_VPtagM_mins.append([Z4_VPtagM_min1,Z4_VPtagM_min2,Z4_VPtagM_min3,Z4_VPtagM_min4,Z4_VPtagM_min5,Z4_VPtagM_min6,Z4_VPtagM_min7,Z4_VPtagM_min8,
                                    Z4_VPtagM_min9,Z4_VPtagM_min10,Z4_VPtagM_min11,Z4_VPtagM_min12,Z4_VPtagM_min13,Z4_VPtagM_min14,Z4_VPtagM_min15])
             Z4_VPtagN_mins.append([Z4_VPtagN_min1,Z4_VPtagN_min2,Z4_VPtagN_min3,Z4_VPtagN_min4,Z4_VPtagN_min5,Z4_VPtagN_min6,Z4_VPtagN_min7,Z4_VPtagN_min8,
                                    Z4_VPtagN_min9,Z4_VPtagN_min10,Z4_VPtagN_min11,Z4_VPtagN_min12,Z4_VPtagN_min13,Z4_VPtagN_min14,Z4_VPtagN_min15])

             Z5_VPtagA_mins.append([Z5_VPtagA_min1,Z5_VPtagA_min2,Z5_VPtagA_min3,Z5_VPtagA_min4,Z5_VPtagA_min5,Z5_VPtagA_min6,Z5_VPtagA_min7,Z5_VPtagA_min8,
                                    Z5_VPtagA_min9,Z5_VPtagA_min10,Z5_VPtagA_min11,Z5_VPtagA_min12,Z5_VPtagA_min13,Z5_VPtagA_min14,Z5_VPtagA_min15])
             Z5_VPtagB_mins.append([Z5_VPtagB_min1,Z5_VPtagB_min2,Z5_VPtagB_min3,Z5_VPtagB_min4,Z5_VPtagB_min5,Z5_VPtagB_min6,Z5_VPtagB_min7,Z5_VPtagB_min8,
                                    Z5_VPtagB_min9,Z5_VPtagB_min10,Z5_VPtagB_min11,Z5_VPtagB_min12,Z5_VPtagB_min13,Z5_VPtagB_min14,Z5_VPtagB_min15])
             Z5_VPtagC_mins.append([Z5_VPtagC_min1,Z5_VPtagC_min2,Z5_VPtagC_min3,Z5_VPtagC_min4,Z5_VPtagC_min5,Z5_VPtagC_min6,Z5_VPtagC_min7,Z5_VPtagC_min8,
                                    Z5_VPtagC_min9,Z5_VPtagC_min10,Z5_VPtagC_min11,Z5_VPtagC_min12,Z5_VPtagC_min13,Z5_VPtagC_min14,Z5_VPtagC_min15])
             Z5_VPtagD_mins.append([Z5_VPtagD_min1,Z5_VPtagD_min2,Z5_VPtagD_min3,Z5_VPtagD_min4,Z5_VPtagD_min5,Z5_VPtagD_min6,Z5_VPtagD_min7,Z5_VPtagD_min8,
                                    Z5_VPtagD_min9,Z5_VPtagD_min10,Z5_VPtagD_min11,Z5_VPtagD_min12,Z5_VPtagD_min13,Z5_VPtagD_min14,Z5_VPtagD_min15])
             Z5_VPtagE_mins.append([Z5_VPtagE_min1,Z5_VPtagE_min2,Z5_VPtagE_min3,Z5_VPtagE_min4,Z5_VPtagE_min5,Z5_VPtagE_min6,Z5_VPtagE_min7,Z5_VPtagE_min8,
                                    Z5_VPtagE_min9,Z5_VPtagE_min10,Z5_VPtagE_min11,Z5_VPtagE_min12,Z5_VPtagE_min13,Z5_VPtagE_min14,Z5_VPtagE_min15])
             Z5_VPtagF_mins.append([Z5_VPtagF_min1,Z5_VPtagF_min2,Z5_VPtagF_min3,Z5_VPtagF_min4,Z5_VPtagF_min5,Z5_VPtagF_min6,Z5_VPtagF_min7,Z5_VPtagF_min8,
                                    Z5_VPtagF_min9,Z5_VPtagF_min10,Z5_VPtagF_min11,Z5_VPtagF_min12,Z5_VPtagF_min13,Z5_VPtagF_min14,Z5_VPtagF_min15])
             Z5_VPtagG_mins.append([Z5_VPtagG_min1,Z5_VPtagG_min2,Z5_VPtagG_min3,Z5_VPtagG_min4,Z5_VPtagG_min5,Z5_VPtagG_min6,Z5_VPtagG_min7,Z5_VPtagG_min8,
                                    Z5_VPtagG_min9,Z5_VPtagG_min10,Z5_VPtagG_min11,Z5_VPtagG_min12,Z5_VPtagG_min13,Z5_VPtagG_min14,Z5_VPtagG_min15])
             Z5_VPtagH_mins.append([Z5_VPtagH_min1,Z5_VPtagH_min2,Z5_VPtagH_min3,Z5_VPtagH_min4,Z5_VPtagH_min5,Z5_VPtagH_min6,Z5_VPtagH_min7,Z5_VPtagH_min8,
                                    Z5_VPtagH_min9,Z5_VPtagH_min10,Z5_VPtagH_min11,Z5_VPtagH_min12,Z5_VPtagH_min13,Z5_VPtagH_min14,Z5_VPtagH_min15])
             Z5_VPtagI_mins.append([Z5_VPtagI_min1,Z5_VPtagI_min2,Z5_VPtagI_min3,Z5_VPtagI_min4,Z5_VPtagI_min5,Z5_VPtagI_min6,Z5_VPtagI_min7,Z5_VPtagI_min8,
                                    Z5_VPtagI_min9,Z5_VPtagI_min10,Z5_VPtagI_min11,Z5_VPtagI_min12,Z5_VPtagI_min13,Z5_VPtagI_min14,Z5_VPtagI_min15])
             Z5_VPtagJ_mins.append([Z5_VPtagJ_min1,Z5_VPtagJ_min2,Z5_VPtagJ_min3,Z5_VPtagJ_min4,Z5_VPtagJ_min5,Z5_VPtagJ_min6,Z5_VPtagJ_min7,Z5_VPtagJ_min8,
                                    Z5_VPtagJ_min9,Z5_VPtagJ_min10,Z5_VPtagJ_min11,Z5_VPtagJ_min12,Z5_VPtagJ_min13,Z5_VPtagJ_min14,Z5_VPtagJ_min15])
             Z5_VPtagK_mins.append([Z5_VPtagK_min1,Z5_VPtagK_min2,Z5_VPtagK_min3,Z5_VPtagK_min4,Z5_VPtagK_min5,Z5_VPtagK_min6,Z5_VPtagK_min7,Z5_VPtagK_min8,
                                    Z5_VPtagK_min9,Z5_VPtagK_min10,Z5_VPtagK_min11,Z5_VPtagK_min12,Z5_VPtagK_min13,Z5_VPtagK_min14,Z5_VPtagK_min15])
             Z5_VPtagL_mins.append([Z5_VPtagL_min1,Z5_VPtagL_min2,Z5_VPtagL_min3,Z5_VPtagL_min4,Z5_VPtagL_min5,Z5_VPtagL_min6,Z5_VPtagL_min7,Z5_VPtagL_min8,
                                    Z5_VPtagL_min9,Z5_VPtagL_min10,Z5_VPtagL_min11,Z5_VPtagL_min12,Z5_VPtagL_min13,Z5_VPtagL_min14,Z5_VPtagL_min15])
             Z5_VPtagM_mins.append([Z5_VPtagM_min1,Z5_VPtagM_min2,Z5_VPtagM_min3,Z5_VPtagM_min4,Z5_VPtagM_min5,Z5_VPtagM_min6,Z5_VPtagM_min7,Z5_VPtagM_min8,
                                    Z5_VPtagM_min9,Z5_VPtagM_min10,Z5_VPtagM_min11,Z5_VPtagM_min12,Z5_VPtagM_min13,Z5_VPtagM_min14,Z5_VPtagM_min15])
             Z5_VPtagN_mins.append([Z5_VPtagN_min1,Z5_VPtagN_min2,Z5_VPtagN_min3,Z5_VPtagN_min4,Z5_VPtagN_min5,Z5_VPtagN_min6,Z5_VPtagN_min7,Z5_VPtagN_min8,
                                    Z5_VPtagN_min9,Z5_VPtagN_min10,Z5_VPtagN_min11,Z5_VPtagN_min12,Z5_VPtagN_min13,Z5_VPtagN_min14,Z5_VPtagN_min15])
             
             VP_Z1_percent=[]
             VP_Z2_percent=[]
             VP_Z3_percent=[]
             VP_Z4_percent=[]
             VP_Z5_percent=[]
     
             VP_Z1_percent.append([Z1_VPtagA_mins,Z1_VPtagB_mins,Z1_VPtagC_mins,Z1_VPtagD_mins,Z1_VPtagE_mins,Z1_VPtagF_mins,Z1_VPtagG_mins,
                                   Z1_VPtagH_mins,Z1_VPtagI_mins,Z1_VPtagJ_mins,Z1_VPtagK_mins,Z1_VPtagL_mins,Z1_VPtagM_mins,Z1_VPtagN_mins])

             VP_Z2_percent.append([Z2_VPtagA_mins,Z2_VPtagB_mins,Z2_VPtagC_mins,Z2_VPtagD_mins,Z2_VPtagE_mins,Z2_VPtagF_mins,Z2_VPtagG_mins,
                                   Z2_VPtagH_mins,Z2_VPtagI_mins,Z2_VPtagJ_mins,Z2_VPtagK_mins,Z2_VPtagL_mins,Z2_VPtagM_mins,Z2_VPtagN_mins])
             
             VP_Z3_percent.append([Z3_VPtagA_mins,Z3_VPtagB_mins,Z3_VPtagC_mins,Z3_VPtagD_mins,Z3_VPtagE_mins,Z3_VPtagF_mins,Z3_VPtagG_mins,
                                   Z3_VPtagH_mins,Z3_VPtagI_mins,Z3_VPtagJ_mins,Z3_VPtagK_mins,Z3_VPtagL_mins,Z3_VPtagM_mins,Z3_VPtagN_mins])
             
             VP_Z4_percent.append([Z4_VPtagA_mins,Z4_VPtagB_mins,Z4_VPtagC_mins,Z4_VPtagD_mins,Z4_VPtagE_mins,Z4_VPtagF_mins,Z4_VPtagG_mins,
                                   Z4_VPtagH_mins,Z4_VPtagI_mins,Z4_VPtagJ_mins,Z4_VPtagK_mins,Z4_VPtagL_mins,Z4_VPtagM_mins,Z4_VPtagN_mins])
                      
             VP_Z5_percent.append([Z5_VPtagA_mins,Z5_VPtagB_mins,Z5_VPtagC_mins,Z5_VPtagD_mins,Z5_VPtagE_mins,Z5_VPtagF_mins,Z5_VPtagG_mins,
                                   Z5_VPtagH_mins,Z5_VPtagI_mins,Z5_VPtagJ_mins,Z5_VPtagK_mins,Z5_VPtagL_mins,Z5_VPtagM_mins,Z5_VPtagN_mins])
       
             
             VP_Z1_percent=np.array(VP_Z1_percent,dtype=np.float64)
             VP_Z2_percent=np.array(VP_Z2_percent,dtype=np.float64)
             VP_Z3_percent=np.array(VP_Z3_percent,dtype=np.float64)
             VP_Z4_percent=np.array(VP_Z4_percent,dtype=np.float64)
             VP_Z5_percent=np.array(VP_Z5_percent,dtype=np.float64)
             
      #       VP_Z1_percent=np.round((VP_Z1_percent/60)*100)    #out of 60(1 minute)
       #      VP_Z2_percent=np.round((VP_Z2_percent/60)*100)  #(1, 14, 1, 15)
        #     VP_Z3_percent=np.round((VP_Z3_percent/60)*100)
         #    VP_Z4_percent=np.round((VP_Z4_percent/60)*100)
          #   VP_Z5_percent=np.round((VP_Z5_percent/60)*100)
             while self.completed <81:
                self.completed += 1
             self.progressBar.setValue (self.completed)
             self.progressBar.setValue (self.almost)
             
    ###################################################### np matrix shape troubleshoot #####################################################################         
    ##         print("Time",Time.shape)
    ##         print("Time_one",Time_one.shape)
    ##         print("countall",count_all.shape)
    ##         print("resultant diff",Resultant_diff.shape)
    ##         print("Work_Rest1",Work_Rest1.shape)

    ##         print("Work_Percent",Work_Percent.shape)
    ##         print("Rest_Percent",Rest_Percent.shape)
    ##         print("VP_Z1_percent",VP_Z1_percent.shape)
    ##         print("VP_Z2_percent",VP_Z2_percent.shape)
    ##         print("VP_Z3_percent",VP_Z3_percent.shape)
    ##         print("VP_Z4_percent",VP_Z4_percent.shape)
    ##         print("VP_Z5_percent",VP_Z5_percent.shape)
    ##         print("Space")
    ##
    ##         print("Resultant_diff_max",Resultant_diff_max.shape)
    ##         print("Distance_max",Distance_max.shape)
    ##         print("Speed_max",Speed_max.shape)
    ##         print("Resultant_Acceleration_max",Resultant_Acceleration_max.shape)
    ##         print("Resultant_Velocity_max",Resultant_Velocity_max.shape)
    ##         print("Distance_mean",Distance_mean.shape)
    ##         print("Speed_mean",Speed_mean.shape)
    ##         print("Resultant_Acceleration_mean",Resultant_Acceleration_mean.shape)
    ##         print("Resultant_Velocity_mean",Resultant_Velocity_mean.shape)

    ################################################################################################################################################
    ################################################################################################################################################

             for i in range (len(Tag_dict)):
                # Graph_amount=["Av.Pos(m)", "Max Pos(m)", "Av.Dist(m)", "Max Dist(m)", "Av.Speed(m/s)", "Max.Speed(m/s)"]
                 Graph_amount1=["Av.Speed", "Max.Speed"]
                 Graph_amount2=["Av.Accel", "Max Accel"]
                 Graph_amount3=["Av.Work", "Av.Rest"]
                 Graph_amount4=["1", "2","3", "4","5", "6","7", "8","9", "10","11", "12","13", "14","15"]
                 
                 if len(Tag_dict) ==1:
                   #  Metric=[Resultant_diff_mean,Resultant_diff_max, Distance_mean, Distance_max, Speed_mean, Speed_max]
                     Metric1=(Speed_mean[0], Speed_max[0])
                     Metric1=np.array(Metric1,dtype=np.float64)
                     Metric2=[Resultant_Acceleration_mean[0], Resultant_Acceleration_max[0]]
                     Metric3=[Average_Work[0], Average_Rest[0]]
                   #  Metric_series = Metric      
                     Metric_series1 = Metric1
                     Metric_series2 = Metric2
                     Metric_series3 = Metric3
                 else:
                 #    Metric=[Resultant_diff_mean[i],Resultant_diff_max[i], Distance_mean[i], Distance_max[i], Speed_mean[i], Speed_max[i]]
                     Metric1=[Speed_mean[i], Speed_max[i]]
                     Metric2=[Resultant_Acceleration_mean[i], Resultant_Acceleration_max[i]]
                     Metric3=[Average_Work[i], Average_Rest[i]]
                 #    Metric_series = pandas.Series.from_array(Metric)            
                     Metric_series1 = pandas.Series.from_array(Metric1)  
                     Metric_series2 = pandas.Series.from_array(Metric2)
                     Metric_series3 = pandas.Series.from_array(Metric3)
                 
               #  print(i)
                 Metric4=[Work_Percent[0][i][0][0], Work_Percent[0][i][0][1],Work_Percent[0][i][0][2],Work_Percent[0][i][0][3],Work_Percent[0][i][0][4],
                 Work_Percent[0][i][0][5],Work_Percent[0][i][0][6],Work_Percent[0][i][0][7],Work_Percent[0][i][0][8],
                 Work_Percent[0][i][0][9],Work_Percent[0][i][0][10],Work_Percent[0][i][0][11],
                 Work_Percent[0][i][0][12],Work_Percent[0][i][0][13],Work_Percent[0][i][0][14]]
                          
                 Metric5=[Rest_Percent[0][i][0][0],Rest_Percent[0][i][0][1],Rest_Percent[0][i][0][2],Rest_Percent[0][i][0][3],Rest_Percent[0][i][0][4],
                 Rest_Percent[0][i][0][5],Rest_Percent[0][i][0][6],Rest_Percent[0][i][0][7],Rest_Percent[0][i][0][8],Rest_Percent[0][i][0][9],
                 Rest_Percent[0][i][0][10],Rest_Percent[0][i][0][11],Rest_Percent[0][i][0][12],Rest_Percent[0][i][0][13],Rest_Percent[0][i][0][14]]
                 
                 Metric6=[VP_Z1_percent[0][i][0][0],VP_Z1_percent[0][i][0][1],VP_Z1_percent[0][i][0][2],VP_Z1_percent[0][i][0][3],VP_Z1_percent[0][i][0][4],
                 VP_Z1_percent[0][i][0][5],VP_Z1_percent[0][i][0][6],VP_Z1_percent[0][i][0][7],VP_Z1_percent[0][i][0][8],VP_Z1_percent[0][i][0][9],
                 VP_Z1_percent[0][i][0][10],VP_Z1_percent[0][i][0][11],VP_Z1_percent[0][i][0][12],VP_Z1_percent[0][i][0][13],VP_Z1_percent[0][i][0][14]]

                 Metric7=[VP_Z2_percent[0][i][0][0],VP_Z2_percent[0][i][0][1],VP_Z2_percent[0][i][0][2],VP_Z2_percent[0][i][0][3],VP_Z2_percent[0][i][0][4],
                 VP_Z2_percent[0][i][0][5],VP_Z2_percent[0][i][0][6],VP_Z2_percent[0][i][0][7],VP_Z2_percent[0][i][0][8],VP_Z2_percent[0][i][0][9],
                 VP_Z2_percent[0][i][0][10],VP_Z2_percent[0][i][0][11],VP_Z2_percent[0][i][0][12],VP_Z2_percent[0][i][0][13],VP_Z2_percent[0][i][0][14]]

                 Metric8=[VP_Z3_percent[0][i][0][0],VP_Z3_percent[0][i][0][1],VP_Z3_percent[0][i][0][2],VP_Z3_percent[0][i][0][3],VP_Z3_percent[0][i][0][4],
                 VP_Z3_percent[0][i][0][5],VP_Z3_percent[0][i][0][6],VP_Z3_percent[0][i][0][7],VP_Z3_percent[0][i][0][8],VP_Z3_percent[0][i][0][9],
                 VP_Z3_percent[0][i][0][10],VP_Z3_percent[0][i][0][11],VP_Z3_percent[0][i][0][12],VP_Z3_percent[0][i][0][13],VP_Z3_percent[0][i][0][14]]

                 Metric9=[VP_Z4_percent[0][i][0][0],VP_Z4_percent[0][i][0][1],VP_Z4_percent[0][i][0][2],VP_Z4_percent[0][i][0][3],VP_Z4_percent[0][i][0][4],
                 VP_Z4_percent[0][i][0][5],VP_Z4_percent[0][i][0][6],VP_Z4_percent[0][i][0][7],VP_Z4_percent[0][i][0][8],VP_Z4_percent[0][i][0][9],
                 VP_Z4_percent[0][i][0][10],VP_Z4_percent[0][i][0][11],VP_Z4_percent[0][i][0][12],VP_Z4_percent[0][i][0][13],VP_Z4_percent[0][i][0][14]]

                 Metric10=[VP_Z5_percent[0][i][0][0],VP_Z5_percent[0][i][0][1],VP_Z5_percent[0][i][0][2],VP_Z5_percent[0][i][0][3],VP_Z5_percent[0][i][0][4],
                 VP_Z5_percent[0][i][0][5],VP_Z5_percent[0][i][0][6],VP_Z5_percent[0][i][0][7],VP_Z5_percent[0][i][0][8],VP_Z5_percent[0][i][0][9],
                 VP_Z5_percent[0][i][0][10],VP_Z5_percent[0][i][0][11],VP_Z5_percent[0][i][0][12],VP_Z5_percent[0][i][0][13],VP_Z5_percent[0][i][0][14]]

                 
                     
                 Metric4=np.array(Metric4,dtype=np.float64)
                 Metric5=np.array(Metric5,dtype=np.float64)
                 Metric6=np.array(Metric6,dtype=np.float64)
                 Metric7=np.array(Metric7,dtype=np.float64)
                 Metric8=np.array(Metric8,dtype=np.float64)
                 Metric9=np.array(Metric9,dtype=np.float64)
                 Metric10=np.array(Metric10,dtype=np.float64)
                 Metric10=Metric10+1
                 #########################save plots ############################################
                 
                 width=1/1.5
                 plt.figure #(figsize=(10,8))
                 if len(Tag_dict) ==1:                     
                     n_groups = 2  #mins
                     fig, ax = plt.subplots()
                   #  ax.hold(False)
                     index = np.arange(n_groups)
                     bar_width = 1
                     opacity = 1
                     rects2 = plt.bar(0, Metric_series1[0],color='orange',width=bar_width,alpha=opacity,edgecolor ='k' )
                     rects3 = plt.bar(1+bar_width, Metric_series1[1],color='b',width=bar_width,alpha=opacity,edgecolor ='k' )
                #     plt.xlabel('Outcome')
                     plt.ylabel('Speed(m/s)')
                     plt.title('Speed')
                     plt.xticks(np.arange(3),("Av.Speed","","Max.Speed"))
                     plt.tight_layout()
                     rects = ax.patches
                     space = 10
                     va='top'


                     for rect in rects:
                        # Get X and Y placement of label from rect.
                            y_value = rect.get_height()
                            x_value = rect.get_x() + rect.get_width() / 2
                            label = "{:.1f}".format(y_value)
                            plt.annotate(
                                label,                      # Use `label` as label
                                (x_value, y_value),         # Place label at end of the bar
                                xytext=(0, space),          # Vertically shift label by `space`
                                textcoords="offset points", # Interpret `xytext` as offset in points
                                ha='center',                # Horizontally center label
                                va=va) 

                     plt.savefig(Output_file_directory2 + "/" + "Speed.png")
                     plt.close()

                 else:
                     ax = Metric_series1.plot(kind='bar',edgecolor ='k')
                     ax.set_title('Speed')
               #      ax.set_xlabel ('Outcome')
                     ax.set_ylabel('Speed(m/s)')
                     ax.set_xticklabels(Graph_amount1)
                     ax.tick_params(axis='x', rotation=0)
               #      ax.hold(False)
                     rects = ax.patches
                     space = 10
                     va='top'


                     for rect in rects:
                        # Get X and Y placement of label from rect.
                            y_value = rect.get_height()
                            x_value = rect.get_x() + rect.get_width() / 2
                            label = "{:.1f}".format(y_value)
                            plt.annotate(
                                label,                      # Use `label` as label
                                (x_value, y_value),         # Place label at end of the bar
                                xytext=(0, space),          # Vertically shift label by `space`
                                textcoords="offset points", # Interpret `xytext` as offset in points
                                ha='center',                # Horizontally center label
                                va=va) 

                     plt.savefig(Output_file_directory2 + "/" + "Speed.png")
                     plt.close()

        ########################
                   
                 width=1/1.5
                 plt.figure #(figsize=(10,8))
                 if len(Tag_dict) ==1:
                     n_groups = 2  #mins
                     fig, ax = plt.subplots()
                    # ax.hold(False)
                     index = np.arange(n_groups)
                     bar_width = 1
                     opacity = 1
                     rects2 = plt.bar(0, Metric_series2[0],color='orange',width=bar_width,alpha=opacity,edgecolor ='k' )
                     rects3 = plt.bar(1+bar_width, Metric_series2[1],color='b',width=bar_width,alpha=opacity,edgecolor ='k' )
                #     plt.xlabel('Outcome')
                     plt.ylabel('Acceleration (m/s)')
                     plt.title('Acceleration')
                     plt.xticks(np.arange(3),("Av.Accel","","Max.Accel"))
                     plt.tight_layout()
                     rects = ax.patches
                     space = 10
                     va='top'


                     for rect in rects:
                        # Get X and Y placement of label from rect.
                            y_value = rect.get_height()
                            x_value = rect.get_x() + rect.get_width() / 2
                            label = "{:.1f}".format(y_value)
                            plt.annotate(
                                label,                      # Use `label` as label
                                (x_value, y_value),         # Place label at end of the bar
                                xytext=(0, space),          # Vertically shift label by `space`
                                textcoords="offset points", # Interpret `xytext` as offset in points
                                ha='center',                # Horizontally center label
                                va=va) 

                     plt.savefig(Output_file_directory2 + "/" + "Acceleration.png")
                     plt.close()

                 else:
                     ax = Metric_series2.plot(kind='bar',edgecolor ='k')
                     ax.set_title('Acceleration')
                #     ax.set_xlabel ('Outcome')
                     ax.set_ylabel('Acceleration (m/s^)')
                     ax.set_xticklabels(Graph_amount2)
                     ax.tick_params(axis='x', rotation=0)
              #       ax.hold(False)
                     rects = ax.patches
                     space = 10
                     va='top'
                     for rect in rects:
                        # Get X and Y placement of label from rect.
                            y_value = rect.get_height()
                            x_value = rect.get_x() + rect.get_width() / 2
                            label = "{:.1f}".format(y_value)
                            plt.annotate(
                                label,                      # Use `label` as label
                                (x_value, y_value),         # Place label at end of the bar
                                xytext=(0, space),          # Vertically shift label by `space`
                                textcoords="offset points", # Interpret `xytext` as offset in points
                                ha='center',                # Horizontally center label
                                va=va) 
                   
                     plt.savefig(Output_file_directory2 + "/" + "Acceleration.png")
                     plt.close()

         ########################
                  
                 width=1/1.5
                 plt.figure #(figsize=(10,8))
                 if len(Tag_dict) ==1:
                     n_groups = 2  #mins
                     fig, ax = plt.subplots()
                #     ax.hold(False)
                     index = np.arange(n_groups)
                     bar_width = 1
                     opacity = 1
                     rects2 = plt.bar(0, Metric_series3[0],color='orange',width=bar_width,alpha=opacity,edgecolor ='k' )
                     rects3 = plt.bar(1+bar_width, Metric_series3[1],color='b',width=bar_width,alpha=opacity,edgecolor ='k' )
                 #    plt.xlabel('Outcome')
                     plt.ylabel('Work:rest (%)')
                     plt.title('Work:Rest percentage during game')
                     plt.xticks(np.arange(3),("Av.Work","","Max.Rest"))
                     plt.tight_layout()
                     rects = ax.patches
                     space = 10
                     va='top'


                     for rect in rects:
                        # Get X and Y placement of label from rect.
                            y_value = rect.get_height()
                            x_value = rect.get_x() + rect.get_width() / 2
                            label = "{:.1f}".format(y_value)
                            plt.annotate(
                                label,                      # Use `label` as label
                                (x_value, y_value),         # Place label at end of the bar
                                xytext=(0, space),          # Vertically shift label by `space`
                                textcoords="offset points", # Interpret `xytext` as offset in points
                                ha='center',                # Horizontally center label
                                va=va) 

                     plt.savefig(Output_file_directory2 + "/" + "Work_Rest.png")
                     plt.close()

                 else:
                     ax = Metric_series3.plot(kind='bar',edgecolor ='k')
                     ax.set_title('Work:Rest percentage during game')
                    # ax.set_xlabel ('Outcome')
                     ax.set_ylabel('Work:rest (%)')
                     ax.set_xticklabels(Graph_amount3)
                     ax.tick_params(axis='x', rotation=0)
                 #    ax.hold(False)
                     rects = ax.patches
                     space = 10
                     va='top' 
                     for rect in rects:
                        # Get X and Y placement of label from rect.
                            y_value = rect.get_height()
                            x_value = rect.get_x() + rect.get_width() / 2
                            label = "{:.1f}".format(y_value)
                            plt.annotate(
                                label,                      # Use `label` as label
                                (x_value, y_value),         # Place label at end of the bar
                                xytext=(0, space),          # Vertically shift label by `space`
                                textcoords="offset points", # Interpret `xytext` as offset in points
                                ha='center',                # Horizontally center label
                                va=va) 

                     plt.savefig(Output_file_directory2 + "/" + "Work_Rest.png")
                     plt.close()
                 
    ########################   
                 n_groups = 14  #mins
                 fig, ax = plt.subplots()
                 #ax.hold(False)
                 index = np.arange(n_groups)
                 bar_width = 0.35
                 opacity = 0.8
                 rects1 = plt.bar(index, Metric5[0:-1], bar_width,alpha=opacity,color='r',label='Rest <2 m/s', edgecolor ='k' )             
                 rects2 = plt.bar(index, Metric4[0:-1], bottom=Metric5[0:-1],color='k',width=bar_width,alpha=opacity,label='Work >2 m/s',edgecolor ='k' )
                 
                 rects8 = plt.bar(index+bar_width, Metric6[0:-1],color='b',width=bar_width,alpha=opacity,label='Zone 1: 0-20 %',edgecolor ='k' )            
                 rects9 = plt.bar(index+bar_width, Metric7[0:-1], bottom=Metric6[0:-1],color='g',width=bar_width,alpha=opacity,label='Zone 2: 20-40 %',edgecolor ='k' )             
                 rects10 = plt.bar(index+bar_width, Metric8[0:-1], bottom=Metric6[0:-1]+Metric7[0:-1],color='y',width=bar_width,alpha=opacity,label='Zone 3: 40-60 %',edgecolor ='k' )
                 rects11 = plt.bar(index+bar_width, Metric9[0:-1], bottom=Metric6[0:-1]+Metric7[0:-1]+Metric8[0:-1],color='m',width=bar_width,alpha=opacity,label='Zone 4: 60-80 %',edgecolor ='k' )
                 rects12 = plt.bar(index+bar_width, Metric10[0:-1], bottom=Metric6[0:-1]+Metric7[0:-1]+Metric8[0:-1]+Metric9[:-1],color='r',width=bar_width,alpha=opacity,label='Zone 5: 80-100 %',edgecolor ='k' )

                 ymin=0
                 ymax=60
                 plt.xlabel('Minute')
                 plt.ylabel('Work:Rest (s)')
                 plt.title('Work:rest Ratios')
                 plt.xticks(index, ('1', '2', '3', '4','5', '6', '7', '8','9', '10', '11', '12','13', '14'))
                 ax.set_ylim([ymin,ymax])
                 plt.savefig(Output_file_directory2 + "/" + "Work_Rest_min.png")
                 plt.close()
##################################################################################################################

                 Tag_Text=str(Player_Tag[i][0])
                 ##################################################################################################################
                 c1=canvas.Canvas(Output_file_directory2 + "/" + Process_File.data()+ Tag_Text + ".pdf")

                 Background='Background.png'
                 c1.drawImage(Background,0,0, width=595, height=845)
                 c1.setFont("Helvetica-Bold", 20,leading=None)
                 c1.drawString(190,750," Peformance Outcomes")
                 c1.setFont("Helvetica-Bold", 15,leading=None)        
                 c1.drawString(300,725,Tag_Text)
 
                 c1.setFillColor(white)
                 Court_Distance_Rectangle= c1.rect(235,450,120,20,fill=True)
                 
                 c1.setFillColor(black)
                 c1.setFont("Helvetica-Bold", 8,leading=None)
                 c1.drawString(236,457,"Total Distance (m):")

              #   print(Distance_max[i])
                 Distance_max3=str(Distance_max[i])
                 c1.setFillColor(black)
                 c1.setFont("Helvetica-Bold", 12,leading=None)
                 c1.drawString(315,457,Distance_max3)
                 c1.setFillColor(white)
                 Court_Speed_Rectangle= c1.rect(50,280,150,150,fill=True)
                 c1.setFillColor(white)
                 Court_Acceleration_Rectangle= c1.rect(225,280,150,150,fill=True)
                 c1.setFillColor(white)
                 Court_Work_Rectangle= c1.rect(405,280,150,150,fill=True)

                 c1.setFillColor(black)
                 c1.setFont("Helvetica-Bold", 10,leading=None)
                 c1.drawString(260,600,"Add video file")
                 Speed_image=(Output_file_directory2 + "/Speed.png")
                 c1.drawImage(Speed_image,49,279, width=162, height=152)
                 Acceleration_image=(Output_file_directory2 + "/Acceleration.png")
                 c1.drawImage(Acceleration_image,224,279, width=162, height=152)
                 Work_image=(Output_file_directory2 + "/Work_Rest.png")
                 c1.drawImage(Work_image,404,279, width=162, height=152)
                 WR_Graph_image=(Output_file_directory2 + "/Work_Rest_min.png")
                 c1.drawImage(WR_Graph_image,100,500, width=400, height=220)
                 Intensity_image1= "intensity1.png"
                 c1.drawImage(Intensity_image1,100,480, width=190, height=15)
                 c1.showPage()
                 c1.save()
                 c1=[]
      
###create a save to PDF check box for game data
         
         while self.completed <100:
            self.completed += 1
            self.progressBar.setValue (self.completed)
        
###########################################################
                 
    def Load_All_Files_Results(self):
        global Output_file_directory2; global file_directory; global Output_file_directory;
        global file_directory;global Output_file_directory; global outputfile;global File_list;global File_list_2; global all_files_2; global all_files
        
        self.File_List_Text_Results.clear()
        all_files_2=os.listdir(Output_file_directory2)          
        for index in range(len(all_files_2)):
           File_list_2=all_files_2[index]
           self.File_List_Text_Results.addItem(File_list_2)
          



    def View_Data(self):
         global Output_file_directory2; global file_directory; global Output_file_directory;
         global file_directory;global Output_file_directory; global outputfile;global File_list;global File_list_2; global all_files_2; global all_files; global Frames_persecond_round
         Time2=[];Absolute_Coordinate_Change=[];Total_Distance=[];Speed=[];Velocity=[];Acceleration=[]
         fivem_max=[];tenm_max=[];fifteenm_max=[];twentym_max=[];Total_Time=[];Total_Max=[];Total_Mean=[];
         
         View_File=self.File_List_Text_Results.selectedIndexes()[0]
         open_file_2=Output_file_directory2 + "/" + View_File.data()
         Tag_sheet_map2 = pandas.read_excel(open_file_2, sheet_name=None) ####long time for operation
         Tag_dict2=list(Tag_sheet_map2.items())
         for i in range (len(Tag_dict2)):
            Time2.append(Tag_dict2[i][1]["Time"])   #(Time=column, Time[0]=row)
           # Absolute_Coordinate_Change.append(Tag_dict2[i][1]["Absolute Coordinate Change(mm)"])
            Total_Distance.append(Tag_dict2[i][1]["Total Distance (m)"])
            Velocity.append(Tag_dict2[i][1]["Velocity (m/s)"])
            Acceleration.append(Tag_dict2[i][1]["Acceleration (m/s)"])
            fivem_max.append(Tag_dict2[i][1]["5m"])
            tenm_max.append(Tag_dict2[i][1]["10m"])
            fifteenm_max.append(Tag_dict2[i][1]["15m"])
            twentym_max.append(Tag_dict2[i][1]["20m"])
            Total_Time.append(Tag_dict2[i][1]["Total Time"])
            Total_Max.append(Tag_dict2[i][1]["Max"])
            Total_Mean.append(Tag_dict2[i][1]["Mean"])

 
         Time2=np.array(Time2,dtype=np.float64)
         #Absolute_Coordinate_Change=np.array(Absolute_Coordinate_Change,dtype=np.float64)
         Total_Distance=np.array(Total_Distance,dtype=np.float64)
         Velocity=np.array(Velocity,dtype=np.float64)
         Acceleration=np.array(Acceleration,dtype=np.float64)
         fivem_max=np.array(fivem_max,dtype=np.float64)
         tenm_max=np.array(tenm_max,dtype=np.float64)
         fifteenm_max=np.array(fifteenm_max,dtype=np.float64)
         twentym_max=np.array(twentym_max,dtype=np.float64)
         Total_Time=np.array(Total_Time,dtype=np.float64)
         Total_Max=np.array(Total_Max,dtype=np.float64)
         Total_Mean=np.array(Total_Mean,dtype=np.float64)         


         vel_5=str(fivem_max[0][1])
         Acc_5=str(fivem_max[0][2])
         Time_5=str(fivem_max[0][3])
         vel_10=str(tenm_max[0][1])
         Acc_10=str(tenm_max[0][2])
         Time_10=str(tenm_max[0][3])
         vel_15=str(fifteenm_max[0][1])
         Acc_15=str(fifteenm_max[0][2])
         Time_15=str(fifteenm_max[0][3])
         vel_20=str(twentym_max[0][1])
         Acc_20=str(twentym_max[0][2])
         Time_20=str(twentym_max[0][3])
         Total_Time=str(Total_Time[0][3])
         Total_Vel_Max=str(Total_Max[0][1])
         Total_Acc_Max=str(Total_Max[0][2])
         Total_Vel_Mean=str(Total_Mean[0][1])
         Total_Acc_Mean=str(Total_Mean[0][2])
         
         time_count2=len(Total_Distance[0])   
         count_all2=list(range(1,time_count2+1,1))
       
         check1=0
         check2=0
         check3=0
         if self.parent_tabWidget.currentIndex()==2:             
            if self.Drill_twenty_checkbox.isChecked():
                 check1=1
            if self.illinois_checkbox.isChecked():
                check2=1
            if self.YoYo_checkbox.isChecked():
                check3=1
            if check1==1 and check2 ==1:
                messagebox.showinfo('Error', 'Only Choose One Drill')
            elif check1==1 and check3 ==1:
                messagebox.showinfo('Error', 'Only Choose One Drill')
            elif check2==1 and check3 ==1:
                messagebox.showinfo('Error', 'Only Choose One Drill')
            elif check1 ==1 and check2 ==0 and check3 ==0:                        
                        self.tableWidget.setItem(1,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(2,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(3,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(0,1, QTableWidgetItem(""))
                        self.tableWidget.setItem(0,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(0,3, QTableWidgetItem(""))
                        self.tableWidget.setItem(0,4, QTableWidgetItem(""))

                        self.tableWidget.setItem(4,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(6,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(7,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(8,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(9,0, QTableWidgetItem(""))

                        self.tableWidget.setItem(5,1, QTableWidgetItem(""))
                        self.tableWidget.setItem(5,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(5,3, QTableWidgetItem(""))
                        self.tableWidget.setItem(4,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(4,3, QTableWidgetItem(""))
                        
                        self.tableWidget.setItem(1,0, QTableWidgetItem("Time"))
                        self.tableWidget.setItem(2,0, QTableWidgetItem("Velocity"))
                        self.tableWidget.setItem(3,0, QTableWidgetItem("Acceleration"))
                        self.tableWidget.setItem(0,1, QTableWidgetItem("5m"))
                        self.tableWidget.setItem(0,2, QTableWidgetItem("10m"))
                        self.tableWidget.setItem(0,3, QTableWidgetItem("15m"))
                        self.tableWidget.setItem(0,4, QTableWidgetItem("20m"))

                        self.tableWidget.setItem(4,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(6,0, QTableWidgetItem("Time"))
                        self.tableWidget.setItem(7,0, QTableWidgetItem("Velocity"))
                        self.tableWidget.setItem(8,0, QTableWidgetItem("Acceleration"))
                       # self.tableWidget.setItem(9,0, QTableWidgetItem("Speed"))

                        self.tableWidget.setItem(5,1, QTableWidgetItem("Total"))
                        self.tableWidget.setItem(5,2, QTableWidgetItem("Max"))
                        self.tableWidget.setItem(5,3, QTableWidgetItem("Average"))
                        
                        self.tableWidget.setItem(1,1, QTableWidgetItem(Time_5))
                        self.tableWidget.setItem(1,2, QTableWidgetItem(Time_10))
                        self.tableWidget.setItem(1,3, QTableWidgetItem(Time_15))
                        self.tableWidget.setItem(1,4, QTableWidgetItem(Time_20))
                        self.tableWidget.setItem(2,1, QTableWidgetItem(vel_5))
                        self.tableWidget.setItem(2,2, QTableWidgetItem(vel_10))
                        self.tableWidget.setItem(2,3, QTableWidgetItem(vel_15))
                        self.tableWidget.setItem(2,4, QTableWidgetItem(vel_20))
                        self.tableWidget.setItem(3,1, QTableWidgetItem(Acc_5))
                        self.tableWidget.setItem(3,2, QTableWidgetItem(Acc_10))
                        self.tableWidget.setItem(3,3, QTableWidgetItem(Acc_15))
                        self.tableWidget.setItem(3,4, QTableWidgetItem(Acc_20))

                        self.tableWidget.setItem(6,1, QTableWidgetItem(Total_Time))
                        self.tableWidget.setItem(7,2, QTableWidgetItem(Total_Vel_Max))
                        self.tableWidget.setItem(7,3, QTableWidgetItem(Total_Vel_Mean))
                        self.tableWidget.setItem(8,2, QTableWidgetItem(Total_Acc_Max))
                        self.tableWidget.setItem(8,3, QTableWidgetItem(Total_Acc_Mean))
                       # self.tableWidget.setItem(9,2, QTableWidgetItem(Speed_Max))
                       # self.tableWidget.setItem(9,3, QTableWidgetItem(Speed_Mean))
                        
                        
                        

                        self.axes = self.figure.add_subplot(311) 
                        self.axes2 = self.figure.add_subplot(312) 
                        self.axes3 = self.figure.add_subplot(313) 
                        # We want the axes cleared every time plot() is called
                        self.axes.hold(False)
                        self.axes2.hold(False)
                        self.axes3.hold(False)
                        self.axes.plot(Velocity[0][:], '-')
                        self.axes.set_title('Velocity')
                        self.axes.set_xlabel('Time')
                        self.axes.set_ylabel('Velocity (m/s)')
                        self.axes2.plot(Acceleration[0][:], '-')
                        self.axes2.set_title('Acceleration')
                        self.axes2.set_xlabel('Time')
                        self.axes2.set_ylabel('Acceleration (m/s)')
                        self.axes3.plot(Total_Distance[0][:], '-')
                        self.axes3.set_title('Distance')
                        self.axes3.set_xlabel('Time')
                        self.axes3.set_ylabel('Meters')
                        plt.tight_layout()
                        self.canvas.draw()
                       
            elif check2 ==1 and check1 ==0 and check3 ==0:                      
                        self.tableWidget.setItem(1,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(2,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(3,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(0,1, QTableWidgetItem(""))
                        self.tableWidget.setItem(0,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(0,3, QTableWidgetItem(""))
                        self.tableWidget.setItem(0,4, QTableWidgetItem(""))

                        self.tableWidget.setItem(4,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(6,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(7,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(8,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(9,0, QTableWidgetItem(""))

                        self.tableWidget.setItem(5,1, QTableWidgetItem(""))
                        self.tableWidget.setItem(5,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(5,3, QTableWidgetItem(""))

                        self.tableWidget.setItem(1,1, QTableWidgetItem(""))
                        self.tableWidget.setItem(1,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(1,3, QTableWidgetItem(""))
                        self.tableWidget.setItem(1,4, QTableWidgetItem(""))
                        self.tableWidget.setItem(2,1, QTableWidgetItem(""))
                        self.tableWidget.setItem(2,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(2,3, QTableWidgetItem(""))
                        self.tableWidget.setItem(2,4, QTableWidgetItem(""))
                        self.tableWidget.setItem(3,1, QTableWidgetItem(""))
                        self.tableWidget.setItem(3,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(3,3, QTableWidgetItem(""))
                        self.tableWidget.setItem(3,4, QTableWidgetItem(""))

                        self.tableWidget.setItem(6,1, QTableWidgetItem(""))
                        self.tableWidget.setItem(7,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(7,3, QTableWidgetItem(""))
                        self.tableWidget.setItem(8,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(8,3, QTableWidgetItem(""))
                        self.tableWidget.setItem(9,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(9,3, QTableWidgetItem(""))

                        self.tableWidget.setItem(1,0, QTableWidgetItem("Time"))
                        self.tableWidget.setItem(2,0, QTableWidgetItem("Velocity"))
                        self.tableWidget.setItem(3,0, QTableWidgetItem("Acceleration"))
                    #    self.tableWidget.setItem(4,0, QTableWidgetItem("Speed"))
                        self.tableWidget.setItem(0,1, QTableWidgetItem("Total"))
                        self.tableWidget.setItem(0,2, QTableWidgetItem("Max"))
                        self.tableWidget.setItem(0,3, QTableWidgetItem("Average"))

                        self.tableWidget.setItem(1,1, QTableWidgetItem(Total_Time))
                        self.tableWidget.setItem(2,2, QTableWidgetItem(Total_Vel_Max))
                        self.tableWidget.setItem(2,3, QTableWidgetItem(Total_Vel_Mean))
                        self.tableWidget.setItem(3,2, QTableWidgetItem(Total_Acc_Max))
                        self.tableWidget.setItem(3,3, QTableWidgetItem(Total_Acc_Mean))
                   #     self.tableWidget.setItem(4,2, QTableWidgetItem(Speed_Max))
                    #    self.tableWidget.setItem(4,3, QTableWidgetItem(Speed_Mean))
                                  
                        self.axes = self.figure.add_subplot(311) 
                        self.axes2 = self.figure.add_subplot(312) 
                        self.axes3 = self.figure.add_subplot(313) 
                        # We want the axes cleared every time plot() is called
                        self.axes.hold(False)
                        self.axes2.hold(False)
                        self.axes3.hold(False)
                        self.axes.plot(Velocity[0][:], 'r-')
                        self.axes.set_title('Velocity')
                        self.axes.set_xlabel('Time')
                        self.axes.set_ylabel('Velocity (m/s)')
                        self.axes2.plot(Acceleration[0][:], 'r-')
                        self.axes2.set_title('Acceleration')
                        self.axes2.set_xlabel('Time')
                        self.axes2.set_ylabel('Acceleration (m/s)')
                        self.axes3.plot(Total_Distance[0][:], '-')
                        self.axes3.set_title('Distance')
                        self.axes3.set_xlabel('Time')
                        self.axes3.set_ylabel('Meters')
                        plt.tight_layout()
                        self.canvas.draw()
                  
            elif check3 ==1 and check1 ==0 and check2 ==0:
                        self.tableWidget.setItem(1,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(2,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(3,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(0,1, QTableWidgetItem(""))
                        self.tableWidget.setItem(0,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(0,3, QTableWidgetItem(""))
                        self.tableWidget.setItem(0,4, QTableWidgetItem(""))

                        self.tableWidget.setItem(4,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(6,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(7,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(8,0, QTableWidgetItem(""))
                        self.tableWidget.setItem(9,0, QTableWidgetItem(""))

                        self.tableWidget.setItem(5,1, QTableWidgetItem(""))
                        self.tableWidget.setItem(5,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(5,3, QTableWidgetItem(""))

                        self.tableWidget.setItem(1,1, QTableWidgetItem(""))
                        self.tableWidget.setItem(1,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(1,3, QTableWidgetItem(""))
                        self.tableWidget.setItem(1,4, QTableWidgetItem(""))
                        self.tableWidget.setItem(2,1, QTableWidgetItem(""))
                        self.tableWidget.setItem(2,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(2,3, QTableWidgetItem(""))
                        self.tableWidget.setItem(2,4, QTableWidgetItem(""))
                        self.tableWidget.setItem(3,1, QTableWidgetItem(""))
                        self.tableWidget.setItem(3,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(3,3, QTableWidgetItem(""))
                        self.tableWidget.setItem(3,4, QTableWidgetItem(""))

                        self.tableWidget.setItem(6,1, QTableWidgetItem(""))
                        self.tableWidget.setItem(7,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(7,3, QTableWidgetItem(""))
                        self.tableWidget.setItem(8,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(8,3, QTableWidgetItem(""))
                        self.tableWidget.setItem(9,2, QTableWidgetItem(""))
                        self.tableWidget.setItem(9,3, QTableWidgetItem(""))

                        self.tableWidget.setItem(1,0, QTableWidgetItem("Time"))
                        self.tableWidget.setItem(2,0, QTableWidgetItem("Velocity"))
                        self.tableWidget.setItem(3,0, QTableWidgetItem("Acceleration"))
                     #   self.tableWidget.setItem(4,0, QTableWidgetItem("Speed"))
                        self.tableWidget.setItem(0,1, QTableWidgetItem("Total"))
                        self.tableWidget.setItem(0,2, QTableWidgetItem("Max"))
                        self.tableWidget.setItem(0,3, QTableWidgetItem("Average"))

                        self.tableWidget.setItem(1,1, QTableWidgetItem(Total_Time))
                        self.tableWidget.setItem(2,2, QTableWidgetItem(Total_Vel_Max))
                        self.tableWidget.setItem(2,3, QTableWidgetItem(Total_Vel_Mean))
                        self.tableWidget.setItem(3,2, QTableWidgetItem(Total_Acc_Max))
                        self.tableWidget.setItem(3,3, QTableWidgetItem(Total_Acc_Mean))
                     #   self.tableWidget.setItem(4,2, QTableWidgetItem(Speed_Max))
                      #  self.tableWidget.setItem(4,3, QTableWidgetItem(Speed_Mean))
                        
                        
                        self.axes = self.figure.add_subplot(311) 
                        self.axes2 = self.figure.add_subplot(312) 
                        self.axes3 = self.figure.add_subplot(313) 
                        # We want the axes cleared every time plot() is called
                        self.axes.hold(False)
                        self.axes2.hold(False)
                        self.axes3.hold(False)
                        self.axes.plot(Velocity[0][:], 'g-')
                        self.axes.set_title('Velocity')
                        self.axes.set_xlabel('Time')
                        self.axes.set_ylabel('Velocity (m/s)')
                        self.axes2.plot(Acceleration[0][:], 'g-')
                        self.axes2.set_title('Acceleration')
                        self.axes2.set_xlabel('Time')
                        self.axes2.set_ylabel('Acceleration (m/s)')
                        self.axes3.plot(Total_Distance[0][:], '-')
                        self.axes3.set_title('Distance')
                        self.axes3.set_xlabel('Time')
                        self.axes3.set_ylabel('Meters')
                        plt.tight_layout()
                        self.canvas.draw()

    #################################################################################

       # place where the MQTT is looking



    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()        
    sys.exit(app.exec_())

