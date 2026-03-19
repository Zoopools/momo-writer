#!/usr/bin/env python3
"""
apply-gene.py - Gene 应用脚本
应用 Gene 到指定 Agent
"""

import json
import sys
import os
from datetime import datetime

def get_gene_path(gene_id):
    """获取 Gene 文件路径"""
    workspace = os.path.expanduser("~/Documents/openclaw/openviking_workspace")
    return f"{workspace}/.openclaw/evolver/genes/{gene_id}.json"

def get_agent_config_path(agent_id):
    """获取 Agent 配置路径"""
    return os.path.expanduser(f"~/.openclaw/agents/{agent_id}/agent/config.json")

def read_gene(gene_path):
    """读取 Gene 文件"""
    try:
        with open(gene_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Gene 文件不存在: {gene_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Gene 文件格式错误: {e}")
        return None

def read_agent_config(config_path):
    """读取 Agent 配置"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Agent 配置不存在，创建新配置: {config_path}")
        return {"genes": [], "evolver": {}}
    except json.JSONDecodeError:
        print(f"❌ Agent 配置格式错误")
        return None

def write_agent_config(config_path, config):
    """写入 Agent 配置"""
    # 确保目录存在
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"✅ Agent 配置已更新: {config_path}")

def apply_gene(gene_id, agent_id):
    """应用 Gene 到 Agent"""
    print(f"🧬 应用 Gene: {gene_id} -> Agent: {agent_id}")
    print("-" * 50)
    
    # 1. 读取 Gene
    gene_path = get_gene_path(gene_id)
    gene = read_gene(gene_path)
    if not gene:
        return False
    
    print(f"📋 Gene 名称: {gene.get('name', 'N/A')}")
    print(f"📋 Gene 描述: {gene.get('description', 'N/A')}")
    print(f"📋 Gene 版本: {gene.get('version', 'N/A')}")
    print(f"📋 目标 Agent: {gene.get('agent', 'N/A')}")
    
    # 2. 验证 Gene 类型
    gene_type = gene.get('type', 'unknown')
    if gene_type == 'exclusive':
        target_agent = gene.get('agent')
        if target_agent and target_agent != agent_id:
            print(f"❌ Gene {gene_id} 是专属 Gene，只能应用到 {target_agent}")
            return False
    
    # 3. 读取 Agent 配置
    config_path = get_agent_config_path(agent_id)
    config = read_agent_config(config_path)
    if config is None:
        return False
    
    # 4. 应用 Gene
    if "genes" not in config:
        config["genes"] = []
    
    if "evolver" not in config:
        config["evolver"] = {}
    
    # 检查是否已应用
    existing_gene = next((g for g in config["genes"] if g.get("id") == gene_id), None)
    if existing_gene:
        print(f"📝 更新已存在的 Gene: {gene_id}")
        existing_gene.update({
            "version": gene.get("version"),
            "applied_at": datetime.now().isoformat(),
            "config": gene.get("config", {})
        })
    else:
        print(f"📝 添加新 Gene: {gene_id}")
        config["genes"].append({
            "id": gene_id,
            "name": gene.get("name"),
            "version": gene.get("version"),
            "applied_at": datetime.now().isoformat(),
            "config": gene.get("config", {})
        })
    
    # 5. 应用增强功能
    enhancements = gene.get("enhancements", [])
    if enhancements:
        print(f"🔧 应用 {len(enhancements)} 个增强功能:")
        for enh in enhancements:
            print(f"  - {enh.get('name')}: {enh.get('description')}")
    
    # 6. 保存配置
    write_agent_config(config_path, config)
    
    print("-" * 50)
    print(f"✅ Gene {gene_id} 成功应用到 {agent_id}")
    print(f"📝 应用时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return True

def main():
    if len(sys.argv) < 3:
        print("Usage: apply-gene.py <gene_id> <agent_id>")
        print("Example: apply-gene.py gene_writer_memory writer")
        sys.exit(1)
    
    gene_id = sys.argv[1]
    agent_id = sys.argv[2]
    
    success = apply_gene(gene_id, agent_id)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
