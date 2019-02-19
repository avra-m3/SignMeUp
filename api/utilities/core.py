import os


class EnvironmentVariableMissing(RuntimeError):
    _message = """Could not run app, please define '{}' in your environment before continuing. 
    For more information please see README.md"""

    def __init__(self, variable):
        super().__init__(EnvironmentVariableMissing._message.format(variable))


class EnvVariable:
    key: str
    map_to: str
    required: bool

    def __init__(self, key, required=False, map_to=None, default=None):
        """
        This class is used to copy variables from the environment to flask config
        :param key: The name of the variable in the environment
        :param required: Is this variable required
        :param map_to: Should it be mapped to an alternative key
        """
        self.key = key
        self.required = required
        self.map_to = map_to or key
        self.default = default

        if self.required and key not in os.environ:
            raise EnvironmentVariableMissing(key)

    def copy(self, app):
        if self.key not in os.environ and not self.default:
            return
        app.config[self.map_to] = os.getenv(self.key, self.default)


def extract_environment_to_flask(app, variables: list):
    """
    Extract the environment into the flask config
    :param app: The flask app
    :param variables: A list of EnvVariable
    :return: None
    """
    for variable in variables:
        variable.copy(app)
