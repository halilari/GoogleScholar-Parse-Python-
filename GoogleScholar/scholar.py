# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Masaüstü/deneme.ui'
#
# Created: Sat Mar 26 01:34:22 2016
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import *
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebKitWidgets import *
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QListWidgetItem
import requests
import html5lib
import lxml
import webbrowser
import urllib3
import time
import random
from Author import Author
import hashlib
import urllib
from urllib import request
import sys


_GOOGLEID = hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()[:16]
_COOKIES = {'GSP': 'ID={0}:CF=4'.format(_GOOGLEID)}
_HEADERS = {
    'accept-language': 'en-US,en',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml'
    }
_SCHOLARHOST="https://scholar.google.com.tr"
_AUTHSEARCH = '/citations?view_op=search_authors&hl=en&mauthors='
_NEXTLINK="&cstart="
_PAGESIZE=100
_STARTLINK=0
pagelink=""
alintiliste=[]
yilliste=[]
_PUBSTART=0
_YAZAR=Author
gitlink=""

class Ui_MainWindow(object):
    def authorSearch(self,Author):
        url=requests.get(_SCHOLARHOST+_AUTHSEARCH+Author.getAdiSoyadi(),headers=_HEADERS, cookies=_COOKIES)
        print(url.url)
        if url.status_code==200:
            self.lbl_link.setText("Bağlantı Sağlandı!!!")
            soup=BeautifulSoup(url.content, "html.parser")
            if(soup.find("div","gs_med")):
                print("Böyle Bir Kullanıcı Yoktur...")
                return
            a=soup.find("h3","gsc_1usr_name")
            link=a.find("a").get("href")
            print(link)
        else:
            print("Siteye Erişim Sağlanamadı...")
            return
        return link

    def ara(self,gelen):
        global _PUBSTART
        _PUBSTART=0
        _YAZAR=Author(self.lineEdit.text())
        _YAZAR.Makaleleri.clear()
        alintiliste.clear()
        yilliste.clear()
        _YAZAR.ilgiAlanlari.clear()
        _YAZAR.Katki.clear()
        self.list_Makale.clear()
        self.list_Yil.clear()
        self.list_Alinti.clear()
        print(_YAZAR.getAdiSoyadi())
        pagelink=self.authorSearch(_YAZAR)
        self.authorPage(pagelink)
        print("Yazar Adı Soyadı:"+_YAZAR.AdiSoyadi)
        print("Çalışma Yeri:"+_YAZAR.CalismaYeri)
        print("Toplam Alıntılanma:"+_YAZAR.ToplamAlintilanma)
        print("İlgi Alanları:"+"\t")
        for i in _YAZAR.ilgiAlanlari:
            print(i)

        for i in range(0,len(_YAZAR.Makaleleri)):
            print("Makale Adı:"+_YAZAR.Makaleleri[i]+"\t\tYayınlanma Yılı:"+yilliste[i]+"\t\tAlıntılanma:"+alintiliste[i])

        self.list_Makale.addItems(_YAZAR.Makaleleri)
        self.list_Alinti.addItems(alintiliste)
        self.list_Yil.addItems(yilliste)
        self.lbl_Calisma.setText(_YAZAR.CalismaYeri)
        self.lbl_Alintilanma.setText(_YAZAR.ToplamAlintilanma)
        a=""
        for i in range(0,len(_YAZAR.ilgiAlanlari)):
            if i==len(_YAZAR.ilgiAlanlari)-1:
                a+=_YAZAR.ilgiAlanlari[i]
            else:
                a+=_YAZAR.ilgiAlanlari[i]+","
        self.lbl_Alanlar.setText(a)
        b=""
        for i in range(0,len(_YAZAR.Katki)):
            if i ==len(_YAZAR.Katki)-1:
                b+=_YAZAR.Katki[i]
            else:
                b+=_YAZAR.Katki[i]+","
        self.lbl_Katkilar.setText(b)
        self.lbl_foto.setPixmap(QtGui.QPixmap("myfile.jpeg"))
        print(self.lineEdit_max.text())


    def authorArticle(self,pagelink):
        global _PUBSTART
        global _PAGESIZE
        global gitlink
        url=requests.get(_SCHOLARHOST+pagelink+_NEXTLINK+str(_PUBSTART)+"&pagesize="+str(_PAGESIZE),headers=_HEADERS, cookies=_COOKIES)
        print(url.url)
        if url.status_code==200:
            soup=BeautifulSoup(url.content,"html.parser")
            a=soup.find("td", class_="gsc_a_t")
            b=a.find("a",class_="gsc_a_at")
            gitlink=b.get("href")
            for i in soup.find_all("tr", class_="gsc_a_tr"):
                for j in i.find("td",class_="gsc_a_c"):
                    for k in i.find("td", class_="gsc_a_y"):
                        if k.text is not "":
                            if int(k.text)>int(self.lineEdit_min.text()) and int(k.text)<int(self.lineEdit_max.text()):
                                 _YAZAR.Makaleleri.append(i.find("a").text)
                                 yilliste.append(k.text)
                                 alintiliste.append(j.text)
            if 'disabled' not in soup.find('button', id='gsc_bpf_next').attrs:
                 _PUBSTART+=_PAGESIZE
                 self.authorArticle(pagelink)

    def authorPage(self,pagelink):
        print(pagelink)
        url=requests.get(_SCHOLARHOST+pagelink,headers=_HEADERS, cookies=_COOKIES)
        print(url.url)
        self.lbl_link.setOpenExternalLinks(True)
        self.lbl_link.setText(url.url)
        if url.status_code==200:
            self.lbl_link.setText("Yazar Sayfasına Ulaşıldı")
            soup=BeautifulSoup(url.content, "html.parser")
            fotourl=urllib.request.urlopen(_SCHOLARHOST+pagelink)
            fotosoup=BeautifulSoup( fotourl.read(),"html.parser")
            images = soup.find_all( 'img' )
            for  i in images:
                filename =_SCHOLARHOST+i.get( 'src' )
                data = urllib.request.urlopen( filename ).read()
                with open( "myfile.jpeg", "wb" ) as code:
                    code.write( data )
            ad=soup.find("div", id="gsc_prf_in").text.upper()
            self.lbl_Ad.setText(ad)
            _YAZAR.setAdiSoyadi(ad)
            print(soup.find("div", id="gsc_prf_in").text.upper())
            _YAZAR.CalismaYeri=soup.find("div", class_="gsc_prf_il").text
            _YAZAR.ToplamAlintilanma=soup.find("td", class_="gsc_rsb_std").text
            a=soup.find("div", class_="gsc_prf_il").next_sibling
            for i in soup.find_all("a",class_="gsc_rsb_aa"):
                _YAZAR.Katki.append(i.text)
            for i in a.find_all("a",class_="gsc_prf_ila"):
                _YAZAR.ilgiAlanlari.append(i.text)
            self.authorArticle(pagelink)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1210, 870)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(110, 190, 661, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_min= QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_min.setGeometry(QtCore.QRect(780, 190, 113, 41))
        self.lineEdit_min.setObjectName("lineEdit")
        self.lineEdit_max= QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_max.setGeometry(QtCore.QRect(910, 190, 113, 41))
        self.lineEdit_max.setObjectName("lineEdit")
        self.btnAra = QtWidgets.QPushButton(self.centralwidget)
        self.btnAra.setEnabled(True)
        self.btnAra.setGeometry(QtCore.QRect(1040, 190, 131, 41))
        self.btnAra.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.btnAra.setMouseTracking(False)
        self.btnAra.setWhatsThis("")
        self.btnAra.setInputMethodHints(QtCore.Qt.ImhNone)
        self.btnAra.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Search-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAra.setIcon(icon)
        self.btnAra.setIconSize(QtCore.QSize(35, 35))
        self.btnAra.setCheckable(False)
        self.btnAra.setObjectName("btnAra")
        self.btnAra.clicked.connect(lambda:self.ara(self.lineEdit.text()))
        self.lbl_Ad = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Ad.setGeometry(QtCore.QRect(520, 20, 630, 17))
        self.lbl_Ad.setText("")
        self.lbl_Ad.setObjectName("lbl_Ad")
        self.lbl_Calisma = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Calisma.setGeometry(QtCore.QRect(250, 50, 630, 17))
        self.lbl_Calisma.setText("")
        self.lbl_Calisma.setObjectName("lbl_Calisma")
        self.lbl_Alintilanma = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Alintilanma.setGeometry(QtCore.QRect(250, 80, 630, 17))
        self.lbl_Alintilanma.setText("")
        self.lbl_Alintilanma.setObjectName("lbl_Alintilanma")
        self.lbl_Alanlar = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Alanlar.setGeometry(QtCore.QRect(250, 110, 630, 17))
        self.lbl_Alanlar.setText("")
        self.lbl_Alanlar.setObjectName("lbl_Alanlar")
        self.lbl_Katkilar = QtWidgets.QLabel(self.centralwidget)
        self.lbl_Katkilar.setGeometry(QtCore.QRect(250, 140, 630, 17))
        self.lbl_Katkilar.setText("")
        self.lbl_Katkilar.setObjectName("lbl_Katkilar")
        self.lbl_link = QtWidgets.QLabel(self.centralwidget)
        self.lbl_link.setGeometry(QtCore.QRect(230, 170, 931, 17))
        self.lbl_link.setText("")
        self.lbl_link.setObjectName("lbl_link")
        self.lbl_link.setOpenExternalLinks(True)
        self.lbl_link.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lbl_bilgi = QtWidgets.QLabel(self.centralwidget)
        self.lbl_bilgi.setGeometry(QtCore.QRect(110, 230, 1051, 17))
        self.lbl_bilgi.setText("")
        self.lbl_bilgi.setObjectName("lbl_bilgi")
        self.list_Makale = QtWidgets.QListWidget(self.centralwidget)
        self.list_Makale.setGeometry(QtCore.QRect(110, 250, 810, 571))
        self.list_Makale.setObjectName("list_Makale")
        self.list_Alinti = QtWidgets.QListWidget(self.centralwidget)
        self.list_Alinti.setGeometry(QtCore.QRect(940, 250, 100, 571))
        self.list_Alinti.setObjectName("list_Alinti")
        self.list_Yil = QtWidgets.QListWidget(self.centralwidget)
        self.list_Yil.setGeometry(QtCore.QRect(1060, 250, 100, 571))
        self.list_Yil.setObjectName("list_Yil")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1210, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAra = QtWidgets.QAction(MainWindow)
        self.actionAra.setObjectName("actionAra")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(900, 200, 66, 17))
        self.label.setText("-")
        self.label.setObjectName("label")
        self.lbl_foto = QtWidgets.QLabel(self.centralwidget)
        self.lbl_foto.setGeometry(QtCore.QRect(110, 20, 131, 141))
        self.lbl_foto.setText("")
        self.lbl_foto.setObjectName("lbl_foto")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Google Scholar"))
        self.actionAra.setText(_translate("MainWindow", "ara"))
        self.actionAra.setShortcut(_translate("MainWindow", "T"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

