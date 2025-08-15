# Aplicación de Deudores de Pensión Alimentaria

Esta aplicación permite gestionar deudores de pensión alimentaria, permitiendo registrar, buscar y visualizar detalles de los deudores en una interfaz de escritorio amigable. El proyecto sigue el patrón Modelo-Vista-Controlador (MVC) y utiliza principios de programación orientada a objetos.

## Características

- Registro de deudores con información esencial:
  - Apellido paterno
  - Apellido materno
  - Nombres
  - Tipo de documento (DNI, Carné de Extranjería, Pasaporte, Otros)
  - Número de documento
  - Fecha de registro (con selector de fecha)
  - Número de expediente judicial
  - Pensión mensual
  - Importe adeudado
  - Nombre completo del demandante

- Búsqueda de deudores por:
  1. Nombres y apellidos (al menos uno requerido)
  2. Tipo y número de documento (tipo de documento con combobox, validación de número)
  3. Periodo de fechas (fecha de inicio y fin con datepicker, validación de rango y límite de fecha actual)

- Visualización de la lista de deudores y detalle individual (detalle no editable).

- Interfaz visual mejorada con paleta de colores basada en `#9a1413` y soporte para temas modernos usando `ttkthemes`.

## Estructura del Proyecto

```
child-support-debtors-app
├── src
│   ├── models - 
│   │   └── debtor.py
│   ├── views
│   │   └── main_view.py
│   ├── controllers
│   │   └── debtor_controller.py
│   ├── services
│   │   └── file_storage.py
│   ├── utils
│   │   └── search.py
│   └── app.py
├── requirements.txt
└── README.md
```

## Instalación

1. Clona el repositorio:
   ```
   git clone git@github.com:milagroslujanc/REDAM_Grupo3.git
   ```

2. Ingresa al directorio del proyecto:
   ```
   cd child-support-debtors-app
   ```

3. Instala las dependencias requeridas:
   ```
   pip install -r requirements.txt
   ```

## Uso

Para ejecutar la aplicación, usa el siguiente comando en la terminal:

python src/app.py


Sigue las instrucciones en pantalla para registrar y gestionar deudores de pensión alimentaria.

## Licencia

Este proyecto está licenciado bajo MIT. Consulta el archivo LICENSE para más detalles.