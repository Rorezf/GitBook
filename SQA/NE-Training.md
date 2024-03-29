# 培训笔记

## 文档分析

### 流程

1. 策划提交需求文档
2. QA进行文档分析
3. QA发送分析报告
4. 策划修改并反馈
5. QA确认修改内容
6. 提交程序进行开发
7. 注意摆正态度

### 原则

1. 正确性：是否满足用户需求，方案是否达到设计目的
2. 必要性：新需求是否有用
3. 完整性：需求是否无遗漏，与用户需求逐一对应
4. 一致性：新内容与旧内容是否矛盾，矛盾处理是否合理，矛盾处是否有提示说明
5. 可行性：需求在现阶段的资源和技术下是否可实现
6. 明确性：任一需求是否都可被测试，结果是否可被预测

### 基本

1. 歧义：各人对需求说明是否可能产生不同理解

2. 关联系统：是否对已有系统产生影响、冲突

3. 时序逻辑问题

4. 数值平衡问题：

   > 合理性：各种数值在整体规划中是否合理
   >
   > 合法性：异常、极限、边界数值是否考虑得当

5. 人文常识的合理性

6. 错别字&笔误：尤其是界面上显示的文案

### 进阶

1. 确认文档的策划目的

   > 1. 需求是否达到目的
   > 2. 三段式检查：为了......（用户需求）通过......（方法）以达到......（目的）

2. 建议

   > 1. 改良性：不影响现有方案，对某些点进行优化
   > 2. 创新性：可能否定原有方案，抛砖引玉提出（需要先经过深思熟虑，提供相关证据再提出）

3. 站在用户的立场

   > 1. 新方案是否有需要
   > 2. 方案是否能迎合用户需求
   > 3. 主观认为用户苛求、直接、浮躁

4. 为程序员考虑

   > 1. 实现的难度
   > 2. 功能是否可扩展
   > 3. 策划的需求是否足够明确

---

## 测试用例

### 测试点

1. 编写步骤

   > 1. 仔细分析策划文档
   > 2. 拆分系统为多个模块
   > 3. 根据流程和逻辑，拆分至内容可以被验证的层级
   > 4. 覆盖所有正常操作
   > 5. 思考异常情况，考虑破坏性测试点

2. 寻找测试点

   > 1. 整体 -> 模块 -> 单元 -> 逻辑
   > 2. 通过内容的划分来寻找
   > 3. 通过流程的递进来寻找

3. 层次划分

   > 1. 校验功能：覆盖策划文档所有需求
   > 2. 用户情景：使用过程中可能遇到的问题
   > 3. 内部构造：根据实现方式寻找测试点，代码层面的处理
   
4. 保证测试点齐全

   > 1. 划分：列举划分（功能A，功能B....），步骤划分（步骤A，步骤B......）
   >
   > 2. 细化：
   >
   >    > 1. 覆盖所有分支
   >    > 2. 等价边界（公示考虑上下限）
   >
   > 3. 推测：
   >
   >    > 1. 程序角度：数据的存储方式，逻辑的实现
   >    > 2. 用户角度

5. 常见问题

   > 1. 客户端：请求的参数可能被修改，重要数据和资源必须经服务器校验
   > 2. 先扣后给：考虑响应时间
   > 3. 二次确认：确认前后的确认条件一致

### 设计用例

1. 三个要素：

   > 1. 验证目标（测试点）
   > 2. 条件：输入，操作步骤
   > 3. 预期结果：可被验证

2. 形成：

   > 1. 等价划分：将所有可能的输入划分为若干个等价级别
   > 2. 边界值分析：确定边界的情况，设定特定验证值
   > 3. 错误推测：根据经验和直觉，参照系统以往的错误

3. 迭代：

   > 1. 遗漏：测试过程中补充
   > 2. 需求变动
   > 3. 挖掘更多的测试点：探索式测试
   > 4. BUG：记录，报告，重现并回归

