from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from src.edamam import get_recipes
import json
import src.spotify as spotify
import random

app = Flask(__name__)
Bootstrap(app)


@app.route('/', methods=['POST'])
def index_post():
    query = json.loads(get_recipes(request.form['query']))
    #return "<h1>{0}</h1>".format(query)
    #return render_template("results.html", image=query[0]['image'], url=query[0]['url'],
    #    label=query[0]['label'], mealType=query[0]['mealType'][0], cuisineType=query[0]['cuisineType'][0],
    #    calories=query[0]['calories'])

    elements = ""

    for i in range(0,len(query)):
        elements += '''<div class="container justify-content-center d-flex" style="padding: 3%">
        <div class="card border-primary mb-3" style="width: 75%;">
            <div class="card-body">
                <div class="row">
                    <div class="col-sm">
                        <img src="{image}" width="100%" height="100%" alt="{label}" style="border-radius: 50%;"/>
                    </div>
                    <div class="col-sm">
                        <div class="coll card text-white bg-primary mb-3" style="height: 100%">
                            <div class="card-header"><h1 style="font-size: 5em">{label}</h1></div>
                                <div class="card-body">
                                    <h4 class="card-title" style="font-size: 4em">meal: {mealType}</h4>
                                    <h4 class="card-title" style="font-size: 4em">cuisine: {cuisineType}</h4>
                                    <h4 class="card-title" style="font-size: 4em">calories: {calories}</h4>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>'''.format(image=query[i]['image'], url=query[i]['url'], label=query[i]['label'], mealType=query[i]['mealType'][0],
        cuisineType=query[i]['cuisineType'][0], calories=query[i]['calories'])

    return render_template("results.html", elements=elements)


@app.route('/')
def index_page():
    return render_template("home.html")


@app.route("/recipe")
def recipe_page():
    # Retrieve recipe from URL
    name = request.args.get("name")
    cuisines = request.args.get("cuisines").split(',')
    dishes = request.args.get("dishes").split(',')
    meals = request.args.get("meals").split(',')
    healths = request.args.get("healths").split(',')
    recipe = {
        "cuisines": cuisines,
        "meals": meals,
        "dishes": dishes,
        "healths": healths,
    }

    # Retrieve Spotify recommendations for recipe
    playlists = spotify.recommend(recipe)
    print(playlists)

    # Render template
    return render_template(
        "recipe.html",
        recipe_name=name,
        recipe_cuisines=cuisines,
        recipe_dishes=dishes,
        spotify_link=random.choice(playlists)["id"],
        recipe_link=request.args.get("recipe-link"),
        image_link=request.args.get("image-link"),
    )


if __name__ == '__main__':
    app.run(debug=True)