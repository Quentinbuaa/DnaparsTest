#!/bin/bash

install_all(){
for i in `seq 11`
do
make -f Makefile.unx install CFLAGS=-FAULTY_V$i
cp ../exe/dnapars ../../../exe/dnapars_v$i
done
}
install_one(){
make -f Makefile.unx install CFLAGS=-FAULTY_V$1
cp ../exe/dnapars ../../../exe/dnapars_v$1
}
cd source/phylip-3.697/src
if [ "$#" == 0 ];then
	install_all	
else
	install_one $1
fi
