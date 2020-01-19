# Change the default behavior of CTRL-C so that the script can intercept and use it versus just terminating the script.
[Console]::TreatControlCAsInput = $True
# Sleep for 1 second and then flush the key buffer so any previously pressed keys are discarded and the loop can monitor for the use of
#   CTRL-C. The sleep command ensures the buffer flushes correctly.
Start-Sleep -Seconds 1
$Host.UI.RawUI.FlushInputBuffer()

$FlaskProcess = Start-Job -Name Backend  -ScriptBlock { cd "${using:PWD}\backend"; $env:FLASK_RUN_PORT=7507; pipenv run flask run }
$NodeProcess  = Start-Job -Name Frontend -ScriptBlock { cd "${using:PWD}\frontend"; $env:PORT=3000; npm run dev }
$NginxProcess = Start-Job -Name Nginx    -ScriptBlock { cd "${using:PWD}"; $env:PORT=80; nginx -c conf/nginx.conf }
Clear-Host
Get-Job

while ($true)
{
	Get-Job | Receive-Job
    if ($Host.UI.RawUI.KeyAvailable)
    {
		$key = $Host.UI.RawUI.ReadKey("AllowCtrlC, IncludeKeyDown, IncludeKeyUp")
		if($key.VirtualKeyCode -eq 67 -and $key.ControlKeyState -eq "LeftCtrlPressed")
		{
			Write-Host "Exiting gracefully..."
			nginx -s quit
			Remove-Job -Force $NginxProcess
			Remove-Job -Force $FlaskProcess
			Remove-Job -Force $NodeProcess
			break;
		}
    }
}