4. 忌讳

   > 1. 变成整理策划文档
   > 2. 可读性差
   > 3. 逻辑混乱
   > 4. 无法执行测试
   > 5. 明显的遗漏

---

## 测试过程

### 准备阶段

1. 计划

   > 1. 人员分工
   > 2. 时间分配
   > 3. 形成具体方案
   > 4. 影响因素：时间预算，系统复杂度，功能属于新增或调整，人员是否熟练

2. 脚本/GM指令：事前先与程序沟通好，了解指令或逻辑，准备好相关脚本，提高测试效率，达到测试条件

3. 权限：明确账户权限

4. 复查文档：需求文档，设计文档

### 执行用例

1. 大局观：先进行冒烟测试，测通主流程，后测细节

   > 1. 给程序留足时间，优先处理BLOCK级别的BUG
   > 2. QA对测试量有个直观判断

2. 提高效率

   > 1. 调整用例执行顺序
   > 2. 了解程序实现，提高用例的准确性
   > 3. 事前准备好测试脚本
   > 4. 查看程序的diff，准确知道修改的内容，通过修改知道和定位BUG

3. 测试目标：功能正确 -> 符合策划意图（基本合格线）-> 功能合理，用户喜欢

### BUG处理

1. 确认是否为BUG

2. 重现BUG：

   > 1. 确认BUG存在，避免误报
   >
   > 2. 确定BUG类型：必然重现/几率重现/无法重现
   >
   > 3. 帮助程序定位问题
   >
   > 4. 方便QA复查，是QA测试能力的体现
   >
   > 5. 建议：
   >
   >    > 1. 测试前，保证环境正确（代码最新，数据最新，账号正确等）
   >    > 2. 测试时，记录操作步骤
   >    > 3. 详细了解系统实现
   >    > 4. 保持用例更新
   >    > 5. 截图
   >    > 6. 关注日志文件
   >    > 7. 保留dump文件

3. 提交BUG：

   > 1. 责任人
   > 2. BUG的准确描述
   > 3. BUG的严重等级和优先程度
   > 4. 截图和关注LOG
   > 5. 提交到相关系统

4. 程序修改后复查BUG：

   > 1. 确认当前版本为已经修改后的版本（代码，数据，账号等）
   > 2. 向程序了解BUG成因和涉及到的系统
   > 3. 确保程序实现和需求文档说明的一致
   > 4. 复查无误后关闭BUG单

---

## 回归测试

1. 全面
2. 时间有限：以关键模块为主要目标
3. 高效：自动化脚本回归

---

## 测试收尾

1. 确认相关系统需求单/BUG单状态
2. 整理测试用例以及相关脚本/指令
3. 发送测试报告
4. 总结方法/经验/教训

---

## 建议

1. 熟悉产品
2. 保持良好的人际关系
3. 乐于分享
4. 提高产品满意度
5. 保持学习

---

## 其它

1. QA：事前预防，生产过程改进，关注机制，长期利益

2. 基本原则：

   > 1. 发现问题：尽早介入测试
   > 2. 追控一切变化
   > 3. 尽量避免问题流入下游环节

3. 预防胜于治疗

4. 容忍犯错，但不能一错再错，对错误的防御逐渐提高

5. 用数据说话：定量分析，定性评价

6. 避免盲目的技术崇拜

   > 1. 与技术问题相比，人的问题更难解决
   > 2. 技术只是手段不是目的，手段为目的服务
   > 3. 单纯技术似乎高端，但产品才是企业的生命

7. 一切从实际出发

   > 1. 寻找目前最适合，而不是理论上最优的方案
   > 2. 先执行然后改进，而不是一步到位

8. 质量并非高于一切

   > 1. 质量也有成本
   > 2. 系统思维
   > 3. 鸡尾酒效应

9. 学会展示工作

   > 1. 主动反馈
   > 2. 数据收集，统计，分析
   > 3. 数据可视化

10. 主人公意识，别以为与自己无关