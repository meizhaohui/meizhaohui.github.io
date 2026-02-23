#!/bin/bash
# filename: grow_centos_space.sh
# function: CentOS7虚拟机分配后，使用本脚本一键扩容，无需手动一步步操作

echo "Step 1: 执行用户检查"
# 检查是否为root用户
if [[ "$(id -u)" != "0" ]]; then
    echo "错误: 这个脚本需要root权限执行." >&2
    exit 0
fi

echo "Step 2: 扩容"
# 磁盘名称
# 默认为 /dev/sda
# 也可以在脚本运行时指定参数 sh grow_centos_space.sh /dev/sdb
DISK_NAME="${1:-/dev/sda}"
echo "磁盘名称：${DISK_NAME}"

echo "Step 2.1: 使用fdisk命令创建新分区：fdisk ${DISK_NAME}"
# 创建新分区
fdisk "${DISK_NAME}" <<EOF
n
p
w
EOF

# 等待分区完成
sleep 2

echo "Step 2.2: 执行 partprobe 让系统识别新增的分区"
partprobe

echo "Step 2.3: 获取最后一个分区号"
# 获取最后一个分区号
last_partition_number=$(fdisk -l "${DISK_NAME}" | grep "^${DISK_NAME}" | tail -1 | awk '{print $1}' | sed "s@$DISK_NAME@@g")

echo "Step 2.4: 创建物理卷 pvcreate ${DISK_NAME}${last_partition_number}"
# 创建物理卷
pvcreate "${DISK_NAME}${last_partition_number}"

# 获取卷组名,默认值是centos
vg_name=$(vgdisplay | grep 'VG Name' | awk '{print $NF}')
echo "卷组名为: ${vg_name}"

echo "Step 2.5: 扩展卷组 vgextend ${vg_name} ${DISK_NAME}${last_partition_number}"
# 扩展卷组，这里的centos是卷组名，需要根据实际情况替换
vgextend "${vg_name}" "${DISK_NAME}${last_partition_number}"

# 扩展逻辑卷，lv0是逻辑卷名，需要根据实际情况替换
# lvextend -l +100%FREE /dev/vg0/lv0
mapper_name=$(df -h | grep 'mapper' | awk '{print $1}')
echo "需要扩容的分区: ${mapper_name}"
echo "Step 2.6: 扩展逻辑卷 lvextend -l +100%FREE ${mapper_name}"
lvextend -l +100%FREE "${mapper_name}"

file_type=$(df -T | grep "${mapper_name}" | awk '{print $2}')
echo "文件类型: ${file_type}"

if [[ "${file_type}" == "xfs" ]]; then
    # 扩展文件系统
    echo "Step 2.7: 扩展文件系统: xfs_growfs ${mapper_name}"
    xfs_growfs "${mapper_name}"
elif [[ "${file_type}" == "ext4" ]]; then
    # 扩展文件系统
    echo "Step 2.7: 扩展文件系统: resize2fs ${mapper_name}"
    resize2fs "${mapper_name}"
else
    echo "文件系统类型异常，请检查" >&2
    exit 1
fi
echo "再次查看磁盘空间"
df -hT
echo "扩容完成."
