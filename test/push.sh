#!/bin/bash
# application name is first parameter : $1
# commit secont parameter : $2
cd $1
heroku git:remote -a $1
git add .
git commit -m $2
git push heroku master


#exit
