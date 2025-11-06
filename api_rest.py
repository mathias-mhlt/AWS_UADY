from app import app
# importer et enregistrer les routes du contrôleur
from controllers.api_route_alumnos import *
from controllers.api_route_profesores import *

if __name__ == '__main__':
    app.run(debug=True)
