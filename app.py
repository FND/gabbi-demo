import json
import sys

from flask import Flask, render_template, url_for, jsonify, request, Response


app = Flask(__name__)


ARTICLES = [{
    "title": "Hello World",
    "content": "lorem ipsum dolor sit amet"
}]


@app.route("/")
def registry():
    resources = {
        "blog": { "href": url_for("blog") },
        "search": { "href": "/search" },
        "admin": { "href": "/admin" }
    }

    if request.headers.get("Accept") == "application/json-home":
        body = json.dumps({ "resources": resources })
        return Response(body, mimetype="application/json-home")

    resources = [(rel, resources[rel]) for rel in sorted(resources)]
    return render_template("registry.html", title="service registry", resources=resources)


@app.route("/blog", methods=["GET", "POST"])
def blog():
    if request.method == "POST":
        if request.headers.get("Content-Type") == "application/json":
            status = 201
            article = request.get_json()
        else:
            status = 302
            article = { name: value for name, value in request.form.items() }
        ARTICLES.append(article)

        res = Response(status=status)
        res.headers["Location"] = url_for("article", article_id=article["title"].lower())
        return res

    if request.headers.get("Accept") == "application/json":
        return jsonify({ "articles": ARTICLES })

    articles = [{
        "title": article["title"],
        "content": article["content"],
        "uri": url_for("article", article_id=article["title"].lower())
    } for article in ARTICLES]
    return render_template("blog.html", title="blog", articles=articles)


@app.route("/blog/<article_id>")
def article(article_id):
    article = next(entry for entry in ARTICLES if entry["title"].lower() == article_id)
    if request.headers.get("Accept") == "application/json":
        return jsonify(article)
    else:
        return render_template("article.html", title="article", article=article)


if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
        app.run(port=port)
    except IndexError: # assume dev mode
        app.run(debug=True)
