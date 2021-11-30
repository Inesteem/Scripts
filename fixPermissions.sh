#!/bin/bash


print_usage() {
  printf "Usage: -d destinationDir: to fix -s srcDir: compare" 
}


fixDir=""
cmpDir=""
askLevel=-1
quitLevel=-1
while getopts 'd:s:a:q:' flag; do
  case "${flag}" in
    d) fixDir="${OPTARG}" ;;
    s) cmpDir="${OPTARG}" ;;
    a) askLevel="${OPTARG}" ;;
    q) quitLevel="${OPTARG}" ;;
    *) print_usage
       exit 1 ;;
  esac
done

function parse {

  local fix="$1"
  local cmp="$2"
  local level="$3"

  for d in $(ls -a ${fix}); do
    if [[ "$d" = "." ]] || [[ "$d" = ".." ]]; then
      continue;
    fi
    local fixPath="${fix}/$d"
    local cmpPath="${cmp}/$d"
    if [[ -d ${fixPath} ]] && [[ -d ${cmpPath} ]]; then
      [ "${level}" = "${askLevel}" ] && echo "setting permissions of $fixPath to permissions of $cmpPath"
      sudo chmod --reference="$cmpPath" "$fixPath"

      if [[ "${level}" = "${quitLevel}" ]]; then
        continue
      fi
      if [[ "${level}" = "${askLevel}" ]]; then
        read -p "Continue? (Y/N): " confirm
        if [[ $confirm == [yY] ]] || [[ $confirm == [yY][eE][sS] ]]; then
          parse $fixPath $cmpPath $((level+1))
        fi
      else
          parse $fixPath $cmpPath $((level+1))
      fi
    elif [[ -f ${fixPath} ]] && [[ -f ${cmpPath} ]]; then
      [ "${level}" = "0" ] && echo "setting permissions of $fixPath to permissions of $cmpPath"
      sudo chmod --reference="$cmpPath" "$fixPath"
    fi
  done
}

if [[ -z ${fixDir} ]] || [[ -z ${cmpDir} ]] || [[ ! -d ${fixDir} ]] || [[ ! -d ${fixDir} ]]; then
  echo "wrong input; maybe one path is not a dir?"
  exit -1
elif [[ "${fixDir}" = "${cmpDir}" ]]; then
  echo "fix and cmp dir should not be identical"
  exit -1
fi

parse ${fixDir} ${cmpDir} 0

