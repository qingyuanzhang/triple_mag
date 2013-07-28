#!/bin/sh 
# author:coralzd
# www.freebsdsystem.org www.linuxtone.org
mysqldump -urtyk_triple  -pwinter4coming rtyk_triple --add-drop-table --opt >/home/rtyk/webapps/backup/$(date -d yesterday +%Y-%m-%d)_rtyk_triple.sql
