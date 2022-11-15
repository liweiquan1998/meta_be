```bash
# 在主节点和worker节点操作如下
sudo su
# 关闭防火墙：
ufw disable

# 关闭selinux：( x )
sed -i 's/enforcing/disabled/' /etc/selinux/config  # 永久
setenforce 0  # 临时

# 关闭swap：
swapoff -a  # 临时
vim /etc/fstab  # 永久

# 设置主机名：
hostnamectl set-hostname <hostname>

# 在master添加hosts：
cat >> /etc/hosts << EOF
192.168.199.208 k8s-master
192.168.199.107 k8s-node1
EOF

# 将桥接的IPv4流量传递到iptables的链：
cat > /etc/sysctl.d/k8s.conf << EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sysctl --system  # 生效

# 时间同步：
apt install ntpdate -y
ntpdate time.windows.com

# 配置并安装kubernetes组件
apt-get update && apt-get install -y apt-transport-https
curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
EOF
apt-get update
apt install kubeadm=1.19.16-00 kubectl=1.19.16-00 kubelet=1.19.16-00 -y --allow-unauthenticated

# 安装docker并配置docker代理（新系统）
apt install docker.io -y
cat << EOF > /etc/docker/daemon.json
{
"exec-opts": ["native.cgroupdriver=systemd"],
"registry-mirrors": ["https://registry.docker-cn.com","https://alzgoonw.mirror.aliyuncs.com"]
}
EOF
systemctl daemon-reload
systemctl restart docker

# 重启
reboot