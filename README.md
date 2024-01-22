# Introducción
Este repositorio corresponde al Sistema Integrado de Evaluación de Equipos de Procesos (SIEVEP), el cual corresponde al resultado del proyecto asociado a la **solicitud de servicio SS23147**. Con Python + Django + JQuery + HTMX se planteó migrar herramientas en Excel de evaluación de equipos de procesos, centralizándose en este software.

## :ledger: Índice

- [Información](#beginner-información)
- [Utilización](#zap-utilización)
  - [Instalación](#electric_plug-instalación)
- [Desarrollo](#wrench-desarrollo)
  - [Pre-Requisitos](#notebook-pre-requisitos)
  - [Ambiente de Desarrollo](#nut_and_bolt-ambiente-de-desarrollo)
  - [Estructura de Archivos](#file_folder-estructura-de-archivos)
  - [Datos de Deployment](#rocket-datos-de-deployment)  
- [Comunidad](#cherry_blossom-comunidad)
  - [Colaboración](#fire-colaboración)
  - [Branches](#cactus-branches)
- [FAQ](#question-faq)
- [Recursos](#page_facing_up-recursos)
- [Reconocimientos](#star2-reconocimientos)

##  :beginner: Información
Este proyecto corresponde al Sistema Integrado de Evaluación de Equipos de Procesos (SIEVEP). Este es un proyecto facturable realizado para Petroquímica de Venezuela S.A. Se utilizó de base las herramientas previamente desarolladas para la evaluación de: Intercambiadores de calor, Calderas, equipos auxiliares de calderas, turbinas de vapor y compresores. Se buscó migrar a software para efectos de escalabilidad y asimismo mejorar las herramientas donde fuera conveniente.

Este proyecto fue realizado con el framework Django de Python para el backend, JQuery y HTMX para el frontend (HTMX solo fue utilizado de calderas en adelante). Además se hizo uso de librerías especializadas para las propiedades termodinámicas, cálculos científicos y conversión de unidades debido a la gran versatilidad de Python en este sentido y la escalabilidad que Django ofrece. JQuery se utilizó inicialmente para el frontend pero luego se decidió utilizar HTMX debido a que era más seguro y confiable. **La estructura del código en intercambiadores es muy distinta al resto del proyecto**.

La base de datos utilizada es de MySQL, pero esta puede ser fácilmente cambiada al cambiar la conexión en el archivo **`settings.py`**.

Este proyecto se inició en septiembre del 2023 y se estima finalizar a mediados del 2024.

## :zap: Utilización
Este proyecto es de código cerrado y puede ser editado y utilizado únicamente por el personal autorizado de Indesca para este fin. Una vez finalizado será entregado e instalado en las instalaciones de Pequiven.

###  :electric_plug: Instalación
- Crear un ambiente virtual con `python -m venv ./env` y entrar al mismo.
- Instalar las dependencias con `pip install -r requirements.txt` en el ambiente virtual.
- Correr el comando `python manage.py migrate` de ser necesario.
- Correr el comando `python manage.py runserver` para iniciar el servidor de prueba.

###  :package: Comandos
Para ejecutar en ambiente de desarrollo:

```
$ python -m venv ./env
v pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver
```

##  :wrench: Desarrollo

### :notebook: Pre-Requisitos
- Instalar **Python 3.9**.
- Clonar el repositorio mediante la consola de git.
- Todas las dependencias contenidas en el archivo ``requirements.txt``

###  :nut_and_bolt: Ambiente de Desarrollo
El ambiente de desarrollo puede ser montado con lo mostrado en la sección de comandos. Se recomienda un mínimo de Windows 7 ya que Microsoft Windows Server 2007 es el ambiente de producción del mismo.

###  :file_folder: Estructura de Archivos
Aquí se encuentran los detalles de la estructura de archivos del proyecto.

| No | Carpeta / Archivo | Detalles 
|----|------------|-------|
| 1  | calculos/ | Archivos de los cálculos de evaluación y transformación de unidades
| 2  | intercambiadores/ | Aquí se encuentran las plantillas, vistas, modelos, comandos, migraciones y plantillas del módulo de intercambiadores
| 3  | reportes/ | Generador de reportes XLSX y PDF
| 4  | simulaciones_pequiven/ | Directorio principal del proyecto
| 5  | static/ | Archivos estáticos
| 6  | templates/ | Plantillas generales
| 7  | templatetags/ | Etiquetas de las plantillas
| 8  | usuarios/ | Directorio del sistema de usuarios

Los archivos en formato .csv y .tsv pueden ser ignorados. Es data que se utilizó en su momento para migrarla a la base de datos.

### :rocket: Datos de Deployment
- Cambiar

## :cherry_blossom: Comunidad

Código cerrado y confidencial. Guiarse bajo los lineamientos aquí indicados.

 ###  :fire: Colaboración
Los únicos colaboradores del proyecto es el personal autorizado de Indesca. Por ahora, personal de Informática únicamente con apoyo de personal de Procesos / Aplicaciones / OOPP.

 ### :cactus: Branches

1. **`develop`** es la branch de desarrollo. Hacer todos los desarrollos partiendo de esta.

2. **`master`** es la branch principal. Solo código estable y testeado debe estar acá.

3. Toda branch adicional deberá de ser eliminada una vez sus cambios lleguen de develop a master.

**Pasos para crear nuevas branches**

1. Crear la branch localmente y actualizar la misma mediante push a esa branch diariamente.
2. Una vez estén listos, hacer una pull request a **`develop`**.

## :question: FAQ
Colocar FAQs al finalizar proyecto.

## :star2: Reconocimientos
- **Fausto Rosales**: Ingeniero de Informática en Indesca (Gestión)
- **Biaggi Zambrano**: Ingeniero en Informática en Indesca (Manual de Usuario)
- **Diego Faria**: Ingeniero en Informática de Indesca (Programación)
- **Edgar Salas**: Ingeniero de Procesos que apoyó en la parte técnica (Modelo Inicial y bibliografía)
- **Alejandra Romero**: Tesista de OOPP que apoyó en la parte técnica (Cambio de Fase)
- **Nicole Pirela**: Ingeniero de Procesos que apoyó en la parte técnica (Cambio de Fase)
