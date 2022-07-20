import csv
import logging

from flask import Flask, Response, redirect, render_template, request, url_for, flash
from flask import current_app as app
from flask_login import login_required

from .service import SlushpoolService


"""
    Empty placeholder just so the dummyservice/static folder can be wired up to retrieve its img
"""

logger = logging.getLogger(__name__)

slushpool_endpoint = SlushpoolService.blueprint



@slushpool_endpoint.route("/")
@login_required
def index():
    if app.specter.user_manager.get_user().has_service(SlushpoolService.id):
        return redirect(url_for(f"{SlushpoolService.get_blueprint_name()}.payouts"))

    return render_template(
        "slushpool/index.jinja",
    )


@slushpool_endpoint.route("/payouts", methods=["GET", "POST"])
@login_required
def payouts():
    return render_template(
        "slushpool/payouts.jinja",
        service=SlushpoolService,
        services=app.specter.service_manager.services,
    )


@slushpool_endpoint.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        csv_file = request.files["csv_file"]
        csv_data = csv_file.stream.read().decode("utf-8").splitlines()
        SlushpoolService.import_payout_history_csv(csv_data)

        return redirect(url_for(f"{SlushpoolService.get_blueprint_name()}.payouts"))

    return render_template(
        "slushpool/upload.jinja",
    )



@slushpool_endpoint.route("/settings", methods=["GET"])
@login_required
def settings():
    return render_template(
        "slushpool/settings.jinja",
    )



@slushpool_endpoint.route("/remove", methods=["POST"])
@login_required
def remove():
    SlushpoolService.clear_slushpool_data()
    return redirect("/")
