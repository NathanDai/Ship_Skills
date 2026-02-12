#!/bin/bash
# 从 V2EX 主页获取前 N 篇文章标题
# 使用方法：get_top_articles.sh [N]
# 默认：5 篇文章

N=${1:-5}

curl -s 'https://www.v2ex.com' | \
 grep -oP '<span class="item_title">.*?</a>' | \
 sed 's/<span class="item_title"><a[^>]*>//; s/<\/a>//' | \
 head -n "$N"