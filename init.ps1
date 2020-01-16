Write-Host "Installing dependencies:"
cd backend
Write-Host "    Backend:"
pipenv install
cd ..\frontend
Write-Host "    Frontend:"
npm install
cd ..
# Nginx throws an error if these 2 folders are not there
New-Item -ErrorAction SilentlyContinue -Name temp -ItemType directory
New-Item -ErrorAction SilentlyContinue -Name logs -ItemType directory
Write-Host "Done"
