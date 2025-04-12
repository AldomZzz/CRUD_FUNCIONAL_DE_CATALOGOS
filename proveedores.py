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

class ConsultaProveedoresWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consulta de Proveedores - oxxo")
        self.setGeometry(150, 150, 500, 400)
        
        layout = QVBoxLayout()
        
        lbl_titulo = QLabel("LISTADO DE PROVEEDORES:")
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
        
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.close)
        layout.addWidget(btn_cerrar)
        
        self.setLayout(layout)
        self.mostrar_proveedores()
    
    def mostrar_proveedores(self):
        cursor.execute("SELECT * FROM proveedores ORDER BY id_proveedor")
        proveedores = cursor.fetchall()
        
        texto = ""
        for prov in proveedores:
            texto += (f"ID: {prov[0]}\n"
                     f"Nombre: {prov[1]}\n"
                     f"Contacto: {prov[2] or 'No especificado'}\n"
                     f"Teléfono: {prov[3] or 'No registrado'}\n"
                     f"Email: {prov[4] or 'No registrado'}\n"
                     "------------------------\n")
        
        self.lbl_resultados.setText(texto)

app = QApplication(sys.argv)
ventana = QWidget()
ventana.setWindowTitle("CRUD Proveedores - oxxo")
ventana.setGeometry(500, 500, 400, 350)

lbl_nombre = QLabel("Nombre:", ventana)
lbl_nombre.move(30, 30)
txt_nombre = QLineEdit(ventana)
txt_nombre.move(150, 30)
txt_nombre.resize(200, 25)

lbl_contacto = QLabel("Contacto:", ventana)
lbl_contacto.move(30, 70)
txt_contacto = QLineEdit(ventana)
txt_contacto.move(150, 70)
txt_contacto.resize(200, 25)

lbl_telefono = QLabel("Teléfono:", ventana)
lbl_telefono.move(30, 110)
txt_telefono = QLineEdit(ventana)
txt_telefono.move(150, 110)
txt_telefono.resize(200, 25)

lbl_email = QLabel("Email:", ventana)
lbl_email.move(30, 150)
txt_email = QLineEdit(ventana)
txt_email.move(150, 150)
txt_email.resize(200, 25)

btn_agregar = QPushButton("Agregar", ventana)
btn_agregar.move(30, 200)
btn_actualizar = QPushButton("Actualizar", ventana)
btn_actualizar.move(150, 200)
btn_eliminar = QPushButton("Eliminar", ventana)
btn_eliminar.move(270, 200)
btn_consultar = QPushButton("Consultar Proveedores", ventana)
btn_consultar.move(30, 240)
btn_consultar.resize(340, 25)

def agregar_proveedor():
    if txt_nombre.text():
        try:
            cursor.execute(
                "INSERT INTO proveedores (nombre, contacto, telefono, email) VALUES (%s, %s, %s, %s)",
                (txt_nombre.text(), 
                 txt_contacto.text() or None, 
                 txt_telefono.text() or None, 
                 txt_email.text() or None)
            )
            conn.commit()
            QMessageBox.information(ventana, "Éxito", "Proveedor agregado")
            limpiar_campos()
        except Exception as e:
            QMessageBox.critical(ventana, "Error", f"Error al agregar: {str(e)}")
    else:
        QMessageBox.warning(ventana, "Advertencia", "El nombre es obligatorio")

def actualizar_proveedor():
    if txt_nombre.text():
        try:
            cursor.execute(
                """UPDATE proveedores SET 
                   nombre = %s, 
                   contacto = %s, 
                   telefono = %s, 
                   email = %s 
                   WHERE id_proveedor = (SELECT id FROM (SELECT MAX(id_proveedor) as id FROM proveedores WHERE nombre = %s) as temp)""",
                (txt_nombre.text(), 
                 txt_contacto.text() or None, 
                 txt_telefono.text() or None, 
                 txt_email.text() or None,
                 txt_nombre.text())
            )
            conn.commit()
            QMessageBox.information(ventana, "Éxito", "Proveedor actualizado")
            limpiar_campos()
        except Exception as e:
            QMessageBox.critical(ventana, "Error", f"Error al actualizar: {str(e)}")
    else:
        QMessageBox.warning(ventana, "Advertencia", "El nombre es obligatorio")

def eliminar_proveedor():
    if txt_nombre.text():
        confirmar = QMessageBox.question(
            ventana, "Confirmar", 
            "¿Eliminar el último proveedor con este nombre?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirmar == QMessageBox.StandardButton.Yes:
            try:
                cursor.execute(
                    "DELETE FROM proveedores WHERE id_proveedor = (SELECT id FROM (SELECT MAX(id_proveedor) as id FROM proveedores WHERE nombre = %s) as temp)",
                    (txt_nombre.text(),)
                )
                conn.commit()
                QMessageBox.information(ventana, "Éxito", "Proveedor eliminado")
                limpiar_campos()
            except Exception as e:
                QMessageBox.critical(ventana, "Error", f"Error al eliminar: {str(e)}")
    else:
        QMessageBox.warning(ventana, "Advertencia", "Ingrese el nombre del proveedor a eliminar")

def limpiar_campos():
    txt_nombre.clear()
    txt_contacto.clear()
    txt_telefono.clear()
    txt_email.clear()

btn_agregar.clicked.connect(agregar_proveedor)
btn_actualizar.clicked.connect(actualizar_proveedor)
btn_eliminar.clicked.connect(eliminar_proveedor)
btn_consultar.clicked.connect(lambda: ConsultaProveedoresWindow().exec())

ventana.show()
sys.exit(app.exec())