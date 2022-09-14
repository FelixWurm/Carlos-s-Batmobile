watch -n .1 '
echo Gateways
sudo batctl gwl;
echo;echo;echo;echo Originators / Next hop;
sudo batctl -H o | grep -ie BATMAN -ie last-seen -ie \*;
echo;echo;echo;echo IPV4 translation;
sudo batctl -H dc

'
