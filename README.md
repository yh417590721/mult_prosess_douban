# mult_thread_douban
多进程爬取豆瓣最受欢迎的250部电影

#设置进程池数量，一般以cpu的核心数
pool = multiprocessing.Pool(multiprocessing.cpu_count())

#以pandas读取表格，CSV格式保存数据
