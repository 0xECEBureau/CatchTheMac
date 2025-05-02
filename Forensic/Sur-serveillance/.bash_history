cd /tmp
ls /etc
cat /etc/hosts
grep 127.0.0.1 /etc/hosts
ping -c 2 8.8.4.4
curl -s http://ifconfig.me
docker ps -a
docker run hello-world
snap install hello-world
pip install requests
npm install -g http-server
systemctl status ssh
journalctl -u ssh -n 20
iptables -L
netstat -tulpn
cd /home/mac
ls
ls -la
pwd
git status
git pull origin main
git log --oneline
nano notes.txt
cat notes.txt
apt update
apt install -y tree htop net-tools
apt install -y python3-pip
pip3 install virtualenv
snap list
./scripts/backup.sh
python3 cleanup.py
grep TODO scripts/*.sh
grep secret *.txt
chmod 777 /var/tmp
touch /var/spool/cron/crontabs/root
ls -l /var/spool/cron/crontabs
chown nobody:nogroup /tmp/testfile
history
whoami
id
date
uptime
df -h
du -sh *
ps aux
top -b -n1
exit
cd /var/log
ls -1
grep error syslog
tail -n 50 auth.log
cd ~
echo "starting legit work"
./scripts/monitor.sh
sleep 1
echo "monitor done"
./scripts/cleanup.sh
ls /var/tmp
rm -rf /var/tmp/testdir
find /home/mac -maxdepth 2 -type f | wc -l
ssh user@10.0.0.5
ssh -p 2222 root@192.168.1.200
ssh -i ~/.ssh/id_rsa attacker@203.0.113.5
ftp anonymous@ftp.example.com
telnet 192.168.1.201 23
scp file.txt user@192.168.1.50:/tmp
echo MAC{G0T_SH3L1,WH0S_TH3R3} > flag.txt
ssh root@192.168.1.100
whoami
id
cd /root
ls -la
cat /root/.bashrc
cd /home/mac
echo "mac ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
visudo -c
apt update
apt install -y vim htop curl wget
curl -fsSL https://packages.crowdstrike.com/falcon/sensor.deb -o sensor.deb
dpkg -i sensor.deb
systemctl enable crowdstrike-sensor
systemctl restart crowdstrike-sensor
rm sensor.deb
exit
cd /home/mac
cat flag.txt
chmod 600 flag.txt
history
logout
ssh mac@localhost
exit
cd /home/mac/projects
ls -R
grep "password" -R .
find . -type f -name "*.sh"
./projects/run_tests.sh
./projects/deploy.sh
python3 -m http.server 8000
sleep 2
curl -s http://127.0.0.1:8000
kill $(pgrep -f http.server)
exit
sudo rm -rf /tmp/*
journalctl --vacuum-time=2d
echo "session end"
