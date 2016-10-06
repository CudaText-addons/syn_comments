''' Plugin for SynWrite
Authors:
    Andrey Kvichansky (kvichans on github.com)
    Alexey T. (SynWrite)
'''

import  os
import  sw            as app
from    sw        import ed

fn_config = os.path.join(app.app_ini_dir(), 'syn_comments.ini')
op_keep_column = False
op_equal_column = True
op_full_line_if_no_sel = False
op_move_down = False

class Command:
    def __init__(self):
        self.pair4lex = {}

    def do_save_ops(self):
        app.ini_write(fn_config, 'op', 'keep_column', '1' if op_keep_column else '0')
        app.ini_write(fn_config, 'op', 'equal_column', '1' if op_equal_column else '0')
        app.ini_write(fn_config, 'op', 'full_line_if_no_sel', '1' if op_full_line_if_no_sel else '0')
        app.ini_write(fn_config, 'op', 'move_down', '1' if op_move_down else '0')

    def do_load_ops(self):
        op_keep_column = app.ini_read(fn_config, 'op', 'keep_column', '0') == '1'
        op_equal_column = app.ini_read(fn_config, 'op', 'equal_column', '0') == '1'
        op_full_line_if_no_sel = app.ini_read(fn_config, 'op', 'full_line_if_no_sel', '0') == '1'
        op_move_down = app.ini_read(fn_config, 'op', 'move_down', '0') == '1'

    def dlg_config(self):
        self.do_save_ops()
        app.file_open(fn_config)


    def cmt_toggle_line_1st(self):
        return self._cmt_toggle_line('bgn', '1st')
    def cmt_add_line_1st(self):
        return self._cmt_toggle_line('add', '1st')
    def cmt_toggle_line_body(self):
        return self._cmt_toggle_line('bgn', 'bod')
    def cmt_add_line_body(self):
        return self._cmt_toggle_line('add', 'bod')
    def cmt_del_line(self):
        return self._cmt_toggle_line('del')


    def _cmt_toggle_line(self, cmt_act, cmt_type=''):
        ''' Add/Remove full line comment
            Params
                cmt_act     'del'   uncomment all lines
                            'add'   comment all lines
                            'bgn'   (un)comment all as toggled first line
                cmt_type    '1st'   at begin of line
                            'bod'   at first not blank
        '''
        self.do_load_ops()
        lex         = ed.get_prop(app.PROP_LEXER_CARET)
        cmt_sgn     = app.lexer_proc(app.LEXER_GET_COMMENT, lex)
        if not cmt_sgn:
            return app.msg_status('No line comment for lexer "%s"' % lex)
        # Analize

        x0, y0 = ed.get_caret_xy()
        line1, line2 = ed.get_sel_lines()
        rWrks = list(range(line1, line2+1))
        bEmpSel = ed.get_text_sel()==''

        do_uncmt    = ed.get_text_line(line1).lstrip().startswith(cmt_sgn) \
                        if cmt_act=='bgn' else \
                      True \
                        if cmt_act=='del' else \
                      False
        # Work
        col_min_bd  = 1000 # infinity
        if op_equal_column:
            for rWrk in rWrks:
                line        = ed.get_text_line(rWrk)
                pos_body    = line.index(line.lstrip())
                pos_body    = len(line) if 0==len(line.lstrip()) else pos_body
                col_min_bd  = min(pos_body, col_min_bd)
                if 0==col_min_bd:
                    break # for rWrk
        blnks4cmt   = ' '*len(cmt_sgn) # '\t'.expandtabs(len(cmt_sgn))

        for rWrk in rWrks:
            line    = ed.get_text_line(rWrk)
            pos_body= line.index(line.lstrip())
            pos_body= len(line) if 0==len(line.lstrip()) else pos_body
            if do_uncmt:
                # Uncomment!
                if not line[pos_body:].startswith(cmt_sgn):
                    # Already no comment
                    continue    #for rWrk
                if False:pass
                elif len(line)==len(cmt_sgn): # and line.startswith(cmt_sgn)
                    line = ''
                elif op_keep_column and (' '==line[0] or
                                      ' '==line[pos_body+len(cmt_sgn)]):
                    # Before or after cmt_sgn must be blank
                    line = line.replace(cmt_sgn, blnks4cmt, 1)
                else:
                    line = line.replace(cmt_sgn, ''       , 1)
            else:
                # Comment!
                if cmt_type=='bod' and line[pos_body:].startswith(cmt_sgn):
                    # Body comment already sets - willnot double it
                    continue    #for rWrk
                if False:pass
                elif cmt_type=='1st' and op_keep_column and line.startswith(blnks4cmt) :
                    line = line.replace(blnks4cmt, cmt_sgn, 1)
               #elif cmt_type=='1st' and op_keep_column #  !line.startswith(blnks4cmt) :
                elif cmt_type=='1st':#  !op_keep_column
                    line = cmt_sgn+line
                elif cmt_type=='bod' and op_keep_column and line.startswith(blnks4cmt):
                    pos_cmnt = col_min_bd if op_equal_column else pos_body
                    pass;          #LOG and log('pos_cmnt={}', (pos_cmnt))
                    if pos_cmnt>=len(cmt_sgn):
                        line = line[:pos_cmnt-len(cmt_sgn)]+cmt_sgn+line[pos_cmnt:             ]
                    else:
                        line = line[:pos_cmnt             ]+cmt_sgn+line[pos_cmnt+len(cmt_sgn):]
                   #line = line[:pos_cmnt-len(cmt_sgn)]+cmt_sgn+line[pos_cmnt:]
                   #line = line[:pos_body-len(cmt_sgn)]+cmt_sgn+line[pos_body:]
               #elif cmt_type=='bod' and op_keep_column #  !line.startswith(blnks4cmt) :
                elif cmt_type=='bod':#  !op_keep_column
                    pos_cmnt = col_min_bd if op_equal_column else pos_body
                    pass;      #LOG and log('pos_cmnt={}', (pos_cmnt))
                    line = line[:pos_cmnt]             +cmt_sgn+line[pos_cmnt:]
                   #line = line[:pos_body]             +cmt_sgn+line[pos_body:]

            pass;              #LOG and log('new line={}', (line))
            ed.set_text_line(rWrk, line)
            #for rWrk
        if bEmpSel and op_move_down:
            ed.set_caret_xy(x0, y0+1)
       #def _cmt_toggle_line


    def cmt_toggle_stream(self):

        if ed.get_sel_mode() != app.SEL_NORMAL:
            return app.msg_status('Comment needs normal selection')
        lex = ed.get_prop(app.PROP_LEXER_CARET)
        ((str1, str2), bFull) = self._get_cmt_pair(lex)
        if not str1:
            return app.msg_status('No range-comments for lexer: '+lex)

        text_sel = ed.get_text_sel()
        if not text_sel:
            return app.msg_status('Comment needs selection')
        pos1, nlen = ed.get_sel()

        if bFull:
            text_sel = text_sel.strip('\n\r')

        if text_sel.startswith(str1):
            #uncomment
            text_sel = text_sel[len(str1):-len(str2)]
            if bFull:
                text_sel = text_sel.strip('\n\r')
        else:
            #comment
            if bFull:
                eol = ed.get_prop(app.PROP_EOL)
                text_sel = str1+eol+text_sel+eol+str2+eol
            else:
                text_sel = str1+text_sel+str2

        ed.replace(pos1, nlen, text_sel)
        ed.set_sel(pos1, len(text_sel))
        app.msg_status('Toggled stream comment')
       #def cmt_toggle_stream

    def _get_cmt_pair(self, lex):
        ''' Return ((begin_sign, end_sign), only_lines)
                begin_sign    as '/*'
                end_sign      as '*/'
                only_lines    True if each of *_sign must be whole line
        '''
        if lex not in self.pair4lex:
            only_ln = False
            pair1 = app.lexer_proc(app.LEXER_GET_COMMENT_STREAM, lex)
            pair2 = app.lexer_proc(app.LEXER_GET_COMMENT_LINED, lex)
            if pair1 is not None: pair = pair1
            elif pair2 is not None: pair = pair2; only_ln = True
            else: pair = ('', '')
            self.pair4lex[lex] = (pair, only_ln)
        return self.pair4lex[lex]
       #def _get_cmt_pair

