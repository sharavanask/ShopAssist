from flask import Flask, render_template, request
import asyncio
from mcp.server.fastmcp import FastMCP
import httpx
import os 
port=os.getenv("PORT")

# Import your MCP tools
from server.mcp import getproduct, gettop3  # Adjust import based on your actual filename

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    product_summary = ""
    if request.method == "POST":
        prod = request.form["prod"]
        minp = float(request.form["minp"])
        maxp = float(request.form["maxp"])
        specific_features = request.form["specific_features"]

        # Run the async MCP tool in a sync Flask route
        product_summary = asyncio.run(getproduct(prod, specific_features, 1, maxp))

    return render_template("index.html", product_summary=product_summary)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=port)