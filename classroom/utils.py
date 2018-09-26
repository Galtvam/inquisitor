import io
import sys

def supress_module_print():
  new_stdout = io.StringIO()
  sys.stdout = new_stdout

def input(*args, **kwargs):
  sys.stdout = sys.__stdout__

  input_answer = globals()['__builtins__']['input'](*args, **kwargs)

  supress_module_print()

  return input_answer

def print(*args, **kwargs):
  sys.stdout = sys.__stdout__

  globals()['__builtins__']['print'](*args, **kwargs)

  supress_module_print()

def input_int(message, min_value, max_value, errorMessage="Erro: Opção inválida!"):
  anwser = None
  while anwser is None:
    try:
      anwser = int(input(message))
      if anwser < min_value or anwser > max_value:
        raise RuntimeError("invalid option")
    except:
      anwser = None
      print(errorMessage)
  return anwser