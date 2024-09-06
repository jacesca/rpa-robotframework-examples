## Installing using GitHub
- Fork the project into your GitHub
- Clone it into your dektop
```
git clone https://github.com/jacesca/rpa-robotframework-examples.git
```
- Setup environment (it requires python3)
```
python -m venv venv
source venv/bin/activate  # for Unix-based system
venv\Scripts\activate  # for Windows
```
- Install requirements
```
pip install -r requirements.txt
```
- Required libraries (Review requirements.txt)
```
pip install pandas numpy
pip install jupyter
pip install scipy seaborn
pip instal python-dotenv scikit-learn
pip install robotframework   # To test installation you can put `robot --version` on the shell
pip install selenium
pip install --upgrade robotframework-seleniumlibrary
pip install webdrivermanager
pip install pyotp
pip install --upgrade robotframework-browser


Get-ExecutionPolicy         # To confirm current police
Set-ExecutionPolicy RemoteSigned
(Install nodejs and reboot)
rfbrowser clean-node
rfbrowser init
Set-ExecutionPolicy Default

pip install robotframework-requests
conda install conda-forge::rpaframework
```

