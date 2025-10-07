from flask import Flask, render_template, request, send_file
import easyocr
from docx import Document
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/editar')
def editar():
    return render_template('editar_texto.html')

@app.route('/upload', methods=['POST'])
def extrair_texto():
    if 'imagem' not in request.files:
        return "Nenhuma imagem enviada", 400
    imagem = request.files['imagem']
    if imagem.filename == '':
        return "Nenhuma imagem selecionada", 400
    reader = easyocr.Reader(['en', 'pt'], gpu=False)
    result = reader.readtext(imagem.read())
    texto_extraido = ' '.join([res[1] for res in result])
    return render_template('editar_texto.html', texto=texto_extraido)

@app.route('/salvar', methods=['POST'])
def salvar():
    texto = request.form.get('texto', '')
    doc = Document()
    doc.add_paragraph(texto)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name='texto_extraido.docx',
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

if __name__ == '__main__':
    app.run(debug=True)