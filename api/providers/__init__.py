import importlib
import pkgutil
from abc import ABC

import flask

from providers.generics import GenericRegistration
from providers.generics.GenericClub import GenericClub
from providers.generics.GenericProvider import GenericProvider


class ProxyProvider(GenericProvider, ABC):
    @staticmethod
    def club(*args, **kwargs) -> GenericClub:
        return ProxyProvider.provider.club(*args, **kwargs)

    @staticmethod
    def register(*args, **kwargs) -> GenericRegistration:
        return ProxyProvider.provider.register(*args, **kwargs)

    @staticmethod
    def registration(*args, **kwargs) -> GenericRegistration:
        return ProxyProvider.provider.register(*args, **kwargs)

    provider: GenericProvider = None


provider = ProxyProvider


def ignore(prop=None):
    """
    Ignore this property but acknowledge it exists.
    :param prop:
    :return:
    """
    return True


def set_provider(prop):
    print("Set Provider")
    print(prop)
    ProxyProvider.provider = prop()
    print(provider)


def equals(value):
    def test(prop):
        if type(prop) == str:
            return prop == value
        return value in prop

    return test


def is_provider(prop):
    return issubclass(prop, GenericProvider)


def setup(app: flask.app):
    # Define functions that require access to app
    def call(prop):
        """
        Immediately call this property
        :param prop:
        :return:
        """
        prop(app)

    def do_after_request(fn):
        """
        :param fn: function to call after a request
        :return:
        """

        @app.after_request
        def wrapper(prop):
            fn()
            return prop

    # Define Constants

    # This constant provides the structure and available variables for provider module additionally it also provides
    # handlers for each variable.
    PROVIDER_METHOD_MAP = {
        "provider_id": ignore,
        "provider": set_provider,
        "before_request": app.before_request,
        "after_request": do_after_request,
        "init": call
    }
    # This constant provides a method of determining whether a provider is valid for the current context.
    PROVIDER_REQUIREMENT_MAP = {
        "provider_id": equals(app.config["PROVIDER"]),
        "provider": ignore
    }

    # Iterate through all sub-modules.
    for module in pkgutil.walk_packages(__path__):
        try:
            # Import the module
            temp = importlib.import_module("api.providers." + module.name)
            value_map = {}

            # Map the attributes the module to those in our Method map
            for attr in dir(temp):
                if attr in PROVIDER_METHOD_MAP:
                    value_map[attr] = temp.__dict__[attr]

            # Check that all the attributes in the requirement map exist and are valid.
            if all([k in value_map and PROVIDER_REQUIREMENT_MAP[k](value_map[k])
                    for k in PROVIDER_REQUIREMENT_MAP]):
                ProxyProvider.provider = value_map["provider"]
                # Call the relevant methods in the provider map
                for attr in value_map:
                    PROVIDER_METHOD_MAP[attr](value_map[attr])

                # exit this function as we now have our provider.
                return
        except ImportError as ix:
            print("Bad Module: {}".format(module.name))
            print(str(ix))
    if provider is None:
        raise RuntimeError("The provider name given did not match any provider modules.")
