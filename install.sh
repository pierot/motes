#!/usr/bin/env bash

DIR=$(cd $(dirname "$0"); pwd)

echo "This will install Motes on your system."
echo "(This method is intented for local dev usage)"

while true
do
  read -p "Proceed? (y/n) " RESP

  case $RESP
    in
    [yY])
      ln -sf "$DIR/bin/motes" /usr/local/bin/motes

      break
      ;;
    [nN])
      break
      ;;
    *)
      echo "Please enter y or n."
  esac
done

