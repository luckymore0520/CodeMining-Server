echo "username:"
read USER_NAME
echo "password:"
read PASSWORD
read PROJECT_NAME
HOST="http://115.29.184.56:10080/"
url=${HOST}${USER_NAME}${PROJECT_NAME}
echo $url
git remote set-url origin $url
git config --global user.email ${USER_NAME}"@mail.smail.edu.cn"                                                                                                                             
git config --global user.name ${USER_NAME}
echo "machine 115.29.184.56
login "${USER_NAME}"
password "${PASSWORD} >> ~/.netrc
git push -u origin master
chmod 777 auto-commit.sh
source auto-commit.sh &
