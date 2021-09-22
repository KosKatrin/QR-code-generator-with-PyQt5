import qrcode
import re
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QStatusBar, \
    QVBoxLayout, QHBoxLayout, QFrame, QSplitter, QPushButton
from PyQt5.QtGui import QPalette, QColor, QFont, QPixmap
from PIL.ImageQt import ImageQt

class MainWindow(QMainWindow, QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        widget = QWidget()
        self.setCentralWidget(widget)
        font = QFont('Open Sans', 16)

        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()

        layout1.setContentsMargins(0, 0, 0, 0)
        layout1.setSpacing(20)

        label = QLabel('Ссылка или текст:')  # Текст рядом со строкой ввода
        label.setFont(font)

        self.textEnter = QLineEdit()  # Строка ввода текста
        self.textEnter.setFont(font)

        self.QRbox = QLabel()
        #self.QRbox.setAlignment(Qt.AlignTop)

        # Выравниваем текст и строку ввода
        layout2.addWidget(label)  # В горизонтальное выравнивание добавляем текст
        layout2.addWidget(self.textEnter)  # В горизонтальное выравнивание добавляем строку ввода
        layout2.addWidget(self.QRbox)

        layout1.addLayout(layout2)  # В вертикальное выравнивание добавляем все горизонтальные элементы

        # Добавляем кнопки
        self.generate_button = QPushButton('Сгенерировать')
        self.generate_button.clicked.connect(self.create_qr_code)

        self.cancel_button = QPushButton('Очистить')
        self.cancel_button.clicked.connect(self.clear_button)

        self.saveimg_button = QPushButton('Скачать QR-код')
        self.saveimg_button.clicked.connect(self.save_code)

        layout3.addWidget(self.generate_button)
        layout3.addWidget(self.cancel_button)
        layout3.addWidget(self.saveimg_button)
        layout1.addLayout(layout3)

        self.statusBar = QStatusBar()
        layout1.addWidget(self.statusBar)

        widget.setLayout(layout1)
        self.setCentralWidget(widget)

    def clear_button(self):
        self.textEnter.clear()
        self.QRbox.clear()
        self.statusBar.clearMessage()  # Очищает статусную строку

    def create_qr_code(self):
        text = self.textEnter.text()
        if text != '':
            img = qrcode.make(text)
            qr = ImageQt(img)
            pixmap = QPixmap.fromImage(qr)
            self.QRbox.setPixmap(pixmap)

    def save_code(self):
        current_dir = os.getcwd()
        file_name = self.textEnter.text()

        if file_name:
            file_name = self.clear_name(file_name)
            self.QRbox.pixmap().save(os.path.join(current_dir, file_name + '.png'))
            self.statusBar.showMessage('QR-код успешно сохранен в {0}'.format
                                           (os.path.join(current_dir, file_name + '.png')))
            # os.path.join - Получение полного абсолютного пути к файлу
            # ShowMessage - Выводит текст в статусную строку


    def clear_name(self, docname,
                       slash_replace='-',
                       # слэш: заменять на минус; используется в идентификаторах документов: типа № 1/2
                       quote_replace='',  # кавычки: замены нет - удаляем
                       multispaces_replace='\x20',  # множественные пробелы на один пробел
                       quotes="""“”«»'\""""  # какие кавычки будут удаляться
                       ):
        docname = re.sub(r'[' + quotes + ']', quote_replace, docname)
        docname = re.sub(r'[/]', slash_replace, docname)
        docname = re.sub(r'[|*?<>:\\\n\r\t\v]', '', docname)  # запрещенные символы в windows
        docname = re.sub(r'\s{2,}', multispaces_replace, docname)
        docname = docname.strip()
        docname = docname.rstrip('-')  # на всякий случай
        docname = docname.rstrip('.')  # точка в конце не разрешена в windows
        docname = docname.strip()  # не разрешен пробел в конце в windows
        return docname


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec_())  # Открываем и закрываем программу