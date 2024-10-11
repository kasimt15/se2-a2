from falsk import Blueprint, request, jsonify
from App.controllers.application import apply_to_job, get_applications_by_job

application_views= Blueprint('application_views', __name__)

@application_views.route('/api/<int:job_id>/apply_to_job', methods= ['POST'])