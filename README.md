# LoterMulti
功能：处理2个或者3个祖先成分及以上的loter软件升级版本。  
注意：  
使用之前，请在python中安装allel, numpy, loter, matplotlib, argparse等模块。  
该软件目前只支持以vcf文件为输入文件，输出文件为一个单倍型文件。  
使用方法：python LoterMulti.py -h  

#LoterAncLen.py  
功能：loter结果后续处理之一。统计祖先片段在混合群体中的总数以及每条片段的长度。  
使用方法：python LoterAncLen.py -h  
结果说明：第一列为片段所在的单倍型；第二列为起始坐标；第三列为终止坐标；第四列为长度  
  
Dealing with more than 2 ancestral populations

Before use, you need to install allel, numpy, loter, matplotlib, argparse in python in advance.  
The software currently only supports vcf files as input files. The output results in a haplotype file.  
Usage: python LoterMulti.py -h.  

#LoterAncLen.py  
The LOTER results were analyzed to count the total number of ancestral fragments in the population and the length of each ancestral fragment.  
Usage: python LoterAncLen.py -h  
Result description: the first column is the haplotype of the fragment; The second column is the starting coordinates; The third column is the termination coordinates; The fourth column is the length  
