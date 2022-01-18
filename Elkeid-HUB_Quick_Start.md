English | [简体中文](Elkeid-HUB_Quick_Start-zh_CN.md)

## Elkeid-HUB Quick Start

### System Requirements

64-bit Linux distribution(amd64)

### Network Requirements

HUB can connect **ES/Kafka** used in Input/Output

### Step 1. Download the HUB file

HUB Compressed package contains the HUB binary file, runtime dependencies, runtime configuration (config), and the runtime environment required by the Python plugin.Execute the following command to download and unzip the HUB file. 

```Shell
mkdir -p ~/elkeid && cd ~/elkeid
wget https://github.com/bytedance/Elkeid-HUB/releases/download/v1.0/elkeid_hub_community_v1.0.zip
unzip elkeid_hub_community_v1.0.zip
cd elkeid_hub_community
```

### Step 2. Edit HUB configuration

Elkeid HUB components mainly include the following types, the configuration files are located in the config directory:

- **Input**: Input indicates the data stream to enter the HUB, currently supports **Kafka**
- **Output**: Output indicates the output data stream of Elkeid HUB, currently supports **ES/Kafka**
- **RuleSet**: RuleSet indicates the core logic of data processing will be defined by RuleSet, such as **detection** (support regular, multi-mode matching, frequency and other detection methods)/**whitelist**/**call Plugin**, etc.
- **Plugin**: Users can **customize arbitrary detection**/**response logic** to meet the needs of some complex scenarios, such as sending alarms to DingTalk/Lark; linking with CMDB for data supplementation; linking with Redis to perform some cache processing, etc.  After writing, these plugins can be called in the RuleSet
- **Project**: Build a set of Elkeid HUB logic through Project, usually composed of one Input and one or more RuleSet and one or more Output

The config directory contains the default Project provided, including an input and an output and a few simple Rulesets.

The following is a brief introduction to the configuration. For details of the specific fields, please refer to the user manual.

- config/input/hids.yml

```YAML
InputID: hids                              #Inputid
InputName: hids
InputType: kafka                            #currently supports Kafka only
DataType: json                              #also support custom datatype
KafkaBootstrapServers: 127.0.0.1:9092       #Must be changed to the real kafka address before running
KafkaGroupId: lch_test1                     #consumer group id
KafkaOffsetReset: earliest                        
KafkaCompression: none
KafkaTopics:
  - hids_svr                                   #you can fill in multiple topics
KafkaOtherConf: ~
KafkaWorkerSize: 1
```

- config/output/test.yml

```YAML
OutputID: test
OutputName: test
OutputType: kafka
KafkaBootstrapServers: 127.0.0.1:9092       #Must be changed to the real kafka address before running
KafkaTopics: res1                           # output topic
AddTimestamp: true
KafkaOtherConf: ~
```

Also provides a default Project file:

- config/project/Project.yml

This project implements simple input from input, through test Ruleset to output, and the specific rules need to be modified in config/ruleset/test.xml.

```Makefile
ProjectID: test
ProjectName: test
SmithDSL: |
          INPUT.hids --> RULESET.test
          RULESET.test --> OUTPUT.test      #For details, please refer to Chapter 8 project in the handbook
```

### Step 3. Run HUB

In normal use, you can run the startup script directly(bootstrap.sh). If you need to modify the config path and api server port, you can add parameters after the script.

The Python venv is initialized the first time it is executed, which takes a few minutes, depending on the machine configuration, and stays in `Building wheel for gevent (PEP 517) ... - ` for a long time in between, do not run Ctrl - C at this time.

```YAML
./bootstrap.sh
```

The API Server running port and configuration file path of HUB can be specified in the running parameters. The optional parameters are as follows:

- -h, --help                      show help
- -p, --port NUM            Set API Server port, default 8091
- -c, --conf CONFDIR    Set the configuration file path, the default is the config folder under the HUB path



### Step 4. Log and Status Check

After the HUB starts, it will automatically check the rules and start all projects. If the Project works normally, there will be normal output at Output. The log log is stored in the log/smith.log file. If you need to check the Project and QPS status, you can query it through the API, such as getting QPS information

```Nginx
curl 127.0.0.1:8091/getQPSInfo
```

It will return the current QPS information of each component as follows

```JSON
{"success":true,"data":{"test":{"ANALYSER":{},"INPUT":{"hids":50},"OUTPUT":{"test":25},"RULESET":{"add_timestamp":0}}}
```

For the specific usage of the API, please refer to Chapter 9 of the HUB Community Edition User Handbook. The Community Edition only provides query-related APIs.

## FAQ

### 1 List plugin error: stat py/elkeid.sock: no such file or directory

Execute cat py/plugin.stdout to view the error log

If `shm_open failed: Permission denied` appears, it is usually because the root user was used in the last operation, which caused file permission pollution. You need to execute the following command to manually clear the polluted file.

```Nginx
sudo rm -r /dev/shm/elkeid_queue_*
```

### 2 Python environment installation problem

When starting the HUB for the first time, due to the path issue, you need to install the downloaded python environment. If you need to migrate the HUB program path, you need to reinstall the python environment.The script judges the environment installation status by whether the `py/.success` file exists, so delete the file and run `bootstrap.sh` again to reinstall the python environment.

