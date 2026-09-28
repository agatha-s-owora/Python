from logic import *

def main():
    app = QApplication([])      # app = QApplication(sys.argv)
    main_window = Logic()
    main_window.setWindowIcon(QIcon("icon.ico"))
    main_window.show()
    app.exec()                  # sys.exit(app.exec())

if __name__ == "__main__":
    main()
