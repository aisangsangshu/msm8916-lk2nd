#!/usr/bin/env python3
"""
合并lk2nd.img和PostmarketOS boot镜像脚本
将lk2nd.img放在前512KB，PostmarketOS boot镜像放在512KB偏移处
"""

import os
import sys
import argparse
from pathlib import Path

def combine_images(lk2nd_path, pmos_path, output_path, offset_kb=512):
    """
    合并lk2nd.img和PostmarketOS boot镜像
    
    参数:
        lk2nd_path: lk2nd.img的路径
        pmos_path: PostmarketOS boot镜像的路径
        output_path: 输出文件的路径
        offset_kb: 偏移量，单位为KB，默认为512KB
    """
    offset_bytes = offset_kb * 1024
    
    # 检查lk2nd镜像大小
    lk2nd_size = os.path.getsize(lk2nd_path)
    if lk2nd_size > offset_bytes:
        print(f"错误: lk2nd.img大小({lk2nd_size}字节)超过了偏移量({offset_bytes}字节)")
        return False
    
    # 读取lk2nd镜像
    with open(lk2nd_path, 'rb') as f:
        lk2nd_data = f.read()
    
    # 读取PostmarketOS boot镜像
    with open(pmos_path, 'rb') as f:
        pmos_data = f.read()
    
    # 创建合并镜像
    with open(output_path, 'wb') as f:
        # 写入lk2nd镜像
        f.write(lk2nd_data)
        
        # 填充空白直到偏移位置
        padding_size = offset_bytes - lk2nd_size
        if padding_size > 0:
            f.write(b'\0' * padding_size)
        
        # 写入PostmarketOS boot镜像
        f.write(pmos_data)
    
    print(f"成功创建合并镜像: {output_path}")
    print(f"lk2nd.img大小: {lk2nd_size}字节")
    print(f"偏移量: {offset_bytes}字节")
    print(f"PostmarketOS boot镜像大小: {len(pmos_data)}字节")
    print(f"合并镜像总大小: {os.path.getsize(output_path)}字节")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='合并lk2nd.img和PostmarketOS boot镜像')
    parser.add_argument('lk2nd', help='lk2nd.img文件路径')
    parser.add_argument('pmos', help='PostmarketOS boot镜像文件路径')
    parser.add_argument('-o', '--output', default='combined_boot.img', help='输出文件路径 (默认: combined_boot.img)')
    parser.add_argument('--offset', type=int, default=512, help='偏移量，单位为KB (默认: 512)')
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    if not os.path.exists(args.lk2nd):
        print(f"错误: 找不到文件 {args.lk2nd}")
        return 1
    
    if not os.path.exists(args.pmos):
        print(f"错误: 找不到文件 {args.pmos}")
        return 1
    
    # 合并镜像
    success = combine_images(args.lk2nd, args.pmos, args.output, args.offset)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 