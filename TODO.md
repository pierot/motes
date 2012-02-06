TODOS
=====

* Homebrew installation
* https://github.com/kennethreitz/clint
* (X) python 2.7.x minimum?
* autocomplete when not giving mote name with command 'open' (http://bash-completion.alioth.debian.org/)
* (X) https://github.com/amoffat/pbs
* DocumentUp (http://documentup.com/#section-5-3)
* import option, Evernote import support ?

import readline
def completer(text, state):
    options = [x in addrs where x.startswith(text)]
    if state < options.length:
        return options[state]
    else
        return None
readline.set_completer(completer)
