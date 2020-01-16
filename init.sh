echo "Installing dependencies:"
cd backend
echo "    Backend:"
pipenv install
cd ../frontend
echo "    Frontend:"
npm install
cd ..
# Nginx throws an error without these 2 folders on Windows. Not sure about Unix
mkdir temp logs
echo "Done"
