# cyclens-server

## Run

1. `source ./bin/activate`
2. `python -m cyclens`

## Common Issues

* `emoticon` değil `emotion` !!!
* `recognation` değil `recognition` !!!

## Installation

```bash
virtualenv -p python3 ./
source ./bin/activate
pip install -r requirements.txt
```

## PreCheck

`pacman -Qs nvidia` : Olması gereken paketler:

1. `cuda`
2. `cudnn`
3. `nvidia`
3. `nvidia-settings`
4. `bumblebee`

## Check

* `virtualenv` aktif edildiği zaman;

1. `which python3` : Bulunan dosyayı göstermeli, `/usr/bin/...` değil!

2. `python3 -c 'import tensorflow as tf; print(tf.__version__)'`: TensorFlow sürümünü vermeli

3. `optirun python3 -c 'import tensorflow as tf; print(tf.__version__)'`: TensorFlow-GPU sürümünü vermeli

## PostCheck

* `nvidia-smi`: Düzgün çalışıp bilgileri doğru bir şekilde almalı

* `nvidia-settings -q all`: Düzgün çalışıp bilgileri doğru bir şekilde almalı

* `optirun nvidia-settings -c :8`: Ayarların doğru olduğundan ve *PowerMizer*, `MAX PERFORMANCE` olarak ayarlandığından emin olunmalı 

KANSER OLMAMAK ICIN TUM ADIMLARIN DUZGUN CALISTIGINDAN EMIN OL!!!

## GPU TEST

* `watch -n 1 nvidia-smi`: Açık dursun

* `optirun glxspheres64`: Çalıştır ve kontrol et
