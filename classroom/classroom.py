'''
Universidade Federal de Pernambuco (UFPE) (http://www.ufpe.br)
Centro de Informática (CIn) (http://www.cin.ufpe.br)
Graduando em Sistemas de Informação
IF969 - Algoritmos e Estrutura de Dados

Autor: Igor Fernandes Carneiro (ifc)
E-mail: ifc@cin.ufpe.br
Data: 2018-09-22

Copyright(c) 2018 Igor Fernandes Carneiro
'''

from classroom.googleapiclient.discovery import build
from classroom.httplib2 import Http
from classroom.googleapiclient.http import MediaIoBaseDownload
from classroom.oauth2client import file, client, tools

import io

# TODO: Remover depois de concluir
from classroom.utils import supress_module_print, print

class Classroom:
  __SCOPES = (
    "https://www.googleapis.com/auth/classroom.courses.readonly " + 
    "https://www.googleapis.com/auth/classroom.coursework.students.readonly " +
    "https://www.googleapis.com/auth/classroom.rosters.readonly " + 
    "https://www.googleapis.com/auth/drive.readonly"
  )

  def __init__(self, clientSecretsFile, tokenFile):
    self.__clientSecretsFile = clientSecretsFile
    self.__tokenFile = tokenFile

    self.__store = file.Storage(tokenFile)
    self.__credentials = self.__getCredentialsFromTokenFile(
      self.__store, tokenFile
    )

    self.__http = None
    self.__classroomService = None
    self.__driveService = None

    if self.__credentials is not None:
      self.__buildServices()

  def obtainAccessCredentials(self):
    if not self.hasPermission():
      flow = client.flow_from_clientsecrets(
        self.__clientSecretsFile, Classroom.__SCOPES
      )
      self.__credentials = tools.run_flow(flow, self.__store)

    self.__buildServices()

  def hasPermission(self):
    return self.__credentials and not self.__credentials.invalid

  def getCourses(self, quantity=15):
    self.__raiseNotClassroomService()

    results = self.__classroomService.courses().list(pageSize=quantity).execute()
    return results.get('courses', [])

  def getStudents(self, courseId):
    self.__raiseNotClassroomService()

    finalResult = []
    nextPageToken = ""

    while nextPageToken is not None:
      args = {
        "courseId": courseId
      }

      if nextPageToken is not None:
        args["pageToken"] = nextPageToken

      results = self.__classroomService.courses().students().list(**args).execute()
      finalResult += results.get('students', [])
      nextPageToken = results.get('nextPageToken')

    return finalResult

  def getCourseWorks(self, courseId, quantity=15):
    self.__raiseNotClassroomService()

    results = self.__classroomService.courses().courseWork().list(
      courseId=courseId, 
      pageSize=quantity
    ).execute()
    return results.get('courseWork', [])

  def getStudentSubmissions(self, courseId, courseWorkId):
    self.__raiseNotClassroomService()

    submissionService = self.__classroomService.courses()\
                        .courseWork().studentSubmissions()

    finalResult = []
    nextPageToken = ""

    while nextPageToken is not None:
      args = {
        "courseId": courseId, 
        "courseWorkId": courseWorkId
      }

      if nextPageToken is not None:
        args["pageToken"] = nextPageToken

      results = submissionService.list(**args).execute()
      finalResult += results.get('studentSubmissions', [])
      nextPageToken = results.get('nextPageToken')

    return finalResult

  def downloadFile(self, driveFileId, filepath):
    request = self.__driveService.files().get_media(fileId=driveFileId)
    fh = io.FileIO(filepath, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        # print("Download %d%%." % int(status.progress() * 100))

  def __getCredentialsFromTokenFile(self, store, tokenFilename):
    try:
      with open(tokenFilename, 'r') as file:
        return store.get()
    except:
      return None

  def __buildServices(self):
    self.__http = self.__credentials.authorize(Http())
    self.__classroomService = build('classroom', 'v1', http=self.__http)
    self.__driveService = build('drive', 'v3', http=self.__http)

  def __raiseNoPermission(self):
    if not self.hasPermission():
      raise PermissionError("no permission to access Classroom")

  def __raiseNotClassroomService(self):
    self.__raiseNoPermission()
    if not self.__classroomService:
      raise RuntimeError("classroom service not initializated")

  def __raiseNotDriveService(self):
    self.__raiseNoPermission()
    if not self.__driveService:
      raise RuntimeError("drive service not initializated")
