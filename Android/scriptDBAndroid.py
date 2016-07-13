import os

os.system("sudo adb kill-server")
os.system("sudo adb start-server")
os.system("sudo adb devices")


os.system("echo 'hello world'")
os.system("adb shell run-as com.info_sync.infosync chmod 666 databases/infosync.db")
os.system("adb shell cp /data/data/com.info_sync.infosync/databases/infosync.db /sdcard/")
os.system("adb pull /sdcard/infosync.db .")
