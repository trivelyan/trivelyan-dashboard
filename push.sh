#!/bin/bash
cd $1
heroku git:remote -a $1
git add .
git commit -m $2
git push heroku master
