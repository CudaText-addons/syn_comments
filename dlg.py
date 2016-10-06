from sw import *

def dialog_config(
    op_keep_column,
    op_equal_column,
    op_full_line_if_no_sel,
    op_move_down):

    id_keep = 0
    id_equal = 1
    id_full = 2
    id_down = 3
    id_ok = 4

    c1 = chr(1)
    text = '\n'.join([]
        +[c1.join(['type=check', 'pos=6,6,500,0', 'cap=(Line commands) Try to keep text position after (un)commenting',
                   'val='+('1' if op_keep_column else '0') ])]
        +[c1.join(['type=check', 'pos=6,28,500,0', 'cap=(Line at non-space) If selected few lines, insert comment at maximal common indent',
                   'val='+('1' if op_equal_column else '0') ])]
        +[c1.join(['type=check', 'pos=6,50,500,0', 'cap=(Stream) Comment full line if no selection',
                   'val='+('1' if op_full_line_if_no_sel else '0') ])]
        +[c1.join(['type=check', 'pos=6,72,500,0', 'cap=(All) Move caret to next line',
                   'val='+('1' if op_move_down else '0') ])]
        +[c1.join(['type=button', 'pos=290,100,390,0', 'cap=&OK', 'props=1'])]
        +[c1.join(['type=button', 'pos=396,100,496,0', 'cap=Cancel'])]
    )

    res = dlg_custom('Comments options', 502, 130, text)
    if res is None:
        return

    res, text = res
    text = text.splitlines()

    if res != id_ok:
        return

    op_keep_column = text[id_keep]=='1'
    op_equal_column = text[id_equal]=='1'
    op_full_line_if_no_sel = text[id_full]=='1'
    op_move_down = text[id_down]=='1'

    return (op_keep_column, op_equal_column, op_full_line_if_no_sel, op_move_down)
