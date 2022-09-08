PAUSETIME = 5
while getopts i:t: flag
do
    case "${flag}" in
        i) sudo apt install speedtest-cli;;
        t) PAUSETIME = ${OPTARG};;
    esac
done


sudo batctl throuputmeter b8:27:eb:91:80:1b

sleep $PAUSETIME
echo;echo;echo

speedtest

sleep $PAUSETIME
echo;echo;echo

