$FlaskProcess = Start-Job -Name Backend  -ScriptBlock { cd "${using:PWD}\backend"; $env:FLASK_RUN_PORT=7507; pipenv run flask run }
$NodeProcess  = Start-Job -Name Frontend -ScriptBlock { cd "${using:PWD}\frontend"; $env:PORT=3000; npm run dev }
$NginxProcess = Start-Job -Name Nginx    -ScriptBlock { cd "${using:PWD}"; $env:PORT=80; nginx -c conf/nginx.conf }
Clear-Host
Get-Job
# TODO: Catch CTRL+C to terminate subprocesses
# TODO: Create some interface to check the processes' outputs/statuses
#     with error reporting in the infinite loop
