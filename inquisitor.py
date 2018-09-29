'''
Univesidade Federal de Pernambuco -- UFPE (http://www.ufpe.br)
Centro de Informatica -- CIn (http://www.cin.ufpe.br)
Bacharelado em Sistemas de Informacao
Autor:    Marcos Antonio Tavares Galvão
Email:    matg@cin.ufpe.br
Licenca: The MIT License (MIT)
			Copyright(c) 2018 Marcos Antonio Tavares Galvão
'''

#-----------------------------------------------------------------------------------------------------
#imports
#-----------------------------------------------------------------------------------------------------

import os
from classroom.main import *

#----------------------------------------------------------------------------------------------------

def abrirArq(alunos,local):
	'''
	retorna um dicionario, chave = Nome do diretorio, contend = [[numero da lista , [linhas do codigo]],[numero da lista , [linhas do código]]
	'''
	listagem = []
	dic = {}
	for dir_or_arquivo in alunos:
		if os.path.isdir(local + dir_or_arquivo):
			dic[dir_or_arquivo] = []
			atividades = os.listdir(local + dir_or_arquivo)
			for arquivo in atividades:
				arq = open(local + dir_or_arquivo+'/'+str(arquivo),"r", encoding="utf8")
				dic[dir_or_arquivo].append([str(arquivo[-8:-3]),arqToList(arq)])
		else:
			arq = open(local+dir_or_arquivo,"r", encoding="utf8")
			listagem.append(arqToList(arq))
	return dic


def arqToList(arquivo):
	'''
	recebe um arquivo como parametro e retorna uma lista contendo todas as linhas do codigo
	'''
	temp_list = arquivo.readlines()
	list_final = []
	flag_add = True
	aux_count = 0
	for linha in range(len(temp_list)):
		temp_list[linha] = temp_list[linha].replace(" ","")
		temp_list[linha] = temp_list[linha].replace("\t","")
		temp_list[linha] = temp_list[linha].replace("\n","")
		for key, contend in enumerate(temp_list[linha]):
			if contend is "#":  
				temp_list[linha] = temp_list[linha][:key]
				break
		if "'''" in temp_list[linha] or '"""' in temp_list[linha]:
			aux_count += 1
			if aux_count == 2:
				flag_add = True
			else:
				flag_add = False
		if len(temp_list[linha]) != 0 and flag_add == True:
			list_final.append(temp_list[linha])    
	if list_final[0] == "'''" or list_final[0] == '"""':
		del list_final[0]
	return list_final

def comparar(dic):
	'''
	executa todo o processo de comparacao das listas de todos os alunos
	checa listas iguais de todos e retorna um dicionario contendo a lista, nome do plagiador e porcentagem
	'''
	cmp = {}
	verified = []
	for pessoa1 in dic.keys():
		cmp[pessoa1] = []
		verified.append(pessoa1)
		print("processing... ({0}/{1})".format(len(verified),len(dic)))
		for lista_p1 in dic[pessoa1]:
			for pessoa2 in dic.keys():
				if pessoa2 is pessoa1 or pessoa2 in verified:
					pass
				else:
					for lista_p2 in dic[pessoa2]:
						if lista_p1[0] in lista_p2:
							cont = 0
							for linha1 in lista_p1[1]:
								for linha2 in lista_p2[1]:
									percent = string_similarity(linha1,linha2)
									if percent >= 0.7:
										cont += 1
										break

							tam = len(lista_p1[1]) if len(lista_p1[1]) > len(lista_p2[1]) else len(lista_p2[1])
							igualdade = cont/tam
							if igualdade >= 0.7:
								cmp[pessoa1].append((lista_p1[0],(pessoa2, round(igualdade*100,2))))
						else:
							pass
		if len(cmp[pessoa1]) == 0:
			del cmp[pessoa1]
	print('\n')
	return cmp

#-----------------------------------------------------------------------------------------------------
#comparação strings
#-----------------------------------------------------------------------------------------------------
# algoritmo desenvolvido por Simon White
#-----------------------------------------------------------------------------------------------------

def get_bigrams(string):
	"""
	recebe uma string e retorna uma lista contendo os bigramas.
	"""
	s = string.lower()
	return [s[i:i+2] for i in list(range(len(s) - 1))]

def string_similarity(str1, str2):
	"""
	realiza a comparacao entre os bigramas de duas string
	retorna uma porcentagem de equivalencia entre os textos
	"""
	pairs1 = get_bigrams(str1)
	pairs2 = get_bigrams(str2)
	union  = len(pairs1) + len(pairs2)
	hit_count = 0
	for x in pairs1:
		for y in pairs2:
			if x == y:
				hit_count += 1
				break
	return (2.0 * hit_count) / union

#-----------------------------------------------------------------------------------------------------
#funcionalidades extra
#-----------------------------------------------------------------------------------------------------

def imprimir(dicionario):
	'''
	imprime o dicionario resultante da comparacao
	'''
	if len(dicionario) != 0:
		for pessoa in dicionario:
			print('{0} : {1}'.format(pessoa,dicionario[pessoa]))
	else:
		print("Não houveram cópias!")

def acess_classwork():
	'''
	-lista ao usuário todos os diretorios de listas no destino /classroom/ClassWorks/
	-solicita a escolha da lista para comparacao
	-realiza a chamada das fuñcoes restantes para prosseguir a avaliacao
	'''
	diretorio = os.listdir("classroom/ClassWorks/")
	aux = 0
	print("Escolha uma opção de Lista: ")
	option = []
	for lista in diretorio:
		print("{0} - {1}".format(aux, lista))
		option.append(lista)
		aux += 1
	num_list = -1
	while num_list < 0 or num_list > aux-1:
		num_list = int(input("option: "))
	print("\n")
	local = "classroom/ClassWorks/{0}/".format(option[num_list])
	diretorio = os.listdir(local)
	pessoasAndListas = abrirArq(diretorio,local)
	repet = comparar(pessoasAndListas)
	imprimir(repet)


def chooseOption():
	print("Bem-vindo \n1 - Baixar Listas \n2 - Inspecionar cópias \n3 - Sair")
	option = 0
	while option > 3 or option < 1:
		try:
			option = int(input("\n Escolha uma opção: "))
		except:
			print("Opção inválida!")
	print("\n")
	if option == 1:
		PlagiarismCheckerApplication()
		print("\n")
		chooseOption()
	elif option == 2:
		acess_classwork()
		print("\n")
		chooseOption()
	else:
		print("Programa Finalizado!")
		exit()

#-----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	chooseOption()