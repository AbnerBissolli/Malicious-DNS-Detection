from IPy import IP
from tld import parse_tld

def ip_check(s):
    try:
        IP(s)
        return 1
    except:
        return 0


def parse_domain(s):
    if ip_check(s):
        return  ('', '', '')
        
    parse = parse_tld(s, fix_protocol=True)
    if parse == (None, None, None):
        return ('', s, '')
    return parse

def get_ssd(t):
    if t[1] == '':
        return t[2]
    elif t[2] == '':
        return t[1]
    else:
        return t[2]+'.'+t[1]
    
def get_sub(t):
    return t[2]

def get_sld(t):
    return t[1]

def get_tld(t):
    return t[0]


def attribute_gen(df):
    df['ip_format'] = df['domain'].apply(ip_check)
    df['parse'] = df['domain'].apply(parse_domain)
    df['SSD'] = df['parse'].apply(get_ssd)
    df['SUB'] = df['parse'].apply(get_sub)    
    df['SLD'] = df['parse'].apply(get_sld)    
    df['TLD'] = df['parse'].apply(get_tld)

    df = df.drop(columns=['parse'])
    return df