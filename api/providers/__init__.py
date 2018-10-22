import os
from os.path import dirname

import flask
from Tools.scripts.make_ctype import method

from providers.generics.GenericProvider import GenericProvider

# Global variables within module scope
provider: GenericProvider = None


def ignore(prop=None):
    """
    Ignore this property but acknowledge it exists.
    :param prop:
    :return:
    """
    return True


def call(prop: method):
    """
    Immediately call this property
    :param prop:
    :return:
    """
    prop()


def set_provider(prop):
    global provider
    provider = prop()


def equals(value):
    def test(prop):
        if type(prop) == str:
            return prop == value
        return value in prop

    return test


def is_provider(prop):
    return issubclass(prop, GenericProvider)


def setup(app: flask.app):
    PROVIDER_METHOD_MAP = {
        "provider_id": ignore,
        "provider": set_provider,
        "before_request": app.before_request,
        "after_request": app.after_request,
        "init": call
    }

    PROVIDER_REQUIREMENT_MAP = {
        "provider_id": equals(app.config["PROVIDER"]),
        "provider": ignore
    }

    directory = dirname(__file__)

    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        if os.path.isdir(path):
            try:
                temp = __import__("api.providers." + file)

                value_map = {}

                # Map the attributes the module to those in our Method map
                for k in temp.__dict__:
                    if k in PROVIDER_METHOD_MAP:
                        value_map[k] = temp.__dict__[k]

                # Check that all the attributes in the requirement map exist and are valid.
                if all([k in value_map and PROVIDER_REQUIREMENT_MAP[k](value_map[k])
                        for k in PROVIDER_REQUIREMENT_MAP]):
                    # Call the relevant methods in the provider map
                    for k in value_map:
                        PROVIDER_METHOD_MAP[k](value_map[k])

                    # exit this function as we now have our provider.
                    return
            except (ImportError, ModuleNotFoundError) as ex:
                print("Bad module '{}'".format(path))
                print(ex)
    if provider is None:
        raise RuntimeError("The provider name given did not match any provider modules.")
