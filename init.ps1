Write-Host "Installing dependencies:"
cd backend
Write-Host "    Backend:"
pipenv install
cd ..\frontend
Write-Host "    Frontend:"
npm install
cd ..
Write-Host "Done"
