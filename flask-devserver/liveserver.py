from livereload import Server

def serve(app):
    app.debug = True
    server = Server(app.wsgi_app)
    server.serve()
