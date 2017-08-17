"""Extensions used by aliquis."""

from flask_ldap3_login import LDAP3LoginManager
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
ldap_manager = LDAP3LoginManager()