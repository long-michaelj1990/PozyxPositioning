# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'POZYX_Processing.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!
from tkinter import messagebox
import tkinter as tk
from tkinter import filedialog

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog

import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
import glob, os
from xlrd import open_workbook
from xlutils.copy import copy
import pandas 
from collections import Counter
import numpy
from numpy import *
import scipy
from scipy import signal
from scipy.signal import butter, lfilter, freqz, filtfilt
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d
from array import array
import time
import collections
from itertools import accumulate

import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Image
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.colors import PCMYKColor, PCMYKColorSep, Color, black, blue, red, white

class Ui_Processing_Window(object):    
    def setupUi(self, Processing_Window):
        Processing_Window.setObjectName("Processing_Window")
        Processing_Window.resize(673, 412)
        Processing_Window.setAutoFillBackground(True)
        self.Close_Button = QtWidgets.QDialogButtonBox(Processing_Window)
        self.Close_Button.setGeometry(QtCore.QRect(310, 380, 341, 32))
        self.Close_Button.setOrientation(QtCore.Qt.Horizontal)
        self.Close_Button.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.Close_Button.setObjectName("Close_Button")
##################### close all
        self.Close_Button.clicked.connect(self.Close)
##################### 
        self.Set_Directory_Button = QtWidgets.QPushButton(Processing_Window)
        self.Set_Directory_Button.setGeometry(QtCore.QRect(130, 10, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.Set_Directory_Button.setFont(font)
        self.Set_Directory_Button.setAutoDefault(False)
        self.Set_Directory_Button.setDefault(True)
        self.Set_Directory_Button.setFlat(False)
        self.Set_Directory_Button.setObjectName("Set_Directory_Button")
##################### Set Directory
        self.Set_Directory_Button.clicked.connect(self.Set_Directory)
#####################        
        self.Directory_Input_Text = QtWidgets.QLineEdit(Processing_Window)
        self.Directory_Input_Text.setGeometry(QtCore.QRect(10, 20, 113, 21))
        self.Directory_Input_Text.setObjectName("Directory_Input_Text")
#######################
        self.File_List_Text = QtWidgets.QListWidget(Processing_Window)
        self.File_List_Text.setGeometry(QtCore.QRect(10, 110, 171, 201))
        self.File_List_Text.setObjectName("File_List_Text")
        self.Load_Files_Button = QtWidgets.QPushButton(Processing_Window)
        self.Load_Files_Button.setGeometry(QtCore.QRect(190, 110, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.Load_Files_Button.setFont(font)
        self.Load_Files_Button.setAutoDefault(False)
        self.Load_Files_Button.setDefault(True)
        self.Load_Files_Button.setFlat(False)
        self.Load_Files_Button.setObjectName("Load_Files_Button")
##################### load all files
        self.Load_Files_Button.clicked.connect(self.Load_All_Files)
#####################
        self.Output_File_Location_Text = QtWidgets.QLineEdit(Processing_Window)
        self.Output_File_Location_Text.setGeometry(QtCore.QRect(10, 60, 113, 21))
        self.Output_File_Location_Text.setObjectName("Output_File_Location_Text")
        self.Set_Output_File_Location = QtWidgets.QPushButton(Processing_Window)
        self.Set_Output_File_Location.setGeometry(QtCore.QRect(130, 50, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.Set_Output_File_Location.setFont(font)
        self.Set_Output_File_Location.setAutoDefault(False)
        self.Set_Output_File_Location.setDefault(True)
        self.Set_Output_File_Location.setFlat(False)
        self.Set_Output_File_Location.setObjectName("Set_Output_File_Location")
##################### Set output location
        self.Set_Output_File_Location.clicked.connect(self.Set_Output_location)        
#####################
        self.Process_File_Button = QtWidgets.QPushButton(Processing_Window)
        self.Process_File_Button.setGeometry(QtCore.QRect(10, 330, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.Process_File_Button.setFont(font)
        self.Process_File_Button.setAutoDefault(False)
        self.Process_File_Button.setDefault(True)
        self.Process_File_Button.setFlat(False)
        self.Process_File_Button.setObjectName("Process_File_Button")
##################### processing button
        self.Process_File_Button.clicked.connect(self.Process)
#####################
        self.Guide_Text = QtWidgets.QTextBrowser(Processing_Window)
        self.Guide_Text.setGeometry(QtCore.QRect(410, 10, 231, 171))
        self.Guide_Text.setAutoFillBackground(True)
        self.Guide_Text.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.Guide_Text.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Guide_Text.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Guide_Text.setObjectName("Guide_Text")
        self.progressBar = QtWidgets.QProgressBar(Processing_Window)
        self.progressBar.setGeometry(QtCore.QRect(130, 330, 221, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
#########################        
        self.Filter_Text = QtWidgets.QTextBrowser(Processing_Window)
        self.Filter_Text.setGeometry(QtCore.QRect(200, 210, 91, 41))
        self.Filter_Text.setAutoFillBackground(True)
        self.Filter_Text.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.Filter_Text.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Filter_Text.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Filter_Text.setObjectName("Filter_Text")
        self.Window_text = QtWidgets.QTextBrowser(Processing_Window)
        self.Window_text.setGeometry(QtCore.QRect(440, 200, 91, 41))
        self.Window_text.setAutoFillBackground(True)
        self.Window_text.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.Window_text.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Window_text.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Window_text.setObjectName("Window_text")
#########################
        self.Position_checkbox = QtWidgets.QCheckBox(Processing_Window)
        self.Position_checkbox.setGeometry(QtCore.QRect(360, 340, 70, 17))
        self.Position_checkbox.setObjectName("Position_checkbox")
######################
        self.Position_checkbox.stateChanged.connect(self.Position_graph)
######################            
        self.Speed_checkbox = QtWidgets.QCheckBox(Processing_Window)
        self.Speed_checkbox.setGeometry(QtCore.QRect(430, 340, 70, 17))
        self.Speed_checkbox.setObjectName("Speed_checkbox")
######################
        self.Speed_checkbox.stateChanged.connect(self.Speed_graph)
###################### 
        self.Distance_checkbox = QtWidgets.QCheckBox(Processing_Window)
        self.Distance_checkbox.setGeometry(QtCore.QRect(490, 340, 70, 17))
        self.Distance_checkbox.setObjectName("Distance_checkbox")
######################
        self.Distance_checkbox.stateChanged.connect(self.Distance_graph)
###################### 
        self.graph_Text = QtWidgets.QTextBrowser(Processing_Window)
        self.graph_Text.setGeometry(QtCore.QRect(420, 320, 91, 41))
        self.graph_Text.setAutoFillBackground(True)
        self.graph_Text.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.graph_Text.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.graph_Text.setFrameShadow(QtWidgets.QFrame.Plain)
        self.graph_Text.setObjectName("graph_Text")
##########################        
        self.Acceleration_checkbox_ = QtWidgets.QCheckBox(Processing_Window)
        self.Acceleration_checkbox_.setGeometry(QtCore.QRect(360, 360, 81, 17))
        self.Acceleration_checkbox_.setObjectName("Acceleration_checkbox_")
######################
        self.Acceleration_checkbox_.stateChanged.connect(self.Acceleration_graph)
###################### ## Actually Velocity
        self.Work_checkbox = QtWidgets.QCheckBox(Processing_Window) 
        self.Work_checkbox.setGeometry(QtCore.QRect(490, 360, 81, 17))
        self.Work_checkbox.setObjectName("Work_checkbox")
######################
        self.Work_checkbox.stateChanged.connect(self.Work_graph)
######################
        self.Moving_Average_Radio = QtWidgets.QRadioButton(Processing_Window)
        self.Moving_Average_Radio.setGeometry(QtCore.QRect(200, 240, 101, 17))
        self.Moving_Average_Radio.setObjectName("Moving_Average_Radio")
##################### moving average button
        self.Moving_Average_Radio.clicked.connect(self.Moving_average)
#####################
#####################
        self.Window_Slider = QtWidgets.QSlider(Processing_Window)
        self.Window_Slider.setGeometry(QtCore.QRect(310, 230, 311, 22))
        self.Window_Slider.setMaximum(201)
        self.Window_Slider.setMinimum(1)
        self.Window_Slider.setProperty("value", 1)
        self.Window_Slider.setTickInterval(10)
        self.Window_Slider.setSingleStep(20)        
        self.Window_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Window_Slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Window_Slider.setObjectName("Window_Slider")
##################### Window slider
        self.Window_Slider.sliderPressed.connect(self.Window)
        self.Window_Slider.sliderMoved.connect(self.Window)
#####################
        self.Window_text.setGeometry(QtCore.QRect(440, 200, 91, 41))
        self.Window_text.setAutoFillBackground(True)
        self.Window_text.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.Window_text.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Window_text.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Window_text.setObjectName("Window_text")
        self.Window_Text_Box = QtWidgets.QLineEdit(Processing_Window)
        self.Window_Text_Box.setGeometry(QtCore.QRect(620, 230, 31, 21))
        self.Window_Text_Box.setObjectName("Window_Text_Box")
        
        self.graph_Text.raise_()
        self.Window_text.raise_()
        self.Filter_Text.raise_()
        self.Close_Button.raise_()
        self.Set_Directory_Button.raise_()
        self.Directory_Input_Text.raise_()
        self.File_List_Text.raise_()
        self.Load_Files_Button.raise_()
        self.Output_File_Location_Text.raise_()
        self.Set_Output_File_Location.raise_()
        self.Process_File_Button.raise_()
        self.Guide_Text.raise_()
        self.progressBar.raise_()
        self.Position_checkbox.raise_()
        self.Speed_checkbox.raise_()
        self.Work_checkbox.raise_()
        self.Distance_checkbox.raise_()
        self.Acceleration_checkbox_.raise_()
        self.Window_Text_Box.raise_()
        self.Moving_Average_Radio.raise_()
        self.Window_Slider.raise_()
     
        
        self.retranslateUi(Processing_Window)
        self.Set_Directory_Button.clicked.connect(self.Set_Directory_Button.showMenu)
        QtCore.QMetaObject.connectSlotsByName(Processing_Window)
        

    def retranslateUi(self, Processing_Window):
        _translate = QtCore.QCoreApplication.translate
        Processing_Window.setWindowTitle(_translate("Processing_Window", "Dialog"))
        self.Set_Directory_Button.setText(_translate("Processing_Window", "Set File Location"))
        self.Load_Files_Button.setText(_translate("Processing_Window", "Load Files"))
        self.Set_Output_File_Location.setText(_translate("Processing_Window", "Set Output File Location"))
        self.Process_File_Button.setText(_translate("Processing_Window", "Process File"))
        self.Guide_Text.setHtml(_translate("Processing_Window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">                 <span style=\" font-size:12pt; font-weight:600; text-decoration: underline;\">Guide</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600; text-decoration: underline;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. Open location where files are located</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. Set the location for processed files</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3. load in all files to be processed</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4. Select file to be processed</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">5. Select Filter</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">6. Select graph(s) to be view</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">7. Process File</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.Moving_Average_Radio.setText(_translate("Processing_Window", "Polynomial (LS)"))
        self.Filter_Text.setHtml(_translate("Processing_Window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; text-decoration: underline;\">Filter</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600; text-decoration: underline;\"><br /></p></body></html>"))
        self.Window_text.setHtml(_translate("Processing_Window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; text-decoration: underline;\">Window</span></p></body></html>"))
        self.Position_checkbox.setText(_translate("Processing_Window", "Postion"))
        self.Speed_checkbox.setText(_translate("Processing_Window", "Speed"))
        self.Distance_checkbox.setText(_translate("Processing_Window", "Distance"))
        self.Work_checkbox.setText(_translate("Processing_Window", "Velocity"))
        self.graph_Text.setHtml(_translate("Processing_Window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; text-decoration: underline;\">View Graphs</span></p></body></html>"))
        self.Acceleration_checkbox_.setText(_translate("Processing_Window", "Acceleration"))

    def Set_Directory (self):
        global file_directory
        file_directory = str(QFileDialog.getExistingDirectory())
        self.Directory_Input_Text.setText(file_directory)
    def Set_Output_location(self):
        global Output_file_directory
        Output_file_directory = str(QFileDialog.getExistingDirectory())
        self.Output_File_Location_Text.setText(Output_file_directory)
    def Load_All_Files(self):
        global file_directory;global Position_G;global Speed_G;global Distance_G;global Acceleration_G;global Metrics_G;global Work_G
        Position_G=0
        Speed_G=0
        Distance_G=0
        Acceleration_G = 0
        Work_G=0
        QListWidgetItem=0
        Metrics_G=0
        self.File_List_Text.clear()
        all_files=os.listdir(file_directory)        
               
        for index in range(len(all_files)):
           File_list=all_files[index]
           self.File_List_Text.addItem(File_list)

    def Close(self):
        Processing_Window.close()

    def Order(self):
        global order_slider
        order_slider=self.Order_Slider.value()
        order_slider1=str(order_slider)
        self.Order_Text_Box.setText(order_slider1)

    def Cuttoff(self):
        global cutoff_slider
        cutoff_slider=self.Cuttoff_slider.value()/10
        cutoff_slider1=str(cutoff_slider)
        self.Cutoff_Text_Box.setText(cutoff_slider1)

    def Window(self):
        global Window_slider
        Window_slider= self.Window_Slider.value()
        Window_slider=str(Window_slider)
        self.Window_Text_Box.setText(Window_slider)

    def Moving_average(self):
        global moving_average;global butterworth 
        moving_average=1
        butterworth=0
        

    def butter_lowpass2(self):
        global moving_average;global butterworth 
        moving_average=0
        butterworth=1

    def Position_graph(self):
        global Position_G
        if self.Position_checkbox.isChecked():
            Position_G=1
        else:
            Position_G=0
            
    def Speed_graph(self):
        global Speed_G
        if self.Speed_checkbox.isChecked():
            Speed_G=1
        else:
            Speed_G=0
            
    def Distance_graph(self):
        global Distance_G
        if self.Distance_checkbox.isChecked():
            Distance_G=1
        else:
            Distance_G=0
            
    def Acceleration_graph (self):
        global Acceleration_G
        if self.Acceleration_checkbox_.isChecked():
            Acceleration_G=1
        else:
            Acceleration_G=0
            
    def Work_graph(self):
        global Work_G
        if self.Work_checkbox.isChecked():
             Work_G =1
        else:
             Work_G =0
             

    def Process(self):
         global file_directory;global Output_file_directory;global butterworth;global order_slider;global cutoff_slider;global Window_slider;global low
         global Frames_persecond;global Distance_G;global Speed_G;global Position_G;global Work_G;global Tag_Amount;global GK_mass;global WD_mass
         global GD_mass;global C_mass;global GA_mass;global WA_mass;global GS_mass;global GK2_mass;global WD2_mass;global GD2_mass;global C2_mass
         global GA2_mass;global WA2_mass;global GS2_mass; global All_Mass; global Tag_Amount; global players

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
         
         players=[]       
         GK='GK'
         WD='WD'
         GD='GD'
         C='C'
         GA='GA'
         WA='WA'
         GS='GS'
         GK2='GK2'
         WD2='WD2'
         GD2='GD2'
         C2='C2'
         GA2='GA2'
         WA2='WA2'
         GS2='GS2'
         players.append([GK,WD,GD,C,GA,WA,GS,GK2,WD2,GD2,C2,GA2,WA2,GS2]) #accessc via[0][#]

         Process_File=self.File_List_Text.selectedIndexes()[0]
         open_file=file_directory + "/" + Process_File.data()
    
######################## Create Excel Output File ################################################
            
         outputfile= xlsxwriter.Workbook(Output_file_directory + "/" + "Processed_" + Process_File.data()) 

         worksheet_Coordinates=outputfile.add_worksheet('Coordinates') ##create excel sheets
         worksheet_Acceleration=outputfile.add_worksheet('Acceleration')
         worksheet_LinearAcceleration=outputfile.add_worksheet('LinearAcceleration')        
#####  excel sheet
         worksheet_Coordinates.write("A1","Time")   
         worksheet_Coordinates.write("B1","X Coordinate Change(mm)")
         worksheet_Coordinates.write("C1","Y Coordinate Change(mm)")
         worksheet_Coordinates.write("D1","Z Coordinate Change(mm)")
         worksheet_Coordinates.write("E1","Flag")
         worksheet_Coordinates.write("G1","Absolute Coordinate Change(m)")
         worksheet_Coordinates.write("H1","Total Distance (m)")
         worksheet_Coordinates.write("I1","Speed (m/s)")
         worksheet_Coordinates.write("J1","Cumulative Work (J)")
         worksheet_Coordinates.write("K1"," Work (J)")
         worksheet_Acceleration.write("A1","Time")
         worksheet_Acceleration.write("B1","Absolute Acceleration")
         worksheet_LinearAcceleration.write("A1","Time")
         worksheet_LinearAcceleration.write("B1","X")
         worksheet_LinearAcceleration.write("C1","Y")
         worksheet_LinearAcceleration.write("D1","Z")
         
         while self.completed <31:
               self.completed += 1
         self.progressBar.setValue (self.completed)
         self.progressBar.setValue (self.start)

         t3=time.time() 
         Tag_sheet_map = pandas.read_excel(open_file, sheet_name=None) ####long time for operation
         t4=time.time()
         total2=t4-t3


         Tag_dict=list(Tag_sheet_map.items())
         Time=[]
         Tag_X=[]          
         Tag_Y=[]
         Tag_X_filtered=[]
         Tag_Y_filtered=[]
         b=[]
         a=[]
         Speed=[]
         count_all = []
         Total_Work=[]
###################### Get Data ###########################################
         
         for i in range (len(Tag_dict)):
            Time.append(Tag_dict[i][1]["Time"])   #(Time=column, Time[0]=row)
            Time[i].fillna(method='ffill', inplace =True)
            Tag_X.append(Tag_dict[i][1]["X"])
            Tag_X[i].fillna(method='ffill', inplace =True)
            Tag_Y.append(Tag_dict[i][1]["Y"])
            Tag_Y[i].fillna(method='ffill', inplace =True)
         
         Time=numpy.array(Time,dtype=numpy.float64) # numpy = (column, row)  
         Time_diff=numpy.diff(Time[0])
         Time_diff1=Time_diff
         Time_diff1=numpy.array(Time_diff1,dtype=numpy.float64)
         Time_diff1=numpy.pad(Time_diff1,(1,0),'reflect')
         Time_diff1=numpy.transpose(Time_diff1)
         
         Time_one=numpy.where(Time_diff==1)
         Time_one=numpy.array(Time_one,dtype=numpy.float64)
         Time_one=numpy.pad(Time_one,[(0,0),(0,1)],'reflect')
         time_count=len(Time[0])
         count_all=list(range(1,time_count+1,1))
         count_all=numpy.array(count_all,dtype=numpy.float64)
         unique_elements, counts_elements = numpy.unique(Time[0], return_counts=True)
         Frames_persecond=numpy.mean(counts_elements) #average FPR
         Frames_persecond_divide=Time_one.size/60
         Frames_persecond=Frames_persecond/Frames_persecond_divide
         print("frames:",count_all.size,"seconds:",Time_one.size,"framesP/S:",Frames_persecond)


#################### Filter ###############################################
         if butterworth==1:                                                             ## order 4 # cutoff max(18 hz = 48) # using 15hz
                Frames_persecond=numpy.mean(Frames_persecond)
                order_slider=int(order_slider)
                nyq= 0.5*Frames_persecond
                Wn = cutoff_slider /nyq
                Wn=Wn/10
                b1,a1=signal.butter(order_slider,Wn)
                b.append(b1)
                a.append(a1)
         b=numpy.array(b,dtype=numpy.float64)
         a=numpy.array(a,dtype=numpy.float64)
         a=a.flatten('C')
         b=b.flatten('C')
         
         Tag_X=numpy.array(Tag_X,dtype=numpy.float64)         
         Tag_Y=numpy.array(Tag_Y,dtype=numpy.float64)

################################################################################################################################################
         ################################################################################################################################################
             ################################################################################################################################################
         
 ######################## variables ##########################################            
         Resultant_X = sqrt(Tag_X**2)                                                                                        
         Resultant_Y= sqrt(Tag_Y**2) 
         Resultant=Resultant_X-Resultant_Y
         Resultant=Resultant

        ########
         print("1 ok")
         moving_count=0
         Resultant_1=[]
         Resultant_2=[]
         Resultant_3=[]
         filtercount=0
         average=[]
         average2=[]
         average1=[]
         if moving_average==1:
              Frames_persecond=numpy.mean(Frames_persecond)
              Window_slider=int(Window_slider)
              N = Window_slider
              Window_slider=numpy.array(Window_slider,dtype=numpy.float64)
              padd=numpy.round(Window_slider/2,decimals=0)
              padd=int(padd)
              for i in range (len(Tag_dict)):                                                                        #### for each tag pad array
                  Resultant_1=numpy.pad(Resultant,[(0,0),(padd,padd)],'reflect')
                 
              average2=savgol_filter(Resultant_1, N, 3, axis = 1)# window size 51, polynomial order 3
              
              average2=numpy.array(average2,dtype=numpy.float64)
              average3=average2[:,padd:-padd]                                                                        # for all tags take away padds
              
              Resultant_diff2=numpy.pad(average3,[(0,0),(0,1)],'reflect')
              Resultant_diff=numpy.diff(Resultant_diff2,axis=1)                                                      # difference for all tag distances
              
         Resultant_diff=numpy.array(Resultant_diff,dtype=numpy.float64)
         Resultant_diff=numpy.absolute(Resultant_diff)
         Resultant_diff1=Resultant_diff
         Resultant_diff2=Resultant_diff1
        
         
         Resultant_Velocity=numpy.gradient(average3, axis=1)                                                         # Resultant Velocity for each tag                      
         Resultant_Velocity_filt_ms_abs=numpy.absolute(Resultant_Velocity)
         Resultant_Velocity_filt_ms_abs1=Resultant_Velocity_filt_ms_abs
         Resultant_Velocity_filt_ms_abs2=Resultant_Velocity_filt_ms_abs
  
         
         Resultant_Acceleration=numpy.gradient(Resultant_Velocity, axis=1)                                           # Resultant Acceleration for each tag
         Resultant_Acceleration_abs=numpy.absolute(Resultant_Acceleration)
         Resultant_Acceleration_abs1=Resultant_Acceleration_abs
         
         
         Distance=numpy.cumsum(Resultant_diff,axis=1)                                                                # cumulative distance for each tag
         Distance=Distance/1000
         Distance2=average3
         Distance2=Distance2/10
         Speed=Distance/Time_one.shape[1] ###check
         Speed=numpy.absolute(Speed)
         Speed=Speed
         Speed1=Speed
         work_count = 0
         Velocity_persecond=[]
         Acceleration_persecond=[]
         Speed_persecond=[]
         Velocity_persecond1=[]
         Acceleration_persecond1=[]
         Speed_persecond1=[]
         Resultant_diff_persecond=[]
         Resultant_diff_persecond1=[]
         cumsum_time=[]

         Second_period=count_all.size/Frames_persecond
         
         Frames_persecond_round=numpy.round(Frames_persecond,decimals=0)
         if len(Tag_dict) ==1:
             second_length=len(Resultant_diff[0])
         else:
             second_length=len(Resultant_diff[1])                                                                    # length of tags recording
         second_length2=list(range(1,second_length+1,1))                                                             # length of tags recording 1:end
         
                
         Tag_1_Velocity_persecond =[];Tag_2_Velocity_persecond =[];Tag_3_Velocity_persecond =[];Tag_4_Velocity_persecond =[];Tag_5_Velocity_persecond =[];
         Tag_6_Velocity_persecond =[];Tag_7_Velocity_persecond =[];Tag_8_Velocity_persecond =[];Tag_9_Velocity_persecond =[];Tag_10_Velocity_persecond =[];
         Tag_11_Velocity_persecond =[];Tag_12_Velocity_persecond =[];Tag_13_Velocity_persecond =[];Tag_14_Velocity_persecond =[];
         
         Tag_1_Acceleration_persecond =[];Tag_2_Acceleration_persecond =[];Tag_3_Acceleration_persecond =[];Tag_4_Acceleration_persecond =[];Tag_5_Acceleration_persecond =[];
         Tag_6_Acceleration_persecond =[];Tag_7_Acceleration_persecond =[];Tag_8_Acceleration_persecond =[];Tag_9_Acceleration_persecond =[];Tag_10_Acceleration_persecond =[];
         Tag_11_Acceleration_persecond =[];Tag_12_Acceleration_persecond =[];Tag_13_Acceleration_persecond =[];Tag_14_Acceleration_persecond =[];
         
         Tag_1_Speed_persecond =[];Tag_2_Speed_persecond =[];Tag_3_Speed_persecond =[];Tag_4_Speed_persecond =[];Tag_5_Speed_persecond =[];
         Tag_6_Speed_persecond =[];Tag_7_Speed_persecond =[];Tag_8_Speed_persecond =[];Tag_9_Speed_persecond =[];Tag_10_Speed_persecond =[];
         Tag_11_Speed_persecond =[];Tag_12_Speed_persecond =[];Tag_13_Speed_persecond =[];Tag_14_Speed_persecond =[];

         Tag_1_Resultant_diff_persecond =[];Tag_2_Resultant_diff_persecond =[];Tag_3_Resultant_diff_persecond =[];Tag_4_Resultant_diff_persecond =[];Tag_5_Resultant_diff_persecond =[];
         Tag_6_Resultant_diff_persecond =[];Tag_7_Resultant_diff_persecond =[];Tag_8_Resultant_diff_persecond =[];Tag_9_Resultant_diff_persecond =[];Tag_10_Resultant_diff_persecond =[];
         Tag_11_Resultant_diff_persecond =[];Tag_12_Resultant_diff_persecond =[];Tag_13_Resultant_diff_persecond =[];Tag_14_Resultant_diff_persecond =[];
         if moving_average==1:
            for j in range (len(Tag_dict)):
             work_count=0
             for i in range(second_length):                                                                         # for length of seconds
                 work_count +=1
                 Velocity_persecond1=(numpy.cumsum(Resultant_Velocity_filt_ms_abs1[j,i]))
                 Acceleration_persecond1=(numpy.cumsum(Resultant_Acceleration_abs1[j,i]))
                 Resultant_diff_persecond1=(numpy.cumsum(Resultant_diff1[j,i]))
                 cumsum_Resultant_diff1=(numpy.cumsum(Resultant_diff2[j,i]))

                 if work_count == Frames_persecond_round:           
                     work_count=-1
                     while j ==0:
                         Tag_1_Velocity_persecond.append(Velocity_persecond1)
                         Tag_1_Acceleration_persecond.append(Acceleration_persecond1)                    
                         Tag_1_Speed_persecond.append(cumsum_Resultant_diff1)
                         Tag_1_Resultant_diff_persecond.append(Resultant_diff_persecond1)

                         Resultant_diff1[j,i]=0
                         Resultant_diff2[j,i]=0
                         Resultant_Velocity_filt_ms_abs1[j,i]=0
                         Resultant_Acceleration_abs1[j,i]=0 
                                               
                         Resultant_diff_persecond1=[]
                         Velocity_persecond1=[]
                         Acceleration_persecond1=[]
                         cumsum_Resultant_diff1=[]                         
                         break;                
                     while j ==1:
                         Tag_2_Velocity_persecond.append(Velocity_persecond1)
                         Tag_2_Acceleration_persecond.append(Acceleration_persecond1)                    
                         Tag_2_Speed_persecond.append(cumsum_Resultant_diff1)
                         Tag_2_Resultant_diff_persecond.append(Resultant_diff_persecond1)

                         Resultant_diff1[j,i]=0
                         Resultant_diff2[j,i]=0
                         Resultant_Velocity_filt_ms_abs1[j,i]=0
                         Resultant_Acceleration_abs1[j,i]=0 
                                               
                         Resultant_diff_persecond1=[]
                         Velocity_persecond1=[]
                         Acceleration_persecond1=[]
                         cumsum_Resultant_diff1=[]                        
                         break;
                     while j ==2:
                         Tag_3_Velocity_persecond.append(Velocity_persecond1)
                         Tag_3_Acceleration_persecond.append(Acceleration_persecond1)                    
                         Tag_3_Speed_persecond.append(cumsum_Resultant_diff1)
                         Tag_3_Resultant_diff_persecond.append(Resultant_diff_persecond1)

                         Resultant_diff1[j,i]=0
                         Resultant_diff2[j,i]=0
                         Resultant_Velocity_filt_ms_abs1[j,i]=0
                         Resultant_Acceleration_abs1[j,i]=0 
                                               
                         Resultant_diff_persecond1=[]
                         Velocity_persecond1=[]
                         Acceleration_persecond1=[]
                         cumsum_Resultant_diff1=[]                         
                         break;
                     while j ==3:
                         Tag_4_Velocity_persecond.append(Velocity_persecond1)
                         Tag_4_Acceleration_persecond.append(Acceleration_persecond1)                    
                         Tag_4_Speed_persecond.append(cumsum_Resultant_diff1)
                         Tag_4_Resultant_diff_persecond.append(Resultant_diff_persecond1)

                         Resultant_diff1[j,i]=0
                         Resultant_diff2[j,i]=0
                         Resultant_Velocity_filt_ms_abs1[j,i]=0
                         Resultant_Acceleration_abs1[j,i]=0 
                                               
                         Resultant_diff_persecond1=[]
                         Velocity_persecond1=[]
                         Acceleration_persecond1=[]
                         cumsum_Resultant_diff1=[]                         
                         break;
                     while j ==4:
                         Tag_5_Velocity_persecond.append(Velocity_persecond1)
                         Tag_5_Acceleration_persecond.append(Acceleration_persecond1)                    
                         Tag_5_Speed_persecond.append(cumsum_Resultant_diff1)
                         Tag_5_Resultant_diff_persecond.append(Resultant_diff_persecond1)

                         Resultant_diff1[j,i]=0
                         Resultant_diff2[j,i]=0
                         Resultant_Velocity_filt_ms_abs1[j,i]=0
                         Resultant_Acceleration_abs1[j,i]=0 
                                               
                         Resultant_diff_persecond1=[]
                         Velocity_persecond1=[]
                         Acceleration_persecond1=[]
                         cumsum_Resultant_diff1=[]                         
                         break;
                     while j ==5:
                         Tag_6_Velocity_persecond.append(Velocity_persecond1)
                         Tag_6_Acceleration_persecond.append(Acceleration_persecond1)                    
                         Tag_6_Speed_persecond.append(cumsum_Resultant_diff1)
                         Tag_6_Resultant_diff_persecond.append(Resultant_diff_persecond1)

                         Resultant_diff1[j,i]=0
                         Resultant_diff2[j,i]=0
                         Resultant_Velocity_filt_ms_abs1[j,i]=0
                         Resultant_Acceleration_abs1[j,i]=0 
                                               
                         Resultant_diff_persecond1=[]
                         Velocity_persecond1=[]
                         Acceleration_persecond1=[]
                         cumsum_Resultant_diff1=[]                         
                         break;
                     while j ==6:
                         Tag_7_Velocity_persecond.append(Velocity_persecond1)
                         Tag_7_Acceleration_persecond.append(Acceleration_persecond1)                    
                         Tag_7_Speed_persecond.append(cumsum_Resultant_diff1)
                         Tag_7_Resultant_diff_persecond.append(Resultant_diff_persecond1)

                         Resultant_diff1[j,i]=0
                         Resultant_diff2[j,i]=0
                         Resultant_Velocity_filt_ms_abs1[j,i]=0
                         Resultant_Acceleration_abs1[j,i]=0 
                                               
                         Resultant_diff_persecond1=[]
                         Velocity_persecond1=[]
                         Acceleration_persecond1=[]
                         cumsum_Resultant_diff1=[]                         
                         break;
                     while j ==7:
                         Tag_8_Velocity_persecond.append(Velocity_persecond1)
                         Tag_8_Acceleration_persecond.append(Acceleration_persecond1)                    
                         Tag_8_Speed_persecond.append(cumsum_Resultant_diff1)
                         Tag_8_Resultant_diff_persecond.append(Resultant_diff_persecond1)

                         Resultant_diff1[j,i]=0
                         Resultant_diff2[j,i]=0
                         Resultant_Velocity_filt_ms_abs1[j,i]=0
                         Resultant_Acceleration_abs1[j,i]=0 
                                               
                         Resultant_diff_persecond1=[]
                         Velocity_persecond1=[]
                         Acceleration_persecond1=[]
                         cumsum_Resultant_diff1=[]                         
                         break;
                     while j ==8:
                         Tag_9_Velocity_persecond.append(Velocity_persecond1)
                         Tag_9_Acceleration_persecond.append(Acceleration_persecond1)                    
                         Tag_9_Speed_persecond.append(cumsum_Resultant_diff1)
                         Tag_9_Resultant_diff_persecond.append(Resultant_diff_persecond1)

                         Resultant_diff1[j,i]=0
                         Resultant_diff2[j,i]=0
                         Resultant_Velocity_filt_ms_abs1[j,i]=0
                         Resultant_Acceleration_abs1[j,i]=0 
                                               
                         Resultant_diff_persecond1=[]
                         Velocity_persecond1=[]
                         Acceleration_persecond1=[]
                         cumsum_Resultant_diff1=[]                         
                         break;
                     while j ==9:
                         Tag_10_Velocity_persecond.append(Velocity_persecond1)
                         Tag_10_Acceleration_persecond.append(Acceleration_persecond1)                    
                         Tag_10_Speed_persecond.append(cumsum_Resultant_diff1)
                         Tag_10_Resultant_diff_persecond.append(Resultant_diff_persecond1)

                         Resultant_diff1[j,i]=0
                         Resultant_diff2[j,i]=0
                         Resultant_Velocity_filt_ms_abs1[j,i]=0
                         Resultant_Acceleration_abs1[j,i]=0 
                                               
                         Resultant_diff_persecond1=[]
                         Velocity_persecond1=[]
                         Acceleration_persecond1=[]
                         cumsum_Resultant_diff1=[]                         
                         break;
                     while j ==10:
                         Tag_11_Velocity_persecond.append(Velocity_persecond1)
                         Tag_11_Acceleration_persecond.append(Acceleration_persecond1)                    
                         Tag_11_Speed_persecond.append(cumsum_Resultant_diff1)
                         Tag_11_Resultant_diff_persecond.append(Resultant_diff_persecond1)

                         Resultant_diff1[j,i]=0
                         Resultant_diff2[j,i]=0
                         Resultant_Velocity_filt_ms_abs1[j,i]=0
                         Resultant_Acceleration_abs1[j,i]=0 
                                               
                         Resultant_diff_persecond1=[]
                         Velocity_persecond1=[]
                         Acceleration_persecond1=[]
                         cumsum_Resultant_diff1=[]                         
                         break; 
                     while j ==11:
                         Tag_12_Velocity_persecond.append(Velocity_persecond1)
                         Tag_12_Acceleration_persecond.append(Acceleration_persecond1)                    
                         Tag_12_Speed_persecond.append(cumsum_Resultant_diff1)
                         Tag_12_Resultant_diff_persecond.append(Resultant_diff_persecond1)

                         Resultant_diff1[j,i]=0
                         Resultant_diff2[j,i]=0
                         Resultant_Velocity_filt_ms_abs1[j,i]=0
                         Resultant_Acceleration_abs1[j,i]=0 
                                               
                         Resultant_diff_persecond1=[]
                         Velocity_persecond1=[]
                         Acceleration_persecond1=[]
                         cumsum_Resultant_diff1=[]                         
                         break;
                     while j ==12:
                         Tag_13_Velocity_persecond.append(Velocity_persecond1)
                         Tag_13_Acceleration_persecond.append(Acceleration_persecond1)                    
                         Tag_13_Speed_persecond.append(cumsum_Resultant_diff1)
                         Tag_13_Resultant_diff_persecond.append(Resultant_diff_persecond1)

                         Resultant_diff1[j,i]=0
                         Resultant_diff2[j,i]=0
                         Resultant_Velocity_filt_ms_abs1[j,i]=0
                         Resultant_Acceleration_abs1[j,i]=0 
                                               
                         Resultant_diff_persecond1=[]
                         Velocity_persecond1=[]
                         Acceleration_persecond1=[]
                         cumsum_Resultant_diff1=[]                         
                         break;
                     while j ==13:                         
                         Tag_14_Velocity_persecond.append(Velocity_persecond1)
                         Tag_14_Acceleration_persecond.append(Acceleration_persecond1)                    
                         Tag_14_Speed_persecond.append(cumsum_Resultant_diff1)
                         Tag_14_Resultant_diff_persecond.append(Resultant_diff_persecond1)

                         Resultant_diff1[j,i]=0
                         Resultant_diff2[j,i]=0
                         Resultant_Velocity_filt_ms_abs1[j,i]=0
                         Resultant_Acceleration_abs1[j,i]=0 
                                               
                         Resultant_diff_persecond1=[]
                         Velocity_persecond1=[]
                         Acceleration_persecond1=[]
                         cumsum_Resultant_diff1=[]
                         break;
            print("2 ok")         
###velocity transforms ###               
            Tag_1_Velocity_persecond=numpy.array(Tag_1_Velocity_persecond,dtype=numpy.float64);Tag_1_Velocity_persecond=numpy.transpose(Tag_1_Velocity_persecond);
            Tag_2_Velocity_persecond=numpy.array(Tag_2_Velocity_persecond,dtype=numpy.float64);Tag_2_Velocity_persecond=numpy.transpose(Tag_2_Velocity_persecond);
            Tag_3_Velocity_persecond=numpy.array(Tag_3_Velocity_persecond,dtype=numpy.float64);Tag_3_Velocity_persecond=numpy.transpose(Tag_3_Velocity_persecond);
            Tag_4_Velocity_persecond=numpy.array(Tag_4_Velocity_persecond,dtype=numpy.float64);Tag_4_Velocity_persecond=numpy.transpose(Tag_4_Velocity_persecond);             
            Tag_5_Velocity_persecond=numpy.array(Tag_5_Velocity_persecond,dtype=numpy.float64);Tag_5_Velocity_persecond=numpy.transpose(Tag_5_Velocity_persecond);             
            Tag_6_Velocity_persecond=numpy.array(Tag_6_Velocity_persecond,dtype=numpy.float64);Tag_6_Velocity_persecond=numpy.transpose(Tag_6_Velocity_persecond);
            Tag_7_Velocity_persecond=numpy.array(Tag_7_Velocity_persecond,dtype=numpy.float64);Tag_7_Velocity_persecond=numpy.transpose(Tag_7_Velocity_persecond);             
            Tag_8_Velocity_persecond=numpy.array(Tag_8_Velocity_persecond,dtype=numpy.float64);Tag_8_Velocity_persecond=numpy.transpose(Tag_8_Velocity_persecond);             
            Tag_9_Velocity_persecond=numpy.array(Tag_9_Velocity_persecond,dtype=numpy.float64);Tag_9_Velocity_persecond=numpy.transpose(Tag_9_Velocity_persecond);
            Tag_10_Velocity_persecond=numpy.array(Tag_10_Velocity_persecond,dtype=numpy.float64);Tag_10_Velocity_persecond=numpy.transpose(Tag_10_Velocity_persecond);             
            Tag_11_Velocity_persecond=numpy.array(Tag_11_Velocity_persecond,dtype=numpy.float64);Tag_11_Velocity_persecond=numpy.transpose(Tag_11_Velocity_persecond);             
            Tag_12_Velocity_persecond=numpy.array(Tag_12_Velocity_persecond,dtype=numpy.float64);Tag_12_Velocity_persecond=numpy.transpose(Tag_12_Velocity_persecond);
            Tag_13_Velocity_persecond=numpy.array(Tag_13_Velocity_persecond,dtype=numpy.float64);Tag_13_Velocity_persecond=numpy.transpose(Tag_13_Velocity_persecond);             
            Tag_14_Velocity_persecond=numpy.array(Tag_14_Velocity_persecond,dtype=numpy.float64);Tag_14_Velocity_persecond=numpy.transpose(Tag_14_Velocity_persecond);             
            
            Tag_1_Velocity_persecond=Tag_1_Velocity_persecond[:,:Time_one.size-1];            
            Velocity_persecond=Tag_1_Velocity_persecond
            Tag_1_Resultant_Velocity_max=Velocity_persecond[0,:].max()
            Tag_1_Resultant_Velocity_mean=Velocity_persecond[0,:].mean()
            Resultant_Velocity_max=Tag_1_Resultant_Velocity_max
            Resultant_Velocity_mean=Tag_1_Resultant_Velocity_mean
#            print("A")

            if len(Tag_2_Velocity_persecond)>0:
                Velocity_persecond=[]
                Resultant_Velocity_max=[]
                Resultant_Velocity_mean=[]
                Tag_2_Velocity_persecond=Tag_2_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                print((Tag_1_Velocity_persecond.shape))
                print((Tag_2_Velocity_persecond.shape))
                Velocity_persecond=numpy.vstack([Tag_1_Velocity_persecond,Tag_2_Velocity_persecond])    
                Tag_2_Resultant_Velocity_max=(Velocity_persecond[1,:].max())
                Tag_2_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean())
                Resultant_Velocity_max=numpy.vstack([Tag_1_Resultant_Velocity_max,Tag_2_Resultant_Velocity_max])
                Resultant_Velocity_mean=numpy.vstack([Tag_1_Resultant_Velocity_mean,Tag_2_Resultant_Velocity_mean])
            else:
                pass

            if len(Tag_3_Velocity_persecond)>0:
                Velocity_persecond=[]
                Resultant_Velocity_max=[]
                Resultant_Velocity_mean=[]
                Tag_2_Velocity_persecond=Tag_2_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_3_Velocity_persecond=Tag_3_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Velocity_persecond=numpy.vstack([Tag_1_Velocity_persecond,Tag_2_Velocity_persecond,Tag_3_Velocity_persecond])
                Tag_2_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_2_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                Tag_3_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_3_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                Resultant_Velocity_max=numpy.vstack([Tag_1_Resultant_Velocity_max,Tag_2_Resultant_Velocity_max,Tag_3_Resultant_Velocity_max])
                Resultant_Velocity_mean=numpy.vstack([Tag_1_Resultant_Velocity_mean,Tag_2_Resultant_Velocity_mean,Tag_3_Resultant_Velocity_mean])
            else:
                pass
            if len(Tag_4_Velocity_persecond)>0:
                Velocity_persecond=[]
                Resultant_Velocity_max=[]
                Resultant_Velocity_mean=[]
                Tag_2_Velocity_persecond=Tag_2_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_3_Velocity_persecond=Tag_3_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_4_Velocity_persecond=Tag_4_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Velocity_persecond=numpy.vstack([Tag_1_Velocity_persecond,Tag_2_Velocity_persecond,Tag_3_Velocity_persecond,Tag_4_Velocity_persecond])
                Tag_2_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_2_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                Tag_3_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_3_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                Tag_4_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_4_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                Resultant_Velocity_max=numpy.vstack([Tag_1_Resultant_Velocity_max,Tag_2_Resultant_Velocity_max,Tag_3_Resultant_Velocity_max,Tag_4_Resultant_Velocity_max])
                Resultant_Velocity_mean=numpy.vstack([Tag_1_Resultant_Velocity_mean,Tag_2_Resultant_Velocity_mean,Tag_3_Resultant_Velocity_mean,Tag_4_Resultant_Velocity_mean])
            else:
                pass
            if len(Tag_5_Velocity_persecond)>0:
                Velocity_persecond=[]
                Resultant_Velocity_max=[]
                Resultant_Velocity_mean=[]
                Tag_2_Velocity_persecond=Tag_2_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_3_Velocity_persecond=Tag_3_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_4_Velocity_persecond=Tag_4_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_5_Velocity_persecond=Tag_5_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Velocity_persecond=numpy.vstack([Tag_1_Velocity_persecond,Tag_2_Velocity_persecond,Tag_3_Velocity_persecond,Tag_4_Velocity_persecond,
                                                 Tag_5_Velocity_persecond])
                Tag_2_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_2_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                Tag_3_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_3_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                Tag_4_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_4_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                Tag_5_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_5_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                Resultant_Velocity_max=numpy.vstack([Tag_1_Resultant_Velocity_max,Tag_2_Resultant_Velocity_max,Tag_3_Resultant_Velocity_max,Tag_4_Resultant_Velocity_max,
                                                 Tag_5_Resultant_Velocity_max])
                Resultant_Velocity_mean=numpy.vstack([Tag_1_Resultant_Velocity_mean,Tag_2_Resultant_Velocity_mean,Tag_3_Resultant_Velocity_mean,Tag_4_Resultant_Velocity_mean,
                                                 Tag_5_Resultant_Velocity_mean])
            else:
                pass
            if len(Tag_6_Velocity_persecond)>0:
                Velocity_persecond=[]
                Resultant_Velocity_max=[]
                Resultant_Velocity_mean=[]
                Tag_2_Velocity_persecond=Tag_2_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_3_Velocity_persecond=Tag_3_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_4_Velocity_persecond=Tag_4_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_5_Velocity_persecond=Tag_5_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_6_Velocity_persecond=Tag_6_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Velocity_persecond=numpy.vstack([Tag_1_Velocity_persecond,Tag_2_Velocity_persecond,Tag_3_Velocity_persecond,Tag_4_Velocity_persecond,
                                                 Tag_5_Velocity_persecond,Tag_6_Velocity_persecond])
                Tag_2_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_2_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                Tag_3_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_3_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                Tag_4_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_4_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                Tag_5_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_5_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                Tag_6_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_6_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                Resultant_Velocity_max=numpy.vstack([Tag_1_Resultant_Velocity_max,Tag_2_Resultant_Velocity_max,Tag_3_Resultant_Velocity_max,Tag_4_Resultant_Velocity_max,
                                                 Tag_5_Resultant_Velocity_max,Tag_6_Resultant_Velocity_max])
                Resultant_Velocity_mean=numpy.vstack([Tag_1_Resultant_Velocity_mean,Tag_2_Resultant_Velocity_mean,Tag_3_Resultant_Velocity_mean,Tag_4_Resultant_Velocity_mean,
                                                 Tag_5_Resultant_Velocity_mean,Tag_6_Resultant_Velocity_mean])
            else:
                pass
            if len(Tag_7_Velocity_persecond)>0:
                Velocity_persecond=[]
                Resultant_Velocity_max=[]
                Resultant_Velocity_mean=[]
                Tag_2_Velocity_persecond=Tag_2_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_3_Velocity_persecond=Tag_3_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_4_Velocity_persecond=Tag_4_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_5_Velocity_persecond=Tag_5_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_6_Velocity_persecond=Tag_6_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_7_Velocity_persecond=Tag_7_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Velocity_persecond=numpy.vstack([Tag_1_Velocity_persecond,Tag_2_Velocity_persecond,Tag_3_Velocity_persecond,Tag_4_Velocity_persecond,
                                                 Tag_5_Velocity_persecond,Tag_6_Velocity_persecond,Tag_7_Velocity_persecond])
                Tag_2_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_2_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                Tag_3_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_3_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                Tag_4_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_4_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                Tag_5_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_5_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                Tag_6_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_6_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                Tag_7_Resultant_Velocity_max=(Velocity_persecond[6,:].max());Tag_7_Resultant_Velocity_mean=(Velocity_persecond[6,:].mean());
                Resultant_Velocity_max=numpy.vstack([Tag_1_Resultant_Velocity_max,Tag_2_Resultant_Velocity_max,Tag_3_Resultant_Velocity_max,Tag_4_Resultant_Velocity_max,
                                                 Tag_5_Resultant_Velocity_max,Tag_6_Resultant_Velocity_max,Tag_7_Resultant_Velocity_max])
                Resultant_Velocity_mean=numpy.vstack([Tag_1_Resultant_Velocity_mean,Tag_2_Resultant_Velocity_mean,Tag_3_Resultant_Velocity_mean,Tag_4_Resultant_Velocity_mean,
                                                 Tag_5_Resultant_Velocity_mean,Tag_6_Resultant_Velocity_mean,Tag_7_Resultant_Velocity_mean])
 
            else:
                pass
            if len(Tag_8_Velocity_persecond)>0:
                Velocity_persecond=[]
                Resultant_Velocity_max=[]
                Resultant_Velocity_mean=[]
                Tag_2_Velocity_persecond=Tag_2_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_3_Velocity_persecond=Tag_3_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_4_Velocity_persecond=Tag_4_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_5_Velocity_persecond=Tag_5_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_6_Velocity_persecond=Tag_6_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_7_Velocity_persecond=Tag_7_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_8_Velocity_persecond=Tag_8_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Velocity_persecond=numpy.vstack([Tag_1_Velocity_persecond,Tag_2_Velocity_persecond,Tag_3_Velocity_persecond,Tag_4_Velocity_persecond,
                                                 Tag_5_Velocity_persecond,Tag_6_Velocity_persecond,Tag_7_Velocity_persecond,Tag_8_Velocity_persecond])
                Tag_2_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_2_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                Tag_3_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_3_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                Tag_4_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_4_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                Tag_5_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_5_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                Tag_6_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_6_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                Tag_7_Resultant_Velocity_max=(Velocity_persecond[6,:].max());Tag_7_Resultant_Velocity_mean=(Velocity_persecond[6,:].mean());
                Tag_8_Resultant_Velocity_max=(Velocity_persecond[7,:].max());Tag_8_Resultant_Velocity_mean=(Velocity_persecond[7,:].mean());
                Resultant_Velocity_max=numpy.vstack([Tag_1_Resultant_Velocity_max,Tag_2_Resultant_Velocity_max,Tag_3_Resultant_Velocity_max,Tag_4_Resultant_Velocity_max,
                                                 Tag_5_Resultant_Velocity_max,Tag_6_Resultant_Velocity_max,Tag_7_Resultant_Velocity_max,Tag_8_Resultant_Velocity_max])
                Resultant_Velocity_mean=numpy.vstack([Tag_1_Resultant_Velocity_mean,Tag_2_Resultant_Velocity_mean,Tag_3_Resultant_Velocity_mean,Tag_4_Resultant_Velocity_mean,
                                                 Tag_5_Resultant_Velocity_mean,Tag_6_Resultant_Velocity_mean,Tag_7_Resultant_Velocity_mean,Tag_8_Resultant_Velocity_mean])
            else:
                pass
            if len(Tag_9_Velocity_persecond)>0:
                Velocity_persecond=[]
                Resultant_Velocity_max=[]
                Resultant_Velocity_mean=[]
                Tag_2_Velocity_persecond=Tag_2_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_3_Velocity_persecond=Tag_3_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_4_Velocity_persecond=Tag_4_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_5_Velocity_persecond=Tag_5_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_6_Velocity_persecond=Tag_6_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_7_Velocity_persecond=Tag_7_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_8_Velocity_persecond=Tag_8_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_9_Velocity_persecond=Tag_9_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Velocity_persecond=numpy.vstack([Tag_1_Velocity_persecond,Tag_2_Velocity_persecond,Tag_3_Velocity_persecond,Tag_4_Velocity_persecond,
                                                 Tag_5_Velocity_persecond,Tag_6_Velocity_persecond,Tag_7_Velocity_persecond,Tag_8_Velocity_persecond,
                                                 Tag_9_Velocity_persecond])
                Tag_2_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_2_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                Tag_3_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_3_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                Tag_4_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_4_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                Tag_5_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_5_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                Tag_6_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_6_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                Tag_7_Resultant_Velocity_max=(Velocity_persecond[6,:].max());Tag_7_Resultant_Velocity_mean=(Velocity_persecond[6,:].mean());
                Tag_8_Resultant_Velocity_max=(Velocity_persecond[7,:].max());Tag_8_Resultant_Velocity_mean=(Velocity_persecond[7,:].mean());
                Tag_9_Resultant_Velocity_max=(Velocity_persecond[8,:].max());Tag_9_Resultant_Velocity_mean=(Velocity_persecond[8,:].mean());
                Resultant_Velocity_max=numpy.vstack([Tag_1_Resultant_Velocity_max,Tag_2_Resultant_Velocity_max,Tag_3_Resultant_Velocity_max,Tag_4_Resultant_Velocity_max,
                                                 Tag_5_Resultant_Velocity_max,Tag_6_Resultant_Velocity_max,Tag_7_Resultant_Velocity_max,Tag_8_Resultant_Velocity_max,
                                                 Tag_9_Resultant_Velocity_max])
                Resultant_Velocity_mean=numpy.vstack([Tag_1_Resultant_Velocity_mean,Tag_2_Resultant_Velocity_mean,Tag_3_Resultant_Velocity_mean,Tag_4_Resultant_Velocity_mean,
                                                 Tag_5_Resultant_Velocity_mean,Tag_6_Resultant_Velocity_mean,Tag_7_Resultant_Velocity_mean,Tag_8_Resultant_Velocity_mean,
                                                 Tag_9_Resultant_Velocity_mean])
            else:
                pass
            if len(Tag_10_Velocity_persecond)>0:
                Velocity_persecond=[]
                Resultant_Velocity_max=[]
                Resultant_Velocity_mean=[]
                Tag_2_Velocity_persecond=Tag_2_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_3_Velocity_persecond=Tag_3_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_4_Velocity_persecond=Tag_4_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_5_Velocity_persecond=Tag_5_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_6_Velocity_persecond=Tag_6_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_7_Velocity_persecond=Tag_7_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_8_Velocity_persecond=Tag_8_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_9_Velocity_persecond=Tag_9_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_10_Velocity_persecond=Tag_10_Velocity_persecond[:,:Time_one.size-1];
                Velocity_persecond=numpy.vstack([Tag_1_Velocity_persecond,Tag_2_Velocity_persecond,Tag_3_Velocity_persecond,Tag_4_Velocity_persecond,
                                                 Tag_5_Velocity_persecond,Tag_6_Velocity_persecond,Tag_7_Velocity_persecond,Tag_8_Velocity_persecond,
                                                 Tag_9_Velocity_persecond,Tag_10_Velocity_persecond])
                Tag_2_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_2_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                Tag_3_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_3_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                Tag_4_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_4_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                Tag_5_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_5_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                Tag_6_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_6_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                Tag_7_Resultant_Velocity_max=(Velocity_persecond[6,:].max());Tag_7_Resultant_Velocity_mean=(Velocity_persecond[6,:].mean());
                Tag_8_Resultant_Velocity_max=(Velocity_persecond[7,:].max());Tag_8_Resultant_Velocity_mean=(Velocity_persecond[7,:].mean());
                Tag_9_Resultant_Velocity_max=(Velocity_persecond[8,:].max());Tag_9_Resultant_Velocity_mean=(Velocity_persecond[8,:].mean());
                Tag_10_Resultant_Velocity_max=(Velocity_persecond[9,:].max());Tag_10_Resultant_Velocity_mean=(Velocity_persecond[9,:].mean());
                Resultant_Velocity_max=numpy.vstack([Tag_1_Resultant_Velocity_max,Tag_2_Resultant_Velocity_max,Tag_3_Resultant_Velocity_max,Tag_4_Resultant_Velocity_max,
                                                 Tag_5_Resultant_Velocity_max,Tag_6_Resultant_Velocity_max,Tag_7_Resultant_Velocity_max,Tag_8_Resultant_Velocity_max,
                                                 Tag_9_Resultant_Velocity_max,Tag_10_Resultant_Velocity_max])
                Resultant_Velocity_mean=numpy.vstack([Tag_1_Resultant_Velocity_mean,Tag_2_Resultant_Velocity_mean,Tag_3_Resultant_Velocity_mean,Tag_4_Resultant_Velocity_mean,
                                                 Tag_5_Resultant_Velocity_mean,Tag_6_Resultant_Velocity_mean,Tag_7_Resultant_Velocity_mean,Tag_8_Resultant_Velocity_mean,
                                                 Tag_9_Resultant_Velocity_mean,Tag_10_Resultant_Velocity_mean])         
        
            else:
                pass
            if len(Tag_11_Velocity_persecond)>0:
                Velocity_persecond=[]
                Resultant_Velocity_max=[]
                Resultant_Velocity_mean=[]
                Tag_2_Velocity_persecond=Tag_2_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_3_Velocity_persecond=Tag_3_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_4_Velocity_persecond=Tag_4_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_5_Velocity_persecond=Tag_5_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_6_Velocity_persecond=Tag_6_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_7_Velocity_persecond=Tag_7_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_8_Velocity_persecond=Tag_8_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_9_Velocity_persecond=Tag_9_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_10_Velocity_persecond=Tag_10_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_11_Velocity_persecond=Tag_11_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Velocity_persecond=numpy.vstack([Tag_1_Velocity_persecond,Tag_2_Velocity_persecond,Tag_3_Velocity_persecond,Tag_4_Velocity_persecond,
                                                 Tag_5_Velocity_persecond,Tag_6_Velocity_persecond,Tag_7_Velocity_persecond,Tag_8_Velocity_persecond,
                                                 Tag_9_Velocity_persecond,Tag_10_Velocity_persecond,Tag_11_Velocity_persecond])
                Tag_2_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_2_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                Tag_3_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_3_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                Tag_4_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_4_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                Tag_5_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_5_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                Tag_6_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_6_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                Tag_7_Resultant_Velocity_max=(Velocity_persecond[6,:].max());Tag_7_Resultant_Velocity_mean=(Velocity_persecond[6,:].mean());
                Tag_8_Resultant_Velocity_max=(Velocity_persecond[7,:].max());Tag_8_Resultant_Velocity_mean=(Velocity_persecond[7,:].mean());
                Tag_9_Resultant_Velocity_max=(Velocity_persecond[8,:].max());Tag_9_Resultant_Velocity_mean=(Velocity_persecond[8,:].mean());
                Tag_10_Resultant_Velocity_max=(Velocity_persecond[9,:].max());Tag_10_Resultant_Velocity_mean=(Velocity_persecond[9,:].mean());
                Tag_11_Resultant_Velocity_max=(Velocity_persecond[10,:].max());Tag_11_Resultant_Velocity_mean=(Velocity_persecond[10,:].mean());
                Resultant_Velocity_max=numpy.vstack([Tag_1_Resultant_Velocity_max,Tag_2_Resultant_Velocity_max,Tag_3_Resultant_Velocity_max,Tag_4_Resultant_Velocity_max,
                                                 Tag_5_Resultant_Velocity_max,Tag_6_Resultant_Velocity_max,Tag_7_Resultant_Velocity_max,Tag_8_Resultant_Velocity_max,
                                                 Tag_9_Resultant_Velocity_max,Tag_10_Resultant_Velocity_max,Tag_11_Resultant_Velocity_max])
                Resultant_Velocity_mean=numpy.vstack([Tag_1_Resultant_Velocity_mean,Tag_2_Resultant_Velocity_mean,Tag_3_Resultant_Velocity_mean,Tag_4_Resultant_Velocity_mean,
                                                 Tag_5_Resultant_Velocity_mean,Tag_6_Resultant_Velocity_mean,Tag_7_Resultant_Velocity_mean,Tag_8_Resultant_Velocity_mean,
                                                 Tag_9_Resultant_Velocity_mean,Tag_10_Resultant_Velocity_mean,Tag_11_Resultant_Velocity_mean])         
            else:
                pass
            if len(Tag_12_Velocity_persecond)>0:
                Velocity_persecond=[]
                Resultant_Velocity_max=[]
                Resultant_Velocity_mean=[]
                Tag_2_Velocity_persecond=Tag_2_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_3_Velocity_persecond=Tag_3_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_4_Velocity_persecond=Tag_4_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_5_Velocity_persecond=Tag_5_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_6_Velocity_persecond=Tag_6_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_7_Velocity_persecond=Tag_7_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_8_Velocity_persecond=Tag_8_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_9_Velocity_persecond=Tag_9_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_10_Velocity_persecond=Tag_10_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_11_Velocity_persecond=Tag_11_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_12_Velocity_persecond=Tag_12_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Velocity_persecond=numpy.vstack([Tag_1_Velocity_persecond,Tag_2_Velocity_persecond,Tag_3_Velocity_persecond,Tag_4_Velocity_persecond,
                                                 Tag_5_Velocity_persecond,Tag_6_Velocity_persecond,Tag_7_Velocity_persecond,Tag_8_Velocity_persecond,
                                                 Tag_9_Velocity_persecond,Tag_10_Velocity_persecond,Tag_11_Velocity_persecond,Tag_12_Velocity_persecond])
                Tag_2_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_2_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                Tag_3_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_3_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                Tag_4_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_4_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                Tag_5_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_5_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                Tag_6_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_6_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                Tag_7_Resultant_Velocity_max=(Velocity_persecond[6,:].max());Tag_7_Resultant_Velocity_mean=(Velocity_persecond[6,:].mean());
                Tag_8_Resultant_Velocity_max=(Velocity_persecond[7,:].max());Tag_8_Resultant_Velocity_mean=(Velocity_persecond[7,:].mean());
                Tag_9_Resultant_Velocity_max=(Velocity_persecond[8,:].max());Tag_9_Resultant_Velocity_mean=(Velocity_persecond[8,:].mean());
                Tag_10_Resultant_Velocity_max=(Velocity_persecond[9,:].max());Tag_10_Resultant_Velocity_mean=(Velocity_persecond[9,:].mean());
                Tag_11_Resultant_Velocity_max=(Velocity_persecond[10,:].max());Tag_11_Resultant_Velocity_mean=(Velocity_persecond[10,:].mean());
                Tag_12_Resultant_Velocity_max=(Velocity_persecond[11,:].max());Tag_12_Resultant_Velocity_mean=(Velocity_persecond[11,:].mean());
                Resultant_Velocity_max=numpy.vstack([Tag_1_Resultant_Velocity_max,Tag_2_Resultant_Velocity_max,Tag_3_Resultant_Velocity_max,Tag_4_Resultant_Velocity_max,
                                                 Tag_5_Resultant_Velocity_max,Tag_6_Resultant_Velocity_max,Tag_7_Resultant_Velocity_max,Tag_8_Resultant_Velocity_max,
                                                 Tag_9_Resultant_Velocity_max,Tag_10_Resultant_Velocity_max,Tag_11_Resultant_Velocity_max,Tag_12_Resultant_Velocity_max])
                Resultant_Velocity_mean=numpy.vstack([Tag_1_Resultant_Velocity_mean,Tag_2_Resultant_Velocity_mean,Tag_3_Resultant_Velocity_mean,Tag_4_Resultant_Velocity_mean,
                                                 Tag_5_Resultant_Velocity_mean,Tag_6_Resultant_Velocity_mean,Tag_7_Resultant_Velocity_mean,Tag_8_Resultant_Velocity_mean,
                                                 Tag_9_Resultant_Velocity_mean,Tag_10_Resultant_Velocity_mean,Tag_11_Resultant_Velocity_mean,Tag_12_Resultant_Velocity_mean])
            else:
                pass
            if len(Tag_13_Velocity_persecond)>0:
                Velocity_persecond=[]
                Resultant_Velocity_max=[]
                Resultant_Velocity_mean=[]
                Tag_2_Velocity_persecond=Tag_2_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_3_Velocity_persecond=Tag_3_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_4_Velocity_persecond=Tag_4_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_5_Velocity_persecond=Tag_5_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_6_Velocity_persecond=Tag_6_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_7_Velocity_persecond=Tag_7_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_8_Velocity_persecond=Tag_8_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_9_Velocity_persecond=Tag_9_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_10_Velocity_persecond=Tag_10_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_11_Velocity_persecond=Tag_11_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_12_Velocity_persecond=Tag_12_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_13_Velocity_persecond=Tag_13_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Velocity_persecond=numpy.vstack([Tag_1_Velocity_persecond,Tag_2_Velocity_persecond,Tag_3_Velocity_persecond,Tag_4_Velocity_persecond,
                                                 Tag_5_Velocity_persecond,Tag_6_Velocity_persecond,Tag_7_Velocity_persecond,Tag_8_Velocity_persecond,
                                                 Tag_9_Velocity_persecond,Tag_10_Velocity_persecond,Tag_11_Velocity_persecond,Tag_12_Velocity_persecond,
                                                 Tag_13_Velocity_persecond])
                Tag_2_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_2_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                Tag_3_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_3_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                Tag_4_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_4_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                Tag_5_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_5_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                Tag_6_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_6_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                Tag_7_Resultant_Velocity_max=(Velocity_persecond[6,:].max());Tag_7_Resultant_Velocity_mean=(Velocity_persecond[6,:].mean());
                Tag_8_Resultant_Velocity_max=(Velocity_persecond[7,:].max());Tag_8_Resultant_Velocity_mean=(Velocity_persecond[7,:].mean());
                Tag_9_Resultant_Velocity_max=(Velocity_persecond[8,:].max());Tag_9_Resultant_Velocity_mean=(Velocity_persecond[8,:].mean());
                Tag_10_Resultant_Velocity_max=(Velocity_persecond[9,:].max());Tag_10_Resultant_Velocity_mean=(Velocity_persecond[9,:].mean());
                Tag_11_Resultant_Velocity_max=(Velocity_persecond[10,:].max());Tag_11_Resultant_Velocity_mean=(Velocity_persecond[10,:].mean());
                Tag_12_Resultant_Velocity_max=(Velocity_persecond[11,:].max());Tag_12_Resultant_Velocity_mean=(Velocity_persecond[11,:].mean());
                Tag_13_Resultant_Velocity_max=(Velocity_persecond[12,:].max());Tag_13_Resultant_Velocity_mean=(Velocity_persecond[12,:].mean());
                Resultant_Velocity_max=numpy.vstack([Tag_1_Resultant_Velocity_max,Tag_2_Resultant_Velocity_max,Tag_3_Resultant_Velocity_max,Tag_4_Resultant_Velocity_max,
                                                 Tag_5_Resultant_Velocity_max,Tag_6_Resultant_Velocity_max,Tag_7_Resultant_Velocity_max,Tag_8_Resultant_Velocity_max,
                                                 Tag_9_Resultant_Velocity_max,Tag_10_Resultant_Velocity_max,Tag_11_Resultant_Velocity_max,Tag_12_Resultant_Velocity_max,
                                                 Tag_13_Resultant_Velocity_max])
                Resultant_Velocity_mean=numpy.vstack([Tag_1_Resultant_Velocity_mean,Tag_2_Resultant_Velocity_mean,Tag_3_Resultant_Velocity_mean,Tag_4_Resultant_Velocity_mean,
                                                 Tag_5_Resultant_Velocity_mean,Tag_6_Resultant_Velocity_mean,Tag_7_Resultant_Velocity_mean,Tag_8_Resultant_Velocity_mean,
                                                 Tag_9_Resultant_Velocity_mean,Tag_10_Resultant_Velocity_mean,Tag_11_Resultant_Velocity_mean,Tag_12_Resultant_Velocity_mean,
                                                 Tag_13_Resultant_Velocity_mean])
            else:
                pass
            if len(Tag_14_Velocity_persecond)>0:
                Velocity_persecond=[]
                Resultant_Velocity_max=[]
                Resultant_Velocity_mean=[]
                Tag_2_Velocity_persecond=Tag_2_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_3_Velocity_persecond=Tag_3_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_4_Velocity_persecond=Tag_4_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_5_Velocity_persecond=Tag_5_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_6_Velocity_persecond=Tag_6_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_7_Velocity_persecond=Tag_7_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_8_Velocity_persecond=Tag_8_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_9_Velocity_persecond=Tag_9_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_10_Velocity_persecond=Tag_10_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_11_Velocity_persecond=Tag_11_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_12_Velocity_persecond=Tag_12_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_13_Velocity_persecond=Tag_13_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                Tag_14_Velocity_persecond=Tag_14_Velocity_persecond[:,:Tag_1_Velocity_persecond.size];
                
                Velocity_persecond=numpy.vstack([Tag_1_Velocity_persecond,Tag_2_Velocity_persecond,Tag_3_Velocity_persecond,Tag_4_Velocity_persecond,
                                                 Tag_5_Velocity_persecond,Tag_6_Velocity_persecond,Tag_7_Velocity_persecond,Tag_8_Velocity_persecond,
                                                 Tag_9_Velocity_persecond,Tag_10_Velocity_persecond,Tag_11_Velocity_persecond,Tag_12_Velocity_persecond,
                                                 Tag_13_Velocity_persecond,Tag_14_Velocity_persecond])
                
                Tag_2_Resultant_Velocity_max=(Velocity_persecond[1,:].max());Tag_2_Resultant_Velocity_mean=(Velocity_persecond[1,:].mean());
                Tag_3_Resultant_Velocity_max=(Velocity_persecond[2,:].max());Tag_3_Resultant_Velocity_mean=(Velocity_persecond[2,:].mean());
                Tag_4_Resultant_Velocity_max=(Velocity_persecond[3,:].max());Tag_4_Resultant_Velocity_mean=(Velocity_persecond[3,:].mean());
                Tag_5_Resultant_Velocity_max=(Velocity_persecond[4,:].max());Tag_5_Resultant_Velocity_mean=(Velocity_persecond[4,:].mean());
                Tag_6_Resultant_Velocity_max=(Velocity_persecond[5,:].max());Tag_6_Resultant_Velocity_mean=(Velocity_persecond[5,:].mean());
                Tag_7_Resultant_Velocity_max=(Velocity_persecond[6,:].max());Tag_7_Resultant_Velocity_mean=(Velocity_persecond[6,:].mean());
                Tag_8_Resultant_Velocity_max=(Velocity_persecond[7,:].max());Tag_8_Resultant_Velocity_mean=(Velocity_persecond[7,:].mean());
                Tag_9_Resultant_Velocity_max=(Velocity_persecond[8,:].max());Tag_9_Resultant_Velocity_mean=(Velocity_persecond[8,:].mean());
                Tag_10_Resultant_Velocity_max=(Velocity_persecond[9,:].max());Tag_10_Resultant_Velocity_mean=(Velocity_persecond[9,:].mean());
                Tag_11_Resultant_Velocity_max=(Velocity_persecond[10,:].max());Tag_11_Resultant_Velocity_mean=(Velocity_persecond[10,:].mean());
                Tag_12_Resultant_Velocity_max=(Velocity_persecond[11,:].max());Tag_12_Resultant_Velocity_mean=(Velocity_persecond[11,:].mean());
                Tag_13_Resultant_Velocity_max=(Velocity_persecond[12,:].max());Tag_13_Resultant_Velocity_mean=(Velocity_persecond[12,:].mean());
                Tag_14_Resultant_Velocity_max=(Velocity_persecond[13,:].max());Tag_14_Resultant_Velocity_mean=(Velocity_persecond[13,:].mean());
                
                Resultant_Velocity_max=numpy.vstack([Tag_1_Resultant_Velocity_max,Tag_2_Resultant_Velocity_max,Tag_3_Resultant_Velocity_max,Tag_4_Resultant_Velocity_max,
                                                 Tag_5_Resultant_Velocity_max,Tag_6_Resultant_Velocity_max,Tag_7_Resultant_Velocity_max,Tag_8_Resultant_Velocity_max,
                                                 Tag_9_Resultant_Velocity_max,Tag_10_Resultant_Velocity_max,Tag_11_Resultant_Velocity_max,Tag_12_Resultant_Velocity_max,
                                                 Tag_13_Resultant_Velocity_max,Tag_14_Resultant_Velocity_max])
                Resultant_Velocity_mean=numpy.vstack([Tag_1_Resultant_Velocity_mean,Tag_2_Resultant_Velocity_mean,Tag_3_Resultant_Velocity_mean,Tag_4_Resultant_Velocity_mean,
                                                 Tag_5_Resultant_Velocity_mean,Tag_6_Resultant_Velocity_mean,Tag_7_Resultant_Velocity_mean,Tag_8_Resultant_Velocity_mean,
                                                 Tag_9_Resultant_Velocity_mean,Tag_10_Resultant_Velocity_mean,Tag_11_Resultant_Velocity_mean,Tag_12_Resultant_Velocity_mean,
                                                 Tag_13_Resultant_Velocity_mean,Tag_14_Resultant_Velocity_mean])
            else:
                pass
 ###Acceleration transforms ###
   #         print("3 ok")  
            Tag_1_Acceleration_persecond=numpy.array(Tag_1_Acceleration_persecond,dtype=numpy.float64);Tag_1_Acceleration_persecond=numpy.transpose(Tag_1_Acceleration_persecond);
            Tag_2_Acceleration_persecond=numpy.array(Tag_2_Acceleration_persecond,dtype=numpy.float64);Tag_2_Acceleration_persecond=numpy.transpose(Tag_2_Acceleration_persecond);             
            Tag_3_Acceleration_persecond=numpy.array(Tag_3_Acceleration_persecond,dtype=numpy.float64);Tag_3_Acceleration_persecond=numpy.transpose(Tag_3_Acceleration_persecond);
            Tag_4_Acceleration_persecond=numpy.array(Tag_4_Acceleration_persecond,dtype=numpy.float64);Tag_4_Acceleration_persecond=numpy.transpose(Tag_4_Acceleration_persecond);             
            Tag_5_Acceleration_persecond=numpy.array(Tag_5_Acceleration_persecond,dtype=numpy.float64);Tag_5_Acceleration_persecond=numpy.transpose(Tag_5_Acceleration_persecond);             
            Tag_6_Acceleration_persecond=numpy.array(Tag_6_Acceleration_persecond,dtype=numpy.float64);Tag_6_Acceleration_persecond=numpy.transpose(Tag_6_Acceleration_persecond);
            Tag_7_Acceleration_persecond=numpy.array(Tag_7_Acceleration_persecond,dtype=numpy.float64);Tag_7_Acceleration_persecond=numpy.transpose(Tag_7_Acceleration_persecond);             
            Tag_8_Acceleration_persecond=numpy.array(Tag_8_Acceleration_persecond,dtype=numpy.float64);Tag_8_Acceleration_persecond=numpy.transpose(Tag_8_Acceleration_persecond);             
            Tag_9_Acceleration_persecond=numpy.array(Tag_9_Acceleration_persecond,dtype=numpy.float64);Tag_9_Acceleration_persecond=numpy.transpose(Tag_9_Acceleration_persecond);
            Tag_10_Acceleration_persecond=numpy.array(Tag_10_Acceleration_persecond,dtype=numpy.float64);Tag_10_Acceleration_persecond=numpy.transpose(Tag_10_Acceleration_persecond);             
            Tag_11_Acceleration_persecond=numpy.array(Tag_11_Acceleration_persecond,dtype=numpy.float64);Tag_11_Acceleration_persecond=numpy.transpose(Tag_11_Acceleration_persecond);             
            Tag_12_Acceleration_persecond=numpy.array(Tag_12_Acceleration_persecond,dtype=numpy.float64);Tag_12_Acceleration_persecond=numpy.transpose(Tag_12_Acceleration_persecond);
            Tag_13_Acceleration_persecond=numpy.array(Tag_13_Acceleration_persecond,dtype=numpy.float64);Tag_13_Acceleration_persecond=numpy.transpose(Tag_13_Acceleration_persecond);             
            Tag_14_Acceleration_persecond=numpy.array(Tag_14_Acceleration_persecond,dtype=numpy.float64);Tag_14_Acceleration_persecond=numpy.transpose(Tag_14_Acceleration_persecond);             

            Tag_1_Acceleration_persecond=Tag_1_Acceleration_persecond[:,:Time_one.size-1];
            Acceleration_persecond=Tag_1_Acceleration_persecond
            Tag_1_Resultant_Acceleration_max=Acceleration_persecond[0,:].max()
            Tag_1_Resultant_Acceleration_mean=Acceleration_persecond[0,:].mean()
            Resultant_Acceleration_max=Tag_1_Resultant_Acceleration_max
            Resultant_Acceleration_mean=Tag_1_Resultant_Acceleration_mean
            
            if len(Tag_2_Acceleration_persecond)>0:
                Tag_2_Acceleration_persecond=Tag_2_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Acceleration_persecond=numpy.vstack([Tag_1_Acceleration_persecond,Tag_2_Acceleration_persecond])
                Tag_2_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max())
                Tag_2_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean())
                Resultant_Acceleration_max=numpy.vstack([Tag_1_Resultant_Acceleration_max,Tag_2_Resultant_Acceleration_max])
                Resultant_Acceleration_mean=numpy.vstack([Tag_1_Resultant_Acceleration_mean,Tag_2_Resultant_Acceleration_mean])
            else:
                pass
            if len(Tag_3_Acceleration_persecond)>0:
                Tag_2_Acceleration_persecond=Tag_2_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_3_Acceleration_persecond=Tag_3_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Acceleration_persecond=numpy.vstack([Tag_1_Acceleration_persecond,Tag_2_Acceleration_persecond,Tag_3_Acceleration_persecond])
                Tag_2_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_2_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                Tag_3_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_3_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                Resultant_Acceleration_max=numpy.vstack([Tag_1_Resultant_Acceleration_max,Tag_2_Resultant_Acceleration_max,Tag_3_Resultant_Acceleration_max])
                Resultant_Acceleration_mean=numpy.vstack([Tag_1_Resultant_Acceleration_mean,Tag_2_Resultant_Acceleration_mean,Tag_3_Resultant_Acceleration_mean])
            else:
                pass
            if len(Tag_4_Acceleration_persecond)>0:
                Tag_2_Acceleration_persecond=Tag_2_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_3_Acceleration_persecond=Tag_3_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_4_Acceleration_persecond=Tag_4_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Acceleration_persecond=numpy.vstack([Tag_1_Acceleration_persecond,Tag_2_Acceleration_persecond,Tag_3_Acceleration_persecond,Tag_4_Acceleration_persecond])
                Tag_2_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_2_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                Tag_3_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_3_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                Tag_4_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_4_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                Resultant_Acceleration_max=numpy.vstack([Tag_1_Resultant_Acceleration_max,Tag_2_Resultant_Acceleration_max,Tag_3_Resultant_Acceleration_max,Tag_4_Resultant_Acceleration_max])
                Resultant_Acceleration_mean=numpy.vstack([Tag_1_Resultant_Acceleration_mean,Tag_2_Resultant_Acceleration_mean,Tag_3_Resultant_Acceleration_mean,Tag_4_Resultant_Acceleration_mean])
            else:
                pass
            if len(Tag_5_Acceleration_persecond)>0:
                Tag_2_Acceleration_persecond=Tag_2_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_3_Acceleration_persecond=Tag_3_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_4_Acceleration_persecond=Tag_4_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_5_Acceleration_persecond=Tag_5_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Acceleration_persecond=numpy.vstack([Tag_1_Acceleration_persecond,Tag_2_Acceleration_persecond,Tag_3_Acceleration_persecond,Tag_4_Acceleration_persecond,
                                                 Tag_5_Acceleration_persecond])
                Tag_2_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_2_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                Tag_3_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_3_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                Tag_4_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_4_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                Tag_5_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_5_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                Resultant_Acceleration_max=numpy.vstack([Tag_1_Resultant_Acceleration_max,Tag_2_Resultant_Acceleration_max,Tag_3_Resultant_Acceleration_max,Tag_4_Resultant_Acceleration_max,
                                                 Tag_5_Resultant_Acceleration_max])
                Resultant_Acceleration_mean=numpy.vstack([Tag_1_Resultant_Acceleration_mean,Tag_2_Resultant_Acceleration_mean,Tag_3_Resultant_Acceleration_mean,Tag_4_Resultant_Acceleration_mean,
                                                 Tag_5_Resultant_Acceleration_mean])
            else:
                pass
            if len(Tag_6_Acceleration_persecond)>0:
                Tag_2_Acceleration_persecond=Tag_2_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_3_Acceleration_persecond=Tag_3_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_4_Acceleration_persecond=Tag_4_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_5_Acceleration_persecond=Tag_5_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_6_Acceleration_persecond=Tag_6_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Acceleration_persecond=numpy.vstack([Tag_1_Acceleration_persecond,Tag_2_Acceleration_persecond,Tag_3_Acceleration_persecond,Tag_4_Acceleration_persecond,
                                                 Tag_5_Acceleration_persecond,Tag_6_Acceleration_persecond])
                Tag_2_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_2_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                Tag_3_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_3_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                Tag_4_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_4_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                Tag_5_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_5_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                Tag_6_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_6_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                Resultant_Acceleration_max=numpy.vstack([Tag_1_Resultant_Acceleration_max,Tag_2_Resultant_Acceleration_max,Tag_3_Resultant_Acceleration_max,Tag_4_Resultant_Acceleration_max,
                                                 Tag_5_Resultant_Acceleration_max,Tag_6_Resultant_Acceleration_max])
                Resultant_Acceleration_mean=numpy.vstack([Tag_1_Resultant_Acceleration_mean,Tag_2_Resultant_Acceleration_mean,Tag_3_Resultant_Acceleration_mean,Tag_4_Resultant_Acceleration_mean,
                                                 Tag_5_Resultant_Acceleration_mean,Tag_6_Resultant_Acceleration_mean])
            else:
                pass
            if len(Tag_7_Acceleration_persecond)>0:
                Tag_2_Acceleration_persecond=Tag_2_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_3_Acceleration_persecond=Tag_3_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_4_Acceleration_persecond=Tag_4_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_5_Acceleration_persecond=Tag_5_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_6_Acceleration_persecond=Tag_6_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_7_Acceleration_persecond=Tag_7_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Acceleration_persecond=numpy.vstack([Tag_1_Acceleration_persecond,Tag_2_Acceleration_persecond,Tag_3_Acceleration_persecond,Tag_4_Acceleration_persecond,
                                                 Tag_5_Acceleration_persecond,Tag_6_Acceleration_persecond,Tag_7_Acceleration_persecond])
                Tag_2_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_2_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                Tag_3_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_3_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                Tag_4_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_4_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                Tag_5_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_5_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                Tag_6_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_6_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                Tag_7_Resultant_Acceleration_max=(Acceleration_persecond[6,:].max());Tag_7_Resultant_Acceleration_mean=(Acceleration_persecond[6,:].mean());
                Resultant_Acceleration_max=numpy.vstack([Tag_1_Resultant_Acceleration_max,Tag_2_Resultant_Acceleration_max,Tag_3_Resultant_Acceleration_max,Tag_4_Resultant_Acceleration_max,
                                                 Tag_5_Resultant_Acceleration_max,Tag_6_Resultant_Acceleration_max,Tag_7_Resultant_Acceleration_max])
                Resultant_Acceleration_mean=numpy.vstack([Tag_1_Resultant_Acceleration_mean,Tag_2_Resultant_Acceleration_mean,Tag_3_Resultant_Acceleration_mean,Tag_4_Resultant_Acceleration_mean,
                                                 Tag_5_Resultant_Acceleration_mean,Tag_6_Resultant_Acceleration_mean,Tag_7_Resultant_Acceleration_mean])
 
            else:
                pass
            if len(Tag_8_Acceleration_persecond)>0:
                Tag_2_Acceleration_persecond=Tag_2_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_3_Acceleration_persecond=Tag_3_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_4_Acceleration_persecond=Tag_4_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_5_Acceleration_persecond=Tag_5_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_6_Acceleration_persecond=Tag_6_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_7_Acceleration_persecond=Tag_7_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_8_Acceleration_persecond=Tag_8_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Acceleration_persecond=numpy.vstack([Tag_1_Acceleration_persecond,Tag_2_Acceleration_persecond,Tag_3_Acceleration_persecond,Tag_4_Acceleration_persecond,
                                                 Tag_5_Acceleration_persecond,Tag_6_Acceleration_persecond,Tag_7_Acceleration_persecond,Tag_8_Acceleration_persecond])
                Tag_2_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_2_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                Tag_3_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_3_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                Tag_4_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_4_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                Tag_5_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_5_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                Tag_6_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_6_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                Tag_7_Resultant_Acceleration_max=(Acceleration_persecond[6,:].max());Tag_7_Resultant_Acceleration_mean=(Acceleration_persecond[6,:].mean());
                Tag_8_Resultant_Acceleration_max=(Acceleration_persecond[7,:].max());Tag_8_Resultant_Acceleration_mean=(Acceleration_persecond[7,:].mean());
                Resultant_Acceleration_max=numpy.vstack([Tag_1_Resultant_Acceleration_max,Tag_2_Resultant_Acceleration_max,Tag_3_Resultant_Acceleration_max,Tag_4_Resultant_Acceleration_max,
                                                 Tag_5_Resultant_Acceleration_max,Tag_6_Resultant_Acceleration_max,Tag_7_Resultant_Acceleration_max,Tag_8_Resultant_Acceleration_max])
                Resultant_Acceleration_mean=numpy.vstack([Tag_1_Resultant_Acceleration_mean,Tag_2_Resultant_Acceleration_mean,Tag_3_Resultant_Acceleration_mean,Tag_4_Resultant_Acceleration_mean,
                                                 Tag_5_Resultant_Acceleration_mean,Tag_6_Resultant_Acceleration_mean,Tag_7_Resultant_Acceleration_mean,Tag_8_Resultant_Acceleration_mean])
            else:
                pass
            if len(Tag_9_Acceleration_persecond)>0:
                Tag_2_Acceleration_persecond=Tag_2_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_3_Acceleration_persecond=Tag_3_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_4_Acceleration_persecond=Tag_4_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_5_Acceleration_persecond=Tag_5_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_6_Acceleration_persecond=Tag_6_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_7_Acceleration_persecond=Tag_7_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_8_Acceleration_persecond=Tag_8_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_9_Acceleration_persecond=Tag_9_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Acceleration_persecond=numpy.vstack([Tag_1_Acceleration_persecond,Tag_2_Acceleration_persecond,Tag_3_Acceleration_persecond,Tag_4_Acceleration_persecond,
                                                 Tag_5_Acceleration_persecond,Tag_6_Acceleration_persecond,Tag_7_Acceleration_persecond,Tag_8_Acceleration_persecond,
                                                 Tag_9_Acceleration_persecond])
                Tag_2_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_2_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                Tag_3_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_3_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                Tag_4_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_4_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                Tag_5_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_5_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                Tag_6_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_6_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                Tag_7_Resultant_Acceleration_max=(Acceleration_persecond[6,:].max());Tag_7_Resultant_Acceleration_mean=(Acceleration_persecond[6,:].mean());
                Tag_8_Resultant_Acceleration_max=(Acceleration_persecond[7,:].max());Tag_8_Resultant_Acceleration_mean=(Acceleration_persecond[7,:].mean());
                Tag_9_Resultant_Acceleration_max=(Acceleration_persecond[8,:].max());Tag_9_Resultant_Acceleration_mean=(Acceleration_persecond[8,:].mean());
                Resultant_Acceleration_max=numpy.vstack([Tag_1_Resultant_Acceleration_max,Tag_2_Resultant_Acceleration_max,Tag_3_Resultant_Acceleration_max,Tag_4_Resultant_Acceleration_max,
                                                 Tag_5_Resultant_Acceleration_max,Tag_6_Resultant_Acceleration_max,Tag_7_Resultant_Acceleration_max,Tag_8_Resultant_Acceleration_max,
                                                 Tag_9_Resultant_Acceleration_max])
                Resultant_Acceleration_mean=numpy.vstack([Tag_1_Resultant_Acceleration_mean,Tag_2_Resultant_Acceleration_mean,Tag_3_Resultant_Acceleration_mean,Tag_4_Resultant_Acceleration_mean,
                                                 Tag_5_Resultant_Acceleration_mean,Tag_6_Resultant_Acceleration_mean,Tag_7_Resultant_Acceleration_mean,Tag_8_Resultant_Acceleration_mean,
                                                 Tag_9_Resultant_Acceleration_mean])
            else:
                pass
            if len(Tag_10_Acceleration_persecond)>0:
                Tag_2_Acceleration_persecond=Tag_2_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_3_Acceleration_persecond=Tag_3_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_4_Acceleration_persecond=Tag_4_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_5_Acceleration_persecond=Tag_5_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_6_Acceleration_persecond=Tag_6_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_7_Acceleration_persecond=Tag_7_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_8_Acceleration_persecond=Tag_8_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_9_Acceleration_persecond=Tag_9_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_10_Acceleration_persecond=Tag_10_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Acceleration_persecond=numpy.vstack([Tag_1_Acceleration_persecond,Tag_2_Acceleration_persecond,Tag_3_Acceleration_persecond,Tag_4_Acceleration_persecond,
                                                 Tag_5_Acceleration_persecond,Tag_6_Acceleration_persecond,Tag_7_Acceleration_persecond,Tag_8_Acceleration_persecond,
                                                 Tag_9_Acceleration_persecond,Tag_10_Acceleration_persecond])
                Tag_2_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_2_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                Tag_3_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_3_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                Tag_4_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_4_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                Tag_5_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_5_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                Tag_6_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_6_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                Tag_7_Resultant_Acceleration_max=(Acceleration_persecond[6,:].max());Tag_7_Resultant_Acceleration_mean=(Acceleration_persecond[6,:].mean());
                Tag_8_Resultant_Acceleration_max=(Acceleration_persecond[7,:].max());Tag_8_Resultant_Acceleration_mean=(Acceleration_persecond[7,:].mean());
                Tag_9_Resultant_Acceleration_max=(Acceleration_persecond[8,:].max());Tag_9_Resultant_Acceleration_mean=(Acceleration_persecond[8,:].mean());
                Tag_10_Resultant_Acceleration_max=(Acceleration_persecond[9,:].max());Tag_10_Resultant_Acceleration_mean=(Acceleration_persecond[9,:].mean());
                Resultant_Acceleration_max=numpy.vstack([Tag_1_Resultant_Acceleration_max,Tag_2_Resultant_Acceleration_max,Tag_3_Resultant_Acceleration_max,Tag_4_Resultant_Acceleration_max,
                                                 Tag_5_Resultant_Acceleration_max,Tag_6_Resultant_Acceleration_max,Tag_7_Resultant_Acceleration_max,Tag_8_Resultant_Acceleration_max,
                                                 Tag_9_Resultant_Acceleration_max,Tag_10_Resultant_Acceleration_max])
                Resultant_Acceleration_mean=numpy.vstack([Tag_1_Resultant_Acceleration_mean,Tag_2_Resultant_Acceleration_mean,Tag_3_Resultant_Acceleration_mean,Tag_4_Resultant_Acceleration_mean,
                                                 Tag_5_Resultant_Acceleration_mean,Tag_6_Resultant_Acceleration_mean,Tag_7_Resultant_Acceleration_mean,Tag_8_Resultant_Acceleration_mean,
                                                 Tag_9_Resultant_Acceleration_mean,Tag_10_Resultant_Acceleration_mean])         
        
            else:
                pass
            if len(Tag_11_Acceleration_persecond)>0:
                Tag_2_Acceleration_persecond=Tag_2_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_3_Acceleration_persecond=Tag_3_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_4_Acceleration_persecond=Tag_4_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_5_Acceleration_persecond=Tag_5_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_6_Acceleration_persecond=Tag_6_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_7_Acceleration_persecond=Tag_7_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_8_Acceleration_persecond=Tag_8_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_9_Acceleration_persecond=Tag_9_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_10_Acceleration_persecond=Tag_10_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_11_Acceleration_persecond=Tag_11_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Acceleration_persecond=numpy.vstack([Tag_1_Acceleration_persecond,Tag_2_Acceleration_persecond,Tag_3_Acceleration_persecond,Tag_4_Acceleration_persecond,
                                                 Tag_5_Acceleration_persecond,Tag_6_Acceleration_persecond,Tag_7_Acceleration_persecond,Tag_8_Acceleration_persecond,
                                                 Tag_9_Acceleration_persecond,Tag_10_Acceleration_persecond,Tag_11_Acceleration_persecond])
                Tag_2_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_2_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                Tag_3_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_3_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                Tag_4_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_4_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                Tag_5_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_5_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                Tag_6_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_6_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                Tag_7_Resultant_Acceleration_max=(Acceleration_persecond[6,:].max());Tag_7_Resultant_Acceleration_mean=(Acceleration_persecond[6,:].mean());
                Tag_8_Resultant_Acceleration_max=(Acceleration_persecond[7,:].max());Tag_8_Resultant_Acceleration_mean=(Acceleration_persecond[7,:].mean());
                Tag_9_Resultant_Acceleration_max=(Acceleration_persecond[8,:].max());Tag_9_Resultant_Acceleration_mean=(Acceleration_persecond[8,:].mean());
                Tag_10_Resultant_Acceleration_max=(Acceleration_persecond[9,:].max());Tag_10_Resultant_Acceleration_mean=(Acceleration_persecond[9,:].mean());
                Tag_11_Resultant_Acceleration_max=(Acceleration_persecond[10,:].max());Tag_11_Resultant_Acceleration_mean=(Acceleration_persecond[10,:].mean());
                Resultant_Acceleration_max=numpy.vstack([Tag_1_Resultant_Acceleration_max,Tag_2_Resultant_Acceleration_max,Tag_3_Resultant_Acceleration_max,Tag_4_Resultant_Acceleration_max,
                                                 Tag_5_Resultant_Acceleration_max,Tag_6_Resultant_Acceleration_max,Tag_7_Resultant_Acceleration_max,Tag_8_Resultant_Acceleration_max,
                                                 Tag_9_Resultant_Acceleration_max,Tag_10_Resultant_Acceleration_max,Tag_11_Resultant_Acceleration_max])
                Resultant_Acceleration_mean=numpy.vstack([Tag_1_Resultant_Acceleration_mean,Tag_2_Resultant_Acceleration_mean,Tag_3_Resultant_Acceleration_mean,Tag_4_Resultant_Acceleration_mean,
                                                 Tag_5_Resultant_Acceleration_mean,Tag_6_Resultant_Acceleration_mean,Tag_7_Resultant_Acceleration_mean,Tag_8_Resultant_Acceleration_mean,
                                                 Tag_9_Resultant_Acceleration_mean,Tag_10_Resultant_Acceleration_mean,Tag_11_Resultant_Acceleration_mean])         
            else:
                pass
            if len(Tag_12_Acceleration_persecond)>0:
                Tag_2_Acceleration_persecond=Tag_2_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_3_Acceleration_persecond=Tag_3_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_4_Acceleration_persecond=Tag_4_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_5_Acceleration_persecond=Tag_5_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_6_Acceleration_persecond=Tag_6_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_7_Acceleration_persecond=Tag_7_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_8_Acceleration_persecond=Tag_8_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_9_Acceleration_persecond=Tag_9_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_10_Acceleration_persecond=Tag_10_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_11_Acceleration_persecond=Tag_11_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_12_Acceleration_persecond=Tag_12_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Acceleration_persecond=numpy.vstack([Tag_1_Acceleration_persecond,Tag_2_Acceleration_persecond,Tag_3_Acceleration_persecond,Tag_4_Acceleration_persecond,
                                                 Tag_5_Acceleration_persecond,Tag_6_Acceleration_persecond,Tag_7_Acceleration_persecond,Tag_8_Acceleration_persecond,
                                                 Tag_9_Acceleration_persecond,Tag_10_Acceleration_persecond,Tag_11_Acceleration_persecond,Tag_12_Acceleration_persecond])
                Tag_2_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_2_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                Tag_3_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_3_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                Tag_4_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_4_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                Tag_5_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_5_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                Tag_6_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_6_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                Tag_7_Resultant_Acceleration_max=(Acceleration_persecond[6,:].max());Tag_7_Resultant_Acceleration_mean=(Acceleration_persecond[6,:].mean());
                Tag_8_Resultant_Acceleration_max=(Acceleration_persecond[7,:].max());Tag_8_Resultant_Acceleration_mean=(Acceleration_persecond[7,:].mean());
                Tag_9_Resultant_Acceleration_max=(Acceleration_persecond[8,:].max());Tag_9_Resultant_Acceleration_mean=(Acceleration_persecond[8,:].mean());
                Tag_10_Resultant_Acceleration_max=(Acceleration_persecond[9,:].max());Tag_10_Resultant_Acceleration_mean=(Acceleration_persecond[9,:].mean());
                Tag_11_Resultant_Acceleration_max=(Acceleration_persecond[10,:].max());Tag_11_Resultant_Acceleration_mean=(Acceleration_persecond[10,:].mean());
                Tag_12_Resultant_Acceleration_max=(Acceleration_persecond[11,:].max());Tag_12_Resultant_Acceleration_mean=(Acceleration_persecond[11,:].mean());
                Resultant_Acceleration_max=numpy.vstack([Tag_1_Resultant_Acceleration_max,Tag_2_Resultant_Acceleration_max,Tag_3_Resultant_Acceleration_max,Tag_4_Resultant_Acceleration_max,
                                                 Tag_5_Resultant_Acceleration_max,Tag_6_Resultant_Acceleration_max,Tag_7_Resultant_Acceleration_max,Tag_8_Resultant_Acceleration_max,
                                                 Tag_9_Resultant_Acceleration_max,Tag_10_Resultant_Acceleration_max,Tag_11_Resultant_Acceleration_max,Tag_12_Resultant_Acceleration_max])
                Resultant_Acceleration_mean=numpy.vstack([Tag_1_Resultant_Acceleration_mean,Tag_2_Resultant_Acceleration_mean,Tag_3_Resultant_Acceleration_mean,Tag_4_Resultant_Acceleration_mean,
                                                 Tag_5_Resultant_Acceleration_mean,Tag_6_Resultant_Acceleration_mean,Tag_7_Resultant_Acceleration_mean,Tag_8_Resultant_Acceleration_mean,
                                                 Tag_9_Resultant_Acceleration_mean,Tag_10_Resultant_Acceleration_mean,Tag_11_Resultant_Acceleration_mean,Tag_12_Resultant_Acceleration_mean])
            else:
                pass
            if len(Tag_13_Acceleration_persecond)>0:
                Tag_2_Acceleration_persecond=Tag_2_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_3_Acceleration_persecond=Tag_3_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_4_Acceleration_persecond=Tag_4_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_5_Acceleration_persecond=Tag_5_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_6_Acceleration_persecond=Tag_6_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_7_Acceleration_persecond=Tag_7_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_8_Acceleration_persecond=Tag_8_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_9_Acceleration_persecond=Tag_9_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_10_Acceleration_persecond=Tag_10_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_11_Acceleration_persecond=Tag_11_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_12_Acceleration_persecond=Tag_12_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_13_Acceleration_persecond=Tag_13_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Acceleration_persecond=numpy.vstack([Tag_1_Acceleration_persecond,Tag_2_Acceleration_persecond,Tag_3_Acceleration_persecond,Tag_4_Acceleration_persecond,
                                                 Tag_5_Acceleration_persecond,Tag_6_Acceleration_persecond,Tag_7_Acceleration_persecond,Tag_8_Acceleration_persecond,
                                                 Tag_9_Acceleration_persecond,Tag_10_Acceleration_persecond,Tag_11_Acceleration_persecond,Tag_12_Acceleration_persecond,
                                                 Tag_13_Acceleration_persecond])
                Tag_2_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_2_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                Tag_3_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_3_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                Tag_4_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_4_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                Tag_5_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_5_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                Tag_6_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_6_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                Tag_7_Resultant_Acceleration_max=(Acceleration_persecond[6,:].max());Tag_7_Resultant_Acceleration_mean=(Acceleration_persecond[6,:].mean());
                Tag_8_Resultant_Acceleration_max=(Acceleration_persecond[7,:].max());Tag_8_Resultant_Acceleration_mean=(Acceleration_persecond[7,:].mean());
                Tag_9_Resultant_Acceleration_max=(Acceleration_persecond[8,:].max());Tag_9_Resultant_Acceleration_mean=(Acceleration_persecond[8,:].mean());
                Tag_10_Resultant_Acceleration_max=(Acceleration_persecond[9,:].max());Tag_10_Resultant_Acceleration_mean=(Acceleration_persecond[9,:].mean());
                Tag_11_Resultant_Acceleration_max=(Acceleration_persecond[10,:].max());Tag_11_Resultant_Acceleration_mean=(Acceleration_persecond[10,:].mean());
                Tag_12_Resultant_Acceleration_max=(Acceleration_persecond[11,:].max());Tag_12_Resultant_Acceleration_mean=(Acceleration_persecond[11,:].mean());
                Tag_13_Resultant_Acceleration_max=(Acceleration_persecond[12,:].max());Tag_13_Resultant_Acceleration_mean=(Acceleration_persecond[12,:].mean());
                Resultant_Acceleration_max=numpy.vstack([Tag_1_Resultant_Acceleration_max,Tag_2_Resultant_Acceleration_max,Tag_3_Resultant_Acceleration_max,Tag_4_Resultant_Acceleration_max,
                                                 Tag_5_Resultant_Acceleration_max,Tag_6_Resultant_Acceleration_max,Tag_7_Resultant_Acceleration_max,Tag_8_Resultant_Acceleration_max,
                                                 Tag_9_Resultant_Acceleration_max,Tag_10_Resultant_Acceleration_max,Tag_11_Resultant_Acceleration_max,Tag_12_Resultant_Acceleration_max,
                                                 Tag_13_Resultant_Acceleration_max])
                Resultant_Acceleration_mean=numpy.vstack([Tag_1_Resultant_Acceleration_mean,Tag_2_Resultant_Acceleration_mean,Tag_3_Resultant_Acceleration_mean,Tag_4_Resultant_Acceleration_mean,
                                                 Tag_5_Resultant_Acceleration_mean,Tag_6_Resultant_Acceleration_mean,Tag_7_Resultant_Acceleration_mean,Tag_8_Resultant_Acceleration_mean,
                                                 Tag_9_Resultant_Acceleration_mean,Tag_10_Resultant_Acceleration_mean,Tag_11_Resultant_Acceleration_mean,Tag_12_Resultant_Acceleration_mean,
                                                 Tag_13_Resultant_Acceleration_mean])
            else:
                pass
            if len(Tag_14_Acceleration_persecond)>0:
                Tag_2_Acceleration_persecond=Tag_2_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_3_Acceleration_persecond=Tag_3_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_4_Acceleration_persecond=Tag_4_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_5_Acceleration_persecond=Tag_5_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_6_Acceleration_persecond=Tag_6_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_7_Acceleration_persecond=Tag_7_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_8_Acceleration_persecond=Tag_8_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_9_Acceleration_persecond=Tag_9_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_10_Acceleration_persecond=Tag_10_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_11_Acceleration_persecond=Tag_11_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_12_Acceleration_persecond=Tag_12_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_13_Acceleration_persecond=Tag_13_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Tag_14_Acceleration_persecond=Tag_14_Acceleration_persecond[:,:Tag_1_Acceleration_persecond.size];
                Acceleration_persecond=numpy.vstack([Tag_1_Acceleration_persecond,Tag_2_Acceleration_persecond,Tag_3_Acceleration_persecond,Tag_4_Acceleration_persecond,
                                                 Tag_5_Acceleration_persecond,Tag_6_Acceleration_persecond,Tag_7_Acceleration_persecond,Tag_8_Acceleration_persecond,
                                                 Tag_9_Acceleration_persecond,Tag_10_Acceleration_persecond,Tag_11_Acceleration_persecond,Tag_12_Acceleration_persecond,
                                                 Tag_13_Acceleration_persecond,Tag_14_Acceleration_persecond])
                Tag_2_Resultant_Acceleration_max=(Acceleration_persecond[1,:].max());Tag_2_Resultant_Acceleration_mean=(Acceleration_persecond[1,:].mean());
                Tag_3_Resultant_Acceleration_max=(Acceleration_persecond[2,:].max());Tag_3_Resultant_Acceleration_mean=(Acceleration_persecond[2,:].mean());
                Tag_4_Resultant_Acceleration_max=(Acceleration_persecond[3,:].max());Tag_4_Resultant_Acceleration_mean=(Acceleration_persecond[3,:].mean());
                Tag_5_Resultant_Acceleration_max=(Acceleration_persecond[4,:].max());Tag_5_Resultant_Acceleration_mean=(Acceleration_persecond[4,:].mean());
                Tag_6_Resultant_Acceleration_max=(Acceleration_persecond[5,:].max());Tag_6_Resultant_Acceleration_mean=(Acceleration_persecond[5,:].mean());
                Tag_7_Resultant_Acceleration_max=(Acceleration_persecond[6,:].max());Tag_7_Resultant_Acceleration_mean=(Acceleration_persecond[6,:].mean());
                Tag_8_Resultant_Acceleration_max=(Acceleration_persecond[7,:].max());Tag_8_Resultant_Acceleration_mean=(Acceleration_persecond[7,:].mean());
                Tag_9_Resultant_Acceleration_max=(Acceleration_persecond[8,:].max());Tag_9_Resultant_Acceleration_mean=(Acceleration_persecond[8,:].mean());
                Tag_10_Resultant_Acceleration_max=(Acceleration_persecond[9,:].max());Tag_10_Resultant_Acceleration_mean=(Acceleration_persecond[9,:].mean());
                Tag_11_Resultant_Acceleration_max=(Acceleration_persecond[10,:].max());Tag_11_Resultant_Acceleration_mean=(Acceleration_persecond[10,:].mean());
                Tag_12_Resultant_Acceleration_max=(Acceleration_persecond[11,:].max());Tag_12_Resultant_Acceleration_mean=(Acceleration_persecond[11,:].mean());
                Tag_13_Resultant_Acceleration_max=(Acceleration_persecond[12,:].max());Tag_13_Resultant_Acceleration_mean=(Acceleration_persecond[12,:].mean());
                Tag_14_Resultant_Acceleration_max=(Acceleration_persecond[13,:].max());Tag_14_Resultant_Acceleration_mean=(Acceleration_persecond[13,:].mean());
                Resultant_Acceleration_max=numpy.vstack([Tag_1_Resultant_Acceleration_max,Tag_2_Resultant_Acceleration_max,Tag_3_Resultant_Acceleration_max,Tag_4_Resultant_Acceleration_max,
                                                 Tag_5_Resultant_Acceleration_max,Tag_6_Resultant_Acceleration_max,Tag_7_Resultant_Acceleration_max,Tag_8_Resultant_Acceleration_max,
                                                 Tag_9_Resultant_Acceleration_max,Tag_10_Resultant_Acceleration_max,Tag_11_Resultant_Acceleration_max,Tag_12_Resultant_Acceleration_max,
                                                 Tag_13_Resultant_Acceleration_max,Tag_14_Resultant_Acceleration_max])
                Resultant_Acceleration_mean=numpy.vstack([Tag_1_Resultant_Acceleration_mean,Tag_2_Resultant_Acceleration_mean,Tag_3_Resultant_Acceleration_mean,Tag_4_Resultant_Acceleration_mean,
                                                 Tag_5_Resultant_Acceleration_mean,Tag_6_Resultant_Acceleration_mean,Tag_7_Resultant_Acceleration_mean,Tag_8_Resultant_Acceleration_mean,
                                                 Tag_9_Resultant_Acceleration_mean,Tag_10_Resultant_Acceleration_mean,Tag_11_Resultant_Acceleration_mean,Tag_12_Resultant_Acceleration_mean,
                                                 Tag_13_Resultant_Acceleration_mean,Tag_14_Resultant_Acceleration_mean])
            else:
                pass
  #          print("4 ok") 
###speed transforms ###
            Tag_1_Speed_persecond=numpy.array(Tag_1_Speed_persecond,dtype=numpy.float64);Tag_1_Speed_persecond=numpy.transpose(Tag_1_Speed_persecond);
            Tag_2_Speed_persecond=numpy.array(Tag_2_Speed_persecond,dtype=numpy.float64);Tag_2_Speed_persecond=numpy.transpose(Tag_2_Speed_persecond);             
            Tag_3_Speed_persecond=numpy.array(Tag_3_Speed_persecond,dtype=numpy.float64);Tag_3_Speed_persecond=numpy.transpose(Tag_3_Speed_persecond);
            Tag_4_Speed_persecond=numpy.array(Tag_4_Speed_persecond,dtype=numpy.float64);Tag_4_Speed_persecond=numpy.transpose(Tag_4_Speed_persecond);             
            Tag_5_Speed_persecond=numpy.array(Tag_5_Speed_persecond,dtype=numpy.float64);Tag_5_Speed_persecond=numpy.transpose(Tag_5_Speed_persecond);             
            Tag_6_Speed_persecond=numpy.array(Tag_6_Speed_persecond,dtype=numpy.float64);Tag_6_Speed_persecond=numpy.transpose(Tag_6_Speed_persecond);
            Tag_7_Speed_persecond=numpy.array(Tag_7_Speed_persecond,dtype=numpy.float64);Tag_7_Speed_persecond=numpy.transpose(Tag_7_Speed_persecond);             
            Tag_8_Speed_persecond=numpy.array(Tag_8_Speed_persecond,dtype=numpy.float64);Tag_8_Speed_persecond=numpy.transpose(Tag_8_Speed_persecond);             
            Tag_9_Speed_persecond=numpy.array(Tag_9_Speed_persecond,dtype=numpy.float64);Tag_9_Speed_persecond=numpy.transpose(Tag_9_Speed_persecond);
            Tag_10_Speed_persecond=numpy.array(Tag_10_Speed_persecond,dtype=numpy.float64);Tag_10_Speed_persecond=numpy.transpose(Tag_10_Speed_persecond);             
            Tag_11_Speed_persecond=numpy.array(Tag_11_Speed_persecond,dtype=numpy.float64);Tag_11_Speed_persecond=numpy.transpose(Tag_11_Speed_persecond);             
            Tag_12_Speed_persecond=numpy.array(Tag_12_Speed_persecond,dtype=numpy.float64);Tag_12_Speed_persecond=numpy.transpose(Tag_12_Speed_persecond);
            Tag_13_Speed_persecond=numpy.array(Tag_13_Speed_persecond,dtype=numpy.float64);Tag_13_Speed_persecond=numpy.transpose(Tag_13_Speed_persecond);             
            Tag_14_Speed_persecond=numpy.array(Tag_14_Speed_persecond,dtype=numpy.float64);Tag_14_Speed_persecond=numpy.transpose(Tag_14_Speed_persecond);             

            Tag_1_Speed_persecond=Tag_1_Speed_persecond[:,:Time_one.size-1];
            Speed_persecond=Tag_1_Speed_persecond
            Tag_1_Resultant_Speed_max=(Speed_persecond[0,:].max())
            Tag_1_Resultant_Speed_mean=(Speed_persecond[0,:].mean())
            Resultant_Speed_max=Tag_1_Resultant_Speed_max
            Resultant_Speed_mean=Tag_1_Resultant_Speed_mean
            
            if len(Tag_2_Speed_persecond)>0:
                Tag_2_Speed_persecond=Tag_2_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Speed_persecond=numpy.vstack([Tag_1_Speed_persecond,Tag_2_Speed_persecond])
                Tag_2_Resultant_Speed_max=(Speed_persecond[1,:].max())
                Tag_2_Resultant_Speed_mean=(Speed_persecond[1,:].mean())
                Resultant_Speed_max=numpy.vstack([Tag_1_Resultant_Speed_max,Tag_2_Resultant_Speed_max])
                Resultant_Speed_mean=numpy.vstack([Tag_1_Resultant_Speed_mean,Tag_2_Resultant_Speed_mean])
            else:
                pass
            if len(Tag_3_Speed_persecond)>0:
                Tag_2_Speed_persecond=Tag_2_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_3_Speed_persecond=Tag_3_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Speed_persecond=numpy.vstack([Tag_1_Speed_persecond,Tag_2_Speed_persecond,Tag_3_Speed_persecond])
                Tag_2_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_2_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                Tag_3_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_3_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                Resultant_Speed_max=numpy.vstack([Tag_1_Resultant_Speed_max,Tag_2_Resultant_Speed_max,Tag_3_Resultant_Speed_max])
                Resultant_Speed_mean=numpy.vstack([Tag_1_Resultant_Speed_mean,Tag_2_Resultant_Speed_mean,Tag_3_Resultant_Speed_mean])
            else:
                pass
            if len(Tag_4_Speed_persecond)>0:
                Tag_2_Speed_persecond=Tag_2_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_3_Speed_persecond=Tag_3_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_4_Speed_persecond=Tag_4_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Speed_persecond=numpy.vstack([Tag_1_Speed_persecond,Tag_2_Speed_persecond,Tag_3_Speed_persecond,Tag_4_Speed_persecond])
                Tag_2_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_2_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                Tag_3_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_3_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                Tag_4_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_4_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                Resultant_Speed_max=numpy.vstack([Tag_1_Resultant_Speed_max,Tag_2_Resultant_Speed_max,Tag_3_Resultant_Speed_max,Tag_4_Resultant_Speed_max])
                Resultant_Speed_mean=numpy.vstack([Tag_1_Resultant_Speed_mean,Tag_2_Resultant_Speed_mean,Tag_3_Resultant_Speed_mean,Tag_4_Resultant_Speed_mean])
            else:
                pass
            if len(Tag_5_Speed_persecond)>0:
                Tag_2_Speed_persecond=Tag_2_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_3_Speed_persecond=Tag_3_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_4_Speed_persecond=Tag_4_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_5_Speed_persecond=Tag_5_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Speed_persecond=numpy.vstack([Tag_1_Speed_persecond,Tag_2_Speed_persecond,Tag_3_Speed_persecond,Tag_4_Speed_persecond,
                                                 Tag_5_Speed_persecond])
                Tag_2_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_2_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                Tag_3_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_3_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                Tag_4_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_4_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                Tag_5_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_5_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                Resultant_Speed_max=numpy.vstack([Tag_1_Resultant_Speed_max,Tag_2_Resultant_Speed_max,Tag_3_Resultant_Speed_max,Tag_4_Resultant_Speed_max,
                                                 Tag_5_Resultant_Speed_max])
                Resultant_Speed_mean=numpy.vstack([Tag_1_Resultant_Speed_mean,Tag_2_Resultant_Speed_mean,Tag_3_Resultant_Speed_mean,Tag_4_Resultant_Speed_mean,
                                                 Tag_5_Resultant_Speed_mean])
            else:
                pass
            if len(Tag_6_Speed_persecond)>0:
                Tag_2_Speed_persecond=Tag_2_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_3_Speed_persecond=Tag_3_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_4_Speed_persecond=Tag_4_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_5_Speed_persecond=Tag_5_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_6_Speed_persecond=Tag_6_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Speed_persecond=numpy.vstack([Tag_1_Speed_persecond,Tag_2_Speed_persecond,Tag_3_Speed_persecond,Tag_4_Speed_persecond,
                                                 Tag_5_Speed_persecond,Tag_6_Speed_persecond])
                Tag_2_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_2_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                Tag_3_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_3_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                Tag_4_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_4_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                Tag_5_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_5_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                Tag_6_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_6_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                Resultant_Speed_max=numpy.vstack([Tag_1_Resultant_Speed_max,Tag_2_Resultant_Speed_max,Tag_3_Resultant_Speed_max,Tag_4_Resultant_Speed_max,
                                                 Tag_5_Resultant_Speed_max,Tag_6_Resultant_Speed_max])
                Resultant_Speed_mean=numpy.vstack([Tag_1_Resultant_Speed_mean,Tag_2_Resultant_Speed_mean,Tag_3_Resultant_Speed_mean,Tag_4_Resultant_Speed_mean,
                                                 Tag_5_Resultant_Speed_mean,Tag_6_Resultant_Speed_mean])
            else:
                pass
            if len(Tag_7_Speed_persecond)>0:
                Tag_2_Speed_persecond=Tag_2_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_3_Speed_persecond=Tag_3_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_4_Speed_persecond=Tag_4_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_5_Speed_persecond=Tag_5_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_6_Speed_persecond=Tag_6_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_7_Speed_persecond=Tag_7_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Speed_persecond=numpy.vstack([Tag_1_Speed_persecond,Tag_2_Speed_persecond,Tag_3_Speed_persecond,Tag_4_Speed_persecond,
                                                 Tag_5_Speed_persecond,Tag_6_Speed_persecond,Tag_7_Speed_persecond])
                Tag_2_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_2_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                Tag_3_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_3_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                Tag_4_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_4_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                Tag_5_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_5_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                Tag_6_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_6_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                Tag_7_Resultant_Speed_max=(Speed_persecond[6,:].max());Tag_7_Resultant_Speed_mean=(Speed_persecond[6,:].mean());
                Resultant_Speed_max=numpy.vstack([Tag_1_Resultant_Speed_max,Tag_2_Resultant_Speed_max,Tag_3_Resultant_Speed_max,Tag_4_Resultant_Speed_max,
                                                 Tag_5_Resultant_Speed_max,Tag_6_Resultant_Speed_max,Tag_7_Resultant_Speed_max])
                Resultant_Speed_mean=numpy.vstack([Tag_1_Resultant_Speed_mean,Tag_2_Resultant_Speed_mean,Tag_3_Resultant_Speed_mean,Tag_4_Resultant_Speed_mean,
                                                 Tag_5_Resultant_Speed_mean,Tag_6_Resultant_Speed_mean,Tag_7_Resultant_Speed_mean])
 
            else:
                pass
            if len(Tag_8_Speed_persecond)>0:
                Tag_2_Speed_persecond=Tag_2_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_3_Speed_persecond=Tag_3_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_4_Speed_persecond=Tag_4_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_5_Speed_persecond=Tag_5_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_6_Speed_persecond=Tag_6_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_7_Speed_persecond=Tag_7_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_8_Speed_persecond=Tag_8_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Speed_persecond=numpy.vstack([Tag_1_Speed_persecond,Tag_2_Speed_persecond,Tag_3_Speed_persecond,Tag_4_Speed_persecond,
                                                 Tag_5_Speed_persecond,Tag_6_Speed_persecond,Tag_7_Speed_persecond,Tag_8_Speed_persecond])
                Tag_2_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_2_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                Tag_3_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_3_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                Tag_4_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_4_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                Tag_5_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_5_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                Tag_6_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_6_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                Tag_7_Resultant_Speed_max=(Speed_persecond[6,:].max());Tag_7_Resultant_Speed_mean=(Speed_persecond[6,:].mean());
                Tag_8_Resultant_Speed_max=(Speed_persecond[7,:].max());Tag_8_Resultant_Speed_mean=(Speed_persecond[7,:].mean());
                Resultant_Speed_max=numpy.vstack([Tag_1_Resultant_Speed_max,Tag_2_Resultant_Speed_max,Tag_3_Resultant_Speed_max,Tag_4_Resultant_Speed_max,
                                                 Tag_5_Resultant_Speed_max,Tag_6_Resultant_Speed_max,Tag_7_Resultant_Speed_max,Tag_8_Resultant_Speed_max])
                Resultant_Speed_mean=numpy.vstack([Tag_1_Resultant_Speed_mean,Tag_2_Resultant_Speed_mean,Tag_3_Resultant_Speed_mean,Tag_4_Resultant_Speed_mean,
                                                 Tag_5_Resultant_Speed_mean,Tag_6_Resultant_Speed_mean,Tag_7_Resultant_Speed_mean,Tag_8_Resultant_Speed_mean])
            else:
                pass
            if len(Tag_9_Speed_persecond)>0:
                Tag_2_Speed_persecond=Tag_2_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_3_Speed_persecond=Tag_3_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_4_Speed_persecond=Tag_4_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_5_Speed_persecond=Tag_5_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_6_Speed_persecond=Tag_6_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_7_Speed_persecond=Tag_7_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_8_Speed_persecond=Tag_8_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_9_Speed_persecond=Tag_9_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Speed_persecond=numpy.vstack([Tag_1_Speed_persecond,Tag_2_Speed_persecond,Tag_3_Speed_persecond,Tag_4_Speed_persecond,
                                                 Tag_5_Speed_persecond,Tag_6_Speed_persecond,Tag_7_Speed_persecond,Tag_8_Speed_persecond,
                                                 Tag_9_Speed_persecond])
                Tag_2_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_2_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                Tag_3_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_3_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                Tag_4_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_4_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                Tag_5_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_5_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                Tag_6_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_6_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                Tag_7_Resultant_Speed_max=(Speed_persecond[6,:].max());Tag_7_Resultant_Speed_mean=(Speed_persecond[6,:].mean());
                Tag_8_Resultant_Speed_max=(Speed_persecond[7,:].max());Tag_8_Resultant_Speed_mean=(Speed_persecond[7,:].mean());
                Tag_9_Resultant_Speed_max=(Speed_persecond[8,:].max());Tag_9_Resultant_Speed_mean=(Speed_persecond[8,:].mean());
                Resultant_Speed_max=numpy.vstack([Tag_1_Resultant_Speed_max,Tag_2_Resultant_Speed_max,Tag_3_Resultant_Speed_max,Tag_4_Resultant_Speed_max,
                                                 Tag_5_Resultant_Speed_max,Tag_6_Resultant_Speed_max,Tag_7_Resultant_Speed_max,Tag_8_Resultant_Speed_max,
                                                 Tag_9_Resultant_Speed_max])
                Resultant_Speed_mean=numpy.vstack([Tag_1_Resultant_Speed_mean,Tag_2_Resultant_Speed_mean,Tag_3_Resultant_Speed_mean,Tag_4_Resultant_Speed_mean,
                                                 Tag_5_Resultant_Speed_mean,Tag_6_Resultant_Speed_mean,Tag_7_Resultant_Speed_mean,Tag_8_Resultant_Speed_mean,
                                                 Tag_9_Resultant_Speed_mean])
            else:
                pass
            if len(Tag_10_Speed_persecond)>0:
                Tag_2_Speed_persecond=Tag_2_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_3_Speed_persecond=Tag_3_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_4_Speed_persecond=Tag_4_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_5_Speed_persecond=Tag_5_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_6_Speed_persecond=Tag_6_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_7_Speed_persecond=Tag_7_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_8_Speed_persecond=Tag_8_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_9_Speed_persecond=Tag_9_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_10_Speed_persecond=Tag_10_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Speed_persecond=numpy.vstack([Tag_1_Speed_persecond,Tag_2_Speed_persecond,Tag_3_Speed_persecond,Tag_4_Speed_persecond,
                                                 Tag_5_Speed_persecond,Tag_6_Speed_persecond,Tag_7_Speed_persecond,Tag_8_Speed_persecond,
                                                 Tag_9_Speed_persecond,Tag_10_Speed_persecond])
                Tag_2_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_2_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                Tag_3_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_3_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                Tag_4_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_4_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                Tag_5_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_5_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                Tag_6_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_6_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                Tag_7_Resultant_Speed_max=(Speed_persecond[6,:].max());Tag_7_Resultant_Speed_mean=(Speed_persecond[6,:].mean());
                Tag_8_Resultant_Speed_max=(Speed_persecond[7,:].max());Tag_8_Resultant_Speed_mean=(Speed_persecond[7,:].mean());
                Tag_9_Resultant_Speed_max=(Speed_persecond[8,:].max());Tag_9_Resultant_Speed_mean=(Speed_persecond[8,:].mean());
                Tag_10_Resultant_Speed_max=(Speed_persecond[9,:].max());Tag_10_Resultant_Speed_mean=(Speed_persecond[9,:].mean());
                Resultant_Speed_max=numpy.vstack([Tag_1_Resultant_Speed_max,Tag_2_Resultant_Speed_max,Tag_3_Resultant_Speed_max,Tag_4_Resultant_Speed_max,
                                                 Tag_5_Resultant_Speed_max,Tag_6_Resultant_Speed_max,Tag_7_Resultant_Speed_max,Tag_8_Resultant_Speed_max,
                                                 Tag_9_Resultant_Speed_max,Tag_10_Resultant_Speed_max])
                Resultant_Speed_mean=numpy.vstack([Tag_1_Resultant_Speed_mean,Tag_2_Resultant_Speed_mean,Tag_3_Resultant_Speed_mean,Tag_4_Resultant_Speed_mean,
                                                 Tag_5_Resultant_Speed_mean,Tag_6_Resultant_Speed_mean,Tag_7_Resultant_Speed_mean,Tag_8_Resultant_Speed_mean,
                                                 Tag_9_Resultant_Speed_mean,Tag_10_Resultant_Speed_mean])         
        
            else:
                pass
            if len(Tag_11_Speed_persecond)>0:
                Tag_2_Speed_persecond=Tag_2_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_3_Speed_persecond=Tag_3_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_4_Speed_persecond=Tag_4_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_5_Speed_persecond=Tag_5_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_6_Speed_persecond=Tag_6_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_7_Speed_persecond=Tag_7_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_8_Speed_persecond=Tag_8_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_9_Speed_persecond=Tag_9_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_10_Speed_persecond=Tag_10_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_11_Speed_persecond=Tag_11_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Speed_persecond=numpy.vstack([Tag_1_Speed_persecond,Tag_2_Speed_persecond,Tag_3_Speed_persecond,Tag_4_Speed_persecond,
                                                 Tag_5_Speed_persecond,Tag_6_Speed_persecond,Tag_7_Speed_persecond,Tag_8_Speed_persecond,
                                                 Tag_9_Speed_persecond,Tag_10_Speed_persecond,Tag_11_Speed_persecond])
                Tag_2_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_2_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                Tag_3_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_3_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                Tag_4_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_4_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                Tag_5_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_5_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                Tag_6_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_6_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                Tag_7_Resultant_Speed_max=(Speed_persecond[6,:].max());Tag_7_Resultant_Speed_mean=(Speed_persecond[6,:].mean());
                Tag_8_Resultant_Speed_max=(Speed_persecond[7,:].max());Tag_8_Resultant_Speed_mean=(Speed_persecond[7,:].mean());
                Tag_9_Resultant_Speed_max=(Speed_persecond[8,:].max());Tag_9_Resultant_Speed_mean=(Speed_persecond[8,:].mean());
                Tag_10_Resultant_Speed_max=(Speed_persecond[9,:].max());Tag_10_Resultant_Speed_mean=(Speed_persecond[9,:].mean());
                Tag_11_Resultant_Speed_max=(Speed_persecond[10,:].max());Tag_11_Resultant_Speed_mean=(Speed_persecond[10,:].mean());
                Resultant_Speed_max=numpy.vstack([Tag_1_Resultant_Speed_max,Tag_2_Resultant_Speed_max,Tag_3_Resultant_Speed_max,Tag_4_Resultant_Speed_max,
                                                 Tag_5_Resultant_Speed_max,Tag_6_Resultant_Speed_max,Tag_7_Resultant_Speed_max,Tag_8_Resultant_Speed_max,
                                                 Tag_9_Resultant_Speed_max,Tag_10_Resultant_Speed_max,Tag_11_Resultant_Speed_max])
                Resultant_Speed_mean=numpy.vstack([Tag_1_Resultant_Speed_mean,Tag_2_Resultant_Speed_mean,Tag_3_Resultant_Speed_mean,Tag_4_Resultant_Speed_mean,
                                                 Tag_5_Resultant_Speed_mean,Tag_6_Resultant_Speed_mean,Tag_7_Resultant_Speed_mean,Tag_8_Resultant_Speed_mean,
                                                 Tag_9_Resultant_Speed_mean,Tag_10_Resultant_Speed_mean,Tag_11_Resultant_Speed_mean])         
            else:
                pass
            if len(Tag_12_Speed_persecond)>0:
                Tag_2_Speed_persecond=Tag_2_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_3_Speed_persecond=Tag_3_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_4_Speed_persecond=Tag_4_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_5_Speed_persecond=Tag_5_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_6_Speed_persecond=Tag_6_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_7_Speed_persecond=Tag_7_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_8_Speed_persecond=Tag_8_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_9_Speed_persecond=Tag_9_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_10_Speed_persecond=Tag_10_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_11_Speed_persecond=Tag_11_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_12_Speed_persecond=Tag_12_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Speed_persecond=numpy.vstack([Tag_1_Speed_persecond,Tag_2_Speed_persecond,Tag_3_Speed_persecond,Tag_4_Speed_persecond,
                                                 Tag_5_Speed_persecond,Tag_6_Speed_persecond,Tag_7_Speed_persecond,Tag_8_Speed_persecond,
                                                 Tag_9_Speed_persecond,Tag_10_Speed_persecond,Tag_11_Speed_persecond,Tag_12_Speed_persecond])
                Tag_2_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_2_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                Tag_3_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_3_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                Tag_4_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_4_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                Tag_5_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_5_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                Tag_6_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_6_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                Tag_7_Resultant_Speed_max=(Speed_persecond[6,:].max());Tag_7_Resultant_Speed_mean=(Speed_persecond[6,:].mean());
                Tag_8_Resultant_Speed_max=(Speed_persecond[7,:].max());Tag_8_Resultant_Speed_mean=(Speed_persecond[7,:].mean());
                Tag_9_Resultant_Speed_max=(Speed_persecond[8,:].max());Tag_9_Resultant_Speed_mean=(Speed_persecond[8,:].mean());
                Tag_10_Resultant_Speed_max=(Speed_persecond[9,:].max());Tag_10_Resultant_Speed_mean=(Speed_persecond[9,:].mean());
                Tag_11_Resultant_Speed_max=(Speed_persecond[10,:].max());Tag_11_Resultant_Speed_mean=(Speed_persecond[10,:].mean());
                Tag_12_Resultant_Speed_max=(Speed_persecond[11,:].max());Tag_12_Resultant_Speed_mean=(Speed_persecond[11,:].mean());
                Resultant_Speed_max=numpy.vstack([Tag_1_Resultant_Speed_max,Tag_2_Resultant_Speed_max,Tag_3_Resultant_Speed_max,Tag_4_Resultant_Speed_max,
                                                 Tag_5_Resultant_Speed_max,Tag_6_Resultant_Speed_max,Tag_7_Resultant_Speed_max,Tag_8_Resultant_Speed_max,
                                                 Tag_9_Resultant_Speed_max,Tag_10_Resultant_Speed_max,Tag_11_Resultant_Speed_max,Tag_12_Resultant_Speed_max])
                Resultant_Speed_mean=numpy.vstack([Tag_1_Resultant_Speed_mean,Tag_2_Resultant_Speed_mean,Tag_3_Resultant_Speed_mean,Tag_4_Resultant_Speed_mean,
                                                 Tag_5_Resultant_Speed_mean,Tag_6_Resultant_Speed_mean,Tag_7_Resultant_Speed_mean,Tag_8_Resultant_Speed_mean,
                                                 Tag_9_Resultant_Speed_mean,Tag_10_Resultant_Speed_mean,Tag_11_Resultant_Speed_mean,Tag_12_Resultant_Speed_mean])
            else:
                pass
            if len(Tag_13_Speed_persecond)>0:
                Tag_2_Speed_persecond=Tag_2_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_3_Speed_persecond=Tag_3_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_4_Speed_persecond=Tag_4_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_5_Speed_persecond=Tag_5_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_6_Speed_persecond=Tag_6_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_7_Speed_persecond=Tag_7_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_8_Speed_persecond=Tag_8_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_9_Speed_persecond=Tag_9_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_10_Speed_persecond=Tag_10_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_11_Speed_persecond=Tag_11_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_12_Speed_persecond=Tag_12_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_13_Speed_persecond=Tag_13_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Speed_persecond=numpy.vstack([Tag_1_Speed_persecond,Tag_2_Speed_persecond,Tag_3_Speed_persecond,Tag_4_Speed_persecond,
                                                 Tag_5_Speed_persecond,Tag_6_Speed_persecond,Tag_7_Speed_persecond,Tag_8_Speed_persecond,
                                                 Tag_9_Speed_persecond,Tag_10_Speed_persecond,Tag_11_Speed_persecond,Tag_12_Speed_persecond,
                                                 Tag_13_Speed_persecond])
                Tag_2_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_2_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                Tag_3_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_3_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                Tag_4_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_4_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                Tag_5_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_5_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                Tag_6_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_6_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                Tag_7_Resultant_Speed_max=(Speed_persecond[6,:].max());Tag_7_Resultant_Speed_mean=(Speed_persecond[6,:].mean());
                Tag_8_Resultant_Speed_max=(Speed_persecond[7,:].max());Tag_8_Resultant_Speed_mean=(Speed_persecond[7,:].mean());
                Tag_9_Resultant_Speed_max=(Speed_persecond[8,:].max());Tag_9_Resultant_Speed_mean=(Speed_persecond[8,:].mean());
                Tag_10_Resultant_Speed_max=(Speed_persecond[9,:].max());Tag_10_Resultant_Speed_mean=(Speed_persecond[9,:].mean());
                Tag_11_Resultant_Speed_max=(Speed_persecond[10,:].max());Tag_11_Resultant_Speed_mean=(Speed_persecond[10,:].mean());
                Tag_12_Resultant_Speed_max=(Speed_persecond[11,:].max());Tag_12_Resultant_Speed_mean=(Speed_persecond[11,:].mean());
                Tag_13_Resultant_Speed_max=(Speed_persecond[12,:].max());Tag_13_Resultant_Speed_mean=(Speed_persecond[12,:].mean());
                Resultant_Speed_max=numpy.vstack([Tag_1_Resultant_Speed_max,Tag_2_Resultant_Speed_max,Tag_3_Resultant_Speed_max,Tag_4_Resultant_Speed_max,
                                                 Tag_5_Resultant_Speed_max,Tag_6_Resultant_Speed_max,Tag_7_Resultant_Speed_max,Tag_8_Resultant_Speed_max,
                                                 Tag_9_Resultant_Speed_max,Tag_10_Resultant_Speed_max,Tag_11_Resultant_Speed_max,Tag_12_Resultant_Speed_max,
                                                 Tag_13_Resultant_Speed_max])
                Resultant_Speed_mean=numpy.vstack([Tag_1_Resultant_Speed_mean,Tag_2_Resultant_Speed_mean,Tag_3_Resultant_Speed_mean,Tag_4_Resultant_Speed_mean,
                                                 Tag_5_Resultant_Speed_mean,Tag_6_Resultant_Speed_mean,Tag_7_Resultant_Speed_mean,Tag_8_Resultant_Speed_mean,
                                                 Tag_9_Resultant_Speed_mean,Tag_10_Resultant_Speed_mean,Tag_11_Resultant_Speed_mean,Tag_12_Resultant_Speed_mean,
                                                 Tag_13_Resultant_Speed_mean])
            else:
                pass
            if len(Tag_14_Speed_persecond)>0:
                Tag_2_Speed_persecond=Tag_2_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_3_Speed_persecond=Tag_3_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_4_Speed_persecond=Tag_4_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_5_Speed_persecond=Tag_5_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_6_Speed_persecond=Tag_6_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_7_Speed_persecond=Tag_7_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_8_Speed_persecond=Tag_8_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_9_Speed_persecond=Tag_9_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_10_Speed_persecond=Tag_10_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_11_Speed_persecond=Tag_11_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_12_Speed_persecond=Tag_12_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_13_Speed_persecond=Tag_13_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Tag_14_Speed_persecond=Tag_14_Speed_persecond[:,:Tag_1_Speed_persecond.size];
                Speed_persecond=numpy.vstack([Tag_1_Speed_persecond,Tag_2_Speed_persecond,Tag_3_Speed_persecond,Tag_4_Speed_persecond,
                                                 Tag_5_Speed_persecond,Tag_6_Speed_persecond,Tag_7_Speed_persecond,Tag_8_Speed_persecond,
                                                 Tag_9_Speed_persecond,Tag_10_Speed_persecond,Tag_11_Speed_persecond,Tag_12_Speed_persecond,
                                                 Tag_13_Speed_persecond,Tag_14_Speed_persecond])
                Tag_2_Resultant_Speed_max=(Speed_persecond[1,:].max());Tag_2_Resultant_Speed_mean=(Speed_persecond[1,:].mean());
                Tag_3_Resultant_Speed_max=(Speed_persecond[2,:].max());Tag_3_Resultant_Speed_mean=(Speed_persecond[2,:].mean());
                Tag_4_Resultant_Speed_max=(Speed_persecond[3,:].max());Tag_4_Resultant_Speed_mean=(Speed_persecond[3,:].mean());
                Tag_5_Resultant_Speed_max=(Speed_persecond[4,:].max());Tag_5_Resultant_Speed_mean=(Speed_persecond[4,:].mean());
                Tag_6_Resultant_Speed_max=(Speed_persecond[5,:].max());Tag_6_Resultant_Speed_mean=(Speed_persecond[5,:].mean());
                Tag_7_Resultant_Speed_max=(Speed_persecond[6,:].max());Tag_7_Resultant_Speed_mean=(Speed_persecond[6,:].mean());
                Tag_8_Resultant_Speed_max=(Speed_persecond[7,:].max());Tag_8_Resultant_Speed_mean=(Speed_persecond[7,:].mean());
                Tag_9_Resultant_Speed_max=(Speed_persecond[8,:].max());Tag_9_Resultant_Speed_mean=(Speed_persecond[8,:].mean());
                Tag_10_Resultant_Speed_max=(Speed_persecond[9,:].max());Tag_10_Resultant_Speed_mean=(Speed_persecond[9,:].mean());
                Tag_11_Resultant_Speed_max=(Speed_persecond[10,:].max());Tag_11_Resultant_Speed_mean=(Speed_persecond[10,:].mean());
                Tag_12_Resultant_Speed_max=(Speed_persecond[11,:].max());Tag_12_Resultant_Speed_mean=(Speed_persecond[11,:].mean());
                Tag_13_Resultant_Speed_max=(Speed_persecond[12,:].max());Tag_13_Resultant_Speed_mean=(Speed_persecond[12,:].mean());
                Tag_14_Resultant_Speed_max=(Speed_persecond[13,:].max());Tag_14_Resultant_Speed_mean=(Speed_persecond[13,:].mean());
                Resultant_Speed_max=numpy.vstack([Tag_1_Resultant_Speed_max,Tag_2_Resultant_Speed_max,Tag_3_Resultant_Speed_max,Tag_4_Resultant_Speed_max,
                                                 Tag_5_Resultant_Speed_max,Tag_6_Resultant_Speed_max,Tag_7_Resultant_Speed_max,Tag_8_Resultant_Speed_max,
                                                 Tag_9_Resultant_Speed_max,Tag_10_Resultant_Speed_max,Tag_11_Resultant_Speed_max,Tag_12_Resultant_Speed_max,
                                                 Tag_13_Resultant_Speed_max,Tag_14_Resultant_Speed_max])
                Resultant_Speed_mean=numpy.vstack([Tag_1_Resultant_Speed_mean,Tag_2_Resultant_Speed_mean,Tag_3_Resultant_Speed_mean,Tag_4_Resultant_Speed_mean,
                                                 Tag_5_Resultant_Speed_mean,Tag_6_Resultant_Speed_mean,Tag_7_Resultant_Speed_mean,Tag_8_Resultant_Speed_mean,
                                                 Tag_9_Resultant_Speed_mean,Tag_10_Resultant_Speed_mean,Tag_11_Resultant_Speed_mean,Tag_12_Resultant_Speed_mean,
                                                 Tag_13_Resultant_Speed_mean,Tag_14_Resultant_Speed_mean])
            else:
                pass
 ###result diff transforms ###
            Tag_1_Resultant_diff_persecond=numpy.array(Tag_1_Resultant_diff_persecond,dtype=numpy.float64);Tag_1_Resultant_diff_persecond=numpy.transpose(Tag_1_Resultant_diff_persecond);
            Tag_2_Resultant_diff_persecond=numpy.array(Tag_2_Resultant_diff_persecond,dtype=numpy.float64);Tag_2_Resultant_diff_persecond=numpy.transpose(Tag_2_Resultant_diff_persecond);             
            Tag_3_Resultant_diff_persecond=numpy.array(Tag_3_Resultant_diff_persecond,dtype=numpy.float64);Tag_3_Resultant_diff_persecond=numpy.transpose(Tag_3_Resultant_diff_persecond);
            Tag_4_Resultant_diff_persecond=numpy.array(Tag_4_Resultant_diff_persecond,dtype=numpy.float64);Tag_4_Resultant_diff_persecond=numpy.transpose(Tag_4_Resultant_diff_persecond);             
            Tag_5_Resultant_diff_persecond=numpy.array(Tag_5_Resultant_diff_persecond,dtype=numpy.float64);Tag_5_Resultant_diff_persecond=numpy.transpose(Tag_5_Resultant_diff_persecond);             
            Tag_6_Resultant_diff_persecond=numpy.array(Tag_6_Resultant_diff_persecond,dtype=numpy.float64);Tag_6_Resultant_diff_persecond=numpy.transpose(Tag_6_Resultant_diff_persecond);
            Tag_7_Resultant_diff_persecond=numpy.array(Tag_7_Resultant_diff_persecond,dtype=numpy.float64);Tag_7_Resultant_diff_persecond=numpy.transpose(Tag_7_Resultant_diff_persecond);             
            Tag_8_Resultant_diff_persecond=numpy.array(Tag_8_Resultant_diff_persecond,dtype=numpy.float64);Tag_8_Resultant_diff_persecond=numpy.transpose(Tag_8_Resultant_diff_persecond);             
            Tag_9_Resultant_diff_persecond=numpy.array(Tag_9_Resultant_diff_persecond,dtype=numpy.float64);Tag_9_Resultant_diff_persecond=numpy.transpose(Tag_9_Resultant_diff_persecond);
            Tag_10_Resultant_diff_persecond=numpy.array(Tag_10_Resultant_diff_persecond,dtype=numpy.float64);Tag_10_Resultant_diff_persecond=numpy.transpose(Tag_10_Resultant_diff_persecond);             
            Tag_11_Resultant_diff_persecond=numpy.array(Tag_11_Resultant_diff_persecond,dtype=numpy.float64);Tag_11_Resultant_diff_persecond=numpy.transpose(Tag_11_Resultant_diff_persecond);             
            Tag_12_Resultant_diff_persecond=numpy.array(Tag_12_Resultant_diff_persecond,dtype=numpy.float64);Tag_12_Resultant_diff_persecond=numpy.transpose(Tag_12_Resultant_diff_persecond);
            Tag_13_Resultant_diff_persecond=numpy.array(Tag_13_Resultant_diff_persecond,dtype=numpy.float64);Tag_13_Resultant_diff_persecond=numpy.transpose(Tag_13_Resultant_diff_persecond);             
            Tag_14_Resultant_diff_persecond=numpy.array(Tag_14_Resultant_diff_persecond,dtype=numpy.float64);Tag_14_Resultant_diff_persecond=numpy.transpose(Tag_14_Resultant_diff_persecond);             

            Tag_1_Resultant_diff_persecond=Tag_1_Resultant_diff_persecond[:,:Time_one.size-1];
            Resultant_diff_persecond=Tag_1_Resultant_diff_persecond
            Tag_1_Resultant_diff_max=(Resultant_diff_persecond[0,:].max())
            Tag_1_Resultant_diff_mean=(Resultant_diff_persecond[0,:].mean())
            Resultant_diff_max=Tag_1_Resultant_diff_max
            Resultant_diff_mean=Tag_1_Resultant_diff_mean
            
            if len(Tag_2_Resultant_diff_persecond)>0:
                Tag_2_Resultant_diff_persecond=Tag_2_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Resultant_diff_persecond=numpy.vstack([Tag_1_Resultant_diff_persecond,Tag_2_Resultant_diff_persecond])
                Tag_2_Resultant_diff_max=(Resultant_diff_persecond[1,:].max())
                Tag_2_Resultant_diff_mean=(Resultant_diff_persecond[1,:].mean())
                Resultant_diff_max=numpy.vstack([Tag_1_Resultant_diff_max,Tag_2_Resultant_diff_max])
                Resultant_diff_mean=numpy.vstack([Tag_1_Resultant_diff_mean,Tag_2_Resultant_diff_mean])
            else:
                pass
            if len(Tag_3_Resultant_diff_persecond)>0:
                Tag_2_Resultant_diff_persecond=Tag_2_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_3_Resultant_diff_persecond=Tag_3_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Resultant_diff_persecond=numpy.vstack([Tag_1_Resultant_diff_persecond,Tag_2_Resultant_diff_persecond,Tag_3_Resultant_diff_persecond])
                Tag_2_Resultant_diff_max=(Resultant_diff_persecond[1,:].max());Tag_2_Resultant_diff_mean=(Resultant_diff_persecond[1,:].mean());
                Tag_3_Resultant_diff_max=(Resultant_diff_persecond[2,:].max());Tag_3_Resultant_diff_mean=(Resultant_diff_persecond[2,:].mean());
                Resultant_diff_max=numpy.vstack([Tag_1_Resultant_diff_max,Tag_2_Resultant_diff_max,Tag_3_Resultant_diff_max])
                Resultant_diff_mean=numpy.vstack([Tag_1_Resultant_diff_mean,Tag_2_Resultant_diff_mean,Tag_3_Resultant_diff_mean])
            else:
                pass
            if len(Tag_4_Resultant_diff_persecond)>0:
                Tag_2_Resultant_diff_persecond=Tag_2_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_3_Resultant_diff_persecond=Tag_3_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_4_Resultant_diff_persecond=Tag_4_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Resultant_diff_persecond=numpy.vstack([Tag_1_Resultant_diff_persecond,Tag_2_Resultant_diff_persecond,Tag_3_Resultant_diff_persecond,Tag_4_Resultant_diff_persecond])
                Tag_2_Resultant_diff_max=(Resultant_diff_persecond[1,:].max());Tag_2_Resultant_diff_mean=(Resultant_diff_persecond[1,:].mean());
                Tag_3_Resultant_diff_max=(Resultant_diff_persecond[2,:].max());Tag_3_Resultant_diff_mean=(Resultant_diff_persecond[2,:].mean());
                Tag_4_Resultant_diff_max=(Resultant_diff_persecond[3,:].max());Tag_4_Resultant_diff_mean=(Resultant_diff_persecond[3,:].mean());
                Resultant_diff_max=numpy.vstack([Tag_1_Resultant_diff_max,Tag_2_Resultant_diff_max,Tag_3_Resultant_diff_max,Tag_4_Resultant_diff_max])
                Resultant_diff_mean=numpy.vstack([Tag_1_Resultant_diff_mean,Tag_2_Resultant_diff_mean,Tag_3_Resultant_diff_mean,Tag_4_Resultant_diff_mean])
            else:
                pass
            if len(Tag_5_Resultant_diff_persecond)>0:
                Tag_2_Resultant_diff_persecond=Tag_2_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_3_Resultant_diff_persecond=Tag_3_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_4_Resultant_diff_persecond=Tag_4_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_5_Resultant_diff_persecond=Tag_5_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Resultant_diff_persecond=numpy.vstack([Tag_1_Resultant_diff_persecond,Tag_2_Resultant_diff_persecond,Tag_3_Resultant_diff_persecond,Tag_4_Resultant_diff_persecond,
                                                 Tag_5_Resultant_diff_persecond])
                Tag_2_Resultant_diff_max=(Resultant_diff_persecond[1,:].max());Tag_2_Resultant_diff_mean=(Resultant_diff_persecond[1,:].mean());
                Tag_3_Resultant_diff_max=(Resultant_diff_persecond[2,:].max());Tag_3_Resultant_diff_mean=(Resultant_diff_persecond[2,:].mean());
                Tag_4_Resultant_diff_max=(Resultant_diff_persecond[3,:].max());Tag_4_Resultant_diff_mean=(Resultant_diff_persecond[3,:].mean());
                Tag_5_Resultant_diff_max=(Resultant_diff_persecond[4,:].max());Tag_5_Resultant_diff_mean=(Resultant_diff_persecond[4,:].mean());
                Resultant_diff_max=numpy.vstack([Tag_1_Resultant_diff_max,Tag_2_Resultant_diff_max,Tag_3_Resultant_diff_max,Tag_4_Resultant_diff_max,
                                                 Tag_5_Resultant_diff_max])
                Resultant_diff_mean=numpy.vstack([Tag_1_Resultant_diff_mean,Tag_2_Resultant_diff_mean,Tag_3_Resultant_diff_mean,Tag_4_Resultant_diff_mean,
                                                 Tag_5_Resultant_diff_mean])
            else:
                pass
            if len(Tag_6_Resultant_diff_persecond)>0:
                Tag_2_Resultant_diff_persecond=Tag_2_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_3_Resultant_diff_persecond=Tag_3_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_4_Resultant_diff_persecond=Tag_4_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_5_Resultant_diff_persecond=Tag_5_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_6_Resultant_diff_persecond=Tag_6_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Resultant_diff_persecond=numpy.vstack([Tag_1_Resultant_diff_persecond,Tag_2_Resultant_diff_persecond,Tag_3_Resultant_diff_persecond,Tag_4_Resultant_diff_persecond,
                                                 Tag_5_Resultant_diff_persecond,Tag_6_Resultant_diff_persecond])
                Tag_2_Resultant_diff_max=(Resultant_diff_persecond[1,:].max());Tag_2_Resultant_diff_mean=(Resultant_diff_persecond[1,:].mean());
                Tag_3_Resultant_diff_max=(Resultant_diff_persecond[2,:].max());Tag_3_Resultant_diff_mean=(Resultant_diff_persecond[2,:].mean());
                Tag_4_Resultant_diff_max=(Resultant_diff_persecond[3,:].max());Tag_4_Resultant_diff_mean=(Resultant_diff_persecond[3,:].mean());
                Tag_5_Resultant_diff_max=(Resultant_diff_persecond[4,:].max());Tag_5_Resultant_diff_mean=(Resultant_diff_persecond[4,:].mean());
                Tag_6_Resultant_diff_max=(Resultant_diff_persecond[5,:].max());Tag_6_Resultant_diff_mean=(Resultant_diff_persecond[5,:].mean());
                Resultant_diff_max=numpy.vstack([Tag_1_Resultant_diff_max,Tag_2_Resultant_diff_max,Tag_3_Resultant_diff_max,Tag_4_Resultant_diff_max,
                                                 Tag_5_Resultant_diff_max,Tag_6_Resultant_diff_max])
                Resultant_diff_mean=numpy.vstack([Tag_1_Resultant_diff_mean,Tag_2_Resultant_diff_mean,Tag_3_Resultant_diff_mean,Tag_4_Resultant_diff_mean,
                                                 Tag_5_Resultant_diff_mean,Tag_6_Resultant_diff_mean])
            else:
                pass
            if len(Tag_7_Resultant_diff_persecond)>0:
                Tag_2_Resultant_diff_persecond=Tag_2_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_3_Resultant_diff_persecond=Tag_3_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_4_Resultant_diff_persecond=Tag_4_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_5_Resultant_diff_persecond=Tag_5_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_6_Resultant_diff_persecond=Tag_6_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_7_Resultant_diff_persecond=Tag_7_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Resultant_diff_persecond=numpy.vstack([Tag_1_Resultant_diff_persecond,Tag_2_Resultant_diff_persecond,Tag_3_Resultant_diff_persecond,Tag_4_Resultant_diff_persecond,
                                                 Tag_5_Resultant_diff_persecond,Tag_6_Resultant_diff_persecond,Tag_7_Resultant_diff_persecond])
                Tag_2_Resultant_diff_max=(Resultant_diff_persecond[1,:].max());Tag_2_Resultant_diff_mean=(Resultant_diff_persecond[1,:].mean());
                Tag_3_Resultant_diff_max=(Resultant_diff_persecond[2,:].max());Tag_3_Resultant_diff_mean=(Resultant_diff_persecond[2,:].mean());
                Tag_4_Resultant_diff_max=(Resultant_diff_persecond[3,:].max());Tag_4_Resultant_diff_mean=(Resultant_diff_persecond[3,:].mean());
                Tag_5_Resultant_diff_max=(Resultant_diff_persecond[4,:].max());Tag_5_Resultant_diff_mean=(Resultant_diff_persecond[4,:].mean());
                Tag_6_Resultant_diff_max=(Resultant_diff_persecond[5,:].max());Tag_6_Resultant_diff_mean=(Resultant_diff_persecond[5,:].mean());
                Tag_7_Resultant_diff_max=(Resultant_diff_persecond[6,:].max());Tag_7_Resultant_diff_mean=(Resultant_diff_persecond[6,:].mean());
                Resultant_diff_max=numpy.vstack([Tag_1_Resultant_diff_max,Tag_2_Resultant_diff_max,Tag_3_Resultant_diff_max,Tag_4_Resultant_diff_max,
                                                 Tag_5_Resultant_diff_max,Tag_6_Resultant_diff_max,Tag_7_Resultant_diff_max])
                Resultant_diff_mean=numpy.vstack([Tag_1_Resultant_diff_mean,Tag_2_Resultant_diff_mean,Tag_3_Resultant_diff_mean,Tag_4_Resultant_diff_mean,
                                                 Tag_5_Resultant_diff_mean,Tag_6_Resultant_diff_mean,Tag_7_Resultant_diff_mean])
 
            else:
                pass
            if len(Tag_8_Resultant_diff_persecond)>0:
                Tag_2_Resultant_diff_persecond=Tag_2_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_3_Resultant_diff_persecond=Tag_3_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_4_Resultant_diff_persecond=Tag_4_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_5_Resultant_diff_persecond=Tag_5_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_6_Resultant_diff_persecond=Tag_6_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_7_Resultant_diff_persecond=Tag_7_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_8_Resultant_diff_persecond=Tag_8_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Resultant_diff_persecond=numpy.vstack([Tag_1_Resultant_diff_persecond,Tag_2_Resultant_diff_persecond,Tag_3_Resultant_diff_persecond,Tag_4_Resultant_diff_persecond,
                                                 Tag_5_Resultant_diff_persecond,Tag_6_Resultant_diff_persecond,Tag_7_Resultant_diff_persecond,Tag_8_Resultant_diff_persecond])
                Tag_2_Resultant_diff_max=(Resultant_diff_persecond[1,:].max());Tag_2_Resultant_diff_mean=(Resultant_diff_persecond[1,:].mean());
                Tag_3_Resultant_diff_max=(Resultant_diff_persecond[2,:].max());Tag_3_Resultant_diff_mean=(Resultant_diff_persecond[2,:].mean());
                Tag_4_Resultant_diff_max=(Resultant_diff_persecond[3,:].max());Tag_4_Resultant_diff_mean=(Resultant_diff_persecond[3,:].mean());
                Tag_5_Resultant_diff_max=(Resultant_diff_persecond[4,:].max());Tag_5_Resultant_diff_mean=(Resultant_diff_persecond[4,:].mean());
                Tag_6_Resultant_diff_max=(Resultant_diff_persecond[5,:].max());Tag_6_Resultant_diff_mean=(Resultant_diff_persecond[5,:].mean());
                Tag_7_Resultant_diff_max=(Resultant_diff_persecond[6,:].max());Tag_7_Resultant_diff_mean=(Resultant_diff_persecond[6,:].mean());
                Tag_8_Resultant_diff_max=(Resultant_diff_persecond[7,:].max());Tag_8_Resultant_diff_mean=(Resultant_diff_persecond[7,:].mean());
                Resultant_diff_max=numpy.vstack([Tag_1_Resultant_diff_max,Tag_2_Resultant_diff_max,Tag_3_Resultant_diff_max,Tag_4_Resultant_diff_max,
                                                 Tag_5_Resultant_diff_max,Tag_6_Resultant_diff_max,Tag_7_Resultant_diff_max,Tag_8_Resultant_diff_max])
                Resultant_diff_mean=numpy.vstack([Tag_1_Resultant_diff_mean,Tag_2_Resultant_diff_mean,Tag_3_Resultant_diff_mean,Tag_4_Resultant_diff_mean,
                                                 Tag_5_Resultant_diff_mean,Tag_6_Resultant_diff_mean,Tag_7_Resultant_diff_mean,Tag_8_Resultant_diff_mean])
            else:
                pass
            if len(Tag_9_Resultant_diff_persecond)>0:
                Tag_2_Resultant_diff_persecond=Tag_2_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_3_Resultant_diff_persecond=Tag_3_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_4_Resultant_diff_persecond=Tag_4_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_5_Resultant_diff_persecond=Tag_5_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_6_Resultant_diff_persecond=Tag_6_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_7_Resultant_diff_persecond=Tag_7_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_8_Resultant_diff_persecond=Tag_8_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_9_Resultant_diff_persecond=Tag_9_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Resultant_diff_persecond=numpy.vstack([Tag_1_Resultant_diff_persecond,Tag_2_Resultant_diff_persecond,Tag_3_Resultant_diff_persecond,Tag_4_Resultant_diff_persecond,
                                                 Tag_5_Resultant_diff_persecond,Tag_6_Resultant_diff_persecond,Tag_7_Resultant_diff_persecond,Tag_8_Resultant_diff_persecond,
                                                 Tag_9_Resultant_diff_persecond])
                Tag_2_Resultant_diff_max=(Resultant_diff_persecond[1,:].max());Tag_2_Resultant_diff_mean=(Resultant_diff_persecond[1,:].mean());
                Tag_3_Resultant_diff_max=(Resultant_diff_persecond[2,:].max());Tag_3_Resultant_diff_mean=(Resultant_diff_persecond[2,:].mean());
                Tag_4_Resultant_diff_max=(Resultant_diff_persecond[3,:].max());Tag_4_Resultant_diff_mean=(Resultant_diff_persecond[3,:].mean());
                Tag_5_Resultant_diff_max=(Resultant_diff_persecond[4,:].max());Tag_5_Resultant_diff_mean=(Resultant_diff_persecond[4,:].mean());
                Tag_6_Resultant_diff_max=(Resultant_diff_persecond[5,:].max());Tag_6_Resultant_diff_mean=(Resultant_diff_persecond[5,:].mean());
                Tag_7_Resultant_diff_max=(Resultant_diff_persecond[6,:].max());Tag_7_Resultant_diff_mean=(Resultant_diff_persecond[6,:].mean());
                Tag_8_Resultant_diff_max=(Resultant_diff_persecond[7,:].max());Tag_8_Resultant_diff_mean=(Resultant_diff_persecond[7,:].mean());
                Tag_9_Resultant_diff_max=(Resultant_diff_persecond[8,:].max());Tag_9_Resultant_diff_mean=(Resultant_diff_persecond[8,:].mean());
                Resultant_diff_max=numpy.vstack([Tag_1_Resultant_diff_max,Tag_2_Resultant_diff_max,Tag_3_Resultant_diff_max,Tag_4_Resultant_diff_max,
                                                 Tag_5_Resultant_diff_max,Tag_6_Resultant_diff_max,Tag_7_Resultant_diff_max,Tag_8_Resultant_diff_max,
                                                 Tag_9_Resultant_diff_max])
                Resultant_diff_mean=numpy.vstack([Tag_1_Resultant_diff_mean,Tag_2_Resultant_diff_mean,Tag_3_Resultant_diff_mean,Tag_4_Resultant_diff_mean,
                                                 Tag_5_Resultant_diff_mean,Tag_6_Resultant_diff_mean,Tag_7_Resultant_diff_mean,Tag_8_Resultant_diff_mean,
                                                 Tag_9_Resultant_diff_mean])
            else:
                pass
            if len(Tag_10_Resultant_diff_persecond)>0:
                Tag_2_Resultant_diff_persecond=Tag_2_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_3_Resultant_diff_persecond=Tag_3_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_4_Resultant_diff_persecond=Tag_4_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_5_Resultant_diff_persecond=Tag_5_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_6_Resultant_diff_persecond=Tag_6_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_7_Resultant_diff_persecond=Tag_7_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_8_Resultant_diff_persecond=Tag_8_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_9_Resultant_diff_persecond=Tag_9_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_10_Resultant_diff_persecond=Tag_10_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Resultant_diff_persecond=numpy.vstack([Tag_1_Resultant_diff_persecond,Tag_2_Resultant_diff_persecond,Tag_3_Resultant_diff_persecond,Tag_4_Resultant_diff_persecond,
                                                 Tag_5_Resultant_diff_persecond,Tag_6_Resultant_diff_persecond,Tag_7_Resultant_diff_persecond,Tag_8_Resultant_diff_persecond,
                                                 Tag_9_Resultant_diff_persecond,Tag_10_Resultant_diff_persecond])
                Tag_2_Resultant_diff_max=(Resultant_diff_persecond[1,:].max());Tag_2_Resultant_diff_mean=(Resultant_diff_persecond[1,:].mean());
                Tag_3_Resultant_diff_max=(Resultant_diff_persecond[2,:].max());Tag_3_Resultant_diff_mean=(Resultant_diff_persecond[2,:].mean());
                Tag_4_Resultant_diff_max=(Resultant_diff_persecond[3,:].max());Tag_4_Resultant_diff_mean=(Resultant_diff_persecond[3,:].mean());
                Tag_5_Resultant_diff_max=(Resultant_diff_persecond[4,:].max());Tag_5_Resultant_diff_mean=(Resultant_diff_persecond[4,:].mean());
                Tag_6_Resultant_diff_max=(Resultant_diff_persecond[5,:].max());Tag_6_Resultant_diff_mean=(Resultant_diff_persecond[5,:].mean());
                Tag_7_Resultant_diff_max=(Resultant_diff_persecond[6,:].max());Tag_7_Resultant_diff_mean=(Resultant_diff_persecond[6,:].mean());
                Tag_8_Resultant_diff_max=(Resultant_diff_persecond[7,:].max());Tag_8_Resultant_diff_mean=(Resultant_diff_persecond[7,:].mean());
                Tag_9_Resultant_diff_max=(Resultant_diff_persecond[8,:].max());Tag_9_Resultant_diff_mean=(Resultant_diff_persecond[8,:].mean());
                Tag_10_Resultant_diff_max=(Resultant_diff_persecond[9,:].max());Tag_10_Resultant_diff_mean=(Resultant_diff_persecond[9,:].mean());
                Resultant_diff_max=numpy.vstack([Tag_1_Resultant_diff_max,Tag_2_Resultant_diff_max,Tag_3_Resultant_diff_max,Tag_4_Resultant_diff_max,
                                                 Tag_5_Resultant_diff_max,Tag_6_Resultant_diff_max,Tag_7_Resultant_diff_max,Tag_8_Resultant_diff_max,
                                                 Tag_9_Resultant_diff_max,Tag_10_Resultant_diff_max])
                Resultant_diff_mean=numpy.vstack([Tag_1_Resultant_diff_mean,Tag_2_Resultant_diff_mean,Tag_3_Resultant_diff_mean,Tag_4_Resultant_diff_mean,
                                                 Tag_5_Resultant_diff_mean,Tag_6_Resultant_diff_mean,Tag_7_Resultant_diff_mean,Tag_8_Resultant_diff_mean,
                                                 Tag_9_Resultant_diff_mean,Tag_10_Resultant_diff_mean])         
        
            else:
                pass
            if len(Tag_11_Resultant_diff_persecond)>0:
                Tag_2_Resultant_diff_persecond=Tag_2_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_3_Resultant_diff_persecond=Tag_3_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_4_Resultant_diff_persecond=Tag_4_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_5_Resultant_diff_persecond=Tag_5_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_6_Resultant_diff_persecond=Tag_6_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_7_Resultant_diff_persecond=Tag_7_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_8_Resultant_diff_persecond=Tag_8_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_9_Resultant_diff_persecond=Tag_9_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_10_Resultant_diff_persecond=Tag_10_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_11_Resultant_diff_persecond=Tag_11_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Resultant_diff_persecond=numpy.vstack([Tag_1_Resultant_diff_persecond,Tag_2_Resultant_diff_persecond,Tag_3_Resultant_diff_persecond,Tag_4_Resultant_diff_persecond,
                                                 Tag_5_Resultant_diff_persecond,Tag_6_Resultant_diff_persecond,Tag_7_Resultant_diff_persecond,Tag_8_Resultant_diff_persecond,
                                                 Tag_9_Resultant_diff_persecond,Tag_10_Resultant_diff_persecond,Tag_11_Resultant_diff_persecond])
                Tag_2_Resultant_diff_max=(Resultant_diff_persecond[1,:].max());Tag_2_Resultant_diff_mean=(Resultant_diff_persecond[1,:].mean());
                Tag_3_Resultant_diff_max=(Resultant_diff_persecond[2,:].max());Tag_3_Resultant_diff_mean=(Resultant_diff_persecond[2,:].mean());
                Tag_4_Resultant_diff_max=(Resultant_diff_persecond[3,:].max());Tag_4_Resultant_diff_mean=(Resultant_diff_persecond[3,:].mean());
                Tag_5_Resultant_diff_max=(Resultant_diff_persecond[4,:].max());Tag_5_Resultant_diff_mean=(Resultant_diff_persecond[4,:].mean());
                Tag_6_Resultant_diff_max=(Resultant_diff_persecond[5,:].max());Tag_6_Resultant_diff_mean=(Resultant_diff_persecond[5,:].mean());
                Tag_7_Resultant_diff_max=(Resultant_diff_persecond[6,:].max());Tag_7_Resultant_diff_mean=(Resultant_diff_persecond[6,:].mean());
                Tag_8_Resultant_diff_max=(Resultant_diff_persecond[7,:].max());Tag_8_Resultant_diff_mean=(Resultant_diff_persecond[7,:].mean());
                Tag_9_Resultant_diff_max=(Resultant_diff_persecond[8,:].max());Tag_9_Resultant_diff_mean=(Resultant_diff_persecond[8,:].mean());
                Tag_10_Resultant_diff_max=(Resultant_diff_persecond[9,:].max());Tag_10_Resultant_diff_mean=(Resultant_diff_persecond[9,:].mean());
                Tag_11_Resultant_diff_max=(Resultant_diff_persecond[10,:].max());Tag_11_Resultant_diff_mean=(Resultant_diff_persecond[10,:].mean());
                Resultant_diff_max=numpy.vstack([Tag_1_Resultant_diff_max,Tag_2_Resultant_diff_max,Tag_3_Resultant_diff_max,Tag_4_Resultant_diff_max,
                                                 Tag_5_Resultant_diff_max,Tag_6_Resultant_diff_max,Tag_7_Resultant_diff_max,Tag_8_Resultant_diff_max,
                                                 Tag_9_Resultant_diff_max,Tag_10_Resultant_diff_max,Tag_11_Resultant_diff_max])
                Resultant_diff_mean=numpy.vstack([Tag_1_Resultant_diff_mean,Tag_2_Resultant_diff_mean,Tag_3_Resultant_diff_mean,Tag_4_Resultant_diff_mean,
                                                 Tag_5_Resultant_diff_mean,Tag_6_Resultant_diff_mean,Tag_7_Resultant_diff_mean,Tag_8_Resultant_diff_mean,
                                                 Tag_9_Resultant_diff_mean,Tag_10_Resultant_diff_mean,Tag_11_Resultant_diff_mean])         
            else:
                pass
            if len(Tag_12_Resultant_diff_persecond)>0:
                Tag_2_Resultant_diff_persecond=Tag_2_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_3_Resultant_diff_persecond=Tag_3_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_4_Resultant_diff_persecond=Tag_4_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_5_Resultant_diff_persecond=Tag_5_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_6_Resultant_diff_persecond=Tag_6_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_7_Resultant_diff_persecond=Tag_7_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_8_Resultant_diff_persecond=Tag_8_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_9_Resultant_diff_persecond=Tag_9_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_10_Resultant_diff_persecond=Tag_10_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_11_Resultant_diff_persecond=Tag_11_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_12_Resultant_diff_persecond=Tag_12_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Resultant_diff_persecond=numpy.vstack([Tag_1_Resultant_diff_persecond,Tag_2_Resultant_diff_persecond,Tag_3_Resultant_diff_persecond,Tag_4_Resultant_diff_persecond,
                                                 Tag_5_Resultant_diff_persecond,Tag_6_Resultant_diff_persecond,Tag_7_Resultant_diff_persecond,Tag_8_Resultant_diff_persecond,
                                                 Tag_9_Resultant_diff_persecond,Tag_10_Resultant_diff_persecond,Tag_11_Resultant_diff_persecond,Tag_12_Resultant_diff_persecond])
                Tag_2_Resultant_diff_max=(Resultant_diff_persecond[1,:].max());Tag_2_Resultant_diff_mean=(Resultant_diff_persecond[1,:].mean());
                Tag_3_Resultant_diff_max=(Resultant_diff_persecond[2,:].max());Tag_3_Resultant_diff_mean=(Resultant_diff_persecond[2,:].mean());
                Tag_4_Resultant_diff_max=(Resultant_diff_persecond[3,:].max());Tag_4_Resultant_diff_mean=(Resultant_diff_persecond[3,:].mean());
                Tag_5_Resultant_diff_max=(Resultant_diff_persecond[4,:].max());Tag_5_Resultant_diff_mean=(Resultant_diff_persecond[4,:].mean());
                Tag_6_Resultant_diff_max=(Resultant_diff_persecond[5,:].max());Tag_6_Resultant_diff_mean=(Resultant_diff_persecond[5,:].mean());
                Tag_7_Resultant_diff_max=(Resultant_diff_persecond[6,:].max());Tag_7_Resultant_diff_mean=(Resultant_diff_persecond[6,:].mean());
                Tag_8_Resultant_diff_max=(Resultant_diff_persecond[7,:].max());Tag_8_Resultant_diff_mean=(Resultant_diff_persecond[7,:].mean());
                Tag_9_Resultant_diff_max=(Resultant_diff_persecond[8,:].max());Tag_9_Resultant_diff_mean=(Resultant_diff_persecond[8,:].mean());
                Tag_10_Resultant_diff_max=(Resultant_diff_persecond[9,:].max());Tag_10_Resultant_diff_mean=(Resultant_diff_persecond[9,:].mean());
                Tag_11_Resultant_diff_max=(Resultant_diff_persecond[10,:].max());Tag_11_Resultant_diff_mean=(Resultant_diff_persecond[10,:].mean());
                Tag_12_Resultant_diff_max=(Resultant_diff_persecond[11,:].max());Tag_12_Resultant_diff_mean=(Resultant_diff_persecond[11,:].mean());
                Resultant_diff_max=numpy.vstack([Tag_1_Resultant_diff_max,Tag_2_Resultant_diff_max,Tag_3_Resultant_diff_max,Tag_4_Resultant_diff_max,
                                                 Tag_5_Resultant_diff_max,Tag_6_Resultant_diff_max,Tag_7_Resultant_diff_max,Tag_8_Resultant_diff_max,
                                                 Tag_9_Resultant_diff_max,Tag_10_Resultant_diff_max,Tag_11_Resultant_diff_max,Tag_12_Resultant_diff_max])
                Resultant_diff_mean=numpy.vstack([Tag_1_Resultant_diff_mean,Tag_2_Resultant_diff_mean,Tag_3_Resultant_diff_mean,Tag_4_Resultant_diff_mean,
                                                 Tag_5_Resultant_diff_mean,Tag_6_Resultant_diff_mean,Tag_7_Resultant_diff_mean,Tag_8_Resultant_diff_mean,
                                                 Tag_9_Resultant_diff_mean,Tag_10_Resultant_diff_mean,Tag_11_Resultant_diff_mean,Tag_12_Resultant_diff_mean])
            else:
                pass
            if len(Tag_13_Resultant_diff_persecond)>0:
                Tag_2_Resultant_diff_persecond=Tag_2_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_3_Resultant_diff_persecond=Tag_3_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_4_Resultant_diff_persecond=Tag_4_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_5_Resultant_diff_persecond=Tag_5_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_6_Resultant_diff_persecond=Tag_6_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_7_Resultant_diff_persecond=Tag_7_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_8_Resultant_diff_persecond=Tag_8_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_9_Resultant_diff_persecond=Tag_9_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_10_Resultant_diff_persecond=Tag_10_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_11_Resultant_diff_persecond=Tag_11_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_12_Resultant_diff_persecond=Tag_12_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_13_Resultant_diff_persecond=Tag_13_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Resultant_diff_persecond=numpy.vstack([Tag_1_Resultant_diff_persecond,Tag_2_Resultant_diff_persecond,Tag_3_Resultant_diff_persecond,Tag_4_Resultant_diff_persecond,
                                                 Tag_5_Resultant_diff_persecond,Tag_6_Resultant_diff_persecond,Tag_7_Resultant_diff_persecond,Tag_8_Resultant_diff_persecond,
                                                 Tag_9_Resultant_diff_persecond,Tag_10_Resultant_diff_persecond,Tag_11_Resultant_diff_persecond,Tag_12_Resultant_diff_persecond,
                                                 Tag_13_Resultant_diff_persecond])
                Tag_2_Resultant_diff_max=(Resultant_diff_persecond[1,:].max());Tag_2_Resultant_diff_mean=(Resultant_diff_persecond[1,:].mean());
                Tag_3_Resultant_diff_max=(Resultant_diff_persecond[2,:].max());Tag_3_Resultant_diff_mean=(Resultant_diff_persecond[2,:].mean());
                Tag_4_Resultant_diff_max=(Resultant_diff_persecond[3,:].max());Tag_4_Resultant_diff_mean=(Resultant_diff_persecond[3,:].mean());
                Tag_5_Resultant_diff_max=(Resultant_diff_persecond[4,:].max());Tag_5_Resultant_diff_mean=(Resultant_diff_persecond[4,:].mean());
                Tag_6_Resultant_diff_max=(Resultant_diff_persecond[5,:].max());Tag_6_Resultant_diff_mean=(Resultant_diff_persecond[5,:].mean());
                Tag_7_Resultant_diff_max=(Resultant_diff_persecond[6,:].max());Tag_7_Resultant_diff_mean=(Resultant_diff_persecond[6,:].mean());
                Tag_8_Resultant_diff_max=(Resultant_diff_persecond[7,:].max());Tag_8_Resultant_diff_mean=(Resultant_diff_persecond[7,:].mean());
                Tag_9_Resultant_diff_max=(Resultant_diff_persecond[8,:].max());Tag_9_Resultant_diff_mean=(Resultant_diff_persecond[8,:].mean());
                Tag_10_Resultant_diff_max=(Resultant_diff_persecond[9,:].max());Tag_10_Resultant_diff_mean=(Resultant_diff_persecond[9,:].mean());
                Tag_11_Resultant_diff_max=(Resultant_diff_persecond[10,:].max());Tag_11_Resultant_diff_mean=(Resultant_diff_persecond[10,:].mean());
                Tag_12_Resultant_diff_max=(Resultant_diff_persecond[11,:].max());Tag_12_Resultant_diff_mean=(Resultant_diff_persecond[11,:].mean());
                Tag_13_Resultant_diff_max=(Resultant_diff_persecond[12,:].max());Tag_13_Resultant_diff_mean=(Resultant_diff_persecond[12,:].mean());
                Resultant_diff_max=numpy.vstack([Tag_1_Resultant_diff_max,Tag_2_Resultant_diff_max,Tag_3_Resultant_diff_max,Tag_4_Resultant_diff_max,
                                                 Tag_5_Resultant_diff_max,Tag_6_Resultant_diff_max,Tag_7_Resultant_diff_max,Tag_8_Resultant_diff_max,
                                                 Tag_9_Resultant_diff_max,Tag_10_Resultant_diff_max,Tag_11_Resultant_diff_max,Tag_12_Resultant_diff_max,
                                                 Tag_13_Resultant_diff_max])
                Resultant_diff_mean=numpy.vstack([Tag_1_Resultant_diff_mean,Tag_2_Resultant_diff_mean,Tag_3_Resultant_diff_mean,Tag_4_Resultant_diff_mean,
                                                 Tag_5_Resultant_diff_mean,Tag_6_Resultant_diff_mean,Tag_7_Resultant_diff_mean,Tag_8_Resultant_diff_mean,
                                                 Tag_9_Resultant_diff_mean,Tag_10_Resultant_diff_mean,Tag_11_Resultant_diff_mean,Tag_12_Resultant_diff_mean,
                                                 Tag_13_Resultant_diff_mean])
            else:
                pass
            if len(Tag_14_Resultant_diff_persecond)>0:
                Tag_2_Resultant_diff_persecond=Tag_2_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_3_Resultant_diff_persecond=Tag_3_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_4_Resultant_diff_persecond=Tag_4_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_5_Resultant_diff_persecond=Tag_5_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_6_Resultant_diff_persecond=Tag_6_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_7_Resultant_diff_persecond=Tag_7_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_8_Resultant_diff_persecond=Tag_8_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_9_Resultant_diff_persecond=Tag_9_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_10_Resultant_diff_persecond=Tag_10_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_11_Resultant_diff_persecond=Tag_11_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_12_Resultant_diff_persecond=Tag_12_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_13_Resultant_diff_persecond=Tag_13_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Tag_14_Resultant_diff_persecond=Tag_14_Resultant_diff_persecond[:,:Tag_1_Resultant_diff_persecond.size];
                Resultant_diff_persecond=numpy.vstack([Tag_1_Resultant_diff_persecond,Tag_2_Resultant_diff_persecond,Tag_3_Resultant_diff_persecond,Tag_4_Resultant_diff_persecond,
                                                 Tag_5_Resultant_diff_persecond,Tag_6_Resultant_diff_persecond,Tag_7_Resultant_diff_persecond,Tag_8_Resultant_diff_persecond,
                                                 Tag_9_Resultant_diff_persecond,Tag_10_Resultant_diff_persecond,Tag_11_Resultant_diff_persecond,Tag_12_Resultant_diff_persecond,
                                                 Tag_13_Resultant_diff_persecond,Tag_14_Resultant_diff_persecond])
                Tag_2_Resultant_diff_max=(Resultant_diff_persecond[1,:].max());Tag_2_Resultant_diff_mean=(Resultant_diff_persecond[1,:].mean());
                Tag_3_Resultant_diff_max=(Resultant_diff_persecond[2,:].max());Tag_3_Resultant_diff_mean=(Resultant_diff_persecond[2,:].mean());
                Tag_4_Resultant_diff_max=(Resultant_diff_persecond[3,:].max());Tag_4_Resultant_diff_mean=(Resultant_diff_persecond[3,:].mean());
                Tag_5_Resultant_diff_max=(Resultant_diff_persecond[4,:].max());Tag_5_Resultant_diff_mean=(Resultant_diff_persecond[4,:].mean());
                Tag_6_Resultant_diff_max=(Resultant_diff_persecond[5,:].max());Tag_6_Resultant_diff_mean=(Resultant_diff_persecond[5,:].mean());
                Tag_7_Resultant_diff_max=(Resultant_diff_persecond[6,:].max());Tag_7_Resultant_diff_mean=(Resultant_diff_persecond[6,:].mean());
                Tag_8_Resultant_diff_max=(Resultant_diff_persecond[7,:].max());Tag_8_Resultant_diff_mean=(Resultant_diff_persecond[7,:].mean());
                Tag_9_Resultant_diff_max=(Resultant_diff_persecond[8,:].max());Tag_9_Resultant_diff_mean=(Resultant_diff_persecond[8,:].mean());
                Tag_10_Resultant_diff_max=(Resultant_diff_persecond[9,:].max());Tag_10_Resultant_diff_mean=(Resultant_diff_persecond[9,:].mean());
                Tag_11_Resultant_diff_max=(Resultant_diff_persecond[10,:].max());Tag_11_Resultant_diff_mean=(Resultant_diff_persecond[10,:].mean());
                Tag_12_Resultant_diff_max=(Resultant_diff_persecond[11,:].max());Tag_12_Resultant_diff_mean=(Resultant_diff_persecond[11,:].mean());
                Tag_13_Resultant_diff_max=(Resultant_diff_persecond[12,:].max());Tag_13_Resultant_diff_mean=(Resultant_diff_persecond[12,:].mean());
                Tag_14_Resultant_diff_max=(Resultant_diff_persecond[13,:].max());Tag_14_Resultant_diff_mean=(Resultant_diff_persecond[13,:].mean());
                Resultant_diff_max=numpy.vstack([Tag_1_Resultant_diff_max,Tag_2_Resultant_diff_max,Tag_3_Resultant_diff_max,Tag_4_Resultant_diff_max,
                                                 Tag_5_Resultant_diff_max,Tag_6_Resultant_diff_max,Tag_7_Resultant_diff_max,Tag_8_Resultant_diff_max,
                                                 Tag_9_Resultant_diff_max,Tag_10_Resultant_diff_max,Tag_11_Resultant_diff_max,Tag_12_Resultant_diff_max,
                                                 Tag_13_Resultant_diff_max,Tag_14_Resultant_diff_max])
                Resultant_diff_mean=numpy.vstack([Tag_1_Resultant_diff_mean,Tag_2_Resultant_diff_mean,Tag_3_Resultant_diff_mean,Tag_4_Resultant_diff_mean,
                                                 Tag_5_Resultant_diff_mean,Tag_6_Resultant_diff_mean,Tag_7_Resultant_diff_mean,Tag_8_Resultant_diff_mean,
                                                 Tag_9_Resultant_diff_mean,Tag_10_Resultant_diff_mean,Tag_11_Resultant_diff_mean,Tag_12_Resultant_diff_mean,
                                                 Tag_13_Resultant_diff_mean,Tag_14_Resultant_diff_mean])
            else:
                pass

####Distance transforms ###
            print("C")
            Tag_1_Resultant_diff_persecond=Tag_1_Resultant_diff_persecond[:,:Time_one.size-1];
            Resultant_diff_persecond=Tag_1_Resultant_diff_persecond
            Tag_1_Distance_max=(Distance[0,:].max())
            Tag_1_Distance_mean=(Distance[0,:].mean())
            Distance_max=Tag_1_Distance_max
            Distance_mean=Tag_1_Distance_mean
            
            if len(Tag_2_Resultant_diff_persecond)>0:
                Tag_2_Distance_max=(Distance[1,:].max())
                Tag_2_Distance_mean=(Distance[1,:].mean())
                Distance_max=numpy.vstack([Tag_1_Distance_max,Tag_2_Distance_max])
                Distance_mean=numpy.vstack([Tag_1_Distance_mean,Tag_2_Distance_mean])
            else:
                pass
            if len(Tag_3_Resultant_diff_persecond)>0:
                Tag_2_Distance_max=(Distance[1,:].max());Tag_2_Distance_mean=(Distance[1,:].mean());
                Tag_3_Distance_max=(Distance[2,:].max());Tag_3_Distance_mean=(Distance[2,:].mean());
                Distance_max=numpy.vstack([Tag_1_Distance_max,Tag_2_Distance_max,Tag_3_Distance_max])
                Distance_mean=numpy.vstack([Tag_1_Distance_mean,Tag_2_Distance_mean,Tag_3_Distance_mean])
            else:
                pass
            if len(Tag_4_Resultant_diff_persecond)>0:
                Tag_2_Distance_max=(Distance[1,:].max());Tag_2_Distance_mean=(Distance[1,:].mean());
                Tag_3_Distance_max=(Distance[2,:].max());Tag_3_Distance_mean=(Distance[2,:].mean());
                Tag_4_Distance_max=(Distance[3,:].max());Tag_4_Distance_mean=(Distance[3,:].mean());
                Distance_max=numpy.vstack([Tag_1_Distance_max,Tag_2_Distance_max,Tag_3_Distance_max,Tag_4_Distance_max])
                Distance_mean=numpy.vstack([Tag_1_Distance_mean,Tag_2_Distance_mean,Tag_3_Distance_mean,Tag_4_Distance_mean])
            else:
                pass
            if len(Tag_5_Resultant_diff_persecond)>0:
                Tag_2_Distance_max=(Distance[1,:].max());Tag_2_Distance_mean=(Distance[1,:].mean());
                Tag_3_Distance_max=(Distance[2,:].max());Tag_3_Distance_mean=(Distance[2,:].mean());
                Tag_4_Distance_max=(Distance[3,:].max());Tag_4_Distance_mean=(Distance[3,:].mean());
                Tag_5_Distance_max=(Distance[4,:].max());Tag_5_Distance_mean=(Distance[4,:].mean());
                Distance_max=numpy.vstack([Tag_1_Distance_max,Tag_2_Distance_max,Tag_3_Distance_max,Tag_4_Distance_max,
                                                 Tag_5_Distance_max])
                Distance_mean=numpy.vstack([Tag_1_Distance_mean,Tag_2_Distance_mean,Tag_3_Distance_mean,Tag_4_Distance_mean,
                                                 Tag_5_Distance_mean])
            else:
                pass
            if len(Tag_6_Resultant_diff_persecond)>0:
                Tag_2_Distance_max=(Distance[1,:].max());Tag_2_Distance_mean=(Distance[1,:].mean());
                Tag_3_Distance_max=(Distance[2,:].max());Tag_3_Distance_mean=(Distance[2,:].mean());
                Tag_4_Distance_max=(Distance[3,:].max());Tag_4_Distance_mean=(Distance[3,:].mean());
                Tag_5_Distance_max=(Distance[4,:].max());Tag_5_Distance_mean=(Distance[4,:].mean());
                Tag_6_Distance_max=(Distance[5,:].max());Tag_6_Distance_mean=(Distance[5,:].mean());
                Distance_max=numpy.vstack([Tag_1_Distance_max,Tag_2_Distance_max,Tag_3_Distance_max,Tag_4_Distance_max,
                                                 Tag_5_Distance_max,Tag_6_Distance_max])
                Distance_mean=numpy.vstack([Tag_1_Distance_mean,Tag_2_Distance_mean,Tag_3_Distance_mean,Tag_4_Distance_mean,
                                                 Tag_5_Distance_mean,Tag_6_Distance_mean])
            else:
                pass
            if len(Tag_7_Resultant_diff_persecond)>0:
                Tag_2_Distance_max=(Distance[1,:].max());Tag_2_Distance_mean=(Distance[1,:].mean());
                Tag_3_Distance_max=(Distance[2,:].max());Tag_3_Distance_mean=(Distance[2,:].mean());
                Tag_4_Distance_max=(Distance[3,:].max());Tag_4_Distance_mean=(Distance[3,:].mean());
                Tag_5_Distance_max=(Distance[4,:].max());Tag_5_Distance_mean=(Distance[4,:].mean());
                Tag_6_Distance_max=(Distance[5,:].max());Tag_6_Distance_mean=(Distance[5,:].mean());
                Tag_7_Distance_max=(Distance[6,:].max());Tag_7_Distance_mean=(Distance[6,:].mean());
                Distance_max=numpy.vstack([Tag_1_Distance_max,Tag_2_Distance_max,Tag_3_Distance_max,Tag_4_Distance_max,
                                                 Tag_5_Distance_max,Tag_6_Distance_max,Tag_7_Distance_max])
                Distance_mean=numpy.vstack([Tag_1_Distance_mean,Tag_2_Distance_mean,Tag_3_Distance_mean,Tag_4_Distance_mean,
                                                 Tag_5_Distance_mean,Tag_6_Distance_mean,Tag_7_Distance_mean])
 
            else:
                pass
            if len(Tag_8_Resultant_diff_persecond)>0:
                Tag_2_Distance_max=(Distance[1,:].max());Tag_2_Distance_mean=(Distance[1,:].mean());
                Tag_3_Distance_max=(Distance[2,:].max());Tag_3_Distance_mean=(Distance[2,:].mean());
                Tag_4_Distance_max=(Distance[3,:].max());Tag_4_Distance_mean=(Distance[3,:].mean());
                Tag_5_Distance_max=(Distance[4,:].max());Tag_5_Distance_mean=(Distance[4,:].mean());
                Tag_6_Distance_max=(Distance[5,:].max());Tag_6_Distance_mean=(Distance[5,:].mean());
                Tag_7_Distance_max=(Distance[6,:].max());Tag_7_Distance_mean=(Distance[6,:].mean());
                Tag_8_Distance_max=(Distance[7,:].max());Tag_8_Distance_mean=(Distance[7,:].mean());
                Distance_max=numpy.vstack([Tag_1_Distance_max,Tag_2_Distance_max,Tag_3_Distance_max,Tag_4_Distance_max,
                                                 Tag_5_Distance_max,Tag_6_Distance_max,Tag_7_Distance_max,Tag_8_Distance_max])
                Distance_mean=numpy.vstack([Tag_1_Distance_mean,Tag_2_Distance_mean,Tag_3_Distance_mean,Tag_4_Distance_mean,
                                                 Tag_5_Distance_mean,Tag_6_Distance_mean,Tag_7_Distance_mean,Tag_8_Distance_mean])
            else:
                pass
            if len(Tag_9_Resultant_diff_persecond)>0:
                Tag_2_Distance_max=(Distance[1,:].max());Tag_2_Distance_mean=(Distance[1,:].mean());
                Tag_3_Distance_max=(Distance[2,:].max());Tag_3_Distance_mean=(Distance[2,:].mean());
                Tag_4_Distance_max=(Distance[3,:].max());Tag_4_Distance_mean=(Distance[3,:].mean());
                Tag_5_Distance_max=(Distance[4,:].max());Tag_5_Distance_mean=(Distance[4,:].mean());
                Tag_6_Distance_max=(Distance[5,:].max());Tag_6_Distance_mean=(Distance[5,:].mean());
                Tag_7_Distance_max=(Distance[6,:].max());Tag_7_Distance_mean=(Distance[6,:].mean());
                Tag_8_Distance_max=(Distance[7,:].max());Tag_8_Distance_mean=(Distance[7,:].mean());
                Tag_9_Distance_max=(Distance[8,:].max());Tag_9_Distance_mean=(Distance[8,:].mean());
                Distance_max=numpy.vstack([Tag_1_Distance_max,Tag_2_Distance_max,Tag_3_Distance_max,Tag_4_Distance_max,
                                                 Tag_5_Distance_max,Tag_6_Distance_max,Tag_7_Distance_max,Tag_8_Distance_max,
                                                 Tag_9_Distance_max])
                Distance_mean=numpy.vstack([Tag_1_Distance_mean,Tag_2_Distance_mean,Tag_3_Distance_mean,Tag_4_Distance_mean,
                                                 Tag_5_Distance_mean,Tag_6_Distance_mean,Tag_7_Distance_mean,Tag_8_Distance_mean,
                                                 Tag_9_Distance_mean])
            else:
                pass
            if len(Tag_10_Resultant_diff_persecond)>0:
                Tag_2_Distance_max=(Distance[1,:].max());Tag_2_Distance_mean=(Distance[1,:].mean());
                Tag_3_Distance_max=(Distance[2,:].max());Tag_3_Distance_mean=(Distance[2,:].mean());
                Tag_4_Distance_max=(Distance[3,:].max());Tag_4_Distance_mean=(Distance[3,:].mean());
                Tag_5_Distance_max=(Distance[4,:].max());Tag_5_Distance_mean=(Distance[4,:].mean());
                Tag_6_Distance_max=(Distance[5,:].max());Tag_6_Distance_mean=(Distance[5,:].mean());
                Tag_7_Distance_max=(Distance[6,:].max());Tag_7_Distance_mean=(Distance[6,:].mean());
                Tag_8_Distance_max=(Distance[7,:].max());Tag_8_Distance_mean=(Distance[7,:].mean());
                Tag_9_Distance_max=(Distance[8,:].max());Tag_9_Distance_mean=(Distance[8,:].mean());
                Tag_10_Distance_max=(Distance[9,:].max());Tag_10_Distance_mean=(Distance[9,:].mean());
                Distance_max=numpy.vstack([Tag_1_Distance_max,Tag_2_Distance_max,Tag_3_Distance_max,Tag_4_Distance_max,
                                                 Tag_5_Distance_max,Tag_6_Distance_max,Tag_7_Distance_max,Tag_8_Distance_max,
                                                 Tag_9_Distance_max,Tag_10_Distance_max])
                Distance_mean=numpy.vstack([Tag_1_Distance_mean,Tag_2_Distance_mean,Tag_3_Distance_mean,Tag_4_Distance_mean,
                                                 Tag_5_Distance_mean,Tag_6_Distance_mean,Tag_7_Distance_mean,Tag_8_Distance_mean,
                                                 Tag_9_Distance_mean,Tag_10_Distance_mean])         
        
            else:
                pass
            if len(Tag_11_Resultant_diff_persecond)>0:
                Tag_2_Distance_max=(Distance[1,:].max());Tag_2_Distance_mean=(Distance[1,:].mean());
                Tag_3_Distance_max=(Distance[2,:].max());Tag_3_Distance_mean=(Distance[2,:].mean());
                Tag_4_Distance_max=(Distance[3,:].max());Tag_4_Distance_mean=(Distance[3,:].mean());
                Tag_5_Distance_max=(Distance[4,:].max());Tag_5_Distance_mean=(Distance[4,:].mean());
                Tag_6_Distance_max=(Distance[5,:].max());Tag_6_Distance_mean=(Distance[5,:].mean());
                Tag_7_Distance_max=(Distance[6,:].max());Tag_7_Distance_mean=(Distance[6,:].mean());
                Tag_8_Distance_max=(Distance[7,:].max());Tag_8_Distance_mean=(Distance[7,:].mean());
                Tag_9_Distance_max=(Distance[8,:].max());Tag_9_Distance_mean=(Distance[8,:].mean());
                Tag_10_Distance_max=(Distance[9,:].max());Tag_10_Distance_mean=(Distance[9,:].mean());
                Tag_11_Distance_max=(Distance[10,:].max());Tag_11_Distance_mean=(Distance[10,:].mean());
                Distance_max=numpy.vstack([Tag_1_Distance_max,Tag_2_Distance_max,Tag_3_Distance_max,Tag_4_Distance_max,
                                                 Tag_5_Distance_max,Tag_6_Distance_max,Tag_7_Distance_max,Tag_8_Distance_max,
                                                 Tag_9_Distance_max,Tag_10_Distance_max,Tag_11_Distance_max])
                Distance_mean=numpy.vstack([Tag_1_Distance_mean,Tag_2_Distance_mean,Tag_3_Distance_mean,Tag_4_Distance_mean,
                                                 Tag_5_Distance_mean,Tag_6_Distance_mean,Tag_7_Distance_mean,Tag_8_Distance_mean,
                                                 Tag_9_Distance_mean,Tag_10_Distance_mean,Tag_11_Distance_mean])         
            else:
                pass
            if len(Tag_12_Resultant_diff_persecond)>0:
                Tag_2_Distance_max=(Distance[1,:].max());Tag_2_Distance_mean=(Distance[1,:].mean());
                Tag_3_Distance_max=(Distance[2,:].max());Tag_3_Distance_mean=(Distance[2,:].mean());
                Tag_4_Distance_max=(Distance[3,:].max());Tag_4_Distance_mean=(Distance[3,:].mean());
                Tag_5_Distance_max=(Distance[4,:].max());Tag_5_Distance_mean=(Distance[4,:].mean());
                Tag_6_Distance_max=(Distance[5,:].max());Tag_6_Distance_mean=(Distance[5,:].mean());
                Tag_7_Distance_max=(Distance[6,:].max());Tag_7_Distance_mean=(Distance[6,:].mean());
                Tag_8_Distance_max=(Distance[7,:].max());Tag_8_Distance_mean=(Distance[7,:].mean());
                Tag_9_Distance_max=(Distance[8,:].max());Tag_9_Distance_mean=(Distance[8,:].mean());
                Tag_10_Distance_max=(Distance[9,:].max());Tag_10_Distance_mean=(Distance[9,:].mean());
                Tag_11_Distance_max=(Distance[10,:].max());Tag_11_Distance_mean=(Distance[10,:].mean());
                Tag_12_Distance_max=(Distance[11,:].max());Tag_12_Distance_mean=(Distance[11,:].mean());
                Distance_max=numpy.vstack([Tag_1_Distance_max,Tag_2_Distance_max,Tag_3_Distance_max,Tag_4_Distance_max,
                                                 Tag_5_Distance_max,Tag_6_Distance_max,Tag_7_Distance_max,Tag_8_Distance_max,
                                                 Tag_9_Distance_max,Tag_10_Distance_max,Tag_11_Distance_max,Tag_12_Distance_max])
                Distance_mean=numpy.vstack([Tag_1_Distance_mean,Tag_2_Distance_mean,Tag_3_Distance_mean,Tag_4_Distance_mean,
                                                 Tag_5_Distance_mean,Tag_6_Distance_mean,Tag_7_Distance_mean,Tag_8_Distance_mean,
                                                 Tag_9_Distance_mean,Tag_10_Distance_mean,Tag_11_Distance_mean,Tag_12_Distance_mean])
            else:
                pass
            if len(Tag_13_Resultant_diff_persecond)>0:
                Tag_2_Distance_max=(Distance[1,:].max());Tag_2_Distance_mean=(Distance[1,:].mean());
                Tag_3_Distance_max=(Distance[2,:].max());Tag_3_Distance_mean=(Distance[2,:].mean());
                Tag_4_Distance_max=(Distance[3,:].max());Tag_4_Distance_mean=(Distance[3,:].mean());
                Tag_5_Distance_max=(Distance[4,:].max());Tag_5_Distance_mean=(Distance[4,:].mean());
                Tag_6_Distance_max=(Distance[5,:].max());Tag_6_Distance_mean=(Distance[5,:].mean());
                Tag_7_Distance_max=(Distance[6,:].max());Tag_7_Distance_mean=(Distance[6,:].mean());
                Tag_8_Distance_max=(Distance[7,:].max());Tag_8_Distance_mean=(Distance[7,:].mean());
                Tag_9_Distance_max=(Distance[8,:].max());Tag_9_Distance_mean=(Distance[8,:].mean());
                Tag_10_Distance_max=(Distance[9,:].max());Tag_10_Distance_mean=(Distance[9,:].mean());
                Tag_11_Distance_max=(Distance[10,:].max());Tag_11_Distance_mean=(Distance[10,:].mean());
                Tag_12_Distance_max=(Distance[11,:].max());Tag_12_Distance_mean=(Distance[11,:].mean());
                Tag_13_Distance_max=(Distance[12,:].max());Tag_13_Distance_mean=(Distance[12,:].mean());
                Distance_max=numpy.vstack([Tag_1_Distance_max,Tag_2_Distance_max,Tag_3_Distance_max,Tag_4_Distance_max,
                                                 Tag_5_Distance_max,Tag_6_Distance_max,Tag_7_Distance_max,Tag_8_Distance_max,
                                                 Tag_9_Distance_max,Tag_10_Distance_max,Tag_11_Distance_max,Tag_12_Distance_max,
                                                 Tag_13_Distance_max])
                Distance_mean=numpy.vstack([Tag_1_Distance_mean,Tag_2_Distance_mean,Tag_3_Distance_mean,Tag_4_Distance_mean,
                                                 Tag_5_Distance_mean,Tag_6_Distance_mean,Tag_7_Distance_mean,Tag_8_Distance_mean,
                                                 Tag_9_Distance_mean,Tag_10_Distance_mean,Tag_11_Distance_mean,Tag_12_Distance_mean,
                                                 Tag_13_Distance_mean])
            else:
                pass
            if len(Tag_14_Resultant_diff_persecond)>0:
                Tag_2_Distance_max=(Distance[1,:].max());Tag_2_Distance_mean=(Distance[1,:].mean());
                Tag_3_Distance_max=(Distance[2,:].max());Tag_3_Distance_mean=(Distance[2,:].mean());
                Tag_4_Distance_max=(Distance[3,:].max());Tag_4_Distance_mean=(Distance[3,:].mean());
                Tag_5_Distance_max=(Distance[4,:].max());Tag_5_Distance_mean=(Distance[4,:].mean());
                Tag_6_Distance_max=(Distance[5,:].max());Tag_6_Distance_mean=(Distance[5,:].mean());
                Tag_7_Distance_max=(Distance[6,:].max());Tag_7_Distance_mean=(Distance[6,:].mean());
                Tag_8_Distance_max=(Distance[7,:].max());Tag_8_Distance_mean=(Distance[7,:].mean());
                Tag_9_Distance_max=(Distance[8,:].max());Tag_9_Distance_mean=(Distance[8,:].mean());
                Tag_10_Distance_max=(Distance[9,:].max());Tag_10_Distance_mean=(Distance[9,:].mean());
                Tag_11_Distance_max=(Distance[10,:].max());Tag_11_Distance_mean=(Distance[10,:].mean());
                Tag_12_Distance_max=(Distance[11,:].max());Tag_12_Distance_mean=(Distance[11,:].mean());
                Tag_13_Distance_max=(Distance[12,:].max());Tag_13_Distance_mean=(Distance[12,:].mean());
                Tag_14_Distance_max=(Distance[13,:].max());Tag_14_Distance_mean=(Distance[13,:].mean());
                Distance_max=numpy.vstack([Tag_1_Distance_max,Tag_2_Distance_max,Tag_3_Distance_max,Tag_4_Distance_max,
                                                 Tag_5_Distance_max,Tag_6_Distance_max,Tag_7_Distance_max,Tag_8_Distance_max,
                                                 Tag_9_Distance_max,Tag_10_Distance_max,Tag_11_Distance_max,Tag_12_Distance_max,
                                                 Tag_13_Distance_max,Tag_14_Distance_max])
                Distance_mean=numpy.vstack([Tag_1_Distance_mean,Tag_2_Distance_mean,Tag_3_Distance_mean,Tag_4_Distance_mean,
                                                 Tag_5_Distance_mean,Tag_6_Distance_mean,Tag_7_Distance_mean,Tag_8_Distance_mean,
                                                 Tag_9_Distance_mean,Tag_10_Distance_mean,Tag_11_Distance_mean,Tag_12_Distance_mean,
                                                 Tag_13_Distance_mean,Tag_14_Distance_mean])
            else:
                pass

         Velocity_persecond=numpy.array(Velocity_persecond,dtype=numpy.float64)
         Velocity_persecond=Velocity_persecond/10
         Acceleration_persecond=numpy.array(Acceleration_persecond,dtype=numpy.float64)
         Acceleration_persecond=Acceleration_persecond
         Speed_persecond=numpy.array(Speed_persecond,dtype=numpy.float64)   
         Speed_persecond=Speed_persecond/Time_one.size
         Speed_persecond=Speed_persecond*100
         Resultant_diff_persecond=numpy.array(Resultant_diff_persecond,dtype=numpy.float64)
         Metric_length=Speed_persecond.shape[1]
         Metric_length2=list(range(1,Metric_length+1,1))
         
         Resultant_diff_max=numpy.array(Resultant_diff_max,dtype=numpy.float64)
         Resultant_Velocity_max=numpy.array(Resultant_Velocity_max,dtype=numpy.float64)       
         Resultant_Velocity_mean=numpy.array(Resultant_Velocity_mean,dtype=numpy.float64)
         Speed_max=numpy.array(Resultant_Speed_max,dtype=numpy.float64)
         Speed_mean=numpy.array(Resultant_Speed_mean,dtype=numpy.float64)
         Speed_max=Speed_max/100
         Speed_mean=Speed_mean/100
         Resultant_Acceleration_max=numpy.array(Resultant_Acceleration_max,dtype=numpy.float64)
         Resultant_Acceleration_mean=numpy.array(Resultant_Acceleration_mean,dtype=numpy.float64)
         Resultant_Acceleration_max=Resultant_Acceleration_max/10
         Resultant_Acceleration_mean=Resultant_Acceleration_mean/10
         Distance_max=numpy.array(Distance_max,dtype=numpy.float64)
         Distance_max=numpy.round(Distance_max, decimals = 0)
         Distance_mean=numpy.array(Distance_mean,dtype=numpy.float64)
         

         Resultant_diff_max=Resultant_diff_max.flatten()
         Resultant_Velocity_max=Resultant_Velocity_max.flatten()
         Resultant_Velocity_mean=Resultant_Velocity_mean.flatten()
         Speed_max=Speed_max.flatten()
         Speed_mean=Speed_mean.flatten()
         Resultant_Acceleration_max=Resultant_Acceleration_max.flatten()
         Resultant_Acceleration_mean=Resultant_Acceleration_mean.flatten()
         Distance_max=Distance_max.flatten()
         Distance_mean=Distance_mean.flatten()
 
         print("distance",Distance_max)
         print("speed",Speed_max)
         print("velocity",Resultant_Velocity_max)
         print("Accel",Resultant_Acceleration_max)

######################### W_R_ratios ##########################################       
         work_count = 0
         Work_Rest=[]
         Work_Rest1=[]
         Work_percent=[]
         Work_percent1=[]
         Velocity_Percentages_PS=[]
         Velocity_Percentages_PS1=[]
         length=(Tag_1_Velocity_persecond.size)
         Wtag1=[];Wtag2=[];Wtag3=[];Wtag4=[];Wtag5=[];Wtag6=[];Wtag7=[];Wtag8=[];Wtag9=[];Wtag10=[];Wtag11=[];Wtag12=[];Wtag13=[];Wtag14=[]
         Rtag1=[];Rtag2=[];Rtag3=[];Rtag4=[];Rtag5=[];Rtag6=[];Rtag7=[];Rtag8=[];Rtag9=[];Rtag10=[];Rtag11=[];Rtag12=[];Rtag13=[];Rtag14=[]   
         for i in range (len(Tag_dict)):                   
                 for j in range(length):
                     while i ==0:
                       if Velocity_persecond[i][j]>=2:
                             Wtag1.append(j)
                       else:
                             Rtag1.append(j)                         
                       break;                
                     while i ==1:
                       if Velocity_persecond[i][j]>=2:
                             Wtag2.append(j)
                       else:
                             Rtag2.append(j)                         
                       break;
                     while i ==2:
                       if Velocity_persecond[i][j]>=2:
                             Wtag3.append(j)
                       else:
                             Rtag3.append(j)                         
                       break;
                     while i ==3:
                       if Velocity_persecond[i][j]>=2:
                             Wtag4.append(j)
                       else:
                             Rtag4.append(j)                         
                       break;
                     while i ==4:
                       if Velocity_persecond[i][j]>=2:
                             Wtag5.append(j)
                       else:
                             Rtag5.append(j)                         
                       break;
                     while i ==5:
                       if Velocity_persecond[i][j]>=2:
                             Wtag6.append(j)
                       else:
                             Rtag6.append(j)                         
                       break;
                     while i ==6:
                       if Velocity_persecond[i][j]>=2:
                             Wtag7.append(j)
                       else:
                             Rtag7.append(j)                         
                       break;
                     while i ==7:
                       if Velocity_persecond[i][j]>=2:
                             Wtag8.append(j)
                       else:
                             Rtag8.append(j)                         
                       break;
                     while i ==8:
                       if Velocity_persecond[i][j]>=2:
                             Wtag9.append(j)
                       else:
                             Rtag9.append(j)                         
                       break;
                     while i ==9:
                       if Velocity_persecond[i][j]>=2:
                             Wtag10.append(j)
                       else:
                             Rtag10.append(j)                         
                       break;
                     while i ==10:
                       if Velocity_persecond[i][j]>=2:
                             Wtag11.append(j)
                       else:
                             Rtag11.append(j)                         
                       break; 
                     while i ==11:
                       if Velocity_persecond[i][j]>=2:
                             Wtag12.append(j)
                       else:
                             Rtag12.append(j)                         
                       break;
                     while i ==12:
                       if Velocity_persecond[i][j]>=2:
                             Wtag13.append(j)
                       else:
                             Rtag13.append(j)                         
                       break;
                     while i ==13:
                       if Velocity_persecond[i][j]>=2:
                             Wtag14.append(j)                
                       else:
                             Rtag14.append(j)
                       break;

############################################# work durations ################################################################        
         # minute 1              
         Wtag1_min1=sum(i <60 for i in Wtag1);Wtag2_min1=sum(i <60 for i in Wtag2);Wtag3_min1=sum(i <60 for i in Wtag3);
         Wtag4_min1=sum(i <60 for i in Wtag4);Wtag5_min1=sum(i <60 for i in Wtag5);Wtag6_min1=sum(i <60 for i in Wtag6);
         Wtag7_min1=sum(i <60 for i in Wtag7);Wtag8_min1=sum(i <60 for i in Wtag8);Wtag9_min1=sum(i <60 for i in Wtag9);
         Wtag10_min1=sum(i <60 for i in Wtag10);Wtag11_min1=sum(i <60 for i in Wtag11);Wtag12_min1=sum(i <60 for i in Wtag12);
         Wtag13_min1=sum(i <60 for i in Wtag13);Wtag14_min1=sum(i <60 for i in Wtag14)
         
         # minute 2
         Wtag1_min2=sum((i >=60) and (i <120) for i in Wtag1);Wtag2_min2=sum((i >=60) and (i <120) for i in Wtag2);
         Wtag3_min2=sum((i >=60) and (i <120) for i in Wtag3);Wtag4_min2=sum((i >=60) and (i <120) for i in Wtag4);
         Wtag5_min2=sum((i >=60) and (i <120) for i in Wtag5);Wtag6_min2=sum((i >=60) and (i <120) for i in Wtag6);
         Wtag7_min2=sum((i >=60) and (i <120) for i in Wtag7);Wtag8_min2=sum((i >=60) and (i <120) for i in Wtag8);
         Wtag9_min2=sum((i >=60) and (i <120) for i in Wtag9);Wtag10_min2=sum((i >=60) and (i <120) for i in Wtag10);
         Wtag11_min2=sum((i >=60) and (i <120) for i in Wtag11);Wtag12_min2=sum((i >=60) and (i <120) for i in Wtag12);
         Wtag13_min2=sum((i >=60) and (i <120) for i in Wtag13);Wtag14_min2=sum((i >=60) and (i <120) for i in Wtag14)

         # minute 3
         Wtag1_min3=sum((i>=120) and (i<180) for i in Wtag1);Wtag2_min3=sum((i>=120) and (i<180) for i in Wtag2);
         Wtag3_min3=sum((i>=120) and (i<180) for i in Wtag3);Wtag4_min3=sum((i>=120) and (i<180) for i in Wtag4);
         Wtag5_min3=sum((i>=120) and (i<180) for i in Wtag5);Wtag6_min3=sum((i>=120) and (i<180) for i in Wtag6);
         Wtag7_min3=sum((i>=120) and (i<180) for i in Wtag7);Wtag8_min3=sum((i>=120) and (i<180) for i in Wtag8);
         Wtag9_min3=sum((i>=120) and (i<180) for i in Wtag9);Wtag10_min3=sum((i>=120) and (i<180) for i in Wtag10);
         Wtag11_min3=sum((i>=120) and (i<180) for i in Wtag11);Wtag12_min3=sum((i>=120) and (i<180) for i in Wtag12);
         Wtag13_min3=sum((i>=120) and (i<180) for i in Wtag13);Wtag14_min3=sum((i>=120) and (i<180) for i in Wtag14)
         
         # minute 4
         Wtag1_min4=sum((i>=180) and (i<240) for i in Wtag1);Wtag2_min4=sum((i>=180) and (i<240) for i in Wtag2);
         Wtag3_min4=sum((i>=180) and (i<240) for i in Wtag3);Wtag4_min4=sum((i>=180) and (i<240) for i in Wtag4);
         Wtag5_min4=sum((i>=180) and (i<240) for i in Wtag5);Wtag6_min4=sum((i>=180) and (i<240) for i in Wtag6);
         Wtag7_min4=sum((i>=180) and (i<240) for i in Wtag7);Wtag8_min4=sum((i>=180) and (i<240) for i in Wtag8);
         Wtag9_min4=sum((i>=180) and (i<240) for i in Wtag9);Wtag10_min4=sum((i>=180) and (i<240) for i in Wtag10);
         Wtag11_min4=sum((i>=180) and (i<240) for i in Wtag11);Wtag12_min4=sum((i>=180) and (i<240) for i in Wtag12);
         Wtag13_min4=sum((i>=180) and (i<240) for i in Wtag13);Wtag14_min4=sum((i>=180) and (i<240) for i in Wtag14)
         
         # minute 5
         Wtag1_min5=sum((i>=240) and (i<300) for i in Wtag1);Wtag2_min5=sum((i>=240) and (i<300) for i in Wtag2);
         Wtag3_min5=sum((i>=240) and (i<300) for i in Wtag3);Wtag4_min5=sum((i>=240) and (i<300) for i in Wtag4);
         Wtag5_min5=sum((i>=240) and (i<300) for i in Wtag5);Wtag6_min5=sum((i>=240) and (i<300) for i in Wtag6);
         Wtag7_min5=sum((i>=240) and (i<300) for i in Wtag7);Wtag8_min5=sum((i>=240) and (i<300) for i in Wtag8);
         Wtag9_min5=sum((i>=240) and (i<300) for i in Wtag9);Wtag10_min5=sum((i>=240) and (i<300) for i in Wtag10);
         Wtag11_min5=sum((i>=240) and (i<300) for i in Wtag11);Wtag12_min5=sum((i>=240) and (i<300) for i in Wtag12);
         Wtag13_min5=sum((i>=240) and (i<300) for i in Wtag13);Wtag14_min5=sum((i>=240) and (i<300) for i in Wtag14)
         
         # minute 6
         Wtag1_min6=sum((i>=300) and (i<360) for i in Wtag1);Wtag2_min6=sum((i>=300) and (i<360) for i in Wtag2);
         Wtag3_min6=sum((i>=300) and (i<360) for i in Wtag3);Wtag4_min6=sum((i>=300) and (i<360) for i in Wtag4);
         Wtag5_min6=sum((i>=300) and (i<360) for i in Wtag5);Wtag6_min6=sum((i>=300) and (i<360) for i in Wtag6);
         Wtag7_min6=sum((i>=300) and (i<360) for i in Wtag7);Wtag8_min6=sum((i>=300) and (i<360) for i in Wtag8);
         Wtag9_min6=sum((i>=300) and (i<360) for i in Wtag9);Wtag10_min6=sum((i>=300) and (i<360)for i in Wtag10);
         Wtag11_min6=sum((i>=300) and (i<360) for i in Wtag11);Wtag12_min6=sum((i>=300) and (i<360) for i in Wtag12);
         Wtag13_min6=sum((i>=300) and (i<360) for i in Wtag13);Wtag14_min6=sum((i>=300) and (i<360) for i in Wtag14)
         
         # minute 7
         Wtag1_min7=sum((i>=360) and (i<420) for i in Wtag1);Wtag2_min7=sum((i>=360) and (i<420) for i in Wtag2);
         Wtag3_min7=sum((i>=360) and (i<420) for i in Wtag3);Wtag4_min7=sum((i>=360) and (i<420) for i in Wtag4);
         Wtag5_min7=sum((i>=360) and (i<420) for i in Wtag5);Wtag6_min7=sum((i>=360) and (i<420) for i in Wtag6);
         Wtag7_min7=sum((i>=360) and (i<420) for i in Wtag7);Wtag8_min7=sum((i>=360) and (i<420) for i in Wtag8);
         Wtag9_min7=sum((i>=360) and (i<420) for i in Wtag9);Wtag10_min7=sum((i>=360) and (i<420)for i in Wtag10);
         Wtag11_min7=sum((i>=360) and (i<420) for i in Wtag11);Wtag12_min7=sum((i>=360) and (i<420) for i in Wtag12);
         Wtag13_min7=sum((i>=360) and (i<420) for i in Wtag13);Wtag14_min7=sum((i>=360) and (i<420) for i in Wtag14)
         
         # minute 8
         Wtag1_min8=sum((i>=420) and (i<480) for i in Wtag1);Wtag2_min8=sum((i>=420) and (i<480) for i in Wtag2);
         Wtag3_min8=sum((i>=420) and (i<480) for i in Wtag3);Wtag4_min8=sum((i>=420) and (i<480) for i in Wtag4);
         Wtag5_min8=sum((i>=420) and (i<480) for i in Wtag5);Wtag6_min8=sum((i>=420) and (i<480) for i in Wtag6);
         Wtag7_min8=sum((i>=420) and (i<480) for i in Wtag7);Wtag8_min8=sum((i>=420) and (i<480)for i in Wtag8);
         Wtag9_min8=sum((i>=420) and (i<480) for i in Wtag9);Wtag10_min8=sum((i>=420) and (i<480)for i in Wtag10);
         Wtag11_min8=sum((i>=420) and (i<480) for i in Wtag11);Wtag12_min8=sum((i>=420) and (i<480) for i in Wtag12);
         Wtag13_min8=sum((i>=420) and (i<480) for i in Wtag13);Wtag14_min8=sum((i>=420) and (i<480) for i in Wtag14)
         
         # minute 9
         Wtag1_min9=sum((i>=480) and (i<540) for i in Wtag1);Wtag2_min9=sum((i>=480) and (i<540) for i in Wtag2);
         Wtag3_min9=sum((i>=480) and (i<540) for i in Wtag3);Wtag4_min9=sum((i>=480) and (i<540) for i in Wtag4);
         Wtag5_min9=sum((i>=480) and (i<540) for i in Wtag5);Wtag6_min9=sum((i>=480) and (i<540) for i in Wtag6);
         Wtag7_min9=sum((i>=480) and (i<540) for i in Wtag7);Wtag8_min9=sum((i>=480) and (i<540) for i in Wtag8);
         Wtag9_min9=sum((i>=480) and (i<540) for i in Wtag9);Wtag10_min9=sum((i>=480) and (i<540) for i in Wtag10);
         Wtag11_min9=sum((i>=480) and (i<540) for i in Wtag11);Wtag12_min9=sum((i>=480) and (i<540) for i in Wtag12);
         Wtag13_min9=sum((i>=480) and (i<540) for i in Wtag13);Wtag14_min9=sum((i>=480) and (i<540) for i in Wtag14)
         
         # minute 10
         Wtag1_min10=sum((i>=540) and (i<600) for i in Wtag1);Wtag2_min10=sum((i>=540) and (i<600) for i in Wtag2);
         Wtag3_min10=sum((i>=540) and (i<600) for i in Wtag3);Wtag4_min10=sum((i>=540) and (i<600) for i in Wtag4);
         Wtag5_min10=sum((i>=540) and (i<600) for i in Wtag5);Wtag6_min10=sum((i>=540) and (i<600) for i in Wtag6);
         Wtag7_min10=sum((i>=540) and (i<600) for i in Wtag7);Wtag8_min10=sum((i>=540) and (i<600) for i in Wtag8);
         Wtag9_min10=sum((i>=540) and (i<600) for i in Wtag9);Wtag10_min10=sum((i>=540) and (i<600) for i in Wtag10);
         Wtag11_min10=sum((i>=540) and (i<600) for i in Wtag11);Wtag12_min10=sum((i>=540) and (i<600) for i in Wtag12);
         Wtag13_min10=sum((i>=540) and (i<600) for i in Wtag13);Wtag14_min10=sum((i>=540) and (i<600) for i in Wtag14)
         
         # minute 11
         Wtag1_min11=sum((i>=600) and (i<660) for i in Wtag1);Wtag2_min11=sum((i>=600) and (i<660) for i in Wtag2);
         Wtag3_min11=sum((i>=600) and (i<660) for i in Wtag3);Wtag4_min11=sum((i>=600) and (i<660) for i in Wtag4);
         Wtag5_min11=sum((i>=600) and (i<660) for i in Wtag5);Wtag6_min11=sum((i>=600) and (i<660) for i in Wtag6);
         Wtag7_min11=sum((i>=600) and (i<660) for i in Wtag7);Wtag8_min11=sum((i>=600) and (i<660) for i in Wtag8);
         Wtag9_min11=sum((i>=600) and (i<660) for i in Wtag9);Wtag10_min11=sum((i>=600) and (i<660) for i in Wtag10);
         Wtag11_min11=sum((i>=600) and (i<660) for i in Wtag11);Wtag12_min11=sum((i>=600) and (i<660) for i in Wtag12);
         Wtag13_min11=sum((i>=600) and (i<660) for i in Wtag13);Wtag14_min11=sum((i>=600) and (i<660) for i in Wtag14)
         
         # minute 12
         Wtag1_min12=sum((i>=660) and (i<720) for i in Wtag1);Wtag2_min12=sum((i>=660) and (i<720) for i in Wtag2);
         Wtag3_min12=sum((i>=660) and (i<720) for i in Wtag3);Wtag4_min12=sum((i>=660) and (i<720) for i in Wtag4);
         Wtag5_min12=sum((i>=660) and (i<720) for i in Wtag5);Wtag6_min12=sum((i>=660) and (i<720) for i in Wtag6);
         Wtag7_min12=sum((i>=660) and (i<720) for i in Wtag7);Wtag8_min12=sum((i>=660) and (i<720) for i in Wtag8);
         Wtag9_min12=sum((i>=660) and (i<720) for i in Wtag9);Wtag10_min12=sum((i>=660) and (i<720) for i in Wtag10);
         Wtag11_min12=sum((i>=660) and (i<720) for i in Wtag11);Wtag12_min12=sum((i>=660) and (i<720) for i in Wtag12);
         Wtag13_min12=sum((i>=660) and (i<720) for i in Wtag13);Wtag14_min12=sum((i>=660) and (i<720) for i in Wtag14)
         
         # minute 13
         Wtag1_min13=sum((i>=720) and (i<780) for i in Wtag1);Wtag2_min13=sum((i>=720) and (i<780)for i in Wtag2);
         Wtag3_min13=sum((i>=720) and (i<780) for i in Wtag3);Wtag4_min13=sum((i>=720) and (i<780) for i in Wtag4);
         Wtag5_min13=sum((i>=720) and (i<780) for i in Wtag5);Wtag6_min13=sum((i>=720) and (i<780) for i in Wtag6);
         Wtag7_min13=sum((i>=720) and (i<780) for i in Wtag7);Wtag8_min13=sum((i>=720) and (i<780) for i in Wtag8);
         Wtag9_min13=sum((i>=720) and (i<780) for i in Wtag9);Wtag10_min13=sum((i>=720) and (i<780) for i in Wtag10);
         Wtag11_min13=sum((i>=720) and (i<780) for i in Wtag11);Wtag12_min13=sum((i>=720) and (i<780) for i in Wtag12);
         Wtag13_min13=sum((i>=720) and (i<780) for i in Wtag13);Wtag14_min13=sum((i>=720) and (i<780) for i in Wtag14)
         
         # minute 14
         Wtag1_min14=sum((i>=780) and (i<840) for i in Wtag1);Wtag2_min14=sum((i>=780) and (i<840) for i in Wtag2);
         Wtag3_min14=sum((i>=780) and (i<840) for i in Wtag3);Wtag4_min14=sum((i>=780) and (i<840) for i in Wtag4);
         Wtag5_min14=sum((i>=780) and (i<840) for i in Wtag5);Wtag6_min14=sum((i>=780) and (i<840) for i in Wtag6);
         Wtag7_min14=sum((i>=780) and (i<840) for i in Wtag7);Wtag8_min14=sum((i>=780) and (i<840) for i in Wtag8);
         Wtag9_min14=sum((i>=780) and (i<840) for i in Wtag9);Wtag10_min14=sum((i>=780) and (i<840) for i in Wtag10);
         Wtag11_min14=sum((i>=780) and (i<840)for i in Wtag11);Wtag12_min14=sum((i>=780) and (i<840) for i in Wtag12);
         Wtag13_min14=sum((i>=780) and (i<840) for i in Wtag13);Wtag14_min14=sum((i>=780) and (i<840) for i in Wtag14)
         
         # minute 15
         Wtag1_min15=sum((i>=840) and (i<=900) for i in Wtag1);Wtag2_min15=sum((i>=840) and (i<=900) for i in Wtag2);
         Wtag3_min15=sum((i>=840) and (i<=900) for i in Wtag3);Wtag4_min15=sum((i>=840) and (i<=900) for i in Wtag4);
         Wtag5_min15=sum((i>=840) and (i<=900) for i in Wtag5);Wtag6_min15=sum((i>=840) and (i<=900) for i in Wtag6);
         Wtag7_min15=sum((i>=840) and (i<=900) for i in Wtag7);Wtag8_min15=sum((i>=840) and (i<=900) for i in Wtag8);
         Wtag9_min15=sum((i>=840) and (i<=900) for i in Wtag9);Wtag10_min15=sum((i>=840) and (i<=900) for i in Wtag10);
         Wtag11_min15=sum((i>=840) and (i<=900) for i in Wtag11);Wtag12_min15=sum((i>=840) and (i<=900) for i in Wtag12);
         Wtag13_min15=sum((i>=840) and (i<=900) for i in Wtag13);Wtag14_min15=sum((i>=840) and (i<=900) for i in Wtag14)


         
         Wtag1_Work_mins=[];Wtag2_Work_mins=[];Wtag3_Work_mins=[];Wtag4_Work_mins=[];Wtag5_Work_mins=[];Wtag6_Work_mins=[];Wtag7_Work_mins=[];
         Wtag8_Work_mins=[];Wtag9_Work_mins=[];Wtag10_Work_mins=[];Wtag11_Work_mins=[];Wtag12_Work_mins=[];Wtag13_Work_mins=[];Wtag14_Work_mins=[]
         
         Wtag1_Work_mins.append([Wtag1_min1,Wtag1_min2,Wtag1_min3,Wtag1_min4,Wtag1_min5,Wtag1_min6,Wtag1_min7,Wtag1_min8,Wtag1_min9,
                                 Wtag1_min10,Wtag1_min11,Wtag1_min12,Wtag1_min13,Wtag1_min14,Wtag1_min15])
         
         Wtag2_Work_mins.append([Wtag2_min1,Wtag2_min2,Wtag2_min3,Wtag2_min4,Wtag2_min5,Wtag2_min6,Wtag2_min7,Wtag2_min8,Wtag2_min9,
                                 Wtag2_min10,Wtag2_min11,Wtag2_min12,Wtag2_min13,Wtag2_min14,Wtag2_min15])
         
         Wtag3_Work_mins.append([Wtag3_min1,Wtag1_min2,Wtag3_min3,Wtag3_min4,Wtag3_min5,Wtag3_min6,Wtag3_min7,Wtag3_min8,Wtag3_min9,
                                 Wtag3_min10,Wtag3_min11,Wtag3_min12,Wtag3_min13,Wtag3_min14,Wtag3_min15])
         
         Wtag4_Work_mins.append([Wtag4_min1,Wtag4_min2,Wtag4_min3,Wtag4_min4,Wtag4_min5,Wtag4_min6,Wtag4_min7,Wtag4_min8,Wtag4_min9,
                                 Wtag4_min10,Wtag4_min11,Wtag4_min12,Wtag4_min13,Wtag4_min14,Wtag4_min15])
         
         Wtag5_Work_mins.append([Wtag5_min1,Wtag5_min2,Wtag5_min3,Wtag5_min4,Wtag5_min5,Wtag5_min6,Wtag5_min7,Wtag5_min8,Wtag5_min9,
                                 Wtag5_min10,Wtag5_min11,Wtag5_min12,Wtag5_min13,Wtag5_min14,Wtag5_min15])
         
         Wtag6_Work_mins.append([Wtag6_min1,Wtag6_min2,Wtag6_min3,Wtag6_min4,Wtag6_min5,Wtag6_min6,Wtag6_min7,Wtag6_min8,Wtag6_min9,
                                 Wtag6_min10,Wtag6_min11,Wtag6_min12,Wtag6_min13,Wtag6_min14,Wtag6_min15])
         
         Wtag7_Work_mins.append([Wtag7_min1,Wtag7_min2,Wtag7_min3,Wtag7_min4,Wtag7_min5,Wtag7_min6,Wtag7_min7,Wtag7_min8,Wtag7_min9,
                                 Wtag7_min10,Wtag7_min11,Wtag7_min12,Wtag7_min13,Wtag7_min14,Wtag7_min15])
         
         Wtag8_Work_mins.append([Wtag8_min1,Wtag8_min2,Wtag8_min3,Wtag8_min4,Wtag8_min5,Wtag8_min6,Wtag8_min7,Wtag8_min8,Wtag8_min9,
                               Wtag8_min10,Wtag8_min11,Wtag8_min12,Wtag8_min13,Wtag8_min14,Wtag8_min15])
         
         Wtag9_Work_mins.append([Wtag9_min1,Wtag9_min2,Wtag9_min3,Wtag9_min4,Wtag9_min5,Wtag9_min6,Wtag9_min7,Wtag9_min8,Wtag9_min9,
                                 Wtag9_min10,Wtag9_min11,Wtag9_min12,Wtag9_min13,Wtag9_min14,Wtag9_min15])
         
         Wtag10_Work_mins.append([Wtag10_min1,Wtag10_min2,Wtag10_min3,Wtag10_min4,Wtag10_min5,Wtag10_min6,Wtag10_min7,Wtag10_min8,Wtag10_min9,
                                 Wtag10_min10,Wtag10_min11,Wtag10_min12,Wtag10_min13,Wtag10_min14,Wtag10_min15])
         
         Wtag11_Work_mins.append([Wtag11_min1,Wtag11_min2,Wtag11_min3,Wtag11_min4,Wtag11_min5,Wtag11_min6,Wtag11_min7,Wtag11_min8,Wtag11_min9,
                                 Wtag11_min10,Wtag11_min11,Wtag11_min12,Wtag11_min13,Wtag11_min14,Wtag11_min15])
         
         Wtag12_Work_mins.append([Wtag12_min1,Wtag12_min2,Wtag12_min3,Wtag12_min4,Wtag12_min5,Wtag12_min6,Wtag12_min7,Wtag12_min8,Wtag12_min9,
                                 Wtag12_min10,Wtag12_min11,Wtag12_min12,Wtag12_min13,Wtag12_min14,Wtag12_min15])
         
         Wtag13_Work_mins.append([Wtag13_min1,Wtag13_min2,Wtag13_min3,Wtag13_min4,Wtag13_min5,Wtag13_min6,Wtag13_min7,Wtag13_min8,Wtag13_min9,
                                 Wtag13_min10,Wtag13_min11,Wtag13_min12,Wtag13_min13,Wtag13_min14,Wtag13_min15])
         
         Wtag14_Work_mins.append([Wtag14_min1,Wtag14_min2,Wtag14_min3,Wtag14_min4,Wtag14_min5,Wtag14_min6,Wtag14_min7,Wtag14_min8,Wtag14_min9,
                                 Wtag14_min10,Wtag14_min11,Wtag14_min12,Wtag14_min13,Wtag14_min14,Wtag14_min15])
         
############################################# Rest durations ################################################################
         # minute 1              
         Rtag1_min1=sum(i <60 for i in Rtag1);Rtag2_min1=sum(i <60 for i in Rtag2);Rtag3_min1=sum(i <60 for i in Rtag3);
         Rtag4_min1=sum(i <60 for i in Rtag4);Rtag5_min1=sum(i <60 for i in Rtag5);Rtag6_min1=sum(i <60 for i in Rtag6);
         Rtag7_min1=sum(i <60 for i in Rtag7);Rtag8_min1=sum(i <60 for i in Rtag8);Rtag9_min1=sum(i <60 for i in Rtag9);
         Rtag10_min1=sum(i <60 for i in Rtag10);Rtag11_min1=sum(i <60 for i in Rtag11);Rtag12_min1=sum(i <60 for i in Rtag12);
         Rtag13_min1=sum(i <60 for i in Rtag13);Rtag14_min1=sum(i <60 for i in Rtag14)

         # minute 2
         Rtag1_min2=sum((i >=60) and (i <120) for i in Rtag1);Rtag2_min2=sum((i >=60) and (i <120) for i in Rtag2);
         Rtag3_min2=sum((i >=60) and (i <120) for i in Rtag3);Rtag4_min2=sum((i >=60) and (i <120) for i in Rtag4);
         Rtag5_min2=sum((i >=60) and (i <120) for i in Rtag5);Rtag6_min2=sum((i >=60) and (i <120) for i in Rtag6);
         Rtag7_min2=sum((i >=60) and (i <120) for i in Rtag7);Rtag8_min2=sum((i >=60) and (i <120) for i in Rtag8);
         Rtag9_min2=sum((i >=60) and (i <120) for i in Rtag9);Rtag10_min2=sum((i >=60) and (i <120) for i in Rtag10);
         Rtag11_min2=sum((i >=60) and (i <120) for i in Rtag11);Rtag12_min2=sum((i >=60) and (i <120) for i in Rtag12);
         Rtag13_min2=sum((i >=60) and (i <120) for i in Rtag13);Rtag14_min2=sum((i >=60) and (i <120) for i in Rtag14)

         # minute 3
         Rtag1_min3=sum((i>=120) and (i<180) for i in Rtag1);Rtag2_min3=sum((i>=120) and (i<180) for i in Rtag2);
         Rtag3_min3=sum((i>=120) and (i<180) for i in Rtag3);Rtag4_min3=sum((i>=120) and (i<180) for i in Rtag4);
         Rtag5_min3=sum((i>=120) and (i<180) for i in Rtag5);Rtag6_min3=sum((i>=120) and (i<180) for i in Rtag6);
         Rtag7_min3=sum((i>=120) and (i<180) for i in Rtag7);Rtag8_min3=sum((i>=120) and (i<180) for i in Rtag8);
         Rtag9_min3=sum((i>=120) and (i<180) for i in Rtag9);Rtag10_min3=sum((i>=120) and (i<180) for i in Rtag10);
         Rtag11_min3=sum((i>=120) and (i<180) for i in Rtag11);Rtag12_min3=sum((i>=120) and (i<180) for i in Rtag12);
         Rtag13_min3=sum((i>=120) and (i<180) for i in Rtag13);Rtag14_min3=sum((i>=120) and (i<180) for i in Rtag14)
         
         # minute 4
         Rtag1_min4=sum((i>=180) and (i<240) for i in Rtag1);Rtag2_min4=sum((i>=180) and (i<240) for i in Rtag2);
         Rtag3_min4=sum((i>=180) and (i<240) for i in Rtag3);Rtag4_min4=sum((i>=180) and (i<240) for i in Rtag4);
         Rtag5_min4=sum((i>=180) and (i<240) for i in Rtag5);Rtag6_min4=sum((i>=180) and (i<240) for i in Rtag6);
         Rtag7_min4=sum((i>=180) and (i<240) for i in Rtag7);Rtag8_min4=sum((i>=180) and (i<240) for i in Rtag8);
         Rtag9_min4=sum((i>=180) and (i<240) for i in Rtag9);Rtag10_min4=sum((i>=180) and (i<240) for i in Rtag10);
         Rtag11_min4=sum((i>=180) and (i<240) for i in Rtag11);Rtag12_min4=sum((i>=180) and (i<240) for i in Rtag12);
         Rtag13_min4=sum((i>=180) and (i<240) for i in Rtag13);Rtag14_min4=sum((i>=180) and (i<240) for i in Rtag14)
         
         # minute 5
         Rtag1_min5=sum((i>=240) and (i<300) for i in Rtag1);Rtag2_min5=sum((i>=240) and (i<300) for i in Rtag2);
         Rtag3_min5=sum((i>=240) and (i<300) for i in Rtag3);Rtag4_min5=sum((i>=240) and (i<300) for i in Rtag4);
         Rtag5_min5=sum((i>=240) and (i<300) for i in Rtag5);Rtag6_min5=sum((i>=240) and (i<300) for i in Rtag6);
         Rtag7_min5=sum((i>=240) and (i<300) for i in Rtag7);Rtag8_min5=sum((i>=240) and (i<300) for i in Rtag8);
         Rtag9_min5=sum((i>=240) and (i<300) for i in Rtag9);Rtag10_min5=sum((i>=240) and (i<300) for i in Rtag10);
         Rtag11_min5=sum((i>=240) and (i<300) for i in Rtag11);Rtag12_min5=sum((i>=240) and (i<300) for i in Rtag12);
         Rtag13_min5=sum((i>=240) and (i<300) for i in Rtag13);Rtag14_min5=sum((i>=240) and (i<300) for i in Rtag14)
         
         # minute 6
         Rtag1_min6=sum((i>=300) and (i<360) for i in Rtag1);Rtag2_min6=sum((i>=300) and (i<360) for i in Rtag2);
         Rtag3_min6=sum((i>=300) and (i<360) for i in Rtag3);Rtag4_min6=sum((i>=300) and (i<360) for i in Rtag4);
         Rtag5_min6=sum((i>=300) and (i<360) for i in Rtag5);Rtag6_min6=sum((i>=300) and (i<360) for i in Rtag6);
         Rtag7_min6=sum((i>=300) and (i<360) for i in Rtag7);Rtag8_min6=sum((i>=300) and (i<360) for i in Rtag8);
         Rtag9_min6=sum((i>=300) and (i<360) for i in Rtag9);Rtag10_min6=sum((i>=300) and (i<360)for i in Rtag10);
         Rtag11_min6=sum((i>=300) and (i<360) for i in Rtag11);Rtag12_min6=sum((i>=300) and (i<360) for i in Rtag12);
         Rtag13_min6=sum((i>=300) and (i<360) for i in Rtag13);Rtag14_min6=sum((i>=300) and (i<360) for i in Rtag14)
         
         # minute 7
         Rtag1_min7=sum((i>=360) and (i<420) for i in Rtag1);Rtag2_min7=sum((i>=360) and (i<420) for i in Rtag2);
         Rtag3_min7=sum((i>=360) and (i<420) for i in Rtag3);Rtag4_min7=sum((i>=360) and (i<420) for i in Rtag4);
         Rtag5_min7=sum((i>=360) and (i<420) for i in Rtag5);Rtag6_min7=sum((i>=360) and (i<420) for i in Rtag6);
         Rtag7_min7=sum((i>=360) and (i<420) for i in Rtag7);Rtag8_min7=sum((i>=360) and (i<420) for i in Rtag8);
         Rtag9_min7=sum((i>=360) and (i<420) for i in Rtag9);Rtag10_min7=sum((i>=360) and (i<420)for i in Rtag10);
         Rtag11_min7=sum((i>=360) and (i<420) for i in Rtag11);Rtag12_min7=sum((i>=360) and (i<420) for i in Rtag12);
         Rtag13_min7=sum((i>=360) and (i<420) for i in Rtag13);Rtag14_min7=sum((i>=360) and (i<420) for i in Rtag14)
         
         # minute 8
         Rtag1_min8=sum((i>=420) and (i<480) for i in Rtag1);Rtag2_min8=sum((i>=420) and (i<480) for i in Rtag2);
         Rtag3_min8=sum((i>=420) and (i<480) for i in Rtag3);Rtag4_min8=sum((i>=420) and (i<480) for i in Rtag4);
         Rtag5_min8=sum((i>=420) and (i<480) for i in Rtag5);Rtag6_min8=sum((i>=420) and (i<480) for i in Rtag6);
         Rtag7_min8=sum((i>=420) and (i<480) for i in Rtag7);Rtag8_min8=sum((i>=420) and (i<480)for i in Rtag8);
         Rtag9_min8=sum((i>=420) and (i<480) for i in Rtag9);Rtag10_min8=sum((i>=420) and (i<480)for i in Rtag10);
         Rtag11_min8=sum((i>=420) and (i<480) for i in Rtag11);Rtag12_min8=sum((i>=420) and (i<480) for i in Rtag12);
         Rtag13_min8=sum((i>=420) and (i<480) for i in Rtag13);Rtag14_min8=sum((i>=420) and (i<480) for i in Rtag14)
         
         # minute 9
         Rtag1_min9=sum((i>=480) and (i<540) for i in Rtag1);Rtag2_min9=sum((i>=480) and (i<540) for i in Rtag2);
         Rtag3_min9=sum((i>=480) and (i<540) for i in Rtag3);Rtag4_min9=sum((i>=480) and (i<540) for i in Rtag4);
         Rtag5_min9=sum((i>=480) and (i<540) for i in Rtag5);Rtag6_min9=sum((i>=480) and (i<540) for i in Rtag6);
         Rtag7_min9=sum((i>=480) and (i<540) for i in Rtag7);Rtag8_min9=sum((i>=480) and (i<540) for i in Rtag8);
         Rtag9_min9=sum((i>=480) and (i<540) for i in Rtag9);Rtag10_min9=sum((i>=480) and (i<540) for i in Rtag10);
         Rtag11_min9=sum((i>=480) and (i<540) for i in Rtag11);Rtag12_min9=sum((i>=480) and (i<540) for i in Rtag12);
         Rtag13_min9=sum((i>=480) and (i<540) for i in Rtag13);Rtag14_min9=sum((i>=480) and (i<540) for i in Rtag14)        

         # minute 10
         Rtag1_min10=sum((i>=540) and (i<600) for i in Rtag1);Rtag2_min10=sum((i>=540) and (i<600) for i in Rtag2);
         Rtag3_min10=sum((i>=540) and (i<600) for i in Rtag3);Rtag4_min10=sum((i>=540) and (i<600) for i in Rtag4);
         Rtag5_min10=sum((i>=540) and (i<600) for i in Rtag5);Rtag6_min10=sum((i>=540) and (i<600) for i in Rtag6);
         Rtag7_min10=sum((i>=540) and (i<600) for i in Rtag7);Rtag8_min10=sum((i>=540) and (i<600) for i in Rtag8);
         Rtag9_min10=sum((i>=540) and (i<600) for i in Rtag9);Rtag10_min10=sum((i>=540) and (i<600) for i in Rtag10);
         Rtag11_min10=sum((i>=540) and (i<600) for i in Rtag11);Rtag12_min10=sum((i>=540) and (i<600) for i in Rtag12);
         Rtag13_min10=sum((i>=540) and (i<600) for i in Rtag13);Rtag14_min10=sum((i>=540) and (i<600) for i in Rtag14)
         
         # minute 11
         Rtag1_min11=sum((i>=600) and (i<660) for i in Rtag1);Rtag2_min11=sum((i>=600) and (i<660) for i in Rtag2);
         Rtag3_min11=sum((i>=600) and (i<660) for i in Rtag3);Rtag4_min11=sum((i>=600) and (i<660) for i in Rtag4);
         Rtag5_min11=sum((i>=600) and (i<660) for i in Rtag5);Rtag6_min11=sum((i>=600) and (i<660) for i in Rtag6);
         Rtag7_min11=sum((i>=600) and (i<660) for i in Rtag7);Rtag8_min11=sum((i>=600) and (i<660) for i in Rtag8);
         Rtag9_min11=sum((i>=600) and (i<660) for i in Rtag9);Rtag10_min11=sum((i>=600) and (i<660) for i in Rtag10);
         Rtag11_min11=sum((i>=600) and (i<660) for i in Rtag11);Rtag12_min11=sum((i>=600) and (i<660) for i in Rtag12);
         Rtag13_min11=sum((i>=600) and (i<660) for i in Rtag13);Rtag14_min11=sum((i>=600) and (i<660) for i in Rtag14)
         
         # minute 12
         Rtag1_min12=sum((i>=660) and (i<720) for i in Rtag1);Rtag2_min12=sum((i>=660) and (i<720) for i in Rtag2);
         Rtag3_min12=sum((i>=660) and (i<720) for i in Rtag3);Rtag4_min12=sum((i>=660) and (i<720) for i in Rtag4);
         Rtag5_min12=sum((i>=660) and (i<720) for i in Rtag5);Rtag6_min12=sum((i>=660) and (i<720) for i in Rtag6);
         Rtag7_min12=sum((i>=660) and (i<720) for i in Rtag7);Rtag8_min12=sum((i>=660) and (i<720) for i in Rtag8);
         Rtag9_min12=sum((i>=660) and (i<720) for i in Rtag9);Rtag10_min12=sum((i>=660) and (i<720) for i in Rtag10);
         Rtag11_min12=sum((i>=660) and (i<720) for i in Rtag11);Rtag12_min12=sum((i>=660) and (i<720) for i in Rtag12);
         Rtag13_min12=sum((i>=660) and (i<720) for i in Rtag13);Rtag14_min12=sum((i>=660) and (i<720) for i in Rtag14)
         
         # minute 13
         Rtag1_min13=sum((i>=720) and (i<780) for i in Rtag1);Rtag2_min13=sum((i>=720) and (i<780)for i in Rtag2);
         Rtag3_min13=sum((i>=720) and (i<780) for i in Rtag3);Rtag4_min13=sum((i>=720) and (i<780) for i in Rtag4);
         Rtag5_min13=sum((i>=720) and (i<780) for i in Rtag5);Rtag6_min13=sum((i>=720) and (i<780) for i in Rtag6);
         Rtag7_min13=sum((i>=720) and (i<780) for i in Rtag7);Rtag8_min13=sum((i>=720) and (i<780) for i in Rtag8);
         Rtag9_min13=sum((i>=720) and (i<780) for i in Rtag9);Rtag10_min13=sum((i>=720) and (i<780) for i in Rtag10);
         Rtag11_min13=sum((i>=720) and (i<780) for i in Rtag11);Rtag12_min13=sum((i>=720) and (i<780) for i in Rtag12);
         Rtag13_min13=sum((i>=720) and (i<780) for i in Rtag13);Rtag14_min13=sum((i>=720) and (i<780) for i in Rtag14)
         
         # minute 14
         Rtag1_min14=sum((i>=780) and (i<840) for i in Rtag1);Rtag2_min14=sum((i>=780) and (i<840) for i in Rtag2);
         Rtag3_min14=sum((i>=780) and (i<840) for i in Rtag3);Rtag4_min14=sum((i>=780) and (i<840) for i in Rtag4);
         Rtag5_min14=sum((i>=780) and (i<840) for i in Rtag5);Rtag6_min14=sum((i>=780) and (i<840) for i in Rtag6);
         Rtag7_min14=sum((i>=780) and (i<840) for i in Rtag7);Rtag8_min14=sum((i>=780) and (i<840) for i in Rtag8);
         Rtag9_min14=sum((i>=780) and (i<840) for i in Rtag9);Rtag10_min14=sum((i>=780) and (i<840) for i in Rtag10);
         Rtag11_min14=sum((i>=780) and (i<840)for i in Rtag11);Rtag12_min14=sum((i>=780) and (i<840) for i in Rtag12);
         Rtag13_min14=sum((i>=780) and (i<840) for i in Rtag13);Rtag14_min14=sum((i>=780) and (i<840) for i in Rtag14)
         
         # minute 15
         Rtag1_min15=sum((i>=840) and (i<=900) for i in Rtag1);Rtag2_min15=sum((i>=840) and (i<=900) for i in Rtag2);
         Rtag3_min15=sum((i>=840) and (i<=900) for i in Rtag3);Rtag4_min15=sum((i>=840) and (i<=900) for i in Rtag4);
         Rtag5_min15=sum((i>=840) and (i<=900) for i in Rtag5);Rtag6_min15=sum((i>=840) and (i<=900) for i in Rtag6);
         Rtag7_min15=sum((i>=840) and (i<=900) for i in Rtag7);Rtag8_min15=sum((i>=840) and (i<=900) for i in Rtag8);
         Rtag9_min15=sum((i>=840) and (i<=900) for i in Rtag9);Rtag10_min15=sum((i>=840) and (i<=900) for i in Rtag10);
         Rtag11_min15=sum((i>=840) and (i<=900) for i in Rtag11);Rtag12_min15=sum((i>=840) and (i<=900) for i in Rtag12);
         Rtag13_min15=sum((i>=840) and (i<=900) for i in Rtag13);Rtag14_min15=sum((i>=840) and (i<=900) for i in Rtag14)

##         print(Wtag1_min1,Rtag1_min1,Wtag14_min1,Rtag14_min1)
##         print(Wtag1_min2,Rtag1_min2,Wtag14_min2,Rtag14_min2)
##         print(Wtag1_min3,Rtag1_min3,Wtag14_min3,Rtag14_min3)
##         print(Wtag1_min4,Rtag1_min4,Wtag14_min4,Rtag14_min4)
##         print(Wtag1_min5,Rtag1_min5,Wtag14_min5,Rtag14_min5)
##         print(Wtag1_min6,Rtag1_min6,Wtag14_min6,Rtag14_min6)
##         print(Wtag1_min7,Rtag1_min7,Wtag14_min7,Rtag14_min7)
##         print(Wtag1_min8,Rtag1_min8,Wtag14_min8,Rtag14_min8)
##         print(Wtag1_min9,Rtag1_min9,Wtag14_min9,Rtag14_min9)
##         print(Wtag1_min10,Rtag1_min10,Wtag14_min10,Rtag14_min10)
##         print(Wtag1_min11,Rtag1_min11,Wtag14_min11,Rtag14_min11)
##         print(Wtag1_min12,Rtag1_min12,Wtag14_min12,Rtag14_min12)
##         print(Wtag1_min13,Rtag1_min13,Wtag14_min13,Rtag14_min13)
##         print(Wtag1_min14,Rtag1_min14,Wtag14_min14,Rtag14_min14)
##         print(Wtag1_min15,Rtag1_min15,Wtag14_min15,Rtag14_min15)

      
         Rtag1_Work_mins=[];Rtag2_Work_mins=[];Rtag3_Work_mins=[];Rtag4_Work_mins=[];Rtag5_Work_mins=[];Rtag6_Work_mins=[];Rtag7_Work_mins=[];
         Rtag8_Work_mins=[];Rtag9_Work_mins=[];Rtag10_Work_mins=[];Rtag11_Work_mins=[];Rtag12_Work_mins=[];Rtag13_Work_mins=[];Rtag14_Work_mins=[]
         
         Rtag1_Work_mins.append([Rtag1_min1,Rtag1_min2,Rtag1_min3,Rtag1_min4,Rtag1_min5,Rtag1_min6,Rtag1_min7,Rtag1_min8,Rtag1_min9,
                                 Rtag1_min10,Rtag1_min11,Rtag1_min12,Rtag1_min13,Rtag1_min14,Rtag1_min15])
         
         Rtag2_Work_mins.append([Rtag2_min1,Rtag2_min2,Rtag2_min3,Rtag2_min4,Rtag2_min5,Rtag2_min6,Rtag2_min7,Rtag2_min8,Rtag2_min9,
                                 Rtag2_min10,Rtag2_min11,Rtag2_min12,Rtag2_min13,Rtag2_min14,Rtag2_min15])
         
         Rtag3_Work_mins.append([Rtag3_min1,Rtag1_min2,Rtag3_min3,Rtag3_min4,Rtag3_min5,Rtag3_min6,Rtag3_min7,Rtag3_min8,Rtag3_min9,
                                 Rtag3_min10,Rtag3_min11,Rtag3_min12,Rtag3_min13,Rtag3_min14,Rtag3_min15])
         
         Rtag4_Work_mins.append([Rtag4_min1,Rtag4_min2,Rtag4_min3,Rtag4_min4,Rtag4_min5,Rtag4_min6,Rtag4_min7,Rtag4_min8,Rtag4_min9,
                                 Rtag4_min10,Rtag4_min11,Rtag4_min12,Rtag4_min13,Rtag4_min14,Rtag4_min15])
         
         Rtag5_Work_mins.append([Rtag5_min1,Rtag5_min2,Rtag5_min3,Rtag5_min4,Rtag5_min5,Rtag5_min6,Rtag5_min7,Rtag5_min8,Rtag5_min9,
                                 Rtag5_min10,Rtag5_min11,Rtag5_min12,Rtag5_min13,Rtag5_min14,Rtag5_min15])
         
         Rtag6_Work_mins.append([Rtag6_min1,Rtag6_min2,Rtag6_min3,Rtag6_min4,Rtag6_min5,Rtag6_min6,Rtag6_min7,Rtag6_min8,Rtag6_min9,
                                 Rtag6_min10,Rtag6_min11,Rtag6_min12,Rtag6_min13,Rtag6_min14,Rtag6_min15])
         
         Rtag7_Work_mins.append([Rtag7_min1,Rtag7_min2,Rtag7_min3,Rtag7_min4,Rtag7_min5,Rtag7_min6,Rtag7_min7,Rtag7_min8,Rtag7_min9,
                                 Rtag7_min10,Rtag7_min11,Rtag7_min12,Rtag7_min13,Rtag7_min14,Rtag7_min15])
         
         Rtag8_Work_mins.append([Rtag8_min1,Rtag8_min2,Rtag8_min3,Rtag8_min4,Rtag8_min5,Rtag8_min6,Rtag8_min7,Rtag8_min8,Rtag8_min9,
                               Rtag8_min10,Rtag8_min11,Rtag8_min12,Rtag8_min13,Rtag8_min14,Rtag8_min15])
         
         Rtag9_Work_mins.append([Rtag9_min1,Rtag9_min2,Rtag9_min3,Rtag9_min4,Rtag9_min5,Rtag9_min6,Rtag9_min7,Rtag9_min8,Rtag9_min9,
                                 Rtag9_min10,Rtag9_min11,Rtag9_min12,Rtag9_min13,Rtag9_min14,Rtag9_min15])
         
         Rtag10_Work_mins.append([Rtag10_min1,Rtag10_min2,Rtag10_min3,Rtag10_min4,Rtag10_min5,Rtag10_min6,Rtag10_min7,Rtag10_min8,Rtag10_min9,
                                 Rtag10_min10,Rtag10_min11,Rtag10_min12,Rtag10_min13,Rtag10_min14,Rtag10_min15])
         
         Rtag11_Work_mins.append([Rtag11_min1,Rtag11_min2,Rtag11_min3,Rtag11_min4,Rtag11_min5,Rtag11_min6,Rtag11_min7,Rtag11_min8,Rtag11_min9,
                                 Rtag11_min10,Rtag11_min11,Rtag11_min12,Rtag11_min13,Rtag11_min14,Rtag11_min15])
         
         Rtag12_Work_mins.append([Rtag12_min1,Rtag12_min2,Rtag12_min3,Rtag12_min4,Rtag12_min5,Rtag12_min6,Rtag12_min7,Rtag12_min8,Rtag12_min9,
                                 Rtag12_min10,Rtag12_min11,Rtag12_min12,Rtag12_min13,Rtag12_min14,Rtag12_min15])
         
         Rtag13_Work_mins.append([Rtag13_min1,Rtag13_min2,Rtag13_min3,Rtag13_min4,Rtag13_min5,Rtag13_min6,Rtag13_min7,Rtag13_min8,Rtag13_min9,
                                 Rtag13_min10,Rtag13_min11,Rtag13_min12,Rtag13_min13,Rtag13_min14,Rtag13_min15])
         
         Rtag14_Work_mins.append([Rtag14_min1,Rtag14_min2,Rtag14_min3,Rtag14_min4,Rtag14_min5,Rtag14_min6,Rtag14_min7,Rtag14_min8,Rtag14_min9,
                                 Rtag14_min10,Rtag14_min11,Rtag14_min12,Rtag14_min13,Rtag14_min14,Rtag14_min15])

         Work_Percent=[]
         Rest_Percent=[]
         
         Work_Percent.append([Wtag1_Work_mins,Wtag2_Work_mins,Wtag3_Work_mins,Wtag4_Work_mins,Wtag5_Work_mins,Wtag6_Work_mins,
                              Wtag7_Work_mins,Wtag8_Work_mins,Wtag9_Work_mins,Wtag10_Work_mins,Wtag11_Work_mins,Wtag12_Work_mins,Wtag13_Work_mins,
                              Wtag14_Work_mins])
                              
         Rest_Percent.append([Rtag1_Work_mins,Rtag2_Work_mins,Rtag3_Work_mins,Rtag4_Work_mins,Rtag5_Work_mins,Rtag6_Work_mins,
                              Rtag7_Work_mins,Rtag8_Work_mins,Rtag9_Work_mins,Rtag10_Work_mins,Rtag11_Work_mins,Rtag12_Work_mins,Rtag13_Work_mins,
                              Rtag14_Work_mins])
         
         Work_Percent=numpy.array(Work_Percent,dtype=numpy.float64)
         Rest_Percent=numpy.array(Rest_Percent,dtype=numpy.float64)
 
         Work_Percent=numpy.round((Work_Percent/60)*100, decimals = 0)
         Rest_Percent=numpy.round((Rest_Percent/60)*100, decimals = 0) #[0] = ignore,[#]= tag column,[0]=ignore,[#] = minute column
         Average_Work=[]
         Average_Rest=[]

         
         for i in range(len(Distance)):
             Average_Work.append(numpy.round(numpy.mean(Work_Percent[0][i][:][:]),decimals = 0))
             Average_Rest.append(numpy.round(numpy.mean(Rest_Percent[0][i][:][:]),decimals = 0))
                   
        
################################################Work percentages ###################################################################################
         VP_Z1_Tag1=[]; VP_Z1_Tag2=[]; VP_Z1_Tag3=[]; VP_Z1_Tag4=[]; VP_Z1_Tag5=[]; VP_Z1_Tag6=[]; VP_Z1_Tag7=[]; VP_Z1_Tag8=[]; VP_Z1_Tag9=[]; VP_Z1_Tag10=[]; VP_Z1_Tag11=[];
         VP_Z1_Tag12=[]; VP_Z1_Tag13=[]; VP_Z1_Tag14=[];

         VP_Z2_Tag1=[]; VP_Z2_Tag2=[]; VP_Z2_Tag3=[]; VP_Z2_Tag4=[]; VP_Z2_Tag5=[]; VP_Z2_Tag6=[]; VP_Z2_Tag7=[]; VP_Z2_Tag8=[]; VP_Z2_Tag9=[]; VP_Z2_Tag10=[]; VP_Z2_Tag11=[];
         VP_Z2_Tag12=[]; VP_Z2_Tag13=[]; VP_Z2_Tag14=[];

         VP_Z3_Tag1=[]; VP_Z3_Tag2=[]; VP_Z3_Tag3=[]; VP_Z3_Tag4=[]; VP_Z3_Tag5=[]; VP_Z3_Tag6=[]; VP_Z3_Tag7=[]; VP_Z3_Tag8=[]; VP_Z3_Tag9=[]; VP_Z3_Tag10=[]; VP_Z3_Tag11=[];
         VP_Z3_Tag12=[]; VP_Z3_Tag13=[]; VP_Z3_Tag14=[];

         VP_Z4_Tag1=[]; VP_Z4_Tag2=[]; VP_Z4_Tag3=[]; VP_Z4_Tag4=[]; VP_Z4_Tag5=[]; VP_Z4_Tag6=[]; VP_Z4_Tag7=[]; VP_Z4_Tag8=[]; VP_Z4_Tag9=[]; VP_Z4_Tag10=[]; VP_Z4_Tag11=[];
         VP_Z4_Tag12=[]; VP_Z4_Tag13=[]; VP_Z4_Tag14=[];

         VP_Z5_Tag1=[]; VP_Z5_Tag2=[]; VP_Z5_Tag3=[]; VP_Z5_Tag4=[]; VP_Z5_Tag5=[]; VP_Z5_Tag6=[]; VP_Z5_Tag7=[]; VP_Z5_Tag8=[]; VP_Z5_Tag9=[]; VP_Z5_Tag10=[]; VP_Z5_Tag11=[];
         VP_Z5_Tag12=[]; VP_Z5_Tag13=[]; VP_Z5_Tag14=[];
         for i in range (len(Tag_dict)): 
             for j in range(length):
                  if i==0:
                      if Velocity_persecond[i][j]<2:
                          VP_Z1_Tag1.append(j)                       
                      elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                          VP_Z2_Tag1.append(j)
                      elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                          VP_Z3_Tag1.append(j)
                      elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                          VP_Z4_Tag1.append(j)
                      elif Velocity_persecond[i][j]>=8:
                          VP_Z5_Tag1.append(j)
                  if i==1: 
                      if Velocity_persecond[i][j]<2:
                          VP_Z1_Tag2.append(j)
                      elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                          VP_Z2_Tag2.append(j)
                      elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                          VP_Z3_Tag2.append(j)
                      elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                          VP_Z4_Tag2.append(j)
                      elif Velocity_persecond[i][j]>=8:
                          VP_Z5_Tag2.append(j)                          
                  if i==2:
                      if Velocity_persecond[i][j]<2:
                          VP_Z1_Tag3.append(j)
                      elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                          VP_Z2_Tag3.append(j)
                      elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                          VP_Z3_Tag3.append(j)
                      elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                          VP_Z4_Tag3.append(j)
                      elif Velocity_persecond[i][j]>=8:
                          VP_Z5_Tag3.append(j)                          
                  if i==3:
                      if Velocity_persecond[i][j]<2:
                          VP_Z1_Tag4.append(j)
                      elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                          VP_Z2_Tag4.append(j)
                      elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                          VP_Z3_Tag4.append(j)
                      elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                          VP_Z4_Tag4.append(j)
                      elif Velocity_persecond[i][j]>=8:
                          VP_Z5_Tag4.append(j)                          
                  if i==4:
                      if Velocity_persecond[i][j]<2:
                          VP_Z1_Tag5.append(j)   
                      elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                          VP_Z2_Tag5.append(j) 
                      elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                          VP_Z3_Tag5.append(j) 
                      elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                          VP_Z4_Tag5.append(j) 
                      elif Velocity_persecond[i][j]>=8:
                          VP_Z5_Tag5.append(j) 
                  if i==5:
                      if Velocity_persecond[i][j]<2:
                          VP_Z1_Tag6.append(j)    
                      elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                          VP_Z2_Tag6.append(j)
                      elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                          VP_Z3_Tag6.append(j)
                      elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                          VP_Z4_Tag6.append(j)
                      elif Velocity_persecond[i][j]>=8:
                          VP_Z5_Tag6.append(j)
                  if i==6:
                      if Velocity_persecond[i][j]<2:
                          VP_Z1_Tag7.append(j)    
                      elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:                          
                          VP_Z2_Tag7.append(j) 
                      elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                          VP_Z3_Tag7.append(j) 
                      elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                          VP_Z4_Tag7.append(j) 
                      elif Velocity_persecond[i][j]>=8:
                          VP_Z5_Tag7.append(j) 
                  if i==7:
                      if Velocity_persecond[i][j]<2:
                          VP_Z1_Tag8.append(j)    
                      elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                          VP_Z2_Tag8.append(j) 
                      elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                          VP_Z3_Tag8.append(j) 
                      elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                          VP_Z4_Tag8.append(j) 
                      elif Velocity_persecond[i][j]>=8:
                          VP_Z5_Tag8.append(j) 
                  if i==8:
                      if Velocity_persecond[i][j]<2:
                          VP_Z1_Tag9.append(j)    
                      elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                          VP_Z2_Tag9.append(j)
                      elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                          VP_Z3_Tag9.append(j)
                      elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                          VP_Z4_Tag9.append(j)
                      elif Velocity_persecond[i][j]>=8:
                          VP_Z5_Tag9.append(j)
                  if i==9:
                      if Velocity_persecond[i][j]<2:
                          VP_Z1_Tag10.append(j)    
                      elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                          VP_Z2_Tag10.append(j)
                      elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                          VP_Z3_Tag10.append(j)
                      elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                          VP_Z4_Tag10.append(j)
                      elif Velocity_persecond[i][j]>=8:
                          VP_Z5_Tag10.append(j)
                  if i==10:
                      if Velocity_persecond[i][j]<2:
                          VP_Z1_Tag11.append(j)    
                      elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                          VP_Z2_Tag11.append(j)  
                      elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                          VP_Z3_Tag11.append(j)  
                      elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                          VP_Z4_Tag11.append(j)  
                      elif Velocity_persecond[i][j]>=8:
                          VP_Z5_Tag11.append(j)  
                  if i==11:
                      if Velocity_persecond[i][j]<2:
                          VP_Z1_Tag12.append(j)    
                      elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                          VP_Z2_Tag12.append(j) 
                      elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                          VP_Z3_Tag12.append(j) 
                      elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                          VP_Z4_Tag12.append(j) 
                      elif Velocity_persecond[i][j]>=8:
                          VP_Z5_Tag12.append(j) 
                  if i==12:
                      if Velocity_persecond[i][j]<2:
                          VP_Z1_Tag13.append(j)    
                      elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                          VP_Z2_Tag13.append(j) 
                      elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                          VP_Z3_Tag13.append(j) 
                      elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                          VP_Z4_Tag13.append(j) 
                      elif Velocity_persecond[i][j]>=8:
                          VP_Z5_Tag13.append(j) 
                  if i==13:
                      if Velocity_persecond[i][j]<2:
                          VP_Z1_Tag14.append(j)
                      elif Velocity_persecond[i][j]>=2 and Velocity_persecond[i][j]<4:
                          VP_Z2_Tag14.append(j)
                      elif Velocity_persecond[i][j]>=4 and Velocity_persecond[i][j]<6:
                          VP_Z3_Tag14.append(j)
                      elif Velocity_persecond[i][j]>=6 and Velocity_persecond[i][j]<8:
                          VP_Z4_Tag14.append(j)
                      elif Velocity_persecond[i][j]>=8:
                          VP_Z5_Tag14.append(j)
                

         ########################################## VP zone durations ################################################################
# Zone 1         
         while self.completed <51:
            self.completed += 1
         self.progressBar.setValue (self.completed)
         self.progressBar.setValue (self.half)
         
         Z1_VPtag1_mins=[];Z1_VPtag2_mins=[];Z1_VPtag3_mins=[];Z1_VPtag4_mins=[];Z1_VPtag5_mins=[];Z1_VPtag6_mins=[];Z1_VPtag7_mins=[];
         Z1_VPtag8_mins=[];Z1_VPtag9_mins=[];Z1_VPtag10_mins=[];Z1_VPtag11_mins=[];Z1_VPtag12_mins=[];Z1_VPtag13_mins=[];Z1_VPtag14_mins=[]


         # minute 1              
         Z1_VPtag1_min1=sum(i <60 for i in VP_Z1_Tag1);Z1_VPtag2_min1=sum(i <60 for i in VP_Z1_Tag2);Z1_VPtag3_min1=sum(i <60 for i in VP_Z1_Tag3);
         Z1_VPtag4_min1=sum(i <60 for i in VP_Z1_Tag4);Z1_VPtag5_min1=sum(i <60 for i in VP_Z1_Tag5);Z1_VPtag6_min1=sum(i <60 for i in VP_Z1_Tag6);
         Z1_VPtag7_min1=sum(i <60 for i in VP_Z1_Tag7);Z1_VPtag8_min1=sum(i <60 for i in VP_Z1_Tag8);Z1_VPtag9_min1=sum(i <60 for i in VP_Z1_Tag9);
         Z1_VPtag10_min1=sum(i <60 for i in VP_Z1_Tag10);Z1_VPtag11_min1=sum(i <60 for i in VP_Z1_Tag11);Z1_VPtag12_min1=sum(i <60 for i in VP_Z1_Tag12);
         Z1_VPtag13_min1=sum(i <60 for i in VP_Z1_Tag13);Z1_VPtag14_min1=sum(i <60 for i in VP_Z1_Tag14);
         
         # minute 2
         Z1_VPtag1_min2=sum((i >=60) and (i <120) for i in VP_Z1_Tag1);Z1_VPtag2_min2=sum((i >=60) and (i <120) for i in VP_Z1_Tag2);
         Z1_VPtag3_min2=sum((i >=60) and (i <120) for i in VP_Z1_Tag3);Z1_VPtag4_min2=sum((i >=60) and (i <120) for i in VP_Z1_Tag4);
         Z1_VPtag5_min2=sum((i >=60) and (i <120) for i in VP_Z1_Tag5);Z1_VPtag6_min2=sum((i >=60) and (i <120) for i in VP_Z1_Tag6);
         Z1_VPtag7_min2=sum((i >=60) and (i <120) for i in VP_Z1_Tag7);Z1_VPtag8_min2=sum((i >=60) and (i <120) for i in VP_Z1_Tag8);
         Z1_VPtag9_min2=sum((i >=60) and (i <120) for i in VP_Z1_Tag9);Z1_VPtag10_min2=sum((i >=60) and (i <120) for i in VP_Z1_Tag10);
         Z1_VPtag11_min2=sum((i >=60) and (i <120) for i in VP_Z1_Tag11);Z1_VPtag12_min2=sum((i >=60) and (i <120) for i in VP_Z1_Tag12);
         Z1_VPtag13_min2=sum((i >=60) and (i <120) for i in VP_Z1_Tag13);Z1_VPtag14_min2=sum((i >=60) and (i <120) for i in VP_Z1_Tag14)

         # minute 3
         Z1_VPtag1_min3=sum((i>=120) and (i<180) for i in VP_Z1_Tag1);Z1_VPtag2_min3=sum((i>=120) and (i<180) for i in VP_Z1_Tag2);
         Z1_VPtag3_min3=sum((i>=120) and (i<180) for i in VP_Z1_Tag3);Z1_VPtag4_min3=sum((i>=120) and (i<180) for i in VP_Z1_Tag4);
         Z1_VPtag5_min3=sum((i>=120) and (i<180) for i in VP_Z1_Tag5);Z1_VPtag6_min3=sum((i>=120) and (i<180) for i in VP_Z1_Tag6);
         Z1_VPtag7_min3=sum((i>=120) and (i<180) for i in VP_Z1_Tag7);Z1_VPtag8_min3=sum((i>=120) and (i<180) for i in VP_Z1_Tag8);
         Z1_VPtag9_min3=sum((i>=120) and (i<180) for i in VP_Z1_Tag9);Z1_VPtag10_min3=sum((i>=120) and (i<180) for i in VP_Z1_Tag10);
         Z1_VPtag11_min3=sum((i>=120) and (i<180) for i in VP_Z1_Tag11);Z1_VPtag12_min3=sum((i>=120) and (i<180) for i in VP_Z1_Tag12);
         Z1_VPtag13_min3=sum((i>=120) and (i<180) for i in VP_Z1_Tag13);Z1_VPtag14_min3=sum((i>=120) and (i<180) for i in VP_Z1_Tag14)
         
         # minute 4
         Z1_VPtag1_min4=sum((i>=180) and (i<240) for i in VP_Z1_Tag1);Z1_VPtag2_min4=sum((i>=180) and (i<240) for i in VP_Z1_Tag2);
         Z1_VPtag3_min4=sum((i>=180) and (i<240) for i in VP_Z1_Tag3);Z1_VPtag4_min4=sum((i>=180) and (i<240) for i in VP_Z1_Tag4);
         Z1_VPtag5_min4=sum((i>=180) and (i<240) for i in VP_Z1_Tag5);Z1_VPtag6_min4=sum((i>=180) and (i<240) for i in VP_Z1_Tag6);
         Z1_VPtag7_min4=sum((i>=180) and (i<240) for i in VP_Z1_Tag7);Z1_VPtag8_min4=sum((i>=180) and (i<240) for i in VP_Z1_Tag8);
         Z1_VPtag9_min4=sum((i>=180) and (i<240) for i in VP_Z1_Tag9);Z1_VPtag10_min4=sum((i>=180) and (i<240) for i in VP_Z1_Tag10);
         Z1_VPtag11_min4=sum((i>=180) and (i<240) for i in VP_Z1_Tag11);Z1_VPtag12_min4=sum((i>=180) and (i<240) for i in VP_Z1_Tag12);
         Z1_VPtag13_min4=sum((i>=180) and (i<240) for i in VP_Z1_Tag13);Z1_VPtag14_min4=sum((i>=180) and (i<240) for i in VP_Z1_Tag14)
         
         # minute 5
         Z1_VPtag1_min5=sum((i>=240) and (i<300) for i in VP_Z1_Tag1);Z1_VPtag2_min5=sum((i>=240) and (i<300) for i in VP_Z1_Tag2);
         Z1_VPtag3_min5=sum((i>=240) and (i<300) for i in VP_Z1_Tag3);Z1_VPtag4_min5=sum((i>=240) and (i<300) for i in VP_Z1_Tag4);
         Z1_VPtag5_min5=sum((i>=240) and (i<300) for i in VP_Z1_Tag5);Z1_VPtag6_min5=sum((i>=240) and (i<300) for i in VP_Z1_Tag6);
         Z1_VPtag7_min5=sum((i>=240) and (i<300) for i in VP_Z1_Tag7);Z1_VPtag8_min5=sum((i>=240) and (i<300) for i in VP_Z1_Tag8);
         Z1_VPtag9_min5=sum((i>=240) and (i<300) for i in VP_Z1_Tag9);Z1_VPtag10_min5=sum((i>=240) and (i<300) for i in VP_Z1_Tag10);
         Z1_VPtag11_min5=sum((i>=240) and (i<300) for i in VP_Z1_Tag11);Z1_VPtag12_min5=sum((i>=240) and (i<300) for i in VP_Z1_Tag12);
         Z1_VPtag13_min5=sum((i>=240) and (i<300) for i in VP_Z1_Tag13);Z1_VPtag14_min5=sum((i>=240) and (i<300) for i in VP_Z1_Tag14)
         
         # minute 6
         Z1_VPtag1_min6=sum((i>=300) and (i<360) for i in VP_Z1_Tag1);Z1_VPtag2_min6=sum((i>=300) and (i<360) for i in VP_Z1_Tag2);
         Z1_VPtag3_min6=sum((i>=300) and (i<360) for i in VP_Z1_Tag3);Z1_VPtag4_min6=sum((i>=300) and (i<360) for i in VP_Z1_Tag4);
         Z1_VPtag5_min6=sum((i>=300) and (i<360) for i in VP_Z1_Tag5);Z1_VPtag6_min6=sum((i>=300) and (i<360) for i in VP_Z1_Tag6);
         Z1_VPtag7_min6=sum((i>=300) and (i<360) for i in VP_Z1_Tag7);Z1_VPtag8_min6=sum((i>=300) and (i<360) for i in VP_Z1_Tag8);
         Z1_VPtag9_min6=sum((i>=300) and (i<360) for i in VP_Z1_Tag9);Z1_VPtag10_min6=sum((i>=300) and (i<360)for i in VP_Z1_Tag10);
         Z1_VPtag11_min6=sum((i>=300) and (i<360) for i in VP_Z1_Tag11);Z1_VPtag12_min6=sum((i>=300) and (i<360) for i in VP_Z1_Tag12);
         Z1_VPtag13_min6=sum((i>=300) and (i<360) for i in VP_Z1_Tag13);Z1_VPtag14_min6=sum((i>=300) and (i<360) for i in VP_Z1_Tag14)
         
         # minute 7
         Z1_VPtag1_min7=sum((i>=360) and (i<420) for i in VP_Z1_Tag1);Z1_VPtag2_min7=sum((i>=360) and (i<420) for i in VP_Z1_Tag2);
         Z1_VPtag3_min7=sum((i>=360) and (i<420) for i in VP_Z1_Tag3);Z1_VPtag4_min7=sum((i>=360) and (i<420) for i in VP_Z1_Tag4);
         Z1_VPtag5_min7=sum((i>=360) and (i<420) for i in VP_Z1_Tag5);Z1_VPtag6_min7=sum((i>=360) and (i<420) for i in VP_Z1_Tag6);
         Z1_VPtag7_min7=sum((i>=360) and (i<420) for i in VP_Z1_Tag7);Z1_VPtag8_min7=sum((i>=360) and (i<420) for i in VP_Z1_Tag8);
         Z1_VPtag9_min7=sum((i>=360) and (i<420) for i in VP_Z1_Tag9);Z1_VPtag10_min7=sum((i>=360) and (i<420)for i in VP_Z1_Tag10);
         Z1_VPtag11_min7=sum((i>=360) and (i<420) for i in VP_Z1_Tag11);Z1_VPtag12_min7=sum((i>=360) and (i<420) for i in VP_Z1_Tag12);
         Z1_VPtag13_min7=sum((i>=360) and (i<420) for i in VP_Z1_Tag13);Z1_VPtag14_min7=sum((i>=360) and (i<420) for i in VP_Z1_Tag14)
         
         # minute 8
         Z1_VPtag1_min8=sum((i>=420) and (i<480) for i in VP_Z1_Tag1);Z1_VPtag2_min8=sum((i>=420) and (i<480) for i in VP_Z1_Tag2);
         Z1_VPtag3_min8=sum((i>=420) and (i<480) for i in VP_Z1_Tag3);Z1_VPtag4_min8=sum((i>=420) and (i<480) for i in VP_Z1_Tag4);
         Z1_VPtag5_min8=sum((i>=420) and (i<480) for i in VP_Z1_Tag5);Z1_VPtag6_min8=sum((i>=420) and (i<480) for i in VP_Z1_Tag6);
         Z1_VPtag7_min8=sum((i>=420) and (i<480) for i in VP_Z1_Tag7);Z1_VPtag8_min8=sum((i>=420) and (i<480)for i in VP_Z1_Tag8);
         Z1_VPtag9_min8=sum((i>=420) and (i<480) for i in VP_Z1_Tag9);Z1_VPtag10_min8=sum((i>=420) and (i<480)for i in VP_Z1_Tag10);
         Z1_VPtag11_min8=sum((i>=420) and (i<480) for i in VP_Z1_Tag11);Z1_VPtag12_min8=sum((i>=420) and (i<480) for i in VP_Z1_Tag12);
         Z1_VPtag13_min8=sum((i>=420) and (i<480) for i in VP_Z1_Tag13);Z1_VPtag14_min8=sum((i>=420) and (i<480) for i in VP_Z1_Tag14)
         
         # minute 9
         Z1_VPtag1_min9=sum((i>=480) and (i<540) for i in VP_Z1_Tag1);Z1_VPtag2_min9=sum((i>=480) and (i<540) for i in VP_Z1_Tag2);
         Z1_VPtag3_min9=sum((i>=480) and (i<540) for i in VP_Z1_Tag3);Z1_VPtag4_min9=sum((i>=480) and (i<540) for i in VP_Z1_Tag4);
         Z1_VPtag5_min9=sum((i>=480) and (i<540) for i in VP_Z1_Tag5);Z1_VPtag6_min9=sum((i>=480) and (i<540) for i in VP_Z1_Tag6);
         Z1_VPtag7_min9=sum((i>=480) and (i<540) for i in VP_Z1_Tag7);Z1_VPtag8_min9=sum((i>=480) and (i<540) for i in VP_Z1_Tag8);
         Z1_VPtag9_min9=sum((i>=480) and (i<540) for i in VP_Z1_Tag9);Z1_VPtag10_min9=sum((i>=480) and (i<540) for i in VP_Z1_Tag10);
         Z1_VPtag11_min9=sum((i>=480) and (i<540) for i in VP_Z1_Tag11);Z1_VPtag12_min9=sum((i>=480) and (i<540) for i in VP_Z1_Tag12);
         Z1_VPtag13_min9=sum((i>=480) and (i<540) for i in VP_Z1_Tag13);Z1_VPtag14_min9=sum((i>=480) and (i<540) for i in VP_Z1_Tag14)        

         # minute 10
         Z1_VPtag1_min10=sum((i>=540) and (i<600) for i in VP_Z1_Tag1);Z1_VPtag2_min10=sum((i>=540) and (i<600) for i in VP_Z1_Tag2);
         Z1_VPtag3_min10=sum((i>=540) and (i<600) for i in VP_Z1_Tag3);Z1_VPtag4_min10=sum((i>=540) and (i<600) for i in VP_Z1_Tag4);
         Z1_VPtag5_min10=sum((i>=540) and (i<600) for i in VP_Z1_Tag5);Z1_VPtag6_min10=sum((i>=540) and (i<600) for i in VP_Z1_Tag6);
         Z1_VPtag7_min10=sum((i>=540) and (i<600) for i in VP_Z1_Tag7);Z1_VPtag8_min10=sum((i>=540) and (i<600) for i in VP_Z1_Tag8);
         Z1_VPtag9_min10=sum((i>=540) and (i<600) for i in VP_Z1_Tag9);Z1_VPtag10_min10=sum((i>=540) and (i<600) for i in VP_Z1_Tag10);
         Z1_VPtag11_min10=sum((i>=540) and (i<600) for i in VP_Z1_Tag11);Z1_VPtag12_min10=sum((i>=540) and (i<600) for i in VP_Z1_Tag12);
         Z1_VPtag13_min10=sum((i>=540) and (i<600) for i in VP_Z1_Tag13);Z1_VPtag14_min10=sum((i>=540) and (i<600) for i in VP_Z1_Tag14)
         
         # minute 11
         Z1_VPtag1_min11=sum((i>=600) and (i<660) for i in VP_Z1_Tag1);Z1_VPtag2_min11=sum((i>=600) and (i<660) for i in VP_Z1_Tag2);
         Z1_VPtag3_min11=sum((i>=600) and (i<660) for i in VP_Z1_Tag3);Z1_VPtag4_min11=sum((i>=600) and (i<660) for i in VP_Z1_Tag4);
         Z1_VPtag5_min11=sum((i>=600) and (i<660) for i in VP_Z1_Tag5);Z1_VPtag6_min11=sum((i>=600) and (i<660) for i in VP_Z1_Tag6);
         Z1_VPtag7_min11=sum((i>=600) and (i<660) for i in VP_Z1_Tag7);Z1_VPtag8_min11=sum((i>=600) and (i<660) for i in VP_Z1_Tag8);
         Z1_VPtag9_min11=sum((i>=600) and (i<660) for i in VP_Z1_Tag9);Z1_VPtag10_min11=sum((i>=600) and (i<660) for i in VP_Z1_Tag10);
         Z1_VPtag11_min11=sum((i>=600) and (i<660) for i in VP_Z1_Tag11);Z1_VPtag12_min11=sum((i>=600) and (i<660) for i in VP_Z1_Tag12);
         Z1_VPtag13_min11=sum((i>=600) and (i<660) for i in VP_Z1_Tag13);Z1_VPtag14_min11=sum((i>=600) and (i<660) for i in VP_Z1_Tag14)
         
         # minute 12
         Z1_VPtag1_min12=sum((i>=660) and (i<720) for i in VP_Z1_Tag1);Z1_VPtag2_min12=sum((i>=660) and (i<720) for i in VP_Z1_Tag2);
         Z1_VPtag3_min12=sum((i>=660) and (i<720) for i in VP_Z1_Tag3);Z1_VPtag4_min12=sum((i>=660) and (i<720) for i in VP_Z1_Tag4);
         Z1_VPtag5_min12=sum((i>=660) and (i<720) for i in VP_Z1_Tag5);Z1_VPtag6_min12=sum((i>=660) and (i<720) for i in VP_Z1_Tag6);
         Z1_VPtag7_min12=sum((i>=660) and (i<720) for i in VP_Z1_Tag7);Z1_VPtag8_min12=sum((i>=660) and (i<720) for i in VP_Z1_Tag8);
         Z1_VPtag9_min12=sum((i>=660) and (i<720) for i in VP_Z1_Tag9);Z1_VPtag10_min12=sum((i>=660) and (i<720) for i in VP_Z1_Tag10);
         Z1_VPtag11_min12=sum((i>=660) and (i<720) for i in VP_Z1_Tag11);Z1_VPtag12_min12=sum((i>=660) and (i<720) for i in VP_Z1_Tag12);
         Z1_VPtag13_min12=sum((i>=660) and (i<720) for i in VP_Z1_Tag13);Z1_VPtag14_min12=sum((i>=660) and (i<720) for i in VP_Z1_Tag14)
         
         # minute 13
         Z1_VPtag1_min13=sum((i>=720) and (i<780) for i in VP_Z1_Tag1);Z1_VPtag2_min13=sum((i>=720) and (i<780)for i in VP_Z1_Tag2);
         Z1_VPtag3_min13=sum((i>=720) and (i<780) for i in VP_Z1_Tag3);Z1_VPtag4_min13=sum((i>=720) and (i<780) for i in VP_Z1_Tag4);
         Z1_VPtag5_min13=sum((i>=720) and (i<780) for i in VP_Z1_Tag5);Z1_VPtag6_min13=sum((i>=720) and (i<780) for i in VP_Z1_Tag6);
         Z1_VPtag7_min13=sum((i>=720) and (i<780) for i in VP_Z1_Tag7);Z1_VPtag8_min13=sum((i>=720) and (i<780) for i in VP_Z1_Tag8);
         Z1_VPtag9_min13=sum((i>=720) and (i<780) for i in VP_Z1_Tag9);Z1_VPtag10_min13=sum((i>=720) and (i<780) for i in VP_Z1_Tag10);
         Z1_VPtag11_min13=sum((i>=720) and (i<780) for i in VP_Z1_Tag11);Z1_VPtag12_min13=sum((i>=720) and (i<780) for i in VP_Z1_Tag12);
         Z1_VPtag13_min13=sum((i>=720) and (i<780) for i in VP_Z1_Tag13);Z1_VPtag14_min13=sum((i>=720) and (i<780) for i in VP_Z1_Tag14)
         
         # minute 14
         Z1_VPtag1_min14=sum((i>=780) and (i<840) for i in VP_Z1_Tag1);Z1_VPtag2_min14=sum((i>=780) and (i<840) for i in VP_Z1_Tag2);
         Z1_VPtag3_min14=sum((i>=780) and (i<840) for i in VP_Z1_Tag3);Z1_VPtag4_min14=sum((i>=780) and (i<840) for i in VP_Z1_Tag4);
         Z1_VPtag5_min14=sum((i>=780) and (i<840) for i in VP_Z1_Tag5);Z1_VPtag6_min14=sum((i>=780) and (i<840) for i in VP_Z1_Tag6);
         Z1_VPtag7_min14=sum((i>=780) and (i<840) for i in VP_Z1_Tag7);Z1_VPtag8_min14=sum((i>=780) and (i<840) for i in VP_Z1_Tag8);
         Z1_VPtag9_min14=sum((i>=780) and (i<840) for i in VP_Z1_Tag9);Z1_VPtag10_min14=sum((i>=780) and (i<840) for i in VP_Z1_Tag10);
         Z1_VPtag11_min14=sum((i>=780) and (i<840)for i in VP_Z1_Tag11);Z1_VPtag12_min14=sum((i>=780) and (i<840) for i in VP_Z1_Tag12);
         Z1_VPtag13_min14=sum((i>=780) and (i<840) for i in VP_Z1_Tag13);Z1_VPtag14_min14=sum((i>=780) and (i<840) for i in VP_Z1_Tag14)
         
         # minute 15
         Z1_VPtag1_min15=sum((i>=840) and (i<=900) for i in VP_Z1_Tag1);Z1_VPtag2_min15=sum((i>=840) and (i<=900) for i in VP_Z1_Tag2);
         Z1_VPtag3_min15=sum((i>=840) and (i<=900) for i in VP_Z1_Tag3);Z1_VPtag4_min15=sum((i>=840) and (i<=900) for i in VP_Z1_Tag4);
         Z1_VPtag5_min15=sum((i>=840) and (i<=900) for i in VP_Z1_Tag5);Z1_VPtag6_min15=sum((i>=840) and (i<=900) for i in VP_Z1_Tag6);
         Z1_VPtag7_min15=sum((i>=840) and (i<=900) for i in VP_Z1_Tag7);Z1_VPtag8_min15=sum((i>=840) and (i<=900) for i in VP_Z1_Tag8);
         Z1_VPtag9_min15=sum((i>=840) and (i<=900) for i in VP_Z1_Tag9);Z1_VPtag10_min15=sum((i>=840) and (i<=900) for i in VP_Z1_Tag10);
         Z1_VPtag11_min15=sum((i>=840) and (i<=900) for i in VP_Z1_Tag11);Z1_VPtag12_min15=sum((i>=840) and (i<=900) for i in VP_Z1_Tag12);
         Z1_VPtag13_min15=sum((i>=840) and (i<=900) for i in VP_Z1_Tag13);Z1_VPtag14_min15=sum((i>=840) and (i<=900) for i in VP_Z1_Tag14)
##############################################################################################################################
# Zone 2

         Z2_VPtag1_mins=[];Z2_VPtag2_mins=[];Z2_VPtag3_mins=[];Z2_VPtag4_mins=[];Z2_VPtag5_mins=[];Z2_VPtag6_mins=[];Z2_VPtag7_mins=[];
         Z2_VPtag8_mins=[];Z2_VPtag9_mins=[];Z2_VPtag10_mins=[];Z2_VPtag11_mins=[];Z2_VPtag12_mins=[];Z2_VPtag13_mins=[];Z2_VPtag14_mins=[]
         # minute 1              
         Z2_VPtag1_min1=sum(i <60 for i in VP_Z2_Tag1);Z2_VPtag2_min1=sum(i <60 for i in VP_Z2_Tag2);Z2_VPtag3_min1=sum(i <60 for i in VP_Z2_Tag3);
         Z2_VPtag4_min1=sum(i <60 for i in VP_Z2_Tag4);Z2_VPtag5_min1=sum(i <60 for i in VP_Z2_Tag5);Z2_VPtag6_min1=sum(i <60 for i in VP_Z2_Tag6);
         Z2_VPtag7_min1=sum(i <60 for i in VP_Z2_Tag7);Z2_VPtag8_min1=sum(i <60 for i in VP_Z2_Tag8);Z2_VPtag9_min1=sum(i <60 for i in VP_Z2_Tag9);
         Z2_VPtag10_min1=sum(i <60 for i in VP_Z2_Tag10);Z2_VPtag11_min1=sum(i <60 for i in VP_Z2_Tag11);Z2_VPtag12_min1=sum(i <60 for i in VP_Z2_Tag12);
         Z2_VPtag13_min1=sum(i <60 for i in VP_Z2_Tag13);Z2_VPtag14_min1=sum(i <60 for i in VP_Z2_Tag14)

         # minute 2
         Z2_VPtag1_min2=sum((i >=60) and (i <120) for i in VP_Z2_Tag1);Z2_VPtag2_min2=sum((i >=60) and (i <120) for i in VP_Z2_Tag2);
         Z2_VPtag3_min2=sum((i >=60) and (i <120) for i in VP_Z2_Tag3);Z2_VPtag4_min2=sum((i >=60) and (i <120) for i in VP_Z2_Tag4);
         Z2_VPtag5_min2=sum((i >=60) and (i <120) for i in VP_Z2_Tag5);Z2_VPtag6_min2=sum((i >=60) and (i <120) for i in VP_Z2_Tag6);
         Z2_VPtag7_min2=sum((i >=60) and (i <120) for i in VP_Z2_Tag7);Z2_VPtag8_min2=sum((i >=60) and (i <120) for i in VP_Z2_Tag8);
         Z2_VPtag9_min2=sum((i >=60) and (i <120) for i in VP_Z2_Tag9);Z2_VPtag10_min2=sum((i >=60) and (i <120) for i in VP_Z2_Tag10);
         Z2_VPtag11_min2=sum((i >=60) and (i <120) for i in VP_Z2_Tag11);Z2_VPtag12_min2=sum((i >=60) and (i <120) for i in VP_Z2_Tag12);
         Z2_VPtag13_min2=sum((i >=60) and (i <120) for i in VP_Z2_Tag13);Z2_VPtag14_min2=sum((i >=60) and (i <120) for i in VP_Z2_Tag14)

         # minute 3
         Z2_VPtag1_min3=sum((i>=120) and (i<180) for i in VP_Z2_Tag1);Z2_VPtag2_min3=sum((i>=120) and (i<180) for i in VP_Z2_Tag2);
         Z2_VPtag3_min3=sum((i>=120) and (i<180) for i in VP_Z2_Tag3);Z2_VPtag4_min3=sum((i>=120) and (i<180) for i in VP_Z2_Tag4);
         Z2_VPtag5_min3=sum((i>=120) and (i<180) for i in VP_Z2_Tag5);Z2_VPtag6_min3=sum((i>=120) and (i<180) for i in VP_Z2_Tag6);
         Z2_VPtag7_min3=sum((i>=120) and (i<180) for i in VP_Z2_Tag7);Z2_VPtag8_min3=sum((i>=120) and (i<180) for i in VP_Z2_Tag8);
         Z2_VPtag9_min3=sum((i>=120) and (i<180) for i in VP_Z2_Tag9);Z2_VPtag10_min3=sum((i>=120) and (i<180) for i in VP_Z2_Tag10);
         Z2_VPtag11_min3=sum((i>=120) and (i<180) for i in VP_Z2_Tag11);Z2_VPtag12_min3=sum((i>=120) and (i<180) for i in VP_Z2_Tag12);
         Z2_VPtag13_min3=sum((i>=120) and (i<180) for i in VP_Z2_Tag13);Z2_VPtag14_min3=sum((i>=120) and (i<180) for i in VP_Z2_Tag14)
         
         # minute 4
         Z2_VPtag1_min4=sum((i>=180) and (i<240) for i in VP_Z2_Tag1);Z2_VPtag2_min4=sum((i>=180) and (i<240) for i in VP_Z2_Tag2);
         Z2_VPtag3_min4=sum((i>=180) and (i<240) for i in VP_Z2_Tag3);Z2_VPtag4_min4=sum((i>=180) and (i<240) for i in VP_Z2_Tag4);
         Z2_VPtag5_min4=sum((i>=180) and (i<240) for i in VP_Z2_Tag5);Z2_VPtag6_min4=sum((i>=180) and (i<240) for i in VP_Z2_Tag6);
         Z2_VPtag7_min4=sum((i>=180) and (i<240) for i in VP_Z2_Tag7);Z2_VPtag8_min4=sum((i>=180) and (i<240) for i in VP_Z2_Tag8);
         Z2_VPtag9_min4=sum((i>=180) and (i<240) for i in VP_Z2_Tag9);Z2_VPtag10_min4=sum((i>=180) and (i<240) for i in VP_Z2_Tag10);
         Z2_VPtag11_min4=sum((i>=180) and (i<240) for i in VP_Z2_Tag11);Z2_VPtag12_min4=sum((i>=180) and (i<240) for i in VP_Z2_Tag12);
         Z2_VPtag13_min4=sum((i>=180) and (i<240) for i in VP_Z2_Tag13);Z2_VPtag14_min4=sum((i>=180) and (i<240) for i in VP_Z2_Tag14)
         
         # minute 5
         Z2_VPtag1_min5=sum((i>=240) and (i<300) for i in VP_Z2_Tag1);Z2_VPtag2_min5=sum((i>=240) and (i<300) for i in VP_Z2_Tag2);
         Z2_VPtag3_min5=sum((i>=240) and (i<300) for i in VP_Z2_Tag3);Z2_VPtag4_min5=sum((i>=240) and (i<300) for i in VP_Z2_Tag4);
         Z2_VPtag5_min5=sum((i>=240) and (i<300) for i in VP_Z2_Tag5);Z2_VPtag6_min5=sum((i>=240) and (i<300) for i in VP_Z2_Tag6);
         Z2_VPtag7_min5=sum((i>=240) and (i<300) for i in VP_Z2_Tag7);Z2_VPtag8_min5=sum((i>=240) and (i<300) for i in VP_Z2_Tag8);
         Z2_VPtag9_min5=sum((i>=240) and (i<300) for i in VP_Z2_Tag9);Z2_VPtag10_min5=sum((i>=240) and (i<300) for i in VP_Z2_Tag10);
         Z2_VPtag11_min5=sum((i>=240) and (i<300) for i in VP_Z2_Tag11);Z2_VPtag12_min5=sum((i>=240) and (i<300) for i in VP_Z2_Tag12);
         Z2_VPtag13_min5=sum((i>=240) and (i<300) for i in VP_Z2_Tag13);Z2_VPtag14_min5=sum((i>=240) and (i<300) for i in VP_Z2_Tag14)
         
         # minute 6
         Z2_VPtag1_min6=sum((i>=300) and (i<360) for i in VP_Z2_Tag1);Z2_VPtag2_min6=sum((i>=300) and (i<360) for i in VP_Z2_Tag2);
         Z2_VPtag3_min6=sum((i>=300) and (i<360) for i in VP_Z2_Tag3);Z2_VPtag4_min6=sum((i>=300) and (i<360) for i in VP_Z2_Tag4);
         Z2_VPtag5_min6=sum((i>=300) and (i<360) for i in VP_Z2_Tag5);Z2_VPtag6_min6=sum((i>=300) and (i<360) for i in VP_Z2_Tag6);
         Z2_VPtag7_min6=sum((i>=300) and (i<360) for i in VP_Z2_Tag7);Z2_VPtag8_min6=sum((i>=300) and (i<360) for i in VP_Z2_Tag8);
         Z2_VPtag9_min6=sum((i>=300) and (i<360) for i in VP_Z2_Tag9);Z2_VPtag10_min6=sum((i>=300) and (i<360)for i in VP_Z2_Tag10);
         Z2_VPtag11_min6=sum((i>=300) and (i<360) for i in VP_Z2_Tag11);Z2_VPtag12_min6=sum((i>=300) and (i<360) for i in VP_Z2_Tag12);
         Z2_VPtag13_min6=sum((i>=300) and (i<360) for i in VP_Z2_Tag13);Z2_VPtag14_min6=sum((i>=300) and (i<360) for i in VP_Z2_Tag14)
         
         # minute 7
         Z2_VPtag1_min7=sum((i>=360) and (i<420) for i in VP_Z2_Tag1);Z2_VPtag2_min7=sum((i>=360) and (i<420) for i in VP_Z2_Tag2);
         Z2_VPtag3_min7=sum((i>=360) and (i<420) for i in VP_Z2_Tag3);Z2_VPtag4_min7=sum((i>=360) and (i<420) for i in VP_Z2_Tag4);
         Z2_VPtag5_min7=sum((i>=360) and (i<420) for i in VP_Z2_Tag5);Z2_VPtag6_min7=sum((i>=360) and (i<420) for i in VP_Z2_Tag6);
         Z2_VPtag7_min7=sum((i>=360) and (i<420) for i in VP_Z2_Tag7);Z2_VPtag8_min7=sum((i>=360) and (i<420) for i in VP_Z2_Tag8);
         Z2_VPtag9_min7=sum((i>=360) and (i<420) for i in VP_Z2_Tag9);Z2_VPtag10_min7=sum((i>=360) and (i<420)for i in VP_Z2_Tag10);
         Z2_VPtag11_min7=sum((i>=360) and (i<420) for i in VP_Z2_Tag11);Z2_VPtag12_min7=sum((i>=360) and (i<420) for i in VP_Z2_Tag12);
         Z2_VPtag13_min7=sum((i>=360) and (i<420) for i in VP_Z2_Tag13);Z2_VPtag14_min7=sum((i>=360) and (i<420) for i in VP_Z2_Tag14)
         
         # minute 8
         Z2_VPtag1_min8=sum((i>=420) and (i<480) for i in VP_Z2_Tag1);Z2_VPtag2_min8=sum((i>=420) and (i<480) for i in VP_Z2_Tag2);
         Z2_VPtag3_min8=sum((i>=420) and (i<480) for i in VP_Z2_Tag3);Z2_VPtag4_min8=sum((i>=420) and (i<480) for i in VP_Z2_Tag4);
         Z2_VPtag5_min8=sum((i>=420) and (i<480) for i in VP_Z2_Tag5);Z2_VPtag6_min8=sum((i>=420) and (i<480) for i in VP_Z2_Tag6);
         Z2_VPtag7_min8=sum((i>=420) and (i<480) for i in VP_Z2_Tag7);Z2_VPtag8_min8=sum((i>=420) and (i<480)for i in VP_Z2_Tag8);
         Z2_VPtag9_min8=sum((i>=420) and (i<480) for i in VP_Z2_Tag9);Z2_VPtag10_min8=sum((i>=420) and (i<480)for i in VP_Z2_Tag10);
         Z2_VPtag11_min8=sum((i>=420) and (i<480) for i in VP_Z2_Tag11);Z2_VPtag12_min8=sum((i>=420) and (i<480) for i in VP_Z2_Tag12);
         Z2_VPtag13_min8=sum((i>=420) and (i<480) for i in VP_Z2_Tag13);Z2_VPtag14_min8=sum((i>=420) and (i<480) for i in VP_Z2_Tag14)
         
         # minute 9
         Z2_VPtag1_min9=sum((i>=480) and (i<540) for i in VP_Z2_Tag1);Z2_VPtag2_min9=sum((i>=480) and (i<540) for i in VP_Z2_Tag2);
         Z2_VPtag3_min9=sum((i>=480) and (i<540) for i in VP_Z2_Tag3);Z2_VPtag4_min9=sum((i>=480) and (i<540) for i in VP_Z2_Tag4);
         Z2_VPtag5_min9=sum((i>=480) and (i<540) for i in VP_Z2_Tag5);Z2_VPtag6_min9=sum((i>=480) and (i<540) for i in VP_Z2_Tag6);
         Z2_VPtag7_min9=sum((i>=480) and (i<540) for i in VP_Z2_Tag7);Z2_VPtag8_min9=sum((i>=480) and (i<540) for i in VP_Z2_Tag8);
         Z2_VPtag9_min9=sum((i>=480) and (i<540) for i in VP_Z2_Tag9);Z2_VPtag10_min9=sum((i>=480) and (i<540) for i in VP_Z2_Tag10);
         Z2_VPtag11_min9=sum((i>=480) and (i<540) for i in VP_Z2_Tag11);Z2_VPtag12_min9=sum((i>=480) and (i<540) for i in VP_Z2_Tag12);
         Z2_VPtag13_min9=sum((i>=480) and (i<540) for i in VP_Z2_Tag13);Z2_VPtag14_min9=sum((i>=480) and (i<540) for i in VP_Z2_Tag14)        

         # minute 10
         Z2_VPtag1_min10=sum((i>=540) and (i<600) for i in VP_Z2_Tag1);Z2_VPtag2_min10=sum((i>=540) and (i<600) for i in VP_Z2_Tag2);
         Z2_VPtag3_min10=sum((i>=540) and (i<600) for i in VP_Z2_Tag3);Z2_VPtag4_min10=sum((i>=540) and (i<600) for i in VP_Z2_Tag4);
         Z2_VPtag5_min10=sum((i>=540) and (i<600) for i in VP_Z2_Tag5);Z2_VPtag6_min10=sum((i>=540) and (i<600) for i in VP_Z2_Tag6);
         Z2_VPtag7_min10=sum((i>=540) and (i<600) for i in VP_Z2_Tag7);Z2_VPtag8_min10=sum((i>=540) and (i<600) for i in VP_Z2_Tag8);
         Z2_VPtag9_min10=sum((i>=540) and (i<600) for i in VP_Z2_Tag9);Z2_VPtag10_min10=sum((i>=540) and (i<600) for i in VP_Z2_Tag10);
         Z2_VPtag11_min10=sum((i>=540) and (i<600) for i in VP_Z2_Tag11);Z2_VPtag12_min10=sum((i>=540) and (i<600) for i in VP_Z2_Tag12);
         Z2_VPtag13_min10=sum((i>=540) and (i<600) for i in VP_Z2_Tag13);Z2_VPtag14_min10=sum((i>=540) and (i<600) for i in VP_Z2_Tag14)
         
         # minute 11
         Z2_VPtag1_min11=sum((i>=600) and (i<660) for i in VP_Z2_Tag1);Z2_VPtag2_min11=sum((i>=600) and (i<660) for i in VP_Z2_Tag2);
         Z2_VPtag3_min11=sum((i>=600) and (i<660) for i in VP_Z2_Tag3);Z2_VPtag4_min11=sum((i>=600) and (i<660) for i in VP_Z2_Tag4);
         Z2_VPtag5_min11=sum((i>=600) and (i<660) for i in VP_Z2_Tag5);Z2_VPtag6_min11=sum((i>=600) and (i<660) for i in VP_Z2_Tag6);
         Z2_VPtag7_min11=sum((i>=600) and (i<660) for i in VP_Z2_Tag7);Z2_VPtag8_min11=sum((i>=600) and (i<660) for i in VP_Z2_Tag8);
         Z2_VPtag9_min11=sum((i>=600) and (i<660) for i in VP_Z2_Tag9);Z2_VPtag10_min11=sum((i>=600) and (i<660) for i in VP_Z2_Tag10);
         Z2_VPtag11_min11=sum((i>=600) and (i<660) for i in VP_Z2_Tag11);Z2_VPtag12_min11=sum((i>=600) and (i<660) for i in VP_Z2_Tag12);
         Z2_VPtag13_min11=sum((i>=600) and (i<660) for i in VP_Z2_Tag13);Z2_VPtag14_min11=sum((i>=600) and (i<660) for i in VP_Z2_Tag14)
         
         # minute 12
         Z2_VPtag1_min12=sum((i>=660) and (i<720) for i in VP_Z2_Tag1);Z2_VPtag2_min12=sum((i>=660) and (i<720) for i in VP_Z2_Tag2);
         Z2_VPtag3_min12=sum((i>=660) and (i<720) for i in VP_Z2_Tag3);Z2_VPtag4_min12=sum((i>=660) and (i<720) for i in VP_Z2_Tag4);
         Z2_VPtag5_min12=sum((i>=660) and (i<720) for i in VP_Z2_Tag5);Z2_VPtag6_min12=sum((i>=660) and (i<720) for i in VP_Z2_Tag6);
         Z2_VPtag7_min12=sum((i>=660) and (i<720) for i in VP_Z2_Tag7);Z2_VPtag8_min12=sum((i>=660) and (i<720) for i in VP_Z2_Tag8);
         Z2_VPtag9_min12=sum((i>=660) and (i<720) for i in VP_Z2_Tag9);Z2_VPtag10_min12=sum((i>=660) and (i<720) for i in VP_Z2_Tag10);
         Z2_VPtag11_min12=sum((i>=660) and (i<720) for i in VP_Z2_Tag11);Z2_VPtag12_min12=sum((i>=660) and (i<720) for i in VP_Z2_Tag12);
         Z2_VPtag13_min12=sum((i>=660) and (i<720) for i in VP_Z2_Tag13);Z2_VPtag14_min12=sum((i>=660) and (i<720) for i in VP_Z2_Tag14)
         
         # minute 13
         Z2_VPtag1_min13=sum((i>=720) and (i<780) for i in VP_Z2_Tag1);Z2_VPtag2_min13=sum((i>=720) and (i<780)for i in VP_Z2_Tag2);
         Z2_VPtag3_min13=sum((i>=720) and (i<780) for i in VP_Z2_Tag3);Z2_VPtag4_min13=sum((i>=720) and (i<780) for i in VP_Z2_Tag4);
         Z2_VPtag5_min13=sum((i>=720) and (i<780) for i in VP_Z2_Tag5);Z2_VPtag6_min13=sum((i>=720) and (i<780) for i in VP_Z2_Tag6);
         Z2_VPtag7_min13=sum((i>=720) and (i<780) for i in VP_Z2_Tag7);Z2_VPtag8_min13=sum((i>=720) and (i<780) for i in VP_Z2_Tag8);
         Z2_VPtag9_min13=sum((i>=720) and (i<780) for i in VP_Z2_Tag9);Z2_VPtag10_min13=sum((i>=720) and (i<780) for i in VP_Z2_Tag10);
         Z2_VPtag11_min13=sum((i>=720) and (i<780) for i in VP_Z2_Tag11);Z2_VPtag12_min13=sum((i>=720) and (i<780) for i in VP_Z2_Tag12);
         Z2_VPtag13_min13=sum((i>=720) and (i<780) for i in VP_Z2_Tag13);Z2_VPtag14_min13=sum((i>=720) and (i<780) for i in VP_Z2_Tag14)
         
         # minute 14
         Z2_VPtag1_min14=sum((i>=780) and (i<840) for i in VP_Z2_Tag1);Z2_VPtag2_min14=sum((i>=780) and (i<840) for i in VP_Z2_Tag2);
         Z2_VPtag3_min14=sum((i>=780) and (i<840) for i in VP_Z2_Tag3);Z2_VPtag4_min14=sum((i>=780) and (i<840) for i in VP_Z2_Tag4);
         Z2_VPtag5_min14=sum((i>=780) and (i<840) for i in VP_Z2_Tag5);Z2_VPtag6_min14=sum((i>=780) and (i<840) for i in VP_Z2_Tag6);
         Z2_VPtag7_min14=sum((i>=780) and (i<840) for i in VP_Z2_Tag7);Z2_VPtag8_min14=sum((i>=780) and (i<840) for i in VP_Z2_Tag8);
         Z2_VPtag9_min14=sum((i>=780) and (i<840) for i in VP_Z2_Tag9);Z2_VPtag10_min14=sum((i>=780) and (i<840) for i in VP_Z2_Tag10);
         Z2_VPtag11_min14=sum((i>=780) and (i<840)for i in VP_Z2_Tag11);Z2_VPtag12_min14=sum((i>=780) and (i<840) for i in VP_Z2_Tag12);
         Z2_VPtag13_min14=sum((i>=780) and (i<840) for i in VP_Z2_Tag13);Z2_VPtag14_min14=sum((i>=780) and (i<840) for i in VP_Z2_Tag14)
         
         # minute 15
         Z2_VPtag1_min15=sum((i>=840) and (i<=900) for i in VP_Z2_Tag1);Z2_VPtag2_min15=sum((i>=840) and (i<=900) for i in VP_Z2_Tag2);
         Z2_VPtag3_min15=sum((i>=840) and (i<=900) for i in VP_Z2_Tag3);Z2_VPtag4_min15=sum((i>=840) and (i<=900) for i in VP_Z2_Tag4);
         Z2_VPtag5_min15=sum((i>=840) and (i<=900) for i in VP_Z2_Tag5);Z2_VPtag6_min15=sum((i>=840) and (i<=900) for i in VP_Z2_Tag6);
         Z2_VPtag7_min15=sum((i>=840) and (i<=900) for i in VP_Z2_Tag7);Z2_VPtag8_min15=sum((i>=840) and (i<=900) for i in VP_Z2_Tag8);
         Z2_VPtag9_min15=sum((i>=840) and (i<=900) for i in VP_Z2_Tag9);Z2_VPtag10_min15=sum((i>=840) and (i<=900) for i in VP_Z2_Tag10);
         Z2_VPtag11_min15=sum((i>=840) and (i<=900) for i in VP_Z2_Tag11);Z2_VPtag12_min15=sum((i>=840) and (i<=900) for i in VP_Z2_Tag12);
         Z2_VPtag13_min15=sum((i>=840) and (i<=900) for i in VP_Z2_Tag13);Z2_VPtag14_min15=sum((i>=840) and (i<=900) for i in VP_Z2_Tag14)

##############################################################################################################################
# Zone 3

         Z3_VPtag1_mins=[];Z3_VPtag2_mins=[];Z3_VPtag3_mins=[];Z3_VPtag4_mins=[];Z3_VPtag5_mins=[];Z3_VPtag6_mins=[];Z3_VPtag7_mins=[];
         Z3_VPtag8_mins=[];Z3_VPtag9_mins=[];Z3_VPtag10_mins=[];Z3_VPtag11_mins=[];Z3_VPtag12_mins=[];Z3_VPtag13_mins=[];Z3_VPtag14_mins=[]
         # minute 1              
         Z3_VPtag1_min1=sum(i <60 for i in VP_Z3_Tag1);Z3_VPtag2_min1=sum(i <60 for i in VP_Z3_Tag2);Z3_VPtag3_min1=sum(i <60 for i in VP_Z3_Tag3);
         Z3_VPtag4_min1=sum(i <60 for i in VP_Z3_Tag4);Z3_VPtag5_min1=sum(i <60 for i in VP_Z3_Tag5);Z3_VPtag6_min1=sum(i <60 for i in VP_Z3_Tag6);
         Z3_VPtag7_min1=sum(i <60 for i in VP_Z3_Tag7);Z3_VPtag8_min1=sum(i <60 for i in VP_Z3_Tag8);Z3_VPtag9_min1=sum(i <60 for i in VP_Z3_Tag9);
         Z3_VPtag10_min1=sum(i <60 for i in VP_Z3_Tag10);Z3_VPtag11_min1=sum(i <60 for i in VP_Z3_Tag11);Z3_VPtag12_min1=sum(i <60 for i in VP_Z3_Tag12);
         Z3_VPtag13_min1=sum(i <60 for i in VP_Z3_Tag13);Z3_VPtag14_min1=sum(i <60 for i in VP_Z3_Tag14)

         # minute 2
         Z3_VPtag1_min2=sum((i >=60) and (i <120) for i in VP_Z3_Tag1);Z3_VPtag2_min2=sum((i >=60) and (i <120) for i in VP_Z3_Tag2);
         Z3_VPtag3_min2=sum((i >=60) and (i <120) for i in VP_Z3_Tag3);Z3_VPtag4_min2=sum((i >=60) and (i <120) for i in VP_Z3_Tag4);
         Z3_VPtag5_min2=sum((i >=60) and (i <120) for i in VP_Z3_Tag5);Z3_VPtag6_min2=sum((i >=60) and (i <120) for i in VP_Z3_Tag6);
         Z3_VPtag7_min2=sum((i >=60) and (i <120) for i in VP_Z3_Tag7);Z3_VPtag8_min2=sum((i >=60) and (i <120) for i in VP_Z3_Tag8);
         Z3_VPtag9_min2=sum((i >=60) and (i <120) for i in VP_Z3_Tag9);Z3_VPtag10_min2=sum((i >=60) and (i <120) for i in VP_Z3_Tag10);
         Z3_VPtag11_min2=sum((i >=60) and (i <120) for i in VP_Z3_Tag11);Z3_VPtag12_min2=sum((i >=60) and (i <120) for i in VP_Z3_Tag12);
         Z3_VPtag13_min2=sum((i >=60) and (i <120) for i in VP_Z3_Tag13);Z3_VPtag14_min2=sum((i >=60) and (i <120) for i in VP_Z3_Tag14)

         # minute 3
         Z3_VPtag1_min3=sum((i>=120) and (i<180) for i in VP_Z3_Tag1);Z3_VPtag2_min3=sum((i>=120) and (i<180) for i in VP_Z3_Tag2);
         Z3_VPtag3_min3=sum((i>=120) and (i<180) for i in VP_Z3_Tag3);Z3_VPtag4_min3=sum((i>=120) and (i<180) for i in VP_Z3_Tag4);
         Z3_VPtag5_min3=sum((i>=120) and (i<180) for i in VP_Z3_Tag5);Z3_VPtag6_min3=sum((i>=120) and (i<180) for i in VP_Z3_Tag6);
         Z3_VPtag7_min3=sum((i>=120) and (i<180) for i in VP_Z3_Tag7);Z3_VPtag8_min3=sum((i>=120) and (i<180) for i in VP_Z3_Tag8);
         Z3_VPtag9_min3=sum((i>=120) and (i<180) for i in VP_Z3_Tag9);Z3_VPtag10_min3=sum((i>=120) and (i<180) for i in VP_Z3_Tag10);
         Z3_VPtag11_min3=sum((i>=120) and (i<180) for i in VP_Z3_Tag11);Z3_VPtag12_min3=sum((i>=120) and (i<180) for i in VP_Z3_Tag12);
         Z3_VPtag13_min3=sum((i>=120) and (i<180) for i in VP_Z3_Tag13);Z3_VPtag14_min3=sum((i>=120) and (i<180) for i in VP_Z3_Tag14)
         
         # minute 4
         Z3_VPtag1_min4=sum((i>=180) and (i<240) for i in VP_Z3_Tag1);Z3_VPtag2_min4=sum((i>=180) and (i<240) for i in VP_Z3_Tag2);
         Z3_VPtag3_min4=sum((i>=180) and (i<240) for i in VP_Z3_Tag3);Z3_VPtag4_min4=sum((i>=180) and (i<240) for i in VP_Z3_Tag4);
         Z3_VPtag5_min4=sum((i>=180) and (i<240) for i in VP_Z3_Tag5);Z3_VPtag6_min4=sum((i>=180) and (i<240) for i in VP_Z3_Tag6);
         Z3_VPtag7_min4=sum((i>=180) and (i<240) for i in VP_Z3_Tag7);Z3_VPtag8_min4=sum((i>=180) and (i<240) for i in VP_Z3_Tag8);
         Z3_VPtag9_min4=sum((i>=180) and (i<240) for i in VP_Z3_Tag9);Z3_VPtag10_min4=sum((i>=180) and (i<240) for i in VP_Z3_Tag10);
         Z3_VPtag11_min4=sum((i>=180) and (i<240) for i in VP_Z3_Tag11);Z3_VPtag12_min4=sum((i>=180) and (i<240) for i in VP_Z3_Tag12);
         Z3_VPtag13_min4=sum((i>=180) and (i<240) for i in VP_Z3_Tag13);Z3_VPtag14_min4=sum((i>=180) and (i<240) for i in VP_Z3_Tag14)
         
         # minute 5
         Z3_VPtag1_min5=sum((i>=240) and (i<300) for i in VP_Z3_Tag1);Z3_VPtag2_min5=sum((i>=240) and (i<300) for i in VP_Z3_Tag2);
         Z3_VPtag3_min5=sum((i>=240) and (i<300) for i in VP_Z3_Tag3);Z3_VPtag4_min5=sum((i>=240) and (i<300) for i in VP_Z3_Tag4);
         Z3_VPtag5_min5=sum((i>=240) and (i<300) for i in VP_Z3_Tag5);Z3_VPtag6_min5=sum((i>=240) and (i<300) for i in VP_Z3_Tag6);
         Z3_VPtag7_min5=sum((i>=240) and (i<300) for i in VP_Z3_Tag7);Z3_VPtag8_min5=sum((i>=240) and (i<300) for i in VP_Z3_Tag8);
         Z3_VPtag9_min5=sum((i>=240) and (i<300) for i in VP_Z3_Tag9);Z3_VPtag10_min5=sum((i>=240) and (i<300) for i in VP_Z3_Tag10);
         Z3_VPtag11_min5=sum((i>=240) and (i<300) for i in VP_Z3_Tag11);Z3_VPtag12_min5=sum((i>=240) and (i<300) for i in VP_Z3_Tag12);
         Z3_VPtag13_min5=sum((i>=240) and (i<300) for i in VP_Z3_Tag13);Z3_VPtag14_min5=sum((i>=240) and (i<300) for i in VP_Z3_Tag14)
         
         # minute 6
         Z3_VPtag1_min6=sum((i>=300) and (i<360) for i in VP_Z3_Tag1);Z3_VPtag2_min6=sum((i>=300) and (i<360) for i in VP_Z3_Tag2);
         Z3_VPtag3_min6=sum((i>=300) and (i<360) for i in VP_Z3_Tag3);Z3_VPtag4_min6=sum((i>=300) and (i<360) for i in VP_Z3_Tag4);
         Z3_VPtag5_min6=sum((i>=300) and (i<360) for i in VP_Z3_Tag5);Z3_VPtag6_min6=sum((i>=300) and (i<360) for i in VP_Z3_Tag6);
         Z3_VPtag7_min6=sum((i>=300) and (i<360) for i in VP_Z3_Tag7);Z3_VPtag8_min6=sum((i>=300) and (i<360) for i in VP_Z3_Tag8);
         Z3_VPtag9_min6=sum((i>=300) and (i<360) for i in VP_Z3_Tag9);Z3_VPtag10_min6=sum((i>=300) and (i<360)for i in VP_Z3_Tag10);
         Z3_VPtag11_min6=sum((i>=300) and (i<360) for i in VP_Z3_Tag11);Z3_VPtag12_min6=sum((i>=300) and (i<360) for i in VP_Z3_Tag12);
         Z3_VPtag13_min6=sum((i>=300) and (i<360) for i in VP_Z3_Tag13);Z3_VPtag14_min6=sum((i>=300) and (i<360) for i in VP_Z3_Tag14)
         
         # minute 7
         Z3_VPtag1_min7=sum((i>=360) and (i<420) for i in VP_Z3_Tag1);Z3_VPtag2_min7=sum((i>=360) and (i<420) for i in VP_Z3_Tag2);
         Z3_VPtag3_min7=sum((i>=360) and (i<420) for i in VP_Z3_Tag3);Z3_VPtag4_min7=sum((i>=360) and (i<420) for i in VP_Z3_Tag4);
         Z3_VPtag5_min7=sum((i>=360) and (i<420) for i in VP_Z3_Tag5);Z3_VPtag6_min7=sum((i>=360) and (i<420) for i in VP_Z3_Tag6);
         Z3_VPtag7_min7=sum((i>=360) and (i<420) for i in VP_Z3_Tag7);Z3_VPtag8_min7=sum((i>=360) and (i<420) for i in VP_Z3_Tag8);
         Z3_VPtag9_min7=sum((i>=360) and (i<420) for i in VP_Z3_Tag9);Z3_VPtag10_min7=sum((i>=360) and (i<420)for i in VP_Z3_Tag10);
         Z3_VPtag11_min7=sum((i>=360) and (i<420) for i in VP_Z3_Tag11);Z3_VPtag12_min7=sum((i>=360) and (i<420) for i in VP_Z3_Tag12);
         Z3_VPtag13_min7=sum((i>=360) and (i<420) for i in VP_Z3_Tag13);Z3_VPtag14_min7=sum((i>=360) and (i<420) for i in VP_Z3_Tag14)
         
         # minute 8
         Z3_VPtag1_min8=sum((i>=420) and (i<480) for i in VP_Z3_Tag1);Z3_VPtag2_min8=sum((i>=420) and (i<480) for i in VP_Z3_Tag2);
         Z3_VPtag3_min8=sum((i>=420) and (i<480) for i in VP_Z3_Tag3);Z3_VPtag4_min8=sum((i>=420) and (i<480) for i in VP_Z3_Tag4);
         Z3_VPtag5_min8=sum((i>=420) and (i<480) for i in VP_Z3_Tag5);Z3_VPtag6_min8=sum((i>=420) and (i<480) for i in VP_Z3_Tag6);
         Z3_VPtag7_min8=sum((i>=420) and (i<480) for i in VP_Z3_Tag7);Z3_VPtag8_min8=sum((i>=420) and (i<480)for i in VP_Z3_Tag8);
         Z3_VPtag9_min8=sum((i>=420) and (i<480) for i in VP_Z3_Tag9);Z3_VPtag10_min8=sum((i>=420) and (i<480)for i in VP_Z3_Tag10);
         Z3_VPtag11_min8=sum((i>=420) and (i<480) for i in VP_Z3_Tag11);Z3_VPtag12_min8=sum((i>=420) and (i<480) for i in VP_Z3_Tag12);
         Z3_VPtag13_min8=sum((i>=420) and (i<480) for i in VP_Z3_Tag13);Z3_VPtag14_min8=sum((i>=420) and (i<480) for i in VP_Z3_Tag14)
         
         # minute 9
         Z3_VPtag1_min9=sum((i>=480) and (i<540) for i in VP_Z3_Tag1);Z3_VPtag2_min9=sum((i>=480) and (i<540) for i in VP_Z3_Tag2);
         Z3_VPtag3_min9=sum((i>=480) and (i<540) for i in VP_Z3_Tag3);Z3_VPtag4_min9=sum((i>=480) and (i<540) for i in VP_Z3_Tag4);
         Z3_VPtag5_min9=sum((i>=480) and (i<540) for i in VP_Z3_Tag5);Z3_VPtag6_min9=sum((i>=480) and (i<540) for i in VP_Z3_Tag6);
         Z3_VPtag7_min9=sum((i>=480) and (i<540) for i in VP_Z3_Tag7);Z3_VPtag8_min9=sum((i>=480) and (i<540) for i in VP_Z3_Tag8);
         Z3_VPtag9_min9=sum((i>=480) and (i<540) for i in VP_Z3_Tag9);Z3_VPtag10_min9=sum((i>=480) and (i<540) for i in VP_Z3_Tag10);
         Z3_VPtag11_min9=sum((i>=480) and (i<540) for i in VP_Z3_Tag11);Z3_VPtag12_min9=sum((i>=480) and (i<540) for i in VP_Z3_Tag12);
         Z3_VPtag13_min9=sum((i>=480) and (i<540) for i in VP_Z3_Tag13);Z3_VPtag14_min9=sum((i>=480) and (i<540) for i in VP_Z3_Tag14)        

         # minute 10
         Z3_VPtag1_min10=sum((i>=540) and (i<600) for i in VP_Z3_Tag1);Z3_VPtag2_min10=sum((i>=540) and (i<600) for i in VP_Z3_Tag2);
         Z3_VPtag3_min10=sum((i>=540) and (i<600) for i in VP_Z3_Tag3);Z3_VPtag4_min10=sum((i>=540) and (i<600) for i in VP_Z3_Tag4);
         Z3_VPtag5_min10=sum((i>=540) and (i<600) for i in VP_Z3_Tag5);Z3_VPtag6_min10=sum((i>=540) and (i<600) for i in VP_Z3_Tag6);
         Z3_VPtag7_min10=sum((i>=540) and (i<600) for i in VP_Z3_Tag7);Z3_VPtag8_min10=sum((i>=540) and (i<600) for i in VP_Z3_Tag8);
         Z3_VPtag9_min10=sum((i>=540) and (i<600) for i in VP_Z3_Tag9);Z3_VPtag10_min10=sum((i>=540) and (i<600) for i in VP_Z3_Tag10);
         Z3_VPtag11_min10=sum((i>=540) and (i<600) for i in VP_Z3_Tag11);Z3_VPtag12_min10=sum((i>=540) and (i<600) for i in VP_Z3_Tag12);
         Z3_VPtag13_min10=sum((i>=540) and (i<600) for i in VP_Z3_Tag13);Z3_VPtag14_min10=sum((i>=540) and (i<600) for i in VP_Z3_Tag14)
         
         # minute 11
         Z3_VPtag1_min11=sum((i>=600) and (i<660) for i in VP_Z3_Tag1);Z3_VPtag2_min11=sum((i>=600) and (i<660) for i in VP_Z3_Tag2);
         Z3_VPtag3_min11=sum((i>=600) and (i<660) for i in VP_Z3_Tag3);Z3_VPtag4_min11=sum((i>=600) and (i<660) for i in VP_Z3_Tag4);
         Z3_VPtag5_min11=sum((i>=600) and (i<660) for i in VP_Z3_Tag5);Z3_VPtag6_min11=sum((i>=600) and (i<660) for i in VP_Z3_Tag6);
         Z3_VPtag7_min11=sum((i>=600) and (i<660) for i in VP_Z3_Tag7);Z3_VPtag8_min11=sum((i>=600) and (i<660) for i in VP_Z3_Tag8);
         Z3_VPtag9_min11=sum((i>=600) and (i<660) for i in VP_Z3_Tag9);Z3_VPtag10_min11=sum((i>=600) and (i<660) for i in VP_Z3_Tag10);
         Z3_VPtag11_min11=sum((i>=600) and (i<660) for i in VP_Z3_Tag11);Z3_VPtag12_min11=sum((i>=600) and (i<660) for i in VP_Z3_Tag12);
         Z3_VPtag13_min11=sum((i>=600) and (i<660) for i in VP_Z3_Tag13);Z3_VPtag14_min11=sum((i>=600) and (i<660) for i in VP_Z3_Tag14)
         
         # minute 12
         Z3_VPtag1_min12=sum((i>=660) and (i<720) for i in VP_Z3_Tag1);Z3_VPtag2_min12=sum((i>=660) and (i<720) for i in VP_Z3_Tag2);
         Z3_VPtag3_min12=sum((i>=660) and (i<720) for i in VP_Z3_Tag3);Z3_VPtag4_min12=sum((i>=660) and (i<720) for i in VP_Z3_Tag4);
         Z3_VPtag5_min12=sum((i>=660) and (i<720) for i in VP_Z3_Tag5);Z3_VPtag6_min12=sum((i>=660) and (i<720) for i in VP_Z3_Tag6);
         Z3_VPtag7_min12=sum((i>=660) and (i<720) for i in VP_Z3_Tag7);Z3_VPtag8_min12=sum((i>=660) and (i<720) for i in VP_Z3_Tag8);
         Z3_VPtag9_min12=sum((i>=660) and (i<720) for i in VP_Z3_Tag9);Z3_VPtag10_min12=sum((i>=660) and (i<720) for i in VP_Z3_Tag10);
         Z3_VPtag11_min12=sum((i>=660) and (i<720) for i in VP_Z3_Tag11);Z3_VPtag12_min12=sum((i>=660) and (i<720) for i in VP_Z3_Tag12);
         Z3_VPtag13_min12=sum((i>=660) and (i<720) for i in VP_Z3_Tag13);Z3_VPtag14_min12=sum((i>=660) and (i<720) for i in VP_Z3_Tag14)
         
         # minute 13
         Z3_VPtag1_min13=sum((i>=720) and (i<780) for i in VP_Z3_Tag1);Z3_VPtag2_min13=sum((i>=720) and (i<780)for i in VP_Z3_Tag2);
         Z3_VPtag3_min13=sum((i>=720) and (i<780) for i in VP_Z3_Tag3);Z3_VPtag4_min13=sum((i>=720) and (i<780) for i in VP_Z3_Tag4);
         Z3_VPtag5_min13=sum((i>=720) and (i<780) for i in VP_Z3_Tag5);Z3_VPtag6_min13=sum((i>=720) and (i<780) for i in VP_Z3_Tag6);
         Z3_VPtag7_min13=sum((i>=720) and (i<780) for i in VP_Z3_Tag7);Z3_VPtag8_min13=sum((i>=720) and (i<780) for i in VP_Z3_Tag8);
         Z3_VPtag9_min13=sum((i>=720) and (i<780) for i in VP_Z3_Tag9);Z3_VPtag10_min13=sum((i>=720) and (i<780) for i in VP_Z3_Tag10);
         Z3_VPtag11_min13=sum((i>=720) and (i<780) for i in VP_Z3_Tag11);Z3_VPtag12_min13=sum((i>=720) and (i<780) for i in VP_Z3_Tag12);
         Z3_VPtag13_min13=sum((i>=720) and (i<780) for i in VP_Z3_Tag13);Z3_VPtag14_min13=sum((i>=720) and (i<780) for i in VP_Z3_Tag14)
         
         # minute 14
         Z3_VPtag1_min14=sum((i>=780) and (i<840) for i in VP_Z3_Tag1);Z3_VPtag2_min14=sum((i>=780) and (i<840) for i in VP_Z3_Tag2);
         Z3_VPtag3_min14=sum((i>=780) and (i<840) for i in VP_Z3_Tag3);Z3_VPtag4_min14=sum((i>=780) and (i<840) for i in VP_Z3_Tag4);
         Z3_VPtag5_min14=sum((i>=780) and (i<840) for i in VP_Z3_Tag5);Z3_VPtag6_min14=sum((i>=780) and (i<840) for i in VP_Z3_Tag6);
         Z3_VPtag7_min14=sum((i>=780) and (i<840) for i in VP_Z3_Tag7);Z3_VPtag8_min14=sum((i>=780) and (i<840) for i in VP_Z3_Tag8);
         Z3_VPtag9_min14=sum((i>=780) and (i<840) for i in VP_Z3_Tag9);Z3_VPtag10_min14=sum((i>=780) and (i<840) for i in VP_Z3_Tag10);
         Z3_VPtag11_min14=sum((i>=780) and (i<840)for i in VP_Z3_Tag11);Z3_VPtag12_min14=sum((i>=780) and (i<840) for i in VP_Z3_Tag12);
         Z3_VPtag13_min14=sum((i>=780) and (i<840) for i in VP_Z3_Tag13);Z3_VPtag14_min14=sum((i>=780) and (i<840) for i in VP_Z3_Tag14)
         
         # minute 15
         Z3_VPtag1_min15=sum((i>=840) and (i<=900) for i in VP_Z3_Tag1);Z3_VPtag2_min15=sum((i>=840) and (i<=900) for i in VP_Z3_Tag2);
         Z3_VPtag3_min15=sum((i>=840) and (i<=900) for i in VP_Z3_Tag3);Z3_VPtag4_min15=sum((i>=840) and (i<=900) for i in VP_Z3_Tag4);
         Z3_VPtag5_min15=sum((i>=840) and (i<=900) for i in VP_Z3_Tag5);Z3_VPtag6_min15=sum((i>=840) and (i<=900) for i in VP_Z3_Tag6);
         Z3_VPtag7_min15=sum((i>=840) and (i<=900) for i in VP_Z3_Tag7);Z3_VPtag8_min15=sum((i>=840) and (i<=900) for i in VP_Z3_Tag8);
         Z3_VPtag9_min15=sum((i>=840) and (i<=900) for i in VP_Z3_Tag9);Z3_VPtag10_min15=sum((i>=840) and (i<=900) for i in VP_Z3_Tag10);
         Z3_VPtag11_min15=sum((i>=840) and (i<=900) for i in VP_Z3_Tag11);Z3_VPtag12_min15=sum((i>=840) and (i<=900) for i in VP_Z3_Tag12);
         Z3_VPtag13_min15=sum((i>=840) and (i<=900) for i in VP_Z3_Tag13);Z3_VPtag14_min15=sum((i>=840) and (i<=900) for i in VP_Z3_Tag14)
         
##############################################################################################################################
# Zone 4

         Z4_VPtag1_mins=[];Z4_VPtag2_mins=[];Z4_VPtag3_mins=[];Z4_VPtag4_mins=[];Z4_VPtag5_mins=[];Z4_VPtag6_mins=[];Z4_VPtag7_mins=[];
         Z4_VPtag8_mins=[];Z4_VPtag9_mins=[];Z4_VPtag10_mins=[];Z4_VPtag11_mins=[];Z4_VPtag12_mins=[];Z4_VPtag13_mins=[];Z4_VPtag14_mins=[]
         # minute 1              
         Z4_VPtag1_min1=sum(i <60 for i in VP_Z4_Tag1);Z4_VPtag2_min1=sum(i <60 for i in VP_Z4_Tag2);Z4_VPtag3_min1=sum(i <60 for i in VP_Z4_Tag3);
         Z4_VPtag4_min1=sum(i <60 for i in VP_Z4_Tag4);Z4_VPtag5_min1=sum(i <60 for i in VP_Z4_Tag5);Z4_VPtag6_min1=sum(i <60 for i in VP_Z4_Tag6);
         Z4_VPtag7_min1=sum(i <60 for i in VP_Z4_Tag7);Z4_VPtag8_min1=sum(i <60 for i in VP_Z4_Tag8);Z4_VPtag9_min1=sum(i <60 for i in VP_Z4_Tag9);
         Z4_VPtag10_min1=sum(i <60 for i in VP_Z4_Tag10);Z4_VPtag11_min1=sum(i <60 for i in VP_Z4_Tag11);Z4_VPtag12_min1=sum(i <60 for i in VP_Z4_Tag12);
         Z4_VPtag13_min1=sum(i <60 for i in VP_Z4_Tag13);Z4_VPtag14_min1=sum(i <60 for i in VP_Z4_Tag14)

         # minute 2
         Z4_VPtag1_min2=sum((i >=60) and (i <120) for i in VP_Z4_Tag1);Z4_VPtag2_min2=sum((i >=60) and (i <120) for i in VP_Z4_Tag2);
         Z4_VPtag3_min2=sum((i >=60) and (i <120) for i in VP_Z4_Tag3);Z4_VPtag4_min2=sum((i >=60) and (i <120) for i in VP_Z4_Tag4);
         Z4_VPtag5_min2=sum((i >=60) and (i <120) for i in VP_Z4_Tag5);Z4_VPtag6_min2=sum((i >=60) and (i <120) for i in VP_Z4_Tag6);
         Z4_VPtag7_min2=sum((i >=60) and (i <120) for i in VP_Z4_Tag7);Z4_VPtag8_min2=sum((i >=60) and (i <120) for i in VP_Z4_Tag8);
         Z4_VPtag9_min2=sum((i >=60) and (i <120) for i in VP_Z4_Tag9);Z4_VPtag10_min2=sum((i >=60) and (i <120) for i in VP_Z4_Tag10);
         Z4_VPtag11_min2=sum((i >=60) and (i <120) for i in VP_Z4_Tag11);Z4_VPtag12_min2=sum((i >=60) and (i <120) for i in VP_Z4_Tag12);
         Z4_VPtag13_min2=sum((i >=60) and (i <120) for i in VP_Z4_Tag13);Z4_VPtag14_min2=sum((i >=60) and (i <120) for i in VP_Z4_Tag14)

         # minute 3
         Z4_VPtag1_min3=sum((i>=120) and (i<180) for i in VP_Z4_Tag1);Z4_VPtag2_min3=sum((i>=120) and (i<180) for i in VP_Z4_Tag2);
         Z4_VPtag3_min3=sum((i>=120) and (i<180) for i in VP_Z4_Tag3);Z4_VPtag4_min3=sum((i>=120) and (i<180) for i in VP_Z4_Tag4);
         Z4_VPtag5_min3=sum((i>=120) and (i<180) for i in VP_Z4_Tag5);Z4_VPtag6_min3=sum((i>=120) and (i<180) for i in VP_Z4_Tag6);
         Z4_VPtag7_min3=sum((i>=120) and (i<180) for i in VP_Z4_Tag7);Z4_VPtag8_min3=sum((i>=120) and (i<180) for i in VP_Z4_Tag8);
         Z4_VPtag9_min3=sum((i>=120) and (i<180) for i in VP_Z4_Tag9);Z4_VPtag10_min3=sum((i>=120) and (i<180) for i in VP_Z4_Tag10);
         Z4_VPtag11_min3=sum((i>=120) and (i<180) for i in VP_Z4_Tag11);Z4_VPtag12_min3=sum((i>=120) and (i<180) for i in VP_Z4_Tag12);
         Z4_VPtag13_min3=sum((i>=120) and (i<180) for i in VP_Z4_Tag13);Z4_VPtag14_min3=sum((i>=120) and (i<180) for i in VP_Z4_Tag14)
         
         # minute 4
         Z4_VPtag1_min4=sum((i>=180) and (i<240) for i in VP_Z4_Tag1);Z4_VPtag2_min4=sum((i>=180) and (i<240) for i in VP_Z4_Tag2);
         Z4_VPtag3_min4=sum((i>=180) and (i<240) for i in VP_Z4_Tag3);Z4_VPtag4_min4=sum((i>=180) and (i<240) for i in VP_Z4_Tag4);
         Z4_VPtag5_min4=sum((i>=180) and (i<240) for i in VP_Z4_Tag5);Z4_VPtag6_min4=sum((i>=180) and (i<240) for i in VP_Z4_Tag6);
         Z4_VPtag7_min4=sum((i>=180) and (i<240) for i in VP_Z4_Tag7);Z4_VPtag8_min4=sum((i>=180) and (i<240) for i in VP_Z4_Tag8);
         Z4_VPtag9_min4=sum((i>=180) and (i<240) for i in VP_Z4_Tag9);Z4_VPtag10_min4=sum((i>=180) and (i<240) for i in VP_Z4_Tag10);
         Z4_VPtag11_min4=sum((i>=180) and (i<240) for i in VP_Z4_Tag11);Z4_VPtag12_min4=sum((i>=180) and (i<240) for i in VP_Z4_Tag12);
         Z4_VPtag13_min4=sum((i>=180) and (i<240) for i in VP_Z4_Tag13);Z4_VPtag14_min4=sum((i>=180) and (i<240) for i in VP_Z4_Tag14)
         
         # minute 5
         Z4_VPtag1_min5=sum((i>=240) and (i<300) for i in VP_Z4_Tag1);Z4_VPtag2_min5=sum((i>=240) and (i<300) for i in VP_Z4_Tag2);
         Z4_VPtag3_min5=sum((i>=240) and (i<300) for i in VP_Z4_Tag3);Z4_VPtag4_min5=sum((i>=240) and (i<300) for i in VP_Z4_Tag4);
         Z4_VPtag5_min5=sum((i>=240) and (i<300) for i in VP_Z4_Tag5);Z4_VPtag6_min5=sum((i>=240) and (i<300) for i in VP_Z4_Tag6);
         Z4_VPtag7_min5=sum((i>=240) and (i<300) for i in VP_Z4_Tag7);Z4_VPtag8_min5=sum((i>=240) and (i<300) for i in VP_Z4_Tag8);
         Z4_VPtag9_min5=sum((i>=240) and (i<300) for i in VP_Z4_Tag9);Z4_VPtag10_min5=sum((i>=240) and (i<300) for i in VP_Z4_Tag10);
         Z4_VPtag11_min5=sum((i>=240) and (i<300) for i in VP_Z4_Tag11);Z4_VPtag12_min5=sum((i>=240) and (i<300) for i in VP_Z4_Tag12);
         Z4_VPtag13_min5=sum((i>=240) and (i<300) for i in VP_Z4_Tag13);Z4_VPtag14_min5=sum((i>=240) and (i<300) for i in VP_Z4_Tag14)
         
         # minute 6
         Z4_VPtag1_min6=sum((i>=300) and (i<360) for i in VP_Z4_Tag1);Z4_VPtag2_min6=sum((i>=300) and (i<360) for i in VP_Z4_Tag2);
         Z4_VPtag3_min6=sum((i>=300) and (i<360) for i in VP_Z4_Tag3);Z4_VPtag4_min6=sum((i>=300) and (i<360) for i in VP_Z4_Tag4);
         Z4_VPtag5_min6=sum((i>=300) and (i<360) for i in VP_Z4_Tag5);Z4_VPtag6_min6=sum((i>=300) and (i<360) for i in VP_Z4_Tag6);
         Z4_VPtag7_min6=sum((i>=300) and (i<360) for i in VP_Z4_Tag7);Z4_VPtag8_min6=sum((i>=300) and (i<360) for i in VP_Z4_Tag8);
         Z4_VPtag9_min6=sum((i>=300) and (i<360) for i in VP_Z4_Tag9);Z4_VPtag10_min6=sum((i>=300) and (i<360)for i in VP_Z4_Tag10);
         Z4_VPtag11_min6=sum((i>=300) and (i<360) for i in VP_Z4_Tag11);Z4_VPtag12_min6=sum((i>=300) and (i<360) for i in VP_Z4_Tag12);
         Z4_VPtag13_min6=sum((i>=300) and (i<360) for i in VP_Z4_Tag13);Z4_VPtag14_min6=sum((i>=300) and (i<360) for i in VP_Z4_Tag14)
         
         # minute 7
         Z4_VPtag1_min7=sum((i>=360) and (i<420) for i in VP_Z4_Tag1);Z4_VPtag2_min7=sum((i>=360) and (i<420) for i in VP_Z4_Tag2);
         Z4_VPtag3_min7=sum((i>=360) and (i<420) for i in VP_Z4_Tag3);Z4_VPtag4_min7=sum((i>=360) and (i<420) for i in VP_Z4_Tag4);
         Z4_VPtag5_min7=sum((i>=360) and (i<420) for i in VP_Z4_Tag5);Z4_VPtag6_min7=sum((i>=360) and (i<420) for i in VP_Z4_Tag6);
         Z4_VPtag7_min7=sum((i>=360) and (i<420) for i in VP_Z4_Tag7);Z4_VPtag8_min7=sum((i>=360) and (i<420) for i in VP_Z4_Tag8);
         Z4_VPtag9_min7=sum((i>=360) and (i<420) for i in VP_Z4_Tag9);Z4_VPtag10_min7=sum((i>=360) and (i<420)for i in VP_Z4_Tag10);
         Z4_VPtag11_min7=sum((i>=360) and (i<420) for i in VP_Z4_Tag11);Z4_VPtag12_min7=sum((i>=360) and (i<420) for i in VP_Z4_Tag12);
         Z4_VPtag13_min7=sum((i>=360) and (i<420) for i in VP_Z4_Tag13);Z4_VPtag14_min7=sum((i>=360) and (i<420) for i in VP_Z4_Tag14)
         
         # minute 8
         Z4_VPtag1_min8=sum((i>=420) and (i<480) for i in VP_Z4_Tag1);Z4_VPtag2_min8=sum((i>=420) and (i<480) for i in VP_Z4_Tag2);
         Z4_VPtag3_min8=sum((i>=420) and (i<480) for i in VP_Z4_Tag3);Z4_VPtag4_min8=sum((i>=420) and (i<480) for i in VP_Z4_Tag4);
         Z4_VPtag5_min8=sum((i>=420) and (i<480) for i in VP_Z4_Tag5);Z4_VPtag6_min8=sum((i>=420) and (i<480) for i in VP_Z4_Tag6);
         Z4_VPtag7_min8=sum((i>=420) and (i<480) for i in VP_Z4_Tag7);Z4_VPtag8_min8=sum((i>=420) and (i<480)for i in VP_Z4_Tag8);
         Z4_VPtag9_min8=sum((i>=420) and (i<480) for i in VP_Z4_Tag9);Z4_VPtag10_min8=sum((i>=420) and (i<480)for i in VP_Z4_Tag10);
         Z4_VPtag11_min8=sum((i>=420) and (i<480) for i in VP_Z4_Tag11);Z4_VPtag12_min8=sum((i>=420) and (i<480) for i in VP_Z4_Tag12);
         Z4_VPtag13_min8=sum((i>=420) and (i<480) for i in VP_Z4_Tag13);Z4_VPtag14_min8=sum((i>=420) and (i<480) for i in VP_Z4_Tag14)
         
         # minute 9
         Z4_VPtag1_min9=sum((i>=480) and (i<540) for i in VP_Z4_Tag1);Z4_VPtag2_min9=sum((i>=480) and (i<540) for i in VP_Z4_Tag2);
         Z4_VPtag3_min9=sum((i>=480) and (i<540) for i in VP_Z4_Tag3);Z4_VPtag4_min9=sum((i>=480) and (i<540) for i in VP_Z4_Tag4);
         Z4_VPtag5_min9=sum((i>=480) and (i<540) for i in VP_Z4_Tag5);Z4_VPtag6_min9=sum((i>=480) and (i<540) for i in VP_Z4_Tag6);
         Z4_VPtag7_min9=sum((i>=480) and (i<540) for i in VP_Z4_Tag7);Z4_VPtag8_min9=sum((i>=480) and (i<540) for i in VP_Z4_Tag8);
         Z4_VPtag9_min9=sum((i>=480) and (i<540) for i in VP_Z4_Tag9);Z4_VPtag10_min9=sum((i>=480) and (i<540) for i in VP_Z4_Tag10);
         Z4_VPtag11_min9=sum((i>=480) and (i<540) for i in VP_Z4_Tag11);Z4_VPtag12_min9=sum((i>=480) and (i<540) for i in VP_Z4_Tag12);
         Z4_VPtag13_min9=sum((i>=480) and (i<540) for i in VP_Z4_Tag13);Z4_VPtag14_min9=sum((i>=480) and (i<540) for i in VP_Z4_Tag14)        

         # minute 10
         Z4_VPtag1_min10=sum((i>=540) and (i<600) for i in VP_Z4_Tag1);Z4_VPtag2_min10=sum((i>=540) and (i<600) for i in VP_Z4_Tag2);
         Z4_VPtag3_min10=sum((i>=540) and (i<600) for i in VP_Z4_Tag3);Z4_VPtag4_min10=sum((i>=540) and (i<600) for i in VP_Z4_Tag4);
         Z4_VPtag5_min10=sum((i>=540) and (i<600) for i in VP_Z4_Tag5);Z4_VPtag6_min10=sum((i>=540) and (i<600) for i in VP_Z4_Tag6);
         Z4_VPtag7_min10=sum((i>=540) and (i<600) for i in VP_Z4_Tag7);Z4_VPtag8_min10=sum((i>=540) and (i<600) for i in VP_Z4_Tag8);
         Z4_VPtag9_min10=sum((i>=540) and (i<600) for i in VP_Z4_Tag9);Z4_VPtag10_min10=sum((i>=540) and (i<600) for i in VP_Z4_Tag10);
         Z4_VPtag11_min10=sum((i>=540) and (i<600) for i in VP_Z4_Tag11);Z4_VPtag12_min10=sum((i>=540) and (i<600) for i in VP_Z4_Tag12);
         Z4_VPtag13_min10=sum((i>=540) and (i<600) for i in VP_Z4_Tag13);Z4_VPtag14_min10=sum((i>=540) and (i<600) for i in VP_Z4_Tag14)
         
         # minute 11
         Z4_VPtag1_min11=sum((i>=600) and (i<660) for i in VP_Z4_Tag1);Z4_VPtag2_min11=sum((i>=600) and (i<660) for i in VP_Z4_Tag2);
         Z4_VPtag3_min11=sum((i>=600) and (i<660) for i in VP_Z4_Tag3);Z4_VPtag4_min11=sum((i>=600) and (i<660) for i in VP_Z4_Tag4);
         Z4_VPtag5_min11=sum((i>=600) and (i<660) for i in VP_Z4_Tag5);Z4_VPtag6_min11=sum((i>=600) and (i<660) for i in VP_Z4_Tag6);
         Z4_VPtag7_min11=sum((i>=600) and (i<660) for i in VP_Z4_Tag7);Z4_VPtag8_min11=sum((i>=600) and (i<660) for i in VP_Z4_Tag8);
         Z4_VPtag9_min11=sum((i>=600) and (i<660) for i in VP_Z4_Tag9);Z4_VPtag10_min11=sum((i>=600) and (i<660) for i in VP_Z4_Tag10);
         Z4_VPtag11_min11=sum((i>=600) and (i<660) for i in VP_Z4_Tag11);Z4_VPtag12_min11=sum((i>=600) and (i<660) for i in VP_Z4_Tag12);
         Z4_VPtag13_min11=sum((i>=600) and (i<660) for i in VP_Z4_Tag13);Z4_VPtag14_min11=sum((i>=600) and (i<660) for i in VP_Z4_Tag14)
         
         # minute 12
         Z4_VPtag1_min12=sum((i>=660) and (i<720) for i in VP_Z4_Tag1);Z4_VPtag2_min12=sum((i>=660) and (i<720) for i in VP_Z4_Tag2);
         Z4_VPtag3_min12=sum((i>=660) and (i<720) for i in VP_Z4_Tag3);Z4_VPtag4_min12=sum((i>=660) and (i<720) for i in VP_Z4_Tag4);
         Z4_VPtag5_min12=sum((i>=660) and (i<720) for i in VP_Z4_Tag5);Z4_VPtag6_min12=sum((i>=660) and (i<720) for i in VP_Z4_Tag6);
         Z4_VPtag7_min12=sum((i>=660) and (i<720) for i in VP_Z4_Tag7);Z4_VPtag8_min12=sum((i>=660) and (i<720) for i in VP_Z4_Tag8);
         Z4_VPtag9_min12=sum((i>=660) and (i<720) for i in VP_Z4_Tag9);Z4_VPtag10_min12=sum((i>=660) and (i<720) for i in VP_Z4_Tag10);
         Z4_VPtag11_min12=sum((i>=660) and (i<720) for i in VP_Z4_Tag11);Z4_VPtag12_min12=sum((i>=660) and (i<720) for i in VP_Z4_Tag12);
         Z4_VPtag13_min12=sum((i>=660) and (i<720) for i in VP_Z4_Tag13);Z4_VPtag14_min12=sum((i>=660) and (i<720) for i in VP_Z4_Tag14)
         
         # minute 13
         Z4_VPtag1_min13=sum((i>=720) and (i<780) for i in VP_Z4_Tag1);Z4_VPtag2_min13=sum((i>=720) and (i<780)for i in VP_Z4_Tag2);
         Z4_VPtag3_min13=sum((i>=720) and (i<780) for i in VP_Z4_Tag3);Z4_VPtag4_min13=sum((i>=720) and (i<780) for i in VP_Z4_Tag4);
         Z4_VPtag5_min13=sum((i>=720) and (i<780) for i in VP_Z4_Tag5);Z4_VPtag6_min13=sum((i>=720) and (i<780) for i in VP_Z4_Tag6);
         Z4_VPtag7_min13=sum((i>=720) and (i<780) for i in VP_Z4_Tag7);Z4_VPtag8_min13=sum((i>=720) and (i<780) for i in VP_Z4_Tag8);
         Z4_VPtag9_min13=sum((i>=720) and (i<780) for i in VP_Z4_Tag9);Z4_VPtag10_min13=sum((i>=720) and (i<780) for i in VP_Z4_Tag10);
         Z4_VPtag11_min13=sum((i>=720) and (i<780) for i in VP_Z4_Tag11);Z4_VPtag12_min13=sum((i>=720) and (i<780) for i in VP_Z4_Tag12);
         Z4_VPtag13_min13=sum((i>=720) and (i<780) for i in VP_Z4_Tag13);Z4_VPtag14_min13=sum((i>=720) and (i<780) for i in VP_Z4_Tag14)
         
         # minute 14
         Z4_VPtag1_min14=sum((i>=780) and (i<840) for i in VP_Z4_Tag1);Z4_VPtag2_min14=sum((i>=780) and (i<840) for i in VP_Z4_Tag2);
         Z4_VPtag3_min14=sum((i>=780) and (i<840) for i in VP_Z4_Tag3);Z4_VPtag4_min14=sum((i>=780) and (i<840) for i in VP_Z4_Tag4);
         Z4_VPtag5_min14=sum((i>=780) and (i<840) for i in VP_Z4_Tag5);Z4_VPtag6_min14=sum((i>=780) and (i<840) for i in VP_Z4_Tag6);
         Z4_VPtag7_min14=sum((i>=780) and (i<840) for i in VP_Z4_Tag7);Z4_VPtag8_min14=sum((i>=780) and (i<840) for i in VP_Z4_Tag8);
         Z4_VPtag9_min14=sum((i>=780) and (i<840) for i in VP_Z4_Tag9);Z4_VPtag10_min14=sum((i>=780) and (i<840) for i in VP_Z4_Tag10);
         Z4_VPtag11_min14=sum((i>=780) and (i<840)for i in VP_Z4_Tag11);Z4_VPtag12_min14=sum((i>=780) and (i<840) for i in VP_Z4_Tag12);
         Z4_VPtag13_min14=sum((i>=780) and (i<840) for i in VP_Z4_Tag13);Z4_VPtag14_min14=sum((i>=780) and (i<840) for i in VP_Z4_Tag14)
         
         # minute 15
         Z4_VPtag1_min15=sum((i>=840) and (i<=900) for i in VP_Z4_Tag1);Z4_VPtag2_min15=sum((i>=840) and (i<=900) for i in VP_Z4_Tag2);
         Z4_VPtag3_min15=sum((i>=840) and (i<=900) for i in VP_Z4_Tag3);Z4_VPtag4_min15=sum((i>=840) and (i<=900) for i in VP_Z4_Tag4);
         Z4_VPtag5_min15=sum((i>=840) and (i<=900) for i in VP_Z4_Tag5);Z4_VPtag6_min15=sum((i>=840) and (i<=900) for i in VP_Z4_Tag6);
         Z4_VPtag7_min15=sum((i>=840) and (i<=900) for i in VP_Z4_Tag7);Z4_VPtag8_min15=sum((i>=840) and (i<=900) for i in VP_Z4_Tag8);
         Z4_VPtag9_min15=sum((i>=840) and (i<=900) for i in VP_Z4_Tag9);Z4_VPtag10_min15=sum((i>=840) and (i<=900) for i in VP_Z4_Tag10);
         Z4_VPtag11_min15=sum((i>=840) and (i<=900) for i in VP_Z4_Tag11);Z4_VPtag12_min15=sum((i>=840) and (i<=900) for i in VP_Z4_Tag12);
         Z4_VPtag13_min15=sum((i>=840) and (i<=900) for i in VP_Z4_Tag13);Z4_VPtag14_min15=sum((i>=840) and (i<=900) for i in VP_Z4_Tag14)
         
##############################################################################################################################
# Zone 5

         Z5_VPtag1_mins=[];Z5_VPtag2_mins=[];Z5_VPtag3_mins=[];Z5_VPtag4_mins=[];Z5_VPtag5_mins=[];Z5_VPtag6_mins=[];Z5_VPtag7_mins=[];
         Z5_VPtag8_mins=[];Z5_VPtag9_mins=[];Z5_VPtag10_mins=[];Z5_VPtag11_mins=[];Z5_VPtag12_mins=[];Z5_VPtag13_mins=[];Z5_VPtag14_mins=[]
         # minute 1              
         Z5_VPtag1_min1=sum(i <60 for i in VP_Z5_Tag1);Z5_VPtag2_min1=sum(i <60 for i in VP_Z5_Tag2);Z5_VPtag3_min1=sum(i <60 for i in VP_Z5_Tag3);
         Z5_VPtag4_min1=sum(i <60 for i in VP_Z5_Tag4);Z5_VPtag5_min1=sum(i <60 for i in VP_Z5_Tag5);Z5_VPtag6_min1=sum(i <60 for i in VP_Z5_Tag6);
         Z5_VPtag7_min1=sum(i <60 for i in VP_Z5_Tag7);Z5_VPtag8_min1=sum(i <60 for i in VP_Z5_Tag8);Z5_VPtag9_min1=sum(i <60 for i in VP_Z5_Tag9);
         Z5_VPtag10_min1=sum(i <60 for i in VP_Z5_Tag10);Z5_VPtag11_min1=sum(i <60 for i in VP_Z5_Tag11);Z5_VPtag12_min1=sum(i <60 for i in VP_Z5_Tag12);
         Z5_VPtag13_min1=sum(i <60 for i in VP_Z5_Tag13);Z5_VPtag14_min1=sum(i <60 for i in VP_Z5_Tag14)
   
         # minute 2
         Z5_VPtag1_min2=sum((i >=60) and (i <120) for i in VP_Z5_Tag1);Z5_VPtag2_min2=sum((i >=60) and (i <120) for i in VP_Z5_Tag2);
         Z5_VPtag3_min2=sum((i >=60) and (i <120) for i in VP_Z5_Tag3);Z5_VPtag4_min2=sum((i >=60) and (i <120) for i in VP_Z5_Tag4);
         Z5_VPtag5_min2=sum((i >=60) and (i <120) for i in VP_Z5_Tag5);Z5_VPtag6_min2=sum((i >=60) and (i <120) for i in VP_Z5_Tag6);
         Z5_VPtag7_min2=sum((i >=60) and (i <120) for i in VP_Z5_Tag7);Z5_VPtag8_min2=sum((i >=60) and (i <120) for i in VP_Z5_Tag8);
         Z5_VPtag9_min2=sum((i >=60) and (i <120) for i in VP_Z5_Tag9);Z5_VPtag10_min2=sum((i >=60) and (i <120) for i in VP_Z5_Tag10);
         Z5_VPtag11_min2=sum((i >=60) and (i <120) for i in VP_Z5_Tag11);Z5_VPtag12_min2=sum((i >=60) and (i <120) for i in VP_Z5_Tag12);
         Z5_VPtag13_min2=sum((i >=60) and (i <120) for i in VP_Z5_Tag13);Z5_VPtag14_min2=sum((i >=60) and (i <120) for i in VP_Z5_Tag14)
            
         # minute 3
         Z5_VPtag1_min3=sum((i>=120) and (i<180) for i in VP_Z5_Tag1);Z5_VPtag2_min3=sum((i>=120) and (i<180) for i in VP_Z5_Tag2);
         Z5_VPtag3_min3=sum((i>=120) and (i<180) for i in VP_Z5_Tag3);Z5_VPtag4_min3=sum((i>=120) and (i<180) for i in VP_Z5_Tag4);
         Z5_VPtag5_min3=sum((i>=120) and (i<180) for i in VP_Z5_Tag5);Z5_VPtag6_min3=sum((i>=120) and (i<180) for i in VP_Z5_Tag6);
         Z5_VPtag7_min3=sum((i>=120) and (i<180) for i in VP_Z5_Tag7);Z5_VPtag8_min3=sum((i>=120) and (i<180) for i in VP_Z5_Tag8);
         Z5_VPtag9_min3=sum((i>=120) and (i<180) for i in VP_Z5_Tag9);Z5_VPtag10_min3=sum((i>=120) and (i<180) for i in VP_Z5_Tag10);
         Z5_VPtag11_min3=sum((i>=120) and (i<180) for i in VP_Z5_Tag11);Z5_VPtag12_min3=sum((i>=120) and (i<180) for i in VP_Z5_Tag12);
         Z5_VPtag13_min3=sum((i>=120) and (i<180) for i in VP_Z5_Tag13);Z5_VPtag14_min3=sum((i>=120) and (i<180) for i in VP_Z5_Tag14)
         
         # minute 4
         Z5_VPtag1_min4=sum((i>=180) and (i<240) for i in VP_Z5_Tag1);Z5_VPtag2_min4=sum((i>=180) and (i<240) for i in VP_Z5_Tag2);
         Z5_VPtag3_min4=sum((i>=180) and (i<240) for i in VP_Z5_Tag3);Z5_VPtag4_min4=sum((i>=180) and (i<240) for i in VP_Z5_Tag4);
         Z5_VPtag5_min4=sum((i>=180) and (i<240) for i in VP_Z5_Tag5);Z5_VPtag6_min4=sum((i>=180) and (i<240) for i in VP_Z5_Tag6);
         Z5_VPtag7_min4=sum((i>=180) and (i<240) for i in VP_Z5_Tag7);Z5_VPtag8_min4=sum((i>=180) and (i<240) for i in VP_Z5_Tag8);
         Z5_VPtag9_min4=sum((i>=180) and (i<240) for i in VP_Z5_Tag9);Z5_VPtag10_min4=sum((i>=180) and (i<240) for i in VP_Z5_Tag10);
         Z5_VPtag11_min4=sum((i>=180) and (i<240) for i in VP_Z5_Tag11);Z5_VPtag12_min4=sum((i>=180) and (i<240) for i in VP_Z5_Tag12);
         Z5_VPtag13_min4=sum((i>=180) and (i<240) for i in VP_Z5_Tag13);Z5_VPtag14_min4=sum((i>=180) and (i<240) for i in VP_Z5_Tag14)
         
         # minute 5
         Z5_VPtag1_min5=sum((i>=240) and (i<300) for i in VP_Z5_Tag1);Z5_VPtag2_min5=sum((i>=240) and (i<300) for i in VP_Z5_Tag2);
         Z5_VPtag3_min5=sum((i>=240) and (i<300) for i in VP_Z5_Tag3);Z5_VPtag4_min5=sum((i>=240) and (i<300) for i in VP_Z5_Tag4);
         Z5_VPtag5_min5=sum((i>=240) and (i<300) for i in VP_Z5_Tag5);Z5_VPtag6_min5=sum((i>=240) and (i<300) for i in VP_Z5_Tag6);
         Z5_VPtag7_min5=sum((i>=240) and (i<300) for i in VP_Z5_Tag7);Z5_VPtag8_min5=sum((i>=240) and (i<300) for i in VP_Z5_Tag8);
         Z5_VPtag9_min5=sum((i>=240) and (i<300) for i in VP_Z5_Tag9);Z5_VPtag10_min5=sum((i>=240) and (i<300) for i in VP_Z5_Tag10);
         Z5_VPtag11_min5=sum((i>=240) and (i<300) for i in VP_Z5_Tag11);Z5_VPtag12_min5=sum((i>=240) and (i<300) for i in VP_Z5_Tag12);
         Z5_VPtag13_min5=sum((i>=240) and (i<300) for i in VP_Z5_Tag13);Z5_VPtag14_min5=sum((i>=240) and (i<300) for i in VP_Z5_Tag14)
         
         # minute 6
         Z5_VPtag1_min6=sum((i>=300) and (i<360) for i in VP_Z5_Tag1);Z5_VPtag2_min6=sum((i>=300) and (i<360) for i in VP_Z5_Tag2);
         Z5_VPtag3_min6=sum((i>=300) and (i<360) for i in VP_Z5_Tag3);Z5_VPtag4_min6=sum((i>=300) and (i<360) for i in VP_Z5_Tag4);
         Z5_VPtag5_min6=sum((i>=300) and (i<360) for i in VP_Z5_Tag5);Z5_VPtag6_min6=sum((i>=300) and (i<360) for i in VP_Z5_Tag6);
         Z5_VPtag7_min6=sum((i>=300) and (i<360) for i in VP_Z5_Tag7);Z5_VPtag8_min6=sum((i>=300) and (i<360) for i in VP_Z5_Tag8);
         Z5_VPtag9_min6=sum((i>=300) and (i<360) for i in VP_Z5_Tag9);Z5_VPtag10_min6=sum((i>=300) and (i<360)for i in VP_Z5_Tag10);
         Z5_VPtag11_min6=sum((i>=300) and (i<360) for i in VP_Z5_Tag11);Z5_VPtag12_min6=sum((i>=300) and (i<360) for i in VP_Z5_Tag12);
         Z5_VPtag13_min6=sum((i>=300) and (i<360) for i in VP_Z5_Tag13);Z5_VPtag14_min6=sum((i>=300) and (i<360) for i in VP_Z5_Tag14)
         
         # minute 7
         Z5_VPtag1_min7=sum((i>=360) and (i<420) for i in VP_Z5_Tag1);Z5_VPtag2_min7=sum((i>=360) and (i<420) for i in VP_Z5_Tag2);
         Z5_VPtag3_min7=sum((i>=360) and (i<420) for i in VP_Z5_Tag3);Z5_VPtag4_min7=sum((i>=360) and (i<420) for i in VP_Z5_Tag4);
         Z5_VPtag5_min7=sum((i>=360) and (i<420) for i in VP_Z5_Tag5);Z5_VPtag6_min7=sum((i>=360) and (i<420) for i in VP_Z5_Tag6);
         Z5_VPtag7_min7=sum((i>=360) and (i<420) for i in VP_Z5_Tag7);Z5_VPtag8_min7=sum((i>=360) and (i<420) for i in VP_Z5_Tag8);
         Z5_VPtag9_min7=sum((i>=360) and (i<420) for i in VP_Z5_Tag9);Z5_VPtag10_min7=sum((i>=360) and (i<420)for i in VP_Z5_Tag10);
         Z5_VPtag11_min7=sum((i>=360) and (i<420) for i in VP_Z5_Tag11);Z5_VPtag12_min7=sum((i>=360) and (i<420) for i in VP_Z5_Tag12);
         Z5_VPtag13_min7=sum((i>=360) and (i<420) for i in VP_Z5_Tag13);Z5_VPtag14_min7=sum((i>=360) and (i<420) for i in VP_Z5_Tag14)
         
         # minute 8
         Z5_VPtag1_min8=sum((i>=420) and (i<480) for i in VP_Z5_Tag1);Z5_VPtag2_min8=sum((i>=420) and (i<480) for i in VP_Z5_Tag2);
         Z5_VPtag3_min8=sum((i>=420) and (i<480) for i in VP_Z5_Tag3);Z5_VPtag4_min8=sum((i>=420) and (i<480) for i in VP_Z5_Tag4);
         Z5_VPtag5_min8=sum((i>=420) and (i<480) for i in VP_Z5_Tag5);Z5_VPtag6_min8=sum((i>=420) and (i<480) for i in VP_Z5_Tag6);
         Z5_VPtag7_min8=sum((i>=420) and (i<480) for i in VP_Z5_Tag7);Z5_VPtag8_min8=sum((i>=420) and (i<480)for i in VP_Z5_Tag8);
         Z5_VPtag9_min8=sum((i>=420) and (i<480) for i in VP_Z5_Tag9);Z5_VPtag10_min8=sum((i>=420) and (i<480)for i in VP_Z5_Tag10);
         Z5_VPtag11_min8=sum((i>=420) and (i<480) for i in VP_Z5_Tag11);Z5_VPtag12_min8=sum((i>=420) and (i<480) for i in VP_Z5_Tag12);
         Z5_VPtag13_min8=sum((i>=420) and (i<480) for i in VP_Z5_Tag13);Z5_VPtag14_min8=sum((i>=420) and (i<480) for i in VP_Z5_Tag14)
         
         # minute 9
         Z5_VPtag1_min9=sum((i>=480) and (i<540) for i in VP_Z5_Tag1);Z5_VPtag2_min9=sum((i>=480) and (i<540) for i in VP_Z5_Tag2);
         Z5_VPtag3_min9=sum((i>=480) and (i<540) for i in VP_Z5_Tag3);Z5_VPtag4_min9=sum((i>=480) and (i<540) for i in VP_Z5_Tag4);
         Z5_VPtag5_min9=sum((i>=480) and (i<540) for i in VP_Z5_Tag5);Z5_VPtag6_min9=sum((i>=480) and (i<540) for i in VP_Z5_Tag6);
         Z5_VPtag7_min9=sum((i>=480) and (i<540) for i in VP_Z5_Tag7);Z5_VPtag8_min9=sum((i>=480) and (i<540) for i in VP_Z5_Tag8);
         Z5_VPtag9_min9=sum((i>=480) and (i<540) for i in VP_Z5_Tag9);Z5_VPtag10_min9=sum((i>=480) and (i<540) for i in VP_Z5_Tag10);
         Z5_VPtag11_min9=sum((i>=480) and (i<540) for i in VP_Z5_Tag11);Z5_VPtag12_min9=sum((i>=480) and (i<540) for i in VP_Z5_Tag12);
         Z5_VPtag13_min9=sum((i>=480) and (i<540) for i in VP_Z5_Tag13);Z5_VPtag14_min9=sum((i>=480) and (i<540) for i in VP_Z5_Tag14)        

         # minute 10
         Z5_VPtag1_min10=sum((i>=540) and (i<600) for i in VP_Z5_Tag1);Z5_VPtag2_min10=sum((i>=540) and (i<600) for i in VP_Z5_Tag2);
         Z5_VPtag3_min10=sum((i>=540) and (i<600) for i in VP_Z5_Tag3);Z5_VPtag4_min10=sum((i>=540) and (i<600) for i in VP_Z5_Tag4);
         Z5_VPtag5_min10=sum((i>=540) and (i<600) for i in VP_Z5_Tag5);Z5_VPtag6_min10=sum((i>=540) and (i<600) for i in VP_Z5_Tag6);
         Z5_VPtag7_min10=sum((i>=540) and (i<600) for i in VP_Z5_Tag7);Z5_VPtag8_min10=sum((i>=540) and (i<600) for i in VP_Z5_Tag8);
         Z5_VPtag9_min10=sum((i>=540) and (i<600) for i in VP_Z5_Tag9);Z5_VPtag10_min10=sum((i>=540) and (i<600) for i in VP_Z5_Tag10);
         Z5_VPtag11_min10=sum((i>=540) and (i<600) for i in VP_Z5_Tag11);Z5_VPtag12_min10=sum((i>=540) and (i<600) for i in VP_Z5_Tag12);
         Z5_VPtag13_min10=sum((i>=540) and (i<600) for i in VP_Z5_Tag13);Z5_VPtag14_min10=sum((i>=540) and (i<600) for i in VP_Z5_Tag14)
         
         # minute 11
         Z5_VPtag1_min11=sum((i>=600) and (i<660) for i in VP_Z5_Tag1);Z5_VPtag2_min11=sum((i>=600) and (i<660) for i in VP_Z5_Tag2);
         Z5_VPtag3_min11=sum((i>=600) and (i<660) for i in VP_Z5_Tag3);Z5_VPtag4_min11=sum((i>=600) and (i<660) for i in VP_Z5_Tag4);
         Z5_VPtag5_min11=sum((i>=600) and (i<660) for i in VP_Z5_Tag5);Z5_VPtag6_min11=sum((i>=600) and (i<660) for i in VP_Z5_Tag6);
         Z5_VPtag7_min11=sum((i>=600) and (i<660) for i in VP_Z5_Tag7);Z5_VPtag8_min11=sum((i>=600) and (i<660) for i in VP_Z5_Tag8);
         Z5_VPtag9_min11=sum((i>=600) and (i<660) for i in VP_Z5_Tag9);Z5_VPtag10_min11=sum((i>=600) and (i<660) for i in VP_Z5_Tag10);
         Z5_VPtag11_min11=sum((i>=600) and (i<660) for i in VP_Z5_Tag11);Z5_VPtag12_min11=sum((i>=600) and (i<660) for i in VP_Z5_Tag12);
         Z5_VPtag13_min11=sum((i>=600) and (i<660) for i in VP_Z5_Tag13);Z5_VPtag14_min11=sum((i>=600) and (i<660) for i in VP_Z5_Tag14)
         
         # minute 12
         Z5_VPtag1_min12=sum((i>=660) and (i<720) for i in VP_Z5_Tag1);Z5_VPtag2_min12=sum((i>=660) and (i<720) for i in VP_Z5_Tag2);
         Z5_VPtag3_min12=sum((i>=660) and (i<720) for i in VP_Z5_Tag3);Z5_VPtag4_min12=sum((i>=660) and (i<720) for i in VP_Z5_Tag4);
         Z5_VPtag5_min12=sum((i>=660) and (i<720) for i in VP_Z5_Tag5);Z5_VPtag6_min12=sum((i>=660) and (i<720) for i in VP_Z5_Tag6);
         Z5_VPtag7_min12=sum((i>=660) and (i<720) for i in VP_Z5_Tag7);Z5_VPtag8_min12=sum((i>=660) and (i<720) for i in VP_Z5_Tag8);
         Z5_VPtag9_min12=sum((i>=660) and (i<720) for i in VP_Z5_Tag9);Z5_VPtag10_min12=sum((i>=660) and (i<720) for i in VP_Z5_Tag10);
         Z5_VPtag11_min12=sum((i>=660) and (i<720) for i in VP_Z5_Tag11);Z5_VPtag12_min12=sum((i>=660) and (i<720) for i in VP_Z5_Tag12);
         Z5_VPtag13_min12=sum((i>=660) and (i<720) for i in VP_Z5_Tag13);Z5_VPtag14_min12=sum((i>=660) and (i<720) for i in VP_Z5_Tag14)
         
         # minute 13
         Z5_VPtag1_min13=sum((i>=720) and (i<780) for i in VP_Z5_Tag1);Z5_VPtag2_min13=sum((i>=720) and (i<780)for i in VP_Z5_Tag2);
         Z5_VPtag3_min13=sum((i>=720) and (i<780) for i in VP_Z5_Tag3);Z5_VPtag4_min13=sum((i>=720) and (i<780) for i in VP_Z5_Tag4);
         Z5_VPtag5_min13=sum((i>=720) and (i<780) for i in VP_Z5_Tag5);Z5_VPtag6_min13=sum((i>=720) and (i<780) for i in VP_Z5_Tag6);
         Z5_VPtag7_min13=sum((i>=720) and (i<780) for i in VP_Z5_Tag7);Z5_VPtag8_min13=sum((i>=720) and (i<780) for i in VP_Z5_Tag8);
         Z5_VPtag9_min13=sum((i>=720) and (i<780) for i in VP_Z5_Tag9);Z5_VPtag10_min13=sum((i>=720) and (i<780) for i in VP_Z5_Tag10);
         Z5_VPtag11_min13=sum((i>=720) and (i<780) for i in VP_Z5_Tag11);Z5_VPtag12_min13=sum((i>=720) and (i<780) for i in VP_Z5_Tag12);
         Z5_VPtag13_min13=sum((i>=720) and (i<780) for i in VP_Z5_Tag13);Z5_VPtag14_min13=sum((i>=720) and (i<780) for i in VP_Z5_Tag14)
         
         # minute 14
         Z5_VPtag1_min14=sum((i>=780) and (i<840) for i in VP_Z5_Tag1);Z5_VPtag2_min14=sum((i>=780) and (i<840) for i in VP_Z5_Tag2);
         Z5_VPtag3_min14=sum((i>=780) and (i<840) for i in VP_Z5_Tag3);Z5_VPtag4_min14=sum((i>=780) and (i<840) for i in VP_Z5_Tag4);
         Z5_VPtag5_min14=sum((i>=780) and (i<840) for i in VP_Z5_Tag5);Z5_VPtag6_min14=sum((i>=780) and (i<840) for i in VP_Z5_Tag6);
         Z5_VPtag7_min14=sum((i>=780) and (i<840) for i in VP_Z5_Tag7);Z5_VPtag8_min14=sum((i>=780) and (i<840) for i in VP_Z5_Tag8);
         Z5_VPtag9_min14=sum((i>=780) and (i<840) for i in VP_Z5_Tag9);Z5_VPtag10_min14=sum((i>=780) and (i<840) for i in VP_Z5_Tag10);
         Z5_VPtag11_min14=sum((i>=780) and (i<840)for i in VP_Z5_Tag11);Z5_VPtag12_min14=sum((i>=780) and (i<840) for i in VP_Z5_Tag12);
         Z5_VPtag13_min14=sum((i>=780) and (i<840) for i in VP_Z5_Tag13);Z5_VPtag14_min14=sum((i>=780) and (i<840) for i in VP_Z5_Tag14)
         
         # minute 15
         Z5_VPtag1_min15=sum((i>=840) and (i<=900) for i in VP_Z5_Tag1);Z5_VPtag2_min15=sum((i>=840) and (i<=900) for i in VP_Z5_Tag2);
         Z5_VPtag3_min15=sum((i>=840) and (i<=900) for i in VP_Z5_Tag3);Z5_VPtag4_min15=sum((i>=840) and (i<=900) for i in VP_Z5_Tag4);
         Z5_VPtag5_min15=sum((i>=840) and (i<=900) for i in VP_Z5_Tag5);Z5_VPtag6_min15=sum((i>=840) and (i<=900) for i in VP_Z5_Tag6);
         Z5_VPtag7_min15=sum((i>=840) and (i<=900) for i in VP_Z5_Tag7);Z5_VPtag8_min15=sum((i>=840) and (i<=900) for i in VP_Z5_Tag8);
         Z5_VPtag9_min15=sum((i>=840) and (i<=900) for i in VP_Z5_Tag9);Z5_VPtag10_min15=sum((i>=840) and (i<=900) for i in VP_Z5_Tag10);
         Z5_VPtag11_min15=sum((i>=840) and (i<=900) for i in VP_Z5_Tag11);Z5_VPtag12_min15=sum((i>=840) and (i<=900) for i in VP_Z5_Tag12);
         Z5_VPtag13_min15=sum((i>=840) and (i<=900) for i in VP_Z5_Tag13);Z5_VPtag14_min15=sum((i>=840) and (i<=900) for i in VP_Z5_Tag14)

         Z1_VPtag1_mins.append([Z1_VPtag1_min1,Z1_VPtag1_min2,Z1_VPtag1_min3,Z1_VPtag1_min4,Z1_VPtag1_min5,Z1_VPtag1_min6,Z1_VPtag1_min7,Z1_VPtag1_min8,
                                Z1_VPtag1_min9,Z1_VPtag1_min10,Z1_VPtag1_min11,Z1_VPtag1_min12,Z1_VPtag1_min13,Z1_VPtag1_min14,Z1_VPtag1_min15])
         Z1_VPtag2_mins.append([Z1_VPtag2_min1,Z1_VPtag2_min2,Z1_VPtag2_min3,Z1_VPtag2_min4,Z1_VPtag2_min5,Z1_VPtag2_min6,Z1_VPtag2_min7,Z1_VPtag2_min8,
                                Z1_VPtag2_min9,Z1_VPtag2_min10,Z1_VPtag2_min11,Z1_VPtag2_min12,Z1_VPtag2_min13,Z1_VPtag2_min14,Z1_VPtag2_min15])
         Z1_VPtag3_mins.append([Z1_VPtag3_min1,Z1_VPtag3_min2,Z1_VPtag3_min3,Z1_VPtag3_min4,Z1_VPtag3_min5,Z1_VPtag3_min6,Z1_VPtag3_min7,Z1_VPtag3_min8,
                                Z1_VPtag3_min9,Z1_VPtag3_min10,Z1_VPtag3_min11,Z1_VPtag3_min12,Z1_VPtag3_min13,Z1_VPtag3_min14,Z1_VPtag3_min15])
         Z1_VPtag4_mins.append([Z1_VPtag4_min1,Z1_VPtag4_min2,Z1_VPtag4_min3,Z1_VPtag4_min4,Z1_VPtag4_min5,Z1_VPtag4_min6,Z1_VPtag4_min7,Z1_VPtag4_min8,
                                Z1_VPtag4_min9,Z1_VPtag4_min10,Z1_VPtag4_min11,Z1_VPtag4_min12,Z1_VPtag4_min13,Z1_VPtag4_min14,Z1_VPtag4_min15])
         Z1_VPtag5_mins.append([Z1_VPtag5_min1,Z1_VPtag5_min2,Z1_VPtag5_min3,Z1_VPtag5_min4,Z1_VPtag5_min5,Z1_VPtag5_min6,Z1_VPtag5_min7,Z1_VPtag5_min8,
                                Z1_VPtag5_min9,Z1_VPtag5_min10,Z1_VPtag5_min11,Z1_VPtag5_min12,Z1_VPtag5_min13,Z1_VPtag5_min14,Z1_VPtag5_min15])
         Z1_VPtag6_mins.append([Z1_VPtag6_min1,Z1_VPtag6_min2,Z1_VPtag6_min3,Z1_VPtag6_min4,Z1_VPtag6_min5,Z1_VPtag6_min6,Z1_VPtag6_min7,Z1_VPtag6_min8,
                                Z1_VPtag6_min9,Z1_VPtag6_min10,Z1_VPtag6_min11,Z1_VPtag6_min12,Z1_VPtag6_min13,Z1_VPtag6_min14,Z1_VPtag6_min15])
         Z1_VPtag7_mins.append([Z1_VPtag7_min1,Z1_VPtag7_min2,Z1_VPtag7_min3,Z1_VPtag7_min4,Z1_VPtag7_min5,Z1_VPtag7_min6,Z1_VPtag7_min7,Z1_VPtag7_min8,
                                Z1_VPtag7_min9,Z1_VPtag7_min10,Z1_VPtag7_min11,Z1_VPtag7_min12,Z1_VPtag7_min13,Z1_VPtag7_min14,Z1_VPtag7_min15])
         Z1_VPtag8_mins.append([Z1_VPtag8_min1,Z1_VPtag8_min2,Z1_VPtag8_min3,Z1_VPtag8_min4,Z1_VPtag8_min5,Z1_VPtag8_min6,Z1_VPtag8_min7,Z1_VPtag8_min8,
                                Z1_VPtag8_min9,Z1_VPtag8_min10,Z1_VPtag8_min11,Z1_VPtag8_min12,Z1_VPtag8_min13,Z1_VPtag8_min14,Z1_VPtag8_min15])
         Z1_VPtag9_mins.append([Z1_VPtag9_min1,Z1_VPtag9_min2,Z1_VPtag9_min3,Z1_VPtag9_min4,Z1_VPtag9_min5,Z1_VPtag9_min6,Z1_VPtag9_min7,Z1_VPtag9_min8,
                                Z1_VPtag9_min9,Z1_VPtag9_min10,Z1_VPtag9_min11,Z1_VPtag9_min12,Z1_VPtag9_min13,Z1_VPtag9_min14,Z1_VPtag9_min15])
         Z1_VPtag10_mins.append([Z1_VPtag10_min1,Z1_VPtag10_min2,Z1_VPtag10_min3,Z1_VPtag10_min4,Z1_VPtag10_min5,Z1_VPtag10_min6,Z1_VPtag10_min7,Z1_VPtag10_min8,
                                Z1_VPtag10_min9,Z1_VPtag10_min10,Z1_VPtag10_min11,Z1_VPtag10_min12,Z1_VPtag10_min13,Z1_VPtag10_min14,Z1_VPtag10_min15])
         Z1_VPtag11_mins.append([Z1_VPtag11_min1,Z1_VPtag11_min2,Z1_VPtag11_min3,Z1_VPtag11_min4,Z1_VPtag11_min5,Z1_VPtag11_min6,Z1_VPtag11_min7,Z1_VPtag11_min8,
                                Z1_VPtag11_min9,Z1_VPtag11_min10,Z1_VPtag11_min11,Z1_VPtag11_min12,Z1_VPtag11_min13,Z1_VPtag11_min14,Z1_VPtag11_min15])
         Z1_VPtag12_mins.append([Z1_VPtag12_min1,Z1_VPtag12_min2,Z1_VPtag12_min3,Z1_VPtag12_min4,Z1_VPtag12_min5,Z1_VPtag12_min6,Z1_VPtag12_min7,Z1_VPtag12_min8,
                                Z1_VPtag12_min9,Z1_VPtag12_min10,Z1_VPtag12_min11,Z1_VPtag12_min12,Z1_VPtag12_min13,Z1_VPtag12_min14,Z1_VPtag12_min15])
         Z1_VPtag13_mins.append([Z1_VPtag13_min1,Z1_VPtag13_min2,Z1_VPtag13_min3,Z1_VPtag13_min4,Z1_VPtag13_min5,Z1_VPtag13_min6,Z1_VPtag13_min7,Z1_VPtag13_min8,
                                Z1_VPtag13_min9,Z1_VPtag13_min10,Z1_VPtag13_min11,Z1_VPtag13_min12,Z1_VPtag13_min13,Z1_VPtag13_min14,Z1_VPtag13_min15])
         Z1_VPtag14_mins.append([Z1_VPtag14_min1,Z1_VPtag14_min2,Z1_VPtag14_min3,Z1_VPtag14_min4,Z1_VPtag14_min5,Z1_VPtag14_min6,Z1_VPtag14_min7,Z1_VPtag14_min8,
                                Z1_VPtag14_min9,Z1_VPtag14_min10,Z1_VPtag14_min11,Z1_VPtag14_min12,Z1_VPtag14_min13,Z1_VPtag14_min14,Z1_VPtag14_min15])

         Z2_VPtag1_mins.append([Z2_VPtag1_min1,Z2_VPtag1_min2,Z2_VPtag1_min3,Z2_VPtag1_min4,Z2_VPtag1_min5,Z2_VPtag1_min6,Z2_VPtag1_min7,Z2_VPtag1_min8,
                                Z2_VPtag1_min9,Z2_VPtag1_min10,Z2_VPtag1_min11,Z2_VPtag1_min12,Z2_VPtag1_min13,Z2_VPtag1_min14,Z2_VPtag1_min15])
         Z2_VPtag2_mins.append([Z2_VPtag2_min1,Z2_VPtag2_min2,Z2_VPtag2_min3,Z2_VPtag2_min4,Z2_VPtag2_min5,Z2_VPtag2_min6,Z2_VPtag2_min7,Z2_VPtag2_min8,
                                Z2_VPtag2_min9,Z2_VPtag2_min10,Z2_VPtag2_min11,Z2_VPtag2_min12,Z2_VPtag2_min13,Z2_VPtag2_min14,Z2_VPtag2_min15])
         Z2_VPtag3_mins.append([Z2_VPtag3_min1,Z2_VPtag3_min2,Z2_VPtag3_min3,Z2_VPtag3_min4,Z2_VPtag3_min5,Z2_VPtag3_min6,Z2_VPtag3_min7,Z2_VPtag3_min8,
                                Z2_VPtag3_min9,Z2_VPtag3_min10,Z2_VPtag3_min11,Z2_VPtag3_min12,Z2_VPtag3_min13,Z2_VPtag3_min14,Z2_VPtag3_min15])
         Z2_VPtag4_mins.append([Z2_VPtag4_min1,Z2_VPtag4_min2,Z2_VPtag4_min3,Z2_VPtag4_min4,Z2_VPtag4_min5,Z2_VPtag4_min6,Z2_VPtag4_min7,Z2_VPtag4_min8,
                                Z2_VPtag4_min9,Z2_VPtag4_min10,Z2_VPtag4_min11,Z2_VPtag4_min12,Z2_VPtag4_min13,Z2_VPtag4_min14,Z2_VPtag4_min15])
         Z2_VPtag5_mins.append([Z2_VPtag5_min1,Z2_VPtag5_min2,Z2_VPtag5_min3,Z2_VPtag5_min4,Z2_VPtag5_min5,Z2_VPtag5_min6,Z2_VPtag5_min7,Z2_VPtag5_min8,
                                Z2_VPtag5_min9,Z2_VPtag5_min10,Z2_VPtag5_min11,Z2_VPtag5_min12,Z2_VPtag5_min13,Z2_VPtag5_min14,Z2_VPtag5_min15])
         Z2_VPtag6_mins.append([Z2_VPtag6_min1,Z2_VPtag6_min2,Z2_VPtag6_min3,Z2_VPtag6_min4,Z2_VPtag6_min5,Z2_VPtag6_min6,Z2_VPtag6_min7,Z2_VPtag6_min8,
                                Z2_VPtag6_min9,Z2_VPtag6_min10,Z2_VPtag6_min11,Z2_VPtag6_min12,Z2_VPtag6_min13,Z2_VPtag6_min14,Z2_VPtag6_min15])
         Z2_VPtag7_mins.append([Z2_VPtag7_min1,Z2_VPtag7_min2,Z2_VPtag7_min3,Z2_VPtag7_min4,Z2_VPtag7_min5,Z2_VPtag7_min6,Z2_VPtag7_min7,Z2_VPtag7_min8,
                                Z2_VPtag7_min9,Z2_VPtag7_min10,Z2_VPtag7_min11,Z2_VPtag7_min12,Z2_VPtag7_min13,Z2_VPtag7_min14,Z2_VPtag7_min15])
         Z2_VPtag8_mins.append([Z2_VPtag8_min1,Z2_VPtag8_min2,Z2_VPtag8_min3,Z2_VPtag8_min4,Z2_VPtag8_min5,Z2_VPtag8_min6,Z2_VPtag8_min7,Z2_VPtag8_min8,
                                Z2_VPtag8_min9,Z2_VPtag8_min10,Z2_VPtag8_min11,Z2_VPtag8_min12,Z2_VPtag8_min13,Z2_VPtag8_min14,Z2_VPtag8_min15])
         Z2_VPtag9_mins.append([Z2_VPtag9_min1,Z2_VPtag9_min2,Z2_VPtag9_min3,Z2_VPtag9_min4,Z2_VPtag9_min5,Z2_VPtag9_min6,Z2_VPtag9_min7,Z2_VPtag9_min8,
                                Z2_VPtag9_min9,Z2_VPtag9_min10,Z2_VPtag9_min11,Z2_VPtag9_min12,Z2_VPtag9_min13,Z2_VPtag9_min14,Z2_VPtag9_min15])
         Z2_VPtag10_mins.append([Z2_VPtag10_min1,Z2_VPtag10_min2,Z2_VPtag10_min3,Z2_VPtag10_min4,Z2_VPtag10_min5,Z2_VPtag10_min6,Z2_VPtag10_min7,Z2_VPtag10_min8,
                                Z2_VPtag10_min9,Z2_VPtag10_min10,Z2_VPtag10_min11,Z2_VPtag10_min12,Z2_VPtag10_min13,Z2_VPtag10_min14,Z2_VPtag10_min15])
         Z2_VPtag11_mins.append([Z2_VPtag11_min1,Z2_VPtag11_min2,Z2_VPtag11_min3,Z2_VPtag11_min4,Z2_VPtag11_min5,Z2_VPtag11_min6,Z2_VPtag11_min7,Z2_VPtag11_min8,
                                Z2_VPtag11_min9,Z2_VPtag11_min10,Z2_VPtag11_min11,Z2_VPtag11_min12,Z2_VPtag11_min13,Z2_VPtag11_min14,Z2_VPtag11_min15])
         Z2_VPtag12_mins.append([Z2_VPtag12_min1,Z2_VPtag12_min2,Z2_VPtag12_min3,Z2_VPtag12_min4,Z2_VPtag12_min5,Z2_VPtag12_min6,Z2_VPtag12_min7,Z2_VPtag12_min8,
                                Z2_VPtag12_min9,Z2_VPtag12_min10,Z2_VPtag12_min11,Z2_VPtag12_min12,Z2_VPtag12_min13,Z2_VPtag12_min14,Z2_VPtag12_min15])
         Z2_VPtag13_mins.append([Z2_VPtag13_min1,Z2_VPtag13_min2,Z2_VPtag13_min3,Z2_VPtag13_min4,Z2_VPtag13_min5,Z2_VPtag13_min6,Z2_VPtag13_min7,Z2_VPtag13_min8,
                                Z2_VPtag13_min9,Z2_VPtag13_min10,Z2_VPtag13_min11,Z2_VPtag13_min12,Z2_VPtag13_min13,Z2_VPtag13_min14,Z2_VPtag13_min15])
         Z2_VPtag14_mins.append([Z2_VPtag14_min1,Z2_VPtag14_min2,Z2_VPtag14_min3,Z2_VPtag14_min4,Z2_VPtag14_min5,Z2_VPtag14_min6,Z2_VPtag14_min7,Z2_VPtag14_min8,
                                Z2_VPtag14_min9,Z2_VPtag14_min10,Z2_VPtag14_min11,Z2_VPtag14_min12,Z2_VPtag14_min13,Z2_VPtag14_min14,Z2_VPtag14_min15])
         
         Z3_VPtag1_mins.append([Z3_VPtag1_min1,Z3_VPtag1_min2,Z3_VPtag1_min3,Z3_VPtag1_min4,Z3_VPtag1_min5,Z3_VPtag1_min6,Z3_VPtag1_min7,Z3_VPtag1_min8,
                                Z3_VPtag1_min9,Z3_VPtag1_min10,Z3_VPtag1_min11,Z3_VPtag1_min12,Z3_VPtag1_min13,Z3_VPtag1_min14,Z3_VPtag1_min15])
         Z3_VPtag2_mins.append([Z3_VPtag2_min1,Z3_VPtag2_min2,Z3_VPtag2_min3,Z3_VPtag2_min4,Z3_VPtag2_min5,Z3_VPtag2_min6,Z3_VPtag2_min7,Z3_VPtag2_min8,
                                Z3_VPtag2_min9,Z3_VPtag2_min10,Z3_VPtag2_min11,Z3_VPtag2_min12,Z3_VPtag2_min13,Z3_VPtag2_min14,Z3_VPtag2_min15])
         Z3_VPtag3_mins.append([Z3_VPtag3_min1,Z3_VPtag3_min2,Z3_VPtag3_min3,Z3_VPtag3_min4,Z3_VPtag3_min5,Z3_VPtag3_min6,Z3_VPtag3_min7,Z3_VPtag3_min8,
                                Z3_VPtag3_min9,Z3_VPtag3_min10,Z3_VPtag3_min11,Z3_VPtag3_min12,Z3_VPtag3_min13,Z3_VPtag3_min14,Z3_VPtag3_min15])
         Z3_VPtag4_mins.append([Z3_VPtag4_min1,Z3_VPtag4_min2,Z3_VPtag4_min3,Z3_VPtag4_min4,Z3_VPtag4_min5,Z3_VPtag4_min6,Z3_VPtag4_min7,Z3_VPtag4_min8,
                                Z3_VPtag4_min9,Z3_VPtag4_min10,Z3_VPtag4_min11,Z3_VPtag4_min12,Z3_VPtag4_min13,Z3_VPtag4_min14,Z3_VPtag4_min15])
         Z3_VPtag5_mins.append([Z3_VPtag5_min1,Z3_VPtag5_min2,Z3_VPtag5_min3,Z3_VPtag5_min4,Z3_VPtag5_min5,Z3_VPtag5_min6,Z3_VPtag5_min7,Z3_VPtag5_min8,
                                Z3_VPtag5_min9,Z3_VPtag5_min10,Z3_VPtag5_min11,Z3_VPtag5_min12,Z3_VPtag5_min13,Z3_VPtag5_min14,Z3_VPtag5_min15])
         Z3_VPtag6_mins.append([Z3_VPtag6_min1,Z3_VPtag6_min2,Z3_VPtag6_min3,Z3_VPtag6_min4,Z3_VPtag6_min5,Z3_VPtag6_min6,Z3_VPtag6_min7,Z3_VPtag6_min8,
                                Z3_VPtag6_min9,Z3_VPtag6_min10,Z3_VPtag6_min11,Z3_VPtag6_min12,Z3_VPtag6_min13,Z3_VPtag6_min14,Z3_VPtag6_min15])
         Z3_VPtag7_mins.append([Z3_VPtag7_min1,Z3_VPtag7_min2,Z3_VPtag7_min3,Z3_VPtag7_min4,Z3_VPtag7_min5,Z3_VPtag7_min6,Z3_VPtag7_min7,Z3_VPtag7_min8,
                                Z3_VPtag7_min9,Z3_VPtag7_min10,Z3_VPtag7_min11,Z3_VPtag7_min12,Z3_VPtag7_min13,Z3_VPtag7_min14,Z3_VPtag7_min15])
         Z3_VPtag8_mins.append([Z3_VPtag8_min1,Z3_VPtag8_min2,Z3_VPtag8_min3,Z3_VPtag8_min4,Z3_VPtag8_min5,Z3_VPtag8_min6,Z3_VPtag8_min7,Z3_VPtag8_min8,
                                Z3_VPtag8_min9,Z3_VPtag8_min10,Z3_VPtag8_min11,Z3_VPtag8_min12,Z3_VPtag8_min13,Z3_VPtag8_min14,Z3_VPtag8_min15])
         Z3_VPtag9_mins.append([Z3_VPtag9_min1,Z3_VPtag9_min2,Z3_VPtag9_min3,Z3_VPtag9_min4,Z3_VPtag9_min5,Z3_VPtag9_min6,Z3_VPtag9_min7,Z3_VPtag9_min8,
                                Z3_VPtag9_min9,Z3_VPtag9_min10,Z3_VPtag9_min11,Z3_VPtag9_min12,Z3_VPtag9_min13,Z3_VPtag9_min14,Z3_VPtag9_min15])
         Z3_VPtag10_mins.append([Z3_VPtag10_min1,Z3_VPtag10_min2,Z3_VPtag10_min3,Z3_VPtag10_min4,Z3_VPtag10_min5,Z3_VPtag10_min6,Z3_VPtag10_min7,Z3_VPtag10_min8,
                                Z3_VPtag10_min9,Z3_VPtag10_min10,Z3_VPtag10_min11,Z3_VPtag10_min12,Z3_VPtag10_min13,Z3_VPtag10_min14,Z3_VPtag10_min15])
         Z3_VPtag11_mins.append([Z3_VPtag11_min1,Z3_VPtag11_min2,Z3_VPtag11_min3,Z3_VPtag11_min4,Z3_VPtag11_min5,Z3_VPtag11_min6,Z3_VPtag11_min7,Z3_VPtag11_min8,
                                Z3_VPtag11_min9,Z3_VPtag11_min10,Z3_VPtag11_min11,Z3_VPtag11_min12,Z3_VPtag11_min13,Z3_VPtag11_min14,Z3_VPtag11_min15])
         Z3_VPtag12_mins.append([Z3_VPtag12_min1,Z3_VPtag12_min2,Z3_VPtag12_min3,Z3_VPtag12_min4,Z3_VPtag12_min5,Z3_VPtag12_min6,Z3_VPtag12_min7,Z3_VPtag12_min8,
                                Z3_VPtag12_min9,Z3_VPtag12_min10,Z3_VPtag12_min11,Z3_VPtag12_min12,Z3_VPtag12_min13,Z3_VPtag12_min14,Z3_VPtag12_min15])
         Z3_VPtag13_mins.append([Z3_VPtag13_min1,Z3_VPtag13_min2,Z3_VPtag13_min3,Z3_VPtag13_min4,Z3_VPtag13_min5,Z3_VPtag13_min6,Z3_VPtag13_min7,Z3_VPtag13_min8,
                                Z3_VPtag13_min9,Z3_VPtag13_min10,Z3_VPtag13_min11,Z3_VPtag13_min12,Z3_VPtag13_min13,Z3_VPtag13_min14,Z3_VPtag13_min15])
         Z3_VPtag14_mins.append([Z3_VPtag14_min1,Z3_VPtag14_min2,Z3_VPtag14_min3,Z3_VPtag14_min4,Z3_VPtag14_min5,Z3_VPtag14_min6,Z3_VPtag14_min7,Z3_VPtag14_min8,
                                Z3_VPtag14_min9,Z3_VPtag14_min10,Z3_VPtag14_min11,Z3_VPtag14_min12,Z3_VPtag14_min13,Z3_VPtag14_min14,Z3_VPtag14_min15])

         Z4_VPtag1_mins.append([Z4_VPtag1_min1,Z4_VPtag1_min2,Z4_VPtag1_min3,Z4_VPtag1_min4,Z4_VPtag1_min5,Z4_VPtag1_min6,Z4_VPtag1_min7,Z4_VPtag1_min8,
                                Z4_VPtag1_min9,Z4_VPtag1_min10,Z4_VPtag1_min11,Z4_VPtag1_min12,Z4_VPtag1_min13,Z4_VPtag1_min14,Z4_VPtag1_min15])
         Z4_VPtag2_mins.append([Z4_VPtag2_min1,Z4_VPtag2_min2,Z4_VPtag2_min3,Z4_VPtag2_min4,Z4_VPtag2_min5,Z4_VPtag2_min6,Z4_VPtag2_min7,Z4_VPtag2_min8,
                                Z4_VPtag2_min9,Z4_VPtag2_min10,Z4_VPtag2_min11,Z4_VPtag2_min12,Z4_VPtag2_min13,Z4_VPtag2_min14,Z4_VPtag2_min15])
         Z4_VPtag3_mins.append([Z4_VPtag3_min1,Z4_VPtag3_min2,Z4_VPtag3_min3,Z4_VPtag3_min4,Z4_VPtag3_min5,Z4_VPtag3_min6,Z4_VPtag3_min7,Z4_VPtag3_min8,
                                Z4_VPtag3_min9,Z4_VPtag3_min10,Z4_VPtag3_min11,Z4_VPtag3_min12,Z4_VPtag3_min13,Z4_VPtag3_min14,Z4_VPtag3_min15])
         Z4_VPtag4_mins.append([Z4_VPtag4_min1,Z4_VPtag4_min2,Z4_VPtag4_min3,Z4_VPtag4_min4,Z4_VPtag4_min5,Z4_VPtag4_min6,Z4_VPtag4_min7,Z4_VPtag4_min8,
                                Z4_VPtag4_min9,Z4_VPtag4_min10,Z4_VPtag4_min11,Z4_VPtag4_min12,Z4_VPtag4_min13,Z4_VPtag4_min14,Z4_VPtag4_min15])
         Z4_VPtag5_mins.append([Z4_VPtag5_min1,Z4_VPtag5_min2,Z4_VPtag5_min3,Z4_VPtag5_min4,Z4_VPtag5_min5,Z4_VPtag5_min6,Z4_VPtag5_min7,Z4_VPtag5_min8,
                                Z4_VPtag5_min9,Z4_VPtag5_min10,Z4_VPtag5_min11,Z4_VPtag5_min12,Z4_VPtag5_min13,Z4_VPtag5_min14,Z4_VPtag5_min15])
         Z4_VPtag6_mins.append([Z4_VPtag6_min1,Z4_VPtag6_min2,Z4_VPtag6_min3,Z4_VPtag6_min4,Z4_VPtag6_min5,Z4_VPtag6_min6,Z4_VPtag6_min7,Z4_VPtag6_min8,
                                Z4_VPtag6_min9,Z4_VPtag6_min10,Z4_VPtag6_min11,Z4_VPtag6_min12,Z4_VPtag6_min13,Z4_VPtag6_min14,Z4_VPtag6_min15])
         Z4_VPtag7_mins.append([Z4_VPtag7_min1,Z4_VPtag7_min2,Z4_VPtag7_min3,Z4_VPtag7_min4,Z4_VPtag7_min5,Z4_VPtag7_min6,Z4_VPtag7_min7,Z4_VPtag7_min8,
                                Z4_VPtag7_min9,Z4_VPtag7_min10,Z4_VPtag7_min11,Z4_VPtag7_min12,Z4_VPtag7_min13,Z4_VPtag7_min14,Z4_VPtag7_min15])
         Z4_VPtag8_mins.append([Z4_VPtag8_min1,Z4_VPtag8_min2,Z4_VPtag8_min3,Z4_VPtag8_min4,Z4_VPtag8_min5,Z4_VPtag8_min6,Z4_VPtag8_min7,Z4_VPtag8_min8,
                                Z4_VPtag8_min9,Z4_VPtag8_min10,Z4_VPtag8_min11,Z4_VPtag8_min12,Z4_VPtag8_min13,Z4_VPtag8_min14,Z4_VPtag8_min15])
         Z4_VPtag9_mins.append([Z4_VPtag9_min1,Z4_VPtag9_min2,Z4_VPtag9_min3,Z4_VPtag9_min4,Z4_VPtag9_min5,Z4_VPtag9_min6,Z4_VPtag9_min7,Z4_VPtag9_min8,
                                Z4_VPtag9_min9,Z4_VPtag9_min10,Z4_VPtag9_min11,Z4_VPtag9_min12,Z4_VPtag9_min13,Z4_VPtag9_min14,Z4_VPtag9_min15])
         Z4_VPtag10_mins.append([Z4_VPtag10_min1,Z4_VPtag10_min2,Z4_VPtag10_min3,Z4_VPtag10_min4,Z4_VPtag10_min5,Z4_VPtag10_min6,Z4_VPtag10_min7,Z4_VPtag10_min8,
                                Z4_VPtag10_min9,Z4_VPtag10_min10,Z4_VPtag10_min11,Z4_VPtag10_min12,Z4_VPtag10_min13,Z4_VPtag10_min14,Z4_VPtag10_min15])
         Z4_VPtag11_mins.append([Z4_VPtag11_min1,Z4_VPtag11_min2,Z4_VPtag11_min3,Z4_VPtag11_min4,Z4_VPtag11_min5,Z4_VPtag11_min6,Z4_VPtag11_min7,Z4_VPtag11_min8,
                                Z4_VPtag11_min9,Z4_VPtag11_min10,Z4_VPtag11_min11,Z4_VPtag11_min12,Z4_VPtag11_min13,Z4_VPtag11_min14,Z4_VPtag11_min15])
         Z4_VPtag12_mins.append([Z4_VPtag12_min1,Z4_VPtag12_min2,Z4_VPtag12_min3,Z4_VPtag12_min4,Z4_VPtag12_min5,Z4_VPtag12_min6,Z4_VPtag12_min7,Z4_VPtag12_min8,
                                Z4_VPtag12_min9,Z4_VPtag12_min10,Z4_VPtag12_min11,Z4_VPtag12_min12,Z4_VPtag12_min13,Z4_VPtag12_min14,Z4_VPtag12_min15])
         Z4_VPtag13_mins.append([Z4_VPtag13_min1,Z4_VPtag13_min2,Z4_VPtag13_min3,Z4_VPtag13_min4,Z4_VPtag13_min5,Z4_VPtag13_min6,Z4_VPtag13_min7,Z4_VPtag13_min8,
                                Z4_VPtag13_min9,Z4_VPtag13_min10,Z4_VPtag13_min11,Z4_VPtag13_min12,Z4_VPtag13_min13,Z4_VPtag13_min14,Z4_VPtag13_min15])
         Z4_VPtag14_mins.append([Z4_VPtag14_min1,Z4_VPtag14_min2,Z4_VPtag14_min3,Z4_VPtag14_min4,Z4_VPtag14_min5,Z4_VPtag14_min6,Z4_VPtag14_min7,Z4_VPtag14_min8,
                                Z4_VPtag14_min9,Z4_VPtag14_min10,Z4_VPtag14_min11,Z4_VPtag14_min12,Z4_VPtag14_min13,Z4_VPtag14_min14,Z4_VPtag14_min15])

         Z5_VPtag1_mins.append([Z5_VPtag1_min1,Z5_VPtag1_min2,Z5_VPtag1_min3,Z5_VPtag1_min4,Z5_VPtag1_min5,Z5_VPtag1_min6,Z5_VPtag1_min7,Z5_VPtag1_min8,
                                Z5_VPtag1_min9,Z5_VPtag1_min10,Z5_VPtag1_min11,Z5_VPtag1_min12,Z5_VPtag1_min13,Z5_VPtag1_min14,Z5_VPtag1_min15])
         Z5_VPtag2_mins.append([Z5_VPtag2_min1,Z5_VPtag2_min2,Z5_VPtag2_min3,Z5_VPtag2_min4,Z5_VPtag2_min5,Z5_VPtag2_min6,Z5_VPtag2_min7,Z5_VPtag2_min8,
                                Z5_VPtag2_min9,Z5_VPtag2_min10,Z5_VPtag2_min11,Z5_VPtag2_min12,Z5_VPtag2_min13,Z5_VPtag2_min14,Z5_VPtag2_min15])
         Z5_VPtag3_mins.append([Z5_VPtag3_min1,Z5_VPtag3_min2,Z5_VPtag3_min3,Z5_VPtag3_min4,Z5_VPtag3_min5,Z5_VPtag3_min6,Z5_VPtag3_min7,Z5_VPtag3_min8,
                                Z5_VPtag3_min9,Z5_VPtag3_min10,Z5_VPtag3_min11,Z5_VPtag3_min12,Z5_VPtag3_min13,Z5_VPtag3_min14,Z5_VPtag3_min15])
         Z5_VPtag4_mins.append([Z5_VPtag4_min1,Z5_VPtag4_min2,Z5_VPtag4_min3,Z5_VPtag4_min4,Z5_VPtag4_min5,Z5_VPtag4_min6,Z5_VPtag4_min7,Z5_VPtag4_min8,
                                Z5_VPtag4_min9,Z5_VPtag4_min10,Z5_VPtag4_min11,Z5_VPtag4_min12,Z5_VPtag4_min13,Z5_VPtag4_min14,Z5_VPtag4_min15])
         Z5_VPtag5_mins.append([Z5_VPtag5_min1,Z5_VPtag5_min2,Z5_VPtag5_min3,Z5_VPtag5_min4,Z5_VPtag5_min5,Z5_VPtag5_min6,Z5_VPtag5_min7,Z5_VPtag5_min8,
                                Z5_VPtag5_min9,Z5_VPtag5_min10,Z5_VPtag5_min11,Z5_VPtag5_min12,Z5_VPtag5_min13,Z5_VPtag5_min14,Z5_VPtag5_min15])
         Z5_VPtag6_mins.append([Z5_VPtag6_min1,Z5_VPtag6_min2,Z5_VPtag6_min3,Z5_VPtag6_min4,Z5_VPtag6_min5,Z5_VPtag6_min6,Z5_VPtag6_min7,Z5_VPtag6_min8,
                                Z5_VPtag6_min9,Z5_VPtag6_min10,Z5_VPtag6_min11,Z5_VPtag6_min12,Z5_VPtag6_min13,Z5_VPtag6_min14,Z5_VPtag6_min15])
         Z5_VPtag7_mins.append([Z5_VPtag7_min1,Z5_VPtag7_min2,Z5_VPtag7_min3,Z5_VPtag7_min4,Z5_VPtag7_min5,Z5_VPtag7_min6,Z5_VPtag7_min7,Z5_VPtag7_min8,
                                Z5_VPtag7_min9,Z5_VPtag7_min10,Z5_VPtag7_min11,Z5_VPtag7_min12,Z5_VPtag7_min13,Z5_VPtag7_min14,Z5_VPtag7_min15])
         Z5_VPtag8_mins.append([Z5_VPtag8_min1,Z5_VPtag8_min2,Z5_VPtag8_min3,Z5_VPtag8_min4,Z5_VPtag8_min5,Z5_VPtag8_min6,Z5_VPtag8_min7,Z5_VPtag8_min8,
                                Z5_VPtag8_min9,Z5_VPtag8_min10,Z5_VPtag8_min11,Z5_VPtag8_min12,Z5_VPtag8_min13,Z5_VPtag8_min14,Z5_VPtag8_min15])
         Z5_VPtag9_mins.append([Z5_VPtag9_min1,Z5_VPtag9_min2,Z5_VPtag9_min3,Z5_VPtag9_min4,Z5_VPtag9_min5,Z5_VPtag9_min6,Z5_VPtag9_min7,Z5_VPtag9_min8,
                                Z5_VPtag9_min9,Z5_VPtag9_min10,Z5_VPtag9_min11,Z5_VPtag9_min12,Z5_VPtag9_min13,Z5_VPtag9_min14,Z5_VPtag9_min15])
         Z5_VPtag10_mins.append([Z5_VPtag10_min1,Z5_VPtag10_min2,Z5_VPtag10_min3,Z5_VPtag10_min4,Z5_VPtag10_min5,Z5_VPtag10_min6,Z5_VPtag10_min7,Z5_VPtag10_min8,
                                Z5_VPtag10_min9,Z5_VPtag10_min10,Z5_VPtag10_min11,Z5_VPtag10_min12,Z5_VPtag10_min13,Z5_VPtag10_min14,Z5_VPtag10_min15])
         Z5_VPtag11_mins.append([Z5_VPtag11_min1,Z5_VPtag11_min2,Z5_VPtag11_min3,Z5_VPtag11_min4,Z5_VPtag11_min5,Z5_VPtag11_min6,Z5_VPtag11_min7,Z5_VPtag11_min8,
                                Z5_VPtag11_min9,Z5_VPtag11_min10,Z5_VPtag11_min11,Z5_VPtag11_min12,Z5_VPtag11_min13,Z5_VPtag11_min14,Z5_VPtag11_min15])
         Z5_VPtag12_mins.append([Z5_VPtag12_min1,Z5_VPtag12_min2,Z5_VPtag12_min3,Z5_VPtag12_min4,Z5_VPtag12_min5,Z5_VPtag12_min6,Z5_VPtag12_min7,Z5_VPtag12_min8,
                                Z5_VPtag12_min9,Z5_VPtag12_min10,Z5_VPtag12_min11,Z5_VPtag12_min12,Z5_VPtag12_min13,Z5_VPtag12_min14,Z5_VPtag12_min15])
         Z5_VPtag13_mins.append([Z5_VPtag13_min1,Z5_VPtag13_min2,Z5_VPtag13_min3,Z5_VPtag13_min4,Z5_VPtag13_min5,Z5_VPtag13_min6,Z5_VPtag13_min7,Z5_VPtag13_min8,
                                Z5_VPtag13_min9,Z5_VPtag13_min10,Z5_VPtag13_min11,Z5_VPtag13_min12,Z5_VPtag13_min13,Z5_VPtag13_min14,Z5_VPtag13_min15])
         Z5_VPtag14_mins.append([Z5_VPtag14_min1,Z5_VPtag14_min2,Z5_VPtag14_min3,Z5_VPtag14_min4,Z5_VPtag14_min5,Z5_VPtag14_min6,Z5_VPtag14_min7,Z5_VPtag14_min8,
                                Z5_VPtag14_min9,Z5_VPtag14_min10,Z5_VPtag14_min11,Z5_VPtag14_min12,Z5_VPtag14_min13,Z5_VPtag14_min14,Z5_VPtag14_min15])
         
         VP_Z1_percent=[]
         VP_Z2_percent=[]
         VP_Z3_percent=[]
         VP_Z4_percent=[]
         VP_Z5_percent=[]
 
         VP_Z1_percent.append([Z1_VPtag1_mins,Z1_VPtag2_mins,Z1_VPtag3_mins,Z1_VPtag4_mins,Z1_VPtag5_mins,Z1_VPtag6_mins,Z1_VPtag7_mins,
                               Z1_VPtag8_mins,Z1_VPtag9_mins,Z1_VPtag10_mins,Z1_VPtag11_mins,Z1_VPtag12_mins,Z1_VPtag13_mins,Z1_VPtag14_mins])

         VP_Z2_percent.append([Z2_VPtag1_mins,Z2_VPtag2_mins,Z2_VPtag3_mins,Z2_VPtag4_mins,Z2_VPtag5_mins,Z2_VPtag6_mins,Z2_VPtag7_mins,
                               Z2_VPtag8_mins,Z2_VPtag9_mins,Z2_VPtag10_mins,Z2_VPtag11_mins,Z2_VPtag12_mins,Z2_VPtag13_mins,Z2_VPtag14_mins])
         
         VP_Z3_percent.append([Z3_VPtag1_mins,Z3_VPtag2_mins,Z3_VPtag3_mins,Z3_VPtag4_mins,Z3_VPtag5_mins,Z3_VPtag6_mins,Z3_VPtag7_mins,
                               Z3_VPtag8_mins,Z3_VPtag9_mins,Z3_VPtag10_mins,Z3_VPtag11_mins,Z3_VPtag12_mins,Z3_VPtag13_mins,Z3_VPtag14_mins])
         
         VP_Z4_percent.append([Z4_VPtag1_mins,Z4_VPtag2_mins,Z4_VPtag3_mins,Z4_VPtag4_mins,Z4_VPtag5_mins,Z4_VPtag6_mins,Z4_VPtag7_mins,
                               Z4_VPtag8_mins,Z4_VPtag9_mins,Z4_VPtag10_mins,Z4_VPtag11_mins,Z4_VPtag12_mins,Z4_VPtag13_mins,Z4_VPtag14_mins])
                  
         VP_Z5_percent.append([Z5_VPtag1_mins,Z5_VPtag2_mins,Z5_VPtag3_mins,Z5_VPtag4_mins,Z5_VPtag5_mins,Z5_VPtag6_mins,Z5_VPtag7_mins,
                               Z5_VPtag8_mins,Z5_VPtag9_mins,Z5_VPtag10_mins,Z5_VPtag11_mins,Z5_VPtag12_mins,Z5_VPtag13_mins,Z5_VPtag14_mins])
   
         
         VP_Z1_percent=numpy.array(VP_Z1_percent,dtype=numpy.float64)
         VP_Z2_percent=numpy.array(VP_Z2_percent,dtype=numpy.float64)
         VP_Z3_percent=numpy.array(VP_Z3_percent,dtype=numpy.float64)
         VP_Z4_percent=numpy.array(VP_Z4_percent,dtype=numpy.float64)
         VP_Z5_percent=numpy.array(VP_Z5_percent,dtype=numpy.float64)
         print(VP_Z1_percent.shape)
         print(VP_Z1_percent[0][0][0][:])
         print(VP_Z2_percent[0][0][0][:])
         print(VP_Z3_percent[0][0][0][:])
         print(VP_Z4_percent[0][0][0][:])
         print(VP_Z5_percent[0][0][0][:])
         
         VP_Z1_percent=numpy.round((VP_Z1_percent/60)*100)    #out of 60(1 minute)
         VP_Z2_percent=numpy.round((VP_Z2_percent/60)*100)  #(1, 14, 1, 15)
         VP_Z3_percent=numpy.round((VP_Z3_percent/60)*100)
         VP_Z4_percent=numpy.round((VP_Z4_percent/60)*100)
         VP_Z5_percent=numpy.round((VP_Z5_percent/60)*100)
         print("ok")
         print(VP_Z1_percent[0][0][0][:])
         print(VP_Z2_percent[0][0][0][:])
         print(VP_Z3_percent[0][0][0][:])
         print(VP_Z4_percent[0][0][0][:])
         print(VP_Z5_percent[0][0][0][:])
         print("graphs")
         
###################################################### Numpy matrix shape troubleshoot #####################################################################         
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
             ################################################################################################################################################ 
######################### Conditional plot #################################
    #### position plot#####
         if Position_G ==1:
            plt.figure
            plt.title('Resultant Absolute Position (m)')       
            plt.plot(second_length2, Resultant[1], 'b') 
            plt.plot(second_length2, average3[1], 'r')
            plt.legend(('position change'), loc='best')
            plt.grid(True)
            plt.show()
                 
    #### Distance plot#####
         if Distance_G==1:
            plt.figure
            plt.title('Cumulative Distance (m)')
            plt.plot(count_all, Distance[1], 'b')
            plt.legend(('Distance'), loc='best')
            plt.grid(True)
            plt.show()
         
    #### Speed plot#####
         if Speed_G ==1:
            plt.figure
            plt.title('Speed (m/s)')
            plt.plot(Metric_length2, Speed_persecond[1], 'b')
            plt.legend(('Speed'), loc='best')
            plt.grid(True)
            plt.show()

     #### Speed plot#####
         if Acceleration_G ==1:
            plt.figure
            plt.title('Acceleration (m/s)')
            plt.plot(Metric_length2,Acceleration_persecond[1],'r')
            plt.legend(('Acceleration'), loc='best')
            plt.grid(True)
            plt.show()
            
         if Work_G ==1:
            plt.figure
            plt.title('Velocity (m/s)')
            plt.plot(Metric_length2,Velocity_persecond[1],'r')
            plt.legend(('Velocity'), loc='best')
            plt.grid(True)
            plt.show()
             

             
         
###################### Plots #############################################
         while self.completed <81:
            self.completed += 1
         self.progressBar.setValue (self.completed)
         self.progressBar.setValue (self.almost)


          
         for i in range (len(Tag_dict)):
             Graph_amount=["Av.Pos(m)", "Max Pos(m)", "Av.Dist(m)", "Max Dist(m)", "Av.Speed(m/s)", "Max.Speed(m/s)"]
             Graph_amount1=["Av.Speed", "Max.Speed"]
             Graph_amount2=["Av.Accel", "Max Accel"]
             Graph_amount3=["Av.Work", "Av.Rest"]
             Graph_amount4=["1", "2","3", "4","5", "6","7", "8","9", "10","11", "12","13", "14","15"]
             
             if len(Tag_dict) ==1:
                 Metric=[Resultant_diff_mean,Resultant_diff_max, Distance_mean, Distance_max, Speed_mean, Speed_max]
                 Metric1=(Speed_mean, Speed_max)
                 Metric1=numpy.array(Metric1,dtype=numpy.float64)
                 Metric2=[Resultant_Acceleration_mean[0], Resultant_Acceleration_max[0]]
                 Metric3=[Average_Work[0], Average_Rest[0]]
                 Metric_series = Metric      
                 Metric_series1 = Metric1
                 Metric_series2 = Metric2
                 Metric_series3 = Metric3
             else:
                 Metric=[Resultant_diff_mean[i],Resultant_diff_max[i], Distance_mean[i], Distance_max[i], Speed_mean[i], Speed_max[i]]
                 Metric1=[Speed_mean[i], Speed_max[i]]
                 Metric2=[Resultant_Acceleration_mean[i], Resultant_Acceleration_max[i]]
                 Metric3=[Average_Work[i], Average_Rest[i]]
                 Metric_series = pandas.Series.from_array(Metric)            
                 Metric_series1 = pandas.Series.from_array(Metric1)  
                 Metric_series2 = pandas.Series.from_array(Metric2)
                 Metric_series3 = pandas.Series.from_array(Metric3)
             
             print(i)
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

             
                 
             Metric4=numpy.array(Metric4,dtype=numpy.float64)
             Metric5=numpy.array(Metric5,dtype=numpy.float64)
             Metric6=numpy.array(Metric6,dtype=numpy.float64)
             Metric7=numpy.array(Metric7,dtype=numpy.float64)
             Metric8=numpy.array(Metric8,dtype=numpy.float64)
             Metric9=numpy.array(Metric9,dtype=numpy.float64)
             Metric10=numpy.array(Metric10,dtype=numpy.float64)
             Metric10=Metric10+1

             print(VP_Z1_percent[0][i][0][2])
             print(VP_Z2_percent[0][i][0][2])
             print(VP_Z3_percent[0][i][0][2])
             print(VP_Z4_percent[0][i][0][2])
             print(VP_Z5_percent[0][i][0][2])
             print("ok")
             print(Metric6.shape)
             print(Metric6[2])
             print(Metric7[2])
             print(Metric8[2])
             print(Metric9[2])
             print(Metric10[:])
             
#########################save plots ############################################
             width=1/1.5
             plt.figure #(figsize=(10,8))
        
             if len(Tag_dict) ==1:
                 n_groups = 2  #mins
                 fig, ax = plt.subplots()
                 index = numpy.arange(n_groups)
                 bar_width = 1
                 opacity = 1
                 rects2 = plt.bar(0, Metric_series1[0],color='orange',width=bar_width,alpha=opacity,edgecolor ='k' )
                 rects3 = plt.bar(bar_width, Metric_series1[1],color='b',width=bar_width,alpha=opacity,edgecolor ='k' )
                 plt.xlabel('Outcome')
                 plt.ylabel('Speed(m/s)')
                 plt.title('Speed')
                 plt.xticks(index, ("Av.Speed", "Max.Speed"))
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

                 plt.savefig(Output_file_directory + "/" + "Speed.png")
                 plt.close()

             else:
                 ax = Metric_series1.plot(kind='bar',edgecolor ='k')
                 ax.set_title('Speed')
                 ax.set_xlabel ('Outcome')
                 ax.set_ylabel('Speed(m/s)')
                 ax.set_xticklabels(Graph_amount1)
                 ax.tick_params(axis='x', rotation=0)
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

                 plt.savefig(Output_file_directory + "/" + "Speed.png")
                 plt.close()

    ########################
               
             width=1/1.5
             plt.figure #(figsize=(10,8))
             if len(Tag_dict) ==1:
                 n_groups = 2  #mins
                 fig, ax = plt.subplots()
                 index = numpy.arange(n_groups)
                 bar_width = 1
                 opacity = 1
                 rects2 = plt.bar(0, Metric_series2[0],color='orange',width=bar_width,alpha=opacity,edgecolor ='k' )
                 rects3 = plt.bar(bar_width, Metric_series2[1],color='b',width=bar_width,alpha=opacity,edgecolor ='k' )
                 plt.xlabel('Outcome')
                 plt.ylabel('Acceleration (m/s)')
                 plt.title('Acceleration')
                 plt.xticks(index, ("Av.Accel", "Max.Accel"))
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

                 plt.savefig(Output_file_directory + "/" + "Acceleration.png")
                 plt.close()

             else:
                 ax = Metric_series2.plot(kind='bar',edgecolor ='k')
                 ax.set_title('Acceleration')
                 ax.set_xlabel ('Outcome')
                 ax.set_ylabel('Acceleration (m/s^)')
                 ax.set_xticklabels(Graph_amount2)
                 ax.tick_params(axis='x', rotation=0)
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
               
                 plt.savefig(Output_file_directory + "/" + "Acceleration.png")
                 plt.close()

     ########################
              
             width=1/1.5
             plt.figure #(figsize=(10,8))
             if len(Tag_dict) ==1:
                 n_groups = 2  #mins
                 fig, ax = plt.subplots()
                 index = numpy.arange(n_groups)
                 bar_width = 1
                 opacity = 1
                 rects2 = plt.bar(0, Metric_series3[0],color='orange',width=bar_width,alpha=opacity,edgecolor ='k' )
                 rects3 = plt.bar(bar_width, Metric_series3[1],color='b',width=bar_width,alpha=opacity,edgecolor ='k' )
                 plt.xlabel('Outcome')
                 plt.ylabel('Work/rest (%)')
                 plt.title('Work/Rest')
                 plt.xticks(index, ("Av.Work", "Av.Rest"))
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

                 plt.savefig(Output_file_directory + "/" + "Work_Rest.png")
                 plt.close()

             else:
                 ax = Metric_series3.plot(kind='bar',edgecolor ='k')
                 ax.set_title('Work/Rest')
                 ax.set_xlabel ('Outcome')
                 ax.set_ylabel('Work/rest (%)')
                 ax.set_xticklabels(Graph_amount3)
                 ax.tick_params(axis='x', rotation=0)
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

                 plt.savefig(Output_file_directory + "/" + "Work_Rest.png")
                 plt.close()
             
########################   
             n_groups = 14  #mins

             fig, ax = plt.subplots()
             index = numpy.arange(n_groups)
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
             ymax=100
             plt.xlabel('Minute')
             plt.ylabel('Work/Rest %')
             plt.title('Work rest Ratios')
             plt.xticks(index, ('1', '2', '3', '4','5', '6', '7', '8','9', '10', '11', '12','13', '14'))
             ax.set_ylim([ymin,ymax])
            # plt.tight_layout()
             plt.savefig(Output_file_directory + "/" + "Work_Rest_min.png")
             plt.close()
##################################################################################################################
             c1=canvas.Canvas(Output_file_directory + "/" + Process_File.data()+ players[0][i] + ".pdf")
             Background='Background.png'
             c1.drawImage(Background,0,0, width=595, height=845)
             c1.setFont("Helvetica-Bold", 20,leading=None)
             c1.drawString(190,750," Peformance Outcomes")
             c1.setFont("Helvetica-Bold", 15,leading=None)        
             c1.drawString(300,725,players[0][i])
             
             c1.setFillColor(white)
             Video_Rectangle=c1.rect(50,500,500,200,fill=True)
             Court_percentage_Rectangle_1= c1.rect(50,480,50,20, fill=True)
             c1.setFillColor(white)
             Court_percentage_Rectangle_2= c1.rect(270,480,50,20, fill=True)
             c1.setFillColor(white)
             Court_percentage_Rectangle_3= c1.rect(500,480,50,20, fill=True)
             c1.setFillColor(white)
             Court_Distance_Rectangle= c1.rect(235,450,120,20,fill=True)
             
             c1.setFillColor(black)
             c1.setFont("Helvetica-Bold", 8,leading=None)
             c1.drawString(236,457,"Total Distance (m):")

             
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
             Speed_image=(Output_file_directory + "/Speed.png")
             c1.drawImage(Speed_image,49,279, width=162, height=152)
             Acceleration_image=(Output_file_directory + "/Acceleration.png")
             c1.drawImage(Acceleration_image,224,279, width=162, height=152)
             Work_image=(Output_file_directory + "/Work_Rest.png")
             c1.drawImage(Work_image,404,279, width=162, height=152)
             WR_Graph_image=(Output_file_directory + "/Work_Rest_min.png")
             c1.drawImage(WR_Graph_image,49,50, width=400, height=220)
             Intensity_image= "intensity.png"
             c1.drawImage(Intensity_image,455,50, width=115, height=65)
             c1.showPage()
             c1.save()
             c1=[]
            
         t4=time.time()
         total2=t4-t3
         print(total2)
         while self.completed <100:
            self.completed += 1
            self.progressBar.setValue (self.completed)
                       
                       
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Processing_Window = QtWidgets.QDialog()
    ui = Ui_Processing_Window()
    ui.setupUi(Processing_Window)
    Processing_Window.show()
    sys.exit(app.exec_())

