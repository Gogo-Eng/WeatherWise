#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint  # type: ignore

app_views = Blueprint("app_views", __name__)

from api.v1.views.registration import *  # type: ignore
