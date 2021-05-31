import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from .invalidfileerror import InvalidFileError


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

	def __init__(self, matriculas, verbose=False):

		if not isinstance(matriculas, list) and not isinstance(matriculas, tuple):
			raise TypeError(f"O parâmetro matrícula deve ser uma lista")

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
				dados['Peso Máximo de Decolagem'] = dados['Peso Máximo de Decolagem'].split("-")[0]
				self.__lista_dados.append(dados) 
			else:
				if verbose:     
					print(f"---- Matrícula {m} não encontrada ----")

			if verbose:
				print(f"Processando a matrícula: {m} | fim")

		self.__df = pd.DataFrame(self.__lista_dados, columns=dados.keys())    
		self.__df.sort_values(by=['Matricula'], inplace=True)
		self.__df = self.__trata_dados(self.__df)

	def obter_dados(self):
	
		return self.__df

	def __trata_dados(self, df):

		aux_df = df
		aux_df['Ano de Fabricação'] = aux_df['Ano de Fabricação'].astype('int32')
		aux_df['Número da Matrícula'] = aux_df['Número da Matrícula'].astype('int32')
		aux_df['Número Máximo de Passageiros'] = aux_df['Número Máximo de Passageiros'].astype('int32')
		aux_df['Peso Máximo de Decolagem'] = aux_df['Peso Máximo de Decolagem'].astype('int32')

		return aux_df

	def salvar_arquivo(self, saida="lista_aeronaves.csv", dados = pd.DataFrame()):

		if dados.empty:
			dados = self.__df

		try:
			tipo_arquivo = saida.split('.')[-1]
		except IndexError as ie:
			raise TypeError(f"O parâmetro saída deve conter o nome do arquivo e a extenção")

		if tipo_arquivo == 'csv':
			pd.DataFrame.to_csv(dados, saida, columns=dados.columns, index=False, encoding="utf-8")
		elif tipo_arquivo == 'xlsx':
			pd.DataFrame.to_excel(dados, saida, columns=dados.columns, index=False, encoding="utf-8")
		else:
			raise InvalidFileError(tipo_arquivo)
	
	def combinar_arquivos(self, arquivo1, arquivo2):
		df1 = pd.read_csv(arquivo1)
		df2 = pd.read_csv(arquivo2)

		if not (list(df1.columns) == list(df1.columns)):
			raise TypeError(f"Os arquivos passados não possuem as mesmas colunas")
		
		result = pd.concat([df1, df2]).drop_duplicates()
		result.reset_index(drop=True, inplace=True)
		
		return result