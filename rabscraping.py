import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from invalidfileerror import InvalidFileError


class RABScraping:
	"""
    Class usada para realizar scraping na página do RAB a partir de uma lista de matrículas e salvar em arquivo csv ou excel

    ...

    Atributos
    ----------
    __lista_dados : list
        Uma lista com dicionários no formato {'matricula':'XX-UUU', 'Proprietário': 'Altino Dantas'}
	__df : DataFrame
		DataFrame contendo a consolidação do dados de __lista_dados

    Métodos
    -------
    obter_dados()
        Retorna um DataFrame pandas com a lista de aeronaves encontradas
	salvar_arquivo(saida="lista_aeronaves.csv")
        Salva um arquivo com a lista das aeronaves encontradas. O arquivo pode ser .xlsx ou .csv
	
    """

	def __init__(self, matriculas=[], verbose=False):

		self.__lista_dados = []
        
		for m in matriculas:
			m = m.strip()

			if verbose:
				print(f"Processando a matrícula: {m} | início")

			html = requests.get(f"https://sistemas.anac.gov.br/aeronaves/cons_rab_resposta.asp?textMarca={m}").content
			soup = BeautifulSoup(html, 'html.parser')

			tabela = soup.find("table", class_="table table-hover")
			linhas = tabela.find_all('tr')
			dados = {'Matricula' : m}

			for ln in linhas:
				texto = ln.text.strip()
				texto = texto.split('\n')
				campo = texto[0].split(":")
				valor = texto[-1].replace("\t","")     
				dados[campo[0]] = valor

			if(dados['Modelo'] != 'Modelo:'):   
				self.__lista_dados.append(dados) 
			else:
				if verbose:     
					print(f"--- Matrícula {m} não encontrada ---")

			if verbose:
				print(f"Processando a matrícula: {m} | fim")

		self.__df = pd.DataFrame(self.__lista_dados, columns=dados.keys())    
		self.__df.sort_values(by=['Matricula'], inplace=True)

	def obter_dados(self):
		return self.__df

	def salvar_arquivo(self, saida="lista_aeronaves.csv"):
		tipo_arquivo = saida.split('.')[1]
		if tipo_arquivo == 'csv':
			pd.DataFrame.to_csv(self.__df, saida, columns=self.__df.columns, index=False, encoding="utf-8")
		elif tipo_arquivo == 'xlsx':
			pd.DataFrame.to_excel(self.__df, saida, columns=self.__df.columns, index=False, encoding="utf-8")
		else:
			raise InvalidFileError(tipo_arquivo)
			#raise NotImplementedError(f"Impossível salva o arquivo. {tipo_arquivo} é um tipo de arquivo não suportado. Informe xlsx ou csv.")
