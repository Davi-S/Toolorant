import wtforms as wtf
import flask_wtf as fwtf
from . import game_resources as gr

# TODO: Add function to format the fields (make upper case, titled, remove underscores, etc) instead of formation on the creation. Its not necessary to make this function part of the form, if it is needed in other places, it can be part of a formatting class or other similar package
##### BLACK MAGIC ZONE #####
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
    name = wtf.StringField('Name: ', validators=[wtf.validators.DataRequired()])
    game_mode = wtf.SelectField('Game Mode',
                                choices=[mode.name.replace('_', ' ').title()
                                         for mode in gr.GameMode],
                                validators=[wtf.validators.DataRequired()])
############################


class SelectProfiles(fwtf.FlaskForm):
    profile_name = wtf.RadioField('Profile name', choices=[],
                                  validators=[wtf.validators.DataRequired()])
    set = wtf.SubmitField('Select')
    delete = wtf.SubmitField('Delete')

    def __init__(self, profile_names: list[str], default: int | None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile_name.choices = profile_names
        self.profile_name.default = default if default is None else profile_names[default]
        # ATTENTION: After setting a default value on for the RadioField in the __init__ method, the form needs to be processed again
        # `self.process` should not be called here because it affects the result of the `validate_on_submit`, so it (process) must be called after the `validate_on_submit`.
