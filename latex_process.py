import numpy as np
import string
########
def tail_str_edit(data:str)->str:
    """check end of string if `\#}` and edit"""
    if data[-3:] == u'\\#}':
        return data[:-3] + u'}'
    else:  # mormal
        return data[:-2]

def find_en_word(data:str):
    ind = 0
    ind_fa_last = 0
    ind_en_first = -1  # Not find yet
    for ind in range(len(data)):
        if data[ind] in fa_chars:
            ind_fa_last = ind
        elif data[ind] in en_chars:  ##### future : special chars
            ind_en_first = ind
            break
    return ind_en_first, ind_fa_last

def find_fa_word(data:str):
    ind = 0
    ind_en_last = 0
    ind_fa_first = -1  # Not find yet
    for ind in range(len(data)):
        if data[ind] in en_chars:
            ind_en_last = ind
        elif data[ind] in fa_chars:  ##### future : special chars
            ind_fa_first = ind
            break
    return ind_fa_first, ind_en_last


def find_spec_chr(data:str):
    ind = 0
    ind_spec_first = -1
    is_equation = 1  # there is no equation, just a single spec chr
    for ind in range(len(data)):
        if data[ind] in special_chars:
            ind_spec_first = ind
            if data[ind] == u'$':
                dollar_ind_next = data.find('$', ind+1)  # find next `$` in text
                if dollar_ind_next == -1:  # there is no `$` in text rest
                    return ind_spec_first, is_equation
                else:  # check all chars between 2 `$` are not farsi
                    for i in range(ind, dollar_ind_next):
                        if data[i] in fa_chars:
                            return ind_spec_first, is_equation
                    # all chars between 2 `$` are not farsi
                    is_equation = dollar_ind_next - ind +1  # equation length
                    return ind_spec_first, is_equation
            else:  # is not equation
                return ind_spec_first, is_equation
    return ind_spec_first, is_equation

def all_spec_chr(data:str)->str:
    """find all intervals of special characters. equations have different head and tail but others have same.
    for example: data= `hello #akbar eq:$x^y=\\frac{z}{x}$`
    """
    spec_loc = []  # list of all location tuples
    ind = 0
    while ind < len(data):
        tmp_start, tmp_length = find_spec_chr(data[ind:])
        if tmp_start == -1:
            break
        else:
            spec_loc.append((tmp_start + ind, tmp_length))
            ind += tmp_length + tmp_start
    return spec_loc


## very simple aleternate
def norm2latex_alt(data:str)->str:
    len_data = len(data)
    mode = 'fa'  # or 'en'
    data_out = ''
    ind = 0
    while True:
        if mode == 'fa':
            ind_en_first, ind_fa_last = find_en_word(data[ind:])
            if ind_en_first == -1:  # rest of text is farsi
                data_out += data[ind:]
                return data_out
            else:
                data_out += data[ind:ind+ind_en_first]
                ind += ind_en_first
                mode = 'en'
        elif mode == 'en':
            ind_fa_first, ind_en_last = find_fa_word(data[ind:])
            if ind_fa_first == -1:  # rest of text is english
                data_out += u'\lr{' + data[ind:] + u'}'
                return data_out
            else:
                data_out += u'\lr{' + data[ind:ind+ind_en_last+1] + u'}'
                ind += ind_en_last+1
                mode = 'fa'


