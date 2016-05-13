sudo yum-config-manager --enable epel
sudo yum install -y spatialindex spatialindex-devel
sudo ln -sf /usr/bin/python2.7 /usr/bin/python
sudo python2.7 -m pip install Rtree==0.7.0
sudo python2.7 -m pip install matplotlib
sudo pip install scipy