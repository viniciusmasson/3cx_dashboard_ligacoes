from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time
import os
import logging

load_dotenv()

CX_USUARIO = os.getenv("CX_USUARIO")
CX_SENHA = os.getenv("CX_SENHA")
CX_URL = os.getenv("CX_URL")
CX_LOG_PATH = os.getenv("CX_LOG_PATH")
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(CX_LOG_PATH, "3cx_tempo_real.log"), encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def automatizar_relatorio():
    logging.info("========== INÍCIO DA EXECUÇÃO ==========")
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option("prefs", {
            "download.default_directory": DOWNLOAD_PATH,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        os.makedirs(DOWNLOAD_PATH, exist_ok=True)
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(15)

        driver.get(f"{CX_URL}/#/login")
        time.sleep(3)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/app/div/div/div/wclogin/standalone-view/div/div/form/div/div[1]/input"))
        ).send_keys(CX_USUARIO)

        driver.find_element(By.XPATH, "/html/body/app/div/div/div/wclogin/standalone-view/div/div/form/div/div[2]/input").send_keys(CX_SENHA)
        driver.find_element(By.XPATH, "/html/body/app/div/div/div/wclogin/standalone-view/div/div/form/button").click()
        time.sleep(5)

        if "login" in driver.current_url.lower():
            logging.error("Falha no login.")
            return False

        logging.info("Login realizado com sucesso.")

        driver.get(f"{CX_URL}/#/office/reports/call-reports")
        time.sleep(10)

        botao = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Exportar') or contains(., 'Export')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", botao)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", botao)
        logging.info("Botão Exportar clicado.")
        time.sleep(3)

        opcao_csv = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'CSV') or contains(text(), 'Excel') or contains(@class, 'csv')]"))
        )
        driver.execute_script("arguments[0].click();", opcao_csv)
        logging.info("Opção CSV selecionada.")
        time.sleep(15)

        arquivos = [f for f in os.listdir(DOWNLOAD_PATH) if f.endswith(".csv")]
        if not arquivos:
            logging.error("Nenhum arquivo CSV encontrado.")
            return False

        mais_recente = max([os.path.join(DOWNLOAD_PATH, f) for f in arquivos], key=os.path.getctime)
        novo_nome = os.path.join(DOWNLOAD_PATH, "relatorio_chamadas.csv")
        if os.path.exists(novo_nome):
            os.remove(novo_nome)
        os.rename(mais_recente, novo_nome)

        logging.info("Arquivo salvo como: relatorio_chamadas.csv")
        return True

    except Exception as e:
        logging.error(f"Erro: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return False

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    automatizar_relatorio()