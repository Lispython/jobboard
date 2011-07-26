#!/bin/bash
source venv/bin/activate
manage(){
	./venv/bin/python manage.py $@
}

minor_update(){
	git push origin master;
	fab-2.6 production minor_update;
}
restart()
{
	fab-2.6 production restart_webserver;
}

deploy(){
	git push origin master;
	fab-2.6 production deploy;
}

case $1 in
    "minor_update") minor_update;;

    "deploy") deploy;;

	"restart") restart;;

    *) ./venv/bin/python manage.py $@;;

esac