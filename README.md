# Introducción
Este repositorio corresponde a la página web de Indesca, la cual será actualizada de acuerdo a los requerimientos del departamento de Asuntos Públicos. Este desarrollo empezó en julio de 2023 pero el repositorio fue creado el 22 de enero de 2024.

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
Este proyecto corresponde con la página web de Indesca. Este es un proyecto interno no facturable. Incluye información general de la empresa así como información de cada gerencia. Este proyecto está siendo llevado a cabo por el departamento de Informática bajo la Gerencia General con apoyo del departamento de Asuntos Públicos. El frontend del mismo fue realizado en NodeJS sin librerías, es decir, únicamente HTML, JS y CSS como tecnologías base. También se utilizó Bootstrap. En cuanto al backend se utilizó únicamente para el envío de correos del formulario con validaciones de Captcha, los cuales serán recibidos en el correo de servicios externos.

## :zap: Utilización
Este proyecto es de código cerrado y puede ser editado y utilizado únicamente por el personal autorizado de Indesca para este fin. Debido a esto, su única finalidad es servir de apoyo informativo en la web en el dominio registrado para este propósito.

###  :electric_plug: Instalación
- Por llenar.

```
$ add installations steps if you have to.
```

###  :package: Comandos
Para ejecutar en ambiente de desarrollo:

```
$ npm install
$ npm run dev
```

##  :wrench: Desarrollo

### :notebook: Pre-Requisitos
Se debe tener acceso a desarrollar con las siguientes tecnologías:
- [Vite](https://vitejs.dev/): Versión 4.4.3
- [Bootstrap](https://vuejs.org/): Versión 5.3.0
- [SASS](https://sass-lang.com/): Versión 1.63.6
- [AOS](https://michalsnik.github.io/aos/): Versión 3.0.0-beta.6

###  :nut_and_bolt: Ambiente de Desarrollo
El ambiente de desarrollo puede ser montado con lo mostrado en la sección de comandos. Sin embargo, adicionalmente, se recomienda montar un servidor PHP en la misma carpeta donde se encuentre el proyecto para poder ejecutar el backend de envío de correo del formulario de contacto.

###  :file_folder: Estructura de Archivos
Aquí se encuentran los detalles de la estructura de archivos del proyecto.

| No | Carpeta / Archivo | Detalles 
|----|------------|-------|
| 1  | images/ | Imágenes utilizadas en las distintas páginas estáticas por gerencia
| 2  | pages/ | Aquí se encuentras las páginas estáticas mostradas por gerencia
| 3  | scss/ | Estilos utilizados en formato .scss; se encuentran los archivos necesarios para el funcionamiento de scss.
| 4  | email.php | Backend de la página utilizado para el envío de correos desde el formulario de contactos.
| 5  | main.js | Importación de librerías de JS utilizadas y determinación de los parámetros de AOS.

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
