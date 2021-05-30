class InvalidFileError(Exception):

  def __init__(self, *args):
    if args:
      self.mensagem = args[0]
    else:
      self.mensagem = None

  def __str__(self):
    if self.mensagem:
      return "Tipo de arquivo não suportado :\
              tipo informado: {0}\
              informe .xlsx ou .csv".format(self.mensagem)
    else:
      return "Tipo de arquivo não suportado. Informe xlsx ou csv"