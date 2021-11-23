from selenium import webdriver

class ExtratorUnifesp:
    def __init__(self, driver=None):
        print('iniciando')
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=options) if not driver else driver
        self.url = "https://ingresso.unifesp.br/informacoes-fixas/informacoes-fixas-misto/cronograma-sistema-misto"
        print('Carregando conteúdo da página...')
        self.driver.get(self.url)
        self.inscricao = []

    def extrair_info_páginas(self):
        dados_lst = []
        for k in range(1, 12):
            data = self.driver.find_element_by_xpath(f"""//*[@id='g-main']/div/div/div/div/div/div/div/div[2]/table/tbody/tr[{k}]/td[1]""")
            data = data.text
            try:
                conteudo = self.driver.find_element_by_xpath(f"""//*[@id='g-main']/div/div/div/div/div/div/div/div[2]/table/tbody/tr[{k}]/td[2]""")
                conteudo = conteudo.text
            except:
                conteudo = ''
            dados = {
                'Data':data,
                'Conteudo':conteudo
                }
            dados_lst.append(dados)
        self.inscricao = dados_lst

    def formatar_dados(self):
        for linha in self.inscricao:
            if  'Período para pedido de isenção de taxa de inscrição do vestibular' in str(linha['Conteudo']):
                data = str( linha['Data']).split('às')
                self.inicio_isencao = data[0]
                self.termino_isencao = data[1]
            elif 'Período de inscrição para as provas complementares' in str(linha['Conteudo']):
                data = str( linha['Data']).split('às')
                self.inicio_das_insc = data[0]
                self.termino_das_insc = data[1]
            elif 'Provas Complementares:\n' in str(linha['Conteudo']):
                data = str(linha['Data']).split('\n')
                self.primeira_fase = data[0]
                self.primeira_fase_dia2 = data[1]
    
    def extrair_informacoes(self):
        print('Extraindo info')
        self.extrair_info_páginas()
        print('formatando dados')
        self.formatar_dados()
            