from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect("printer.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feil (
        rom TEXT NOT NULL,
        printer_id TEXT NOT NULL,
        feilmelding TEXT NOT NULL
    )
    ''')

    if request.method == "POST":
        rom = request.form["rom"].strip()
        printer_id = request.form["printer_id"].strip()
        feilmelding = request.form["feilmelding"].strip()
        if rom and printer_id and feilmelding:
            cursor.execute("INSERT INTO feil (rom, printer_id, feilmelding) VALUES (?, ?, ?)", (rom, printer_id, feilmelding))
            conn.commit()

    cursor.execute("SELECT rom, printer_id, feilmelding FROM feil")
    feil = cursor.fetchall()
    conn.close()

    return render_template_string('''
    <html>
    <head>
        <title>Printer Feilmeldinger</title>
        <style>
            body { font-family: Arial; background-color: #f9f9f9; padding: 20px; }
            h2, h3 { color: #444; }
            form, li { background-color: #fff; padding: 15px; border-radius: 6px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            input[type="text"], textarea { width: 100%; padding: 8px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; }
            input[type="submit"] { background-color: #007BFF; color: white; padding: 10px; border: none; border-radius: 4px; cursor: pointer; }
            input[type="submit"]:hover { background-color: #0056b3; }
        </style>
    </head>
    <body>
        <h2>Logg en printerfeil</h2>
        <form method="POST">
            Rom: <input type="text" name="rom" required><br>
            Printer-ID: <input type="text" name="printer_id" required><br>
            Feilmelding:<br>
            <textarea name="feilmelding" rows="4" placeholder="Hva er problemet?" required></textarea><br>
            <input type="submit" value="Send inn">
        </form>
        <h3>Innsendte meldinger:</h3>
        <ul>
            {% for rom, printer_id, feilmelding in feil %}
                <li><strong>{{ rom }}</strong> – {{ printer_id }} – {{ feilmelding }}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
    ''', feil=feil)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
