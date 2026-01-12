# 开源贡献者成长知识图谱关系（RAG知识）
## 一、核心实体类型
1. 贡献者相关：新手开发者（NoviceDeveloper）、低频贡献者（LowFrequencyContributor）
2. 项目相关：入门项目（EntryProject）、健康项目（HighHealthLevelProject）
3. 行为动作相关：Star仓库（StarRepository）、创建Issue（OpenIssue）、评论Issue（CommentIssue）、提交拉取请求（SubmitPullRequest）、Fork仓库（Fork）
4. 生命周期相关：Issue生命周期（IssueLifecycle）、拉取请求生命周期（PullRequestLifecycle）
5. 激励成长相关：成长规则（GrowthRule）、学习路径（LearningPath）、贡献类型（ContributionType）

## 二、实体关系详情
### （一）贡献者-行为动作关系
1. 新手开发者-入门项目行为关系
   - 行为类型：创建Issue（OpenIssue）、评论Issue（CommentIssue）、Star仓库（StarRepository）
   - 核心属性：语义含义均为学习启动（LearningInitiation），贡献权重范围0.1-0.3，时间顺序分布在1-30区间
   - 关系说明：新手开发者在入职第一个月，通过对入门项目执行上述三种行为开启学习历程，不同行为的贡献权重存在差异，反映行为对项目贡献的价值程度

2. 低频贡献者-项目行为路径关系
   - 路径模式1：创建Issue→无响应→不再活跃（OpenIssue→NoResponse→Inactive）
     - 触发原因：无反馈（NoFeedback）、难度高（HighDifficulty）、响应时间长（LongResponseTime）
     - 典型时长：7-29天，路径稳定性低（Low），未达到激活阈值（ActivationThresholdReached: No）
   - 路径模式2：Star→评论Issue→不再活跃（Star→IssueComment→Inactive）
     - 触发原因：无反馈、难度高、响应时间长
     - 典型时长：8-30天，路径稳定性低，未达到激活阈值
   - 路径模式3：Fork→无拉取请求→不再活跃（Fork→NoPR→Inactive）
     - 触发原因：无反馈、难度高、响应时间长
     - 典型时长：8-27天，路径稳定性低，未达到激活阈值

### （二）行为动作-学习路径关系
1. 核心学习路径：创建Issue→提交拉取请求（OpenIssue→SubmitPullRequest）
   - 必要支持：维护者反馈（MaintainerFeedback）
   - 转换概率：0.41-0.8，平均转换概率约0.61
   - 学习成果：首次有效贡献（FirstValidContribution）
   - 关系说明：该路径是新手开发者实现有效贡献的核心路径，维护者反馈是关键支撑条件，转换概率反映该路径的可行性和有效性

### （三）项目-生命周期关系
1. 健康项目-节奏属性关系
   - 项目健康等级：高（High）
   - 核心节奏指标：
     - Issue响应中位数时长：5-24小时
     - 拉取请求审核中位数时长：1-4天
     - 合并率：0.63-0.88
     - 贡献者留存率：0.51-0.8
   - 节奏模式：快速反馈稳定合并（FastFeedbackStableMerge）
   - 关系说明：高健康等级项目通过快速响应Issue、高效审核拉取请求、稳定的合并率和较高的贡献者留存率，形成良性发展节奏

2. Issue/拉取请求-生命周期属性关系
   - 生命周期维度：开启到首次响应时长（OpenToFirstResponseHours）、解决时长（ResolutionDays）、解决类型（ResolutionType）、贡献者结果（ContributorOutcome）、后续贡献概率（FollowUpContributionProbability）
   - Issue生命周期特征：
     - 响应时长：2-47小时
     - 解决时长：1-14天
     - 解决类型：已回答（Answered）、已关闭（Closed）、已合并（Merged）
     - 贡献者结果：受激励（Motivated）、中立（Neutral）、受挫（Discouraged）
     - 后续贡献概率：0.22-0.66
   - 拉取请求生命周期特征：
     - 响应时长：1-47小时
     - 解决时长：1-14天
     - 解决类型：已回答、已关闭、已合并
     - 贡献者结果：受激励、中立、受挫
     - 后续贡献概率：0.21-0.69

### （四）贡献类型-价值属性关系
| 贡献类型 | 难度等级 | 学习价值 | 社区价值 | 基础分数 | 成长影响权重 |
|----------|----------|----------|----------|----------|--------------|
| Star仓库 | 极低（VeryLow） | 低（Low） | 低（Low） | 2 | 0.1 |
| 创建Issue | 低（Low） | 中（Medium） | 中（Medium） | 10 | 0.4 |
| 提交拉取请求 | 高（High） | 高（High） | 高（High） | 30 | 0.8 |
| 关系说明：贡献类型的难度等级与学习价值、社区价值、基础分数、成长影响权重呈正相关，提交拉取请求是价值最高的贡献类型 |

### （五）贡献行为-激励成长关系
1. 触发贡献（TriggerContribution）与激励规则映射
   - 触发类型1：Issue已解决（IssueResolved）
     - 奖励类型：等级提升（LevelUp）、徽章（Badge）、积分（Score）
     - 奖励名称：活跃贡献者（ActiveContributor）、明日之星（RisingStar）
     - 积分增量：26-98，均具有等级提升影响（LevelUpImpact: Yes），对社区健康产生积极影响（CommunityHealthImpact: Positive）
   - 触发类型2：首次拉取请求合并（FirstPRMerged）
     - 奖励类型：等级提升、徽章、积分
     - 奖励名称：活跃贡献者、明日之星、首次贡献者（FirstContribution）
     - 积分增量：19-88，均具有等级提升影响，对社区健康产生积极影响
   - 触发类型3：五次贡献（FiveContributions）
     - 奖励类型：等级提升、积分
     - 奖励名称：活跃贡献者、明日之星
     - 积分增量：27-58，均具有等级提升影响，对社区健康产生积极影响

## 三、知识图谱核心逻辑
1. 贡献者成长逻辑：新手开发者从基础行为（Star、创建Issue、评论Issue）起步，在维护者反馈支持下，通过核心学习路径（创建Issue→提交拉取请求）实现首次有效贡献，进而通过持续贡献获得激励成长；若缺乏反馈、面临高难度或长响应时间，易沦为低频贡献者并最终停止活跃
2. 项目健康逻辑：高健康等级项目通过快速反馈、高效审核、稳定合并的良性节奏，提升贡献者留存率和后续贡献概率，反向促进贡献者成长；贡献者的积极贡献行为也为项目健康提供支撑
3. 价值激励逻辑：贡献类型的价值决定其成长影响权重，高价值贡献（如提交拉取请求）对应更丰厚的激励回报，激励机制通过明确的触发条件和奖励规则，引导贡献者向高价值贡献行为转化，形成"贡献-价值-激励-成长"的正向循环