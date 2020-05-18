import cv2
import numpy as np
import matplotlib.pyplot as plt
from img_class import image
from PyQt5 import QtWidgets
from gui2 import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog,QMessageBox
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5 import QtCore, QtWidgets, QtMultimedia
import logging

logging.basicConfig(filename='logging.log', level=logging.INFO,
                    format='%(levelname)s:%(message)s')


img1_size=()
img2_size=()

class ApplicationWindow(QtWidgets.QMainWindow):
    w1=0
    w2=0
    flag=0
    
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    
        self.ui.actionOpen_Img1.triggered.connect(self.loaddata)
        self.ui.actionOpen_Img2.triggered.connect(self.loaddata2)
        self.ui.img1_comp.currentTextChanged.connect(self.plot_combobox)
        self.ui.img2_comp.currentTextChanged.connect(self.plot_combobox2)
        self.ui.Slider1.valueChanged[int].connect(self.read_slider1)
        self.ui.slider2.valueChanged[int].connect(self.read_slider2)
        #self.ui.comboBox_out.currentTextChanged.connect(self.start_mix)
        self.remove([0,1,1,2],self.ui.comboBox_comp2)
        self.timer1 = QtCore.QTimer()
        self.timer1.setInterval(500)
        self.timer1.timeout.connect(self.combo_fn)
        self.timer1.start()
        self.ui.comboBox_comp1.currentTextChanged.connect(self.start)


    
        

    def loaddata(self):
        filename = QFileDialog.getOpenFileName(self)
        if filename[0]:
            self.path1 = filename[0]
            self.flag = 1
            self.get_image(self.path1)
            

    def combo_fn(self):
        comp1 = self.ui.comboBox_comp1.currentText()
        self.remove([0,0,0,0,0,0],self.ui.comboBox_comp2)
        if(comp1=="Magnitude"):
            self.ui.comboBox_comp2.addItems(["Phase","Uniform Phase"])
            self.timer1.stop()
        if(comp1=="Phase"):
            self.ui.comboBox_comp2.addItems(["Magnitude","Uniform Magnitude"])
            self.timer1.stop()
        if(comp1=="Real"):
            self.ui.comboBox_comp2.addItems(["Imaginary"])
            self.timer1.stop()
        if(comp1=="Imaginary"):
            self.ui.comboBox_comp2.addItems(["Real"])
            self.timer1.stop()
        if(comp1=="Uniform Phase"):
            self.ui.comboBox_comp2.addItems(["Magnitude","Uniform Magnitude"])
            self.timer1.stop()
        if(comp1=="Uniform Magnitude"):
            self.ui.comboBox_comp2.addItems(["Phase","Uniform Phase"])
            self.timer1.stop()


        
    def start(self):
        self.timer1.start()

    def get_image(self,path):
        
        self.img1=image(path)
        self.img1_size = self.img1.shape
        self.ui.view_img1.show()
        self.ui.view_img1.setImage(self.img1.img.T)
        logging.info('Image 1 is loaded correctly')


    def loaddata2(self):
        filename = QFileDialog.getOpenFileName(self)
        if filename[0]:
            self.path2 = filename[0]
            if(self.flag==1):
                self.get_image2(self.path2)
            else:
                self.error("please select image 1 first")
                logging.warning('please select image 1 first')

    def get_image2(self,path):
        
        self.img2=image(path)
        self.img2_size = self.img2.shape   
        if(self.img1_size==self.img2_size):
            self.ui.view_img2.show()
            self.ui.view_img2.setImage(self.img2.img.T)
            logging.info('Image 2 is loaded correctly')
        else:
            self.error("please chose another images with the same size")
            logging.error("please chose another images with the same size")

        
    def plot_combobox(self):
        self.text = self.ui.img1_comp.currentText()
        if(self.text =="Magnitude"):
            self.ui.view_comp1.show()
            self.ui.view_comp1.setImage(self.img1.mag_spectrum.T)
        if(self.text=="Phase"):
            self.ui.view_comp1.show()
            self.ui.view_comp1.setImage(self.img1.phase_spectrum.T)
        if(self.text=="Real"):
            self.ui.view_comp1.show()
            self.ui.view_comp1.setImage(self.img1.real_spectrum.T)
        if(self.text=="Imaginary"):
            self.ui.view_comp1.show()
            self.ui.view_comp1.setImage(self.img1.imag_spectrum.T)
        if(self.text!="Select Componant...."):
            logging.info('{} componant of image 1 is loaded correctly'.format(self.text))
            
        


    def plot_combobox2(self):
        self.text2 = self.ui.img2_comp.currentText()
        if(self.text2=="Magnitude"):
            self.ui.view_comp2.show()
            self.ui.view_comp2.setImage(self.img2.mag_spectrum.T)
        if(self.text2=="Phase"):
            self.ui.view_comp2.show()
            self.ui.view_comp2.setImage(self.img2.phase_spectrum.T)
        if(self.text2=="Real"):
            self.ui.view_comp2.show()
            self.ui.view_comp2.setImage(self.img2.real_spectrum.T)
        if(self.text2=="Imaginary"):
            self.ui.view_comp2.show()
            self.ui.view_comp2.setImage(self.img2.imag_spectrum.T)
        if(self.text2!="Select Componant...."):
            logging.info('{} componant of image 2 is loaded correctly'.format(self.text2))
    
        
    def read_slider1(self,value):
        self.w1=value/100
        self.start_mix()

    def read_slider2(self,value):
        self.w2=value/100
        self.start_mix()

    def remove(self,arr,value):
        for i in arr:
            value.removeItem(i)

    def mixing(self,w1,w2,out1,out2,out3,out4):
        out_T = self.ui.comboBox_out.currentText()
        comp1 = self.ui.comboBox_comp1.currentText()
        comp2 = self.ui.comboBox_comp2.currentText()
        if(out_T=="Output 1"):
            if(comp1=="Real" or comp2=="Real" or comp1=="Imaginary" or comp2=="Imaginary" ):
                mix2= (w1*out1+((1-w1)*out3)) + ((w2*out2)+((1-w2)*out4))*1j 
                mix2 = np.fft.ifft2(mix2)
                mix2 = np.real(mix2)
                self.ui.view_out1.show()
                self.ui.view_out1.setImage(mix2.T)
                logging.info('We have mixed {} of {} of {} with {} of {} of {} in {} window'.format(w1,comp1,self.img1_T,w2,comp2,self.img2_T,out_T))
            else:
                mix1= ((w1*out1)+((1-w1)*out3))*np.exp(1j*((w2*out2)+((1-w2)*out4))) 
                mix1 = np.fft.ifft2(mix1)
                mix1 = np.real(mix1)
                self.ui.view_out1.show()
                self.ui.view_out1.setImage(mix1.T)
                logging.info('We have mixed {} of {} of {} with {} of {} of {} in {} window'.format(w1,comp1,self.img1_T,w2,comp2,self.img2_T,out_T))
        if(out_T=="Output 2"):
            if(comp1=="Real" or comp2=="Real" or comp1=="Imaginary" or comp2=="Imaginary" ):
                mix2= (w1*out1+((1-w1)*out3)) + ((w2*out2)+((1-w2)*out4))*1j 
                mix2 = np.fft.ifft2(mix2)
                mix2 = np.real(mix2)
                self.ui.view_out2.show()
                self.ui.view_out2.setImage(mix2.T)
                logging.info('We have mixed {} of {} of {} with {} of {} of {} in {} window'.format(w1,comp1,self.img1_T,w2,comp2,self.img2_T,out_T))
            else:
                mix1= ((w1*out1)+((1-w1)*out3))*np.exp(1j*((w2*out2)+((1-w2)*out4))) 
                mix1 = np.fft.ifft2(mix1)
                mix1 = np.real(mix1)
                self.ui.view_out2.show()
                self.ui.view_out2.setImage(mix1.T)
                logging.info('We have mixed {} of {} of {} with {} of {} of {} in {} window'.format(w1,comp1,self.img1_T,w2,comp2,self.img2_T,out_T))

    def start_mix(self):
        self.img1_T = self.ui.comboBox1_img.currentText()
        self.img2_T = self.ui.comboBox2_img.currentText()
        comp1 = self.ui.comboBox_comp1.currentText()
        comp2 = self.ui.comboBox_comp2.currentText()

        if (self.img1_T== 'Image 1'):
            if(comp1=="Phase"):
                out1=self.img1.phase_spectrum
                out3=self.img2.phase_spectrum
            if(comp1=="Magnitude"):
                out1=self.img1.fourier_abs
                out3=self.img2.fourier_abs
            if(comp1=="Real"):
                out1=self.img1.real_spectrum
                out3=self.img2.real_spectrum
            if(comp1=="Imaginary"):
                out1=self.img1.imag_spectrum
                out3=self.img2.imag_spectrum
            if(comp1=="Uniform Phase"):
                out1=self.img1.uniform_phase
                out3=self.img2.uniform_phase
            if(comp1=="Uniform Magnitude"):
                out1=self.img1.uniform_mag
                out3=self.img2.uniform_mag

        if(self.img1_T== 'Image 2'):
            if(comp1=="Phase"):
                out1=self.img2.phase_spectrum
                out3=self.img1.phase_spectrum
            if(comp1=="Magnitude"):
                out1=self.img2.fourier_abs
                out3=self.img1.fourier_abs
            if(comp1=="Real"):
                out1=self.img2.real_spectrum
                out3=self.img1.real_spectrum
            if(comp1=="Imaginary"):
                out1=self.img2.imag_spectrum
                out3=self.img1.imag_spectrum
            if(comp1=="Uniform Phase"):
                out1=self.img2.uniform_phase
                out3=self.img1.uniform_phase
            if(comp1=="Uniform Magnitude"):
                out1=self.img2.uniform_mag
                out3=self.img1.uniform_mag

        if (self.img2_T== 'Image 1'):
            if(comp2=="Phase"):
                out2=self.img1.phase_spectrum
                out4=self.img2.phase_spectrum
            if(comp2=="Magnitude"):
                out2=self.img1.fourier_abs
                out4=self.img2.fourier_abs           
            if(comp2=="Real"):
                out2=self.img1.real_spectrum
                out4=self.img2.real_spectrum
            if(comp2=="Imaginary"):
                out2=self.img1.imag_spectrum
                out4=self.img2.imag_spectrum
            if(comp2=="Uniform Phase"):
                out2=self.img1.uniform_phase
                out4=self.img2.uniform_phase
            if(comp2=="Uniform Magnitude"):
                out2=self.img1.uniform_mag
                out4=self.img2.uniform_mag

        if(self.img2_T== 'Image 2'):
            if(comp2=="Phase"):
                out2=self.img2.phase_spectrum
                out4=self.img1.phase_spectrum
            if(comp2=="Magnitude"):
                out2=self.img2.fourier_abs
                out4=self.img1.fourier_abs
            if(comp2=="Real"):
                out2=self.img2.real_spectrum
                out4=self.img1.real_spectrum
            if(comp2=="Imaginary"):
                out2=self.img2.imag_spectrum
                out4=self.img1.imag_spectrum
            if(comp2=="Uniform Phase"):
                out2=self.img2.uniform_phase
                out4=self.img1.uniform_phase
            if(comp2=="Uniform Magnitude"):
                out2=self.img2.uniform_mag
                out4=self.img1.uniform_mag  
        self.mixing(self.w1,self.w2,out1,out2,out3,out4)

    def error(self,value):
        msg = QMessageBox()
        msg.setWindowTitle("error message")
        msg.setText(value)  
        msg.setIcon(QMessageBox.Critical)
        x=msg.exec_()      






def main():
	app = QtWidgets.QApplication(sys.argv)
	application = ApplicationWindow()
	application.show()
	app.exec_()


if __name__ == "__main__":
	main()







