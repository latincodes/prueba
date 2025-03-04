import flet as ft
# Protocolo para enviar correos
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
# Para manejar los datos
import pandas as pd
from datetime import datetime
import locale
import time
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
rows_per_page = 5
################## para encriptar y desencriptar
import bcrypt
from cryptography.fernet import Fernet
import base64
import hashlib
import io
import sys, os
##################
from consultas import main as consulta_app

def validacion(page: ft.Page):
    pwd = b'$2b$12$2EU1DdXLoQ94aN/zD0kzyuPtD6DBntPcopiwj82EgoeCdL3dQtpvy'

    # Función para obtener la ruta correcta del archivo
    def obtener_ruta_archivo(nombre_archivo):
        if getattr(sys, 'frozen', False):  # Si el programa está empaquetado como .exe
            ruta_base = sys._MEIPASS
        else:
            ruta_base = os.path.dirname(__file__)  # Si se ejecuta como script .py

        return os.path.join(ruta_base, nombre_archivo)

    # Usa la función al cargar el CSV
    ruta_csv = obtener_ruta_archivo("correos_encrypted.csv")

    # Descifrar CSV
    def descifrar_csv(password):
        clave = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
        fernet = Fernet(clave)

        try:
            # Leer archivo cifrado
            with open(ruta_csv, "rb") as file:
                encrypted_data = file.read()

            # Intentar descifrar
            data = fernet.decrypt(encrypted_data).decode()
            return pd.read_csv(io.StringIO(data))

        except Exception as e:
            print("Error al descifrar:", e)
            return None  # Retorna None si la contraseña es incorrecta
        
    def validar_contraseña(e):

        if bcrypt.checkpw(password_input.value.encode('utf-8'), pwd):

            df_correos = descifrar_csv(password_input.value)
            
            page.close(dialog)
            page.update()
            main(page,df_correos)

        else:
            error_text1.value="Contraseña Incorrecta"
            page.update()
            error_text1.value=""

    def cerrar_dialogo(e):
        try:
            """ Cierra el diálogo y vuelve a la página de Consultas. """
            page.close(dialog)
            page.update()
            e.control.selected_index = 0
            page.navigation_bar.content.controls[0].content.selected_index = 0 
            consulta_app(page)
        except:
            page.open(dialog)
            page.update()
            pass

    password_input = ft.TextField(
        autofocus=True,
        hint_text=("Ingrese La Contraseña"),
        text_size=16,
        password=True,
        can_reveal_password=True,
        width=220,
        height=42,
        on_submit=validar_contraseña
    )
    error_text1 = ft.Text("", size=14, color="red",weight="BOLD")  # Mensaje de error si la contraseña es incorrecta

    dialog = ft.CupertinoAlertDialog(
        title=ft.Text("Acceso restringido",weight="BOLD"),
        modal=True,
        content=ft.Column([password_input, error_text1],height=64),
        actions=[
            ft.CupertinoDialogAction("Cancelar",is_destructive_action=True, on_click=cerrar_dialogo),  # Cierra y regresa a consultas
            ft.CupertinoDialogAction("Ingresar",is_default_action=True, on_click=validar_contraseña)
        ],
    )
    page.overlay.append(dialog)
    page.update()
    page.open(dialog)
    page.update()