def norm2latex(data):
    data += u'#'  # add manually specaial char to code work
    mode = 'fa'  # or 'en'
    data_out = ''
    ind = 0
    spec_list = np.array(all_spec_chr(data))
    while True:
        ind_oppos_first, ind_same_last = dict_find_en_fa[mode]['find_oppos'](data[ind:])
        if ind_oppos_first == -1:  # rest of text is in language `mode`
            if spec_list.size>0:  # empty or not
                spec_loc = spec_list - ind * np.array([1,0]).reshape(1,2)  # to normalize
                tmp_data = convert_spec2latex(data[ind:], spec_loc)
            else:
                tmp_data = data[ind:]
            data_out += tmp_data if mode == 'fa' else u'\lr{' + tmp_data + u'}'
            return tail_str_edit(data_out)
        else:
            ind_spec = ind  # copy of index
            spec_2opp_count = 0  # number of special chars between now and first oppos char
            while True:
                ind_oppos_first, ind_same_last = dict_find_en_fa[mode]['find_oppos'](data[ind_spec:])
                if ind_oppos_first == -1:  # rest of text is in language `mode`
                    if spec_list.size>0:  # empty or not
                        spec_loc = spec_list - ind * np.array([1,0]).reshape(1,2)  # to normalize
                        tmp_data = convert_spec2latex(data[ind:], spec_loc)
                    else:
                        tmp_data = data[ind:]
                    data_out += tmp_data if mode == 'fa' else u'\lr{' + tmp_data + u'}'
                    return tail_str_edit(data_out)
                ind_oppos_first = ind_oppos_first if mode=='fa' else ind_same_last+1
                # check `first_oppos cahr` is in special string intervals or not.
                tmp_spec = spec_list[spec_list[:,0]< ind_spec+ind_oppos_first]
                tmp_spec[:,0] = ind_spec+ind_oppos_first - tmp_spec[:,0]
                tmp_spec = tmp_spec @ np.array([[1],[-1]])
                spec_2opp_count = tmp_spec.shape[0]  # increase spec chars
                if (tmp_spec >=0).all():  # valid position i.e. first oppos char is out of special intervals
                    if tmp_spec.size>0:  # empty or not
                        spec_loc = spec_list[:spec_2opp_count,:] - ind * np.array([1,0]).reshape(1,2)  # to normalize
                        tmp_data = convert_spec2latex(data[ind:ind_spec+ind_oppos_first], spec_loc)
                    else:
                        tmp_data = data[ind:ind_spec+ind_oppos_first]
                    data_out += tmp_data if mode == 'fa' else u'\lr{' + tmp_data + u'}'
                    ind = ind_spec + ind_oppos_first
                    spec_list = spec_list[spec_2opp_count:]
                    break
                # invalid position i.e. first oppos char in one of special intervals
                # spec_2opp_count: index of spec interval has first oppos char
                ind_spec = spec_list[spec_2opp_count-1,:].sum()  # update index to be search
            mode = 'fa' if mode=='en' else 'en'
    return data_out


def convert_spec2latex(data:str, spec_loc:np.ndarray)->str:
    """convert """
    data_out = ''
    ind = 0
    for i in range(spec_loc.shape[0]):
        data_out += data[ind: spec_loc[i, 0]]
        if spec_loc[i,1] > 1:  # equation
            data_out += data[spec_loc[i,0]:spec_loc[i,:].sum()]
            ind = spec_loc[i,:].sum()
        else:  # single spec char
            if data[spec_loc[i,0]] in trans_spec_chr:  # must use latex command
                data_out += trans_spec_chr[data[spec_loc[i,0]]]
            else:  # e.g. \# \&
                data_out += u'\\' + data[spec_loc[i,0]]
            ind = spec_loc[i,:].sum()
    data_out += data[ind:]
    return data_out


######
def find_back_comment(data:str):
    """find first `\` or `%` in  `data`
        output: (ind, type). type: 1:`\` 2:`%` 0: nothing"""
    for i in range(len(data)):
        if data[i] == u'\\':
            return (i, 1)  # 1: means `\`
        elif data[i] == u'%':
            return (i, 2)  # 2: means `%`
    return (-1, 0)

def comm_latx_length(data:str, back_ind=0):
    """find length and type of latex command e.g. `\lr{}`
        output: (command_length, brace_ind)
        `brace_ind`: which index of command has `{` (-1:no`{`)."""
    command = ''
    enter_pressed = 0  # `\n` used or not. JUST one `\n` can be use between `command` and `{`
    end_command = 0  # `command` has ended or not (before ` ` or `%{`)
    # loop
    ind = back_ind + 1
    while ind <len(data):
        char = data[ind]
        if end_command == 0:
            if char in special_chars+u',;' and len(command)==0:
                return (1, -1)  # e.g. `\#`
            elif char == u'{':
                return (len(command), ind)
            elif char == u' ':
                end_command = 1
            elif char == u'\n':
                end_command = 1
                enter_pressed += 1
            elif char == u'%':  # skip comments
                end_command = 1
                tmp_ind = data.find(u'\n', ind)
                if tmp_ind == -1:  # rest of text is comment
                    return (len(command), -1)
                else:
                    enter_pressed += 1
                    ind = tmp_ind
            else:  # regular char e.g. `a`
                command += char
            ind += 1
        else:  # command has ended
            if char == u'{':
                return (len(command), ind)
            elif char == u' ':
                pass  # just continue!
            elif char == u'\n':
                enter_pressed += 1
                if enter_pressed > 1:
                    return (len(command), -1)
            elif char == u'%':  # skip comments
                tmp_ind = data.find(u'\n', ind)
                if tmp_ind == -1:  # rest of text is comment
                    return (len(command), -1)
                else:
                    ind = tmp_ind
            else:  # regular char e.g. `a` => end command
                return (len(command), -1)
            ind += 1
    return (len(command), -1)

