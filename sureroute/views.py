from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from .layouts import Layouts
import colander
import deform

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    SureRoute,
    )


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'one': '', 'project': 'sureroute'}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_sureroute_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

class HomeView(Layouts):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(route_name='test', renderer='test.jinja2')
    def test_view(self):

        return {'hello':'test'}

class SureRouteView(Layouts):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(route_name='sureroute', renderer='templates/sureroute.jinja2')
    def list_view(self):
        sureroutes = DBSession.query(SureRoute).all()
        return {'sureroutes':sureroutes}

    @view_config(route_name='sureroute_results', renderer='templates/sureroute_results.jinja2')
    def list_view(self):
        sureroutes = DBSession.query(SureRoute).all()
        return {'sureroutes':sureroutes}

    @view_config(route_name='add_sureroute', renderer='templates/create_sureroute.jinja2')
    def new_view(self):
        class SureRouteSchema(colander.Schema):
            customer_name = colander.SchemaNode(colander.String(),
                                                description='Customer Name')
            hostname = colander.SchemaNode(colander.String(),
                                           description='Host Name')
            object_path = colander.SchemaNode(colander.String(),
                                              validator=colander.url,
                                              descripton='Object Path')
            email = colander.SchemaNode(colander.String(),
                                        validator=colander.Email(),
                                        description='Email ID for alerts')
        schema = SureRouteSchema()
        form = deform.Form(schema, buttons=('submit', ))
        if 'submit' in self.request.POST:
            controls = self.request.POST.items()
            try:
                form.validate(controls)
                post = self.request.POST
                sureroute = SureRoute(customer_name=post['customer_name'],hostname=post['hostname'],object_path=post['object_path'], email=post['email'])
                DBSession.add(sureroute)
                DBSession.flush()
                return HTTPFound(location=self.request.route_url('sureroute'))
            except deform.ValidationFailure:
                return {'form' : form}
        return {'form': form}

