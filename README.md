# tcp_pack_demo

TCP分包/粘包的问题, 本质上是同一个问题, 由于socket在发送或者接收数据的时候会等待缓冲区中的数据满了才会进行, 这个时候就会导致
1. 分包, 应用程序发送了一段比较大的数据,被拆分成2个或者多于两个包发送出去, 这个时候在接收方接收的时候需要将2个包的数据合在一起才是一段完成的业务数据, 
2. 与分包相反的就是粘包, 就是发送方发送了2段或者多段的比较小的数据, 在缓冲区中被合成一个包发送出去, 相应的在接收方需要把收到的一个包分拆成2个或者多个包

其实分包/粘包是不可避免的问题, 不管是在TCP层还是基于TCP之上的应用层,比如 HTTP 就采用了Content-Length 指定了数据的大小, 或者是 chunked 编码的方式, 还有回车换行 \r\n 分隔符的方式去避免/解决这个问题

tcp_pack_demo 是针对TCP分包/粘包的一种解决方案, 是在业务层定义的规范/协议针对这个问题的办法, 当然这不是唯一的办法, 比如还可以用换行符(或者约定的分隔符, JDK中socket相关的API就有readline()这样的方法进行解决)进行分隔......等等等等

这个demo大致的想法就是在业务数据前面附加一段 meta_data, 这个 meta_data (类似HTTP里头的 header)可以根据业务需要设置不同的元数据, 这个demo中在meta_data中只设置了真正的业务数据的长度, 比如业务上需要发送 "hello server" 这段数据, 这个时候需要在发送前计算一下这段字符的字节数为12, 如果我们定义meta_data的长度为4位(也可以更长, 更具业务需要定义规范/协议)在高位补 '0' 填充至4位即: 0012, 然后将 meta_data 拼在业务数据的前面, 那么数据将变成 "0012hello server"这样发送出去, 那么接收端在接收的时候会先获取前面4位(meta_data)以确定接下来需要从缓冲区中读取多少字节的数据......
