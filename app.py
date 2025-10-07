from flask import Flask, render_template, request
import easyocr

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/editar')
def editar():
    return render_template('editar_texto.html')

@app.route('/upload', methods=['POST'])
def extrair_texto():
    if 'image' not in request.files:
        return "Nenhuma imagem enviada", 400
    imagem = request.files['image']
    if imagem.filename == '':
        return "Nenhuma imagem selecionada", 400
    reader = easyocr.Reader(['en', 'pt'], gpu=False)
    result = reader.readtext(imagem.read())
    texto_extraido = ' '.join([res[1] for res in result])
    return render_template('editar_texto.html', texto=texto_extraido)

if __name__ == '__main__':
    app.run(debug=True)