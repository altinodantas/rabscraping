# rabscraping

Código pyhon que realiza um scraping no site do Registro Aeronáutico Brasileiro (RAB) através da busca por matrícula. 
A classe RABScraping, a partir de uma lista de matrículas brasileiras, realiza o scraping e fornece um Pandas DataFrame e/ou salva um arquivo com as informações encontradas.

## Arquivos suportados
- csv
- Excel (.xlsx)

## Exemplos de uso

O construtor `RABScraping(matriculas, verbose=False)` possui dois parâmetros: 
- **matriculas**: a lista de matrículas (obrigatório); 
- **verbose**: booleano que define impressão do progresso (Opcional). 

### Salvar dados da consulta em arquivo

``` py
from lib.rabscraping import RABScraping

lista_matriculas = ['PR-GUM','PS-AEH', 'PR-PJN', 'XE', 'PR-TOL']
lista = RABScraping(matriculas=lista_matriculas, verbose=True)
lista.salvar_arquivo()
```
O método `RABScraping.salvar_arquivo()` salva um arquivo **lista_aeronaves.csv** contendo os dados consultados. 
Caso deseje informar o nome e o formato do arquivo, basta definir o parâmetro `saida`. 
No exemplo acima, uma das matrículas é **XE**, que obvimanente não existe na base do RAB, logo, não constará nos resultados da consulta. 
Caso `verbose=True`, então haverá a impressão no console do andamento da consulta. Esta opção é `False` por padrão.

```
Processando a matrícula: PR-GUM | início
Processando a matrícula: PR-GUM | fim
Processando a matrícula: PS-AEH | início
Processando a matrícula: PS-AEH | fim
Processando a matrícula: PR-PJN | início
Processando a matrícula: PR-PJN | fim
Processando a matrícula: XE | início
--- Matrícula XE não encontrada ---
Processando a matrícula: XE | fim
Processando a matrícula: PR-TOL | início
Processando a matrícula: PR-TOL | fim
```

### Obter DataFrame com os dados da consulta

O método `RABScraping.obter_dados()` tem como retorno um DataFrame do Pandas e pode, portanto, ser utilizado para manipulação dos dados obtidos. 
O método RABScraping.salvar_arquivo() pode ser usado para salvar qualquer DataFrame como arquivo, através do parâmetro dados.

``` py
from lib.rabscraping import RABScraping

lista = RABScraping(['PR-GUM','PS-AEH', 'PR-PJN', 'XE', 'PR-TOL'], verbose=True)
df = lista.obter_dados()
df = df[df['Ano de Fabricação'] > 2019]

lista.salvar_arquivo(saida='aeronaves_novas.xlsx', dados=df)

```

### Combinar dois arquivos
O método `RABScraping.combinar_arquivos()` combina os dados de dois arquivos e salva o resultado em um terceiro arquivo. Os dois arquivos a serem combinados devem possir o mesmo cabeçalhos. Caso `duplicados=False`, a combinação removerá registros repetidos, considerando a matrícula como chave, caso contrário funcionará como _append_. Essa funcionalidade pode ser útil para lidar com situações de permanente atualização em registros de log (ideal para *plane sportters*). 

``` py
from lib.rabscraping import RABScraping

lista_matriculas = ('PR-GUM','PS-AEH', 'PR-PJN', 'XE', 'PR-TOL')
lista = RABScraping(matriculas=lista_matriculas, verbose=True)
lista.salvar_arquivo("arquivo_a.xlsx")

lista_matriculas = ['PR-PJN']
lista = RABScraping(matriculas=lista_matriculas, verbose=True)
lista.salvar_arquivo("arquivo_b.csv")

RABScraping.combinar_arquivos('arquivo_a.xlsx','arquivo_b.csv','saida.xlsx', duplicados=True)

```

-----------------------------------------------------------------------------------------------------------------------
### Métodos disponíveis

| Método         | Parâmetros                    | Retorno   | Funcionalidade                                         |
|----------------|-------------------------------|-----------|--------------------------------------------------------|
| RABScraping    | <ul><li>**matriculas**: list (Obrigatório)</li><li>**verbose**: Booleano (Opcional)</li>Valor padrão: False</ul>                             | Objeto da classe RABScraping | Construtor da classe.                  |
| obter_dados    | Nenhum                        | DataFrame | Fornece os dados obtidos na consulta.                  |
| salvar_arquivo | <ul><li>**dados**: DataFrame (opcional)</li> Valor padrão: vazio. <li>**saida**: str (opcional)</li> Valor padrão: 'lista_aeronaves.csv' | Nenhum        | Salva os dados da consulta em um arquivo csv ou xlsx. Se o parâmetro dados for informado, salva esse DataFrame em arquivo. |
|combinar_arquivos | <ul><li>**arquivo1**: str (Obrigatório)</li> <li>**arquivo2**: str (Obrigatório)</li> <li>**saida**: str (Opcional) </li>Valor padão: lista_combinada_aeronaves.csv <li>**duplicados**: booleano (Opcional)</li> Valor padrão: False</ul> | Nenhum  | Combina os arquivos __arquivo1__ e __arquivo2__ e salva no caminho informado no parâmetro **saida**. 
  
## Requisitos
  - Python 3.7 ou superior
  - pacotes no requirements.txt
  
  **OBS**.:  Até a última revisão deste (01/05/2021), a página de consulta por matrícula do RAB renderiza a tabela principal com uma das linhas contendo apenas uma célula `(<td>)`, enquanto as demais têm duas. Nesse caso, algumas versões do BeautifulSoup4 não conseguem capturar todas as linhas da tabela através do _find_all_. Caso o código seja executado no *colab*, é possível que não esteja disponível a versão mais atualizada do BS4, sendo assim, a consulta não retornará os últimos campos.   
