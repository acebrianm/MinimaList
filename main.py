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

from models import Empresa, Team, Artist, Genero, Sponsor, Servicio

import cloudstorage
from google.appengine.api import app_identity
from google.appengine.api import taskqueue
from google.appengine.api import mail

jinja_env = jinja2.Environment(
 loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class DemoClass(object):
 pass

def MyClass(obj):
 return obj.__dict__

def send_approved_mail(sender_address, name, email, content):
    # [START send_message]
    message = mail.EmailMessage(
        sender=sender_address,
        subject="Message by " + name + " from " + email)

    message.to = "Alexandro Cebrian <alex.cebrianm@gmail.com>"
    message.body = content
    message.send()
    # [END send_message]


class SendMessageHandler(webapp2.RequestHandler):
    def get(self):
        #if not 'X-AppEngine-TaskName' in self.request.headers:
           #self.error(403)
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'

        name = self.request.get('name')
        email = self.request.get('email')
        content = self.request.get('message')
        print("NEPE: " + name+" "+email+" "+content)
        send_approved_mail("admin@minimalist-161601.appspotmail.com".format(app_identity.get_application_id()), name, email, content)
        #taskqueue.add(url='/sendmail',
                     #params={'name': name, 'email': email, 'content': content})
        self.response.write("TRUE")

class GetTotalCounts(webapp2.RequestHandler):

    def get(self):
        # if 'X-AppEngine-Cron' not in self.request.headers:
            # self.error(403)
        artists = Artist.query().fetch()
        myObj = DemoClass()
        myList = []

        myObj.artista = len(artists)
        myList.append(myObj)
        
        bucketName = app_identity.get_default_gcs_bucket_name()
        fileName = "/" + bucketName + "/somedir/somefile.txt"

        with cloudstorage.open(fileName, "w") as gcsFile:
            gcsFile.write("text")

        # json_string = json.dumps(myList, default=MyClass)
        # self.response.write(json_string)


class GetEmpresasHandler(webapp2.RequestHandler):

    def get(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*')
     self.response.headers['Content-Type'] = 'application/json'

     empresas = Empresa.query().fetch()

     myList = []
     for i in empresas:
      myObj = DemoClass()
      myObj.nombre = i.nombre_empresa
      myObj.codigo = i.codigo_empresa
      myObj.id_empresa = i.entityKey
      myObj.lat = i.lat
      myObj.lng = i.lng
      myList.append(myObj)
       
     json_string = json.dumps(myList, default=MyClass)
     self.response.write(json_string)

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

class GetEmpresaHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'

        id_empresa = self.request.get('empresa')
        emp_key = ndb.Key(urlsafe=id_empresa)
        objemp = emp_key.get()

        myList = []
        myObj = DemoClass()
        myObj.lat = objemp.lat
        myObj.lng = objemp.lng
        myList.append(myObj)
        
        json_string = json.dumps(myList, default=MyClass)
        self.response.write(json_string)

class GetArtistHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'

        id_empresa = self.request.get('empresa')
        emp_key = ndb.Key(urlsafe=id_empresa)
        objemp = emp_key.get()
        strKey = objemp.key.urlsafe() 
        myEmpKey = ndb.Key(urlsafe=strKey) 
        myartist = Artist.query(Artist.empresa_key == myEmpKey)

        myList = []
        for i in myartist:
            myObj = DemoClass()
            myObj.nombre = i.nombre
            myObj.urlImage = i.urlImage
            myObj.id_artist = i.entityKey
            myList.append(myObj)
        
        json_string = json.dumps(myList, default=MyClass)
        self.response.write(json_string)


class GetGeneroHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'

        id_empresa = self.request.get('empresa')
        emp_key = ndb.Key(urlsafe=id_empresa)
        objemp = emp_key.get()
        strKey = objemp.key.urlsafe() 
        myEmpKey = ndb.Key(urlsafe=strKey) 
        mygenero = Genero.query(Genero.empresa_key == myEmpKey)

        myList = []
        for i in mygenero:
            myObj = DemoClass()
            myObj.nombre = i.nombre
            myObj.urlImage = i.urlImage
            myObj.id_genero = i.entityKey
            myList.append(myObj)
        
        json_string = json.dumps(myList, default=MyClass)
        self.response.write(json_string)

class GetServicioHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'

        id_empresa = self.request.get('empresa')
        emp_key = ndb.Key(urlsafe=id_empresa)
        objemp = emp_key.get()
        strKey = objemp.key.urlsafe()
        myEmpKey = ndb.Key(urlsafe=strKey)
        myservicio = Servicio.query(Servicio.empresa_key == myEmpKey)

        myList = []
        for i in myservicio:
            myObj = DemoClass()
            myObj.nombre = i.nombre
            myObj.urlImage = i.urlImage
            myObj.id_servicio = i.entityKey
            myList.append(myObj)

        json_string = json.dumps(myList, default=MyClass)
        self.response.write(json_string)

class GetSponsorHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'

        id_empresa = self.request.get('empresa')
        emp_key = ndb.Key(urlsafe=id_empresa)
        objemp = emp_key.get()
        strKey = objemp.key.urlsafe()
        myEmpKey = ndb.Key(urlsafe=strKey)
        mysponsor = Sponsor.query(Sponsor.empresa_key == myEmpKey)

        myList = []
        for i in mysponsor:
            myObj = DemoClass()
            myObj.nombre = i.nombre
            myObj.urlImage = i.urlImage
            myObj.id_sponsor = i.entityKey
            myList.append(myObj)

        json_string = json.dumps(myList, default=MyClass)
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
      self._render_template('list-genero.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class GeneroEditHandler(webapp2.RequestHandler):

    def get(self):
        key = self.request.get('key')
        template_context = {}
        self.response.out.write(self._render_template('edit-genero.html', template_context))

    def _render_template(self, template_name, context=None):
        if context is None:
            context = {}

        template = jinja_env.get_template(template_name)
        return template.render(context)

class EmpresasHanlder(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('empresas.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class GeneroNewHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('new-genero.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class ArtistNewHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('admin-artist.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class ArtistHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('admin-artist2.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class ArtistEditHandler(webapp2.RequestHandler):

    def get(self):
        key = self.request.get('key')
        template_context = {}
        self.response.out.write(self._render_template('edit-artist.html', template_context))

    def _render_template(self, template_name, context=None):
        if context is None:
            context = {}

        template = jinja_env.get_template(template_name)
        return template.render(context)


class ServicioHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('list-service.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class ServicioEditHandler(webapp2.RequestHandler):

    def get(self):
        key = self.request.get('key')
        template_context = {}
        self.response.out.write(self._render_template('edit-service.html', template_context))

    def _render_template(self, template_name, context=None):
        if context is None:
            context = {}

        template = jinja_env.get_template(template_name)
        return template.render(context)

class ServicioNewHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('admin-service.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class SponsorHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('list-sponsor.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class SponsorEditHandler(webapp2.RequestHandler):

    def get(self):
        key = self.request.get('key')
        template_context = {}
        self.response.out.write(self._render_template('edit-sponsor.html', template_context))

    def _render_template(self, template_name, context=None):
        if context is None:
            context = {}

        template = jinja_env.get_template(template_name)
        return template.render(context)

class SponsorNewHandler(webapp2.RequestHandler):

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
    ('/edit-artist', ArtistEditHandler),
    ('/new-artist', ArtistNewHandler),
    ('/admin-genero', GeneroHandler),
    ('/new-genero', GeneroNewHandler),
    ('/edit-genero', GeneroEditHandler),
    ('/admin-service', ServicioHandler),
    ('/edit-service', ServicioEditHandler),
    ('/new-service', ServicioNewHandler),
    ('/admin-sponsor', SponsorHandler),
    ('/edit-sponsor', SponsorEditHandler),
    ('/new-sponsor', SponsorNewHandler),
    ('/empresas', EmpresasHanlder),
    ('/up', UpHandler),
    ('/getteam', GetTeamHandler),
    ('/getartist', GetArtistHandler),
    ('/getgenero', GetGeneroHandler),
    ('/getservice', GetServicioHandler),
    ('/getsponsor', GetSponsorHandler),
    ('/getempresas', GetEmpresasHandler),
    ('/getempresa', GetEmpresaHandler),
    ('/cron', GetTotalCounts),
    ('/sendmail', SendMessageHandler)
], debug = True)
