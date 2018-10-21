"""
This module implements the Provider framework for a mysql database.
"""
from providers.rdbms_provider.Model import setup, before_request, after_request
from providers.rdbms_provider.provider import DBProvider

provider_id = ["DB_LOCAL", "DB_REMOTE"]
provider = DBProvider
init = setup
before_request = before_request
after_request = after_request
