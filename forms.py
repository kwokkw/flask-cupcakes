from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import Optional


class CupcakeForm(FlaskForm):
    """Form to add a cupcake"""

    flavor = StringField("Flavor")
    size = StringField("Size")
    rating = FloatField("Rating")
    image = StringField(
        "Image URL",
        default="https://thestayathomechef.com/wp-content/uploads/2017/12/Most-Amazing-Chocolate-Cupcakes-1-small.jpg",
    )
