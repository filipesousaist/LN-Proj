python3 qc.py -coarse TRAIN.txt DEV-questions.txt > predicted-labels.txt
python3 evaluate.py DEV-labels.txt predicted-labels.txt
python3 qc.py -fine TRAIN.txt DEV-questions.txt > predicted-labels.txt
python3 evaluate.py DEV-labels.txt predicted-labels.txt