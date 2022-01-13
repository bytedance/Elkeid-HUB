[English](README.md) | 简体中文
# Elkeid HUB
Elkeid HUB 是一款由 Elkeid Team 维护的事规则/事件处理引擎，支持流式/离线(社区版尚未支持)数据处理。 初衷是通过标准化的抽象语法/规则来解决复杂的数据/事件处理与外部系统联动需求。

## Core Components
* `INPUT` 数据输入层，社区版仅支持Kafka
* `RULEENGINE/RULESET` 对数据进行检测/外部数据联动/数据处理的核心组件
* `OUTPUT` 数据输出层，社区版仅支持Kafka/ES
* `SMITH_DSL` 用来描述数据流转关系


## Application Scenarios

* Simple HIDS
<img src="example_hids.png"/>

* IDS Like Scenarios
<img src="example_ids.png"/>

* Multiple input and output scenarios
<img src="example_complex.png"/>


## Advantage
* 高性能
* 依赖极少
* 支持复杂数据处理
* 插件支持
* 支持有状态逻辑
* 支持外部系统/数据联动

## Elkeid Internal Best Practices
* 使用 Elkeid HUB 处理 Elkeid HIDS/RASP/Sandbox 原始数据，TPS 9千万/秒。HUB 调度实例 4000+
* 99% 告警产生时间 < 0.5s
* 内部维护策略2000+

## Community Version
* 不支持集群模式，仅支持单节点
* 没有前端支持，不支持数据可视化能力，不支持前端管理能力
* 不支持 Rule/RuleSet/Project Debug 能力
* 不支持 WorkSpace，不支持用户管理
* 无运维管理能力

## Install and deploy
waiting for update

## Getting Started
waiting for update

## Elkeid HUB Handbook (chinese only)
waiting for update

## LICENSE (Not Business Friendly)
[LICENSE](LICENSE)

## Contact us && Cooperation
<img src="./Lark.png" width="40%" style="float:left;"/>