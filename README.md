# rabscraping

Código pyhon que realiza um scraping no site do Registro Aeronáutico Brasileiro (RAB) através da busca por matrícula. 
A classe RABScraping, a partir de uma lista de matrículas brasileiras, realiza o scraping e fornece um Pandas DataFrame e/ou salva um arquivo com as informações encontradas.

## Arquivos suportados para salvamento
- csv
- Excel (.xlsx)

## Exemplos de uso

O construtor `RABScraping(matriculas, verbose=False)` espera **matriculas** como lista obrigatória e um boleano **verbose** como opcional. 

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


-----------------------------------------------------------------------------------------------------------------------
### Métodos disponíveis

| Método         | Parâmetros                    | Retorno   | Funcionalidade                                         |
|----------------|-------------------------------|-----------|--------------------------------------------------------|
| RABScraping    | <ul><li>**matriculas**: list (Obrigatório)</li><li>**verbose**: Booleano (Opcional)</li>Valor padrão: False</ul>                             | Objeto da classe RABScraping | Construtor da classe.                  |
| obter_dados    |                              | DataFrame | Fornece os dados obtidos na consulta.                  |
| salvar_arquivo | <ul><li>**dados**: DataFrame (opcional)</li> Valor padrão: vazio. <li>**saida**: str (opcional)</li> Valor padrão: 'lista_aeronaves.csv' |          | Salva os dados da consulta em um arquivo csv ou xlsx. Se o parâmetro dados for informado, salva esse DataFrame em arquivo. |

