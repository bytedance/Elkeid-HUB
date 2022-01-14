English | [简体中文](README-zh_CN.md)

# Elkeid HUB
Elkeid HUB is a rule/event processing engine maintained by the Elkeid Team that supports streaming/offline (not yet supported by the community edition) data processing. The original intention is to solve complex data/event processing and external system linkage requirements through standardized rules.

## Core Components
* `INPUT` data input layer, community edition only supports Kafka.
* `RULEENGINE/RULESET` core components for data detection/external data linkage/data processing.
* `OUTPUT` data output layer, community edition only supports Kafka/ES.
* `SMITH_DSL` used to describe the data flow relationship.


## Application Scenarios

* Simple HIDS
<img src="example_hids.png"/>

* IDS Like Scenarios
<img src="example_ids.png"/>

* Multiple input and output scenarios
<img src="example_complex.png"/>


## Advantage
* High Performance
* Very Few Dependencies
* Support Complex Data Processing
* Custom Plugin Support
* Support Stateful Logic Build
* Support External System/Data Linkage

## Elkeid Internal Best Practices
* Use Elkeid HUB to process Elkeid HIDS/RASP/Sandbox/etc. raw data, TPS ninety million/s. HUB scheduling instance 4000+
* 99% alarm produce time is less than 0.5s
* Internal Maintenance Rules 2000+


## Getting Started
waiting for update

## Elkeid HUB Handbook (chinese only)
[Handbook](handbook/handbook.md)

## Community Version
* Does not support cluster mode, only supports single node.
* No front-end support, no data visualization capabilities, no front-end management capabilities.
* Rule/RuleSet/Project Debug capabilities are not supported.
* WorkSpace is not supported, user management is not supported.
* No operation and maintenance management capabilities.

## LICENSE (Not Business Friendly)
[LICENSE](LICENSE)

## Contact us && Cooperation
<img src="./Lark.png" width="40%" style="float:left;"/>