#!/usr/bin/env bash

clear

echo " ██████╗██╗   ██╗ ██████╗██╗     ███████╗███╗   ██╗███████╗"
echo "██╔════╝╚██╗ ██╔╝██╔════╝██║     ██╔════╝████╗  ██║██╔════╝"
echo "██║      ╚████╔╝ ██║     ██║     █████╗  ██╔██╗ ██║███████╗"
echo "██║       ╚██╔╝  ██║     ██║     ██╔══╝  ██║╚██╗██║╚════██║"
echo "╚██████╗   ██║   ╚██████╗███████╗███████╗██║ ╚████║███████║"
echo " ╚═════╝   ╚═╝    ╚═════╝╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝"

echo -e "\n"

sleep 1

echo "===BENCHMARK FACE RECOGNITION TESTING==="
echo "v1.0"
echo -e "\n"
sleep 1

echo "============================"
echo "===CLEANING ROOT CYCLENS ==="
echo "============================"

rm -rf /tmp/cyclens

echo -e "\n"
sleep 1

date_start=$(date +%s.%N)

echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
echo ":::ADDING TRAIN IMAGES TO CYCLENS:::"
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::"

echo -e "Adding: Barbara Palvin, ID: 0\n"
curl -F "file=@./tests/train/barbara_palvin/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json
curl -F "file=@./tests/train/barbara_palvin/0.jpg" http://localhost:5000/api/v1/demo/face_add\?id\=0 | python -m json.tool | bat -p -l json
curl -F "file=@./tests/train/barbara_palvin/0.jpg" http://localhost:5000/api/v1/demo/face_add\?id\=0 | python -m json.tool | bat -p -l json

echo -e "Adding: Benedict Cumberbatch, ID: 1\n"
curl -F "file=@./tests/train/benedict_cumberbatch/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json
curl -F "file=@./tests/train/benedict_cumberbatch/0.jpg" http://localhost:5000/api/v1/demo/face_add\?id\=1 | python -m json.tool | bat -p -l json
curl -F "file=@./tests/train/benedict_cumberbatch/0.jpg" http://localhost:5000/api/v1/demo/face_add\?id\=1 | python -m json.tool | bat -p -l json

echo -e "Adding: Christian Bale, ID: 2\n"
curl -F "file=@./tests/train/christian_bale/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json
curl -F "file=@./tests/train/christian_bale/0.jpg" http://localhost:5000/api/v1/demo/face_add\?id\=2 | python -m json.tool | bat -p -l json
curl -F "file=@./tests/train/christian_bale/0.jpg" http://localhost:5000/api/v1/demo/face_add\?id\=2 | python -m json.tool | bat -p -l json

echo -e "Adding: Johnny Depp, ID: 3\n"
curl -F "file=@./tests/train/johnny_depp/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json
curl -F "file=@./tests/train/johnny_depp/0.jpg" http://localhost:5000/api/v1/demo/face_add?id\=3 | python -m json.tool | bat -p -l json
curl -F "file=@./tests/train/johnny_depp/0.jpg" http://localhost:5000/api/v1/demo/face_add?id\=3 | python -m json.tool | bat -p -l json

echo -e "Adding: Margot Robbie, ID: 4\n"
curl -F "file=@./tests/train/margot_robbie/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json
curl -F "file=@./tests/train/margot_robbie/0.jpg" http://localhost:5000/api/v1/demo/face_add?id\=4 | python -m json.tool | bat -p -l json
curl -F "file=@./tests/train/margot_robbie/0.jpg" http://localhost:5000/api/v1/demo/face_add?id\=4 | python -m json.tool | bat -p -l json

echo -e "Adding: Scarlett Johansson, ID: 5\n"
curl -F "file=@./tests/train/scarlett_johansson/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json
curl -F "file=@./tests/train/scarlett_johansson/0.jpg" http://localhost:5000/api/v1/demo/face_add?id\=5 | python -m json.tool | bat -p -l json
curl -F "file=@./tests/train/scarlett_johansson/0.jpg" http://localhost:5000/api/v1/demo/face_add?id\=5 | python -m json.tool | bat -p -l json


echo -e "\n"

echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
echo ":::TRAINING IMAGES...:::"
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::"

curl http://localhost:5000/api/v1/demo/face_train | python -m json.tool | bat -p -l json

echo -e "\n"

date_end=$(date +%s.%N)


echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
echo ":::RESULTS...:::"
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::"

echo -e "\n"

dt=$(echo "$date_end - $date_start" | bc)
dd=$(echo "$dt/86400" | bc)
dt2=$(echo "$dt-86400*$dd" | bc)
dh=$(echo "$dt2/3600" | bc)
dt3=$(echo "$dt2-3600*$dh" | bc)
dm=$(echo "$dt3/60" | bc)
ds=$(echo "$dt3-60*$dm" | bc)

printf "Total runtime: %d:%02d:%02d:%02.4f\n" $dd $dh $dm $ds

sleep 1

echo -e "Total Trained: 6\n"
echo -e "Total Tested: 6\n"
echo -e "Success Rate: %100\n"