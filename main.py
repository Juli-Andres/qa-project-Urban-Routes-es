import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Keys



# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
# Localizadores Punto 1 Configurar la dirección
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

# Localizadores Punto 2 Seleccionar la tarifa Comfort.
    boton_pedir_taxi = (By.CSS_SELECTOR, ".button.round")
    boton_tarifa_confort = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")

# Localizadores Punto 3 Rellenar el número de teléfono.
    boton_numero_telefono = (By.CLASS_NAME, 'np-text')
    campo_numero_telefono = (By.ID, 'phone')
    boton_siguiente = (By.CSS_SELECTOR, ".button.full")
    boton_campo_codigo = (By.ID, 'code')
    boton_confirmar = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')

# Localizadores Punto 4 Agregar una tarjeta de crédito
    boton_metodo_pago = (By.CLASS_NAME, 'pp-text')
    boton_agregar_tarjeta = (By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")
    campo_numero_tarjeta = (By.XPATH, '//*[@id="number"]')
    campo_codigo_tarjeta = (By.CSS_SELECTOR, "input[placeholder='12']")
    boton_agregar = (By.XPATH, "//button[@type='submit' and text()='Agregar']")
    boton_cerrar_metodo_pago = (By.XPATH, '//div[@class="payment-picker open"]//button[@class="close-button section-close"]')

# Localizadores Punto 5 Escribir un mensaje para el controlador.
    campo_mensaje = (By.ID, "comment")

#Localizadores Punto 6 Pedir una manta y pañuelos.
    boton_manta = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')
    confirmacion_manta = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/input')
    option_switches_inputs = (By.CLASS_NAME, 'switch-input')
    option_switches = (By.CLASS_NAME, 'switch')

#Localizadores Punto 7 Pedir 2 helados.
    boton_adicionar_helados = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
    cantidad_helados = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]')

#Localizadores Punto 8 Aparece el modal para buscar un taxi.
    boton_reservar_taxi = (By.XPATH, "//span[@class='smart-button-main' and text()='Pedir un taxi']")
    order_wait_screen_title = (By.XPATH, "//div[@class='order shown']//div[@class='order-body']//div[@class='order-header']//div[@class='order-header-title']")



    def __init__(self, driver):
        self.driver = driver


    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def set_from(self, from_address):
        WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located(self.from_field)
        ).send_keys(from_address)

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_to(self, to_address):
        WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located(self.to_field)
        ).send_keys(to_address)

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

#  localizar boton pedir taxi y dar clic en el
    def get_boton_pedir_taxi(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.boton_pedir_taxi)
        )

    def click_boton_pedir_taxi(self):
        self.get_boton_pedir_taxi().click()

#   localizar boton Comfort y dar clic en el
    def get_boton_tarifa_confort(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.boton_tarifa_confort)
        )

    def click_boton_tarifa_confort(self):
        self.get_boton_tarifa_confort().click()

#   localizar boton numero de telefono y dar clic en el
    def get_boton_numero_telefono(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.boton_numero_telefono)
        )

    def click_boton_numero_telefono(self):
        self.get_boton_numero_telefono().click()

#   localizar campo numero de telefono e ingresar Numero valido +13168919047
    def get_campo_numero_telefono(self):
        return self.driver.find_element(*self.campo_numero_telefono).get_property('value')

    def set_campo_numero_telefono(self, phone_number):
        WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located(self.campo_numero_telefono)
        ).send_keys(phone_number)

#   localizar boton siguiente y dar clic en el
    def get_boton_siguiente(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.boton_siguiente)
        )

    def click_boton_siguiente(self):
        self.get_boton_siguiente().click()

#   localizar campo codigo y pasar el codigo generado
    def get_campo_codigo(self):
        return self.driver.find_element(*self.boton_campo_codigo).get_property('value')

    def set_campo_codigo(self, code):
        #self.driver.find_element(*self.from_field).send_keys(from_address)
        WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located(self.boton_campo_codigo)
        ).send_keys(code)

#   localizar boton confirmar y dar clic en el
    def get_boton_confirmar(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.boton_confirmar)
        )

    def click_boton_confirmar(self):
        self.get_boton_confirmar().click()

#   localizar el boton Metodo de pago y dar clic en el
    def get_boton_metodo_pago(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.boton_metodo_pago)
        )

    def click_boton_metodo_pago(self):
        self.get_boton_metodo_pago().click()

#   localizar el boton agregar tarjeta y dar clic en el
    def get_boton_agregar_tarjeta(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.boton_agregar_tarjeta)
        )

    def click_boton_agregar_tarjeta(self):
        self.get_boton_agregar_tarjeta().click()

#   localizar el campo numero de tarjeta y registrar el numero
    def get_tarjeta(self):
        return self.driver.find_element(*self.campo_numero_tarjeta).get_property('value')

    def set_tarjeta(self, numero):
        WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located(self.campo_numero_tarjeta)
        ).send_keys(numero)

