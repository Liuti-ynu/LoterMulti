'''
loter结果后续分析其一：统计祖先片段在混合群体中的总数以及每个片段的长度。
注意：该脚本统计的祖先片段长度为连续祖先成分的终止位置所对应的SNP位点在vcf文件中的pos减去起始位置所对应的SNP位点在vcf文件中的pos。
'''

import vcf
import pandas as pd
import argparse

# 解析命令行参数
parser = argparse.ArgumentParser(description='LoterAncLen.py - 分析结果解析，统计祖先片段在混合群体中的总数以及每个片段的长度')
parser.add_argument('-v','--vcf_file', type=str,required=True, help='输入的VCF文件')
parser.add_argument('-l','--loter_file', type=str,required=True, help='输入的Loter的结果文件（单倍型格式）')
parser.add_argument('-o','--output_file', type=str,default="output.txt", help='输出文件名')
parser.add_argument('-L','--Length', type=int,default=2, help='最小片段长度，默认为2')
parser.add_argument('-p','--parent', type=int,required=True, help='输入的亲本组分，只能为0,1,2,...')

args = parser.parse_args()

# 打开VCF文件并指定编码
with open(args.vcf_file, 'r', encoding='utf-8') as vcf_file:
    vcf_reader = vcf.Reader(vcf_file)
    # 提取每个记录的 POS 列
    pos_list = [record.POS for record in vcf_reader]


#loter结果，以vcf文件的pos为列名
loter_result = pd.read_csv(args.loter_file,sep=" ",header=None)
loter_result.columns = pos_list

# 获取连续祖先片段的总数、每个片段的起始和终止位置的列名
def get_segment_info(row):
    segments = []
    segment_length = 0
    start_index = None
    
    for idx, val in enumerate(row):
        if val == args.parent:
            if segment_length == 0:
                start_index = idx  # 记录片段开始的位置
            segment_length += 1
        else:
            if segment_length >= 2:
                # 获取起始和终止位置的列名并计算差值
                start_col = row.index[start_index]
                end_col = row.index[idx - 1]
                diff = end_col - start_col
                # 只记录列名之差大于多少的片段
                if diff >= args.Length:
                    segments.append(diff)
            segment_length = 0
            start_index = None
    
    # 如果最后一个片段满足条件，记录其起始和终止位置之差
    if segment_length >= 2:
        start_col = row.index[start_index]
        end_col = row.index[len(row) - 1]
        diff = end_col - start_col
        if diff >= args.Length:
            segments.append(diff)
    
    return {
        'total_segments': len(segments),  # 总片段数
        'differences': segments  # 每个片段的终止位置与起始位置之差
    }

# 应用函数到每一行
Ancestry = loter_result.apply(get_segment_info, axis=1)

Ancestry.to_csv(args.output_file,sep="\t", index=False, header=None)
# 读取文件内容
with open(args.output_file, "r", encoding="utf-8") as f:
    content = f.read()

# 去掉 '{', '}', 和单引号
content = content.replace("{", "").replace("}", "").replace("'", "")

# 写入新的文件
with open(args.output_file, "w", encoding="utf-8") as f:
    f.write(content)
