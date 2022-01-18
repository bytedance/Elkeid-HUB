# Elkeid HUB Demo

本文会通过运行和讲解以下demo来介绍HUB的核心功能，同时提供简易的ruleset验证环境，用来辅助编写和验证ruleset。

Elkeid HUB通常作为流处理策略引擎，Input和Output一般直接对接消息队列。但demo中Input和Output都为消息队列会非常不便，所以在以下示例中，Input和Output均使用文件读写代替。Input为按行读取，请确保Input文件中每个json为一行，且文件以换行符结尾。

所有以下测试用例均位于demo文件夹中，不需要从该文档中粘贴走。所有demo都可以直接执行，除demo 1详尽介绍项目结构外，其他demo都是只介绍了关键部分，其余部分与demo 1相同。

## 运行 demo

解压好hub 社区版后，在当前目录下执行 `./bootstrap.sh -c demo/1.RM_LOG/` 即可运行demo。首次执行会涉及到初始化python运行环境，比较慢，请勿在中途Ctrl-C。在看见 `[AgentSmith] SMITH 'elkeid_demo' PROJECT READY TO START` 输出后且无其他报错提示，表示demo执行正常。等待10s，Ctrl-C结束HUB，查看 `demo/1.RM_LOG/output/output_demo.result` 文件。该文件中有json，证明demo执行成功。

成功运行demo后，可以直接查看demo内的各个文件，每个文件基本上都是自解释的，可以尝试自行修改。如果需要相关讲解，再继续看以下文档对应部分或Ruleset介绍部分。

## 1. RM LOG 删除日志 

此demo用于匹配删除敏感日志的操作。查看 /var/log/auth.log是查看入侵行为中必要的一步，如果有人手动删除和修改了auth.log，需要记录此行为。

### Exec

在elkeid community社区版的根目录下执行该demo：

```sh
./bootstrap.sh -c demo/1.RM_LOG/
```

看见标准输出中有 `[AgentSmith] SMITH 'elkeid_demo' PROJECT READY TO START` 的输出后，等待10s，ctrl-c结束HUB，查看 `demo/1.RM_LOG/output/output_demo.result` 文件。该文件中有json，证明demo执行成功。

注：该文件手动格式化过，实际文件中是未格式化的json。

### Project

elkeid_demo.yml 位于 demo/1.RM_LOG/project/ 下，所有demo的project文件均位于各自demo文件夹下的project文件中。

该demo是一个最简单的project，一个名为demo的input，经过名为demo_rm_log的ruleset后，匹配的结果输出到名为result的output中。Project文件内容如下：

```yaml
ProjectID: elkeid_demo
ProjectName: elkeid_demo
SmithDSL: |
  INPUT.demo --> RULESET.demo_rm_log
  RULESET.demo_rm_log --> OUTPUT.result
```

### Input

该input表示数据从文件 demo/1.RM_LOG/input/input_demo.json 中读取，input如下：

```YAML
InputID: demo
InputName: demo
InputType: mock_from_files
DataType: json
MockFromFiles: 
  - demo/1.RM_LOG/input/input_demo.json
MockFromFilesRepeat: 1
```

