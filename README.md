# Automatización de pruebas - Urban Routes

## *Julián Andrés Córdoba Peña  Cohorte 25*

Este proyecto automatiza el flujo de reservas de taxi en la aplicación **Urban Routes** usando **Python** y **Selenium**. Muestra los diferentes localizadores metodos y funciones empleados en el paso a paso del proceso de automatizacion.

---

## 🧰 Herramientas utilizadas

- **Python 3**
- **Selenium WebDriver**
- **Google Chrome**
- **Pytest (opcional para ejecutar pruebas)**

---

## 🗂️ Estructura general

El proyecto contiene dos clases principales:

- `UrbanRoutesPage`: contiene todos los elementos de la página y las acciones.
- `TestUrbanRoutes`: contiene los pasos de prueba automatizados.

Además, se incluye una función especial:

- `retrieve_phone_code(driver)`: obtiene el código de confirmación del teléfono desde los logs del navegador.

---

## 🔧 Preparación del entorno

1. Abrir Python.
2. Instalar selenium y pytest
   ```
   pip install selenium
   pip install pytest

## 🧪 Flujo de pruebas automatizado
1. Configurar dirección (origen y destino).
2. Seleccionar tarifa Comfort.
3. Ingresar número de teléfono y confirmar con código.
4. Agregar método de pago (tarjeta).
5. Escribir un mensaje para el conductor.
6. Adicionar una manta y pañuelos.
7. Pedir 2 helados.
8. Reservar el taxi.


## 📚 Aprendizaje
Este proyecto sirvió para ayudar a practicar:

- Automatización de pruebas funcionales.
- Uso del patrón Page Object Model.
- Manejo de Selenium WebDriver.
- Lectura de logs del navegador para obtener datos dinámicos.