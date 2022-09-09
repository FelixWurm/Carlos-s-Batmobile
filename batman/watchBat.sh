watch -n .1 '
sudo batctl gwl;
echo;echo;echo;
sudo batctl o | grep -ie BATMAN -ie last-seen -ie \*
'
