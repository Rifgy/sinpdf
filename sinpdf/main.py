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
logging.getLogger('SinPdfApp').setLevel(logging.DEBUG)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("sinpdf.log",'w','utf-8'),
        logging.StreamHandler()
    ]
)

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
        self.text_to_search.textChanged.connect(self.on_search_text_change)
        self.text_to_search.returnPressed.connect(self.on_search_enter)

        self.get_path_button = QPushButton('...', self)
        self.get_path_button.setToolTip('Select path to scan')
        self.get_path_button.resize(self.get_path_button.sizeHint())
        self.get_path_button.clicked.connect(self.get_files_from_path)

        self.get_help = QPushButton('?', self)
        self.get_help.setToolTip('About...')
        self.get_help.resize(self.get_help.sizeHint())
        self.get_help.clicked.connect(self.on_get_help_click)

        self.results_list = QListWidget(self)
        self.results_list.setToolTip('Double click to open file')
        self.results_list.doubleClicked.connect(self.on_result_item_doubleclick)
        self.results_list.keyPressEvent = self.on_results_list_keypress_event

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

    def to_center(self) -> None:
        """
        Set main form to center user desktop

        :rtype: None
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_get_help_click(self) -> None:
        """
        Processing the click on get_help button

        :rtype: None
        """
        now = dt.now()
        QMessageBox.about(self, 'SinPdf about', MSG['about'].format(version=__version__, year=now.year))
        logging.info('Help information displayed.')

    def on_results_list_keypress_event(self, event) -> None:
        """
        Processing the key pressed on item in results_list

        :param event:
        :rtype: None
        """
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.on_result_item_doubleclick()  # Вызываем метод для обработки двойного клика
        else:
            #self.keyPressEvent(event)  # Обрабатываем другие нажатия клавиш super().
            QtWidgets.QListWidget.keyPressEvent(self.results_list, event)

    def on_result_item_doubleclick(self) -> None:
        """
        Processing the double click on item in results_list

        :rtype: None
        """
        doc = self.results_list.currentItem().text()
        with sessionmaker(bind=engine)() as session:
            res = session.query(ResultBase).filter(ResultBase.docname == doc).first()
            if res:
                open_file_with_default(str(res.fullpath))
                logging.info(f'Opened file: {res.fullpath}')
            else:
                logging.warning(f'File not found in database: {doc}')

    def on_search_text_change(self) -> None:
        """
        Processing the change text in text_to_search

        :rtype: None
        """
        search_str = self.text_to_search.text()
        self.load_last_result(search_str)
        #ogging.debug(f'Search text changed to: {search_str}')

    def on_search_enter(self) -> None:
        """
        Processing the Enter key pressing event in text_to_search

        :rtype: None
        """
        search_str = self.text_to_search.text()
        self.load_last_result(search_str)
        logging.info(f'Search entered: {search_str}')

    def load_last_result(self, search_filter: str) -> None:
        """
        Load item's to results_list from Base with filter

        :param search_filter: string from text_to_search or ''
        :rtype: None
        """
        self.results_list.clear()
        with sessionmaker(bind=engine)() as session:
            if search_filter:
                list_result = session.query(ResultBase).filter(ResultBase.doctext.like(f"%{search_filter}%")).all()
            else:
                list_result = session.query(ResultBase).all()
            for item in list_result:
                self.results_list.addItem(f"{item.docname}")
            # status bar update
            text = "No results found." if len(list_result) == 0 else f"{len(list_result)} result(s) found."
            self.update_status_bar(text)
            logging.debug(f'Loaded {len(list_result)} results for search filter: {search_filter}')

    def update_status_bar(self, text_to_status: str) -> None:
        """
        Update status bar message fron text_to_status

        :param text_to_status:
        :rtype: None
        """
        self.status_bar.showMessage(text_to_status)

    def get_files_from_path(self):
        self.path_to_scan.clear()
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Select folder to find PDF files",
            None,
            QtWidgets.QFileDialog.ShowDirsOnly
        )

        if directory:
            self.path_to_scan.setText(directory)
            self.path_to_scan.setCursorPosition(0)

            host_name = get_local_hostname()
            logging.info(f'Selected directory: {directory}')

            target_dir = Path(directory)

            self.update_status_bar(f'Scan all PDF file\'s in {directory}')

            # get list ALL pdf-files in select dir
            pdf_files = list(target_dir.rglob('*.pdf'))

            # create add set QProgressDialog
            progress_dialog = QProgressDialog("Processing files...", "Cancel", 0, len(pdf_files), self)
            progress_dialog.setWindowTitle("File Processing")
            progress_dialog.setModal(True)
            progress_dialog.setValue(0)

            with sessionmaker(bind=engine)() as session:
                for index, entry in enumerate(pdf_files):
                    if progress_dialog.wasCanceled():
                        break  # Если пользователь отменил, выходим из цикла
                    try:
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
                        logging.info(f'Processed file: {entry}')
                    except (IOError, ValueError) as e:
                        logging.error(f"Error processing file {entry}: {e}")
                        self.status_bar.showMessage(f"Error processing file {entry.name}: {e}")
                        continue
                    # progress bar update
                    progress_dialog.setValue(index + 1)
            progress_dialog.close()  # Закрываем диалог после завершения обработки
            self.load_last_result('')
            logging.info('File processing completed.')
        else:
            QMessageBox.warning(self, 'Select folder error', 'Please select directory with files')
            logging.warning('No directory selected for file processing.')


# start app
if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        app.setFont(QFont(APP_FONT, APP_FONTSIZE))
        ex = SinPdfApp()
        ex.show()
        logging.info('Application started.')
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f'Exception occurred: {e}')