首先看下原始数据，以下部分为原始数据的部分关键字段，实际exec类型采集的数据非常丰富，具体参照[https://gitHUB.com/bytedance/Elkeid/tree/main/driver](https://gitHUB.com/bytedance/Elkeid/tree/main/driver)。
如果需要在demo的input中放入更多的样例数据，需要保证每个数据占一行，需要是压缩过后的json，不能是format后的json。

demo/1.RM_LOG/input/input_demo.json 内容格式化后如下：

```JSON
{
    "agent_id": "80ab2f3b-0000-0000-0000-000000000000",
    "argv": "rm -i -fr /var/log/aumux.log /var/log/auth.log /var/log/daemon.log /var/log/dpkg.log /var/log/systemd_monitor.log /var/log/user.log",
    "comm": "rm",
    "data_type": "59",
    "exe": "/bin/rm",
    "exe_hash": "c04ea6e4d1d72c3f",
    "hostname": "xxx",
    "ld_preload": "-1",
    "pgid": "3417264",
    "pgid_argv": "-3",
    "pid": "3417264",
    "pid_tree": "3417264.rm<3417230.bash<3417223.sshd<994.sshd<1.systemd",
    "pns": "4026531836",
    "ppid": "3417230",
    "ppid_argv": "-bash",
    "run_path": "/root",
    "sa_family": "2",
    "sessionid": "71525",
    "sid": "3417230",
    "sip": "x.x.x.x",
    "socket_argv": "/usr/sbin/sshd -D -R",
    "socket_pid": "3417223",
    "sport": "22",
    "ssh": "x.x.x.x 60660 x.x.x.x 22",
    "stdin": "/dev/pts/0",
    "stdout": "/dev/pts/0",
    "tags": "",
    "tgid": "3417264",
    "time": "1641971122",
    "time_pkg": "1641971122",
    "timestamp": "2022-01-12T07:05:22Z"
}
```

### Output

同理，output位于demo/1.RM_LOG/output/ 下，output的结果会写入到`demo/1.RM_LOG/output/output_demo.result` 文件中。

output配置文件如下：

```YAML
OutputID: result
OutputName: result
OutputType: file
OutputFile: "demo/1.RM_LOG/output/output_demo.result"
```

### Ruleset

Ruleset是HUB的核心部分，用于执行策略。这里我们重点关注数据中的argv字段，该字段为实际执行的命令。接下来我们的工作就是匹配到argv，这里我们使用的Regex+INCL。第一个check node表示argv中需要包含 `/var/log`，第二个check node是一个正则表达式，会匹配到rm，nano，gedit，emacs等命令的执行。两个check node同时匹配到才会命中此策略。

Ruleset示例如下：

```XML
<root ruleset_id="demo_rm_log" ruleset_name="demo_rm_log" type="Rule" undetected_discard="true">
    <rule rule_id="DEMO_RM_LOG_001" type="Detection" author="elkeid_group">
        <rule_name>DEMO_RM_LOG_001</rule_name>
        <harm_level>critical</harm_level>
        <filter part="data_type">59</filter>
        <check_list>
            <check_node part="argv" type="INCL" check_data_type="static">/var/log/</check_node>
            <check_node part="argv" type="REGEX" check_data_type="static"><![CDATA[(?:(?:\brm\b|\bnano\b|\bgedit\b|\bemacs\b|\bprintf\b|\becho\b|\bchattr\s+\+i\b\s+-[\w-]*\b)[a-zA-Z0-9-\n ./]*\b)]]></check_node>
        </check_list>
        <alert_data>true</alert_data>
        <modify></modify>
        <del></del>
        <action></action>
        <desc affected_target="create file">检测到删除日志文件</desc>
    </rule>
</root>
```

### 执行 & 查看结果

结果在文件`demo/1.RM_LOG/output/output_demo.result` 中，格式化后如下。

```JSON
{
    "SMITH_ALERT_DATA": {
        "HIT_DATA": [
            "DEMO_RM_LOG_001 argv:[INCL]:/var/log/",
            "DEMO_RM_LOG_001 argv:[REGEX]:rm -i -fr /var/log/aumux.log /var/log/auth.log /var/log/daemon.log /var/log/dpkg.log /var/log/"
        ],
        "RULE_INFO": {
            "Action": null,
            "AffectedTarget": "create file",
            "Author": "elkeid_group",
            "Desc": "检测到删除日志文件",
            "DesignateNode": null,
            "FreqCountField": "",
            "FreqCountType": "",
            "FreqHitReset": false,
            "FreqRange": 0,
            "HarmLevel": "critical",
            "KillChainID": "",
            "RuleID": "DEMO_RM_LOG_001",
            "RuleName": "DEMO_RM_LOG_001",
            "RuleType": "Detection",
            "Threshold": ""
        }
    },
    "SMITH_INPUT": "demo",
    "SMITH_KEY": "302581201917444107",
    "SMITH_TIMESTAM": 1642145028264325095,
    "agent_id": "80ab2f3b-0000-0000-0000-000000000000",
    "argv": "rm -i -fr /var/log/aumux.log /var/log/auth.log /var/log/daemon.log /var/log/dpkg.log /var/log/systemd_monitor.log /var/log/user.log",
    "comm": "rm",
    "data_type": "59",
    "exe": "/bin/rm",
    "exe_hash": "c04ea6e4d1d72c3f",
    "hostname": "xxx",
    "ld_preload": "-1",
    "pgid": "3417264",
    "pgid_argv": "-3",
    "pid": "3417264",
    "pid_tree": "3417264.rm<3417230.bash<3417223.sshd<994.sshd<1.systemd",
    "pns": "4026531836",
    "ppid": "3417230",
    "ppid_argv": "-bash",
    "run_path": "/root",
    "sa_family": "2",
    "sessionid": "71525",
    "sid": "3417230",
    "sip": "x.x.x.x",
    "socket_argv": "/usr/sbin/sshd -D -R",
    "socket_pid": "3417223",
    "sport": "22",
    "ssh": "x.x.x.x 60660 x.x.x.x 22",
    "stdin": "/dev/pts/0",
    "stdout": "/dev/pts/0",
    "tags": "",
    "tgid": "3417264",
    "time": "1641971122",
    "time_pkg": "1641971122",
    "timestamp": "2022-01-12T07:05:22Z"
}
```

关键数据会放到SMITH_ALERT_DATA中，以下为关键字段：

HIT_DATA 表示命中check node的结果，表示argv字段命中了check node

RULE_INFO.RuleID 表示命中的是哪个rule

RULE_INFO.Desc 是命中的Rule中的Description，这里可以添加关于rule的解释。

到这里，该project就完成了，输入的是elkeid agent上报的原始日志，输出的是敏感日志删除操作。

### 扩展

1. check node之间是“与”的关系，有时候需要更多的过滤条件，都可以在通过添加check node来实现，可以参考 demo/1.RM_LOG/extra/demo_rm_log_1.xml 中的ruleset，添加了更多的check node用来实现过滤。例如，有自定义tag data且host name不包含 test 的主机才会产生告警。可以用该ruleset文件覆盖 demo/1.RM_LOG/ruleset/demo_rm_log.xml来测试。

2. 针对删除不同的log，可以产生的不同的告警，此时可以通过在一个ruleset中写多个rule来实现。或者说同一个ruleset中就可以处理很多类型的告警。参考 demo/1.RM_LOG/extra/demo_critical.xml，里面有多个rule，分别产生不同类型的告警。
3. 将项目中提供的其他测试策略复制到 demo/1.RM_LOG/ruleset 文件夹中，修改project，保证数据经过此部分ruleset，验证测试策略的功能。

## 2. SSH LOGIN 登录记录

demo 1 中使用的是Rule类型的Rule，还有Frequency类型的Ruleset。

Detection类型的Ruleset主要是检查单个数据就能确定的告警，Frequency类型在Rule类型的基础上，增加了频率检测，以SSH登录为例，单位时间内多次登录失败，才需要出发告警。

ssh日志是elkeid agent的journal watcher plugin上报的，data type为4000。

### Exec

在elkeid community社区版的根目录下执行该demo：

```XML
./bootstrap.sh -c demo/2.SSH_LOGIN/
```

### Input

Input数据中的关键部分：

```undefined
{
    "agent_id": "80ab2f3b-0000-0000-0000-000000000000",
    "data_type": "4000",
    "hostname": "debian",
    "invalid": "false",
    "pid": "46182",
    "rawlog": "Failed password for root from x.x.x.x port 37266 ssh2",
    "risk": 2,
    "sip": "1.2.3.4",
    "sport": "37266",
    "status": "false",
    "time": "1642055662",
    "time_pkg": "1642055662",
    "timestamp": "2022-01-13T06:34:22Z",
    "types": "password",
    "user": "root"
}
```

status表示登录是否成功，单位时间内超过x次登录失败，可以怀疑是存在暴力破解。

Input中的 `MockFromFilesRepeat: 5 ` 代表该数据重复5次。

### Ruleset

```XML
<root ruleset_id="demo_ssh_login" ruleset_name="demo_ssh_login" type="rule" undetected_discard="true">
    <rule rule_id="demo_sip_multi_login" type="Frequency" author="elkeid_group">
        <rule_name>demo_sip_multi_login</rule_name>
        <harm_level>high</harm_level>
        <threshold count_field="agent_id" range="60">5</threshold>
        <node_designate>
        </node_designate>
        <filter part="data_type">4000</filter>
        <check_list>
            <check_node part="status" type="INCL" check_data_type="static">false</check_node>
            <check_node part="rawlog" type="NI" check_data_type="static"><![CDATA[receive identification]]></check_node>
        </check_list>
        <alert_data>true</alert_data>
        <modify></modify>
        <del></del>
        <action></action>
        <desc>集群中存在同IP爆破情况</desc>
    </rule>
</root>
```

### Output

结果文件如下，结果中只有一条，因为threshold值为5，单位时间内超过5条才触发。

```JSON
{
    "SMITH_ALERT_DATA": {
        "HIT_DATA": [
            "demo_sip_multi_login status:[INCL]:false",
            "demo_sip_multi_login rawlog:[NI]:receive identification",
            "demo_sip_multi_login Frequency:5"
        ],
        "RULE_INFO": {
            "Action": null,
            "AffectedTarget": "host_process",
            "Author": "elkeid_group",
            "Desc": "集群中存在同IP爆破情况",
            "FreqCountField": "agent_id",
            "FreqCountType": "",
            "FreqHitReset": false,
            "FreqRange": 60,
            "HarmLevel": "high",
            "KillChainID": "critical",
            "RuleID": "demo_sip_multi_login",
            "RuleName": "demo_sip_multi_login",
            "RuleType": "Frequency",
            "Threshold": "5"
        }
    },
    ...
}
```

### 扩展

1. 修改Input中的 `MockFromFilesRepeat: 5` 为其他数字，验证是否还会触发告警或触发多个告警。

2. 在ruleset demo_ssh_login的threshold部分添加上 hit_reset="true"，验证触发多个告警时的告警数量。

3. 在ruleset demo_ssh_login的node_designate部分添加上`<node_designate><node part="sip"></node></node_designate>` ，表示根据sip字段进行group by，同时修改input的数据，验证效果。

## 3. Append & Action 

### Exec

在elkeid community社区版的根目录下执行该demo：

```XML
./bootstrap.sh -c demo/3.APPEND/
```

### Append

通常Agent上报的原始数据中无法包含CMDB等业务信息，虽然AC是开源的，可以通过修改AC将部分业务信息一同写入原始数据，但是门槛较高，而且操作不当会影响AC性能及稳定性，不建议一般用户使用。所以多些时候，还是可以通过append类plugin尽可能的丰富业务信息。

本demo中提供了一个名为AddCmdbInfo的Plugin，该Plugin用于模拟获取cmdb信息。

该plugin位于 `demo/3.APPEND/plugin/AddCMDBInfo` 文件夹中，核心逻辑为在plugin.py中。

### Action

我们推荐将告警通过output写入消息队列，用户通过消费消息队列来查看告警，但很多时候希望可以临时发送出结果，或者简单的和其他系统联动。此时可以通过action plugin发出该消息，我们预先提供了dingding，weixin，email，telgram等类型的plugin，可以将数据直接推送出去。用户也可以自行实现，

`demo/3.APPEND/plugin/PushMsgToFile` 内提供了一个将结果写入到文件 `/tmp/elkeid_action.txt` 的简单plugin。所有发送消息类的plugin都需要额外配置发送到哪里，所以提供了一个简易的写文件plugin用于模拟。

### Ruleset

本次提供了两个简易的ruleset，demo_load_lvm和push_alert。demo_load_lvm用于匹配内核模块加载事件，同时触发AddCMDBInfo插件，将cmdb信息附加到数据流，push_alert用于触发action插件。

### 执行 & 查看结果

预期在文件 /tmp/elkeid_action.txt 中可以查看到插件写入的数据。

### 扩展

1. Plugin开发文档中提供了dingding，weixin，email，telgram等类型的plugin，可以放到 `demo/3.APPEND/plugin` 文件夹中，同时修改push_alert这个ruleset中的action，测试其他plugin。