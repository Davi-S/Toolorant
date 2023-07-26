import wtforms as wtf
import flask_wtf as fwtf
from . import game_resources as gr

########## BLACK MAGIC ZONE ##########
# This metaclass creates the map-agent fields as class attributes dynamically from the dataclasses.
# This is not needed if the form worked with instance attributes. This is only needed because of the CLASS attributes
# https://chat.openai.com/share/3e7fe2d6-4527-4f76-8806-f4f3f3cefc76
class M_MapAgentField(type(fwtf.FlaskForm), type):
    def __new__(cls, name, bases, attrs):
        map_agent_attrs = {}
        for map_enum in gr.Map:
            field = wtf.SelectField(map_enum.name.title(),
                                    choices=['None'] + [agent.name.title()
                                                        for agent in gr.Agent],
                                    validators=[wtf.validators.Optional()])
            map_agent_attrs[map_enum.name.lower()] = field
        return super().__new__(cls, name, bases, attrs | map_agent_attrs)


class NewProfileInfo(fwtf.FlaskForm, metaclass=M_MapAgentField):
    # Attention to the MapAgentField metaclass: it adds more fields to the form class
    name = wtf.StringField('Name: ', validators=[wtf.validators.DataRequired()])
    game_mode = wtf.SelectField('Game Mode',
                                choices=[mode.name.replace('_', ' ').title()
                                         for mode in gr.GameMode],
                                validators=[wtf.validators.DataRequired()])
######################################