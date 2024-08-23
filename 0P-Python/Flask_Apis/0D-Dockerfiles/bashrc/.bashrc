# para compatibilidad con distribuciones Debian y derivados de esta '.bashrc'
## BEGIN alias for run and debug JavaScript
alias python='python3'

## END   alias for python
# set view path in propmt, con color
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:[\[\033[01;34m\]\W\[\033[00m\]]\$ '
# set view path in propmt, sin color
#PS1='${debian_chroot:+($debian_chroot)}\u@\h:\W\$ '

alias cds='cd /home/user/'
alias log='cd /home/user/logs'

