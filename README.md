# inquisitor

Sistema de verificação de plagio em listas

Funcionalidades:
  - Baixa listas enviadas pelo classroom diretamente na pasta do pragrama
  - Executa verificação de plágio entre todas as questões, de todos os alunos, enviadas na lista escolhidade.
  
Como utilizar:
  1. Escolha a opção para executar ('baixar listas' ou  'inspecionar copias'):
  
    1.1. Baixar Listas:
        - Seu navegador se abrirá solicitando autorização de acesso na sua conta do Google
        - Você deverá escolher em qual turma do classroom ele deve listar as atividades
        - Escolha a lista para ser baixada e o download será automaticamente iniciado
          Obs: Todas as listas baixadas se encontraram na pasta classroom/ClasssWorks/
    
    1.2. Inspecionar Listas:
        - Você deverá escolher qual lista deve ser inspecionada
        - Caso existam arquivos nomeadas fora do padrão l#-q#.py (onde o # corresponde a um número) será solicitado ao inspetor o número correto da questão a qual está associado o respectivo arquivo.
        - Ao fim da verificação o programa te informará uma listagem com os nomes do produtor da lista, juntamente terá a lista plagiada e o nome do plagiador. (Obs: O programa retornará uma porcentagem, ocasionalmente ocorrem Falsos-Positivos)
        
  2. Habilidades:
  
    2.1. Reconhecimento de mudanças:
        - O programa possui a capacidade de detectar alterações em nomes de variáveis ou textos, avaliando a similiaridade entre os comandos utilizados linha-a-linha.
        - Mesmo que o usuário inverta ordens de execução dos comandos o programa identificará.
        - Desconsidera docstrings e comentários
  
  3. Necessidades para funcionamento:
    
    OBS: Caso o download direto do classroom da Utilidade 1 seja usado desconsidere as necessidades abaixo:
    - Cada aluno pussiu uma pasta com seu nome, dentro do diretorio de "Lista #", dentro da pasta com o nome do mesmo estarão os arquivos .py nomeados no padrão "l#-q#.py" onde # corresponde ao numero da lista e questão, respectivamente.
    - Os diretórios dos alunos devem estar dentro de uma pasta nomeada como "Lista #" onde # corresponde ao numero da lista.
    - As pastas contendo as listas, por exemplo, a pasta chamada "Lista 4" contendo as listas de numero 4, devem estar no diretório classroom/ClasssWorks/
    
    3.1 Exemplo de diretorio ate uma lista
       - classroom/ClasssWorks/Lista 4/Marcos Galvão/l4-q2.py
        
Problemas conhecidos:
 - Quando a atividade Lista 4(versão 2) for baixada deve ser renomeada para Lista 4 caso contrario acarreterá em quebra de execução, devido ao programa não aceitar um nome de diretório diferente de "Lista #".
