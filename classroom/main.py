'''
Universidade Federal de Pernambuco (UFPE) (http://www.ufpe.br)
Centro de Informática (CIn) (http://www.cin.ufpe.br)
Graduando em Sistemas de Informação
IF969 - Algoritmos e Estrutura de Dados

Autor: Igor Fernandes Carneiro (ifc)
E-mail: ifc@cin.ufpe.br

Copyright(c) 2018 Igor Fernandes Carneiro
'''

from classroom.classroom import Classroom

# Módulo para suprimir print dados por outros módulos
from classroom.utils import supress_module_print, print, input, input_int

from datetime import datetime

import classroom.httplib2 as httplib2
import os

class PlagiarismCheckerApplication:
  __DOWNLOAD_DIR = "classroom/ClassWorks/"

  def __init__(self):
    supress_module_print()

    print("################ Bem-vindo ao PlagiarismChecker ################\n")

    print("Inicializando aplicação...")

    # Criando a pasta de Downloads
    if not os.path.exists(PlagiarismCheckerApplication.__DOWNLOAD_DIR):
      os.makedirs(PlagiarismCheckerApplication.__DOWNLOAD_DIR)

    try:
      self.__classroom = Classroom('credentials.json', 'token.json')
      
      if not self.__classroom.hasPermission():
        print("\nPara iniciar a aplicação, realize o login no Classroom, pelo seu navegador.")
        print("Abrindo navegador...")

        self.__classroom.obtainAccessCredentials()

      self.__run()

    except httplib2.ServerNotFoundError:
      print("Erro: Não foi possível conectar-se aos servidores do Google!")
      print("      Tente executar aplicação novamente em poucos segundos.")

  def __run(self):
    print("\nCarregando turmas...\n")
    courses = self.__classroom.getCourses()

    if len(courses) == 0:
      print("Você não possui turmas para utilizar a aplicação!")
      return

    selectedCourse = self.__askSelectCourse(courses)

    print("\nCarregando dados dos alunos da turma...\n")

    students = self.__classroom.getStudents(selectedCourse['id'])

    print("\nCarregando tarefas criadas...\n")   

    courseWorks = self.__classroom.getCourseWorks(selectedCourse['id'])

    if len(courseWorks) == 0:
      print("Ainda não há exercícios nesta turma!")
      return

    selectedCourseWork = self.__askCourseWork(courseWorks)

    print("\nCarregando submissões dos alunos...")

    studentSubmissions = self.__classroom.getStudentSubmissions(
      selectedCourse['id'], selectedCourseWork['id']
    )

    self.__downloadStudentSubmissions(
      selectedCourseWork['title'], studentSubmissions, students
    )


  def __askSelectCourse(self, courses):
    print("Qual é a turma contém os exerícios de Programação?")
    for index, course in enumerate(courses):
      name = course['name']
      status = course['courseState']
      createdDate = datetime.strptime(
        course['creationTime'], "%Y-%m-%dT%H:%M:%S.%fZ"
      )
      strCreateDate = createdDate.strftime("%d/%m/%Y às %H:%M")
      finalString = "{0} - {1} \n   Status: {2}\n   Criado em: {3}\n"
      print(finalString.format(index + 1, name, status, strCreateDate))

    courseIndex = input_int(
      "Escolha dentre as opções acima: ", 
      1, len(course) - 1, 
      "Erro: Opção inválida!"
    )

    courseIndex -= 1
    return courses[courseIndex]

  def __askCourseWork(self, courseWorks):
    print("\n\nEm qual das tarefas abaixo você deseja executar o programa? ")

    for index, work in enumerate(courseWorks):
      title = work['title']
      status = work['state']
      workDueDate = work['dueDate']
      workDueTime = work['dueTime']
      dueDate = datetime(
        workDueDate['year'], workDueDate['month'], workDueDate['day'], 
        workDueTime['hours'], workDueTime['minutes']
      )
      createdDate = datetime.strptime(
        work['creationTime'], "%Y-%m-%dT%H:%M:%S.%fZ"
      )
      strCreateDate = createdDate.strftime("%d/%m/%Y às %H:%M")
      strDueDate = dueDate.strftime("%d/%m/%Y às %H:%M")
      finalString = ("{0} - {1} \n   Status: {2}\n   Criado em: " +
                     "{3} \n   Prazo: {4}\n")
      print(finalString.format(
        index + 1, title, status, strCreateDate, strDueDate)
      )
    
    courseWorkIndex = input_int(
      "Escolha dentre as opções acima: ", 
      1, len(courseWorks), 
      "Erro: Opção inválida!"
    )

    courseWorkIndex -= 1
    return courseWorks[courseWorkIndex]

  def __get_student_by_id(self, studentId, students):
    for student in students:
      if student['userId'] == studentId:
        return student
    return None

  def __downloadStudentSubmissions(self, courseWorkName, submissions, students):
    # Criar a pasta
    courseWorkDir = self.__getCourseWorkDir(courseWorkName)

    if not os.path.exists(courseWorkDir):
      os.makedirs(courseWorkDir)

    totalSubmissions = len(submissions)

    print("\nBaixando tarefas dos alunos...")
    print("Há num total de {0} submissões: \n".format(totalSubmissions))

    cantDownloadFiles = {}

    for index, submission in enumerate(submissions):
      student = self.__get_student_by_id(submission['userId'], students)
      studentName = student['profile']['name']['fullName']

      attachments = submission['assignmentSubmission']
      if not "attachments" in attachments:
        errorMessage = "{0} ({1}/{2}): submeteu, mas não enviou anexos!\n"
        print(errorMessage.format(studentName, index + 1, totalSubmissions))
        continue 
      
      attachments = attachments['attachments']

      studentDir = self.__getCourseWorkFilePath(
        courseWorkName, studentName, ""
      )

      if not os.path.exists(studentDir):
        os.makedirs(studentDir)

      print("{0} ({1}/{2}): ".format(studentName, index + 1, totalSubmissions))

      for attachment in attachments:
        if not "driveFile" in attachment:
          typeAttacment = tuple(attachment.keys())[0]
          finalString = "   Tipo de anexo não reconhecido pelo programa ({0})!"
          print(finalString.format(typeAttacment))
        else:
          driveFile = attachment['driveFile']
          filename = driveFile['title']
          fileId = driveFile['id']
          print("   Baixando '{0}'...".format(filename))
          filepath = self.__getCourseWorkFilePath(
            courseWorkName, studentName, filename
          )
          try:
            self.__classroom.downloadFile(fileId, filepath)
          except:
            if not studentName in cantDownloadFiles:
              cantDownloadFiles[studentName] = []
            cantDownloadFiles[studentName].append(filename)
            print("   Não foi possível baixar o arquivo: '{0}'!".format(filename))

      print()

    print("Download das tarefas concluída!")

    if len(cantDownloadFiles) > 0:
      print("Os anexos dos seguintes alunos não puderam ser baixados: \n")
      for studentName in cantDownloadFiles:
        print("{0}:".format(studentName))
        for index, filename in enumerate(cantDownloadFiles[studentName]):
          print("   {0} - '{1}'".format(index + 1, filename))

  def __getCourseWorkDir(self, courseWorkName):
    downloadDir = os.path.realpath(PlagiarismCheckerApplication.__DOWNLOAD_DIR)
    courseWorkDir = os.path.join(downloadDir, courseWorkName)
    return courseWorkDir

  def __getCourseWorkFilePath(self, courseWorkName, studentName, filename):
    downloadDir = os.path.realpath(PlagiarismCheckerApplication.__DOWNLOAD_DIR)
    courseWorkDir = os.path.join(downloadDir, courseWorkName)
    courseWorkStudentDir = os.path.join(courseWorkDir, studentName)
    filepath = os.path.join(courseWorkStudentDir, filename)
    return filepath

if __name__ == '__main__':
  program = PlagiarismCheckerApplication()