def find_inv_brace(data:str)->int:
    ind = 0
    brace_count = 1
    while ind < len(data):
        if data[ind] == u'{':
            brace_count += 1
        elif data[ind] == u'}':
            brace_count -= 1
        elif data[ind] == u'%':
            ind = data.find('\n', ind)
            if ind == -1:
                return -1
        if brace_count == 0:  # parsed
            return ind
        ind += 1
    return -1

## latex to noraml function
def latex2norm(data:str)->str:
    """convert latex text to normal text"""
    data_out = u''
    ind = 0
    while ind < len(data):
        intrp_ind, intrpt_type = find_back_comment(data[ind:])
        if intrpt_type == 0:  # rest of text has no interrupt
            return data_out + data[ind:]
        elif intrpt_type == 1:  # `\` => command
            comm_len, brace_ind = comm_latx_length(data, ind+intrp_ind)
            data_out += data[ind: ind+intrp_ind]
            command_lat = data[ind+intrp_ind+1: ind+intrp_ind+comm_len+1]
            if comm_len == 0:
                data_out += u' '
                ind += intrp_ind + 2
            elif comm_len == 1:
                if command_lat in special_chars:
                    data_out += command_lat
                    ind += intrp_ind + 2
                else:  # e.g. `\,`
                    data_out += u'\\'+command_lat
                    ind += intrp_ind + 2
            elif command_lat in ['textasciitilde', 'textbackslash', 'textasciicircum']:
                data_out += trans_spec_chr_inv[command_lat]
                ind += intrp_ind + comm_len + 1
            elif brace_ind == -1:  # no `{` => rewrite
                data_out += u'\\'+command_lat
                ind += intrp_ind + comm_len + 1
            elif command_lat == u'lr':
                ind_inv = find_inv_brace(data[brace_ind+1:])
                if ind_inv == -1:
                    data_out += u'\\lr{'
                    ind = brace_ind + 1
                else:
                    ind = brace_ind + 1
                    data_out += latex2norm(data[ind: ind+ind_inv])
                    ind += ind_inv +1
        else:  # `%` => comment
            data_out += data[ind: ind+intrp_ind]
            ind = data.find('\n', ind+intrp_ind) + 1  # go to next line
    return data_out




## change 
def number_fa2en(data:str)->str:
    ar2en_trans = str.maketrans(arabic_numbers, english_numbers)
    fa2en_trans = str.maketrans(persian_numbers, english_numbers)
    data = data.translate(ar2en_trans)
    data = data.translate(fa2en_trans)
    return data


def number_en2fa(data)->str:
    ar2fa_trans = str.maketrans(arabic_numbers, persian_numbers)
    en2fa_trans = str.maketrans(english_numbers, persian_numbers)
    data = data.translate(ar2fa_trans)
    data = data.translate(en2fa_trans)
    return data


def lang_chars():
    en_chars = string.ascii_letters + string.digits
    first_chr_fa = u'\u0600'
    last_chr_fa = u'\u06FF'
    fa_chars = ''
    for chr_ord in range(ord(first_chr_fa), ord(last_chr_fa)+1):
        fa_chars = fa_chars + chr(chr_ord)
    return en_chars, fa_chars

# Always must run
special_chars = '&%$#_{}~^\\'  # special charaacters in LaTeX
trans_spec_chr = {u'\\':u'\\textbackslash', u'~':u'\\textasciitilde', u'^':u'\\textasciicircum'}
trans_spec_chr_inv = {u'textbackslash':u'\\', u'textasciitilde':u'~', u'textasciicircum':u'^'}
en_chars, fa_chars = lang_chars()
persian_numbers = u'۱۲۳۴۵۶۷۸۹۰'
english_numbers = u'1234567890'
arabic_numbers  = u'١٢٣٤٥٦٧٨٩٠'
dict_find_en_fa = {'en':{'find_same':find_en_word,'find_oppos':find_fa_word}, 'fa':{'find_same':find_fa_word,'find_oppos':find_en_word}}