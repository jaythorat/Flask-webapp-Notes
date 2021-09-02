# Importing Modules
from website import create_app

# Calling create_app() func. from  website/__init__.py 
app = create_app()

#Starting the server
if __name__ == '__main__':
    app.run(port=8000)



