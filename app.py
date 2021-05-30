from rabscraping import RABScraping


lista = RABScraping(['PR-GUM','PS-AEH', 'PR-PJN', 'XE', 'PR-TOL'], verbose=True)
lista.obter_dados()
lista.salvar_arquivo()