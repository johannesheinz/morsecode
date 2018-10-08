#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
AUDIO="https://www.dropbox.com/s/hznoest3cxr42c5/audio.zip?dl=1"

# Go to main directory
cd $DIR

# Download additional audio files
wget $AUDIO -O audio.zip
unzip audio.zip
rm -rf audio.zip

# Create and activate virtual environment
python3 -m venv morsecode-env
source morsecode-env/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Print info
echo
echo
echo "Started a virtual Python 3 environment called 'morsecode-env'."
echo "You can start it by typing 'source morsecode-env/bin/activate'"
echo "You can stop it by simply typing 'deactivate'"

