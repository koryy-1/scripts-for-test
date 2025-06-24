#!/bin/bash

set -e

for unit in $(systemctl list-units --type=service | grep foobar- | awk '{print $1}'); do
    echo "Останавливаем $unit"
    systemctl stop "$unit"

    name=$(echo "$unit" | sed 's/foobar-//' | sed 's/\.service//')
    old_dir="/opt/misc/$name"
    new_dir="/srv/data/$name"

    echo "Перемещаем $old_dir -> $new_dir"
    mv "$old_dir" "$new_dir"

    unit_file="/etc/systemd/system/$unit"

    sed -i "s|WorkingDirectory=/opt/misc/$name|WorkingDirectory=$new_dir|" "$unit_file"
    sed -i "s|ExecStart=/opt/misc/$name/foobar-daemon|ExecStart=$new_dir/foobar-daemon|" "$unit_file"

    echo "Перезапускаем $unit"
    systemctl daemon-reexec
    systemctl daemon-reload
    systemctl start "$unit"
done