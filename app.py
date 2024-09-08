from flask import Flask, render_template, request
import re

app = Flask(__name__)

kode_provinsi = r'(11|12|13|14|15|16|17|18|19|21|31|32|33|34|35|36|51|52|53|61|62|63|64|65|71|72|73|74|75|76|81|82|91|92)'

kata_kasar_list = [
    'anjing', 'babi', 'kontol', 'pantek', 'jancok', 'jancuk', 'cok', 'goblok', 'brengsek', 'asu', 
    'sialan', 'bangsat', 'anjir', 'bajingan', 'celeng', 'tolol', 'kampret', 'tahi', 'tai', 'ngentot', 
    'santet', 'jalang', 'idiot', 'bodoh', 'anj', 'anjay', 'geblek', 'memek', 
    'pepek', 'puki', 'setan', 'asw', 'jablay', 'bangke', 'jangkrik', 'puqi', 'fuck', 'shit', 'bitch', 
    'asshole', 'cunt', 'dick', 'piss', 'motherfucker', 'slut', 'whore', 'twat', 'faggot', 'cock', 
    'prick', 'pussy', 'bastard', 'douchebag', 'ass', 'wanker'
]

kata_kasar_pattern = r'\b(' + '|'.join([re.escape(kata) for kata in kata_kasar_list]) + r')\b'

kata_kasar_pattern += r'|' + '|'.join([rf'({re.escape(kata)}){{2,}}' for kata in kata_kasar_list])

pola = {
    'nik': rf'{kode_provinsi}\d{{6}}[01]\d{{7}}',  # NIK
    'email': r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',  # Email
    'link': r'\b(?:https?://|www\.)?[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+[^\s]*\b',  # Link
    'kata_kasar': kata_kasar_pattern  # Kata kasar
}

def sensor_data_pribadi(text, pilihan_tipe):
    hasil = text
    for tipe in pilihan_tipe:
        if tipe in pola:
            hasil = re.sub(pola[tipe], lambda x: '*' * len(x.group()), hasil, flags=re.IGNORECASE)
    return hasil

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/masking', methods=['GET', 'POST'])
def masking():
    output = ''
    if request.method == 'POST':
        text_input = request.form.get('text_input', '')
        masking_options = request.form.getlist('masking_option')
        output = sensor_data_pribadi(text_input, masking_options)
    return render_template('masking.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
