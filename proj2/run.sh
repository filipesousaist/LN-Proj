#!/bin/bash

mkdir -p compiled images

for i in sources/*.txt tests/*.txt; do
	echo "Compiling: $i"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/$(basename $i ".txt").fst
done


fstconcat compiled/e.fst compiled/minutos.fst > compiled/e_minutos.fst
fstconcat compiled/horas.fst compiled/e_minutos.fst > compiled/text2num.fst

fstunion compiled/e_minutos.fst compiled/zeros.fst > compiled/lazy_end.fst
fstconcat compiled/horas.fst compiled/lazy_end.fst > compiled/lazy2num.fst

fstproject compiled/horas.fst > compiled/horas_acc.fst
fstproject compiled/e.fst > compiled/e_acc.fst
fstconcat compiled/horas_acc.fst compiled/e_acc.fst > compiled/horas_e_acc.fst
fstunion compiled/meias.fst compiled/quartos.fst > compiled/meias_ou_quartos.fst
fstconcat compiled/horas_e_acc.fst compiled/meias_ou_quartos.fst > compiled/rich2text.fst

fstcompose compiled/meias_ou_quartos.fst compiled/minutos.fst > compiled/meias_ou_quartos2num.fst
fstconcat compiled/e.fst compiled/meias_ou_quartos2num.fst > compiled/e_meias_ou_quartos2num.fst
fstunion compiled/lazy_end.fst compiled/e_meias_ou_quartos2num.fst > compiled/rich2num_end.fst
fstconcat compiled/horas.fst compiled/rich2num_end.fst > compiled/rich2num.fst

#fstcompose compiled/rich2text.fst compiled/text2num.fst > compiled/rich2text2num.fst
#fstunion compiled/rich2text2num.fst compiled/lazy2num.fst > compiled/rich2num.fst

fstinvert compiled/text2num.fst > compiled/num2text.fst

fstcompose compiled/sleepN_90714.fst compiled/num2text.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
fstcompose compiled/sleepT_90714.fst compiled/rich2num.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
fstcompose compiled/wakeupN_90714.fst compiled/num2text.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
fstcompose compiled/wakeupT_90714.fst compiled/rich2num.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

fstcompose compiled/sleepN_90762.fst compiled/num2text.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
fstcompose compiled/sleepT_90762.fst compiled/rich2num.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
fstcompose compiled/wakeupN_90762.fst compiled/num2text.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
fstcompose compiled/wakeupT_90762.fst compiled/rich2num.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt



for i in compiled/*.fst; do
	echo "Creating image: images/$(basename $i '.fst').pdf"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/$(basename $i '.fst').pdf
done

#echo "Testing the transducer 'converter' with the input 'tests/numero.txt'"
#fstcompose compiled/numero.fst compiled/converter.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
