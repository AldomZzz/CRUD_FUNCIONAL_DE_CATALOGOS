import sys
import mysql.connector
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                            QPushButton, QMessageBox, QDialog)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="oxxo_db",
    port=3306
)
cursor = conn.cursor()

class ConsultaWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consulta de Categorías - oxxo")
        self.setGeometry(150, 150, 400, 300)
        
        self.lbl_titulo = QLabel("LISTADO DE CATEGORÍAS:", self)
        self.lbl_titulo.move(30, 30)
        
        self.lbl_resultados = QLabel(self)
        self.lbl_resultados.move(30, 60)
        self.lbl_resultados.resize(340, 200)

        self.mostrar_categorias()
    
    def mostrar_categorias(self):
        cursor.execute("SELECT * FROM categorias ORDER BY id_categoria")
        categorias = cursor.fetchall()
        
        texto = ""
        for cat in categorias:
            texto += f"ID: {cat[0]} - Nombre: {cat[1]}\n"
        
        self.lbl_resultados.setText(texto)

app = QApplication(sys.argv)
ventana = QWidget()
ventana.setWindowTitle("CRUD Categorías - oxxo")
ventana.setGeometry(100, 100, 400, 250)

lbl_id = QLabel("ID Categoría:", ventana)
lbl_id.move(30, 30)
txt_id = QLineEdit(ventana)
txt_id.move(150, 30)
txt_id.resize(200, 25)

lbl_nombre = QLabel("Nombre:", ventana)
lbl_nombre.move(30, 70)
txt_nombre = QLineEdit(ventana)
txt_nombre.move(150, 70)
txt_nombre.resize(200, 25)

btn_agregar = QPushButton("Agregar", ventana)
btn_agregar.move(30, 130)
btn_actualizar = QPushButton("Actualizar", ventana)
btn_actualizar.move(150, 130)
btn_eliminar = QPushButton("Eliminar", ventana)
btn_eliminar.move(270, 130)
btn_consultar = QPushButton("Consultar", ventana)
btn_consultar.move(30, 180)
btn_consultar.resize(340, 25)

btn_agregar.clicked.connect(lambda: (
    cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (txt_nombre.text(),)),
    conn.commit(),
    QMessageBox.information(ventana, "Éxito", "Categoría agregada."),
    txt_nombre.clear(),
    txt_id.clear()
) if txt_nombre.text() else QMessageBox.warning(ventana, "Error", "El nombre no puede estar vacío."))

btn_actualizar.clicked.connect(lambda: (
    cursor.execute("UPDATE categorias SET nombre = %s WHERE id_categoria = %s", (txt_nombre.text(), txt_id.text())),
    conn.commit(),
    QMessageBox.information(ventana, "Éxito", "Categoría actualizada.")
) if txt_nombre.text() and txt_id.text() else QMessageBox.warning(ventana, "Error", "Completa ambos campos para actualizar."))

btn_eliminar.clicked.connect(lambda: (
    cursor.execute("DELETE FROM categorias WHERE id_categoria = %s", (txt_id.text(),)),
    conn.commit(),
    QMessageBox.information(ventana, "Éxito", "Categoría eliminada."),
    txt_nombre.clear(),
    txt_id.clear()
) if txt_id.text() else QMessageBox.warning(ventana, "Error", "Escribe el ID a eliminar."))

btn_consultar.clicked.connect(lambda: ConsultaWindow().exec())

ventana.show()
sys.exit(app.exec())