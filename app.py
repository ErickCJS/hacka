from flask import Flask, render_template, request

app = Flask(__name__, template_folder='app/templates')

@app.route('/')
def home():
    return "hombres trabajando"

@app.route('/denuncias', methods=['GET', 'POST'])
def denuncias():
    return render_template('contenido/denuncias.html')

if __name__ == '__main__':
    app.run(debug=True)
