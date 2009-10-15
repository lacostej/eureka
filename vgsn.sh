while [ 1 ]; do
  git pull
  python2.6 ./vgsn_autogen.py 2>&1 | tee -a vgsn.log
  sleep 10
done
