"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template, flash, redirect
from models import db, connect_db, Cupcake
from forms import CupcakeForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:Kwok17273185@localhost:5432/cupcakes"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "oh-so-secret"


connect_db(app)


# Return an HTML page (via ***render_template***). This page should be entirely static (the route should just render the template, without providing any information on cupcakes in the database).
@app.route("/")
def index_page():
    """Renders html template that includes some JS - NOT PART OF JSON API!"""

    # Queries the database to retrieve all records from the `Cupcake` table.
    cupcakes = Cupcake.query.all()

    # Creates an instance of the `CupcakeForm` class.
    form = CupcakeForm()

    # Renders an HTML template and passes data to it.
    return render_template("index.html", cupcakes=cupcakes, form=form)


@app.route("/edit-cupcake/<int:id>")
def update_page(id):
    """Handles fetching a specific caupcake - NOT PART OF JSON API!"""

    # Retrieves a specific cupcake by its primary key (`id`)
    # If found, the cupcake record is returned,
    # else, Flask returns a 404 error page
    cupcake = Cupcake.query.get_or_404(id)

    # Creates an instance of the `CupcakeForm`, AND
    # Pre-populates its fields with the data from the retrieved `cupcake` object.
    form = CupcakeForm(obj=cupcake)

    # Renders the HTML template and passes cupcake object and the form instance to it.
    return render_template("edit-cupcake-form.html", cupcake=cupcake, form=form)


# ********************************
#  DEFINES API ENDPOINT
# ********************************


# Get data about all cupcakes. Returns a JSON response.
# The values comes from each cupcake instance.
# Decorator defines the route for the endpoint
@app.route("/api/cupcakes")
# Defines the function that will be called when the route is accessed.
def list_cupcakes():
    """Returns a list of all cupcakes as a JSON object"""

    # List comprehension that iterates over each `Cupcake object (`c`) in the list`.
    # For each cupcake, it calls the `serialize()` method,
    # converts the object into a dictionary that is JSON serializable.
    # The result is a list of dictionaries, each representing a cupcake.
    all_cupcakes = [c.serialize() for c in Cupcake.query.all()]

    # Converts `all_cupcakes` list into a JSON object.
    return jsonify(cupcakes=all_cupcakes)


# Get data about a single cupcake. Returns a JSON response.
# Raise a 404 if the cupcake cannot be found.
# Decorator defines the route for the endpoint
# <int:id> is a route parameter that allows you to pass an integer value to the function.
@app.route("/api/cupcakes/<int:id>")
# Defines the function that will be called when the route is accessed.
# Take the `id` parameter from the route.
def get_cupcake(id):

    # If a cupcake with the given `id` exists, return as a `Cupcake` object,
    # else, Flask auomatically returns a 404 error page.
    cupcake = Cupcake.query.get_or_404(id)

    # Converts the cupcake object into a dictionary
    # Converts the serialized cupcake dictionary into a JSON object
    # jsonify function ensures that the response is sent with content-type header(`application/json`)
    return jsonify(cupcake=cupcake.serialize())


# Add cupcake
# Decorator defines the route for the endpoint
@app.route("/api/cupcakes", methods=["POST"])
# Defines the function that will be executed when the route is accessed.
def create_cupcake():
    """Handle the creation of a new cupcake"""

    # Creates an instance of `CupcakeForm`
    # The form is populated with data from the POST request.
    form = CupcakeForm()

    # Check if the form data is valid and if the form was submitted.
    # Returns `True` if both conditions are met.
    if form.validate_on_submit():

        # Extract the submitted form data
        flavor = form.data["flavor"]
        size = form.data["size"]
        rating = form.data["rating"]
        image = form.data["image"]

        # Create a new `Cupcake` object with extracted form data.
        new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

        # Add to SQLAlchemy session
        db.session.add(new_cupcake)
        # Save the new cupcake to the database
        db.session.commit()

        # Flash message
        flash(f"Cupcake '{new_cupcake.flavor}' has been successfully added!")

        # Converts Python dictionaries into JSON strings
        # Creates a JSON object where the key is `cupcake` and the
        # value is the serialized cupcake dictionary returned by
        # `new_cupcake.serialize()`
        response_json = jsonify(cupcake=new_cupcake.serialize())

        # Return JSON response along with a status code of `201`
        return (response_json, 201)

    # Handling validation failure
    else:
        return "request failed"


# Update cupcake
# Decorator defines the route for the endpoint
@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
# Defines the function that will be executed when the route is accessed.
def update_cupcake(id):
    """Handle a particular cupcake update"""

    # If a cupcake with the given `id` exists, return the `Cupcake` object,
    # else, Flask automatically returns `404` error page.
    cupcake = Cupcake.query.get_or_404(id)

    # Creates an instance of the `CupcakeForm`
    # TODO(verify): the form is populated with data from PATCH request
    form = CupcakeForm()

    # Check if the form data is valid and if the form is submitted.
    if form.validate_on_submit():

        # Extract data from the from object
        cupcake.flavor = form.flavor.data
        cupcake.size = form.size.data
        cupcake.rating = form.rating.data
        cupcake.image = form.image.data
        db.session.commit()

        # Converts Python dictionaries into JSON strings
        return jsonify(cupcake=cupcake.serialize())
    else:
        return "request failed"


# Delete cupcak
# Decorator defines the route for the endpoint
@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
# Defines the function that will be executed when the route is accessed.
def delete_cupcake(id):
    """Deletes a particular cupcake"""

    # If a cupcake with the given `id` exists, return the `Cupcake` object,
    # else, Flask automatically returns `404` error page.
    cupcake = Cupcake.query.get_or_404(id)

    # Delete the cupcake
    db.session.delete(cupcake)

    # Save to database
    db.session.commit()

    # Converts Python dictionaries into JSON strings
    return jsonify(message="deleted")


# Search cupcake
# Decorator defines the route for the endpoint
@app.route("/api/cupcakes/search")
# Defines the function that will be executed when the route is accessed.
def search_cupcake():
    search_term = request.args.get("term")

    # Cupcake.flavor.ilike(...): SQLAlchemy method that generates a SQL ILIKE condition, which is a case-insensitive version of the LIKE operator. The ILIKE operator is used to match patterns in text data. The %{search_term}% is a wildcard pattern where % matches zero or more characters, meaning it will find any flavor containing the search_term anywhere in the text, regardless of case.
    # SELECT * FROM cupcakes WHERE flavor ILIKE '%search_term%';
    cupcakes = Cupcake.query.filter(Cupcake.flavor.ilike(f"%{search_term}%")).all()

    # Return a list of dictionaries that is JSON serialzable.
    cupcakes = [c.serialize() for c in cupcakes]

    # Converts Python dictionaries into JSON strings
    return jsonify(cupcakes=cupcakes)


""" 
form.flavor.data vs. form.data["flavor"]

 """
