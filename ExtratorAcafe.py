from selenium import webdriver
from selenium.webdriver import Chrome
from time import sleep

class ExtratorUniv:

    def __init__(self, periodo, driver = None):
        #Inicia nossa classe definindo o drive a abrindo a página
        '''
        Período = Qual edição da prova queremos (ex:'Verão 2022', 'Inverno 2022', ...)
        '''
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=options) if not driver else driver
        self.periodo =  periodo
        self.url = 'https://acafe.org.br/site/'
        self.driver.get(self.url)


    def abrir_calendario(self):
        #fechar banner
        try:
            sleep(15)
            banner = self.driver.find_element_by_xpath(f'''/html/body/div[3]/div/div/div[3]/button''')
            banner.click()
            print('banner fechado.')
        except:
            pass
        #Aceita os cookies e abre o calendário 
        aceitar_cookies = self.driver.find_element_by_class_name(f'''btn-cookies''')
        print('cookies aceitos.')
        abrir_calendario = self.driver.find_element_by_xpath(f'''/html/body/div[5]/div/div[2]''')
        print('Calendário aberto.')
        sleep(5)
        aceitar_cookies.click()
        sleep(3)
        abrir_calendario.click()    

    def extrair_conteudo(self):
        #extrai o conteúdo do calendário (os acontecimentos que queremos para o nosso banco de dados e suas respectivas datas)
        self.abrir_calendario()
        self.titulos_element = self.driver.find_elements_by_tag_name(f'''th''')
        self.linhas_element = self.driver.find_elements_by_tag_name(f'''td''')

        #organizando conteúdo em listas
        linhas = []
        for linha in self.linhas_element:
            linhas.append(linha.text)
        self.linhas = linhas
        titulos = []
        for titulo in self.titulos_element:
            if titulo.text != '':
                titulos.append(titulo.text)
        self.titulos = titulos

    def atribuir_datas(self):
        #correlacionando e formatando a lista de datas e de títulos(acontecimento)
        self.indice_do_perido = int(self.titulos.index(self.periodo))
        for i in range(0,len(self.linhas), len(self.titulos)):
            if self.linhas[i] == 'Aplicação da prova':
                self.primeira_fase = self.linhas[(i+self.indice_do_perido)]
            elif self.linhas[i] == 'Inscrição':
                datas = (self.linhas[(i+self.indice_do_perido)]).split('a')
                self.inicio_das_insc = datas[0]
                self.termino_das_insc = datas[1]  
            elif self.linhas[i]   == 'Pagamento':
                datas = (self.linhas[(i+self.indice_do_perido)]).split('Até')
                self.inicio_pagamento = datas[0]
                self.termino_pagamento = datas[1]

    def extrair_informacoes(self):
        #função que ao ser chamada, executa todas as anteriores (exceto init)
        self.extrair_conteudo()
        self.atribuir_datas()
