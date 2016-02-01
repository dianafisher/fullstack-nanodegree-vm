from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class EditForm(Form):
	itemName = StringField('Item Name', validators=[DataRequired()])

	def __init__(self, original_name, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.original_name = original_name

	def validate(self):
		return True