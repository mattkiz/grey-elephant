from wtforms import Form, StringField, DecimalField, validators, ValidationError
from wtforms.fields.html5 import EmailField
import decimal

def num_range(form, field, max=500.0, min=0.0):
    try:
        parsed_decimal = decimal.Decimal(field.data)
    except Exception as e:
        return ValidationError("Not a valid input")
    if max < parsed_decimal:
        return ValidationError("Enter number between ${0} and ${1}".format(min, max))
    if min > parsed_decimal:
        return ValidationError("Enter number between ${0} and ${1}".format(min, max))

class RecipientForm(Form):
    firstname = StringField("Recipient First Name",
                            validators=[validators.InputRequired()])
    lastname = StringField("Recipient Last Name",
                           validators=[validators.InputRequired()])
    email = EmailField("Recipient Email", validators=[validators.Email("Not valid email!"), validators.InputRequired()])
    instagram = StringField("Recipient Instagram Username")
    budget = DecimalField("How much would you like to spend on this gift?",
                          validators=[validators.InputRequired(), validators.NumberRange(min=0.0, max=500.0)])