#   localizar el campo codigo de tarjeta (cvv) y registrar el numero
    def get_cvv(self):
        return self.driver.find_element(*self.campo_codigo_tarjeta).get_property('value')

    def set_cvv(self, cvv):
        WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located(self.campo_codigo_tarjeta)
        ).send_keys(cvv)
        cvv_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='12']")
        cvv_field.send_keys(Keys.TAB)

#   localizar el boton adicionar tarjeta y dar clic en el
    def get_boton_adicionar_tarjeta(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.boton_agregar)
        )

    def click_boton_adicionar_tarjeta(self):
        self.get_boton_adicionar_tarjeta().click()

#   localizar el boton cerrar metodo de pago y dar clic en el
    def get_boton_cerrar_metodo_pago(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.boton_cerrar_metodo_pago)
        )

    def click_boton_cerrar_metodo_pago(self):
        self.get_boton_cerrar_metodo_pago().click()

#   localizar el campo mensaje y registrar texto
    def get_campo_mensaje_conductor(self):
        return self.driver.find_element(*self.campo_mensaje).get_property('value')

    def set_campo_mensaje_conductor(self, mensaje):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.campo_mensaje)
        ).send_keys(mensaje)

#   localizar y activar los botones para adicionar extras
    def get_adicionar_mantas(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.option_switches)
        )

    def click_adicionar_mantas(self):
        self.get_adicionar_mantas().click()

    def get_manta_checked(self):
        switches = self.driver.find_elements(*self.option_switches_inputs)
        return switches[0].get_property('checked')


#   localizar el campo helados y adicionar 2
    def get_boton_adicionar_helados(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.boton_adicionar_helados)
        )

    def click_boton_adicionar_helados(self):
        self.get_boton_adicionar_helados().click()

    def get_cant_helados(self):
        return self.driver.find_element(*self.cantidad_helados).get_attribute('innerHTML')

#   localizar el boton reservar taxi
    def get_boton_reservar_taxi(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.boton_reservar_taxi)
        )

    def click_boton_reservar_taxi(self):
        self.get_boton_reservar_taxi().click()

#  Validar que aparezca la pantalla buscar un taxi
    def timer_descendente(self):
        for contador in range(50, -1, -1):
            print(f'Buscando conductor: {contador}')
#        print(self.get_order_screen_title())


    def get_order_screen_title(self):
        return self.driver.find_element(*self.order_wait_screen_title).get_attribute('innerText')




class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(service=Service(), options=options)

# 1. Configurar la dirección
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

# 2. Seleccionar la tarifa Comfort.
    def test_seleccionar_tarifa_confort(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_boton_pedir_taxi()
        routes_page.click_boton_tarifa_confort()
        assert routes_page.get_boton_tarifa_confort().text in "Comfort"

#3. Rellenar el número de teléfono.
    def test_ingresar_numero_telefono(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_boton_numero_telefono()
        phone_number = data.phone_number
        routes_page.set_campo_numero_telefono(phone_number)
        routes_page.click_boton_siguiente()
        codigo = retrieve_phone_code(self.driver)
        routes_page.set_campo_codigo(codigo)
        routes_page.click_boton_confirmar()
        assert routes_page.get_campo_numero_telefono() == phone_number
        assert routes_page.get_campo_codigo() == codigo

# 4. Agregar una tarjeta de crédito.
    def test_ingresar_metodo_de_pago(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_boton_metodo_pago()
        routes_page.click_boton_agregar_tarjeta()
        numero_tarjeta = data.card_number
        routes_page.set_tarjeta(numero_tarjeta)
        cvv = data.card_code
        routes_page.set_cvv(cvv)
        routes_page.click_boton_adicionar_tarjeta()
        routes_page.click_boton_cerrar_metodo_pago()
        assert routes_page.get_tarjeta() == numero_tarjeta
        assert routes_page.get_cvv() == cvv

# 5. Escribir un mensaje para el controlador.
    def test_mensaje_conductor(self):
        routes_page = UrbanRoutesPage(self.driver)
        mensaje = data.message_for_driver
        routes_page.set_campo_mensaje_conductor(mensaje)
        assert routes_page.get_campo_mensaje_conductor() == mensaje

# 6. Pedir una manta y pañuelos.
    def test_adicionar_mantas_y_panuelos(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_adicionar_mantas()
        assert routes_page.get_manta_checked()

# 7. Pedir 2 helados.
    def test_pedir_helados(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_boton_adicionar_helados()
        routes_page.click_boton_adicionar_helados()
        assert routes_page.get_cant_helados() == "2"
        
# 8. Aparece el modal para buscar un taxi.
    def test_reservar_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.get_boton_reservar_taxi()
        routes_page.click_boton_reservar_taxi()
        routes_page.timer_descendente()
        assert "Buscar automóvil" in routes_page.get_order_screen_title()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()



