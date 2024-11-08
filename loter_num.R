'''
使用方法：Rscript loter_num.R -i LoterMulti_result.txt -o ancestry_num.txt -a 1
其中-i,-o,-a参数均必须输入，-a为0,1,2。表示祖先成分。
'''
library(getopt)

spec <- matrix(c("first","i",1,"character","input",
                 "second","o",1,"character","output",
                 "third","a",2,"integer","input ancestry num"),byrow = TRUE,ncol = 5)

opt <- getopt(spec=spec)

hapfile <- read.csv(opt$first,sep = " ",header = FALSE)


# 函数：计算每行中连续出现2的区域数量和每个区域的长度
count_continuous_twos <- function(row) {
  # 找到2的位置
  twos <- row == opt$third
  # 标记连续区域
  runs <- rle(twos)
  # 找到连续2的区域数量,并筛选出长度大于3的区域
  num_regions <- sum(runs$values)
  # 获取每个符合条件的区域长度
  lengths <- runs$lengths[runs$values]
  
  list(num_regions = num_regions, lengths = lengths)
}

# 应用函数到每一行
result <- apply(hapfile, 1, count_continuous_twos)

# 显示结果
# 将结果转化为期望格式
formatted_result <- sapply(result, function(x) {
# 提取 `num_regions` 和 `lengths`，并将其合并为一个字符串
  paste(c(x$num_regions, x$lengths), collapse = " ")
})

# 将结果写入文件或显示
file_conn <- file(opt$second,"w")
writeLines("祖先区域数量 每个区域的长度", file_conn)
# 写入格式化结果
writeLines(formatted_result, file_conn)
close(file_conn)
