#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
queries=(
 "everquest planes of power saryrn"
 "everquest planes of power solusek ro"
 "everquest planes of power flagging"
 "everquest planes of power aerin dar"
 "everquest planes of power plane of time raid"
 "everquest planes of power xegony"
 "everquest planes of power coirnav"
 "everquest planes of power fennin ro"
 "everquest planes of power agnarr storm lord"
 "everquest planes of power bertoxxulous"
 "everquest planes of power terris thule"
 "everquest planes of power grummus"
 "everquest planes of power zek tactics"
 "everquest planes of power halls of honor trials"
 "everquest planes of power plane of justice"
 "everquest planes of power manaetic behemoth"
 "everquest planes of power lord marr"
)
for q in "${queries[@]}"; do
  n=$(echo "$q" | tr ' ' '_')
  curl -s --max-time 20 -A "$UA" "https://www.youtube.com/results?search_query=$q" -o "yt/$n.html" &
done
mkdir -p yt
wait
for q in "${queries[@]}"; do
  n=$(echo "$q" | tr ' ' '_')
  mkdir -p yt; curl -s --max-time 20 -A "$UA" "https://www.youtube.com/results?search_query=$q" -o "yt/$n.html" &
done
wait
ls yt/ | wc -l
