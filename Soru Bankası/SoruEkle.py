from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
)
import openpyxl
import os

class SoruEkleSayfasi(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()
        self.sorular = []  

    def init_ui(self):
        layout = QVBoxLayout()

        # Soru girişi
        self.soru_input = QLineEdit()
        self.soru_input.setPlaceholderText("Soru metni")
        layout.addWidget(self.soru_input)

        # Şıklar
        self.siklar = []
        for harf in ["A", "B", "C", "D", "E"]:
            line = QLineEdit()
            line.setPlaceholderText(f"{harf} cevabi")
            self.siklar.append(line)
            layout.addWidget(line)

        # Doğru şık seçimi
        self.dogru_sik_combo = QComboBox()
        self.dogru_sik_combo.addItems(["A", "B", "C", "D", "E"])
        layout.addWidget(QLabel("Dogru cevap:"))
        layout.addWidget(self.dogru_sik_combo)

        # Ekle ve Kaydet butonları
        btn_ekle = QPushButton("Soru Ekle")
        btn_ekle.clicked.connect(self.soru_ekle)
        layout.addWidget(btn_ekle)

        btn_kaydet = QPushButton("Excel'e Kaydet")
        btn_kaydet.clicked.connect(self.excele_kaydet)
        layout.addWidget(btn_kaydet)

        # Soru tablosu
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(7)
        self.tablo.setHorizontalHeaderLabels(["Soru", "A", "B", "C", "D", "E", "Doru"])
        layout.addWidget(self.tablo)

        self.setLayout(layout)

    def soru_ekle(self):
        soru = self.soru_input.text()
        siklar = [sik.text() for sik in self.siklar]
        dogru = self.dogru_sik_combo.currentText()

        if not soru or any(not s for s in siklar):
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanlari doldurun.")
            return

        yeni_soru = [soru] + siklar + [dogru]
        self.sorular.append(yeni_soru)

        # Tabloya ekle
        row = self.tablo.rowCount()
        self.tablo.insertRow(row)
        for i, veri in enumerate(yeni_soru):
            self.tablo.setItem(row, i, QTableWidgetItem(veri))

        # Alanları temizle
        self.soru_input.clear()
        for s in self.siklar:
            s.clear()

    def excele_kaydet(self):
        dosya_adi = "soru_bankasi.xlsx"

        # Dosya yoksa oluştur
        if not os.path.exists(dosya_adi):
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(["Soru", "A", "B", "C", "D", "E", "Doru"])
        else:
            wb = openpyxl.load_workbook(dosya_adi)
            ws = wb.active

        # Eklenen her soruyu yaz
        for soru in self.sorular:
            ws.append(soru)

        wb.save(dosya_adi)
        QMessageBox.information(self, "Basarili", "Sorular Excel dosyasina kaydedildi.")
        self.sorular.clear()
        self.tablo.setRowCount(0)