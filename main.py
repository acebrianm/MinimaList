import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import app_identity
from google.appengine.api import images
from google.appengine.ext import blobstore
import cloudstorage
import mimetypes
import json
import os
import jinja2

from models import Empresa, Team, Artist, Genero

jinja_env = jinja2.Environment(
 loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class DemoClass(object):
 pass

def MyClass(obj):
 return obj.__dict__


class GetTeamHandler(webapp2.RequestHandler):

    def get(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*')
     self.response.headers['Content-Type'] = 'application/json'

     id_empresa = self.request.get('empresa')
     objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()
     strKey = objemp.key.urlsafe() 
     myEmpKey = ndb.Key(urlsafe=strKey) 
     myTeam = Team.query(Team.empresa_key == myEmpKey)

     myList = []
     for i in myTeam:
      myObj = DemoClass()
      myObj.nombre = i.nombre
      myObj.puesto = i.puesto
      myObj.urlImage = i.urlImage
      myList.append(myObj)
       
     json_string = json.dumps(myList, default=MyClass)
     self.response.write(json_string)

class GetArtistHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'

        id_empresa = self.request.get('empresa')
        objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()
        strKey = objemp.key.urlsafe()
        myEmpKey = ndb.Key(urlsafe=strkey)
        myartist = Artist.query(Artist.empresa_key == myEmpKey)

        myList = []
        for i in myartist:
            myObj = DemoClass()
            myObj.nombre = i.nombre
            myObj.urlImage = i.urlImage

            myList.append(myObj)

        json_string = json.dumps(myList, default=Myclass)
        self.response.write(json_string)

class GetGeneroHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'

        id_empresa = self.request.get('empresa')
        objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()
        strKey = objemp.key.urlsafe()
        myEmpKey = ndb.Key(urlsafe=strkey)
        mygenero = Genero.query(Genero.empresa_key == myEmpKey)

        myList = []
        for i in mygenero:
            myObj = DemoClass()
            myObj.nombre = i.nombre
            myObj.urlImage = i.urlImage

            myList.append(myObj)

        json_string = json.dumps(myList, default=Myclass)
        self.response.write(json_string)

class GetServicioHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'

        id_empresa = self.request.get('empresa')
        objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()
        strKey = objemp.key.urlsafe()
        myEmpKey = ndb.Key(urlsafe=strkey)
        myservicio = Servicio.query(Servicio.empresa_key == myEmpKey)

        myList = []
        for i in myservicio:
            myObj = DemoClass()
            myObj.nombre = i.nombre
            myObj.urlImage = i.urlImage

            myList.append(myObj)

        json_string = json.dumps(myList, default=Myclass)
        self.response.write(json_string)

class GetSponsorHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'

        id_empresa = self.request.get('empresa')
        objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()
        strKey = objemp.key.urlsafe()
        myEmpKey = ndb.Key(urlsafe=strkey)
        mysponsor = Sponsor.query(Sponsor.empresa_key == myEmpKey)

        myList = []
        for i in mysponsor:
            myObj = DemoClass()
            myObj.nombre = i.nombre
            myObj.urlImage = i.urlImage

            myList.append(myObj)

        json_string = json.dumps(myList, default=Myclass)
        self.response.write(json_string)

###########################################################################     


class UpHandler(webapp2.RequestHandler):
    def _get_urls_for(self, file_name):
        
     bucket_name = app_identity.get_default_gcs_bucket_name()
     path = os.path.join('/', bucket_name, file_name)
     real_path = '/gs' + path
     key = blobstore.create_gs_key(real_path)
     try:
      url = images.get_serving_url(key, size=0)
     except (images.TransformationError, images.NotImageError):
      url = "http://storage.googleapis.com{}".format(path)

     return url


    def post(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*')
     self.response.headers['Content-Type'] = 'application/json'

     bucket_name = app_identity.get_default_gcs_bucket_name()
     uploaded_file = self.request.POST.get('uploaded_file')
     file_name = getattr(uploaded_file, 'filename', None)
     file_content = getattr(uploaded_file, 'file', None)
     real_path = ''

     if file_name and file_content:
      content_t = mimetypes.guess_type(file_name)[0]
      real_path = os.path.join('/', bucket_name, file_name)

      with cloudstorage.open(real_path, 'w', content_type=content_t,
       options={'x-goog-acl': 'public-read'}) as f:
       f.write(file_content.read())

      key = self._get_urls_for(file_name)
      self.response.write(key)


class LoginHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('login.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)


class AdminHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('admin.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class GeneroHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('admin-genero.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class ArtistHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('admin-artist.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class ServicioHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('admin-servicio.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class SponsorHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('admin-sponsor.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class MainHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('index.html', template_context))


   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/admin', AdminHandler),
    ('/admin-artist', ArtistHandler),
    ('/admin-genero', GeneroHandler),
    ('/admin-servicio', ServicioHandler),
    ('/admin-sponsor', SponsorHandler),
    ('/up', UpHandler),
    ('/getteam', GetTeamHandler),
    ('/getartist', GetArtistHandler),
    ('/getgenero', GetGeneroHandler),
    ('/getservicio', GetServicioHandler),
    ('/getsponsor', GetSponsorHandler),
], debug = True)
