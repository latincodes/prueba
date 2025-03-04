# APPEND, pd.dataframe (convertir a dataframe), fillna,sort_value, append,

######################################################## LIBRERIAS
import pandas as pd
import flet as ft

######################################################## Definir antes de ejecutar para evitar conflictos
rows_per_page = 5
df_emp = pd.DataFrame()
mostrar_table= True
titulo_dinamico=  ft.Text(value="TABLA NORMAL",weight=ft.FontWeight.BOLD,size=20)

def main(page: ft.Page):
    import os
    page.title = "GOBERNACIÓN DE CASANARE - Realizar Consultas"

    carpeta_descarga = os.path.expanduser("~")  # Carpeta de descarga predeterminada

    ######################################################## DECLARAR VARIABLES GLOBALES
    global sort_dropdown, columns_dropdown, table_i,table_d, column_checkboxes, asc_desc, current_page, subir,nuevo_rows_per_page
    current_page = 0
    nuevo_rows_per_page = rows_per_page

    ######################################################################################################################### CONTROLADOR  
    ######################################################## FUNCIÓN PARA CARGAR EL ARCHIVO
    def cargar_archivo(e):
        global df_emp
        if archivo_txt_dialog.result.files is not None: 
            archivo = archivo_txt_dialog.result.files[0].path
        else: 
            archivo = None

        if archivo is not None and archivo != "":
            try:
                ######################################################## MODELO
                column_checkboxes.visible=True
                botones.visible=True
                df_emp = pd.read_csv(archivo, delimiter=';', encoding='latin1')        
                
                ######################################################## CONTROLADOR                
                # Actualizar opciones de columnas en column_checkboxes
                column_checkboxes.content.controls[1].controls.clear()  # Limpiar checkboxes anteriores
                for col in df_emp.columns:
                    column_checkboxes.content.controls[1].controls.append(ft.CupertinoCheckbox(visible=True,check_color="black",active_color="blue",label=col, value=False, on_change=lambda e, c=col: [update_table(e, page), update_filters_visibility(page)]))
                
                # Actualizar opciones en sort_dropdown
                sort_dropdown.options = [ft.dropdown.Option(col) for col in df_emp.columns]
                if df_emp.columns.any():
                    sort_dropdown.value = df_emp.columns[0]  # Seleccionar primera columna por defecto

                columns_dropdown.options = [ft.dropdown.Option(col) for col in df_emp.columns]
                if df_emp.columns.any():
                    columns_dropdown.value = df_emp.columns[0]  # Seleccionar primera columna por defecto
                
                toggle_button.controls[1].tooltip="Primero Seleccione las Columnas a Mostrar"
                etiqueta.value = "Archivo cargado exitosamente."
                asc_desc.disabled=False
                tabla.visible=True
                update_table(e, page)
                
                
            except Exception as ex:
                etiqueta.value = "Error al cargar el archivo"
        else:
            etiqueta.value = "No se seleccionó ningún archivo"
        page.update()  # Actualizar la interfaz
        

    ######################################################## FUNCION DESCARGAR ARCHIVO
    def descargar_archivo(e):
        nonlocal carpeta_descarga
        global sorted_df, table_data, table_i, table_d
        if nombre_doc.value:
            if table_i and table_i.rows or table_d and table_d.rows: # CONTROLADOR
                try: 
                    columnas = [col.label.value for col in table_i.columns]
                    columnas_dinamicas = [col.label.value for col in table_d.columns]
                    
                    if mostrar_table:
                        # TABLA NORMAL
                        df_exportado = pd.DataFrame(sorted_df, columns=columnas)                         # MODELO
                        output_file = os.path.join(carpeta_descarga, f"{nombre_doc.value}.csv")
                        df_exportado.to_csv(output_file, sep=';', encoding='latin1', index=False)        # MODELO
                        status_label.value = f"Tabla Normal guardada en: {carpeta_descarga}"             # CONTROLADOR
                    
                    else:
                        # TABLA DINÁMICA
                        df_dinamico = pd.DataFrame(table_data, columns = columnas_dinamicas)            # MODELO
                        output_dinamico = os.path.join(carpeta_descarga, f"{nombre_doc.value}.csv")
                        df_dinamico.to_csv(output_dinamico, sep=';', encoding='latin1', index=False)    # MODELO
                        status_label.value = f"Tabla Dinámica guardada en: {carpeta_descarga}"          # CONTROLADOR
                    
                    # CONTROLADOR
                    descargar_button.icon=ft.Icons.DOWNLOAD_DONE_ROUNDED
                    descargar_button.disabled=True
                    nombre_doc.disabled=True
                    page.update()
                except Exception as ex:
                    status_label.value = f"Error al guardar el archivo: {str(ex)}"
                    page.update()

    ######################################################## FUNCIÓN SELECCIONAR CARPETA DONDE SE GUARDARÁ EL ARCHIVO 
    def seleccionar_carpeta(e):
        nonlocal carpeta_descarga
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()  # Ocultar la ventana principal de Tkinter
            root.lift()  # Levantar la ventana al frente
            root.attributes("-topmost", True)  # Mantener la ventana al frente
            carpeta_descarga = filedialog.askdirectory()
            if carpeta_descarga:
                status_label.value = f"Carpeta seleccionada: {carpeta_descarga}"
                descargar_button.icon=ft.Icons.DOWNLOAD_ROUNDED
                descargar_button.disabled = False
                nombre_doc.disabled = False
            else:
                status_label.value = "No se seleccionó ninguna carpeta."

            page.update()
        except:
            status_label.value = "Error al seleccionar carpeta"

    ######################################################## Función para abrir el cuadro de diálogo de selección de archivo (seleccionar archivo txt)
    def abrir_dialogo_archivo(e):
        archivo_txt_dialog.pick_files(allowed_extensions=['txt', 'csv']) 
    ############################### El archivo seleccionado "ejecuta" la función cargar_archivo
    archivo_txt_dialog = ft.FilePicker(on_result=cargar_archivo)
    
    ######################################################## FUNCION BORRAR ARCHIVO
    def borrar_archivo(e):
        try:
            global df_emp, table_i
            etiqueta.value = "Por favor, suba el archivo en formato (.txt) (.csv)"
            tabla.visible=False
            df_emp = pd.DataFrame()
            column_checkboxes.visible=False
            column_checkboxes.content.controls[1].controls.clear()
            sort_dropdown.options = [ft.dropdown.Option(col) for col in df_emp.columns]
            columns_dropdown.options = [ft.dropdown.Option(col) for col in df_emp.columns]

            download_bottom.visible=False

            filter_row.controls.clear()
            descargar_button.disabled=True
            nombre_doc.disabled=True
            descargar_button.icon =icon=ft.Icons.DOWNLOAD_ROUNDED
            status_label.value=""
            total_filas.value = ""
            paginas.value = ""
            table_i.rows.clear()
            table_i.columns = [ft.DataColumn(ft.Text("SUBA UN ARCHIVO"))]
            table_d.rows.clear()
            table_d.columns = [ft.DataColumn(ft.Text("TABLA DINAMICA"))]
            columns_dropdown.visible=False
            toggle_button.visible=False
            #toggle_button.controls[1].icon=ft.Icons.AUTO_MODE_ROUNDED
        except:
            status_label.value = "Error al eliminar archivo"
        page.update()


    ######################################################## Funcion para aplicar los filtros al dataframe (df) y así luego mostrarlo en la tabla (update_table)

    def apply_column_filters(df_emp):
        """Aplica los filtros seleccionados en los checkboxes a las columnas del DataFrame, permitiendo filtrar por valores vacíos."""
        try:
            for col, selected_values in selected_filters.items():
                if selected_values:
                    # Si "Vacío/NaN" está seleccionado, filtrar filas donde la columna esté vacía o sea NaN
                    if "Vacío/NaN" in selected_values:
                        df_emp = df_emp[df_emp[col].isna() | (df_emp[col] == "")]
                    else:
                        df_emp = df_emp[df_emp[col].isin(selected_values)]
            return df_emp
        except Exception as e:
            return df_emp  
    ######################################################################################################################### VISTA
    ######################################################## Función para buscar las columnas a seleccionar
    def column_search(e, page):
        try:
            # Filtra dinámicamente las columnas a seleccionar basadas en la búsqueda
            search_text = e.control.value.lower()
            for checkbox in column_checkboxes.content.controls[1].controls:  # Lista de checkboxes
                checkbox.visible = search_text in checkbox.label.lower()
        
        except:
            status_label.value = "Error al buscar las columnas a seleccionar"
        page.update()

    ######################################################## Función para actualizar la tabla en la GUI
    def update_table(e, page):
        global pivot_df, sorted_df, table_data, filtered_df, total_pages, total_rows, total_pages
        if df_emp is not None:
            toggle_button.controls[1].disabled=False         
            try:
                sort_by = sort_dropdown.value

                if asc_desc.value:
                    ascending_order = True if asc_desc.value == 'Menor a Mayor' else False
                else:
                    dlg = ft.AlertDialog(icon=ft.Icon(name=ft.Icons.WARNING_OUTLINED, size=70, color=ft.Colors.RED),bgcolor=ft.Colors.WHITE, alignment=ft.alignment.center,title=ft.Text("Primero elija el orden", color=ft.Colors.BLACK87, weight=ft.FontWeight.BOLD))
                    page.open(dlg)
                    return

                filtered_df = apply_column_filters(df_emp)
                sorted_df = filtered_df.sort_values(by=sort_by,ascending=ascending_order)
                
                if table_i in tablas_container.content.controls:
                    filtrar_por.visible=True
                    download_bottom.visible=True
                    toggle_button.visible=True
                    toggle_button.controls[1].tooltip="Presione para mostrar la TABLA DINÁMICA"
                    columns_dropdown.visible=False
                    selected_columns = [cb.label for cb in column_checkboxes.content.controls[1].controls if isinstance(cb, ft.CupertinoCheckbox) and cb.value]
                    
                    if not selected_columns:
                        filtrar_por.visible=False
                        download_bottom.visible=False
                        toggle_button.visible=False
                        table_i.rows.clear()
                        table_i.columns = [ft.DataColumn(ft.Text("ELIJA LAS COLUMNAS"))]
                        table_i.update()
                        return
                    
                    # Actualizar la tabla con las filas de la página actual
                    start_row = current_page * nuevo_rows_per_page
                    end_row = start_row + nuevo_rows_per_page
                    page_data = sorted_df.iloc[start_row:end_row]

                    table_i.rows.clear()
                    table_i.columns = [ft.DataColumn(ft.Text(col)) for col in selected_columns]
                    

                    for _, row in page_data.iterrows():
                        table_i.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(row[col]),selectable=True)) for col in selected_columns]))
                    
                    # Paginación
                    total_rows = len(sorted_df)
                    total_pages = (total_rows // nuevo_rows_per_page) + (1 if total_rows % nuevo_rows_per_page > 0 else 0)

                ###########################
                ########################### TABLA_DINAMICA  
                if table_d in tablas_container.content.controls:
                    filtrar_por.visible=True
                    download_bottom.visible=True
                    toggle_button.visible=True
                    toggle_button.controls[1].tooltip="Presione para mostrar la TABLA NORMAL"
                    columns_dropdown.visible=True
                    valor_n = "APELLIDO1"
                    columnas_dinamica = columns_dropdown.value if columns_dropdown.value != valor_n else None
                    selected_columns_d = [cb.label for cb in column_checkboxes.content.controls[1].controls if isinstance(cb, ft.CupertinoCheckbox) and cb.value and cb.label != columnas_dinamica and cb.label != valor_n]

                    if not selected_columns_d:
                        filtrar_por.visible=False
                        download_bottom.visible=False
                        toggle_button.visible=False
                        columns_dropdown.visible=False
                        table_d.rows.clear()
                        table_d.columns = [ft.DataColumn(ft.Text("TABLA DINAMICA"))]
                        table_d.update()
                        return
                    
                    ############################################################## TABLA DINAMICA
                    pivot_df = filtered_df.pivot_table(values=valor_n, 
                                    index=selected_columns_d, 
                                    columns=columnas_dinamica, 
                                    aggfunc='count', 
                                    fill_value=0,
                                    margins=True,
                                    margins_name='Total',
                                    sort=True
                                    )
 
                    # Limitar a 100 columnas dinamicas
                    pivot_df = pivot_df.iloc[:, :100]
                    # Convertir los niveles del índice en columnas separadas
                    pivot_df = pivot_df.reset_index()  # Aquí descompone el índice jerárquico en columnas normales
                    
                    pivot_df = pivot_df.fillna("")          ### reemplazar nan por "nada, vacío"
                    column_names = list(pivot_df.columns)
                    table_data = pivot_df.values.tolist()

                    # Paginacion
                    start_row = current_page * nuevo_rows_per_page
                    end_row = start_row + nuevo_rows_per_page

                    table_d.columns.clear()
                    table_d.columns.extend([ft.DataColumn(ft.Text(col)) for col in column_names])
                    paginated_data = table_data[start_row:end_row]

                    # Actualizar filas de la tabla
                    table_d.rows.clear()
                    for row in paginated_data:
                        table_d.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell),selectable=True)) for cell in row]))
                    # Paginación
                    total_rows = len(table_data)
                    total_pages = (total_rows // nuevo_rows_per_page) + (1 if total_rows % nuevo_rows_per_page > 0 else 0)



                
                # Mostrar pagina actual, total de paginas y total de filas
                paginas.value = f"{current_page+1}/{total_pages}"
                total_filas.value = f"Total de filas: {total_rows}"

                page.update()
            
            except Exception as ex:
                dlg = ft.AlertDialog(icon=ft.Icon(name=ft.Icons.WARNING_OUTLINED, size=70, color=ft.Colors.RED),bgcolor=ft.Colors.WHITE, alignment=ft.alignment.center,title=ft.Text("Error actualizando tabla", color=ft.Colors.BLACK87, weight=ft.FontWeight.BOLD))
                page.open(dlg)


    ######################################################## Función para filtrar las columnas que han sido seleccionadas según lo buscado por el usuario. 
    filter_row = ft.Row() 
    filter_containers = {}
    def update_filters_visibility(page):
        """Genera los checkboxes dinámicos para filtrar cada columna"""  
        try:
            filter_row.controls.clear()
            selected_columns = [
                cb.label for cb in column_checkboxes.content.controls[1].controls 
                if isinstance(cb, ft.CupertinoCheckbox) and cb.value
            ]

            for col in selected_columns:
                all_unique_values = df_emp[col].dropna().unique()  # Obtener todos los valores únicos sin límite
                all_unique_values = sorted(all_unique_values, key=lambda x: (str(x).isnumeric(), str(x)))
                limited_values = all_unique_values[:150]  # Mostrar solo los primeros 150

                prev_selected = selected_filters.get(col, set())  # Valores seleccionados previamente
                search_field = ft.TextField(
                    width=150, height=35, text_size=12,
                    hint_text=f"Filtrar por {col}", 
                    on_change=lambda e, c=col, values=all_unique_values: filter_search(e, c, values, page)
                )

                checkboxes = []
                # Verificar si hay valores vacíos en la columna y agregarlos al principio
                has_nan = df_emp[col].isna().sum() > 0 or (df_emp[col] == "").sum() > 0
                if has_nan:
                    checkboxes.append(ft.Checkbox(
                        width=150, label="Vacíos",
                        value=("Vacío/NaN" in prev_selected), 
                        on_change=lambda e, v="Vacío/NaN", c=col: toggle_filter(e, v, c, page)
                    ))

                # Agregar los primeros 500 valores únicos
                checkboxes += [
                    ft.Checkbox(
                        width=160, tooltip=str(val),
                        label=str(val)[:14] + "..." if len(str(val)) > 14 else str(val),
                        value=(val in prev_selected), 
                        on_change=lambda e, v=val, c=col: toggle_filter(e, v, c, page)
                    ) for val in sorted(limited_values)
                ]

                filter_containers[col] = ft.Column(controls=[search_field] + checkboxes, scroll="always", height=150)

                filter_row.controls.append(ft.Container(
                    content=ft.Column([filter_containers[col]]), padding=ft.padding.only(right=5)
                ))

        except Exception as e:
            dlg = ft.AlertDialog(
                icon=ft.Icon(name=ft.Icons.WARNING_OUTLINED, size=70, color=ft.Colors.RED),
                bgcolor=ft.Colors.WHITE, alignment=ft.alignment.center,
                title=ft.Text("Error actualizando filtros", color=ft.Colors.BLACK87, weight=ft.FontWeight.BOLD)
            )
            page.open(dlg)
            print(f"{e}")
            pass

        page.update()
    ################################################ Función actualizar (filtrar) la tabla con los valores seleccionados de cada columna. 
    ################################################ Además actualiza dinámicamente el contenido de cada checkbox de cada columna, según los valores ya seleccionados.
    selected_filters = {col: set() for col in df_emp.columns}
    #### CONTROLADOR
    def toggle_filter(e, value, col, page):
        # Agrega o elimina valores seleccionados del filtro
        if col not in selected_filters:
            selected_filters[col] = set()  # Asegurar que la columna exista en el diccionario

        if e.control.value:  # Si el checkbox está marcado
            selected_filters[col].add(value)
        else:  # Si se desmarca
            selected_filters[col].discard(value)
        
        update_table(e,page)  # Actualizar tabla con los filtros aplicados
    
    ######################################################## Función para buscar los valores de cada columna, basado en lo buscado por el usuario
    def filter_search(e, col, all_unique_values, page):
        """Filtra dinámicamente los checkboxes de una columna basada en la búsqueda"""
        search_text = e.control.value.lower()
        checkboxes_list = filter_containers[col].controls[1:]  # Omitir el campo de búsqueda
        
        # Mostrar solo los valores que coincidan con la búsqueda
        found_values = [cb for cb in checkboxes_list if search_text in cb.tooltip.lower()]
        
        # Si el valor buscado no está en los primeros 500, pero sí en el DataFrame, agregarlo
        if search_text and not found_values:
            matching_values = [val for val in all_unique_values if search_text in str(val).lower()]
            for val in matching_values:
                if val not in [cb.tooltip for cb in checkboxes_list]:  # Evitar duplicados
                    new_checkbox = ft.Checkbox(
                        width=160, tooltip=str(val),
                        label=str(val)[:14] + "..." if len(str(val)) > 14 else str(val),
                        value=False,
                        on_change=lambda e, v=val, c=col: toggle_filter(e, v, c, page)
                    )
                    filter_containers[col].controls.append(new_checkbox)

        # Ocultar los que no coincidan con la búsqueda
        for checkbox in checkboxes_list:
            checkbox.visible = search_text in checkbox.tooltip.lower()
        
        page.update()

    ######################################################## Función para cambiar de tabla normal a tabla dinámica 
    def toggle_tables(e):
        global mostrar_table, titulo_dinamico
        
        mostrar_table = not mostrar_table
        tablas_container.content=ft.Row([table_i if mostrar_table else table_d],scroll="always")
        if not mostrar_table:
            botones.visible=False
            nombre_doc.value = "Tabla_Dinamica"
            titulo_dinamico.value="TABLA DINAMICA"
            columns_dropdown.visible=True
            toggle_button.controls[0].value = "Cambiar a Tabla Normal:"
            toggle_button.controls[1].icon=ft.Icons.AUTORENEW_ROUNDED
        else:
            botones.visible=True
            nombre_doc.value = "Tabla_Normal"
            titulo_dinamico.value="TABLA NORMAL"
            columns_dropdown.visible=False
            toggle_button.controls[0].value = "Cambiar a Tabla Dinámica:"
            toggle_button.controls[1].icon=ft.Icons.AUTO_MODE_ROUNDED
        update_table(e,page)

    ######################################################## Funciones para la paginación
    def in_page(e):  # primera página
        global current_page
        current_page = 0
        update_table(e, page)

    def prev_page(e): # página anterior
        global current_page
        if current_page > 0:
            current_page -= 1
            update_table(e, page)

    def next_page(e): # página siguiente
        global current_page
        try:
            if current_page < total_pages - 1:
                current_page += 1
                update_table(e, page)
        except:
            pass

    def fin_page(e): # última página
        global current_page
        try:
            current_page = total_pages - 1
            update_table(e, page)
        except:
            pass    
    
    ######################################################## Función para asignar nuevo valor de FILAS por PÁGINA
    def set_rows_per_page(valorr: str):
        global nuevo_rows_per_page
        try:
            nuevo_rows_per_page = int(valorr) if 1 <= int(valorr) <= 60 else rows_per_page
        except:
            nuevo_rows_per_page = rows_per_page
    
        filas_x_pag.value = str(nuevo_rows_per_page)
        in_page(None)
        update_table(None, page)
    

   
    ########################################################
    ########################################################
    ########################################################
    ######################################################## Boton para Cargar y Eliminar el archivo
    etiqueta = ft.Text(value="Por favor, suba el archivo en formato (.txt) (.csv)", weight=ft.FontWeight.BOLD)
    upload= ft.Container(
        ft.Column([
            ft.Row([ft.Text("SUBIR ARCHIVO"),ft.IconButton(tooltip="Upload File", icon= ft.Icons.UPLOAD_ROUNDED,icon_size=30, on_click=abrir_dialogo_archivo)]),
            ft.Row([ft.Text("ELIMINAR ARCHIVO"),ft.IconButton(tooltip="Delete File",icon= ft.Icons.DELETE,icon_size=30, icon_color="red",on_click=borrar_archivo)]),
            etiqueta
        ])
    )

    ######################################################## Text para buscar las columnas a mostrar
    search_column = ft.TextField(width=150,text_size=12,hint_text=f"Buscar columna", on_change=lambda e: column_search(e, page))

    ######################################################## Contenedor para seleccionar las columnas a mostrar de la tabla normal y la tabla dinámica (index de pivot_df)
    column_checkboxes = ft.Container(visible=False,padding=8, border=ft.border.all(1.5), border_radius=10, height=140, expand=True,
        content=
            ft.Column([
                ft.Row([ft.Text("SELECCIONE LAS COLUMNAS A MOSTRAR", weight=ft.FontWeight.BOLD),search_column]),
                ft.Row(scroll="always",height=50,controls=[ft.CupertinoCheckbox(visible=False,check_color="black",active_color="blue",label=col, value=False, on_change=lambda e, c=col:[update_table(e,page),update_filters_visibility(page)]) for col in df_emp.columns])
        ])
    )

    ######################################################## BOTONES DE FILTRAR POR y ORDENAR POR
    asc_desc = ft.Dropdown(text_size=14,width=166,label="De", options=[ft.dropdown.Option("Menor a Mayor"), ft.dropdown.Option("Mayor a Menor")],value="Menor a Mayor",on_change=lambda e: update_table(e, page),disabled=True)    
    sort_dropdown = ft.Dropdown(text_size=14,width=166,label="Ordenar por",on_change=lambda e: update_table(e, page), options=[ft.dropdown.Option(col) for col in df_emp.columns], value=df_emp.columns[0] if not df_emp.empty else None)
    botones = ft.Container(ft.Column([sort_dropdown,asc_desc])) 

    ######################################################## BOTONES para elegir carpeta, elegir nombre y guardar el archivo
    seleccionar_carpeta_button = ft.ElevatedButton("¿Dónde Desea Guardar el Archivo?", on_click=seleccionar_carpeta, disabled=False)  # elegir carpeta
    nombre_doc = ft.TextField(value="Tabla_Normal",text_align=ft.TextAlign.CENTER,width=150,label="Elija un nombre",disabled=True)    # elegir nombre
    descargar_button=ft.IconButton(tooltip="Descargar Archivo",icon=ft.Icons.DOWNLOAD_ROUNDED, icon_color="green", on_click=descargar_archivo,icon_size=30,disabled=True) #descargar
    status_label = ft.Text(value="") # Iniciar la etiqueta vacía
    ############################################# Contenedor con los elementos elegir carpeta, elegir nombre y boton descargar archivo
    download_bottom = ft.Container(ft.Row(controls=[seleccionar_carpeta_button,nombre_doc,descargar_button,status_label],spacing=20),expand=True, padding=ft.padding.only(top=7),visible=False)
    
    ######################################################## Definir inicialmente TABLA NORMAL y TABLA DINÁMICA
    table_i = ft.DataTable(columns=[ft.DataColumn(ft.Text("PRIMERO SUBA EL ARCHIVO"))],border=ft.border.all(0.3, "black"))   # tabla normal
    table_d = ft.DataTable(columns=[ft.DataColumn(ft.Text("ESPERANDO"))],border=ft.border.all(0.3, "black"))                 # tabla dinámica

    ######################################################## TABLA CON PAGINADO, TOTAL FILAS Y PAGINAS. Y  FILTRAR EN TIEMPO REAL
    ################################ Botones de paginación
    in_button = ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT, on_click=in_page,tooltip="Primera página")
    prev_button = ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT,on_click=prev_page, tooltip="Página anterior")
    next_button = ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT,on_click=next_page,tooltip="Página siguiente")
    fin_button = ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_RIGHT,on_click=fin_page,tooltip="Última página")

    ############################################# Elegir nuevas Filas x Página
    filas_x_pag = ft.TextField(tooltip="Máximo 60",text_align=ft.TextAlign.CENTER,width=60,value=str(nuevo_rows_per_page),on_submit=lambda e: set_rows_per_page(e.control.value))

    paginas = ft.Text(f"") ################## Inicializar las páginas (start-end)

    ############################################# Total de filas de la tabla
    total_filas = ft.Text(f"",weight=ft.FontWeight.BOLD)

    ############################################# Inicializar container con la tabla normal, permitiendo cambiar a la tabla dinámica
    tablas_container = ft.Container(content=ft.Row(controls=[table_i], scroll="always"))

    ############################################# Botón para cambiar de tabla normal a tabla dinámica
    toggle_button = ft.Row([ft.Text("Cambiar a Tabla Dinámica:",weight=ft.FontWeight.BOLD,size=16),ft.IconButton(disabled=True,tooltip="Primero Suba el Archivo", icon= ft.Icons.AUTO_MODE_ROUNDED,icon_color="blue",icon_size=33, on_click=toggle_tables)],visible=False,spacing=0)
    
    ############################################# Opciones para dejar elegir al usuario las columnas dinámicas (columns de pivot_df)
    columns_dropdown = ft.Dropdown(width=200,visible=False,label="Tabla Dinámica",on_change=lambda e: update_table(e, page), options=[ft.dropdown.Option(col) for col in df_emp.columns], value=df_emp.columns[0] if not df_emp.empty else None)

    ############################################# Contenedor con TODOS LOS ELEMENOS DE LAS TABLAS
    filtrar_por = ft.Container(border_radius=10,border=ft.border.all(1.5),padding=5,content=ft.Row([filter_row],scroll="always"),expand=True,visible=False)
    tabla = ft.Card(
        ft.Container(
            ft.Column(spacing=2,controls=[
                    ft.Row([botones,filtrar_por,
                            ]),
                    ft.Row([
                            ft.Container(ft.Row([in_button,prev_button, paginas, next_button, fin_button,filas_x_pag, ft.Text("filas por página"),total_filas],alignment=ft.MainAxisAlignment.CENTER),expand=True,padding=ft.padding.only(bottom=10))
                            ]),
                    ft.Column(controls=[ft.Row([titulo_dinamico,columns_dropdown],alignment=ft.MainAxisAlignment.CENTER),
                                        ft.Row([tablas_container],scroll="always")],scroll="always",expand=True)
            ])
            , padding=10
        ),
        elevation=5,margin=10,visible=False)
    



    ############ Necesario para poder cargar archivos
    page.overlay.append(archivo_txt_dialog)

    ######################################################## Agregar elementos a la página
    page.add(ft.ResponsiveRow([ft.Column([
        ft.Row([upload,column_checkboxes]),
        ft.Row([ft.Container(ft.Row([download_bottom]),expand=True),
                ft.Container(ft.Row([toggle_button],alignment=ft.MainAxisAlignment.END))]),
        tabla
        ],spacing=2.5)])
    )

######################################################## Ejecutar la aplicación
#if __name__ == "__main__":
#    ft.app(target=main)