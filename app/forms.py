from flask.ext.wtf import Form
from wtforms.fields import TextField, BooleanField
from wtforms.validators import Required
class FormOne(Form):
    area_list=['appendectomy','asthma','pneumonia','seizure']
    severity_list=['minor','moderate','major']

class FormThree(Form):
    interval_from=TextField(label="from",default="1.0", validators=[Required()])
    interval_to=TextField(label="to", default="2.0", validators=[Required()])
    interval_min=TextField(label="Min", default="2", validators=[Required()])
    orderset_from=TextField(label="from",default="1.0", validators=[Required()])
    orderset_to=TextField(label="to", default="2.0", validators=[Required()])
