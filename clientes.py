import sys
import mysql.connector
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                            QPushButton, QMessageBox, QDialog, 
                            QVBoxLayout, QScrollArea)
from PyQt6.QtCore import Qt

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="oxxo_db",
    port=3306
)
cursor = conn.cursor()

class ConsultaClientesWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consulta de Clientes - oxxo")
        self.setGeometry(150, 150, 500, 400)
        
        layout = QVBoxLayout()
        
        # Título
        lbl_titulo = QLabel("LISTADO DE CLIENTES:")
        lbl_titulo.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(lbl_titulo)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        self.lbl_resultados = QLabel()
        self.lbl_resultados.setWordWrap(True)
        self.lbl_resultados.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.lbl_resultados.setStyleSheet("font-family: monospace;")
        
        scroll.setWidget(self.lbl_resultados)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
        self.mostrar_clientes()
    
    def mostrar_clientes(self):
        cursor.execute("SELECT * FROM clientes ORDER BY id_cliente")
        clientes = cursor.fetchall()
        
        texto = ""
        for cli in clientes:
            texto += (f"ID: {cli[0]}\n"
                     f"Nombre: {cli[1]}\n"
                     f"Teléfono: {cli[2] or 'No registrado'}\n"
                     f"Email: {cli[3] or 'No registrado'}\n"
                     f"Puntos: {cli[4]}\n"
                     "------------------------\n")
        
        self.lbl_resultados.setText(texto)

app = QApplication(sys.argv)
ventana = QWidget()
ventana.setWindowTitle("CRUD Clientes - oxxo")
ventana.setGeometry(500, 500, 400, 350)

lbl_nombre = QLabel("Nombre:", ventana)
lbl_nombre.move(30, 30)
txt_nombre = QLineEdit(ventana)
txt_nombre.move(150, 30)
txt_nombre.resize(200, 25)

lbl_telefono = QLabel("Teléfono:", ventana)
lbl_telefono.move(30, 70)
txt_telefono = QLineEdit(ventana)
txt_telefono.move(150, 70)
txt_telefono.resize(200, 25)

lbl_email = QLabel("Email:", ventana)
lbl_email.move(30, 110)
txt_email = QLineEdit(ventana)
txt_email.move(150, 110)
txt_email.resize(200, 25)

lbl_puntos = QLabel("Puntos:", ventana)
lbl_puntos.move(30, 150)
txt_puntos = QLineEdit(ventana)
txt_puntos.move(150, 150)
txt_puntos.resize(200, 25)
txt_puntos.setText("0") 

btn_agregar = QPushButton("Agregar", ventana)
btn_agregar.move(30, 200)
btn_actualizar = QPushButton("Actualizar", ventana)
btn_actualizar.move(150, 200)
btn_eliminar = QPushButton("Eliminar", ventana)
btn_eliminar.move(270, 200)
btn_consultar = QPushButton("Consultar Clientes", ventana)
btn_consultar.move(30, 240)
btn_consultar.resize(340, 25)

def agregar_cliente():
    if txt_nombre.text():
        try:
            puntos = int(txt_puntos.text()) if txt_puntos.text() else 0
            cursor.execute(
                "INSERT INTO clientes (nombre, telefono, email, puntos) VALUES (%s, %s, %s, %s)",
                (txt_nombre.text(), txt_telefono.text() or None, txt_email.text() or None, puntos)
            )
            conn.commit()
            QMessageBox.information(ventana, "Éxito", "Cliente agregado")
            limpiar_campos()
        except Exception as e:
            QMessageBox.critical(ventana, "Error", f"Error al agregar: {str(e)}")
    else:
        QMessageBox.warning(ventana, "Advertencia", "El nombre es obligatorio")

def actualizar_cliente():
    if txt_nombre.text() and txt_puntos.text():
        try:
            puntos = int(txt_puntos.text())
            cursor.execute(
                """UPDATE clientes SET 
                   nombre = %s, 
                   telefono = %s, 
                   email = %s, 
                   puntos = %s 
                   WHERE id_cliente = (SELECT id FROM (SELECT MAX(id_cliente) as id FROM clientes) as temp)""",
                (txt_nombre.text(), txt_telefono.text() or None, txt_email.text() or None, puntos)
            )
            conn.commit()
            QMessageBox.information(ventana, "Éxito", "Cliente actualizado")
            limpiar_campos()
        except Exception as e:
            QMessageBox.critical(ventana, "Error", f"Error al actualizar: {str(e)}")
    else:
        QMessageBox.warning(ventana, "Advertencia", "Nombre y puntos son obligatorios")

def eliminar_cliente():
    if txt_nombre.text():
        confirmar = QMessageBox.question(
            ventana, "Confirmar", 
            "¿Eliminar el último cliente agregado con este nombre?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirmar == QMessageBox.StandardButton.Yes:
            try:
                cursor.execute(
                    "DELETE FROM clientes WHERE id_cliente = (SELECT id FROM (SELECT MAX(id_cliente) as id FROM clientes WHERE nombre = %s) as temp)",
                    (txt_nombre.text(),)
                )
                conn.commit()
                QMessageBox.information(ventana, "Éxito", "Cliente eliminado")
                limpiar_campos()
            except Exception as e:
                QMessageBox.critical(ventana, "Error", f"Error al eliminar: {str(e)}")
    else:
        QMessageBox.warning(ventana, "Advertencia", "Ingrese el nombre del cliente a eliminar")

def limpiar_campos():
    txt_nombre.clear()
    txt_telefono.clear()
    txt_email.clear()
    txt_puntos.setText("0")

btn_agregar.clicked.connect(agregar_cliente)
btn_actualizar.clicked.connect(actualizar_cliente)
btn_eliminar.clicked.connect(eliminar_cliente)
btn_consultar.clicked.connect(lambda: ConsultaClientesWindow().exec())

ventana.show()
sys.exit(app.exec())