SSHAGENT=/usr/bin/ssh-agent
SSHAGENTARGS="-s"

cd ~/Code/Eureka/eureka

while [ 1 ]; do
  echo "resetting dropbox daemon"
  nb_dropbox=`ps -u vgsn -aef | grep dropbox | grep -v grep | wc -l`
  if [ $nb_dropbox -gt 0  ]; then
    ps -o pid,user,comm -ae | grep dropbox | cut -c 0-6 | xargs -l1 kill
  fi
  ~/.dropbox-dist/dropbox &

  echo "resetting ssh agent"
  nb_ssh_agent=`ps -u vgsn -aef | grep ssh-agent | grep -v grep | wc -l`
  if [ $nb_ssh_agent -gt 0  ]; then
    ps -o pid,user,comm -ae | grep ssh-agent | cut -c 0-6 | xargs -l1 kill
  fi
  if [ -x "$SSHAGENT" ]; then
    eval `$SSHAGENT $SSHAGENTARGS`
   # trap "kill $SSH_AGENT_PID" 0
  fi
  DISPLAY=junk SSH_ASKPASS=./add-phrase.sh ssh-add </dev/null

  echo "getting latest code"
  git pull

  echo "starting daemon"
  python2.6 ./vgsn_autogen.py 2>&1 | tee -a vgsn.log

  echo "sleeping a bit..."
  sleep 10
done
