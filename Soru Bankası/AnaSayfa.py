import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget
)
from SoruEkle import SoruEkleSayfasi
from Yazdirma import YazdirSayfasi



class AnaSayfa(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        baslik = QLabel("Soru Bankasi Uygulamasi")
        baslik.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(baslik)

        btn_soru_ekle = QPushButton("Yeni Soru Ekle")
        btn_soru_ekle.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(btn_soru_ekle)


        btn_soru_yazdir = QPushButton("Soru Sec ve Yazdir")
        btn_soru_yazdir.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        layout.addWidget(btn_soru_yazdir)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    stacked_widget = QStackedWidget()
    anasayfa = AnaSayfa(stacked_widget)
    sayfa2 = SoruEkleSayfasi(stacked_widget)
    sayfa3 = YazdirSayfasi(stacked_widget)

    stacked_widget.addWidget(anasayfa)  
    stacked_widget.addWidget(sayfa2)    
    stacked_widget.addWidget(sayfa3)    

    
    stacked_widget.setWindowTitle("Soru Bankasi")
    stacked_widget.show()

    sys.exit(app.exec_())