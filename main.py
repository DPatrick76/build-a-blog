import os
import webapp2
import jinja2

from google.appengine.ext import db  #code for Googel App Engine Database

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)  # write calls write to not have to type all the time

    def render_str(self, template, **params):  #takes a Template name and returns a string of renderd template
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))  #calls write on the string prints the template
#Code to store in Database
class BlogData(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):  #mapped to slash and writes ASCII Chan to browser
    #def render_front(self, title="", body="", error=""):  #taking variables and passing to template
        #blog_posts = db.GqlQuery("SELECT * FROM BlogData ORDER BY created DESC LIMIT 5")
        #self.render("front.html", title=title, body=body, error=error, blog_posts = blog_posts)

    def get(self):
        self.render("newpost.html") #draws the blank form

    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")

        if title and body:
            #create new BlogData stored in variable b
            b = BlogData(title = title, body = body)
            #input into the database
            b.put()
            self.redirect("/blog/"+str(b.key().id()))
        else:
            error = "We need a title and a body!"
            self.render("newpost.html",title=title, body=body, error=error) #renders form with error message

class Blog(Handler):
    """Handles requests coming into '/blog'
        #e.g. build-a-blog/blog"""
    def render_blogPosts(self, title="", body="", error=""):
        blog_posts = db.GqlQuery("SELECT * FROM BlogData ORDER BY created DESC LIMIT 5")
        self.render("blog.html",title=title, body=body,error=error, blog_posts= blog_posts)

    def get(self):
        self.render_blogPosts()

    def post(self):
        a = BlogData(title = title, body = body)
        b.put()

class ViewPostHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self,template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def get(self,id):
        id = int(id)
        blogEntry = BlogData.get_by_id(id)
        title = BlogData.title
        body = BlogData.body
        blogEntry = [blogEntry]

        if blogEntry:
            self.render("blog.html", title=title, body=body, blog_posts = blogEntry, oneEntry=True)
        else:
            self.response.write("Not working homie.")

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', MainPage),
    ('/blog', Blog),
    webapp2.Route('/blog/<id:\d+>',ViewPostHandler)
], debug=True)
