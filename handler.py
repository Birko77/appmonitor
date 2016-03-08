import webapp2
import jinja2
import os
import logging


# Create an instance of the Jinja2.environment class to
# load the templates from the filesystem.
# Use the Jinja2 builtin FileSystemLoader().
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                       autoescape = True)


# The following Handler-class will be inherited 
# by every request handler class.

class Handler(webapp2.RequestHandler):

# --- RENDERING ---

    def write(self, *a, **kw):
        '''Write to the body fo the response-object

        Arguments:
        *a, **kw -- here the response body created by render_str()
        '''
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        '''Render a template with the given parameters

        Load the template by calling the get_template() method
        Render the template by calling the render() method and passing
        the params to it.
        Arguments:
        template -- the name of the template-file
        **params -- the variables to be passed to the renderer
        Return value:
        the redered template
        '''
        template_params = params
        t = jinja_environment.get_template(template)
        return t.render(template_params)

    def render(self, template, **kw):
        '''Create a response-body 

        Render a given template and write the result to the 
        response body.
        Arguments:
        template -- name of the template-file
        **kw -- the variables to be passed to the renderer
        '''
        self.write(self.render_str(template, **kw))




#--- EXCEPTIONS ---

    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            webapp2.RequestHandler.handle_exception(self, exception, debug_mode)
        else:
            logging.exception(exception)
            self.error(500)
            self.render('error.html')


