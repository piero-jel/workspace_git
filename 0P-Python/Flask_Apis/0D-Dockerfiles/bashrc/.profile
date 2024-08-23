# para compatibilidad con distribuciones alpine '.profile'
## BEGIN alias for run and debug JavaScript
alias run='node'
alias debug='node inspect'
## END   alias for python
# set view path in propmt, con color
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:[\[\033[01;34m\]\W\[\033[00m\]]\$ '
# set view path in propmt, sin color
#PS1='${debian_chroot:+($debian_chroot)}\u@\h:\W\$ '

alias cds='cd /home/user/0E-Examples'
alias emul='cd /home/user/0E-Examples/0E-Emulator'
# alias curr='cd /home/user/0E-Examples/0F-Files'
alias curr='cd /home/user/0E-Examples/0P-Promise'

