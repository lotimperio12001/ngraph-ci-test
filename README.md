# ONNX Backend Scoreboard
https://postrational.github.io/ngraph-ci-test/

## Adding new frameweork to the scoreboard

### 1. Prepare Dockerfile
Use dockerfile template link from the exmples to create Dockerfile for new runtime.
#### Find and edit code marked `## ONNX Backend dependencies ##`.
* Set `ONNX_BACKEND` env with python onnx backend module needed to be import in the test script. <br/>
* Write commands required to install all dependencies. <br/>
* If you use release version of packages paste created Dockerfile in the new directory <br/> 
`onnx-backend-scoreboard/runtimes/{new_framework}/stable` <br/>
otherwise use <br/> 
`onnx-backend-scoreboard//runtimes/{new_framework}/development`.

```
############## ONNX Backend dependencies ###########
ENV ONNX_BACKEND="{new_framework.backend}"

# Install dependencies
RUN pip install onnx
RUN pip install {new_framework}

####################################################
```

### 2. Configuration update
* Add new framework to `config.json` file conseqently to `stable` or `development` group.

<br/> For `stable` version:

```json
"new_framework": {
            "name": "New Framework",
            "results_dir": "./results/new_framework/stable",
            "core_packages": ["new-framework"]
        }
```

<br/> For `development` version (`core_packages` list is optional):

```json
"new_framework": {
            "name": "New Framework",
            "results_dir": "./results/new_framework/development",
        }
```

# Usage

## Build docker images
From the main dir (onnx-backend-scoreboard/) 

### Stable 

* ONNX-runtime <br/>
`docker build -t scoreboard-onnx -f runtimes/onnx-runtime/stable/Dockerfile .`

* nGraph <br/>
`docker build -t scoreboard-ngraph -f runtimes/ngraph/stable/Dockerfile .`

* Tensorflow <br/>
`docker build -t scoreboard-tensorflow -f runtimes/tensorflow/stable/Dockerfile .`

### Development (build from source)

* nGraph <br/>
`docker build -t scoreboard-ngraph -f runtimes/ngraph/development/Dockerfile .`

* PyTorch <br/>
`docker build -t scoreboard-pytorch -f runtimes/pytorch/development/Dockerfile .`

<br/>

###### Proxy settings
Use --build-arg to set http and https proxy

`docker build -t scoreboard-<backend> --build-arg http_proxy=your-http-proxy.com/ --build-arg https_proxy=your-https-proxy.com/ -f <path_to_dockerfile>/Dockerfile .`

## Run docker containers

### Stable

* ONNX-runtime <br/>
`docker run --name onnx-runtime --env-file setups/env.list -v ~/onnx-backend-scoreboard/results/onnx-runtime/stable:/root/results scoreboard/onnx`

* nGraph <br/>
`docker run --name ngraph --env-file setups/env.list -it -v ~/onnx-backend-scoreboard/results/ngraph/stable:/root/results scoreboard/ngraph`

* Tensorflow <br/>
`docker run --name tensorflow --env-file setups/env.list -it -v ~/onnx-backend-scoreboard/results/tensorflow/stable:/root/results scoreboard/tensorflow`

### Development (build from source)

* nGraph <br/>
`docker run --name ngraph --env-file setups/env.list -it -v ~/onnx-backend-scoreboard/results/ngraph/development:/root/results scoreboard/ngraph`

* PyTorch <br/>
`docker run --name pytorch --env-file setups/env.list -it -v ~/onnx-backend-scoreboard/results/pytorch/development:/root/results scoreboard/pytorch`

<br/>


## Generation of static pages
From the main dir (onnx-backend-scoreboard/) 

`python3 website-generator/generator.py --config ./setups/config.json`

where --config parameter is the path to config.json file

### Configuration file
Configuration in the `config.json` file contains a list of frameworks included in ONNX Backend Scoreboard. 
This is a place for base information like results paths or core packages names. 
Each new runtime has to be added to this file.

Example of config.json file:
```json
{
    "stable": {
        "onnxruntime": {
            "name": "ONNX-Runtime",
            "results_dir": "./results/onnx-runtime/stable",
            "core_packages": ["onnxruntime"]
        },
        "ngraph": {
            "name": "nGraph",
            "results_dir": "./results/ngraph/stable",
            "core_packages": ["ngraph-onnx", "ngraph-core"]
        },
        "tensorflow": {
            "name": "Tensorflow",
            "results_dir": "./results/tensorflow/stable",
            "core_packages": ["tensorflow"]
        }
    },
    "development": {
        "ngraph": {
            "name": "nGraph",
            "results_dir": "./results/ngraph/development"
        },
        "pytorch": {
            "name": "Pytorch",
            "results_dir": "./results/pytorch/development"
        }
    },
    "deploy_paths": {
        "index": "./docs",
        "subpages": "./docs",
        "resources": "./docs/resources"
    }
}

```


