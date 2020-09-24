from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets as qt
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
    self.__setup_ui()
    self.__image_type="Image Files (*.png *.jpg *.bmp)"
    self.__secret_type="Text files (*.txt)"
    self.enc_image=None
    self.secret=None
    self.show()
  def __setup_ui(self):
    layout=qt.QGridLayout()
    browse_image=qt.QPushButton('Browse Image', parent=self)
    browse_image.clicked.connect(self.__browse_image)
    browse_secret=qt.QPushButton('Browse Secret', parent=self)
    browse_secret.clicked.connect(self.__browse_secret)
    encrypt=qt.QPushButton('Encrypt Secret', parent=self)
    encrypt.clicked.connect(self.__encrypt)
    decrypt=qt.QPushButton('Decrypt Secret', parent=self)
    decrypt.clicked.connect(self.__decrypt)
    key=qt.QLineEdit(parent=self)
    key.setEchoMode(qt.QLineEdit.Password)
    self.key_widget=key
    layout.addWidget(browse_image, 1,1)
    layout.addWidget(browse_secret, 2, 1)
    layout.addWidget(key, 3, 1)
    layout.addWidget(encrypt, 4, 1)
    layout.addWidget(decrypt, 5, 1)
    self.setLayout(layout)
  def __browse_image(self):
    image = qt.QFileDialog.getOpenFileName(self, ("Open Image"), "", self.__image_type)
    if image[1]==self.__image_type:
      self.enc_image=image[0]
  def __browse_secret(self):
    secret = qt.QFileDialog.getOpenFileName(self, ("Browse Secret"), "", self.__secret_type)
    if secret[1]==self.__secret_type:
      self.secret=secret[0]
  def __encrypt(self):
    msg = qt.QMessageBox(parent=self)
    if self.enc_image==None or self.secret==None or self.key_widget.text()=='':
      print(self.key_widget.text)
      msg.setIcon(qt.QMessageBox.Critical)
      msg.setText("Error")
      msg.setInformativeText('All input fields are required!')
      msg.setWindowTitle("Error")
      msg.exec_()
      return
    msg.setIcon(qt.QMessageBox.Information)
    msg.setWindowTitle('Success')
    msg.setText('Files selected successfully'), 
    msg.setInformativeText(f"Image is located at {self.enc_image} \n Secret is located at {self.secret}")
    msg.exec_()
    # try:
    image=(encryption(self.enc_image, self.secret , self.key_widget.text()))
    filename = qt.QFileDialog.getSaveFileName(self, "Save file", "encrypted_image.png", ".png")
    # print(filename)
    plt.imsave(filename[0], image)
    # except:
    #   print('ERROR!!!')
        
  def __decrypt(self):
    msg = qt.QMessageBox(parent=self)
    if self.enc_image==None or self.key_widget.text()=='':
      msg.setIcon(qt.QMessageBox.Critical)
      msg.setText("Error")
      msg.setInformativeText('Image file and key are required!')
      msg.setWindowTitle("Error")
      msg.exec_()
      return
    # try:
    msg=(decryption(self.enc_image, self.key_widget.text()))
    filename = qt.QFileDialog.getSaveFileName(self, "Save file", "secret.txt", ".txt")
    with open(filename[0],"w+") as f:
      f.write(msg)
    # except:
    #   print("ERROR!!")

if __name__=='__main__':
  print('DONE')
  app = QApplication(sys.argv)
  ex = App()
  sys.exit(app.exec_())