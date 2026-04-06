from collections import namedtuple

FormatLabelsGroup = namedtuple('FormatLabelsGroup',[
        'admin',
        'client',
        'programmer'
    ]
)

GROUPS:FormatLabelsGroup = FormatLabelsGroup(
    'Administrador',
    'Cliente',
    'Programador'
)

PERMISSION:FormatLabelsGroup = FormatLabelsGroup(
    'admin',
    'register',
    'attend'
)
                        
