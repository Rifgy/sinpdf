import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox

from sqlalchemy import create_engine, Column, Integer, String, Sequence, TEXT, DateTime
from sqlalchemy.orm import sessionmaker, registry

BASE_NAME='results.db'

reg = registry()
# declarative base class
Base = reg.generate_base()

# Определяем модель книги
class ResultBase(Base):
    __tablename__ = 'results'
    id = Column(Integer, Sequence('result_id_seq'), primary_key=True)
    hoctname = Column(String(30))
    fullpath = Column(String(255))
    pagecount = Column(Integer)
    doctext = Column(TEXT)
    creationdate = Column(DateTime)
    moddate = Column(DateTime)
    creator = Column(String(50))
    producer = Column(String(50))
    author = Column(String(50))

'''
file_metadata = {
    'ModDate': "D:20240209071733+03'00'",
    'Producer': 'Aspose.Words for .NET 19.3',
    'Author': 'Ларцева Галина Павловна',
    'Creator': 'Microsoft Office Word',
    'CreationDate': 'D:20240117010500Z'
}
'''

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
        #set font
        self.setFont(QFont('SansSerif',12))
        # Создаем элементы интерфейса
        self.path_to_scan = QtWidgets.QLineEdit(self)
        self.path_to_scan.setPlaceholderText('Path to scan')
        self.text_to_search = QtWidgets.QLineEdit(self)
        self.text_to_search.setPlaceholderText('Text to search')

        self.get_path_button = QtWidgets.QPushButton('...', self)
        self.get_path_button.setToolTip('Select path to scan')
        self.get_path_button.clicked.connect(self.add_book)

        self.results_list = QtWidgets.QListWidget(self)

        # Устанавливаем компоновку
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.path_to_scan)
        layout.addWidget(self.text_to_search)
        layout.addWidget(self.get_path_button)
        layout.addWidget(self.results_list)

        self.setLayout(layout)

        self.resize(700,400)
        self.to_center()

        self.load_books()

    def to_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def load_books(self):
        self.results_list.clear()
        list = session.query(ResultBase).all()
        for item in list:
            self.results_list.addItem(f"{item.doctext} by {item.author}")

    def add_book(self):
        title = self.path_to_scan.text()
        author = self.text_to_search.text()

        if title and author:
            new_book = ResultBase(doctext=title, author=author)
            session.add(new_book)
            session.commit()
            self.load_books()
            self.path_to_scan.clear()
            self.text_to_search.clear()
        else:
            QMessageBox.warning(self, 'Input Error', 'Please enter both title and author!')

# Запуск приложения
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = SinPdfApp()

    ex.show()
    sys.exit(app.exec_())