echo "" > time.txt
for i in `seq 1 10`;
do
	{ time python main.py $1; } 2>> time.txt
done

python mean_time.py time.txt
rm time.txt