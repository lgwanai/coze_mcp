#!/bin/bash

# Coze工作流MCP服务器管理脚本
# 用法: ./mcp-server.sh {start|stop|restart|status}

# 配置
SERVER_SCRIPT="server.py"
PID_FILE=".mcp-server.pid"
LOG_FILE="mcp-server.log"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查服务器是否运行
is_running() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0
        else
            # PID文件存在但进程不存在，清理PID文件
            rm -f "$PID_FILE"
            return 1
        fi
    fi
    return 1
}

# 获取服务器PID
get_pid() {
    if [ -f "$PID_FILE" ]; then
        cat "$PID_FILE"
    else
        echo ""
    fi
}

# 启动服务器
start_server() {
    log_info "正在启动Coze工作流MCP服务器..."
    
    # 检查是否已经运行
    if is_running; then
        local pid=$(get_pid)
        log_warning "服务器已经在运行中 (PID: $pid)"
        return 1
    fi
    
    # 检查server.py文件是否存在
    if [ ! -f "$SERVER_SCRIPT" ]; then
        log_error "找不到服务器脚本: $SERVER_SCRIPT"
        return 1
    fi
    
    # 检查Python环境
    if ! command -v python3 &> /dev/null; then
        log_error "Python3未安装或不在PATH中"
        return 1
    fi
    
    # 启动服务器
    cd "$SCRIPT_DIR"
    nohup python3 -u "$SERVER_SCRIPT" > "$LOG_FILE" 2>&1 &
    local pid=$!
    
    # 保存PID
    echo $pid > "$PID_FILE"
    
    # 等待一下确保启动成功
    sleep 3
    
    if is_running; then
        log_success "MCP服务器启动成功 (PID: $pid)"
        log_info "日志文件: $LOG_FILE"
        log_info "MCP服务器已启动"
        return 0
    else
        log_error "MCP服务器启动失败"
        rm -f "$PID_FILE"
        return 1
    fi
}

# 停止服务器
stop_server() {
    log_info "正在停止Coze工作流MCP服务器..."
    
    if ! is_running; then
        log_warning "服务器未运行"
        return 1
    fi
    
    local pid=$(get_pid)
    log_info "正在终止进程 (PID: $pid)..."
    
    # 尝试优雅关闭
    kill "$pid" 2>/dev/null
    
    # 等待进程结束
    local count=0
    while [ $count -lt 10 ] && ps -p "$pid" > /dev/null 2>&1; do
        sleep 1
        count=$((count + 1))
    done
    
    # 如果还在运行，强制终止
    if ps -p "$pid" > /dev/null 2>&1; then
        log_warning "优雅关闭失败，强制终止进程..."
        kill -9 "$pid" 2>/dev/null
        sleep 1
    fi
    
    # 清理PID文件
    rm -f "$PID_FILE"
    
    if ! ps -p "$pid" > /dev/null 2>&1; then
        log_success "MCP服务器已停止"
        return 0
    else
        log_error "无法停止MCP服务器"
        return 1
    fi
}

# 重启服务器
restart_server() {
    log_info "正在重启Coze工作流MCP服务器..."
    
    if is_running; then
        stop_server
        if [ $? -ne 0 ]; then
            log_error "停止服务器失败，无法重启"
            return 1
        fi
    fi
    
    # 等待一下确保完全停止
    sleep 1
    
    start_server
    return $?
}

# 显示服务器状态
show_status() {
    echo "=== Coze工作流MCP服务器状态 ==="
    
    if is_running; then
        local pid=$(get_pid)
        log_success "服务器正在运行 (PID: $pid)"
        
        # 显示进程信息
        if command -v ps &> /dev/null; then
            echo ""
            echo "进程信息:"
            ps -p "$pid" -o pid,ppid,cmd,etime,pcpu,pmem 2>/dev/null || echo "无法获取进程详细信息"
        fi
        
        # 显示日志文件信息
        if [ -f "$LOG_FILE" ]; then
            echo ""
            echo "日志文件: $LOG_FILE"
            echo "最近的日志 (最后10行):"
            tail -n 10 "$LOG_FILE" 2>/dev/null || echo "无法读取日志文件"
        fi
    else
        log_warning "服务器未运行"
    fi
    
    echo ""
    echo "文件状态:"
    echo "  服务器脚本: $([ -f "$SERVER_SCRIPT" ] && echo "✓ 存在" || echo "✗ 不存在")"
    echo "  PID文件: $([ -f "$PID_FILE" ] && echo "✓ 存在" || echo "✗ 不存在")"
    echo "  日志文件: $([ -f "$LOG_FILE" ] && echo "✓ 存在" || echo "✗ 不存在")"
}

# 显示帮助信息
show_help() {
    echo "Coze工作流MCP服务器管理脚本"
    echo ""
    echo "用法: $0 {start|stop|restart|status|help}"
    echo ""
    echo "命令:"
    echo "  start   - 启动MCP服务器"
    echo "  stop    - 停止MCP服务器"
    echo "  restart - 重启MCP服务器"
    echo "  status  - 显示服务器状态"
    echo "  help    - 显示此帮助信息"
    echo ""
    echo "文件:"
    echo "  服务器脚本: $SERVER_SCRIPT"
    echo "  PID文件: $PID_FILE"
    echo "  日志文件: $LOG_FILE"
}

# 主函数
main() {
    case "$1" in
        start)
            start_server
            ;;
        stop)
            stop_server
            ;;
        restart)
            restart_server
            ;;
        status)
            show_status
            ;;
        help|--help|-h)
            show_help
            ;;
        "")
            log_error "请指定操作命令"
            echo ""
            show_help
            exit 1
            ;;
        *)
            log_error "未知命令: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"