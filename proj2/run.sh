#!/bin/bash

mkdir -p compiled images

for i in sources/*.txt tests/*.txt; do
	echo "Compiling: $i"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/$(basename $i ".txt").fst
done

# text2num
fstconcat compiled/e.fst compiled/minutos.fst > compiled/e_minutos.fst
fstconcat compiled/horas.fst compiled/e_minutos.fst > compiled/text2num.fst

# lazy2num
fstunion compiled/e_minutos.fst compiled/zeros.fst > compiled/lazy_end.fst
fstconcat compiled/horas.fst compiled/lazy_end.fst > compiled/lazy2num.fst

# rich2text
fstproject compiled/horas.fst > compiled/horas_acc.fst
fstproject compiled/e.fst > compiled/e_acc.fst
fstconcat compiled/horas_acc.fst compiled/e_acc.fst > compiled/horas_e_acc.fst
fstunion compiled/meias.fst compiled/quartos.fst > compiled/meias_ou_quartos.fst
fstconcat compiled/horas_e_acc.fst compiled/meias_ou_quartos.fst > compiled/rich2text.fst

# rich2num
fstcompose compiled/rich2text.fst compiled/text2num.fst > compiled/rich2text2num.fst
fstunion compiled/rich2text2num.fst compiled/lazy2num.fst > compiled/rich2num.fst

# num2text
fstinvert compiled/text2num.fst > compiled/num2text.fst

fstcompose compiled/sleepA_90714.fst compiled/num2text.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort > compiled/sleepC_90714.fst
fstcompose compiled/sleepB_90714.fst compiled/rich2num.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort > compiled/sleepD_90714.fst
fstcompose compiled/wakeupA_90714.fst compiled/num2text.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort > compiled/wakeupC_90714.fst
fstcompose compiled/wakeupB_90714.fst compiled/rich2num.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort > compiled/wakeupD_90714.fst

fstcompose compiled/sleepA_90762.fst compiled/num2text.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort > compiled/sleepC_90762.fst
fstcompose compiled/sleepB_90762.fst compiled/rich2num.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort > compiled/sleepD_90762.fst
fstcompose compiled/wakeupA_90762.fst compiled/num2text.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort > compiled/wakeupC_90762.fst
fstcompose compiled/wakeupB_90762.fst compiled/rich2num.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort > compiled/wakeupD_90762.fst

for i in compiled/*.fst; do
	echo "Creating image: images/$(basename $i '.fst').pdf"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/$(basename $i '.fst').pdf
done

#echo "Testing the transducer 'converter' with the input 'tests/numero.txt'"
#fstcompose compiled/numero.fst compiled/converter.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
