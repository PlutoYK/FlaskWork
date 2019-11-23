from app import app,db
from flask import render_template
# 错误处理
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('500.html'),500