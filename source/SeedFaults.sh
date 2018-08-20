
insert_define(){
	echo "#define FAULTY_V$1" | cat - seq.c > temp && mv temp seq.c
}

for i in `seq 10`
do
	cp -rv faulty v$i
	cd v$i
	insert_define $i
	cd ..
done
