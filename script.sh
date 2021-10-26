#!/bin/bash
mkdir -p media
chmod 777 media
mkdir -p static
echo "¡Bienvenido a SistemaGestor!"
echo "Seleccione uno de los siguientes entornos de despliegue:"
PS3='Por favor, ingrese una opción:'
options=("Desarrollo" "Producción" "Salir")
select opt in "${options[@]}"
do
    case $opt in
        "Desarrollo")
            echo "Elegió desplegar desarrollo..."
            echo
            #echo "Elija uno de los siguientes tags:"
            #git tag
            #echo "Ingrese en nombre del tag:"
            #read tg
            #git checkout $tg
            #while [ "$?" -ne 0 ]; do
            #     echo
            #     echo "No existe tag con el nombre proveído. Vuelva a intentar..."
            #     echo
            #     echo "Elija uno de los siguientes tags:"
            #     git tag
            #     read -p "Ingrese en nombre del tag: " tg
            #     git checkout $tg
            #done
            echo
            pip install virtualenv
            virtualenv venv --python=python3
            source venv/bin/activate
            pip install -r requeriments.txt
            echo
            chmod +x devbdconf.sh
            -u postgres ./devbdconf.sh
            break
            ;;
        "Producción")
            echo "Eligió desplegar producción..."
            echo
            virtualenv venv --python=python3
            source venv/bin/activate
            pip install -r requeriments.txt
            echo
            chmod +x prodbdconf.sh
            -u postgres ./prodbdconf.sh
            cd ..
            path=$(pwd)
            cd poliproyectos
            echo "Configurando servidor httpd..."
            echo "<VirtualHost *:80>
                    ServerName localhost
                    WSGIDaemonProcess poliproyectos python-home=$path/poliproyectos/venv python-path=$path/poliproyectos
                    WSGIProcessGroup poliproyectos
                    WSGIScriptAlias / $path/poliproyectos/poliproyecto/wsgi.py

                    Alias /static/ $path/poliproyectos/static/
                    <Directory $path/poliproyectos/static/ >
                        Require all granted
                        Allow from all
                    </Directory>

                    <Directory $path/poliproyectos/poliproyecto >
                        <Files wsgi.py>
                            Require all granted
                        </Files>
                    </Directory>
                </VirtualHost>

                # vim: syntax=apache ts=4 sw=4 sts=4 sr noet"> /etc/apache2/sites-available/prueba.conf
            service apache2 restart
            sudo a2dissite 000-default.conf
            sudo a2ensite prueba.conf
            break
            ;;
        "Salir")
            break
            ;;
        *) echo "Opción inválida";;
    esac
done


