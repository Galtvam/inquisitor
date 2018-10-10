# inquisitor

Sistema de verificação de plagio em listas

Funcionalidades:
  -Baixa listas enviadas pelo classroom diretamente na pasta do pragrama
  -Executa verificação de plágio entre todas as questões enviadas na lista escolhida
  
Como utilizar:
  1. Escolha a opção para executar ('baixar listas' ou  'inspecionar copias'):
  
    1.1. Baixar Listas:
        - Seu navegador se abrirá solicitando autorização de acesso na sua conta do Google
        - Você deverá escolher em qual turma do classroom ele deve listar as atividades
        - Escolha a lista para ser baixada e o download será automaticamente iniciado
          Obs: Todas as listas baixadas se encontraram na pasta classroom/ClasssWorks/
    
    1.2. Inspecionar Listas:
        - Você deverá escolher qual lista deve ser inspecionada
        - Ao fim da verificação o programa te informará uma listagem com os nomes do produtor da lista, juntamente terá o a lista plagiada e o nome do plagiador. (Obs: O programa retornará uma porcentagem, ocasionalmente ocorrem Falsos-Positivos)
        
  2. Habilidades:
  
    2.1. Reconhecimento de mudanças:
        - O programa possui a capacidade de detectar alterações em nomes de variáveis ou textos, avaliando a similiaridade entre os comandos utilizados linha-a-linha.
        - Mesmo que o usuário inverta ordens de execução dos comandos o programa identificará.
        - Desconsideras docstrings e comentários
        
Problemas conhecidos:
 - Quando a atividade Lista 4(versão 2) for baixada deve ser renomeada para Lista 4 caso contrario acarreterá em quebra de execução.
