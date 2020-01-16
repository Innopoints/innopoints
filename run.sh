cd backend
FLASK_RUN_PORT=7507 flask run&
flask_pid=$!
cd ../frontend
PORT=3000 npm run dev&
node_pid=$!
cd ..
PORT=80 nginx -c conf/nginx.conf&
nginx_pid=$!

kill_processes() {
    printf "\rExiting\n"
	pkill -P $$
	exit
}

trap 'kill_processes' SIGINT

input="$@"
while true; do
    read input
done
