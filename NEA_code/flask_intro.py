'''from flask import Flask, render_template

app = Flask(__name__)#refers to this file

@app.route("/")#allows us to return info for root page for local host
def index():
    #vari = "<h2>hello world</h2>"
    return render_template("bases.html")

@app.route("/<name>")
def user(name):
    return f"Hello {name}"

if __name__ == "__main__":
    app.run(debug=True)
'''
from yahoo_fin import stock_info
msft_price = stock_info.get_live_price('msft')
print(msft_price)
