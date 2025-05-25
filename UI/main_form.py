import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox

from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker, registry

BASE_NAME='books.db'

reg = registry()
# declarative base class
Base = reg.generate_base()

# Определяем модель книги
class ResultBase(Base):
    __tablename__ = 'books'
    id = Column(Integer, Sequence('book_id_seq'), primary_key=True)
    title = Column(String(50))
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
        books = session.query(ResultBase).all()
        for book in books:
            self.results_list.addItem(f"{book.title} by {book.author}")

    def add_book(self):
        title = self.path_to_scan.text()
        author = self.text_to_search.text()

        if title and author:
            new_book = ResultBase(title=title, author=author)
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