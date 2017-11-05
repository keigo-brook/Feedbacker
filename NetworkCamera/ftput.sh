set -ex
file=$1
ftp -nv <<END
open localhost 18888
user user pass
cd /test
binary
prompt
put $file
END

