from PyQt4 import QtGui
import sys
import re
import design
import stegano
import functions
import shutil
from video_reader import Video
from txt_reader import Textfile

class ExampleApp(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.btnBrowse.clicked.connect(self.browse_videos)
        self.pushButton_2.clicked.connect(self.start_encoding)
        self.pushButton.clicked.connect(self.browse_txt)
        self.pushButton_3.clicked.connect(self.browse_videos_decode)
        self.pushButton_4.clicked.connect(self.start_decoding)
        self.msgBox = QtGui.QMessageBox()
        self.msgBox.setText('Pojemnosc wybranego pliku multimedialnego jest zbyt mala.\nWybierz inny plik lub zmniejsz ilosc danych do ukrycia.')
        self.msgBox.setWindowTitle('Komunikat')
        self.msgBox.addButton(QtGui.QPushButton('OK'), QtGui.QMessageBox.YesRole)
        self.msgBox2 = QtGui.QMessageBox()
        self.msgBox2.setText('Cos poszlo nie tak.\nNajprawdopodobniej nie wybrano pliku multimedialnego lub tekstowego')
        self.msgBox2.setWindowTitle('Komunikat')
        self.msgBox2.addButton(QtGui.QPushButton('OK'), QtGui.QMessageBox.YesRole)
        self.msgBox3 = QtGui.QMessageBox()
        self.msgBox3.setText('Nie wybrano trybu')
        self.msgBox3.setWindowTitle('Komunikat')
        self.msgBox3.addButton(QtGui.QPushButton('OK'), QtGui.QMessageBox.YesRole)
        self.msgBox4 = QtGui.QMessageBox()
        self.msgBox4.setText('Cos poszlo nie tak. Najprawdopodobniej nie wybrano pliku z ktorego bedzie dekodowana wiadomosc.')
        self.msgBox4.setWindowTitle('Komunikat')
        self.msgBox4.addButton(QtGui.QPushButton('OK'), QtGui.QMessageBox.YesRole)
        self.msgBox5 = QtGui.QMessageBox()
        self.msgBox5.setText('Operacja zakonczona sukcesem.')
        self.msgBox5.setWindowTitle('Komunikat')
        self.msgBox5.addButton(QtGui.QPushButton('OK'), QtGui.QMessageBox.YesRole)
        #ret = msgBox.exec_()

    def browse_videos(self):
        global vid
        vid = QtGui.QFileDialog.getOpenFileName(self, "Wybierz plik multimedialny")
        print vid
        if vid:
            self.btnBrowse.setText(re.search(r'[^/]+$', vid).group(0))

    def browse_videos_decode(self):
        global decode_vid
        decode_vid = QtGui.QFileDialog.getOpenFileName(self, "Wybierz plik multimedialny")
        #print decode_vid
        if decode_vid:
            self.pushButton_3.setText(re.search(r'[^/]+$', decode_vid).group(0))

    def browse_txt(self):
        global txt
        txt = QtGui.QFileDialog.getOpenFileName(self, "Wybierz plik tekstowy", selectedFilter='*.txt')
        #print txt

        if txt:
            self.pushButton.setText(re.search(r'[^/]+$', txt).group(0))

    def start_encoding(self):
        seed = None
        mode = None
        if self.radioButton.isChecked():
            #print 'standard'
            mode = 's'
        elif self.radioButton_2.isChecked():
            #print 'deterministic'
            mode = 'd'
        elif self.radioButton_4.isChecked():
            #print 'nondeterministic'
            mode = 'n'
            seed = int(self.lineEdit.displayText())
            #print seed #self.lineEdit.displayText()

        if mode:
            try:
                print txt
                message = Textfile(txt)
                print str(vid)
                video = Video(str(vid))

                randmax = min(functions.rand_max(video.audio_capacity, video.vid_capacity, message.len_bits), video.framesize)

                if mode == 'd' and not functions.det_cap(video.audio_capacity, video.vid_capacity, message.data):
                    self.msgBox.exec_()
                elif randmax < 0:
                    self.msgBox.exec_()
                else:
                    fileName = QtGui.QFileDialog.getSaveFileName(self, 'Zapisz wynikowy plik jako...', selectedFilter='*.mkv')
                    stegano.encode(str(vid), message.data, mode, seed, randmax)

                    functions.make_vid(video.fps, str(fileName))
                    print "zapisz video"
                    # shutil.rmtree('temp')
                    self.msgBox5.exec_()
            except Exception as e:
                print e
                self.msgBox2.exec_()
        else:
            self.msgBox3.exec_()



    def start_decoding(self):
        seed = None
        mode = None
        if self.radioButton_5.isChecked():
            #print 'standard'
            mode = 's'
        elif self.radioButton_6.isChecked():
            #print 'deterministic'
            mode = 'd'
        elif self.radioButton_8.isChecked():
            #print 'nondeterministic'
            mode = 'n'
            seed = int(self.lineEdit_2.displayText())
            #print seed

        if mode:
            global decode_vid
            try:
                txtName = QtGui.QFileDialog.getSaveFileName(self, 'Zdekodowana wiadomosc zapisz jako...', selectedFilter='*.txt')
                s = stegano.decode(str(decode_vid), mode, seed)
                # shutil.rmtree('temp')
                #txtName = QtGui.QFileDialog.getSaveFileName(self, 'Zdekodowana wiadomosc zapisz jako...', selectedFilter='*.txt')
                text_file = open(txtName, "w")
                text_file.write(s)
                text_file.close()
                self.msgBox5.exec_()
            except Exception as e:
                print e
                self.msgBox4.exec_()
        else:
            self.msgBox3.exec_()


def main():
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
