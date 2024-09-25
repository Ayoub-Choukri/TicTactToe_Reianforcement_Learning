# Copy Policies directory into dist directory
cp -r ./Policies ./dist

cp -r ./Code/Policies ./dist

# Run the application main in the dist directory
cd dist
chmod +x main
./main
cd ..

