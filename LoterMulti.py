import allel
import os
import numpy as np
import loter.locanc.local_ancestry as lc
import matplotlib.pyplot as plt
import argparse

# 设置 argparse 参数
parser = argparse.ArgumentParser(description='LoterMulti - LoterMulti软件：根据3个祖先的基因型，推断本地祖先')
parser.add_argument('-i1', '--input_1', type=str, required=True, help='输入第一个祖先的基因型文件路径')
parser.add_argument('-i2', '--input_2', type=str, required=True, help='输入第二个祖先的基因型文件路径')
parser.add_argument('-i3', '--input_3', type=str, required=True, help='输入第三个祖先的基因型文件路径')
parser.add_argument('-a', '--input_adm', type=str, required=True, help='输入混合个体的基因型文件路径')
parser.add_argument("-t", "--threads", type=int, default=1, help="设置线程数")
parser.add_argument('-o', '--output', type=str, required=True, help='输出文件路径')
parser.add_argument("-v", "--verbose", action="version", version="LoterMulti 1.0.0", help="显示软件版本")
args = parser.parse_args()

# vcf格式转npy格式

def vcf2npy(vcfpath):
    callset = allel.read_vcf(vcfpath)
    haplotypes_1 = callset['calldata/GT'][:,:,0]
    haplotypes_2 = callset['calldata/GT'][:,:,1]
    
    m, n = haplotypes_1.shape
    mat_haplo = np.empty((2*n, m))
    mat_haplo[::2] = haplotypes_1.T
    mat_haplo[1::2] = haplotypes_2.T
    
    return mat_haplo.astype(np.uint8)

#输入文件路径
H_ref1 = vcf2npy(os.path.join(args.input_1))
H_ref2 = vcf2npy(os.path.join(args.input_2))
H_ref3 = vcf2npy(os.path.join(args.input_3))
H_Adm = vcf2npy(os.path.join(args.input_adm))

#调用loter
res_impute,res_loter = lc.loter_local_ancestry(l_H=[H_ref1, H_ref2, H_ref3], h_adm=H_Adm, num_threads=args.threads,default=False) ## set the number of threads

#输出文件
np.savetxt(f"{args.output}.loter.txt",res_loter[0],fmt="%i")

#绘制图片
plt.imshow(res_loter[0], interpolation='nearest', aspect='auto')
plt.colorbar()
plt.savefig(f"{args.output}.loter.png",dpi=300)
