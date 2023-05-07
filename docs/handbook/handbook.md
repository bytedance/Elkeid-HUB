# Elkeid HUB Community Edition User Guide

## **Applicable version**

Elkeid HUB Elkeid Community Edition


## **1 Overview**

Elkeid Hub is a product born to address the needs of **data reporting - real-time stream processing and event processing** in **real-time processing** in various fields, suitable for scenarios such as **intrusion detection/event processing and orchestration** and so on.


![alt_text](002.png "image_tooltip")



## **2 Elkeid HUB Advantages**



* **High performance.** 10 times compare to Flink, and supports distributed horizontal expansion.
* **Policies writing is simplified.** security operators only need to focus on data processing itself and the learning cost is very low.
* **Support custom plugins.** Support plugins to better handle complex requirements.
* **Easy deployment.** Written in go, standalone and limited dependency.


## **3 Elkeid HUB Component Overview**

Elkeid HUB components are mainly divided into the following categories:



* **Input**: Data is consumed through the Input component and entered into Elkeid HUB, currently supporting Kafka **Kafka.**
* **Output**: Data pushes the data flowing in the Elkeid HUB out of the HUB through the Output component, which currently supports **ES /Kafka.**
* **RuleSet**: The core logic of data processing will be written through RuleSet, such as **detection** (support regular, multi-mode matching, frequency, and other detection methods)/**Whitelist/Execute plugin** , etc.
* **Plugin**: Users can **customize arbitrary detection/response logic** to meet the needs of some complex scenarios, such as sending alarms to DingTalk/Feishu; linkage with CMDB for data supplementation; linkage to Redis for some cache processing. After writing, you can call these plugins in RuleSet.
* **Project**: Project to build a set of Elkeid HUB logic, usually consisting of an Input + one or more RuleSets + one or more Outputs


## **4 Elkeid Input/Input Source**


![alt_text](003.png "image_tooltip")



### **4.1 Input configuration suggestions**



* The input source currently only supports Kafka as the data input source. The data format supports **Json or any streaming log with a clear eliminator**.
* Suggested data source types:
  * **Alarm logs of other security products,** HUB can effectively carry out secondary processing, such as linkage with other basic components to make up for the missing part of the alarm data, or through custom Action (rule engine support) to realize the automatic processing of alarms
  * **Basic logs**, such as HTTP Mirroring Traffic /Access logs/HIDS data, etc. Through the rule engine, linkage module and anomaly detection module to the original data source for security analysis/intrusion detection/automatic defense operations
  * **Application audit logs,** Such as: login, original SQL request, sensitive operation and other logs. HUB can customize its audit function


### **4.2 Input configuration instructions**

Configuration field:


<table>
  <tr>
   <td>Field
   </td>
   <td>Description
   </td>
  </tr>
  <tr>
   <td>InputID
   </td>
   <td>Not repeatable, describe an input, only English + "_/-" + numbers
   </td>
  </tr>
  <tr>
   <td>InputName
   </td>
   <td>Describe the name of the input, can be repeated, can use Chinese
   </td>
  </tr>
  <tr>
   <td>InputType
   </td>
   <td>Currently only supports Kafka
   </td>
  </tr>
  <tr>
   <td>DataType
   </td>
   <td>json/protobuf/custom/grok
   </td>
  </tr>
  <tr>
   <td>KafkaBootstrapServers
   </td>
   <td>KafkaBootstrapServers, split IP: PORT tuple with comma
   </td>
  </tr>
  <tr>
   <td>KafkaGroupId
   </td>
   <td>GroupID used when consuming
   </td>
  </tr>
  <tr>
   <td>KafkaOffsetReset
   </td>
   <td>earliest or latest
   </td>
  </tr>
  <tr>
   <td>KafkaCompression
   </td>
   <td>Data compression algorithm in Kafka
   </td>
  </tr>
  <tr>
   <td>KafkaWorkerSize
   </td>
   <td>concurrent consumption
   </td>
  </tr>
  <tr>
   <td>KafkaOtherConf
   </td>
   <td>Other configurations are supported, for specific configuration see:<a href="https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md"> https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md</a>
   </td>
  </tr>
  <tr>
   <td>KafkaTopics
   </td>
   <td>Consumption Topic, supports multiple Topics
   </td>
  </tr>
  <tr>
   <td>GrokPattern
   </td>
   <td>It is meaningful when the DataType is grok, and the data will be parsed and passed backwards according to the GrokPattern
   </td>
  </tr>
  <tr>
   <td>DataPattern
   </td>
   <td>It is meaningful when DataType is custom, describing the data format
   </td>
  </tr>
  <tr>
   <td>Separator
   </td>
   <td>Meaningful when the DataType is custom, the delimiter used to split the data
   </td>
  </tr>
</table>



> All fields above are required

Configuration example (DataType: json):

```
InputID: wafdeny
InputName: wafdeny
InputType: kafka
DataType: json
TTL: 30
KafkaBootstrapServers: secmq1.xxx.com:9092,secmq2.xxx.com:9092,secmq3.xxx.com:9092,secmq4.xxx.com:9092
KafkaGroupId: smith-hub
KafkaOffsetReset: latest
KafkaCompression: none
KafkaWorkerSize: 3
KafkaOtherConf: ~

KafkaTopics:
  - wafdeny
```


## **5 Elkeid Output/Output**


![alt_text](004.png "image_tooltip")



### **5.1 Output Configuration Recommendations**

At present, the default policy of the default HUB is that the alarm does not go Output, and the plug-in is used to directly interact with the Manager to write to the database. If you need to configure the original alarm, you can consider configuring Output

Since HUB is a stream data processing tool and does not have storage capability, it is recommended to configure the output source of data storage, such as ES , Hadoop, SOC , SIEM and other platforms. Currently supported Output types are:



* Kafka
* Elasticsearch


### **5.2 Output configuration instructions**

Configuration field:


<table>
  <tr>
   <td>Field
   </td>
   <td>Description
   </td>
  </tr>
  <tr>
   <td>OutputID
   </td>
   <td>Not repeatable, describe an output, only English + "_/-" + numbers
   </td>
  </tr>
  <tr>
   <td>OutputName
   </td>
   <td>Describe the name of the output, can be repeated, can use Chinese
   </td>
  </tr>
  <tr>
   <td>OutputType
   </td>
   <td>es or kafka
   </td>
  </tr>
  <tr>
   <td>AddTimestamp
   </td>
   <td>true or false, after it is enabled, a timestamp field is added to the final result and a timestamp is added (if this field already exists, it will be overwritten). The format is: 2021-07-05T11:48:14Z
   </td>
  </tr>
  <tr>
   <td>KafkaBootstrapServers
   </td>
   <td>It is meaningful when OutputType is kafka
   </td>
  </tr>
  <tr>
   <td>KafkaTopics
   </td>
   <td>It is meaningful when OutputType is kafka
   </td>
  </tr>
  <tr>
   <td>KafkaOtherConf
   </td>
   <td>It is meaningful when OutputType is kafka
   </td>
  </tr>
  <tr>
   <td>ESHost
   </td>
   <td>It is meaningful when the OutputType is es, and arrays are supported
   </td>
  </tr>
  <tr>
   <td>ESIndex
   </td>
   <td>It is meaningful when OutputType is kafka
   </td>
  </tr>
</table>


Configuration example (es):

```
OutputID: es_abnormal_dbcloud_task
OutputName: es_abnormal_dbcloud_task
OutputType: es
ESHost:
  - http://10.6.24.60:9200
ESIndex: abnormal_dbcloud_task
```

Configuration example (kafka):

```
OutputID: dc_sqlhunter
OutputName: dc_sqlhunter
OutputType: kafka
KafkaBootstrapServers: 10.6.210.112:9092,10.6.210.113:9092,10.6.210.126:9092
KafkaTopics: mysqlaudit_alert
KafkaOtherConf: ~
```

## **6 Elkeid HUB RuleSet**

RuleSet is the part of HUB that implements core detection/response actions, which need to be implemented according to specific business requirements. The following figure shows the simple workflow of RuleSet in HUB:


![alt_text](005.png "image_tooltip")



### **6.1 RuleSet**

HUB RuleSet is a set of rules described by XML

RuleSet has two types, **rule** and **whitelist**, as follows:

```
<root ruleset_id="test1" ruleset_name="test1" type="C">
... ....
</root>
```

```
<root ruleset_id="test2" ruleset_name="test2" type="rule" undetected_discard="true">
... ...
</root>
```

Among them, the &lt; root > &lt;/root > of RuleSet is a fixed mode and cannot be changed at will. Other properties:


<table>
  <tr>
   <td>Field
   </td>
   <td>Description
   </td>
  </tr>
  <tr>
   <td>ruleset_id
   </td>
   <td>Not repeatable, describe an output, only English + "_/-" + numbers
   </td>
  </tr>
  <tr>
   <td>ruleset_name
   </td>
   <td>Describe the name of the ruleset, can be repeated, can use Chinese
   </td>
  </tr>
  <tr>
   <td>type
   </td>
   <td>It is a rule or a whitelist, where the rule means that the detection continues to pass backward, and the whitelist means that the detection does not pass backward; the concept of backward pass can be simply understood as the detection event of the ruleset
   </td>
  </tr>
  <tr>
   <td>undetected_discard
   </td>
   <td>It is meaningful only when the rule is a rule, which means whether it is discarded if it is not detected. If it is true, it will be discarded if it is not detected by the ruleset. If it is false, it will continue to pass backwards if it is not detected by the rulset
   </td>
  </tr>
</table>



### **6.2 Rule**

Usually ruleset is composed of one or more rules, it should be noted that the relationship between multiple rules is an'or 'relationship, that is, if a piece of data can Hit one or more of the rules.

```
<root ruleset_id="test2" ruleset_name="test2" type="rule" undetected_discard="true">

    <rule rule_id="rule_xxx_1" author="xxx" type="Detection">
        ... ...
    </rule>

    <rule rule_id="rule_xxx_2" author="xxx" type="Frequency">
        ... ...
    </rule>

</root>
```

The basic properties of a rule are:


<table>
  <tr>
   <td>field
   </td>
   <td>Description
   </td>
  </tr>
  <tr>
   <td>rule_id
   </td>
   <td>Not repeatable in the same ruleset, identify a rule
   </td>
  </tr>
  <tr>
   <td>author
   </td>
   <td>Identify the author of the rule
   </td>
  </tr>
  <tr>
   <td>type
   </td>
   <td>There are two types of rules, one is Detection, which is a stateless detection type rule; the other is Frequency, which is a frequency correlation detection of data streams based on Detection
   </td>
  </tr>
</table>


Let's start with simple examples of two different types of rules.

Let's first assume that the data sample passed from Input to Ruleset is:
```
{

    "data_type":"59",

    "exe":"/usr/bin/nmap",

    "uid":"0"

}
```

##### **6.2.1 Detection Simple Example**

```
<rule rule_id="detection_test_1" author="EBwill" type="Detection">
   <rule_name>detection_test_1</rule_name>
   <alert_data>True</alert_data>
   <harm_level>high</harm_level>
   <desc affected_target="test">这是一个Detection的测试</desc>
   <filter part="data_type">59</filter>
   <check_list>
       <check_node type="INCL" part="exe">nmap</check_node>
   </check_list>
</rule>
```

The detection_test_1 meaning of this rule is that when the data_type with data is 59 and there is nmap in exe, the data continues to be passed backwards.


##### **6.2.2 Frequency Simple Example**

```
<rule rule_id="frequency_test_1" author="EBwill" type="Frequency">
   <rule_name> frequency_test_1 </rule_name>
   <alert_data>True</alert_data>
   <harm_level>high</harm_level>
   <desc affected_target="test">这是一个Frequency的测试</desc>
   <filter part="data_type">59</filter>
   <check_list>
       <check_node type="INCL" part="exe">nmap</check_node>
   </check_list>
   <node_designate>
       <node part="uid"/>
   </node_designate>
   <threshold range="30" local_cache="true">10</threshold>
</rule>
```

The meaning frequency_test_1 this rule is: when the data_type of data is 59, and there is nmap in exe, enter the frequency detection: when the same uid , more than > = 10 behavior occurs within 30 seconds, then the alarm, and the current HUB instance itself cache is used in this process.

We can see that in fact, Frequency is only more than Detection **node_designate and threshold** fields, that is, no matter what the rules, will need to have the most basic fields, we will first understand these general basic fields.


##### **6.2.3 General field description**


<table>
  <tr>
   <td>field
   </td>
   <td>Description
   </td>
  </tr>
  <tr>
   <td>rule_name
   </td>
   <td>Represents the name of rule, unlike rule_id, can use Chinese or other ways to better express the meaning of rule, can be repeated
   </td>
  </tr>
  <tr>
   <td>alert_data
   </td>
   <td>True or False, if True, the underlying information of the rule will be added to the current data and passed backwards; if False, the information of the rule will not be added to the current data
   </td>
  </tr>
  <tr>
   <td>harm_level
   </td>
   <td>Expressing a risk level for the rule, which can be info/low/ a /high/critical
   </td>
  </tr>
  <tr>
   <td>desc
   </td>
   <td>It is used to provide a description of the rule itself, affected_target of which is the component information for which the rule is directed, which is filled in by the user without mandatory restrictions
   </td>
  </tr>
  <tr>
   <td>filter
   </td>
   <td>The first layer of filtering data, part represents which field in the data is filtered, the specific content is the detection content, the meaning is whether there is part, the detection data, if the type of RuleSet is rule exists, the logic of the rule continues to be executed downward, if it does not exist, it is not detected downward; when the RuleSet type is whitelist, the opposite is true, that is, the detection is skipped if it exists, and the detection continues if it does not exist.
<p>
Only one filter can exist, and by default only supports "presence" logical detection
   </td>
  </tr>
  <tr>
   <td>check_list
   </td>
   <td>There can be 0 or more check_node in the check_list, a rule can only exist one check_list, where the logic of the check_node is' and 'is'and', if the type of RuleSet is rule, all check_node of them need to pass before they can continue down, if whitelist is the opposite, that is, check_node all of them do not pass before they can continue down
   </td>
  </tr>
  <tr>
   <td>check_node
   </td>
   <td>check_node is a specific test
   </td>
  </tr>
</table>



##### **6.2.4 alert_data**

Let's take the Decetion example above as an example:

Data to be detected:
```
{
    "data_type":"59",
    "exe":"/usr/bin/nmap",
    "uid":"0"

}
```

RuleSet：
```
<root ruleset_id="test2" ruleset_name="test2" type="rule" undetected_discard="true">
<rule rule_id="detection_test_1" author="EBwill" type="Detection">
   <rule_name>detection_test_1</rule_name>
   <alert_data>True</alert_data>
   <harm_level>high</harm_level>
   <desc affected_target="test">This is a detection test</desc>
   <filter part="data_type">59</filter>
   <check_list>
       <check_node type="INCL" part="exe">nmap</check_node>
   </check_list>
</rule>
</root>
```

If the **alert_data is True** , the RuleSet passes the following data backwards, incrementing **SMITH_ALETR_DATA** fields, including **HIT_DATA** details describing the Hit rule, and **RULE_INFO** , basic information about the rule itself:

```
{
    "SMITH_ALETR_DATA":{
        "HIT_DATA":[
            "test2 exe:[INCL]: nmap"
        ],
        "RULE_INFO":{
            "AffectedTarget":"all",
            "Author":"EBwill",
            "Desc":"This is a detection test",
            "DesignateNode":null,
            "FreqCountField":"",
            "FreqCountType":"",
            "FreqHitReset":false,
            "FreqRange":0,
            "HarmLevel":"high",
            "RuleID":"test2",
            "RuleName":"detection_test_1",
            "RuleType":"Detection",
            "Threshold":""
        }
    },
    "data_type":"59",
    "exe":"/usr/bin/nmap",
    "uid":"0"
}
```

If **alert_data False** , the following data is passed backwards, the original data source:

```
{

    "data_type":"59",

    "exe":"/usr/bin/nmap",

    "uid":"0"

}
```

##### **6.2.5 check_node**

The basic structure of the check_node is as follows:

```
<check_node type="检测类型" part="待检测路径">
   检测内容
</check_node>
```

###### **6.2.5.1 detection type**

The following detection types are currently supported:


<table>
  <tr>
   <td>Type
   </td>
   <td>Description
   </td>
  </tr>
  <tr>
   <td>END
   </td>
   <td>The content in the Path to be detected, to detect the content, end
   </td>
  </tr>
  <tr>
   <td>NCS_END
   </td>
   <td>The content in the Path to be detected, to detect the content, the end, case insensitive
   </td>
  </tr>
  <tr>
   <td>START
   </td>
   <td>The content in the Path to be detected, starting with Detect content
   </td>
  </tr>
  <tr>
   <td>NCS_START
   </td>
   <td>The content in the Path to be detected, starting with detection content, case insensitive
   </td>
  </tr>
  <tr>
   <td>NEND
   </td>
   <td>The content in the Path to be detected does not end with the detected content
   </td>
  </tr>
  <tr>
   <td>NCS_NEND
   </td>
   <td>The content in the Path to be detected does not end with Detected content, case insensitive
   </td>
  </tr>
  <tr>
   <td>NSTART
   </td>
   <td>The content in the Path to be detected does not start with the detected content
   </td>
  </tr>
  <tr>
   <td>NCS_NSTART
   </td>
   <td>The content in the Path to be detected does not start with Detected content
   </td>
  </tr>
  <tr>
   <td>INCL
   </td>
   <td>Content in Path to be detected
   </td>
  </tr>
  <tr>
   <td>NCS_INCL
   </td>
   <td>Content in Path to be detected, exists, detected content, case insensitive
   </td>
  </tr>
  <tr>
   <td>NI
   </td>
   <td>Content in Path to be detected, does not exist, detect content
   </td>
  </tr>
  <tr>
   <td>NCS_NI
   </td>
   <td>Content in Path to be detected, does not exist, detected content, case insensitive
   </td>
  </tr>
  <tr>
   <td>MT
   </td>
   <td>The content in the Path to be detected is greater than
   </td>
  </tr>
  <tr>
   <td>LT
   </td>
   <td>The content in the Path to be detected, less than, the detected content
   </td>
  </tr>
  <tr>
   <td>REGEX
   </td>
   <td>To treat the content in the detection Path, perform regular matching of the detection content
   </td>
  </tr>
  <tr>
   <td>ISNULL
   </td>
   <td>The content in the Path to be detected is empty
   </td>
  </tr>
  <tr>
   <td>NOTNULL
   </td>
   <td>The content in the Path to be detected is not empty
   </td>
  </tr>
  <tr>
   <td>EQU
   </td>
   <td>The content in the Path to be detected is equal to the detected content
   </td>
  </tr>
  <tr>
   <td>NCS_EQU
   </td>
   <td>The content in the Path to be detected is equal to the detected content, case insensitive
   </td>
  </tr>
  <tr>
   <td>NEQ
   </td>
   <td>The content in the Path to be detected is not equal to the detected content
   </td>
  </tr>
  <tr>
   <td>NCS_NEQ
   </td>
   <td>The content in the Path to be detected, is not equal to, detect the content, case insensitive
   </td>
  </tr>
  <tr>
   <td>CUSTOM
   </td>
   <td>For the content in the detection Path, perform, detect the content, specify, custom plug-in detection
   </td>
  </tr>
  <tr>
   <td>CUSTOM_ALLDATA
   </td>
   <td>Customize plug-in detection for the content to be detected; in this way, part can be empty, because it does not depend on this field, the entire data is passed to the plug-in for detection
   </td>
  </tr>
</table>


Next, we explain the use of the next part, which is consistent with the use of the part of the filter.


###### **6.2.5.2 part**

Suppose the data to be detected is:
```
{
    "data":{
        "name":"EBwill",
        "number":100,
        "list":[
            "a1",
            "a2"
        ]
    },
    "class.id":"E-19"
}
```

The corresponding part description is as follows:

```
data               =       "{\"name\":\"EBwill\",\"number\":100,\"list\":[\"a1\",\"a2\"]
data.name          =       "EBwill"
data.number        =       "100"
data.list.#_0      =       "a1"
data.list.#_1      =       "a2"
class\.id          =       "E-19"
```

It should be noted that if there is "." in the key to be detected, it needs to be escaped with "\"


###### **6.2.5.3 Advanced Usage check_data_type**

Suppose the data to be detected is

```
{
    "stdin":"/dev/pts/1",
    "stdout":"/dev/pts/1"
}
```

Assuming we need to detect that **stdin is equal to stdout** , that is, our detection content comes from the data to be detected, then we need to use **check_data_type = "from_ori_data" to redefine the source of the detection content is from the data to be detected rather than the content filled in** , as follows:

```
<check_node type="EQU" part="stdin" check_data_type="from_ori_data">stdout</check_node>
```


###### **6.2.5.4 Advanced Usage logic_type**

Suppose the data to be detected is

```
{
    "data":"test1 test2 test3",
    "size": 96,
}
```

When we need to detect whether there is test1 or test2 in data, we can write regular to achieve, or we can define **logic_type to achieve check_node support "AND" or "OR" logic **, as follows:

```
<!-- Value "test1" or "test2" exist in "data" field -->
<check_node type="INCL" part="data" logic_type="or" separator="|">
    <![CDATA[test1|test2]]>
</check_node>

<!-- Value "test1" or "test2" exist in "data" field  -->
<check_node type="INCL" part="data" logic_type="and" separator="|">
    <![CDATA[test1|test2]]>
</check_node>
```

Among them logic_type is used to describe logical types, support "and" and "or", and separator is used to customize the way to identify cut detection data


###### **6.2.5.5 advanced usage of foreach**

When we need to have more complex detection of arrays, it may be solved by **foreach**.

Suppose the data to be detected is

```
{
    "data_type":"12",
    "data":[
        {
            "name":"a",
            "id":"14"
        },
        {
            "name":"b",
            "id":"98"
        },
        {
            "name":"c",
            "id":"176"
        },
        {
            "name":"d",
            "id":"172"
        }
    ]
}
```

**We want to filter out the obj of the data with id > 100 and the top-level data_type equal to 12**, then we can traverse through foreach first, and then judge the traversed data, as follows:

```
<check_list foreach="d in data">
    <check_node type="MT" part="d.id">100</check_node>
    <check_node type="EQU" part="data_type">12</check_node>
</check_list>
```

Multiple pieces of data are passed downsteam:

```
{
    "data_type":"12",
    "data":[
        {
            "name":"c",
            "id":"176"
        }
    ]
}

#with another output

{
    "data_type":"12",
    "data":[
        {
            "name":"d",
            "id":"172"
        }
    ]
}
```

We can better understand the advanced usage of **foreach** through the following figure


![alt_text](006.png "image_tooltip")


Suppose the data to be detected is

```
{
    "data_type":"12",
    "data":[
        1,
        2,
        3,
        4,
        5,
        6,
        7
    ]
}
```

If we want to filter out the data less than 5 in the data, we need to write it like this:

```
<check_list foreach="d in data">
    <check_node type="LT" part="d">5</check_node>
</check_list>
```

###### **6.2.5.6 Advanced Usage cep**

By default, the relationship between the checknode and the data will be checked out when all the detection conditions of the checknode are met. When you need to customize the relationship between the checknode, you can use cep to solve it.

Suppose the data to be detected is

```
{
    "data_type":"12",
    "comm":"ETNET",
    "node_name":"p23",
    "exe":"bash",
    "argv":"bash"
}
```

We want to **node_name equal to p23 or comm equal to ETNET, and exe and argv equal to bash** , such data is filtered out, as follows:

```
<check_list cep="(a or b) and c">
    <check_node part="comm" group="a" type="INCL" check_data_type="static">ETNET</check_node>
    <check_node part="nodename" group="b" type="INCL" check_data_type="static">p23</check_node>
    <check_node part="exe" group="c" type="INCL" check_data_type="static">bash</check_node>
    <check_node part="argv" group="c" type="INCL" check_data_type="static">bash</check_node>
</check_list>
```

You can declare check_node as a group, and then write cep write conditions for the group in cep. Support **or **and **and **.


##### **6.2.6 Frequency field**

The logic of Frequency check_list, but after the data passes through filter and check_list, if the current rule is of type Frequency, it will enter the special detection logic of Frequency. Frequency has two fields, **node_designate **and **threshold **, as follows:

```
<node_designate>
    <node part="uid"/>
    <node part="pid"/>
</node_designate>
<threshold range="30">5</threshold>
```

###### **6.2.6.1 node_designate**

Where **node_designate** is on behalf of **group_by** , the meaning of the above example is to group_by the two fields uid and pid.


###### **6.2.6.2 threshold**

**threshold is a description of the specific detection content of frequency detection: how many times (range) occurs (threshold).** As expressed in the above example: the same uid and pid appear 5 times within 30 seconds is detected, where the unit of range is seconds.


![alt_text](007.png "image_tooltip")


As shown in the figure above, since it occurs 5 times in only 10s, all data with pid = 10 and uid = 1 that occurs in the remaining 20s will be alerted, as follows:


![alt_text](008.png "image_tooltip")


But this problem can cause too much alarm data, so a parameter called: **hit_reset** parameter called:

```
<node_designate>
    <node part="uid"/>
    <node part="pid"/>
</node_designate>
<threshold range="30" hit_reset="true" >5</threshold>
```

When hit_reset is true, the time window is remastered each time the threshold policy is satisfied, as follows:


![alt_text](009.png "image_tooltip")


In the scene of frequency detection, there is also a problem of performance, because this kind of stateful detection needs to save some intermediate states, this part of the intermediate state data we stored in Redis, but if the amount of data is too large, Redis will have a certain impact, so we also support the use of frequency detection using HUB's own Local Cache to store these intermediate state data, but it will also lose the global, the way to open is to set **local_cache parameter is true **:

```
<node_designate>
    <node part="uid"/>
    <node part="pid"/>
</node_designate>
<threshold range="30" local_cache="true" hit_reset="true" >5</threshold>
```

The reason for the loss of globalization is that the cache only serves the HUB instance it belongs to. If it is in cluster mode, the Local Cache is not shared with each other, but it will bring certain performance improvement.


###### **6.2.6.3 Advanced Usage count_type**

In some cases, we do not want to calculate the frequency to calculate "how many times", but there will be some other requirements, **such as how many classes appear **, **how **much** data appear in the field**,** and how much. **Let's look at the first requirement, how many classes appear.

Suppose the data to be detected is

```
{
    "sip":"10.1.1.1",
    "sport":"6637",
    "dip":"10.2.2.2",
    "dport":"22"
}
```

When we want to write a rule for detecting scanners, we often don't care how many times a IP access other assets, but how many different other assets are accessed. When this data is large, there may be the possibility of network scanning detection. **Within 3600 seconds, the number of different IP accessed by the same IP is recorded if it exceeds 100 **, then his frequency part rule should be written like this:

```
<node_designate>
    <node part="sip"/>
</node_designate>
<threshold range="3600" count_type="classify" count_field="dip">100</threshold>
```

At this time **count_type **needs to be **classify;** **count_field** is the field that the type calculation depends on, that is, dip.

The second scenario assumes that the data to be detected is

```
{
    "sip":"10.1.1.1",
    "qps":1
}
```

Suppose we need to filter out data with a total of qps greater than 1000 in 3600s, then we can write it like this:

```
<node_designate>
    <node part="sip"/>
</node_designate>
<threshold range="3600" count_type="sum" count_field="qps">1000</threshold>
```

By default hub count numbers of data flows when **count_type **is empty. When** classify **is assigned**, the distinct value **is calculated**. **When** **the **sum **is assigned, the **sum of** **values for **appointing** field** will be calculated.


##### **6.2.7 append**

When we want to add some information to the data, we can use append to add data. The syntax of append is as follows:

```
<append type="append类型" rely_part="依赖字段" append_field_name="增加字段名称">增加内容</append>
```
###### **6.2.7.1 append - STATIC**

Suppose the data to be detected is

```
{
    "alert_data":"data"
}
```

Assuming that the data has passed filter/check_list/frequency detection (if any), then we want to add some fixed data to the data, such as: data_type: 10, then we can increase it in the following ways:

```
<append type="static" append_field_name="data_type">10</append>
```

We will get the following data:

```
{
    "alert_data":"data",
    "data_type":"10"
}
```


###### **6.2.7.2 append - FIELD**

Suppose the data to be detected is

```
{
    "alert_data":"data",
    "data_type":"10"
}
```

If we want to add a field to this data: data_type_copy: 10 (from the data_type field in the data), then we can write it as follows:

```
<append type="field" rely_part="data_type" append_field_name="data_type_copy"></append>
```

###### **6.2.7.3 append**

Suppose the data to be detected is

```
{
    "sip":"10.1.1.1",
    "sport":"6637",
    "dip":"10.2.2.2",
    "dport":"22"
}
```

If we want to query the CMDB information of sip through external API, then we cannot achieve it through simple rules in this scenario, and we need to use Plugin to achieve it. The specific writing method of Plugin will be explained below. Here we first introduce if we call custom Plugin in RuleSet, as follows:

```
append type="CUSTOM" rely_part="sip" append_field_name="cmdb_info">AddCMDBInfo</append>
```

Here we will pass the data of the fields in the rely_part to the AddCMDBInfo plugin for data query, and append the plugin return data to cmdb_info data, as follows:

```
{
    "sip":"10.1.1.1",
    "sport":"6637",
    "dip":"10.2.2.2",
    "dport":"22",
    "cmdb_info": AddCMDBInfo(sip) --> The data in cmdb_info is the return data of the plugin AddCMDBInfo(sip)
}
```


###### **6.2.7.4 CUSTOM_ALLORI**

Suppose the data to be detected is

```
{
    "sip":"10.1.1.1",
    "sport":"6637",
    "dip":"10.2.2.2",
    "dport":"22"
}
```

If we want to query the permission relationship between sip and dip through the API of the internal permission system, then we also need to use the plugin to achieve this query, but our imported parameter of the plugin is not unique, we need to pass the complete data to be detected into the plugin, written as follows:

```
<append type="CUSTOM_ALLORI" append_field_name="CONNECT_INFO">AddConnectInfo</append>
```

We can get:

```
{
    "sip":"10.1.1.1",
    "sport":"6637",
    "dip":"10.2.2.2",
    "dport":"22",
    "CONNECT_INFO": AddConnectInfo({"sip":"10.1.1.1","sport":"6637","dip":"10.2.2.2","dport":"22"}) --> CONNECT_INFO中的数据为插件AddConnectInfo的返回数据
}
```


###### **6.2.7.5 GROK**

Append supports grok parsing for the specified field and appends the parsed data to the data stream:

```
<append type="GROK" rely_part="data" append_field_name="data2"><![CDATA[
%{COMMONAPACHELOG}]]></append>
```

The above example will data data for % {COMMONAPACHELOG} after parsing the new data2 field, stored in the parsed data.


###### **6.2.7.6 6.2.7.6 Other**

Append can exist multiple times in a rule, as follows:

```
<rule rule_id="rule_1" type="Detection" author="EBwill">
    ...
    <append type="CUSTOM_ALLORI" append_field_name="CONNECT_INFO">AddConnectInfo</append>
    <append type="field" rely_part="data_type"></append>
    <append type="static" append_field_name="data_type">10</append>
    ...
</rule>
```


##### **6.2.8 del**

When we need to do some clipping of the data, we can use the del field to operate.

Suppose the data to be detected is

```
{
    "sip":"10.1.1.1",
    "sport":"6637",
    "dip":"10.2.2.2",
    "dport":"22",
    "CONNECT_INFO": "false"
}
```

Assuming we need to remove the field CONNECT_INFO, I can write it as follows:

```
<del>CONNECT_INFO</del>
```

The following data can be obtained:

```
{
    "sip":"10.1.1.1",
    "sport":"6637",
    "dip":"10.2.2.2",
    "dport":"22"
}
```

Del can be written multiple times, which need to be separated by ";", as follows:

```
<del>CONNECT_INFO;sport;dport</del>
```

The following data can be obtained:

```
{
    "sip":"10.1.1.1",
    "dip":"10.2.2.2"
}
```


##### **6.2.9 modify**

When we need to process complex data, append and del cannot meet the needs, such as flattening the data, changing the key of the data, etc. At this time, we can use modify to operate. It should be noted that modify only supports plugins. The usage method is as follows:

```
<modify>plugin_name_no_space</modify>
```

The process is as follows:


![alt_text](010.png "image_tooltip")



##### **6.2.10 Action**

When we need to do some special operations, such as linkage with other systems, send alarms to DingTalk/Lark/mail, linkage WAF Ban IP and other operations, we can use Action to achieve related operations. It should be noted that only plugins are supported. The usage method is as follows:

```
<action>emailtosec</action>
```

The input data of the plugin emailtosec is the current data, and other operations can be written as required.

Action also supports multiple plugins. The usage method is as follows, and you need to press ";" to separate them:

```
<action>emailtosec1;emailtosec2</action>
```

In the above example, both emailtosec1 and emailtosec2 will be triggered to run.


#### **6.3 Detection/Execution Sequence**


![alt_text](011.png "image_tooltip")


It should be noted that the data is dynamic in the process of passing the Rule, that is, if it passes the append, then the next data received by the del is the data after the append takes effect.


##### **6.3.1 The relationship between Rules**

For the relationship where Rule is "OR" in the same RuleSet, suppose the RuleSet is as follows:

```
<root ruleset_id="test2" ruleset_name="test2" type="rule" undetected_discard="true">
<rule rule_id="detection_test_1" author="EBwill" type="Detection">
   <rule_name>detection_test_1</rule_name>
   <alert_data>True</alert_data>
   <harm_level>high</harm_level>
   <desc affected_target="test">This is a Detection test 1</desc>
   <filter part="data_type">59</filter>
   <check_list>
       <check_node type="INCL" part="exe">redis</check_node>
   </check_list>
</rule>
<rule rule_id="detection_test_2" author="EBwill" type="Detection">
   <rule_name>detection_test_2</rule_name>
   <alert_data>True</alert_data>
   <harm_level>high</harm_level>
   <desc affected_target="test">This is a Detection test 2</desc>
   <filter part="data_type">59</filter>
   <check_list>
       <check_node type="INCL" part="exe">mysql</check_node>
   </check_list>
</rule>
</root>
```

Assuming that the exe field of the data is mysql-redis, it will be detection_test_1 detection_test_2 will be triggered and two data will be passed backwards, which belong to the two rules


#### **6.4 More examples**

```
<rule rule_id="critical_reverse_shell_rlang_black" author="lez" type="Detection">
    <rule_name>critical_reverse_shell_rlang_black</rule_name>
    <alert_data>True</alert_data>
    <harm_level>high</harm_level>
    <desc kill_chain_id="critical" affected_target="host_process">There may be behavior that creates an R reverse shell</desc>
    <filter part="data_type">42</filter>
    <check_list>
        <check_node type="INCL" part="exe">
            <![CDATA[exec/R]]>
        </check_node>
        <check_node type="REGEX" part="argv">
            <![CDATA[(?:\bsystem\b|\bshell\b|readLines.*pipe.*readLines|readLines.*writeLines)]]>
        </check_node>
    </check_list>
    <node_designate>
    </node_designate>
    <del />    
    <action />
    <alert_email />
    <append append_field_name="" rely_part="" type="none" />
</rule>
```

```
<rule rule_id="init_attack_network_tools_freq_black" author="lez" type="Frequency">
    <rule_name>init_attack_network_tools_freq_black</rule_name>
    <freq_black_data>True</freq_black_data>
    <harm_level>medium</harm_level>
    <desc kill_chain_id="init_attack" affected_target="service">Multiple use of network attack tools, possible man-in-the-middle/network spoofing</desc>
    <filter part="SMITH_ALETR_DATA.RULE_INFO.RuleID">init_attack_network</filter>
    <check_list>
    </check_list>
    <node_designate>
        <node part="agent_id" />
        <node part="pgid" />
    </node_designate>
    <threshold range="30" local_cache="true" count_type="classify" count_field="argv">3</threshold>
    <del />
    <action />
    <alert_email />
    <append append_field_name="" rely_part="" type="none" />
</rule>
```

```
<rule rule_id="tip_add_info_01" type="Detection" author="yaopengbo">
    <rule_name>tip_add_info_01</rule_name>
    <harm_level>info</harm_level>
    <threshold/>
    <node_designate/>
    <filter part="data_type">601</filter>
    <check_list>
        <check_node part="query" type="CUSTOM">NotLocalDomain</check_node>
    </check_list>
    <alert_data>False</alert_data>
    <append type="FIELD" rely_part="query" append_field_name="tip_data"></append>
    <append type="static" append_field_name="tip_type">3</append>
    <append type="CUSTOM_ALLORI" append_field_name="tip_info">AddTipInfo</append>
    <del/>
    <alert_email/>
    <action/>
<desc affected_target="tip">DNS added domain name with threat intel information</rule>
```

#### **6.5 Suggestions for rule writing**



* Good use of filter can greatly reduce performance pressure, the goal of filter writing should be to let as little data as possible into the CheckList
* Use as little regularity as possible


## **7 Elkeid HUB Plugin/Plugin**

Elkeid HUB Plugin is used to remove some restrictions of Ruleset in the writing process and improve the flexibility of HUB use. By writing plugins, you can achieve some operations that cannot be done by writing Ruleset. At the same time, if you need to interact with third-party components that are not currently supported, you can only do so by writing plugins.

Elkeid HUB currently supports both Golang Golang Plugin and Python Plugin. The current stock Plugin is developed with Golang developed with Golang and loaded through the Golang Golang Plugin mechanism. Due to limitations, it is no longer open to the public, but it can still be used in the preparation of Ruleset Golang Plugin. Currently only open to the public Python Plugin.

Python The essence of the Plugin is to execute the Python Python script through another process while the HUB is running, and return the execution result to the Elkeid HUB.

Plugin has a total of 6 types, all of which are introduced in the doc written in Ruleset. The following will introduce each plugin in combination with the above examples. The type name of Plugin does not correspond to the tag name in Ruleset one by one. In actual use, please strictly follow the doc.


### **7.1 Introduction of common parameter**


##### **7.1.1 Format**

Each Plugin is a Python Class. When the plugin is loaded, HUB will instantiate this Class and assign the name, type, log, redis four variables. Each time the plugin is executed, the plugin_exec method of the class will be called.

Classes are as follows:

```
class Plugin(object):

    def __init__(self):
        self.name = ''
        self.type = ''
        self.log = None
        self.redis = None
    
    def plugin_exec(self, arg, config):
        pass
```


##### **7.1.2 init**

__init__ method contains the following four variables:



* name: Plugin Name
* type: Plugin Type
* log: logging
* redis: redis client

If you have your own init logic, you can add it at the end


##### **7.1.3 plugin_exec**

plugin_exec aspect has two parameters, arg and config.



* Arg is the parameter that the plugin accepts when executing. Depending on the plugin type, arg is string or dict ().

For Action, Modify, Origin, OriginAppend four types of plugins, arg is dict () dict () .

For Append, Custom has two types of plugins, arg is string.



* Config is an additional parameter that the plugin can accept. Currently only Action and Modify support it. If it is specified in Ruleset, it will be passed to the plugin through the config parameter.

For example: add extra tag in ruleset, HUB will call plugin_exec method with config imported parameter in the form of dict. Extra uses : as kv the delimiter of ; as the delimiter of each group of kv

```
<action extra="mail:xxx@bytedance.com;foo:bar">PushMsgToMatao</action>
```

```
config = {"mail":"xxx@bytedance.com"}
```


### **7.2 example**


##### **7.2.1 Plugin之Action**

See 6.2.10 for the role in rule.

Action is used to perform some additional operations after the data passes through the current rule.

An Action plugin receives a copy of the entire data stream. Returns whether the action was successfully executed. Whether the action is successfully executed does not affect whether the data flow continues to go down, it will only be reflected in the HUB's log.

Implementation Reference

```
class Plugin(object):


    def __init__(self):
        self.name = None
        self.type = None
        self.log = None
        self.redis = None


    def plugin_exec(self, arg, config):
        # Example: request a callback address
        requests.post(xxx)
        result = dict()
        result["done"] = True
        return result
```

##### **7.2.2 Append of Plugin of Plugin**

For the role of rule, see 6.2.7.3

Append and OriginAppend are similar in that both Append operations can be customized. The difference is that Append accepts a certain attribute value determined in the data stream, while OriginAppend accepts a copy of the entire data stream. The return value of both will be written to the specified attribute in the data stream.

implementation reference

```
class Plugin(object):
    def __init__(self):
        self.name = None
        self.type = None
        self.log = None
        self.redis = None
    def plugin_exec(self, arg, config):
        result = dict()
        result["flag"] = True
        # Add the __new__ suffix after the original arg
        result["msg"] = arg + "__new__"
        return result
```


##### **7.2.3 Custom of Plugin of Plugin**

For the role of rule, see Custom in 6.2.5.2.

CUSTOM is used to implement custom CheckNode. Although more than 10 common judgment methods are predefined in CheckNode, they cannot be completely covered in the actual rule writing process, so the plugin is opened to have more flexible judgment logic.

The parameter received by the plugin is the property value specified in the data stream, and the return is whether to Hit and write the part in the hit.

implementation reference

```
class Plugin(object):
    def __init__(self):
        self.name = None
        self.type = None
        self.log = None
        self.redis = None
    def plugin_exec(self, arg, config):
        result = dict()
        # If the length of arg is 10
        if arg.length() == 10:
            result["flag"] = True
            result["msg"] = arg
        else:
            result["flag"] = True
            result["msg"] = arg
        return result
```


##### **7.2.4 Modify the Plugin the Plugin**

Role in rule see 6.2.9

Modify is the most flexible plugin of all plugins. When writing ruleset or other plugins cannot meet the needs, you can use the modify plugin to obtain full manipulation of data flow.

The imported parameter of the Modify plugin is a piece of data in the current data stream. The return is divided into two cases, which can return a single piece of data or multiple pieces of data.

When returning a single piece of data, Flag is true, the data is in Msg, when returning multiple pieces of data, MultipleDataFlag is true, and the data is in the array MultipleData. If both Flag and MultipleDataFlag are true, it is meaningless.

Implementation reference 1:

```
class Plugin(object):
    def __init__(self):
        self.name = None
        self.type = None
        self.log = None
        self.redis = None
    def plugin_exec(self, arg, config):
        result = dict()
        # Modify the data at will, such as adding a field
        arg["x.y"] = ["y.z"]
        result["flag"] = True
        result["msg"] = arg
        return result
```

Implementation reference 2:

```
class Plugin(object):
    def __init__(self):
        self.name = None
        self.type = None
        self.log = None
        self.redis = None
    def plugin_exec(self, arg, config):
        result = dict()
        # Copy the piece of data into 5 points
        args = []
        args.append(arg)
        args.append(arg)
        args.append(arg)
        args.append(arg)
        args.append(arg)
        result["multiple_data_flag"] = True
        result["multiple_data"] = args
        return result
```


##### **2.5 Origin of the Plugin of the Plugin**

For the role of rule, see 6.2.5.2 CUSTOM_ALLORI

The advanced version of the Custom plug-in, instead of checking a field in the data stream, checks the entire data stream. The imported parameter changes from a single field to the entire data stream.

implementation reference

```
class Plugin(object):
    def __init__(self):
        self.name = None
        self.type = None
        self.log = None
        self.redis = None
    def plugin_exec(self, arg, config):
        result = dict()
        # If the length of arg["a"] and arg["b"] are both 10
        if arg["a"].length() == 10 and arg["b"].length() == 10:
            result["flag"] = True
            result["msg"] = ""
        else:
            result["flag"] = False
            result["msg"] = ""
        return result
```

##### **7.2.6 Plugin之OriginAppend**

For the role of rule, see 6.2.7.4

The advanced version of the Append plug-in no longer judges a field in the data stream and appends, but judges the entire data in the data stream. The imported parameter becomes the entire data stream from a single field.

implementation reference

```
class Plugin(object):
    def __init__(self):
        self.name = None
        self.type = None
        self.log = None
        self.redis = None
    def plugin_exec(self, arg, config):
        result = dict()
        result["flag"] = True
        # merge two fields
        result["msg"] = arg["a"] + "__" + arg["b"]
        return result

```


### **7.3 Plugin development process**

The runtime environment of the plugin is pypy3.7-v7.3.5-linux64, if you want python scripts to run normally, you need to test in this environment.

HUB itself introduces some basic dependencies, but it is far from covering python common packages. When necessary, users need to install them by themselves in the following ways.



1. Venv is located under/opt/Elkeid_HUB/plugin/output/pypy, you can switch to venv with the following command and execute pip install to install.

```
source /opt/Elkeid_HUB/plugin/output/pypy/bin/activate
```

2. Call pip module in the plugin's init method pip module in the plugin's init method


##### **7.3.1 Creating a Plugin**



1. Click the Create plugin button


![alt_text](012.png "image_tooltip")




2. Fill in the information as required


![alt_text](013.png "image_tooltip")




3. Click Confirm to complete the creation


![alt_text](014.png "image_tooltip")




4. View Plugin


![alt_text](015.png "image_tooltip")




5. Download plugin

When the Plugin is successfully created, the Plugin will be automatically downloaded, and then you can also click the Download button on the interface to download again


![alt_text](016.png "image_tooltip")



##### **7.3.2 Online Development & Testing Plugin**

Click Name or click the View Plugin button to bring up Plugin.py preview screen where you can preview & edit the code.

The editor is in read-only mode by default. Click the Edit button, the editor will switch to read-write mode, and the Plugin can be edited at this time.


![alt_text](017.png "image_tooltip")


After editing, you can click the Confirm button to save, or click the Cancel button to discard the changes.

After clicking the Confirm button, the changes will not take effect in real time. Similar to Ruleset, the Publish operation is also required.


##### **7.3.3 Local Development Plugin**

Unzip the automatically downloaded zip package when creating the plugin, you can use IDE Open, execute test.py to test the plugin.

After the test is correct, you need to manually compress the zip file for uploading.

Pay attention when compressing, make sure all files are in the root directory of zip.


![alt_text](018.png "image_tooltip")



##### **7.3.4 Uploading the Plugin**



1. Click the Upload button in the interface


![alt_text](019.png "image_tooltip")




1. Same as policy release, publish the policy in the policy release interface


### **7.4 Common development dependencies of Plugin**


##### **7.4.1 requests**

Elkeid HUB introduces the requests library by default, which can be used to implement http requests.

The reference code is as follows:

```
import requests
import json
def __init__(self):
    ...
    
def plugin_exec(self, arg, config):
    p_data = {'username':user_name,'password':user_password}    
    p_headers = {'Content-Type': 'application/json'}
    r = requests.post("http://x.x.x.x/", data=json.dumps(p_data), headers=p_headers)
    result["flag"] = True
    result["msg"] = r.json()['data']
    return result
```


##### **7.4.2Redis**

Plugin Object After executing __init__ method, before executing plugin_exec method, HUB will set the redis connection to the self.redis, and then you can call redis in the plugin_exec method. The redis is the redis configured by HUB itself, and the library used is https://github.com/redis/redis-py.

The reference code is as follows:

```
redis_result = self.redis.get(redis_key_prefix + arg)

self.redis.set(redis_key_prefix + arg, json.dumps(xxx), ex=random_ttl())
```


##### **7.4.3Cache**

Elkeid HUB introduces the cacheout library by default, you can use the cacheout library to achieve local cache, or with redis to achieve multi-level cache. cacheout doc reference https://pypi.org/project/cacheout/.

Simple example:

```
from cacheout import LRUCache
class Plugin(object):
    def __init__(self):
        ...
        self.cache = LRUCache(maxsize=1024 * 1024)
        ...
        
    def plugin_exec(self, arg, config):
        ...
        cache_result = self.cache.get(arg)
        if cache_result is None:
           pass
        ...
        self.cache.set(arg, query_result, ttl=3600)
        ...
```
Cooperate with redis to achieve multi-level cache:

```
from cacheout import LRUCache
class Plugin(object):
    def __init__(self):
        ...
        self.cache = LRUCache(maxsize=1024 * 1024)
        ...
        
    def plugin_exec(self, arg, config):
        ...
        cache_result = self.cache.get(arg)
        if cache_result is None:
            redis_result = self.redis.get(redis_key_prefix + arg)
            if redis_result is None:
                # fetch by api
                ...
                self.redis.set(prefix + arg, json.dumps(api_ret), ex=random_ttl())
                self.cache.set(arg, ioc_query_source, ttl=3600)
            else:
                # return
                ...
        else:
            # return
            ...
```

## **8 Project/Project**


### **8.1 Project**

Project is the smallest unit of the executed policy, which mainly describes the data process in the data flow. From the beginning of Input to the end of Output or RuleSet, let's look at an example:

```
INPUT.hids --> RULESET.critacal_rule
RULESET.critacal_rule --> RULESET.whitelist
RULESET.whitelist --> RULESET.block_some
RULESET.whitelist --> OUTPUT.hids_alert_es
```


![alt_text](020.png "image_tooltip")


Let's describe the configuration of this Project:

INPUT.hids consume data remotely and pass it to RULESET.critacal _rule

RULESET.critacal _rule the detected data to the RULESET.whitelist

RULESET.whitelist the detected data to RULESET.block _some and OUTPUT.hids _alert_es

RULESET.block _some may be to perform some blocking operations through action linkage with other components, OUTPUT.hids _alert_es is obviously to send data to the external es


### **8.2 About ElkeidDSL syntax**

There are several concepts in HUB:

| Name/Operator | Desc               | SmithDSL          | Example               |
|---------------|--------------------|-------------------|-----------------------|
| INPUT         | Data input source  | INPUT.inputID     | INPUT.test1           |
| OUTPUT        | Data output source | OUTPUT.outputID   | OUTPUT.test2          |
| RULESET       | Ruleset            | RULESET.rulesetID | RULESET.test3         |
| —>            | Data Pipline       | —>                | INPUT.A1 —> RULESET.A |



### **8.3 About data transfer**

Data transfer can use: -- > to indicate.

If we want to pass the data input source HTTP_LOG to the rule set HTTP:

```
INPUT.HTTP_LOG --> RULESET.HTTP
```

If we want the above alarm to be output SOC_KAFKA data output source:

```
INPUT.HTTP_LOG --> RULESET.HTTP
RULESET.HTTP --> OUTPUT.SOC_KAFKA
```

If we want the above alarms to be SOC_KAFKA and SOC_ES data output source:

```
INPUT.HTTP_LOG --> RULESET.HTTP
RULESET.HTTP --> OUTPUT.SOC_KAFKA
RULESET.HTTP --> OUTPUT.SOC_ES
```

## **9 Elkeid HUB Front End User Guide**

The front end mainly includes five parts: Home, RuleEdit (rule page), Publish (rule publishing), Status (log/status), User Management (system management), Debug (rule testing). This part only introduces the use of the front end page, specific rule configuration and field meaning, please refer to the previous chapters.RuleEdit (rule page), Publish (rule publishing), Status (log/status), User Management (system management), Debug (rule testing)


### **9.1 Usage process**



1. Rules release:
2.   Go to the **Rules page** -- > **Input Source/Output/Rule Set/Plugin/Item** to make relevant edits and modifications. \
     Go to the **Rule Publishing**-- > **Rule Publishing** page to publish the rule to the hub cluster.
1. **Project operation**:
2.   Go to the **rule publishing** -- > **project operation** page start/stop/restart corresponding to the project.


### **9.2 Home**


![alt_text](021.png "image_tooltip")


The home page mainly includes **HUB status information **, **QPS information **, **HUB occupancy information **, **toolbar **. Toolbar includes Chinese and English switching, page mode switching and notification bar information.


![alt_text](022.png "image_tooltip")


QPS The information shows the overall qps information of Input and Output, and the data is updated every 30 seconds. This is only displayed as a global display. If you need to view more detailed information, you can go to the rule page -- > project -- > project details page to view.


![alt_text](023.png "image_tooltip")


The HUB occupancy information analyzes the HUB occupancy by analyzing the CPU time used by the ruleset, and gives a bar graph of the HUB occupancy information, including the CPU time and proportion used by the rule set.


### **9.3 Rule Edit/Rule Page**

All rules (including Input/Output/Ruleset/Plugin/Project) are added, deleted, and modified in RuleEdit.

The edited rules here are not automatically published to the HUB cluster. If you need to publish, please go to the Publish-- > RulePublish page to operate.

**In order to quickly find their own related configurations, the configuration list will be divided into two tabs, My Subscription shows the user's favorite configuration information, and the other shows all the configurations (such as input). Users can go to All Configurations first to find the configuration they need to manage and bookmark the configuration for the next modification.**


#### **9.3.1 Input/Input Sources**


![alt_text](024.png "image_tooltip")


The input source page supports adding and importing files:



1. Add: Click Add, the following page will appear, the specific field meaning can refer to the above **Elkeid Input **section.


![alt_text](025.png "image_tooltip")




1. File import: First create an input file according to your needs, which currently supports yml format. Examples are as follows.

```
InputID: test_for_example
InputName: test_for_example
InputType: kafka
DataType: json
TTL: 30
KafkaBootstrapServers: test1.com:9092,test2.com:9092
KafkaGroupId: hub-01
KafkaOffsetReset: latest
KafkaCompression: none
KafkaWorkerSize: 3
KafkaOtherConf: ~

KafkaTopics:
  - testtopic
```

Then click Import, select the file to be imported, and then confirm the import after the pop-up box.


![alt_text](026.png "image_tooltip")




1. sampling

Click Sample to get the sampled data during the operation of the input source.


![alt_text](027.png "image_tooltip")



![alt_text](028.png "image_tooltip")



#### **9.3.2 Output/Output**

The use of the output is similar to the input source, supporting elasticsearch , kafka , influxdb three types.


![alt_text](029.png "image_tooltip")



#### **9.3.3 RuleSet/Rule Set**



1. ruleset page

Similarly, the rule set also supports page addition and file import, and also supports full export of all rules.


![alt_text](030.png "image_tooltip")


**Sample **Button to view the input/output sample data for this rule (if the rule has no data coming in, there will be no data).

[Test](https://bytedance.feishu.cn/docs/doccnRifPBdLL8Z2xyHawARqFGb#k9hm3b)<span style="text-decoration:underline;"> </span>will test the **non-encrypted **rule set, take the test data as input, and record the Hit profile after the data flows into the rule set. If you choose **Coloring Rule **, then the specific data of Hit will be recorded. ( **There is load on the database. It is recommended to consider the number and size of test data **). If the rule set is running, you can use **Load Data **Load Sample Data and Test. See Rule Testing/Debug page for details


![alt_text](031.png "image_tooltip")


**Create copy **The button creates a replica set of rules using the current ruleset as a template, with the suffix rulesetid and rulesename _copy:


![alt_text](032.png "image_tooltip")


**Search within rule set **Provides a global search for all rule sets. Matches the rule ID corresponding to all rule sets. Users can jump to edit or delete the rule if the search results.


![alt_text](033.png "image_tooltip")




1. rules page

Click the rule set ID **rule set ID **button to view its details and enter the rule edit page.


![alt_text](034.png "image_tooltip")



![alt_text](035.png "image_tooltip")


**New **button is to add a rule to the current rule set. Here support **XML editing **and **table editing **two ways, by clicking **form editing **and **XML editing **to switch.


![alt_text](036.png "image_tooltip")



![alt_text](037.png "image_tooltip")


**Test **The button supports testing a single rule, the sample button can import sample data from the Hub (if any), click execute, and the sample data will be sent to the Hub instance for testing. Testing does not affect the online data flow.


![alt_text](038.png "image_tooltip")



#### **9.3.4 Plugins/Plugins**

For details, see 7.3 Plugin Development Process


#### **9.3.5 Project/Project**

**project **Page addition and file import are also supported. Running/Stopped/Unknown represents the number of machines running/not running/unknown for the project, respectively. In particular, the status data is updated every 30s.


![alt_text](039.png "image_tooltip")


Click on the **project ID **Go to the project details page. You can view the project details, Input lag (only kafka ), the qps information of each component qps information. At the same time, right-click on the node in the node graph to view the node SampleData or jump to the node details.


![alt_text](040.png "image_tooltip")


**[Test](https://bytedance.feishu.cn/docs/doccnRifPBdLL8Z2xyHawARqFGb#k9hm3b)<span style="text-decoration:underline;"> </span>**The button will test the project that does not contain the encrypted rule set, and the test process is the same as the rule set test.


![alt_text](041.png "image_tooltip")



### **9.4 Publish/Rules**

All operations involving changes to the hub cluster are under this page.


#### **9.4.1 RulePublish/Rule Publishing**

Rules are published here, and the edited rule change operation can be seen on this page.

**Commit the changes **, publish the changes to the HUB cluster; **undo the changes **, discard all changes, and roll back the rule to the previous stable version (the version where the changes were last committed).


![alt_text](042.png "image_tooltip")


Click on **diff **to see details of the change


![alt_text](043.png "image_tooltip")


After submitting the changes, it will automatically jump to the Task Detail page. You can view the number of successful and failed machines, failed error messages, and the change details and diff of this task task .


![alt_text](044.png "image_tooltip")



#### **9.4.2 Project Operation/Project Operation**

This page is used to control the start, stop and restart of projects. All new projects are stopped by default and need to be manually opened on this page.


![alt_text](045.png "image_tooltip")



#### **9.4.3 Task/Task List**

The task list page shows all the tasks that have been assigned to the hub cluster.


![alt_text](046.png "image_tooltip")



### **9.5 Status/Status Page**

Status is used to display the running status of the HUB, error events and leader operation records.


#### **9.5.1 Event/HUB event**

Event is the error information generated by the HUB. The leader collects the error information and aggregates it, so each information may be an error that occurred jointly by multiple hub machines over a period of time. You can see the event level, number of hosts, location and information in the list. You can filter by time and Event type at the top. Click the small arrow on the left to expand and view the error details.


![alt_text](047.png "image_tooltip")


Each error message contains details of the error, trace, and the hub machine's ip : port.


#### **9.5.3 Log/operation log**

Log is used to record the modification of the HUB. Log contains URL, operation user, IP, time and other information, which can be filtered by time above.


![alt_text](048.png "image_tooltip")



### **9.6 System Management/System Administration**

This page is used to manage HUB users. Users can create new users, delete users, and manage user rights


#### **9.6.1 User Management**


![alt_text](049.png "image_tooltip")


Click Add User to create a new user, set the user's username, password, and user level in the interface, the user level is divided into 6 levels, namely admin , manager , hub readwirte , hub readonly .



* **admin **Users can access all pages and interfaces
* **Manager  **Users can access pages and interfaces other than user manager
* **hub readwrite  **Users can use normal pages and interfaces related to the hub readwrite permissions
* **hub readonly  **Users can use normal hub readonly pages and interfaces


### **9.8 Debug/Rule Testing**

It is used to test the already written **rules **/ **rule sets **/ **projects **to test whether its function is as expected.


