for i1 in {4..8}
do
    for i2 in {4..8}
    do
        for i3 in {4..8}
        do
            echo ${i1} ${i2} ${i3}
            python3 qc.py -coarse TRAIN.txt DEV-questions.txt ${i1} ${i2} ${i3} > predicted-labels.txt
            python3 evaluate.py DEV-labels.txt predicted-labels.txt
            python3 qc.py -fine TRAIN.txt DEV-questions.txt ${i1} ${i2} ${i3} > predicted-labels.txt
            python3 evaluate.py DEV-labels.txt predicted-labels.txt
        done
    done
done