
import sys
import os
import datetime

from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox, QStatusBar

from sqlalchemy import create_engine, Column, Integer, String, Sequence, TEXT, DateTime
from sqlalchemy.orm import sessionmaker, registry

from resource import MSG

__version__ = "0.1"

BASE_NAME='results.db'

reg = registry()
# declarative base class
Base = reg.generate_base()

# Определяем модель книги
class ResultBase(Base):
    __tablename__ = 'results'
    id = Column(Integer, Sequence('result_id_seq'), primary_key=True)
    hoctname = Column(String(30))
    docname = Column(String(255))
    fullpath = Column(String(255))
    pagecount = Column(Integer)
    doctext = Column(TEXT)
    creationdate = Column(DateTime)
    moddate = Column(DateTime)
    creator = Column(String(50))
    producer = Column(String(50))
    author = Column(String(50))

# Создаем базу данных SQLite
engine = create_engine('sqlite:///'+BASE_NAME)
Base.metadata.create_all(engine)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# основной класс приложения
class SinPdfApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Search in PDF')
        self.setMinimumSize(500,200)
        # set font
        #self.setFont(QFont('SansSerif',12))
        # create UI elements
        self.path_to_scan = QtWidgets.QLineEdit(self)
        self.path_to_scan.setPlaceholderText('Path to scan')
        self.text_to_search = QtWidgets.QLineEdit(self)
        self.text_to_search.setPlaceholderText('Text to search')
        self.get_path_button = QtWidgets.QPushButton('...', self)
        self.get_path_button.setToolTip('Select path to scan')
        self.get_path_button.resize(self.get_path_button.sizeHint())
        self.get_path_button.clicked.connect(self.get_files_from_path)
        self.get_help = QtWidgets.QPushButton('?', self)
        self.get_help.setToolTip('About...')
        self.get_help.resize(self.get_help.sizeHint())
        self.get_help.clicked.connect(self.get_about)
        self.results_list = QtWidgets.QListWidget(self)

        # Install the layout
        vlay = QtWidgets.QVBoxLayout()
        hlay = QtWidgets.QHBoxLayout()
        hlay1 = QtWidgets.QHBoxLayout()
        hlay.addWidget(self.path_to_scan)
        hlay.addWidget(self.get_path_button)
        hlay1.addWidget(self.text_to_search)
        hlay1.addWidget(self.get_help)
        vlay.addLayout(hlay)
        vlay.addLayout(hlay1)
        vlay.addWidget(self.results_list)
        self.setLayout(vlay)
        # set tab ordering
        self.setTabOrder(self.path_to_scan, self.get_path_button)
        self.setTabOrder(self.get_path_button, self.text_to_search)
        self.setTabOrder(self.text_to_search,self.results_list)

        # resize & move form to center
        self.resize(700,400)
        self.to_center()

        self.load_last_result()

    def to_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_about(self):
        now = datetime.datetime.now()
        QMessageBox.about(self, 'SinPdf about', MSG['about'].format(version=__version__, year=now.year))

    def load_last_result(self):
        self.results_list.clear()
        list = session.query(ResultBase).all()
        for item in list:
            #self.results_list.addItem(f"{item.doctext} by {item.author}")
            self.results_list.addItem((f"{item.hoctname} : {item.fullpath}"))

    def get_files_from_path(self):
        '''
        # очистить, если в списке уже есть элементы
        self.listWidget.clear()
        self.txtSource.clear()
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, MSG['selectFolder'])
        self.txtSource.setText(directory)
        self.txtSource.setCursorPosition(0)
        # диалог выбора директории -> установить значение переменной
        # в путь выбранной директории
        # не продолжать выполнение, если пользователь не выбрал директорию
        if directory:
            # для каждого файла в директории
            for file_name in os.listdir(directory):
                # добавить файл в dirListWidget
                self.listWidget.addItem(file_name)
        '''
        host_name = self.path_to_scan.text()
        full_path = self.text_to_search.text()
        if host_name and full_path:
            new_result = ResultBase(hoctname=host_name, fullpath=full_path)
            session.add(new_result)
            session.commit()
            self.load_last_result()
            self.path_to_scan.clear()
            self.text_to_search.clear()
        else:
            QMessageBox.warning(self, 'Input Error', 'Please enter both title and author!')

# start app
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # set font for all app widget
    app.setFont(QFont('SansSerif',12))

    ex = SinPdfApp()
    ex.show()
    sys.exit(app.exec_())