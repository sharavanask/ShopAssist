from flask import Flask, redirect

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return redirect("https://my-streamlit-app.streamlit.app", code=302)

if __name__ == "__main__":
    app.run()
