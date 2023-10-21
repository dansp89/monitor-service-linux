# DSP - Monitor Service

Monitor Ubuntu services and receive notifications via Telegram.

# 1. Instalation

## 1.1 Basic installation on the Operating System
```bash
sudo apt update
```

```bash
sudo apt install -y python3 systemd python3-pip
```

```bash
pip3 install requests python-systemd
```
## 1.2 Installation of the monitoring application

```bash
pip install -r requirements.txt
```

## 1.3 Install monitor service

- Create a new service

```bash
sudo nano /etc/systemd/system/dsp-monitor.service
```

- Copy and Paste the code below, change the monitor.py file path in <code>/etc/systemd/system/dsp-monitor.service</code>

```bash
[Unit]
Description=DSP - Monitors and restarts the service when necessary

[Service]
ExecStart=sudo /usr/bin/python3.10 /home/dansp/dsp-monitor.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## 1.4 Allow execution

```bash
chmod +x /home/dansp/dsp-monitor.py
```

## 1.5 Restart services

```bash
sudo systemctl daemon-reload
sudo systemctl start dsp-monitor
sudo systemctl enable dsp-monitor
```
