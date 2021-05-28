import requests
from bs4 import BeautifulSoup
import pandas as pd

matriculas = ['PS-AEH', 'PR-PJN', 'XE', 'PR-TOL']
arquivo_saida = 'lista_avioes.csv'

df = []

for m in matriculas:
    
    print(f"Processando a matrícula: {m}")
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
      df.append(dados)    

df = pd.DataFrame(df, columns=dados.keys())    

pd.DataFrame.to_csv(df, arquivo_saida, columns=df.columns, index=False)
