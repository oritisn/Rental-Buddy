"""https://pythonhosted.org/Flask-Uploads/"""
import os

from flask_uploads import UploadSet, configure_uploads

from app import basedir, app

leases = UploadSet('leases', extensions=('txt', 'pdf'))
UPLOAD_FOLDER = os.path.join(basedir, 'Upload')
app.config['UPLOADED_LEASES_DEST'] = UPLOAD_FOLDER
configure_uploads(app, leases)