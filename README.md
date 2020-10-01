# Steganography-Tool

## About
This tool allows the users to save sensitive information securely. The tool combines encryption with steganography. The user provides an image and a text file (data to be secured). \
The data is encrypted using state of the art methods. Then the cipher text is stored in the image provided by the user. It is impossible to differentiate between the input image and the output image.

## Encryption Steps
 - A secure key is generated from the user password and a salt using PBKDF2.
 - Then the data is encrypted using AES-CBC.
 - The cipher text is hashed with SHA256.
 - Then a token is generated using AES-CBC (with different key) to ensure data integrity.
 - Finally, token and cipher are concatenated and the resultant string is embedded in the image file provided by the user.

## Using the tool
Clone the repo
```
git clone https://github.com/bhagwatgarg/steganography-tool
cd Steganography-Tool
```
Install required dependencies and run the tool.
```
pip install -r requirements.txt
python app.py
```

## Tip
You can change the default salt in [encryption.py](https://github.com/bhagwatgarg/Steganography-Tool/blob/master/encryption.py).