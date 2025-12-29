#!/bin/bash
# start script for pydagoras back end

date
if pgrep -f /home/pydagoras/venv/bin/python > /dev/null; then
    echo "pydagroas back end is running"
    exit 0
fi

echo "Start pydagroas back end"
echo "ENV is set to ${ENV}"

if [ -z "${ENV}" ]; then
    echo "WARNING: ENV is unset or set to the empty string"
    exit 1 
fi

echo "start ${ENV} backend"
echo "  LOG_DIR = ${LOG_DIR}"
echo "  PYDAGORAS_V = ${PYDAGORAS_V}"
echo "  BACKEND_V = ${BACKEND_V}"

if [ ${ENV} = "PROD" ]; then
    source /root/lib/${PYDAGORAS_V}/bin/activate
    cd /root/backend/${BACKEND_V}/pydagoras_backend
    
    uvicorn main:app \
            --ssl-keyfile ${CERT_DIR}/www_pydagoras_com.key \
	        --ssl-certfile ${CERT_DIR}/www_pydagoras_com.crt \
		    --host pydagoras.com

elif [ ${ENV} = "DEV" ]; then
    source /Users/python/pydagoras/dev/lib/${PYDAGORAS_V}/bin/activate
    cd /Users/python/pydagoras/dev/backend/${BACKEND_V}/pydagoras_backend

    uvicorn main:app \
        --host 127.0.0.1 \
        --port 8000 \
        --reload
    
else
    echo "Unknown env ${ENV}" 
    exit 1 

fi
