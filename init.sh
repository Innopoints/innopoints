echo "Installing dependencies:"
cd backend
echo "    Backend:"
pipenv install
cd ../frontend
echo "    Frontend:"
npm install
cd ..
echo "Done"
