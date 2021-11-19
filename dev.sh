#!/bin/bash

#prompt$ sh dev.sh

echo "Borrando base de datos desarrollo..."

psql -c "REVOKE CONNECT ON DATABASE desarrollo FROM public;"

psql -c "SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'desarrollo';"

dropdb -i --if-exists desarrollo
if [ "$?" -ne 0 ]
then
    echo -e "No se pudo borrar la base de datos desarrollo, verifique que no esté siendo usada."
    exit 1
fi
echo "Se ha borrado la base de datos desarrollo."
echo "Creando la base de datos desarrollo..."
createdb desarrollo
if [ "$?" -ne 0 ]
then
    echo -e "No se pudo crear desarrollo"
    exit 2
fi
echo "Se ha creado desarrollo"

#source venv/bin/activate
POSTGRES_PASS="postgres"
PGPASSWORD="postgres"
psql -h localhost -p 5432 -U postgres -d desarrollo -f /home/sole/Documentos/is2_014/backup
echo "desarrollo se cargó exitosamente."
