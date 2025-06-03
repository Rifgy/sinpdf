import sys
from datetime import datetime as dt

from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QDesktopWidget, QMessageBox, QProgressDialog,
                             QStatusBar, QLineEdit, QPushButton, QListWidget)

from sqlalchemy import create_engine, Column, Integer, String, Sequence, TEXT
from sqlalchemy.orm import sessionmaker, registry

from sinpdf.functions import get_local_hostname, get_pdf_meta, get_pdf_text, open_file_with_default
from sinpdf.config import APP_FONT, APP_FONTSIZE, BASE_NAME, BASE_PATH, LIMIT_TO_SCAN_PAGE, GET_META_FROM_PDF
from sinpdf.resource import MSG

#debug: Module pdfminer errors
import logging
logging.getLogger('pdfminer').setLevel(logging.ERROR)

__version__ = "0.0.1"

reg = registry()
# declarative base class
Base = reg.generate_base()

# Определяем модель книги
class ResultBase(Base):
    __tablename__ = 'results'
    id = Column(Integer, Sequence('result_id_seq'), primary_key=True)
    hostname = Column(String(30))
    docname = Column(String(255))
    uripath = Column(String(255))
    fullpath = Column(String(255))
    pagecount = Column(Integer)
    doctext = Column(TEXT)
    creationdate = Column(String(30))
    moddate = Column(String(30))
    creator = Column(String(50))
    producer = Column(String(50))
    author = Column(String(50))

# Create SQLite bd
#engine = create_engine("sqlite:///относительный_путь/database")
#engine = create_engine("sqlite:////абсолютный_путь/database")
db_url = 'sqlite:///'+BASE_PATH+BASE_NAME
engine = create_engine(db_url)
Base.metadata.create_all(engine)

# Create session
Session = sessionmaker(bind=engine)
session = Session()

# App main class
class SinPdfApp(QtWidgets.QWidget): #
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Search in PDF')
        self.setMinimumSize(500,200)

        # create status bar
        self.status_bar = QStatusBar()

        # create UI elements
        self.path_to_scan = QLineEdit(self)
        self.path_to_scan.setPlaceholderText('Path to scan')

        self.text_to_search = QLineEdit(self)
        self.text_to_search.setPlaceholderText('Text to search')
        self.text_to_search.textChanged.connect(self.on_search_text_chandge)
        self.text_to_search.returnPressed.connect(self.on_search_enter)

        self.get_path_button = QtWidgets.QPushButton('...', self)
        self.get_path_button.setToolTip('Select path to scan')
        self.get_path_button.resize(self.get_path_button.sizeHint())
        self.get_path_button.clicked.connect(self.get_files_from_path)

        self.get_help = QtWidgets.QPushButton('?', self)
        self.get_help.setToolTip('About...')
        self.get_help.resize(self.get_help.sizeHint())
        self.get_help.clicked.connect(self.on_get_help_click)

        self.results_list = QtWidgets.QListWidget(self)
        self.results_list.setToolTip('Double click to open file')
        self.results_list.doubleClicked.connect(self.on_resultitem_doubleclick)
        self.results_list.keyPressEvent = self.results_list_keyPressEvent

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
        vlay.addWidget(self.status_bar)  # Добавляем статус-бар в макет
        self.setLayout(vlay)
        # set tab ordering
        self.setTabOrder(self.path_to_scan, self.get_path_button)
        self.setTabOrder(self.get_path_button, self.text_to_search)
        self.setTabOrder(self.text_to_search,self.results_list)

        # resize, move form to center, and load data from db to results_list
        self.resize(700,400)
        self.to_center()
        self.load_last_result('')

    def to_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_get_help_click(self):
        now = dt.now()
        QMessageBox.about(self, 'SinPdf about', MSG['about'].format(version=__version__, year=now.year))

    def results_list_keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.on_resultitem_doubleclick()  # Вызываем метод для обработки двойного клика
        else:
            #self.keyPressEvent(event)  # Обрабатываем другие нажатия клавиш super().
            QtWidgets.QListWidget.keyPressEvent(self.results_list, event)

    def on_resultitem_doubleclick(self):
        doc = self.results_list.currentItem().text()
        res = session.query(ResultBase).filter(ResultBase.docname == doc).first()
        open_file_with_default(str(res.fullpath))

    def on_search_text_chandge(self):
        search_str = self.text_to_search.text()
        self.load_last_result(search_str)

    def on_search_enter(self):
        search_str = self.text_to_search.text()
        print(self.text_to_search.text())
        self.load_last_result(search_str)

    def load_last_result(self, search_filter):
        self.results_list.clear()
        if search_filter:
            list_result = session.query(ResultBase).filter(ResultBase.doctext.like(f"%{search_filter}%")).all()
        else:
            list_result = session.query(ResultBase).all()
        for item in list_result:
            self.results_list.addItem(f"{item.docname}")

        # Обновляем статус-бар с количеством найденных результатов
        self.update_status_bar(len(list_result))

    def update_status_bar(self, count):
        if count == 0:
            self.status_bar.showMessage("No results found.")
        else:
            self.status_bar.showMessage(f"{count} result(s) found.")

    def get_files_from_path(self):
        self.path_to_scan.clear()
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select folder to find PDF files", None, QtWidgets.QFileDialog.ShowDirsOnly
        )

        if directory:
            self.path_to_scan.setText(directory)
            self.path_to_scan.setCursorPosition(0)
            host_name = get_local_hostname()

            target_dir = Path(directory)
            pdf_files = list(target_dir.rglob('*.pdf'))  # Получаем список всех PDF-файлов

            # Создаем и настраиваем QProgressDialog
            progress_dialog = QProgressDialog("Processing files...", "Cancel", 0, len(pdf_files), self)
            progress_dialog.setWindowTitle("File Processing")
            progress_dialog.setModal(True)
            progress_dialog.setValue(0)

            for index, entry in enumerate(pdf_files):
                if progress_dialog.wasCanceled():
                    break  # Если пользователь отменил, выходим из цикла
                text = get_pdf_text(entry, LIMIT_TO_SCAN_PAGE)
                meta = get_pdf_meta(entry, GET_META_FROM_PDF)
                new_result = ResultBase(
                    hostname=host_name,
                    docname=entry.name,
                    uripath=entry.as_uri(),
                    fullpath=entry.as_posix(),
                    pagecount=meta['PageCount'],
                    doctext=text,
                    creationdate=meta['CreationDate'],
                    moddate=meta['ModDate'],
                    creator=meta['Creator'],
                    producer=meta['Producer'],
                    author=meta['Author']
                )
                session.add(new_result)
                session.commit()
                # Обновляем прогресс
                progress_dialog.setValue(index + 1)

            progress_dialog.close()  # Закрываем диалог после завершения обработки
            self.load_last_result('')
        else:
            QMessageBox.warning(self, 'Select folder error', 'Please select directory with files')

# start app
if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        # set font for all app widget
        app.setFont(QFont(APP_FONT, APP_FONTSIZE))
        ex = SinPdfApp()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)