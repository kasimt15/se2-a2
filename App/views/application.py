from flask import Blueprint, request, jsonify
from App.controllers.application import apply_to_job, get_applications_by_job, get_all_applications_json

application_views = Blueprint('application_views', __name__)

@application_views.route('/api/<int:job_id>/apply_to_job', methods=['POST'])
def apply_to_job_api(job_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID required'}), 400
    application = apply_to_job(user_id, job_id)
    return jsonify({'message': 'Applied to job', 'application_id': application.id}), 201

@application_views.route('/api/<int:job_id>/applications', methods=['GET'])
def get_applications_api(job_id):
    applications = get_all_applications_json(job_id)
    return jsonify(applications)