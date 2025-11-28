from app import app
# importer et enregistrer les routes du contrôleur
from controllers.api_route_alumnos import *
from controllers.api_route_profesores import *

if __name__ == '__main__':

    print("Launching Flask with SQLite database")
    app.run(host='0.0.0.0', port=5000, debug=False)