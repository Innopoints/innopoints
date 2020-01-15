cd backend
FLASK_RUN_PORT=7507 flask run&
cd ../frontend
PORT=3000 npm run dev&
cd ..
PORT=80 nginx -c conf/nginx.conf&
# TODO: find a way to stop all at once
