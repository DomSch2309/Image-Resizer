import sys, os
from app import create_app

sys.path.append(os.path.dirname(__file__))
app = create_app()

if __name__=='__main__':
    app.run(debug = True, port = 5000)