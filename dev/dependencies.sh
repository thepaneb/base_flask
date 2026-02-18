pip install --upgrade pip
pip list -o | cut -f1 -d' ' | tr " " "\n" | awk '{if(NR>=3)print}' | cut -d' ' -f1 | xargs -n1 pip install -U
pip install -r app/requirements.txt --upgrade --upgrade-strategy eager