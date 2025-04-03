#/bin/sh
echo "  _______        _                 _     ________   __   ___  _____ "
echo " |__   __|      | |     /\        | |   |  ____\ \ / /  / _ \| ____|"
echo "    | | _____  _| |_   /  \   _ __| |_  | |__   \ V /  | (_) | |__  "
echo "    | |/ _ \ \/ / __| / /\ \ | '__| __| |  __|   > <    \__, |___ \ "
echo "    | |  __/>  <| |_ / ____ \| |  | |_  | |     / . \     / / ___) |"
echo "    |_|\___/_/\_\\__/_/    \_\_|   \__| |_|    /_/ \_\   /_/ |____/ "
echo ""

if [ $# -ne 2 ]; then
  echo "Usage: $0 <IP serveur TextArt FX 95> <image>"
  exit 1
fi

res_path="tmp.bmp"
convert "$2" -resize 22x22^ -format bmp .tmp.bmp
output=$(base64 -w 0 .tmp.bmp)
rm .tmp.bmp
echo "$output" | nc $1 2222
echo "Conversion terminée avec succès."
