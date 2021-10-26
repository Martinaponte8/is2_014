#!/bin/bash
echo "---Base de datos sistemagestor para entorno de Desarrollo---"
echo "Borrando base de datos sistemagestor existente..."
dropdb -i --if-exists sistemagestor
if [ "$?" -ne 0 ]
then
    echo -e "No se pudo borrar la base de datos sistemagestor, verifique que no esté siendo usada."
    exit 1
fi
echo "Se ha borrado la base de datos sistemagestor."
echo "Creando la base de datos sistemagestor..."
createdb sistemagestor
if [ "$?" -ne 0 ]
then
    echo -e "No se pudo crear sistemagestor"
    exit 2
fi
echo "Se ha creado sistemagestor"

source venv/bin/activate
#PGPASSWORD="admin"
PGPASSWORD="postgres"
psql -h localhost -p 5432 -U postgres -d sistemagestor -f db.backup
echo "sistemagestor se cargó exitosamente."
