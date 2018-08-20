#!/bin/bash

install_all(){
for i in `seq 10`
do 
cp v$i/seq.c ./phylip-3.697/src
cd ./phylip-3.697/src
make -f Makefile.unx install
cd ../../
cp ./phylip-3.697/exe/dnapars ../exe/dnapars_v$i
done
}
install_one(){
cp v$1/seq.c ./phylip-3.697/src
cd ./phylip-3.697/src
make -f Makefile.unx install
cd ../../
cp ./phylip-3.697/exe/dnapars ../exe/dnapars_v$1
}
cd source/phylip-3.697/src
if [ "$#" == 0 ];then
	install_all	
else
	install_one $1
fi
