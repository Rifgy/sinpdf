import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox

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

        self.get_path_button = QtWidgets.QPushButton('Get path to scan', self)
        #self.add_button.clicked.connect(self.add_book)

        self.books_list = QtWidgets.QListWidget(self)

        # Устанавливаем компоновку
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.path_to_scan)
        layout.addWidget(self.text_to_search)
        layout.addWidget(self.get_path_button)
        layout.addWidget(self.books_list)

        self.setLayout(layout)

        self.resize(700,400)
        self.to_center()

        #load db to list
        #self.load_books()

    def to_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    '''
    def load_books(self):
        self.books_list.clear()
        books = session.query(Book).all()
        for book in books:
            self.books_list.addItem(f"{book.title} by {book.author}")

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()

        if title and author:
            new_book = Book(title=title, author=author)
            session.add(new_book)
            session.commit()
            self.load_books()
            self.title_input.clear()
            self.author_input.clear()
        else:
            QMessageBox.warning(self, 'Input Error', 'Please enter both title and author!')
    '''

# Запуск приложения
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = SinPdfApp()

    ex.show()
    sys.exit(app.exec_())