from flask_restful import Api

from bapi import app
from bapi.config import config
from bapi.routes import routes

api = Api(app)
app.config.from_object(config['development'])
routes(api)


if (__name__) == '__main__':
    app.run(debug=True)
