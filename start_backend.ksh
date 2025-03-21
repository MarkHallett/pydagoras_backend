#!/bin/bash

# start script for pydagoras back end
#

date
if pgrep -f /home/pydagoras/venv/bin/python > /dev/null; then
    echo "pydagroas back end is running"
else
    echo "Start pydagroas back end"
    cd ~pydagoras
    source venv/bin/activate
    cd pydagoras_backend/
    uvicorn main:app --ssl-keyfile /root/certs/www_pydagoras_com.key \
	             --ssl-certfile /root/certs/www_pydagoras_com.crt \
		     --host pydagoras.com
fi

