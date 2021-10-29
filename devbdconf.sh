#!/bin/bash


psql -c "REVOKE CONNECT ON DATABASE sistemagestor FROM public;"

psql -c "SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'sistemagestor';"

echo "---Base de datos sistemagestor para entorno de Desarrollo---"
echo "Borrando base de datos devbd existente..."
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
PGPASSWORD="admin"
psql -h localhost -p 5432 -U postgres -d sistemagestor -f backup
echo "sistemagestor se cargó exitosamente."
