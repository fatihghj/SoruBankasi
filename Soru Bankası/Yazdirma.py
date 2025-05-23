from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
)
import pandas as pd
from fpdf import FPDF
import os

class YazdirSayfasi(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        baslik = QLabel("Soru Bankasını PDF Olarak Yazdır")
        baslik.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(baslik)

        self.tablo = QTableWidget()
        layout.addWidget(self.tablo)

        btn_yukle = QPushButton("Soruları Yükle")
        btn_yukle.clicked.connect(self.sorulari_yukle)
        layout.addWidget(btn_yukle)


        btn_yazdir = QPushButton("PDF Olarak Yazdır")
        btn_yazdir.clicked.connect(self.pdf_olustur)
        layout.addWidget(btn_yazdir)

        self.setLayout(layout)
    
    def sorulari_yukle(self):
        try:
            df = pd.read_excel("soru_bankasi.xlsx")
            self.tablo.setColumnCount(len(df.columns))
            self.tablo.setRowCount(len(df))
            self.tablo.setHorizontalHeaderLabels(df.columns.tolist())
            for i in range(len(df)):
                for j in range(len(df.columns)):
                    self.tablo.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Sorular yüklenemedi:\n{str(e)}")
    

    def pdf_olustur(self):
        excel_dosya = "soru_bankasi.xlsx"

        if not os.path.exists(excel_dosya):
            QMessageBox.warning(self, "Hata", "soru_bankasi.xlsx bulunamadi!")
            return

        try:
            df = pd.read_excel(excel_dosya)

            # Gerekli sütunlar
            gerekli = ["Soru", "A", "B", "C", "D", "E", "Doru"]
            for sutun in gerekli:
                if sutun not in df.columns:
                    QMessageBox.critical(self, "Hata", f"Excel'de '{sutun}' sutunu bulunamadi!")
                    return

            if df.empty:
                QMessageBox.warning(self, "Bos", "Excel dosyasinda hic soru yok.")
                return

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            for index, row in df.iterrows():
                pdf.multi_cell(0, 10, f"Soru {index+1}: {row['Soru']}")
                for harf in ['A', 'B', 'C', 'D', 'E']:
                    pdf.multi_cell(0, 10, f"{harf}) {row[harf]}")
                pdf.multi_cell(0, 10, f"Doru Cevap: {row['Doru']}")
                pdf.cell(0, 10, "-"*50, ln=True)

            pdf.output("soru_yazdir.pdf")
            QMessageBox.information(self, "Basarili", "PDF olusturuldu: soru_yazdir.pdf")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"PDF olusturulamadi:\n{str(e)}")