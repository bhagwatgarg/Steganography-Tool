from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets as qt
from PyQt5.QtCore import Qt as qt_align
import PyQt5.QtGui as gui
import math
import time

import sys
import numpy as np
import matplotlib.pyplot as plt

from encryption import encryption, decryption

class App(qt.QDialog):
  def __init__(self):
    super().__init__()
    self.title='Steganography'
    self.left = 10
    self.top = 10
    self.width = 400
    self.height = 200
    self.__image_type="Image Files (*.png *.jpg *.bmp)"
    self.__secret_type="Text files (*.txt)"
    self.enc_image=None
    self.secret=None
    self.stop=True
    self.__setup_ui()
    self.show()
  def __setup_ui(self):
    layout=qt.QGridLayout()

    browse_image=qt.QPushButton('Browse Image', parent=self)
    browse_image.clicked.connect(self.__browse_image)
    browse_image_l=qt.QLabel('Image', parent=self)
    image_label=qt.QLabel('Image Path Not Set', parent=self)
    image_label.setAlignment(qt_align.AlignCenter)
    image_label.setStyleSheet(" padding: 3px; border-top: 0px solid black; border-bottom: 1px solid black;")
    self.image_label=image_label
    
    browse_secret=qt.QPushButton('Browse Secret', parent=self)
    browse_secret.clicked.connect(self.__browse_secret)
    browse_secret_l=qt.QLabel('Secret', parent=self)
    secret_label=qt.QLabel('Secret Path Not Set (Ignore if decrypting)', parent=self)
    secret_label.setAlignment(qt_align.AlignCenter)
    secret_label.setStyleSheet(" padding: 3px; border-top: 0px solid black; border-bottom: 1px solid black;")
    self.secret_label=secret_label

    encrypt=qt.QPushButton('Encrypt Secret', parent=self)
    encrypt.clicked.connect(self.__encrypt)
    decrypt=qt.QPushButton('Decrypt Secret', parent=self)
    decrypt.clicked.connect(self.__decrypt)

    key=qt.QLineEdit(parent=self)
    key.setEchoMode(qt.QLineEdit.Password)
    key_label=qt.QLabel('Password', parent=self)
    self.key_widget=key

    self.process=qt.QLabel('', parent=self)

    layout.addWidget(browse_image_l, 1,1)
    layout.addWidget(browse_image, 1,2)
    layout.addWidget(image_label, 2,1, 1, 2)
    layout.addWidget(browse_secret_l, 3,1, alignment=qt_align.AlignCenter)
    layout.addWidget(browse_secret, 3, 2)
    layout.addWidget(secret_label, 4, 1, 1, 2)
    layout.addWidget(key_label, 5, 1)
    layout.addWidget(key, 5, 2)
    layout.addWidget(encrypt, 6, 1, 1, 2)
    layout.addWidget(decrypt, 7, 1, 1, 2)
    layout.addWidget(self.process, 8, 1, 1, 2)

    self.setLayout(layout)

  def __browse_image(self):
    image = qt.QFileDialog.getOpenFileName(self, ("Open Image"), "", self.__image_type)
    if image[1]==self.__image_type:
      self.enc_image=image[0]
      self.image_label.setText(f'Image Path: {self.enc_image}')

  def __browse_secret(self):
    secret = qt.QFileDialog.getOpenFileName(self, ("Browse Secret"), "", self.__secret_type)
    if secret[1]==self.__secret_type:
      self.secret=secret[0]
      self.secret_label.setText(f'Secret Path: {self.secret}')

  def show_error(self, title, text, info):
    msg = qt.QMessageBox(parent=self)
    msg.setIcon(qt.QMessageBox.Critical)
    msg.setText(text)
    msg.setInformativeText(info)
    msg.setWindowTitle(title)
    msg.exec_()
  
  def __encrypt(self):
    if self.enc_image==None or self.secret==None or self.key_widget.text()=='':
      print(self.key_widget.text)
      self.show_error("Error", "Error", 'All input fields are required!')
      return
    try:
      self.process.setText('Processing...')
      self.process.repaint()
      image=(encryption(self.enc_image, self.secret , self.key_widget.text()))
      self.process.setText('')
      filename = qt.QFileDialog.getSaveFileName(self, "Save file", "encrypted_image.png", ".png")
      # print(filename)
      plt.imsave(filename[0], image)
    except:
      self.process.setText('')
      self.show_error("Error", "Something Went Wrong", '')
  
  def __decrypt(self):
    msg = qt.QMessageBox(parent=self)
    if self.enc_image==None or self.key_widget.text()=='':
      msg.setIcon(qt.QMessageBox.Critical)
      msg.setText("Error")
      msg.setInformativeText('Image file and key are required!')
      msg.setWindowTitle("Error")
      msg.exec_()
      return
    try:
      self.process.setText('Processing...')
      self.process.repaint()
      msg=(decryption(self.enc_image, self.key_widget.text()))
      self.process.setText('')
      filename = qt.QFileDialog.getSaveFileName(self, "Save file", "secret.txt", ".txt")
      with open(filename[0],"w+") as f:
        f.write(msg)
    except:
      self.process.setText('')
      self.show_error("Error", "Something Went Wrong", '')

if __name__=='__main__':
  app = QApplication(sys.argv)
  ex = App()
  sys.exit(app.exec_())