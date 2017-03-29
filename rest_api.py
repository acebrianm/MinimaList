import endpoints
from google.appengine.ext import ndb
from google.appengine.api import app_identity
from protorpc import remote

import jwt
import time

from CustomExceptions import NotFoundException

from messages import EmailPasswordMessage, TokenMessage, CodeMessage, Token, TokenKey,MessageNone
from messages import EmpresaInput, EmpresaUpdate, EmpresaList
from messages import TeamInput, TeamUpdate, TeamList
from messages import ArtistInput, ArtistUpdate, ArtistList
from messages import UserInput, UserUpdate, UserList
from messages import GeneroInput, GeneroUpdate, GeneroList
from messages import ServicioInput, ServicioUpdate, ServicioList
from messages import SponsorInput, SponsorUpdate, SponsorList

from endpoints_proto_datastore.ndb import EndpointsModel

import models
from models import validarEmail
from models import Empresa, Usuarios, Team, Artist, Genero, Sponsor, Servicio

###############
# Usuarios
###############
@endpoints.api(name='usuarios_api', version='v1', description='usuarios endpoints')
class UsuariosApi(remote.Service):
###############get the info of one########
 @endpoints.method(TokenKey, UserList, path='users/get', http_method='POST', name='users.get')
 def users_get(cls, request):
  try:                 
   token = jwt.decode(request.tokenint, 'secret')  #checa token
   userentity = ndb.Key(urlsafe=request.entityKey)
   user = Usuarios.get_by_id(userentity.id()) #obtiene usuario
            #user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = []  #crea lista
   lstMessage = UserList(code=1) # crea objeto mensaje
   lista.append(UserUpdate(token='', 
    entityKey= user.entityKey,
    #empresa_key = user.empresa_key.urlsafe(),
    email = user.email))
   lstMessage.data = lista#ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = UserList(code=-1, data=[]) #token invalido
  except jwt.ExpiredSignatureError:
   message = UserList(code=-2, data=[]) #token expiro
  return message


########################## list###################
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, UserList, path='users/list', http_method='POST', name='users.list')
 def lista_usuarios(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')  #checa token
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = []  #crea lista
   lstMessage = UserList(code=1) # crea objeto mensaje
   lstBd = Usuarios.query().fetch() # recupera de base de datos
   for i in lstBd: # recorre
    lista.append(UserUpdate(token='',
     entityKey=i.entityKey,
     #empresa_key=user.empresa_key.urlsafe(),
     email=i.email)) # agrega a la lista
    
   lstMessage.data = lista # la manda al messa
   message = lstMessage #regresa
    
  except jwt.DecodeError:
   message = UserList(code=-1, data=[]) #token invalido
  except jwt.ExpiredSignatureError:
   message = UserList(code=-2, data=[]) #token expiro
  return message

# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='users/delete', http_method='POST', name='users.delete')
 #siempre lleva cls y request
 def user_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   usersentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   usersentity.delete()#BORRA
   message = CodeMessage(code=1, message='Succesfully deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(UserInput, CodeMessage, path='users/insert', http_method='POST', name='users.insert')
 def user_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])
   if validarEmail(request.email) == False: #checa si el email esta registrado
                       #empresakey = ndb.Key(urlsafe=request.empresa_key) #convierte el string dado a entityKey
    if user.usuario_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
     codigo=1
    else:
     codigo=-3
                       #la funcion josue_m puede actualizar e insertar
                       #depende de la ENTRADA de este endpoint method
    message = CodeMessage(code=codigo, message='Succesfully added')
   else:
    message = CodeMessage(code=-4, message='El email ya ha sido registrado')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message


##login##

 @endpoints.method(EmailPasswordMessage, TokenMessage, path='users/login', http_method='POST', name='users.login')
 def users_login(cls, request):
  try:
   user = Usuarios.query(Usuarios.email == request.email).fetch() #obtiene el usuario dado el email
   if not user or len(user) == 0: #si no encuentra user saca
    raise NotFoundException()
   user = user[0] 
   keye = user.empresa_key.urlsafe() # regresa como mensaje el empresa key
   if not user.verify_password(request.password): # checa la contrasena
    raise NotFoundException()

   token = jwt.encode({'user_id': user.key.id(), 'exp': time.time() + 43200}, 'secret') #crea el token
   message = TokenMessage(token=token, message=keye, code=1) # regresa token
  except NotFoundException:
   message = TokenMessage(token=None, message='Wrong username or password', code=-1)
  return message

