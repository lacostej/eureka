while [ 1 ]; do
  python2.6 ./vgsn_autogen.py 2>&1 | tee -a vgsn.log
  sleep 10
done