################################################33
def main(page: ft.Page, df_correos):
    import os
    page.title = "GOBERNACIÓN DE CASANARE - Faltantes por PAE"
    page.scroll = "adaptive"  # Permite desplazamiento si es necesario

    # inicialiazr y definir variables globales
    df = None           #DataFrame Detallado
    df_A = None         #DataFrame Anexo 13A
    df_filtrado = None  #DataFrame filtrado Detallado Alumnos
    filtro_anexo = None
    df_final = None
    df_descargar = None
    df_tabla = None
    carpeta_descarga = os.path.expanduser("~")  # Carpeta de descarga predeterminada
    global table_i, current_page, subir,nuevo_rows_per_page, tabla_destino
    current_page = 0
    nuevo_rows_per_page = rows_per_page
    fecha_actual = datetime.now().strftime('%B %d %Y').capitalize()  # Formato: Febrero 17 2025


    #################################################################################
    # Estilo CupertinoActionSheet
    def show_cupertino_action_sheet(e):
        page.open(bottom_sheet)
    def handle_click(e):
        page.close(bottom_sheet)

    #########################################################################################################################        
    ################################################# COLUMNAS OBLIGATORIAS PARA DETALLADO ALUMNOS
    columnas_df = ['ANO', 'ETC', 'ESTADO', 'JERARQUIA', 'INSTITUCION', 'DANE', 'CALENDARIO', 'SECTOR', 'SEDE', 'CODIGO_DANE_SEDE', 'CONSECUTIVO',
       'ZONA_SEDE', 'JORNADA', 'GRADO_COD', 'GRUPO', 'MODELO', 'MOTIVO', 'FECHAINI', 'FECHAFIN', 'NUI', 'ESTRATO', 'SISBEN IV', 'PER_ID', 'DOC',
       'TIPODOC', 'APELLIDO1', 'APELLIDO2', 'NOMBRE1', 'NOMBRE2', 'GENERO', 'FECHA_NACIMIENTO', 'BARRIO', 'EPS', 'TIPO DE SANGRE', 'MATRICULACONTRATADA', 
       'FUENTE_RECURSOS', 'INTERNADO', 'NUM_CONTRATO', 'APOYO_ACADEMICO_ESPECIAL', 'SRPA', 'DISCAPACIDAD', 'PAIS_ORIGEN','CORREO'
    ]   
    ################################################# COLUMNAS OBLIGATORIAS PARA ANEXO 13A
    columnas_df_A = ['ANO_INF', 'MUN_CODIGO', 'CODIGO_DANE', 'DANE_ANTERIOR', 'NOMBRE_EE', 'CONS_SEDE', 'NOMBRE_SEDE', 'TIPO_DOCUMENTO', 'NRO_DOCUMENTO',
       'EXP_DEPTO', 'EXP_MUN', 'APELLIDO1', 'APELLIDO2', ' NOMBRE1', 'NOMBRE2', 'DIRECCION_RESIDENCIA', 'TEL', 'RES_DEPTO', 'RES_MUN', 'ESTRATO', 'SISBEN IV',
       'FECHA_NACIMIENTO', 'NAC_DEPTO', 'NAC_MUN', 'GENERO', 'POB_VICT_CONF_RUV', ' PROVIENE_SECTOR_PRIV', 'PROVIENE_OTR_MUN', 'TIPO_DISCAPACIDAD', 'CAP_EXC', 
       'ETNIA', 'RES', 'INS_FAMILIAR', 'TIPO_JORNADA', 'CARACTER', 'ESPECIALIDAD', 'GRADO', 'GRUPO', 'METODOLOGIA', 'MATRICULA_CONTRATADA', 'REPITENTE', 'NUEVO', 
       'FUE_RECU', 'ZON_ALU', 'CAB_FAMILIA', 'BEN_MAD_FLIA', 'BEN_VET_FP', 'BEN_HER_NAC', 'CODIGO_INTERNADO', 'CODIGO_VALORACION_1', 'CODIGO_VALORACION_2', 
       'ID_ESTRATEGIA', 'NOMBRE_ESTRATEGIA', 'TIPO_ESTRATEGIA', 'ESTRATEGIA_SUBTIPO', 'FECHA_INICIO_ESTRATEGIA', 'FECHA_FIN_ESTRATEGIA', 
       'FECHA_INICIO_ESTRATEGIA_ALUMNO', 'FECHA_FIN_ESTRATEGIA_ALUMNO', 'APOYO_ACADEMICO_ESPECIAL', 'SRPA', 'PAIS_ORIGEN', 'PER_ID', 'FECHA_GENERACION'
    ]

    
    ######################################################## Función para cargar el archivo detallado .txt y validar las columnas. DETALLADO ALUMNOS
    def cargar_archivo(e):
        nonlocal df,df_A
        if archivo_txt_dialog.result.files is not None: archivo = archivo_txt_dialog.result.files[0].path
        else: archivo = None

        if archivo is not None and archivo != "":
            try:
                df = pd.read_csv(archivo, delimiter=';', encoding='latin1') # MODELO
                if list(df.columns) == columnas_df:
                    action_sheet.message = ft.Text(value="Detallado de Alumnos cargado exitosamente. 🫡",size=15,color="blue",weight=ft.FontWeight.BOLD)
                    action_sheet.actions[0].disabled=True

                    if df_A is not None:
                        etiqueta.value = "Ya puede descargar el reporte Faltantes x PAE"
                        aplicar_filtros(e)
                    else:
                        pass

                else:
                    action_sheet.message = ft.Text(value="Ese no es el DETALLADO DE ALUMNOS 👀",size=15,color="blue",weight=ft.FontWeight.BOLD)
                    df = None  # Reiniciar df si las columnas no coinciden
            except:
                etiqueta.value = "Error al cargar el archivo. Intentelo Nuevamente"
                df = None
        else:
            etiqueta.value = "No se seleccionó ningún archivo."
            df = None
            action_sheet.message = ft.Text(value="No se seleccionó ningún archivo",size=15,color="blue",weight=ft.FontWeight.BOLD)

        page.update()

    ######################################################## Función para cargar el archivo anexo .txt y validar las columnas ANEXO 13A
    def cargar_archivo_anexo(e):
        nonlocal df_A,df
        if archivo_txt_dialog_anexo.result.files is not None: archivo_anexo = archivo_txt_dialog_anexo.result.files[0].path
        else: archivo_anexo = None

        if archivo_anexo is not None and archivo_anexo != "":
            try:
                df_A = pd.read_csv(archivo_anexo, delimiter=';', encoding='latin1')

                # CONTROLADOR
                if list(df_A.columns) == columnas_df_A:
                    action_sheet.message = ft.Text(value="Anexo 13A cargado exitosamente. 🫡",size=15,color="blue",weight=ft.FontWeight.BOLD)
                    action_sheet.actions[1].disabled=True

                    if df is not None:
                        etiqueta.value = "Ya puede descargar el reporte FALTANTES x PAE"
                        aplicar_filtros(e)
                    else:
                        pass

                else:
                    action_sheet.message = ft.Text(value="Ese no es el ANEXO 13A 👀",size=15,color="blue",weight=ft.FontWeight.BOLD)
                    
                    df_A = None  # Reiniciar df si las columnas no coinciden
            except:
                etiqueta.value = "Error al cargar el archivo. Intentelo nuevamente"
                df_A = None
        else:
            etiqueta.value = "No se seleccionó ningún archivo."  
            df_A = None 
            action_sheet.message = ft.Text(value="No se seleccionó ningún archivo",size=15,color="blue",weight=ft.FontWeight.BOLD)

        page.update()

    ########################################  FUNCION PARA APLICAR FILTROS
    def aplicar_filtros(e):
        nonlocal df_filtrado  #### FILTRADO DEL DETALLADO DE ALUMNOS
        nonlocal filtro_anexo #### FILTRADO DEL ANEXO 13A
        if df is not None and df_A is not None:
            try:
                ##################### Aplicar los filtros para DETALLADO ALUMNOS (todos los beneficiarios con PAE)
                filtro_rural = df[ (df['ESTADO'] == 'MATRICULADO') & (df['SECTOR'] == 'OFICIAL') & (df['ZONA_SEDE'] == 'RURAL') &
                    (df['JORNADA'].isin(['MAÑANA', 'TARDE', 'ÚNICA'])) & ((df['INTERNADO'] == 'NINGUNO') | (df['INTERNADO'].isna())) ]

                filtro_urbana = df[ (df['ESTADO'] == 'MATRICULADO') & (df['SECTOR'] == 'OFICIAL') & (df['ZONA_SEDE'] == 'URBANA') &
                    (df['JORNADA'] == 'ÚNICA') & ((df['INTERNADO'] == 'NINGUNO') | (df['INTERNADO'].isna())) ]

                filtro_tamara = df[ (df['ESTADO'] == 'MATRICULADO') & (df['JERARQUIA'] == 'TÁMARA') & (df['SECTOR'] == 'OFICIAL') &
                    (df['ZONA_SEDE'] == 'URBANA') & (df['GRADO_COD'] == 0.0) ]

                # Concatenar filtrados
                df_unido = pd.concat([filtro_rural, filtro_urbana, filtro_tamara])
                # Filtrar según criterios adicionales
                df_filtrado = df_unido[~((df_unido['SEDE'] == 'FRANCISCO DE ASIS') & (df_unido['ZONA_SEDE'] == 'RURAL'))]
                
                ##################### Aplicar los filtros para ANEXO 13A (reportados con PAE)
                filtro_anexo = df_A[ ((df_A['CODIGO_INTERNADO'] == 3) | (df_A['CODIGO_INTERNADO'].isna())) & 
                    (df_A['NOMBRE_ESTRATEGIA'].isin(['CASANARE-2025-ALIMENTACION ESCOLAR-ALMUERZO-OTROS-COFINANCIACIÓN NACIÓN PARA ALIMENTACIÓN ESCOLAR-A-27-01-2025', 'CASANARE-2025-ALIMENTACION ESCOLAR-REFRIGERIO-OTROS-COFINANCIACIÓN NACIÓN PARA ALIMENTACIÓN ESCOLAR-A-27-01-2025'])) & 
                    (df_A['FECHA_FIN_ESTRATEGIA_ALUMNO'].isna()) ]
                

                eliminar_duplicados(e) 

                
            except:
                status_label.value = "Error al aplicar filtros"
        else:
            status_label.value = "Primero se deben subir los archivos necesarios."

        page.update()

    ######################################################## Función para terminar de aplicar filtros
    def eliminar_duplicados(e):
        #import main
        nonlocal df_filtrado  #### FILTRADO DEL DETALLADO DE ALUMNOS
        nonlocal filtro_anexo #### FILTRADO DEL ANEXO 13A
        nonlocal df_final, df_tabla
        global total_destinatarios, destinatarios_pae

        if df_filtrado is not None and filtro_anexo is not None:
            try:
                # Obtiene los estudiantes beneficiados(df_filtrado) que ya fueron marcados con PAE (filtro_anexo).
                duplicados = df_filtrado['DOC'].isin(filtro_anexo['NRO_DOCUMENTO'])

        # elimina los estudiantes beneficiados que ya fueron marcados con pae del dataframe df_filtrado, para obtener los estudiantes beneficiados que aún no han sido marcados con PAE
                df_final = df_filtrado[~duplicados]
                df_tabla = df_final[['ANO','ESTADO','JERARQUIA','INSTITUCION','DANE','SEDE','JORNADA','GRADO_COD','GRUPO','DOC','TIPODOC','APELLIDO1','APELLIDO2','NOMBRE1','NOMBRE2']]
                df_tabla = df_tabla.sort_values(by='DANE',ascending=True)
                df_tabla['DANE'] = df_tabla['DANE'].astype('int64')


                print(df_correos.head())

                df_destinatarios = df_tabla.merge(df_correos[['DANE', 'CORREO']], on='DANE', how='left')
                # Filtrar los correos únicos
                destinatarios_pae = df_destinatarios['CORREO'].unique().tolist()


                # TABLA PARA MOSTRAR LOS DESTINATARIOS
                destinatarios_tabla = df_destinatarios[['INSTITUCION','CORREO']].drop_duplicates()
                total_destinatarios = len(destinatarios_tabla)
                tabla_destino.rows.clear()   # LIMPIO LA TABLA
                #Definir columnas de la tabla
                columnas_destino = list(destinatarios_tabla.columns)
                tabla_destino.columns = [ft.DataColumn(ft.Text(col)) for col in columnas_destino]

                for _, row in destinatarios_tabla.iterrows():
                    tabla_destino.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(row[col]), selectable=True)) for col in columnas_destino]))
                

                total_destinatarios_label.value = f"Cantidad de Destinatarios: {total_destinatarios}"

                label_login.value = "Primero descargue el archivo, luego podrá enviar el email."
                status_label.value = "Selecciona una carpeta para guardar el archivo y luego descárguelo."
                seleccionar_carpeta_button.disabled = False
                status_label.visible=True
                download_bottom.visible=True
                login_datos.visible=True
                tabla_d.visible=True
            except:
                status_label.value = "ERROR: al eliminar duplicados."
        else:
            status_label.value = "Error al eliminar duplicados. Inténtalo nuevamente."

        update_table(None, page)
        page.update()  

    ######################################################## DESCARGAR ARCHIVO FILTRADO
    def descargar_archivo(e):
        nonlocal carpeta_descarga
        global filtered_df, output_final
        if df_filtrado is not None:
            if filtro_anexo is not None:
                try:
                    output_file = os.path.join(carpeta_descarga, "Beneficiarios PAE.csv")                         ## total beneficiados
                    output_anexo = os.path.join(carpeta_descarga, "Reportados PAE.csv")                               ## total de beneficiados reportados
                    output_final = os.path.join(carpeta_descarga, f"Faltantes x PAE - {fecha_actual}.csv")                ## beneficiados que aún no se reportan

                    df_filtrado.to_csv(output_file, sep=';', encoding='latin1', index=False)   ### ARCHIVO FINAL DEL FILTRO DETALLADO ALUMNOS
                    filtro_anexo.to_csv(output_anexo, sep=';', encoding='latin1', index=False) ### ARCHIVO FINAL DEL FILTRO ANEXO 13A
                    filtered_df.to_csv(output_final, sep=';', encoding='latin1', index=False)     ### ARCHIVO FINAL FALTANTES POR PAE
                    status_label.value = f"GUARDADO EN: ({carpeta_descarga})"
                    descargar_button.icon=ft.Icons.DOWNLOAD_DONE_ROUNDED
                    descargar_button.disabled=True

                    
                    label_login.value = "Ya puede ingresar sus datos para enviar el email."
                    correo_input.disabled=False
                    pass_input.disabled=False
                    nombre.disabled=False
                    prueba_real.visible=True
                    
                    
                    
                except Exception as ex:
                    status_label.value = "Error al guardar el archivo"
            page.update()
    

    ######################################################################################################################### CONTROLADOR
    ######################################################## SELECCIONAR CARPETA DONDE SE DESCARGARÁ EL ARCHIVO 
    def seleccionar_carpeta(e):
        import tkinter as tk
        from tkinter import filedialog
        try:
            nonlocal carpeta_descarga
            root = tk.Tk()
            root.withdraw()  # Ocultar la ventana principal de Tkinter
            root.lift()  # Levantar la ventana al frente
            root.attributes("-topmost", True)  # Mantener la ventana al frente
            carpeta_descarga = filedialog.askdirectory()
            if carpeta_descarga:
                status_label.value = f"Carpeta seleccionada: {carpeta_descarga}"
                descargar_button.icon=ft.Icons.DOWNLOAD_ROUNDED
                descargar_button.disabled = False
                seleccionar_carpeta_button.disabled=True
            else:
                status_label.value = "No se seleccionó ninguna carpeta."
        except:
            status_label.value = "Error seleccionado la carpeta"
        page.update()

    ######################################################## Función para abrir el cuadro de diálogo de selección de archivo (seleccionar archivo txt)
    # DETALLADO DE ALUMNOS
    def abrir_dialogo_archivo(e):
        archivo_txt_dialog.pick_files(allowed_extensions=['txt'])
    # ANEXO 13A
    def abrir_dialogo_archivo_anexo(e):
        archivo_txt_dialog_anexo.pick_files(allowed_extensions=['txt'])  
    ################################### El archivo seleccionado "ejecuta" la función cargar_archivo o cargar_archivo_anexo
    archivo_txt_dialog = ft.FilePicker(on_result=cargar_archivo)                    # DETALLADO DE ALUMNOS
    archivo_txt_dialog_anexo = ft.FilePicker(on_result=cargar_archivo_anexo)        # ANEXO 13A

    ######################################################## FUNCION EMPEZAR DE NUEVO
    def borrar_archivo(e):
        nonlocal df,df_A,df_filtrado,filtro_anexo,df_final, df_tabla
        global table_i, filtered_df, tabla_destino
        df = None           #DataFrame Detallado
        df_A = None         #DataFrame Anexo 13A
        df_filtrado = None  #DataFrame filtrado Detallado Alumnos
        filtro_anexo = None
        df_final = None
        df_tabla = None
        filtered_df = None
        action_sheet.actions[1].disabled=False  ## Boton subir anexo 13a
        action_sheet.actions[0].disabled=False  ## Bootn subir detallado alumnos
        action_sheet.message=ft.Text("Elige los documentos en formato (.txt) a subir.",size=15,color="blue",weight=ft.FontWeight.BOLD)
        etiqueta.value="Primero suba los archivos necesarios"

        seleccionar_carpeta_button.disabled=True
        descargar_button.disabled=True
        descargar_button.icon =ft.Icons.DOWNLOAD_ROUNDED
        status_label.visible=False
        download_bottom.visible=False
        login_datos.visible=False
        tabla_d.visible=False


        total_filas.value = ""
        paginas.value = ""
        table_i.rows.clear()
        table_i.columns = [ft.DataColumn(ft.Text("SUBA UN ARCHIVO"))]

        tabla_destino.rows.clear()
        tabla_destino.columns = [ft.DataColumn(ft.Text("DESTINATARIOS"))]
        total_destinatarios_label.value = ""

        label_login.value = "Primero suba los archivos necesarios."
        prueba_real.visible=False
        correo_input.value=""
        correo_input.disabled=True
        pass_input.value=""
        pass_input.disabled=True
        nombre.value=""
        nombre.disabled=True
        button_enviar_email.content.disabled=True
        button_enviar_email.content = config_boton
        button_enviar_email.content.icon = ft.Icons.SEND_ROUNDED
        button_enviar_email.content.tooltip = "Primero debe descargar el archivo Faltantes por PAE"
        page.update()


    ######################################################## Función para actualizar la tabla en la GUI
    def update_table(e, page):
        nonlocal df_tabla
        if df_tabla is not None:
            try:
                global total_pages, total_rows, filtered_df

                filtered_df = df_tabla.drop('DANE', axis=1)                    # Dataframe usado para descargarse
                # Paginación
                total_rows = len(filtered_df)
                total_pages = (total_rows // nuevo_rows_per_page) + (1 if total_rows % nuevo_rows_per_page > 0 else 0)

                # Actualizar la tabla con las filas de la página actual
                start_row = current_page * nuevo_rows_per_page
                end_row = start_row + nuevo_rows_per_page
                page_data = filtered_df.iloc[start_row:end_row]

                table_i.rows.clear()
                columnas_df = list(filtered_df.columns)
                table_i.columns = [ft.DataColumn(ft.Text(col)) for col in columnas_df]

                for _, row in page_data.iterrows():
                    table_i.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(row[col]),selectable=True)) for col in columnas_df]))

                #### Mostrar pagina actual, total de paginas y total de filas
                paginas.value = f"{current_page+1}/{total_pages}"
                total_filas.value = f"Total de estudiantes faltantes por PAE: {total_rows}"
                page.update()
            
            except Exception as e:
                status_label.value = "Error mostrando la tabla"

    ######################################################## Función para asignar nuevo valor de FILAS por PÁGINA
    def set_rows_per_page(valorr: str):
        global nuevo_rows_per_page
        try:
            nuevo_rows_per_page = int(valorr) if 1 <= int(valorr) <= 60 else rows_per_page
        except:
            nuevo_rows_per_page = rows_per_page
    
        filas_x_pag.value = str(nuevo_rows_per_page)
        update_table(None, page)

    ######################################################## Funciones para la paginación
    def in_page(e):
        global current_page
        current_page = 0
        update_table(e, page)
    
    def prev_page(e):
        global current_page
        if current_page > 0:
            current_page -= 1
            update_table(e, page)

    def next_page(e):
        global current_page
        try:
            if current_page < total_pages - 1:
                current_page += 1
                update_table(e, page)
        except:
            pass

    def fin_page(e):
        global current_page
        try:
            current_page = total_pages - 1
            update_table(e, page)
        except:
            pass


    def validar_inputs(e):
        try:
            """Habilita el botón si ambos campos tienen contenido"""
            if correo_input.value and pass_input.value and nombre.value:
                button_enviar_email.content.disabled = False
                button_enviar_email.content.icon = ft.Icons.SEND_ROUNDED
                label_login.value = "Ya puede enviar el email. Recuerde validar sus datos"
                button_enviar_email.content.tooltip = "Presione para enviar el email"
            else:
                button_enviar_email.content.disabled = True
                button_enviar_email.content.tooltip = "Primero ingrese un correo y contraseña válidos"
                label_login.value = "Ingrese su correo y contraseña para enviar el email"
        except:
            status_label.value= "Ingrese un correo y contraseña válidos"
        page.update()

    
    # ENVIAR CORREO
    def enviar_email(e):
        global output_final
        try:
            
            button_enviar_email.content = ft.ProgressRing(width=18, height=18)
            page.update()

            remitente = correo_input.value
            destinatarios = destinatarios_pae if prueba_real.value else [correo_prueba.value]
            asunto = 'Faltantes por PAE'
            # Cuerpo del correo en HTML con negrilla
            nombre_remitente = nombre.value
            cuerpo = f"""\
            <html>
            <body>
                <p>Respetados directivos,</p>

                <br>

                <p>Su institución educativa presenta <strong>estudiantes sin caracterizar con la estrategia de Alimentación Escolar (PAE)</strong> en el sistema SIMAT.</p>

                <p>Con el fin de garantizar el correcto acceso a este beneficio, solicitamos <strong>verificar y actualizar la información</strong> correspondiente a la mayor brevedad posible.</p>

                <p>Agradecemos su gestión y compromiso con la permanencia educativa de los estudiantes.</p>

                <br>
                
                <p>Atentamente,</p>

                <p><strong>{nombre_remitente}</strong></p>

                <p><strong>SECRETARÍA DE EDUCACIÓN DE CASANARE</strong></p>

                <p><img src="https://www.casanare.gov.co/SiteAssets/Images/Secretarias%202017-07.jpg" alt="Logo Secretaría de Educación" width="220"></p>
            </body>
            </html>
            """

            nombre_adjunto = f"Faltantes x PAE - {fecha_actual}.csv"
            ruta_adjunto = output_final
            

            # Creamos el objeto mensaje
            mensaje = MIMEMultipart()
            
            # Establecemos los atributos del mensaje
            mensaje['From'] = remitente 
            mensaje['To'] = ", ".join(destinatarios)
            mensaje['Subject'] = asunto
            
            # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
            mensaje.attach(MIMEText(cuerpo, 'html'))
            try:
                label_login.value = "Buscando el archivo a enviar..."
                page.update()
                time.sleep(2)
                # Abrimos el archivo que vamos a adjuntar
                archivo_adjunto = open(ruta_adjunto, 'rb')
                
                # Creamos un objeto MIME base
                adjunto_MIME = MIMEBase('application', 'octet-stream')
                # Y le cargamos el archivo adjunto
                adjunto_MIME.set_payload((archivo_adjunto).read())
                
            except:
                label_login.value = "No se encontró el archivo. Intente nuevamente"
                button_enviar_email.content = config_boton
                page.update()
            
            # Codificamos el objeto en BASE64
            encoders.encode_base64(adjunto_MIME)
            # Agregamos una cabecera al objeto
            adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
            # Y finalmente lo agregamos al mensaje
            mensaje.attach(adjunto_MIME)
            
            # Creamos la conexión con el servidor
            sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
            
            # Ciframos la conexión
            sesion_smtp.starttls()

            # Iniciamos sesión en el servidor
            try:
                label_login.value = "Enviando, por favor espere..."
                page.update()
                time.sleep(1)
                sesion_smtp.login(correo_input.value,pass_input.value)
            
                # Convertimos el objeto mensaje a texto
                texto = mensaje.as_string()
                # Enviamos el mensaje
                sesion_smtp.sendmail(remitente, destinatarios, texto)
                label_login.value = "Correos Enviados Exitosamente."
                button_enviar_email.content = config_boton

            except:
                label_login.value ="Correo o contraseña incorrecta. Intente nuevamente."
                button_enviar_email.content.disabled = True
                button_enviar_email.content = config_boton
            # Cerramos la conexión
            sesion_smtp.quit()
        except:
            pass
        page.update()
        


    def cambiar_label(e):
        if prueba_real.value:
            prueba_real.label = "Real"
            correo_prueba.visible = False
        else:
            prueba_real.label = "Prueba"
            correo_prueba.visible = True
        page.update()

    ############################################### ENVIAR CORREO ELECTRÓNICO
    config_boton = ft.IconButton(icon_color="black",tooltip="Primero debe descargar el archivo Faltantes x PAE",icon=ft.Icons.SEND_ROUNDED, disabled=True,on_click=enviar_email)
    label_login = ft.Text("Primero suba los archivos necesarios",weight="bold",text_align=ft.TextAlign.JUSTIFY)
    correo_input = ft.TextField(color="black",label="Correo - SOLO GMAIL.COM", text_size=12, prefix_icon_size_constraints=4, width=230,border="underline",prefix_icon=ft.Icons.EMAIL_ROUNDED,disabled=True,on_change=validar_inputs)
    pass_input = ft.TextField(color="black",label="Contraseña", text_size=12, password=True, can_reveal_password=True, width=200,border="underline", prefix_icon=ft.Icons.LOCK_ROUNDED,disabled=True,on_change=validar_inputs,on_submit=enviar_email)
    button_enviar_email = ft.Container(config_boton)
    recordar_clave = ft.TextButton("¿Olvidó su contraseña?", url="https://myaccount.google.com/apppasswords")

    correo_prueba = ft.TextField(color="black",label="Correo de prueba", width=250,border="underline",visible=False)
    nombre = ft.TextField(color="black",label="Nombre", text_size=12, width=195,border="underline",prefix_icon=ft.Icons.PERSON_ROUNDED,disabled=True,on_change=validar_inputs)
    prueba_real = ft.CupertinoSwitch(label="Real",value=True,on_change=cambiar_label,visible=False)

    login_datos = ft.Container(
        content=ft.Column([
            ft.Row([label_login,ft.Text("     "),recordar_clave,prueba_real]),
            ft.Row([correo_input,pass_input,nombre,button_enviar_email])
        ],alignment=ft.MainAxisAlignment.CENTER,  # Centrar elementos dentro del Row
        ),
        border_radius=15,  # Mejor usar border_radius que border
        gradient=ft.LinearGradient([ft.Colors.INVERSE_PRIMARY,ft.Colors.TERTIARY_CONTAINER]),
        padding=10,
        visible=False
        )
    
    
    ########################################################  DEFINIR LAS TABLAS
    table_i = ft.DataTable(columns=[ft.DataColumn(ft.Text("PRIMERO SUBA EL ARCHIVO"))],border=ft.border.all(0.3, "black"))
    tabla_destino = ft.DataTable(columns=[ft.DataColumn(ft.Text("DESTINATARIOS"))],border=ft.border.all(0.3, "black"))

    ######################################################## Elegir nuevas Filas x Página
    filas_x_pag = ft.TextField(tooltip="Máximo 60",text_align=ft.TextAlign.CENTER,width=60,value=str(nuevo_rows_per_page),on_submit=lambda e: set_rows_per_page(e.control.value))

    
    ######################################################## TABLA CON PAGINADO, TOTAL FILAS Y PAGINASL
    ############################################### Paginas y total filas
    paginas = ft.Text(f"")
    total_filas = ft.Text(f"",weight=ft.FontWeight.BOLD)
    

    ######################################################## Botones de paginación
    in_button = ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT, on_click=in_page,tooltip="Primera página")
    prev_button = ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT,on_click=prev_page, tooltip="Página anterior")
    next_button = ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT,on_click=next_page,tooltip="Página siguiente")
    fin_button = ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_RIGHT,on_click=fin_page,tooltip="Última página")

    tabla = ft.Card(
        ft.Container(
            ft.Column(spacing=2,controls=[
                    ft.Row([ft.Text("FALTANTES por PAE",weight=ft.FontWeight.BOLD,size=20)],alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([
                            ft.Row(controls=[in_button,prev_button, paginas, next_button, fin_button]),
                            ft.Row(controls=[filas_x_pag, ft.Text("filas por página")]),
                            ft.Row(controls=[total_filas])
                            ],alignment=ft.MainAxisAlignment.CENTER),
                    ft.Column([ft.Row([table_i],scroll="always")],scroll="always",expand=True)])
            , padding=10
        ),
        elevation=5, margin=10)

    # TABLA DE DESTINATARIOS
    total_destinatarios_label = ft.Text(f"",weight=ft.FontWeight.BOLD,size=17)
    tabla_d = ft.Container(
                ft.Column(spacing=2,controls=[
                        total_destinatarios_label,
                        ft.Column([tabla_destino],scroll="always",expand=True)]
                        )
                , padding=ft.padding.only(bottom=2), height=195,visible=False
            )

    ######################################################## Boton para Cargar y Empezar de Nuevo
    etiqueta = ft.Text(value="Primero suba los archivos necesarios", weight=ft.FontWeight.BOLD)
    boton_subir = ft.IconButton(tooltip="Upload File", icon= ft.Icons.UPLOAD_ROUNDED,icon_size=30, on_click=show_cupertino_action_sheet)
    boton_reiniciar = ft.IconButton(tooltip="Delete File",icon= ft.Icons.RESTART_ALT_ROUNDED,icon_size=30, icon_color="red",on_click=borrar_archivo)
    
    ######################################### Botones Subir, Empezar de nuevo
    upload= ft.Container(
        ft.Row([
            ft.Row([ft.Text("SUBIR ARCHIVO"),boton_subir],spacing=1),
            ft.Row([ft.Text("EMPEZAR DE NUEVO"),boton_reiniciar],spacing=1),
            etiqueta
        ],alignment=ft.MainAxisAlignment.START,spacing=30)
    )

    ########################################################## ACCIÓN AL PRESIONAR BOTON SUBIR ARCHIVOS

    action_sheet = ft.CupertinoActionSheet(
        #title=ft.Text("SUBIR ARCHIVOS"),
        message=ft.Text("Elige los documentos en formato (.txt) a subir.",size=15,color="blue",weight=ft.FontWeight.BOLD),
        cancel=ft.CupertinoActionSheetAction(
            is_destructive_action=True,
            content=ft.Text("CERRAR"),
            on_click=handle_click,
            
        ),
        actions=[
            ft.CupertinoActionSheetAction(
                content=ft.Text("SUBIR DETALLADO ALUMNOS",weight=ft.FontWeight.BOLD), # DETALLADO ALUMNOS
                is_default_action=True,
                #is_destructive_action=True,
                on_click=abrir_dialogo_archivo,
                
            ),
            ft.CupertinoActionSheetAction(
                content=ft.Text("SUBIR ANEXO 13A",weight=ft.FontWeight.BOLD), # ANEXO 13A
                is_default_action=True,
                #is_destructive_action=True,
                on_click=abrir_dialogo_archivo_anexo,
            ),
        ],
    )
    ######################################### Botón estilo Cupertino
    bottom_sheet = ft.CupertinoBottomSheet(action_sheet) 
    
    ######################################################## BOTONES para guardar el archivo en una carpeta específica
    descargar_button=ft.IconButton(tooltip="Descargar Reportes",icon=ft.Icons.DOWNLOAD_ROUNDED, on_click=descargar_archivo,icon_size=30,disabled=True)
    seleccionar_carpeta_button = ft.ElevatedButton("¿Dónde Desea Guardar el Archivo?", on_click=seleccionar_carpeta, disabled=True)
    status_label = ft.Text(value="")

    ############################### Contenedor con los elementos elegir carpeta y boton descargar archivo
    download_bottom = ft.Row([seleccionar_carpeta_button,descargar_button,correo_prueba],visible=False)
 
    ############################### ETIQUETA DE TEXTO
    status_label = ft.Text(value="",weight=ft.FontWeight.BOLD,visible=False)

    ######################################################## Agregar el FilePicker a la página. Necesario para poder cargar archivos
    page.overlay.append(archivo_txt_dialog)
    page.overlay.append(archivo_txt_dialog_anexo)
    
    page.add(ft.ResponsiveRow([
        upload,
        tabla,
        ft.Row([ft.Column([status_label,download_bottom,login_datos],spacing=1),tabla_d],alignment=ft.MainAxisAlignment.CENTER),
        
        ]))


######################################################## Ejecutar la aplicación
#if __name__ == "__main__":
#    ft.app(target=validacion)
