# Canva a PDF

Aplicación de escritorio para convertir presentaciones de **Canva** en un único archivo PDF, permitiendo seleccionar un rango específico de diapositivas y personalizar el tiempo de espera para la carga de cada página.

<img width="591" height="426" alt="image" src="https://github.com/user-attachments/assets/f49a5b99-6899-48ae-82c8-f7220496c9f3" />

---
## Descarga

[![GitHub All Releases](https://img.shields.io/github/v/release/doedecom/Canva-a-PDF?style=for-the-badge)](https://github.com/doedecom/Canva-a-PDF/releases/latest)

---

## Características

* Conversión automática de presentaciones de Canva a PDF.
* Selección de carpeta de destino.
* Definición del nombre del archivo PDF final.
* Exportación de un rango específico de diapositivas.
* Configuración del tiempo de espera para la carga de Canva.
* Generación de un único PDF con todas las páginas seleccionadas.

---

## Requisitos

Antes de usar la aplicación asegúrate de:

* Tener acceso a una presentación pública o compartida de Canva.
* Contar con conexión a Internet.
* Disponer de espacio suficiente en disco para guardar el PDF generado.

---

## Cómo obtener el enlace de Canva

1. Abre la presentación en Canva.
2. Haz clic en **Compartir**.
3. Copia el enlace de visualización de la presentación.
4. Pega el enlace en el campo **Enlace Canva** de la aplicación.

Ejemplo:

```text
https://www.canva.com/design/XXXXXXXXXXX/view
```

---

## Uso de la aplicación

### 1. Ingresar el enlace de Canva

En el campo **Enlace Canva**, pega la URL de la presentación.

---

### 2. Seleccionar la carpeta de destino

1. Haz clic en **Examinar**.
2. Selecciona la carpeta donde deseas guardar el PDF final.

---

### 3. Definir el nombre del PDF

En **Nombre PDF final**, escribe el nombre que tendrá el archivo generado.

Ejemplo:

```text
presentacion_final
```

No es necesario escribir la extensión `.pdf`.

---

### 4. Seleccionar el rango de diapositivas

Configura las diapositivas que deseas exportar:

* **Desde:** primera diapositiva.
* **Hasta:** última diapositiva.

Ejemplo:

```text
Desde: 5
Hasta: 20
```

La aplicación exportará únicamente las diapositivas comprendidas entre esos valores.

---

### 5. Configurar el tiempo de espera

El campo **Tiempo espera Canva (ms)** define cuánto tiempo esperará la aplicación para que cada diapositiva cargue completamente antes de capturarla.

Valor recomendado:

```text
3000 ms
```

Si la presentación contiene:

* Videos
* Animaciones complejas
* Muchas imágenes

puede ser necesario aumentar el valor a:

```text
5000 - 8000 ms
```

---

### 6. Generar el PDF

Haz clic en **Generar PDF**.

La aplicación:

1. Abre la presentación.
2. Recorre las diapositivas seleccionadas.
3. Genera un PDF individual de cada página.
4. Une todas las páginas en un único archivo PDF.
5. Guarda el resultado en la carpeta seleccionada.

Al finalizar aparecerá un mensaje indicando que el proceso fue completado correctamente.

---

## Recomendaciones

* Mantén una conexión estable a Internet durante el proceso.
* No cierres la aplicación mientras se está generando el PDF.
* Si alguna página aparece incompleta, aumenta el tiempo de espera.
* Verifica que el enlace de Canva sea accesible desde un navegador.

---

## Solución de problemas

### No se genera el PDF

Verifica que:

* El enlace de Canva sea válido.
* La presentación sea accesible.
* Exista permiso de escritura en la carpeta de destino.

---

### Algunas diapositivas aparecen en blanco

Incrementa el valor de:

```text
Tiempo espera Canva (ms)
```

para permitir que Canva cargue completamente el contenido.

---

### El proceso es muy lento

Reduce el tiempo de espera o exporta menos diapositivas por ejecución.

---

## Tecnologías utilizadas

* Python
* PyQt5
* Playwright
* PyPDF
* Chromium

---

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Puedes modificarlo y utilizarlo libremente respetando los términos de la licencia.
