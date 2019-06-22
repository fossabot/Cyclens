# [Cyclens](https://github.com/Dentrax/Cyclens)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FDentrax%2FCyclens.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FDentrax%2FCyclens?ref=badge_shield)
[![Sourcegraph](https://img.shields.io/badge/view%20on-Sourcegraph-brightgreen.svg)](https://sourcegraph.com/github.com/Dentrax/Cyclens)

**Blazingly Fast, Async, Multi-Task, All-in-One, Image Recognition Modules**

[What It Is](#what-it-is)

[Features](#features)

[How To Use](#how-to-use)

[Installation](#installation)

[Requirements](#requirements)

[Dependencies](#dependencies)

[Collaborators](#collaborators)

[Branches](#branches)

[Copyright & Licensing](#copyright--licensing)

[Contributing](#contributing)

## What It Is

**Cyclens is an All-in-One recognition API server with Async features.**

* Age Prediction

* Emotion Recognition

* Face Recognition

* Gender Prediction

## Features

* Pipeline based process structure between tasks

* Async powered, non-blocking API loop

* Multitask struct for each module process

* Apache Solr powered face search engine

## How To Use

Just send a POST request with module parameters to the Flask server.

* cURL POST 
```bash
$ curl -F "file=@/home/path/to/your/image/file.jpg" http://localhost:5000/api/v1/demo/single?ar=true&ap=true&er=true&fr=true&gp=true
```

* Face Recognition 
```bash
$ curl -F "file=@/home/path/to/your/image/file.jpg" http://localhost:5000/api/v1/demo/face_add?id=0&name=FooBar
```

* Example Output:
```json
{
    "success": true,
    "message": "null",
    "process": {
        "start": "2019-06-02T01:50:05.731130",
        "end": "2019-06-02T01:50:06.580368",
        "total": 849.24
    },
    "modules": [
        {
            "success": true,
            "module": "module_name",
            "message": "null",
            "process": {
                "start": "2019-06-02T01:50:05.731208",
                "end": "2019-06-02T01:50:06.579839",
                "total": 848.63,
                "locations": 97.39,
                "encodings": 240.98,
                "search": 21.1
            },
            "found": 1,
            "rate": 100.0,
            "faces": [
                {
                    "result": "Test",
                    "confidence": 0.87
                }
            ]
        },
    ]
}
```

## Installation

1. Clone the project to your computer and navigate to folder by executing the following command:
```bash
$ git clone https://github.com/Dentrax/Cyclens.git && cd ./Cyclens/
```

2. Create your own virtualenv and install the requirements by executing the following commands:
```bash
$ virtualenv -p python ./
$ source ./bin/activate
$ pip install -r requirements.txt
```

3. Run the Cyclens with following command
```bash
$ sh ./start.sh
```

* Run this command if you want to test all cases
```bash
$ python -m unittest -v
```

* Run this command if you want to test demo project
```bash
$ python ./demo/demo.py
```

## Requirements

### Data Models

1. Download [this](https://github.com/Tony607/Keras_age_gender/releases/download/V1.0/weights.18-4.06.hdf5) and put in `./models/data/age/`
2. Download [this](https://github.com/oarriaga/face_classification/raw/master/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5) and put in `./models/data/emotion/`
3. Download [this](https://github.com/ageitgey/face_recognition_models/tree/master/face_recognition_models/models) and put in `./models/data/face/`
4. Download [this](https://github.com/oarriaga/face_classification/raw/master/trained_models/gender_models/simple_CNN.81-0.96.hdf5) and put in `./models/data/gender/`

### Apache Solr

1. Download the Apache Solr from [here](https://lucene.apache.org/solr/downloads.html)
2. Start the Solr with: `./bin/solr start`
3. Make sure the Solr running on the port `8983`

## Dependencies

* Please see the **[requirements.txt](https://github.com/Dentrax/Cyclens/blob/master/requirements.txt)** file for dependency informations

## Collaborators

* Furkan Türkal (GitHub: **[Dentrax](https://github.com/Dentrax)**)
* Metin UR (GitHub: **[metinUr](https://github.com/metinUr)**)

## Branches

We publish source for the **[Cyclens]** in single rolling branch:

The **[master branch](https://github.com/Dentrax/Cyclens/tree/master)** is extensively tested and makes a great starting point. Also tracks [live changes](https://github.com/Dentrax/Cyclens/commits/master) by commits.

## Copyright & Licensing
 
 All program code (i.e. .py) is licensed under **MIT** License unless otherwise specified. Please see the **[LICENSE](https://github.com/Dentrax/Netlyser/blob/master/LICENSE)** file for more information.

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FDentrax%2FCyclens.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FDentrax%2FCyclens?ref=badge_large)

**References**

While this repository is being prepared, it may have been quoted from some sources.

Please see the **[REFERENCES](https://github.com/Dentrax/Cyclens/blob/master/REFERENCES)** file for more information.

If there is an unspecified source or if you think that I made a copyright infringement, please contact with me.

## Contributing

Please check the [CONTRIBUTING.MD](CONTRIBUTING.MD) file for contribution instructions and naming guidelines.
