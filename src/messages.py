# Contains all the error and default messages for the System"

INVALIDAUTH = "Invalid Username and/or Authentication"
INVALIDJSON = "Invalid JSON format"
INVALIDCODE = "Invalid Python Code"

CONNERROR = "Connection Error, Terminating Connection"
SSLERROR = "SSL Connection Error"

STATE_START = "started"
STATE_RUNNING = "running"
STATE_FINISHED = "finished"
STATE_ERROR = "did not finish"

ERROR_NODB = "Database does not exist.\nPlease run with --dbadmin first"
ERROR_DBCORRUPT = "Database tables are corrupt.\nPlease recreate the database using --dbadmin"

DBA_WELCOME = "## PyServerless Database Admin Tool ##"
DBA_COMMANDS = "Select a Number:\n\t1 Add User\n\t2 Delete User\n\t3 Build Empty Database\n\tq Quit\n% "
DBA_NAME = "Enter Username: "
DBA_AUTH = "Enter AuthCode: "
DBA_ADDED = "Added: "
DBA_DELETED = "Deleted: "
DBA_INIT = "Empty database constructed"
DBA_INVALID = "Invalid Command"
