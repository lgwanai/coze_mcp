# Coze工作流MCP服务

这是一个基于Model Context Protocol (MCP)的Coze工作流服务，使用官方MCP Python SDK构建，允许通过MCP协议调用Coze平台的工作流。

## 功能特性

- 🔧 **工具调用**: 执行Coze工作流
- 📊 **资源获取**: 获取工作流信息
- 🚀 **异步支持**: 支持异步工作流执行
- 🔍 **状态查询**: 查询异步执行状态
- 📝 **提示词**: 创建工作流执行提示词
- ✅ **标准协议**: 完全兼容MCP协议标准

## 项目结构

```
coze-mcp/
├── server.py              # MCP服务器主文件 (官方SDK版本)
├── coze_client.py         # Coze API客户端
├── config.py              # 配置管理
├── requirements.txt       # 项目依赖
├── .env                   # 环境变量配置
├── README.md              # 项目说明
├── api_doc.md             # API文档
├── demo.py                # 演示脚本
└── test/                  # 测试文件夹
    ├── test_server.py     # 服务器测试
    ├── test_coze_client.py # 客户端测试
    ├── test_simple.py     # 简单测试
    └── debug_connection.py # 连接调试
```

## 启动服务

### 方式1: 直接运行Python脚本

```bash
python server.py
```

### 方式2: 使用FastMCP CLI

```bash
# 安装FastMCP CLI
pip install fastmcp

# 启动SSE模式服务
fastmcp run server.py --transport sse --host 0.0.0.0 --port 8000
```

## 配置说明

### 环境变量配置 (.env)

```env
# Coze平台配置
COZE_BASE_URL=localhost:8888
COZE_TOKEN=your_coze_token_here

# 测试工作流配置
TEST_WORKFLOW_ID=7531773147675099136
TEST_SPACE_ID=7531337975355932672

# MCP服务配置
MCP_HOST=0.0.0.0
MCP_PORT=8000
```

### 配置文件 (config.py)

配置文件包含Coze平台的基础设置，包括API地址、认证token等。

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境
复制 `.env.example` 到 `.env` 并填入你的Coze API配置：
```bash
cp .env.example .env
```

### 3. 启动服务器

#### 使用管理脚本（推荐）
```bash
# 启动SSE模式服务器
./mcp-server.sh start

# 查看服务器状态
./mcp-server.sh status

# 停止服务器
./mcp-server.sh stop

# 重启服务器
./mcp-server.sh restart
```

#### 手动启动
```bash
# SSE模式（用于远程连接）
python server.py --sse

# STDIO模式（用于本地连接）
python server.py
```

### 4. 测试服务
```bash
python test/test_server.py
```

服务启动后将在 `http://localhost:8000` 提供MCP服务。

## MCP功能

### 工具 (Tools)

#### 1. run_coze_workflow
执行Coze工作流

**参数:**
- `workflow_id` (必需): 工作流ID
- `parameters` (可选): 工作流输入参数
- `bot_id` (可选): 关联的智能体ID
- `is_async` (可选): 是否异步执行
- `app_id` (可选): 应用ID

**示例:**
```python
result = await run_coze_workflow(
    workflow_id="7531773147675099136",
    parameters={"user_input": "Hello World"},
    is_async=False
)
```

#### 2. get_workflow_status
查询异步工作流执行状态（预留接口）

**参数:**
- `execute_id` (必需): 异步执行ID

### 资源 (Resources)

#### coze://workflow/{workflow_id}
获取指定工作流的信息和使用说明

**示例:**
```
coze://workflow/7531773147675099136
```

### 提示词 (Prompts)

#### create_workflow_execution_prompt
创建工作流执行的提示词模板

**参数:**
- `workflow_id` (必需): 工作流ID
- `task_description` (必需): 任务描述

## 测试

### 测试Coze客户端

```bash
python test/test_coze_client.py
```

这将测试:
- 同步工作流执行
- 异步工作流执行
- API连接和响应处理

### 测试MCP服务

首先启动MCP服务:
```bash
python server.py
```

然后在另一个终端运行测试:
```bash
python test/test_mcp_server.py
```

这将测试:
- 服务器健康状态
- MCP工具调用
- MCP资源获取

## API文档

详细的Coze工作流API文档请参考 `api_doc.md` 文件。

## 近期计划

1.  完善异步调用，实现查询工作流异步执行结果
2.  执行工作流（流式响应）
3.  恢复运行工作流
4.  执行对话流

## 使用示例

### 在Claude Desktop中使用

1. 启动MCP服务
2. 在Claude Desktop的配置中添加MCP服务器
3. 使用工具执行工作流

### 编程方式调用

```python
import asyncio
from coze_client import CozeWorkflowClient, WorkflowRequest

async def main():
    client = CozeWorkflowClient()
    
    request = WorkflowRequest(
        workflow_id="7531773147675099136",
        parameters={"input": "test data"}
    )
    
    response = await client.run_workflow(request)
    print(f"结果: {response.data}")
    
    await client.close()

asyncio.run(main())
```

## 注意事项

1. **工作流状态**: 确保要执行的工作流已在Coze平台发布
2. **网络连接**: 确保能够访问Coze平台API
3. **Token权限**: 确保使用的token具有执行工作流的权限
4. **参数格式**: 工作流参数需要符合对应工作流的输入要求
5. **文件支持**: 当前版本暂不支持文件类型参数，后续版本将完善

## 故障排除

### 常见问题

1. **连接失败**: 检查Coze平台地址和网络连接
2. **认证失败**: 验证token是否正确且有效
3. **工作流执行失败**: 检查工作流ID和参数是否正确
4. **MCP服务无响应**: 确认服务已正确启动且端口未被占用

### 调试方法

1. 查看服务日志输出
2. 使用debug_url查看工作流执行详情
3. 运行测试脚本验证各组件功能

## 开发计划

- [ ] 支持文件类型参数
- [ ] 实现工作流状态查询API
- [ ] 添加更多错误处理和重试机制
- [ ] 支持批量工作流执行
- [ ] 添加工作流执行历史记录

## 许可证

MIT License