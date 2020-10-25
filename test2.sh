python3 qc.py -coarse TRAIN2.txt DEV2-questions.txt > predicted-labels2.txt
python3 evaluate.py DEV2-labels.txt predicted-labels2.txt
python3 qc.py -fine TRAIN2.txt DEV2-questions.txt > predicted-labels2.txt
python3 evaluate.py DEV2-labels.txt predicted-labels2.txt