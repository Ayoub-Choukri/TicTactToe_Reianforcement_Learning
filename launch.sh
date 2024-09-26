pip install -r  requirement.txt

TRAIN=1

if [ "$TRAIN" -eq 1 ]; then
    echo "Training the model"
    python Code/train.py
fi


if [ -d "dist" ] && [ -f "dist/main" ]; then
    echo "dist/main exists"
    cp -r ./Code/Policies ./dist/

else
    echo "dist/main does not exist"
    pyinstaller --onefile --distpath dist Code/main.py

    cp -r ./Code/Policies ./dist/
fi

# Run the application main in the dist directory
cd ./dist/
chmod +x main
./main
cd ..

