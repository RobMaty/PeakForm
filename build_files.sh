python3 -m pip install -r requirements.txt --target /tmp/packages
export PYTHONPATH=/tmp/packages:$PYTHONPATH
python3 manage.py collectstatic --noinput
python3 manage.py migrate --noinput
