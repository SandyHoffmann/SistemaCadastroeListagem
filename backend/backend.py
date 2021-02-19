from config import *

@app.route("/home")
def home():
    return('alo')

app.run(debug=True)
