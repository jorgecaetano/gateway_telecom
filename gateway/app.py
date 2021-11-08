from gateway import create_app

"""
Módulo de inicialização da API
"""

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True, use_reloader=False)
