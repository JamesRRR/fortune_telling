#!/bin/bash

if [ "$1" = "dev" ] || [ "$1" = "test" ] || [ "$1" = "prod" ]; then
    # 首先复制基础配置
    cp .env.common .env
    
    # 然后追加环境特定的配置（会覆盖相同的变量）
    cat .env.$1 >> .env
    
    echo "Switched to $1 environment"
else
    echo "Usage: ./switch-env.sh [dev|test|prod]"
    exit 1
fi 