from lib.rabscraping import RABScraping

lista_matriculas = ['PR-GUM','PS-AEH', 'PR-PJN', 'XE', 'PR-TOL']
lista_matriculas = ('PR-GUM','PS-AEH', 'PR-PJN', 'XE', 'PR-TOL')

lista = RABScraping(matriculas=lista_matriculas, verbose=True)
lista.obter_dados()
lista.salvar_arquivo()