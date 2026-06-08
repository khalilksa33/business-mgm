#!/bin/bash
set -e
sshpass -p '*/*iicc2*/*' scp -o StrictHostKeyChecking=no /tmp/deploy_remote.sh iicc2@192.168.8.59:~/deploy_remote.sh
sshpass -p '*/*iicc2*/*' ssh -o StrictHostKeyChecking=no iicc2@192.168.8.59 "tr -d '\r' < ~/deploy_remote.sh > ~/deploy_remote_clean.sh && chmod +x ~/deploy_remote_clean.sh && ~/deploy_remote_clean.sh"
