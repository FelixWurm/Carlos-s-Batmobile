PAUSETIME=5
while getopts i:t: flag
do
    case "${flag}" in
        t) PAUSETIME=${OPTARG};;
    esac
done
case "$-" in
   *i*) sudo apt install speedtest-cli;;
esac
clear



echo batctl throughputmeter to gateway:
sudo batctl throughputmeter b8:27:eb:91:80:1b
sleep $PAUSETIME
echo;echo;echo


echo speedtest-cli:
speedtest

