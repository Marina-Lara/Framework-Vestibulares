from selenium import webdriver
from time import sleep 
import pandas as pd



## Modelagem OO 
class ExtratorUEPGVest:
    """
    O ExtratorUEPGVest é uma classe utilitária que facilita a extração das informações sobre o vestibular atual da Univesidade Estadual de Ponta Grossa (UEPG)   
    """
    def __init__(self, driver=None):
        """
        Construtor
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=options) if not driver else driver
        self.url = "https://cps.uepg.br/inicio/"
        self.driver.get(self.url)
        self.lst_informações = []
        self.qntd_linhas = 9
        
    def pagina_vestibular(self):
        """
        Seleciona o último vestibular para visualizar mais detalhes sobre
        """
        # Clica no ùltimo vestibular postado
        vestibular = self.driver.find_element_by_xpath("""//*[@id="content-1column"]/section/div/article/table/tbody/tr[3]/td[1]/a[1]""")
        vestibular.click()

    def informações_vestibular(self):
        """
        Extrai as informações do vestibular
        """
        # Grava o nome do vestibular
        vestibular_atual = self.driver.find_element_by_xpath("""//*[@id="content-1column"]/article/table/tbody/tr[2]/td/p[1]/span""")
        self.lst_informações.append(vestibular_atual.text)
        
        # Extrai as informações como data de abertura e encerramento de inscrições, data de liberação dos resultados, taxa de inscrição etc.
        for i in range (1, self.qntd_linhas):
            xpath_linhas = f'//*[@id="content-1column"]/article/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[{i}]'
            informações = self.driver.find_element_by_xpath(xpath_linhas)
            self.lst_informações.append(informações.text)

    def atribuir_datas(self):
        #correlacionando e formatando a lista de datas e de títulos(acontecimento)
        for linha in self.lst_informações:
            if 'Período de inscrição' in linha:
                texto = linha.split(':')
                texto = str(texto[1])
                data = texto.split('a')
                self.inicio_das_insc = data[0]
                self.termino_das_insc = data[1]
            elif 'Aplicação das provas' in linha:
                texto = linha.split(':')
                texto = str(texto[1])
                self.primeira_fase = texto
    def extrair_informações(self):
            self.pagina_vestibular()
            self.informações_vestibular()
            self.atribuir_datas()

