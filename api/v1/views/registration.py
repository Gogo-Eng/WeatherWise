#!/usr/bin/env python3
"""A simple Flask app with user authentication features.
"""
from flask import abort, Flask, jsonify, make_response, request, redirect, render_template, url_for
from api.v1.views import app_views  # type: ignore
from api.v1.auth.auth import Auth # type: ignore

AUTH = Auth() 

@app_views.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    """ handles credentials """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            registered_user = AUTH.register_user(email, password)
            return redirect(url_for('app_views.login'))
        except Exception:
            return render_template('signup.html', error='Email already registered')
    
    return render_template('signup.html')


@app_views.route('/sessions', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """ handles login credentials """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            response = make_response(redirect(url_for('home')))  #redirect(url_for('app_views.home'))
            response.set_cookie("session_id", session_id)
            return response
        else:
            return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')


@app_views.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ handles session deletion """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app_views.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """profile route"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app_views.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ returns a token that allows passwd reset """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except Exception:
        abort(403)


@app_views.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ updates a user's password """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        updated_password = AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)
