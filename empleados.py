import sys
import mysql.connector
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QDialog, QVBoxLayout, QScrollArea
from PyQt6.QtCore import Qt

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
        self.setWindowTitle("Consulta de Empleados - oxxo")
        self.setGeometry(150, 150, 400, 300)
        
        layout = QVBoxLayout()
        
        lbl_titulo = QLabel("LISTADO DE EMPLEADOS:")
        layout.addWidget(lbl_titulo)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        self.lbl_resultados = QLabel()
        self.lbl_resultados.setWordWrap(True)
        self.lbl_resultados.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        scroll.setWidget(self.lbl_resultados)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
        self.mostrar_empleados()  
    
    def mostrar_empleados(self):
        cursor.execute("SELECT * FROM empleados ORDER BY id_empleado")
        empleados = cursor.fetchall()
        
        texto = ""
        for emp in empleados:
            texto += f"ID: {emp[0]} - Nombre: {emp[1]}\nPuesto: {emp[2]}\nFecha: {emp[3]}\nSueldo: ${emp[4]:.2f}\n\n"
        
        self.lbl_resultados.setText(texto)

app = QApplication(sys.argv)
ventana = QWidget()
ventana.setWindowTitle("CRUD Empleados - oxxo")
ventana.setGeometry(500, 500, 400, 350)

lbl_id = QLabel("Telefono:", ventana)
lbl_id.move(30, 30)
txt_id = QLineEdit(ventana)
txt_id.move(150, 30)
txt_id.resize(200, 25)

lbl_nombre = QLabel("Nombre:", ventana)
lbl_nombre.move(30, 70)
txt_nombre = QLineEdit(ventana)
txt_nombre.move(150, 70)
txt_nombre.resize(200, 25)

lbl_puesto = QLabel("Puesto:", ventana)
lbl_puesto.move(30, 110)
combo_puesto = QComboBox(ventana)
combo_puesto.move(150, 110)
combo_puesto.resize(200, 25)
combo_puesto.addItems(['gerente', 'cajero', 'almacen'])

lbl_fecha = QLabel("Fecha Contratación:", ventana)
lbl_fecha.move(30, 150)
txt_fecha = QLineEdit(ventana)
txt_fecha.move(150, 150)
txt_fecha.resize(200, 25)
txt_fecha.setPlaceholderText("YYYY-MM-DD")

lbl_sueldo = QLabel("Sueldo:", ventana)
lbl_sueldo.move(30, 190)
txt_sueldo = QLineEdit(ventana)
txt_sueldo.move(150, 190)
txt_sueldo.resize(200, 25)

btn_agregar = QPushButton("Agregar", ventana)
btn_agregar.move(30, 250)
btn_actualizar = QPushButton("Actualizar", ventana)
btn_actualizar.move(150, 250)
btn_eliminar = QPushButton("Eliminar", ventana)
btn_eliminar.move(270, 250)
btn_consultar = QPushButton("Consultar", ventana)
btn_consultar.move(30, 290)
btn_consultar.resize(340, 25)

def agregar_empleado():
    if (txt_id.text() and txt_nombre.text() and txt_fecha.text() and txt_sueldo.text()):
        try:
            cursor.execute(
                "INSERT INTO empleados (id_empleado, nombre, puesto, fecha_contratacion, sueldo) VALUES (%s, %s, %s, %s, %s)",
                (txt_id.text(), txt_nombre.text(), combo_puesto.currentText(), txt_fecha.text(), float(txt_sueldo.text())))
            conn.commit()
            QMessageBox.information(ventana, "Éxito", "Empleado agregado")
            limpiar_campos()
        except Exception as e:
            QMessageBox.critical(ventana, "Error", f"Error al agregar: {str(e)}")
    else:
        QMessageBox.warning(ventana, "Advertencia", "Todos los campos son obligatorios")

def actualizar_empleado():
    if (txt_id.text() and txt_nombre.text() and txt_fecha.text() and txt_sueldo.text()):
        try:
            cursor.execute(
                """UPDATE empleados SET 
                   nombre = %s, 
                   puesto = %s, 
                   fecha_contratacion = %s, 
                   sueldo = %s 
                   WHERE id_empleado = %s""",
                (txt_nombre.text(), combo_puesto.currentText(), txt_fecha.text(), 
                 float(txt_sueldo.text()), int(txt_id.text())))
            conn.commit()
            QMessageBox.information(ventana, "Éxito", "Empleado actualizado")
            limpiar_campos()
        except Exception as e:
            QMessageBox.critical(ventana, "Error", f"Error al actualizar: {str(e)}")
    else:
        QMessageBox.warning(ventana, "Advertencia", "Todos los campos son obligatorios")

def eliminar_empleado():
    if txt_id.text():
        confirmar = QMessageBox.question(ventana, "Confirmar", 
                                        "¿Eliminar este empleado?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmar == QMessageBox.StandardButton.Yes:
            try:
                cursor.execute("DELETE FROM empleados WHERE id_empleado = %s", 
                             (int(txt_id.text()),))
                conn.commit()
                QMessageBox.information(ventana, "Éxito", "Empleado eliminado")
                limpiar_campos()
            except Exception as e:
                QMessageBox.critical(ventana, "Error", f"Error al eliminar: {str(e)}")
    else:
        QMessageBox.warning(ventana, "Advertencia", "Ingrese un ID para eliminar")

def limpiar_campos():
    txt_id.clear()
    txt_nombre.clear()
    combo_puesto.setCurrentIndex(0)
    txt_fecha.clear()
    txt_sueldo.clear()

btn_agregar.clicked.connect(agregar_empleado)
btn_actualizar.clicked.connect(actualizar_empleado)
btn_eliminar.clicked.connect(eliminar_empleado)
btn_consultar.clicked.connect(lambda: ConsultaWindow().exec())

ventana.show()
sys.exit(app.exec())