##update##
# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(UserUpdate, CodeMessage, path='user/update', http_method='POST', name='user.update')
#siempre lleva cls y request
 def user_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   if user.usuario_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message


'''
'''

###########################
#### Empresa
###########################


## Google Cloud Endpoint
@endpoints.api(name='empresas_api', version='v1', description='empresas REST API')
class EmpresasApi(remote.Service):


# get one

 @endpoints.method(TokenKey, EmpresaList, path='empresa/get', http_method='POST', name='empresa.get')
#siempre lleva cls y request
 def empresa_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   empresaentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #empresaentity.get().empresa_key.urlsafe() para poder optener el EntityKey
     ##### ejemplo real
    ####### message = EmpresaList(code=1, data=[EmpresaUpdate(token='Succesfully get', nombre_empresa=empresaentity.get().nombre_empresa, empresa_key=empresaentity.get().empresa_key.urlsafe(), entityKey=empresaentity.get().entityKey)])
   message = EmpresaList(code=1, data = [EmpresaUpdate(token='Succesfully get',
    entityKey = empresaentity.get().entityKey,
    codigo_empresa=empresaentity.get().codigo_empresa, 
    nombre_empresa = empresaentity.get().nombre_empresa,
    lat = empresaentity.get().lat,
    lng = empresaentity.get().lng)])

  except jwt.DecodeError:
   message = EmpresaList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = EmpresaList(code=-2, data=[])
  return message




 @endpoints.method(TokenKey, CodeMessage, path='empresa/delete', http_method='POST', name='empresa.delete')
#siempre lleva cls y request
 def empresa_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   empresaentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   empresaentity.delete()#BORRA
   message = CodeMessage(code=1, message='Succesfully deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message


# insert
 @endpoints.method(EmpresaInput, CodeMessage, path='empresa/insert', http_method='POST', name='empresa.insert')
#siempre lleva cls y request
 def empresa_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario models.py 
   myempresa = Empresa()
   if myempresa.empresa_m(request)==0: 
    codigo=1
   else: codigo=-3 #la funcion josue_m puede actualizar e insertar
	      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Succesfully added')
      #else:
	    #  message = CodeMessage(code=-4, message='Succesfully added')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message



# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(EmpresaUpdate, CodeMessage, path='empresa/update', http_method='POST', name='empresa.update')
#siempre lleva cls y request
 def empresa_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN 
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
      #empresakey = ndb.Key(urlsafe=request.empresa_key)#convierte el string dado a entityKey
   myempresa = Empresa()
   if myempresa.empresa_m(request)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message



# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, EmpresaList, path='empresa/list', http_method='POST', name='empresa.list')
#siempre lleva cls y request
 def empresa_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   #if user.importante==1 or user.importante==2:
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = EmpresaList(code=1) #CREA el mensaje de salida
   lstBdEmpresa = Empresa.query().fetch() #obtiene de la base de datos
   for i in lstBdEmpresa: #recorre la base de datos
             #inserta a la lista creada con los elementos que se necesiten de la base de datos
             #i.empresa_key.urlsafe() obtiene el entityKey
	     #lista.append(ClientesUpdate(token='', nombre=i.nombre, status=i.status, empresa_key=i.empresa_key.urlsafe(), entityKey=i.entityKey))
    lista.append(EmpresaUpdate(token='', 
     entityKey = i.entityKey,
     codigo_empresa=i.codigo_empresa, 
     nombre_empresa = i.nombre_empresa,
     lat = i.lat,
     lng = i.lng))
      
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
      #else:
      #    message = EmpresaList(code=-3, data=[])
  except jwt.DecodeError:
   message = EmpresaList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = EmpresaList(code=-2, data=[])
  return message


###########################
#### Team
###########################

@endpoints.api(name='team_api', version='v1', description='team REST API')
class TeamApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, TeamList, path='team/get', http_method='POST', name='team.get')
#siempre lleva cls y request
 def team_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   teamentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = TeamList(code=1, data=[TeamUpdate(token='Succesfully get',
    entityKey=teamentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(), 
    nombre=teamentity.get().nombre, 
    puesto=teamentity.get().puesto, 
    urlImage=teamentity.get().urlImage)])
  except jwt.DecodeError:
   message = TeamList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = TeamList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='team/delete', http_method='POST', name='team.delete')
