#!/bin/bash

echo "Borrando base de datos produccion..."

psql -c "REVOKE CONNECT ON DATABASE produccion FROM public;"

psql -c "SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'produccion';"

dropdb -i --if-exists produccion
if [ "$?" -ne 0 ]
then
    echo -e "No se pudo borrar la base de datos produccion, verifique que no esté siendo usada."
    exit 1
fi


echo "Se ha borrado la base de datos produccion."
echo "Creando la base de datos produccion..."
createdb produccion
if [ "$?" -ne 0 ]
then
    echo -e "No se pudo crear produccion"
    exit 2
fi
echo "Se ha creado produccion"

#source venv/bin/activate
POSTGRES_PASS="postgres"
psql -h localhost -p 5432 -U postgres -d produccion -f backupProdu
echo "produccion se cargó exitosamente."
