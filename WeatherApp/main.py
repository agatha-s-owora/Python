from logic import *

def main():
    app = QApplication([])
    main_window = Logic()
    main_window.show()
    app.exec()

if __name__ == '__main__':
    main()
