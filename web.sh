#!/bin/sh

set -e

SERVER_NAME=$(curl ifconfig.me)
echo "from .prod import *\n\nALLOWED_HOSTS = [\n    '$SERVER_NAME',\n]\n\nDATABASES['default']['USER'] = 'shared_poem'\nDATABASES['default']['PASSWORD'] = 'shared_poem'" > $PWD/shared_poem/config/__init__.py

sudo cp $PWD/shared_poem/config/nginx.conf /etc/nginx/sites-enabled/shared_poem.nginx.conf

sudo ln -sf $PWD/shared_poem/config/supervisor.conf /etc/supervisor/conf.d/shared_poem.supervisor.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart shared_poem