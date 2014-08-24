************************
Software Raid with mdadm
************************

Build RAID with mdadm
=====================


RAID Recovery
============= 

RAID 1
------

测试盘：一块Toshibar 7200 2T和一块WD 7200 2T(此盘性能差，已经用3年)

mdadm (cat /proc/mdstat) 显示需耗时270分钟恢复，平均速度125M/s。 基本与磁盘顺序写性能相当，但实际耗时390分钟。磁盘的读写输出基本呈线性下降。

换了一块新的Toshibar 7200 2T， mdadm恢复需耗时186分钟，平均速度171M/S，但实际耗时323分钟，Data Check耗时256分钟。

结论：2T硬盘RAID 1恢复总耗时需579分钟，近10个小时。

.. image:: /_static/img/data/software_raid_with_mdadm_build_result.png
   :scale: 60%
   :alt: mdadm raid recovery test result




.. author:: default
.. categories:: none
.. tags:: none
.. comments::
