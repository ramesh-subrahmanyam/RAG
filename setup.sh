#!bash

# Install Python 3.10
sudo apt-get update
sudo apt-get install python3.10

# Set Python 3.10 as the default Python version
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Verify the Python version again
python --version

pip install langchain==0.1.0 openai==1.7.2 langchain-openai==0.0.2 langchain-community==0.0.12 langchainhub==0.1.14 chromadb==0.5.0
pip install python-dotenv
pip install --prefer-binary chromadb==0.5.0 --verbose