#siempre lleva cls y request
 def team_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   teamentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   teamentity.delete()#BORRA
   message = CodeMessage(code=0, message='Se ha eliminado el r.h.')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, TeamList, path='team/list', http_method='POST', name='team.list')
#siempre lleva cls y request
 def team_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = TeamList(code=1) #CREA el mensaje de salida
   lstBd = Team.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
	     
    lista.append(TeamUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     nombre=i.nombre, 
     puesto=i.puesto, 
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = TeamList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = TeamList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TeamInput, CodeMessage, path='team/insert', http_method='POST', name='team.insert')
#siempre lleva cls y request
 def team_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   myteam = Team()
   if myteam.team_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Su r.h. se ha sido registrado exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TeamUpdate, CodeMessage, path='team/update', http_method='POST', name='team.update')
#siempre lleva cls y request
 def team_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   myteam = Team()
   if myteam.team_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

###########################
#### Artist
###########################

@endpoints.api(name='artist_api', version='v1', description='Artist REST API')
class ArtistApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, ArtistList, path='artist/get', http_method='POST', name='artist.get')
#siempre lleva cls y request
 def artist_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   artist_entity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = ArtistList(code=1, data=[ArtistUpdate(token='Succesfully get',
    entityKey=artist_entity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(), 
    nombre=artist_entity.get().nombre, 
    urlImage=artist_entity.get().urlImage)])
  except jwt.DecodeError:
   message = ArtistList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = ArtistList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='artist/delete', http_method='POST', name='artist.delete')
#siempre lleva cls y request
 def artist_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   artist_entity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   artist_entity.delete()#BORRA
   message = CodeMessage(code=0, message='Se ha eliminado el artista')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, ArtistList, path='artist/list', http_method='POST', name='artist.list')
#siempre lleva cls y request
 def artist_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = ArtistList(code=1) #CREA el mensaje de salida
   lstBd = Artist.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
	     
    lista.append(ArtistUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     nombre=i.nombre, 
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = ArtistList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = ArtistList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(ArtistInput, CodeMessage, path='artist/insert', http_method='POST', name='artist.insert')
#siempre lleva cls y request
 def artist_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   myartist = Artist()
   if myartist.artist_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Su artista se ha sido registrado exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(ArtistUpdate, CodeMessage, path='artist/update', http_method='POST', name='artist.update')
#siempre lleva cls y request
 def artist_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   myartist = Artist()
   if myartist.artist_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

###########################
#### Genero
###########################

@endpoints.api(name='genero_api', version='v1', description='Genero REST API')
class GeneroApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, GeneroList, path='genero/get', http_method='POST', name='genero.get')
#siempre lleva cls y request
 def genero_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   genero_entity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = GeneroList(code=1, data=[GeneroUpdate(token='Succesfully get',
    entityKey=genero_entity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(), 
    nombre=genero_entity.get().nombre, 
    urlImage=genero_entity.get().urlImage)])
  except jwt.DecodeError:
   message = GeneroList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = GeneroList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='genero/delete', http_method='POST', name='genero.delete')
#siempre lleva cls y request
 def genero_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   genero_entity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   genero_entity.delete()#BORRA
   message = CodeMessage(code=0, message='Se ha eliminado el genero')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, GeneroList, path='genero/list', http_method='POST', name='genero.list')
