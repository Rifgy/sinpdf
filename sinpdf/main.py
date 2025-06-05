import sys
from datetime import datetime as dt

from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QDesktopWidget, QMessageBox, QProgressDialog, QComboBox,
                             QStatusBar, QLineEdit, QPushButton, QListWidget)

from sqlalchemy import create_engine, Column, Integer, String, Sequence, TEXT
from sqlalchemy.orm import sessionmaker, registry

from sinpdf.functions import get_local_hostname, get_pdf_meta, get_pdf_text, open_file_with_default
from sinpdf.config import ConfigReader
from sinpdf.resource import MessA

__version__ = "0.0.4"

config_reader = ConfigReader('config.ini')
APP_FONT = config_reader.get('Default', 'FontName')
APP_FONTSIZE = config_reader.get_int('Default', 'FontSize')
BASE_NAME = config_reader.get('ScanOpt', 'BaseName')
BASE_PATH = config_reader.get('ScanOpt', 'BasePath')
LIMIT_TO_SCAN_PAGE = config_reader.get_int('ScanOpt', 'LimitToScanPages')
GET_META_FROM_PDF = config_reader.get_bool('ScanOpt', 'GetMetaFromPdf')
DB_LIST = config_reader.get_dict('BaseFile')

#debug: Module pdfminer errors
import logging

logging.getLogger('pdfminer').setLevel(logging.ERROR)
logging.getLogger(__name__).setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.WARNING,
    format='%(name)s %(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(f"sinpdf.log",'w','utf-8'),
        logging.StreamHandler()
    ]
)

mess = MessA()

reg = registry()
# declarative base class
Base = reg.generate_base()

# determine the model of the result base
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
        self.setWindowTitle(mess.WindowTitle)
        self.setMinimumSize(500,200)

        self.status_bar = QStatusBar()

        self.path_to_scan = QLineEdit(self)
        self.path_to_scan.setPlaceholderText(mess.PathToScanPlaceholderText)

        self.text_to_search = QLineEdit(self)
        self.text_to_search.setPlaceholderText(mess.TextToSearchPlaceholderText)
        self.text_to_search.textChanged.connect(self.on_search_text_change)
        self.text_to_search.returnPressed.connect(self.on_search_enter)

        self.get_path_button = QPushButton(mess.GetPathButtonText, self)
        self.get_path_button.setToolTip(mess.GetPathButtonToolTip)
        self.get_path_button.resize(self.get_path_button.sizeHint())
        self.get_path_button.clicked.connect(self.get_files_from_path)

        self.get_help = QPushButton(mess.GetHelpText, self)
        self.get_help.setToolTip(mess.GetHelpToolTip)
        self.get_help.resize(self.get_help.sizeHint())
        self.get_help.clicked.connect(self.on_get_help_click)

        self.get_base = QComboBox()
        for key, value in DB_LIST.items():
            self.get_base.addItem(value, key)
        self.get_base.currentIndexChanged.connect(self.on_get_base_changed)

        self.results_list = QListWidget(self)
        self.results_list.setToolTip(mess.ResultsListSetToolTip)
        self.results_list.doubleClicked.connect(self.on_result_item_doubleclick)
        self.results_list.keyPressEvent = self.on_results_list_keypress_event

        # Install the layout
        vlay = QtWidgets.QVBoxLayout()
        vlay0 = QtWidgets.QVBoxLayout()
        vlay1 = QtWidgets.QVBoxLayout()

        vlay0.addWidget(self.path_to_scan)
        vlay0.addWidget(self.cmb_get_base)
        vlay0.addWidget(self.text_to_search)
        vlay1.addWidget(self.get_path_button)
        vlay1.addWidget(self.chk_new_base)
        vlay1.addWidget(self.get_help)

        hlay = QtWidgets.QHBoxLayout()
        hlay.addLayout(vlay0)
        hlay.addLayout(vlay1)

        vlay.addLayout(hlay)
        vlay.addWidget(self.get_base)
        vlay.addLayout(hlay1)
        vlay.addWidget(self.results_list)
        vlay.addWidget(self.status_bar)  # Добавляем статус-бар в макет
        self.setLayout(vlay)
        # set tab ordering
        self.setTabOrder(self.path_to_scan, self.get_path_button)
        self.setTabOrder(self.get_path_button, self.cmb_get_base)
        self.setTabOrder(self.cmb_get_base,self.chk_new_base)
        self.setTabOrder(self.chk_new_base, self.text_to_search)
        self.setTabOrder(self.text_to_search, self.get_help)
        self.setTabOrder(self.get_help,self.results_list)


        # resize, move form to center, and load data from db to results_list
        self.resize(900,500)
        self.to_center()
        self.load_last_result('')
        self.on_get_base_changed(0)

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
        QMessageBox.about(self, mess.MsgBoxAbout, mess.About.format(version=__version__, year=now.year))

    def on_results_list_keypress_event(self, event) -> None:
        """
        Processing the key pressed on item in results_list

        :param event:
        :rtype: None
        """
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.on_result_item_doubleclick()  # Вызываем метод для обработки двойного клика
        else:
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
            else:
                logging.warning(f'File not found in database: {doc}')

    def on_search_text_change(self) -> None:
        """
        Processing the change text in text_to_search

        :rtype: None
        """
        search_str = self.text_to_search.text()
        self.load_last_result(search_str)


    def on_get_base_changed(self, index):
        selected_value = self.get_base.currentText()
        selected_key = self.get_base.itemData(index)
        self.update_status_bar(f"Select: {selected_value} (Key: {selected_key})")

    def on_search_enter(self) -> None:
        """
        Processing the Enter key pressing event in text_to_search

        :rtype: None
        """
        search_str = self.text_to_search.text()
        self.load_last_result(search_str)

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
            mess.FileDlgText,
            None,
            QtWidgets.QFileDialog.ShowDirsOnly
        )

        if directory:
            self.update_status_bar(f'{mess.StatusScanFileInDir} {directory}')
            self.path_to_scan.setText(directory)
            self.path_to_scan.setCursorPosition(0)

            host_name = get_local_hostname()

            target_dir = Path(directory)

            # get list ALL pdf-files in select dir
            pdf_files = list(target_dir.rglob('*.pdf'))

            # create add set QProgressDialog
            progress_dialog = QProgressDialog(mess.ProcDlgText, mess.ProcDlgBtnText, 0, len(pdf_files), self)
            progress_dialog.setWindowTitle(mess.ProcDlgWinTitle)
            progress_dialog.setModal(True)
            progress_dialog.setValue(0)

            with sessionmaker(bind=engine)() as session:
                for index, entry in enumerate(pdf_files):
                    if progress_dialog.wasCanceled():
                        break
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
        else:
            QMessageBox.warning(self, mess.MsgBoxWarnTitle, mess.MsgBoxWarnText)
            logging.warning('No directory selected for file processing.')


# start app
if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        app.setFont(QFont(APP_FONT, APP_FONTSIZE))
        ex = SinPdfApp()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f'Exception occurred: {e}')