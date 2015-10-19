import json

from flask import Flask, url_for, jsonify, request, Response


app = Flask(__name__)


ARTICLES = [{
    "title": "Hello World",
    "content": "lorem ipsum dolor sit amet"
}]


@app.route("/")
def registry():
    resources = {
        "blog": { "href": url_for("blog") },
        "admin": { "href": "/admin" }
    }
    body = json.dumps({ "resources": resources })
    return Response(body, mimetype="application/json-home")


@app.route("/blog", methods=["GET", "POST"])
def blog():
    if request.method == "POST":
        article = request.get_json()
        ARTICLES.append(article)

        res = Response(status=201)
        res.headers["Location"] = url_for("article", article_id=article["title"].lower())
        return res

    return jsonify({ "articles": ARTICLES })


@app.route("/blog/<article_id>")
def article(article_id):
    article = next(entry for entry in ARTICLES if entry["title"].lower() == article_id)
    return jsonify(article)


if __name__ == "__main__":
    app.run(debug=True)
