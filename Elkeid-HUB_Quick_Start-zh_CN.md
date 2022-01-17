## Elkeid-HUB Quick Start

### 系统要求

64位 Linux 发行版（amd64) 

### 网络要求

HUB自身能够连通Input/Output中所用到的**ES/Kafka**

### Step 1. 下载HUB文件

预编译版本中包含了HUB二进制，运行依赖，运行配置（config），以及Python插件需要的运行环境。执行如下命令来下载并解压HUB文件。

```Shell
mkdir -p ~/elkeid && cd ~/elkeid

curl http://tosv.byted.org/obj/agentsmith-hub-testing/elkeid_hub_community.zip -o elkeid_hub_community.zip

unzip elkeid_hub_community.zip

cd elkeid_hub_community
```

### Step 2. 编辑HUB配置

Elkeid HUB 组件主要有以下几种，配置文件位于config目录下：

- **Input**：Input表示要进入HUB的数据流，目前支持**Kafka**
- **Output**：Output表示Elkeid HUB的输出数据流，目前支持**ES/Kafka**
- **RuleSet**：数据处理的核心逻辑将通过RuleSet定义，如**检测**(支持正则，多模匹配，频率等多种检测方式)/**白名单**/**调用Plugin**等
- **Plugin**：用户可以**自定义任意检测**/**响应逻辑**，来满足一些复杂场景的需求，如发送告警到钉钉/飞书；与CMDB联动进行数据补充；联动Redis进行一些缓存处理等。编写完成后可以在RuleSet中调用这些插件
- **Project**：通过Project来构建一组Elkeid HUB逻辑，通常是由一个Input+一个或多个RuleSet+一个或多个Output组成

config目录包含了提供的默认Project，包含一个input和一个output和几个简单的Ruleset。

下面为对配置进行简单介绍，具体字段的详细内容可以参考使用手册。

- config/input/hids.yml

```YAML
InputID: hids                              #Input的id

InputName: hids

InputType: kafka                            #目前仅支持kafka

DataType: json                              #也支持自定义格式

KafkaBootstrapServers: 127.0.0.1:9092       #kafka地址 运行前务必修改为真实kafka地址

KafkaGroupId: lch_test1                     #consumer group id

KafkaOffsetReset: earliest                        

KafkaCompression: none

KafkaTopics:

  - hids_svr                                   #kafka topic,可以填写多个topic

KafkaOtherConf: ~

KafkaWorkerSize: 1
```

- config/output/test.yml

```YAML
OutputID: test

OutputName: test

OutputType: kafka

KafkaBootstrapServers: 127.0.0.1:9092       #kafka地址 运行前务必修改为真实kafka地址

KafkaTopics: res1                           #输出的topic

AddTimestamp: true

KafkaOtherConf: ~
```

同时提供了默认的Project文件

- config/project/Project.yml

这个project实现了简单的从input输入，经过test Ruleset到output，具体的规则需要在config/ruleset/test.xml中修改。

```Makefile
ProjectID: test

ProjectName: test

SmithDSL: |

          INPUT.hids --> RULESET.test

          RULESET.test --> OUTPUT.test      #这里详情可以参看手册中第8章project
```

### Step 3. 运行HUB

正常使用可以直接运行启动脚本来运行，如果需要修改配置路径以及访问端口可以在脚本后添加参数。

首次执行时会初始化Python venv，需要数分钟，具体取决于机器配置，同时中间会有较长时间停留在`Building wheel for gevent (PEP 517) ... - `，此时请勿Ctrl - C。

```YAML
./bootstrap.sh
```

HUB的API Server运行端口和配置文件路径可以在运行参数中指定，可选参数如下：

- -h, --help                      显示参数帮助
- -p, --port NUM            设置API Server端口，默认8091
- -c, --conf CONFDIR    设置配置文件路径，默认当前路径下的config文件夹



### Step 4. 日志及状态检查

HUB启动后会自动对规则进行检查，并且启动全部的Project。如果Project工作正常，Output处会有正常输出。日志日志存放在log/smith.log文件中。如果需要查看Project、QPS状态可以通过API接口进行查询，比如查询QPS数据信息

```Nginx
curl 127.0.0.1:8091/getQPSInfo
```

会返回当前各个组件的QPS信息如下

```JSON
{"success":true,"data":{"test":{"ANALYSER":{},"INPUT":{"hids":50},"OUTPUT":{"test":25},"RULESET":{"add_timestamp":0}}}
```

API的具体使用方法可以参考HUB社区版使用手册第9章。社区版仅提供了查询相关的API。

## 常见问题

### 1 List plugin error: stat py/elkeid.sock: no such file or directory

执行cat py/plugin.stdout 查看错误日志

如果出现`shm_open failed: Permission denied`，通常为上次运行使用了root用户，造成了文件权限污染，需要执行以下命令手动清除被污染的文件。

```Nginx
sudo rm -r /dev/shm/elkeid_queue_*
```

### 2 Python环境安装问题

在第一次启动HUB时，由于路径，需要安装已经下载好的python环境，如果需要迁移HUB程序路径，就需要重新安装python环境。脚本通过`py/.success`文件是否存在来判断环境安装状态，因此删除该文件再次运行`bootstrap.sh`即可重新安装python环境。

