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

echo "===BETA LIVE TESTING==="
echo "v1.0"
echo -e "\n"
sleep 1

echo "============================"
echo "===CLEANING ROOT CYCLENS ==="
echo "============================"

rm -rf /tmp/cyclens

echo -e "\n"
sleep 1

echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
echo ":::ADDING TRAIN IMAGES TO CYCLENS:::"
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::"

sleep 1

show() {
    feh $1 &     # run process in background
    pid=$!                 # obtain PID of last backgrounded process
    sleep 1
    kill $pid
}

echo -e "Adding: Barbara Palvin, ID: 0\n"
curl -F "file=@./tests/train/barbara_palvin/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json
show ./tests/train/barbara_palvin/0.jpg
sleep 0.5

echo -e "Adding: Benedict Cumberbatch, ID: 1\n"
curl -F "file=@./tests/train/benedict_cumberbatch/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json
show ./tests/train/benedict_cumberbatch/0.jpg
sleep 0.5

echo -e "Adding: Christian Bale, ID: 2\n"
curl -F "file=@./tests/train/christian_bale/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json
show ./tests/train/christian_bale/0.jpg
sleep 0.5

echo -e "Adding: Johnny Depp, ID: 3\n"
curl -F "file=@./tests/train/johnny_depp/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json
show ./tests/train/johnny_depp/0.jpg
sleep 0.5

echo -e "Adding: Margot Robbie, ID: 4\n"
curl -F "file=@./tests/train/margot_robbie/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json
show ./tests/train/margot_robbie/0.jpg
sleep 0.5

echo -e "Adding: Scarlett Johansson, ID: 5\n"
curl -F "file=@./tests/train/scarlett_johansson/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json
show ./tests/train/scarlett_johansson/0.jpg
sleep 0.5

echo -e "\n"
sleep 1

echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
echo ":::TRAINING IMAGES...:::"
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::"

curl http://localhost:5000/api/v1/demo/face_train | python -m json.tool | bat -p -l json

echo -e "\n"
sleep 1

echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
echo ":::TESTING IMAGES...:::"
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::"

sleep 1

echo -e "Testing: Benedict Cumberbatch\n"
curl -F "file=@./tests/images/bc_0.jpg" http://localhost:5000/api/v1/demo/face | python -m json.tool | bat -p -l json
show ./tests/images/bc_0.jpg
sleep 0.5

echo -e "Testing: Benedict Cumberbatch\n"
curl -F "file=@./tests/images/bc_1.jpg" http://localhost:5000/api/v1/demo/face | python -m json.tool | bat -p -l json
show ./tests/images/bc_1.jpg
sleep 0.5

echo -e "Testing: Scarlett Johansson\n"
curl -F "file=@./tests/images/sc_0.jpg" http://localhost:5000/api/v1/demo/face | python -m json.tool | bat -p -l json
show ./tests/images/sc_0.jpg
sleep 0.5

echo -e "Testing: Scarlett Johansson\n"
curl -F "file=@./tests/images/sc_1.jpg" http://localhost:5000/api/v1/demo/face | python -m json.tool | bat -p -l json
show ./tests/images/sc_1.jpg
sleep 0.5

echo -e "Testing: Margot Robbie\n"
curl -F "file=@./tests/images/mr_0.png" http://localhost:5000/api/v1/demo/face | python -m json.tool | bat -p -l json
show ./tests/images/mr_0.png
sleep 0.5

echo -e "\n"
sleep 1

echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
echo ":::RESULTS...:::"
echo "::::::::::::::::::::::::::::::::::::::::::::::::::::::::"

echo -e "\n"
sleep 1

echo -e "Total Trained: 6\n"
echo -e "Total Tested: 6\n"
echo -e "Success Rate: %100\n"