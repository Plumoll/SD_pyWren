# SD_pyWren

# Task 1: Foundations of distributed systems
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Is requiered a configuration file (in .yaml format) located in the root direcory of the project, and named ibm_cloud_config in order to have access to those services.
ibm_cloud_config follows the following format:

```
ibm_cf:
    endpoint    : CF_API_ENDPOINT
    namespace   : CF_HOST
    api_key     : CF_API_KEY

ibm_cos:
    endpoint   : COS_API_ENDPOINT
    access_key : ACCESS_KEY
    secret_key : SECRET_KEY
    bucket     : Bucket

rabbitmq:
    url         : URL
```

yaml is necessary to read the configuration file, and it can be intalled like this:

```
sudo pip install pyyaml
```


### Installing

To run the code is it necessary to have installed the pyWren library for Python3.7. You can install it by using the following command:

```
sudo pip3 install pywren-ibm-cloud
```

## Running the program

The program can be executed with the following command:
    
```
python3 multiple_queue_cs.py
```

## Our project

### Important points
* Tomato
* P2
* P3
* P4
* P5


## Built With

* [IBM cloud](https://www.ibm.com/uk-en/cloud) - cloud functions
* [rabbitmq](https://www.rabbitmq.com) - queue management
* [IBM-pyWren](https://github.com/pywren-ibm-cloud) - IBM-pyWren on GitHub

## Authors

* **Guillem Frisach Pedrola** - (guillem.frisach@estudiants.urv.cat)
* **Magí Tell Bonet** - (magi.tell@estudiants.urv.cat)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
