from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

path = 'chromedriver.exe'
# chrome_options = Options()
# chrome_options.add_argument("--kiosk")

email = "automacaotiktok@gmail.com"
senhaTiktok = "automacao10!"

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(path, options=options)
driver.get("https://www.tiktok.com/pt-BR/")

# Clica no botão "Entrar"
driver.find_element_by_xpath(
    "/html/body/div[2]/div[1]/div/div[2]/button").click()
time.sleep(1)
# Clica no botão "Usar telefone/e-mail/nome de usuário"
driver.find_element_by_xpath(
    "/html/body/div[6]/div[2]/div[1]/div[1]/div/div/a[2]").click()
time.sleep(1)
# Clica no botão "Entrar com nome de usuário ou e-mail"
driver.find_element_by_xpath(
    "/html/body/div[6]/div[2]/div[2]/div[1]/div/form/div[2]/a").click()
time.sleep(1)
# Inserindo email do formulário
driver.find_element_by_xpath(
    "/html/body/div[6]/div[2]/div[2]/div[1]/div/form/div[1]/input").send_keys(email)
time.sleep(1)
# Inserindo senha do formulário
driver.find_element_by_xpath(
    "/html/body/div[6]/div[2]/div[2]/div[1]/div/form/div[2]/div/input").send_keys(senhaTiktok)
time.sleep(1)
# Clica no botão "Entrar" do formulário
driver.find_element_by_xpath(
    "/html/body/div[6]/div[2]/div[2]/div[1]/div/form/button").click()
time.sleep(1)