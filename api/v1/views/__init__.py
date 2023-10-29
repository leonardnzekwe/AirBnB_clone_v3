#!/usr/bin/python3
"""Init File"""
from flask import Blueprint

# Create a Blueprint instance with a URL prefix of '/api/v1'
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import of everything in the package api.v1.views
from api.v1.views.index import *
