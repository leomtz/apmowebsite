Dev commands for Linux

export FLASK_APP=webpage.py
export FLASK_ENV=development
flask run

Dev commands for Windows

$env:FLASK_APP = "webpage.py"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"
python -m flask run