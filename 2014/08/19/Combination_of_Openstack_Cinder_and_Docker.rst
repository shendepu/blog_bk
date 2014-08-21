******************************************
Combination of Openstack Cinder and Docker
******************************************

Docker暂时还不可以连接Cinder生成的Volume，使用KVM的虚机在CPU的利用率上尽管可能过Nova的CPU Over Ratio尽可能充分利用，但内存因一般Nova配置为1.5的Over Ratio而可能利用不充分，同时产生的VM的overhead也随着VM的数量而大大增加。

那如何能既利Docker (LXC)的高效CPU及内存利用率，同时又利用Cinder的Volume呢？

通过Cinder可以以低成本实现企业级别的磁盘（Block Device）高可用性及可靠性。具体可采用双节点Cinder Node以Active-Passive模式实现高可用性，同时在每节点建立RAID 10磁阵，磁盘可选用7200转的西部数据的4TB红盘，RAID卡可选用LSI的千元级别阵列卡，如20块4TB磁盘能过RAID 10可实现40TB容量，平均1000 IO。并可进一步升级更高级的阵列卡加BBU提高磁盘写IO，如果对磁盘IO的要求更高，可以建立SSD磁盘构建的Cinder节点。 从而可以抛弃传统昂贵的企业级阵（如果只有一台还不是高可用性及可靠性）。

既然Docker无法利用Cinder，但KVM的Nova是可以连接Cinder的volume，那我们可以建立一台大的KVM虚拟机，然后在此VM中运行Docker实例。因数据存储在Cinder中，从而也不用担心数据的可靠性。



.. author:: default
.. categories:: none
.. tags:: none
.. comments::
