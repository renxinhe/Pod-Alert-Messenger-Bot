import os

from flask import Flask, redirect, make_response, render_template, url_for, session, request, escape, flash

from model import make_new_alert, get_printer_raw, get_printer_json, get_all_printer_json

from app import app
app.secret_key = os.environ.get('SECRET_KEY') or 'hard to guess string'

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/new_alert', methods=['GET', 'POST'])
def new_alert():
    if request.method == 'POST':
        printer_json = get_printer_json(request.form['serial'])
        return str(printer_json)
    else:
        return redirect(url_for('dashboard'))

@app.route('/job_data')
def get_all_job_data():
    return str(get_all_printer_json())

@app.route('/job_data/<int:serial>')
def get_job_data(serial):
    printer_status = get_printer_raw(serial)
    if printer_status is None:
        return str({"code":"ENOTFOUND","errno":"ENOTFOUND","syscall":"getaddrinfo"})
    else:
        return str(printer_status)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
