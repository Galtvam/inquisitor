#-----------------------------------------------------------------------------------------------------
#imports
#-----------------------------------------------------------------------------------------------------

import os

#----------------------------------------------------------------------------------------------------

def abrirArq(diretorios):
	'''
	retorna um dicionário, chave = Nome do diretório, contend = [[numero da lista , [linhas do código]],[numero da lista , [linhas do código]]
	'''
	listagem = []
	dic = {}
	for dir_or_arquivo in diretorios:
		if os.path.isdir(dir_or_arquivo):
			dic[dir_or_arquivo] = []
			atividades = os.listdir(dir_or_arquivo)
			for arquivo in atividades:
				arq = open(str(dir_or_arquivo)+'/'+str(arquivo),"r", encoding="utf8")
				dic[dir_or_arquivo].append([str(arquivo[-8:-3]),arqToList(arq)])
		else:
			arq = open(dir_or_arquivo,"r", encoding="utf8")
			listagem.append(arqToList(arq))
	return dic

def arqToList(arquivo):
	temp_list = arquivo.readlines()
	list_final = []
	for linha in range(len(temp_list)):
		temp_list[linha] = temp_list[linha].replace(" ","")
		temp_list[linha] = temp_list[linha].replace("\t","")
		temp_list[linha] = temp_list[linha].replace("\n","")
		for key, contend in enumerate(temp_list[linha]):
			if contend is "#":  
				temp_list[linha] = temp_list[linha][:key]
				break
		if temp_list[linha] is not "":
			list_final.append(temp_list[linha])    
	if "'''" in list_final[0]:
		list_final = list_final[6:]
	return list_final

def comparar(dic):
	cmp = {}
	verified = []
	for pessoa1 in dic.keys():
		cmp[pessoa1] = []
		verified.append(pessoa1)
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
								cmp[pessoa1].append((lista_p1[0],(pessoa2, igualdade*100)))
						else:
							pass
		if len(cmp[pessoa1]) == 0:
			del cmp[pessoa1]
	return cmp

#-----------------------------------------------------------------------------------------------------
#comparação strings
#-----------------------------------------------------------------------------------------------------

def get_bigrams(string):
	"""
	Take a string and return a list of bigrams.
	"""
	s = string.lower()
	return [s[i:i+2] for i in list(range(len(s) - 1))]

def string_similarity(str1, str2):
	"""
	Perform bigram comparison between two strings
	and return a percentage match in decimal form.
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
    for pessoa in dicionario:
        print('{0} : {1}'.format(pessoa,dicionario[pessoa]))

#-----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	diretorio = os.listdir()
	diretorio.remove(os.path.basename(__file__))
	pessoasAndListas = abrirArq(diretorio)
	repet = comparar(pessoasAndListas)
	imprimir(repet)