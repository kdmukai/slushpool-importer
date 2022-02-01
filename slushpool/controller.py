import logging
from flask import Flask, Response, redirect, render_template, request, url_for, flash
from flask_login import login_required

from cryptoadvance.specter.services.controller import user_secret_decrypted_required
from .service import SlushpoolService


"""
    Empty placeholder just so the dummyservice/static folder can be wired up to retrieve its img
"""

logger = logging.getLogger(__name__)

slushpool_endpoint = SlushpoolService.blueprint


@slushpool_endpoint.route("/")
@login_required
@user_secret_decrypted_required
def index():
    return render_template(
        "slushpool/index.jinja",
    )
