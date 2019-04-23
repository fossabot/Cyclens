#!/usr/bin/env bash

clear

echo "===LIVE TESTING==="
echo "STABLE: v1.0"
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

curl -F "file=@./tests/train/barbara_palvin/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json
curl -F "file=@./tests/train/benedict_cumberbatch/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json
curl -F "file=@./tests/train/christian_bale/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json
curl -F "file=@./tests/train/johnny_depp/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json
curl -F "file=@./tests/train/margot_robbie/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json
curl -F "file=@./tests/train/scarlett_johansson/0.jpg" http://localhost:5000/api/v1/demo/face_add | python -m json.tool | bat -p -l json

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

curl -F "file=@./tests/images/bp_0.jpg" http://localhost:5000/api/v1/demo/face | python -m json.tool | bat -p -l json

curl -F "file=@./tests/images/bc_0.jpg" http://localhost:5000/api/v1/demo/face | python -m json.tool | bat -p -l json
curl -F "file=@./tests/images/bc_1.jpg" http://localhost:5000/api/v1/demo/face | python -m json.tool | bat -p -l json

curl -F "file=@./tests/images/sc_0.jpg" http://localhost:5000/api/v1/demo/face | python -m json.tool | bat -p -l json
curl -F "file=@./tests/images/sc_1.jpg" http://localhost:5000/api/v1/demo/face | python -m json.tool | bat -p -l json

curl -F "file=@./tests/images/mr_0.png" http://localhost:5000/api/v1/demo/face | python -m json.tool | bat -p -l json

echo -e "\n"
sleep 1