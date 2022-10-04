import sys
import Swaptoken
# pip install pyqt5
from PyQt5.QtWidgets import QApplication, QMainWindow
from output import Ui_MainWindow

class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.uic.Btn_Swap.clicked.connect(self.swapToken)
        self.uic.LD_soluong1.textChanged.connect(self.checkSwap)
        self.uic.LD_addressA.textChanged.connect(self.checkSwap)
        self.uic.LD_addressA_2.textChanged.connect(self.checkSwap)

    def checkSwap(self):
        token_A = self.uic.LD_addressA.text()
        token_B = self.uic.LD_addressA_2.text()
        soluongcanban = (self.uic.LD_soluong1.text())
        try :
            float_scb = float(soluongcanban)
        except Exception as b :
            float_scb = 0.0
            pass
        print(token_A)
        print(token_B)
        print(float_scb,'float_scbfloat_scbfloat_scb')
        if soluongcanban == "" or float_scb == 0:
            self.uic.LD_soluong1_2.setText("0")
        else :
            quoter = Swaptoken.qouter_token(token_A,token_B,float_scb)
            string_quoter = str(quoter)
            self.uic.LD_soluong1_2.setText(string_quoter)

        if (token_A == "") or (token_B =="") or ( soluongcanban == "") :
            print(token_A)
            print(token_B)
            print(soluongcanban)
            self.uic.textEdit.setText('Invalid Value')
        else :
            self.uic.textEdit.setText('')
    def swapToken(self) : 
        token_A = self.uic.LD_addressA.text()
        token_B = self.uic.LD_addressA_2.text()
        soluongcanban = (self.uic.LD_soluong1.text())
        try :
            float_scb = float(soluongcanban)
        except Exception as b :
            float_scb = 0.0
            pass
        print(Swaptoken.checkSoLuongBan(token_A, float_scb))
        if (Swaptoken.checkSoLuongBan(token_A, float_scb) == False) :
            self.uic.textEdit.setText('Insufficient number of transactions')
        else :
            giaodichthanhcong = Swaptoken.sell_pancake(token_A=token_A,token_B=token_B,socanban=float_scb)
            confirm = giaodichthanhcong['confirm']
            hashh = giaodichthanhcong['hash']
            print(confirm)
            print(hashh)
            if confirm == 1 :
                self.uic.textEdit.setText(f'Success Transaction !!!!!! \nTransaction Hash : {hashh}')
            else :
                self.uic.textEdit.setText(f'Fail Transaction !!!!!! \nTransaction Hash : {hashh}')

    def show(self):
        # command to run
        self.main_win.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())