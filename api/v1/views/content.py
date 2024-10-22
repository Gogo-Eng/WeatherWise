#!/usr/bin/env python3
"""A simple Flask app with user authentication features.
"""
from flask import abort, flash, Flask, jsonify, make_response, request, redirect, render_template, session, url_for
from api.v1.views import app_views  # type: ignore
from api.v1.auth.auth import Auth # type: ignore
from model.feedback import Feedback # type: ignore

AUTH = Auth()

@app_views.route('/feedback', methods=['GET', 'POST'], strict_slashes=False)
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback_text']
    
        try:
            feedback = AUTH.accept_feedback(feedback_text=feedback_text)
            return redirect(url_for('feedback'))  #'feedback.html', success='Email already registered')
        except ValueError as e:
            return str(e)
    
    return render_template('feedback.html')