#!/bin/bash

REPO="git@github.com:Martinaponte8/is2_014.git"
FOLDER="is2_014"
PYTHONPATH="/usr/bin/python3"


#clonar proyecto grupo 14
echo "Clonancion de Proyecto en proceso..."
cd
cd /home/sole/PycharmProjects

#git clone "${REPO}"
echo "Proyecto Clonado"

cd $FOLDER

#virtualenv -q -p "$PYTHONPATH" venv
virtualenv venv -p /usr/bin/python3
echo "Entorno virtual creado"

source venv/bin/activate
echo "Entorno virtual activado"

pip install -r requirements.txt
echo "Requerimientos instalados"

deactivate

cd
cd /home/sole/PycharmProjects/is2_014

echo "Montaje de entornos "
echo "Seleccionar una opción: "
options=("Desarrollo" "Producción" "Salir")
select opt in "${options[@]}"
do
    case $opt in
        "Desarrollo")
            echo "---¿Esta seguro que desea montar el ambiente de desarrollo?---"
            echo "Presione Enter para continuar, Ctrl+C para finalizar la instalacion"
	    read -r

            echo "Montando ambiente de desarrollo..."

            chmod +x /home/sole/PycharmProjects/is2_014/dev.sh
            sudo -u postgres /home/sole/PycharmProjects/is2_014/dev.sh

            echo "Activando entorno virtual..."
            source venv/bin/activate
            echo "Ejecutando makemigrations..."
            python manage.py makemigrations
            echo "Ejecutando migrate..."
            python manage.py migrate
            echo "Crear super usuario..."
            python manage.py createsuperuser
            echo "Ejecutando runserver..."
            python manage.py runserver


            break
            ;;
        "Producción")
            echo "---¿Esta seguro que desea montar el ambiente de produccion?---"
            echo "Presione Enter para continuar, Ctrl+C para finalizar la instalacion"
	    read -r

            echo "Montando ambiente de producción..."

            chmod +x /home/sole/PycharmProjects/is2_014/prod.sh
            sudo -u postgres /home/sole/PycharmProjects/is2_014/prod.sh

            echo "Activando entorno virtual..."
            source venv/bin/activate
            echo "Ejecutando makemigrations..."
            python manage.py makemigrations
            echo "Ejecutando migrate..."
            python manage.py migrate
            echo "Crear super usuario..."
            python manage.py createsuperuser

            #path=$(pwd)

            break
            ;;
        "Salir")
            break
            ;;
        *) echo "Opción inválida";;
    esac
done





#chmod +x dev.sh
#sudo -u postgres ./dev.sh


#chmod +x prod.sh
#sudo -u postgres ./prod.sh