![alt_text](050.png "image_tooltip")


DataSource, Debug Config, and Debug Task are associated as follows:

Each **configuration **contains a copy of **data **, and a test component (rule, ruleset, or project). **Configuration **creates **task **assigns it a Host, **the task **is executed, it is executed only on that Host.


![alt_text](051.png "image_tooltip")



#### **9.8.1 Data Source/Data**

Data source, can be understood as a type of configurable, limit the number of data consumption **input source **.


![alt_text](052.png "image_tooltip")



![alt_text](053.png "image_tooltip")




* types : Data source types, there are two types:
  * debug_user_input (custom) : User input data source;
  * debug_topic (streaming) : Actual input source, this type of data is limited to consume 50 input sources.
* Associated configuration : Associated configuration list, showing the Debug Config using the data source Debug Config
* Associated input source : Represents the input source represented by this data source, only if the type is debug_topic is not empty.


#### **9.8.2 Debug Config/Configuration**


![alt_text](054.png "image_tooltip")


Field description:



* type : Configuration type, indicating which test component the configuration was created based on
* Coloring rule : Represents the rule node of "coloring". After selecting the rule that needs to be "coloring", the data passing through this rule will be marked with coloring fields. You can not select it, at this time, the **configuration **The generated **task **will not collect specific data.
* Status : Configuration status:
  * All configured Ready to complete, now you can create a task
  * Unconfirmed Data may not be configured **Data **or **data **deleted, need to create **data **to create **data**
  * test Profile, no coloring rule configured, you can create a task at this time, but will not collect specific data, only see the profile data of each node (input/ruleset/output), such as In/Out (the number of data flowing into the rule, the number of data flowing out of the rule).


#### **9.8.3 Debug Task/Task**


![alt_text](055.png "image_tooltip")


Field description:



* Task Status: Status
  * undefined : Undefined, the task may be deleted due to hub upgrade or exit, and the result cannot be viewed at this time
  * Ready : Ready, click Start Task to execute the task
  * Running : Running
  * Completed : Run successfully, click **View Results **to view results

Result page:


![alt_text](056.png "image_tooltip")




* Top left: DSL Figure. It is convenient to view the project structure of the test, and the task is ID
* Bottom left: Overview of the results. Shows the inflow/outflow of data from each node.
  * In : In number of data
  * Out Number of Data Outflows
  * LabelIn : Coloring Data LabelIn Number
  * LabelOut : Coloring Data LabelOut Jump
* Right: detail result. You can view the coloring data of this task and support paging query
