import datetime
import os
from anchor_pki.acme import Manager

manager = Manager(
    directory_url=os.getenv('ACME_DIRECTORY_URL'),

    eab_kid=os.getenv('ACME_KID'),
    eab_hmac_key=os.getenv('ACME_HMAC_KEY'),

    server_names=os.getenv('SERVER_NAMES').split(','),
    renew_in=datetime.timedelta(hours=336))

certfile = manager.certfile()
keyfile  = manager.keyfile()

ssl_context = manager.ssl_context()