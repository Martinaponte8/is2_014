#!/bin/bash
echo "---Base de datos prodbd para entorno de Producción---"
echo "Borrando base de datos prodbd existente..."
dropdb -i --if-exists prodbd
if [ "$?" -ne 0 ]
then
    echo -e "No se pudo borrar la base de datos prodbd, verifique que no esté siendo usada."
    exit 1
fi
echo "Se ha borrado la base de datos prodbd."
echo "Creando la base de datos prodbd..."
createdb prodbd
if [ "$?" -ne 0 ]
then
    echo -e "No se pudo crear prodbd"
    exit 2
fi
echo "Se ha creado prodbd"

source venv/bin/activate
PGPASSWORD="admin"
psql -h localhost -p 5432 -U postgres -d prodbd -f dbdev
echo "prodbd se cargó exitosamente."