#siempre lleva cls y request
 def genero_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = GeneroList(code=1) #CREA el mensaje de salida
   lstBd = Genero.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
	     
    lista.append(GeneroUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     nombre=i.nombre, 
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = GeneroList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = GeneroList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(GeneroInput, CodeMessage, path='genero/insert', http_method='POST', name='genero.insert')
#siempre lleva cls y request
 def genero_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   mygenero = Genero()
   if mygenero.genero_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Su genero se ha sido registrado exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(GeneroUpdate, CodeMessage, path='genero/update', http_method='POST', name='genero.update')
#siempre lleva cls y request
 def genero_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   mygenero = Genero()
   if mygenero.genero_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

###########################
#### Servicio
###########################

@endpoints.api(name='servicio_api', version='v1', description='Servicio REST API')
class ServicioApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, ServicioList, path='servicio/get', http_method='POST', name='servicio.get')
#siempre lleva cls y request
 def servicio_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   servicio_entity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = ServicioList(code=1, data=[ServicioUpdate(token='Succesfully get',
    entityKey=servicio_entity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(), 
    nombre=servicio_entity.get().nombre, 
    urlImage=servicio_entity.get().urlImage)])
  except jwt.DecodeError:
   message = ServicioList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = ServicioList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='servicio/delete', http_method='POST', name='servicio.delete')
#siempre lleva cls y request
 def servicio_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   servicio_entity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   servicio_entity.delete()#BORRA
   message = CodeMessage(code=0, message='Se ha eliminado el servicio')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, ServicioList, path='servicio/list', http_method='POST', name='servicio.list')
#siempre lleva cls y request
 def servicio_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = ServicioList(code=1) #CREA el mensaje de salida
   lstBd = Servicio.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
	     
    lista.append(ServicioUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     nombre=i.nombre, 
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = ServicioList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = ServicioList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(ServicioInput, CodeMessage, path='servicio/insert', http_method='POST', name='servicio.insert')
#siempre lleva cls y request
 def servicio_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   myserv = Servicio()
   if myserv.servicio_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Su servicio se ha sido registrado exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(ServicioUpdate, CodeMessage, path='servicio/update', http_method='POST', name='servicio.update')
#siempre lleva cls y request
 def servicio_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   myserv = Servicio()
   if myserv.servicio_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

###########################
#### Sponsor
###########################

@endpoints.api(name='sponsor_api', version='v1', description='Sponsor REST API')
class SponsorApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, SponsorList, path='sponsor/get', http_method='POST', name='sponsor.get')
#siempre lleva cls y request
 def sponsor_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   sponsor_entity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = SponsorList(code=1, data=[SponsorUpdate(token='Succesfully get',
    entityKey=sponsor_entity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(), 
    nombre=sponsor_entity.get().nombre, 
    urlImage=sponsor_entity.get().urlImage)])
  except jwt.DecodeError:
   message = SponsorList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = SponsorList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='sponsor/delete', http_method='POST', name='sponsor.delete')
#siempre lleva cls y request
 def sponsor_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   sponsor_entity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   sponsor_entity.delete()#BORRA
   message = CodeMessage(code=0, message='Se ha eliminado el sponsor')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, SponsorList, path='sponsor/list', http_method='POST', name='sponsor.list')
#siempre lleva cls y request
 def sponsor_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = SponsorList(code=1) #CREA el mensaje de salida
   lstBd = Sponsor.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
	     
    lista.append(SponsorUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     nombre=i.nombre, 
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = SponsorList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = SponsorList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(SponsorInput, CodeMessage, path='sponsor/insert', http_method='POST', name='sponsor.insert')
#siempre lleva cls y request
 def sponsor_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   myspon = Sponsor()
   if myspon.sponsor_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Su sponsor se ha sido registrado exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(SponsorUpdate, CodeMessage, path='sponsor/update', http_method='POST', name='sponsor.update')
#siempre lleva cls y request
 def sponsor_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   myspon = Sponsor()
   if myspon.sponsor_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

application = endpoints.api_server([UsuariosApi, EmpresasApi, TeamApi,
    ArtistApi, GeneroApi, ServicioApi, SponsorApi], restricted=False)

