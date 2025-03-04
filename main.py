import flet as ft
from consultas import main as consulta_app
from reportes import validacion as pae_app
def main(page: ft.Page):
    
    consulta_app(page)  #### Iniciar primero la pagina de CONSULTAS
    #page.title = "GOBERNACIÓN DE CASANARE - Realizar Consultas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.maximized = True
    page.scroll = "adaptive"  # Permite desplazamiento si es necesario
    
    ########################################################################################## 🔹 Función para cambiar el tema CLARO/OSCURO
    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if theme_switch.value else ft.ThemeMode.LIGHT
        page.update()
    # 🔹 Crear el Switch para cambiar el tema
    theme_switch = ft.Switch(value=False,on_change=toggle_theme,thumb_color="black",thumb_icon={ft.ControlState.DEFAULT: ft.Icons.LIGHT_MODE_ROUNDED,ft.ControlState.SELECTED: ft.Icons.DARK_MODE})

    def cerrar_about(e):
        """ Cierra el diálogo y vuelve a la página de Consultas. """
        page.close(about_dialog)
        e.control.selected_index = 0
        page.navigation_bar.content.controls[0].content.selected_index = 0 
        on_nav_change(e)

    def highlight_link(e):
        e.control.color = "blue " if e.data == "true" else "black"
        e.control.update()

    about_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Acerca de CONSULTAS PAE", size=20, weight="bold"),
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Manual de Usuario", size=16, weight="bold", text_align="center"),
                    ft.ElevatedButton("Ver Manual", color="black",bgcolor=ft.Colors.TERTIARY_CONTAINER, elevation=2, url="https://github.com/latincodes/Manual-de-Usuario-Consultas-PAE/", on_hover=highlight_link),


                    ft.Divider(height=20, thickness=1),

                    ft.Text("Descripción:", size=16, weight="bold"),
                    ft.Column([
                        ft.Text("Esta es una aplicación creada con el fin de facilitar las consultas de los reportes planos del SIMAT y generar tablas personalizadas.",size=14, text_align=ft.TextAlign.CENTER),
                        ft.Text("Además, permite visualizar los estudiantes faltantes por parametrizar con la estrategia PAE en el SIMAT en las instituciones educativas del departamento de Casanare ",size=14, text_align=ft.TextAlign.CENTER),
                    ],spacing=1),

                    ft.Divider(height=20, thickness=1),

                    ft.Text("Desarrollador:", size=16, weight="bold"),
                    ft.Text("Yesid Mauricio Ramirez Rojas", weight="w600",size=14),
                    ft.Text("yesid.ramirez01@uptc.edu.co", selectable=True, size=14),

                    ft.Divider(height=20, thickness=1),

                    ft.Text("Tecnologías:", size=16, weight="bold"),
                    ft.Text("Python, Flet", size=14),

                    ft.Divider(height=20, thickness=1),

                    ft.Text("Licencia Propietaria:", size=16, weight="bold"),
                    ft.Text("Su uso está restringido exclusivamente al área de Cobertura Educativa e Instituciones Educativas de Casanare. No se permite su distribución ni modificación sin autorización expresa.", size=14,text_align=ft.TextAlign.CENTER),

                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll="always"
            ),
            padding=7, height=400, width=800
        ),
        alignment=ft.alignment.bottom_center,
        actions=[ft.TextButton("Cerrar", on_click=cerrar_about)],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    ########################################################################################## Funcion Que mostrar en Pantalla
    def on_nav_change(e):
        page.controls.clear()  # Limpiar los controles actuales de la página
        if e.control.selected_index == 0:  # Consultas
            consulta_app(page)

        elif e.control.selected_index == 1:  # Faltantes por PAE  (con autenticación)
            #page.open(dialog)
            pae_app(page)

        elif e.control.selected_index == 2:  # Acerca de
            page.title = "Acerca de la Aplicación CONSULTAS PAE"
            page.open(about_dialog)

        page.update()

    ########################################################################################## 🔹 BARRA DE NAGEVACIÓN 
    page.navigation_bar = ft.Container(
        content= ft.Row(
            controls=[
                ############ BOTONES DE NAGEVACION
                ft.Container(
                    border_radius=13,
                    expand=True,
                    content=ft.NavigationBar(
                        selected_index = 0,  # Página seleccionada por defecto
                        bgcolor=ft.Colors.INVERSE_PRIMARY,
                        indicator_color = ft.Colors.BLACK12,
                        destinations=[
                            ft.NavigationBarDestination(icon=ft.Icons.SEARCH, selected_icon=ft.Icons.PERSON_SEARCH,label="Realizar Consultas"),
                            ft.NavigationBarDestination(icon=ft.Icons.FASTFOOD_OUTLINED, selected_icon=ft.Icons.FASTFOOD_ROUNDED, label="Faltantes por PAE"),
                            ft.NavigationBarDestination(icon=ft.Icons.INFO_OUTLINED, selected_icon=ft.Icons.INFO_SHARP, label="Información"),
                        ],on_change=on_nav_change  # Agregar el listener para el cambio de navegación
                    )
                ),theme_switch ########## BOTON SWITCH CLARO/OSCURO
            ]
        )
    )

    page.add()


ft.app(main)

