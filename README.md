# MazeSolverLLM

> [MIT NEWS MAGAZINE: Mighty mouse](https://www.technologyreview.com/2018/12/19/138508/mighty-mouse/)

迷宫问题可以转化为最短路径求解问题，如4x4的地图标记为16个节点，将所有可行路径作为连接节点的边，即构建了一张图（Graph），给出起始节点和目标节点，寻找图中最短路径。

- 基础：以图构造纯文本数据 finetune LLM使其具备解谜能力。
- 进阶：不构造Graph, 直接输入迷宫图片，使用多模态数据finetune LLM.
