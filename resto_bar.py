import cgi

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Place(db.Model):
  type = db.StringProperty()
  name = db.StringProperty()
  description = db.StringProperty(multiline=True)
  created_at = db.DateTimeProperty(auto_now_add=True)
  address = db.PostalAddressProperty()
  visit = db.BooleanProperty()
  location = db.GeoPtProperty() 

class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    
    if user:
      self.response.out.write("<html><body>")
      places = db.GqlQuery("SELECT * FROM Place ORDER BY created_at DESC")
      for place in places:
        self.response.out.write(place.type)
        self.response.out.write(": <br />")
        self.response.out.write(place.name)
        self.response.out.write("<br />")
        self.response.out.write(place.address)
        self.response.out.write("<br />")
      self.response.out.write("</body></html>")
    else:
      self.redirect(users.create_login_url(self.request.uri))

class CreatePlace(webapp.RequestHandler):
  def post(self):
    place = Place()
    place.name = self.request.get('name')
    place.type = self.request.get('place_type')
    place.description = self.request.get('description')
    place.address = self.request.get('address')
    if(self.request.get("visit") == "on"):
      place.visit = True
    else:
      place.visit = False
    place.put()
    self.redirect("/")

class NewPlace(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
      <html>
        <body>
          <form action="/place/create" method="post">
            <div>
            <label for="place_type">Type</label>
            <select name="place_type">
            <option value="restaurant">Restaurant</option>
            <option value="bar">Bar</option>
            </select>
            </div>
            <div>
            <label for="name">Nom</label>
            <input name="name">
            </div>
            <div>
            <label for="address">Adresse</label>
            <input name="address" size="50">
            </div>
            <div>
            <label for="visit">Visiter</label>
            <input name="visit" type="checkbox">
            </div>
            <div>
            <label for="description">Description</label><br />
            <textarea name="description" rows="3" cols="60"></textarea>
            </div>
            <div><input type="submit" value="Create"></div>
          </form>
        </body>
      </html>""")

    
application = webapp.WSGIApplication(
                                     [('/', MainPage), ("/place/new", NewPlace), ("/place/create", CreatePlace)],
                                     debug=True)
    
def main():
  run_wsgi_app(application)
     
if __name__ == "__main__":
   main()
