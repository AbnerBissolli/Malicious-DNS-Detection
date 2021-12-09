from whois import whois
from ipwhois import IPWhois
import datetime
import numpy as np
import enchant
import pandas as pd
from tld import parse_tld
from scipy.stats import entropy
from collections import Counter

def ip_check(s):
    try:
        IP(s)
        return 1
    except:
        return 0

def try_whois(s):
    try:
        return whois(s)
    except:
        return 0       

def try_ipwhois(s):
    try:
        return IPWhois(s).lookup_whois()
    except:
        return 0 
    
def get_cdt(s):
    if ip_check(s):
        return try_ipwhois(s)
    else:
        return try_whois(s)

##########################################

def get_sld_from_s(s):
    parse = parse_tld(s, fix_protocol=True)
    return parse[1]


def get_famous_domains():
	alexa_rank = pd.read_csv('../Dataset/Alexa Rank/top-1m.csv', header=None)
	alexa_rank.columns = ['rank', 'domain']

	alexa_rank['SLD'] = alexa_rank['domain'].apply(get_sld_from_s)
	famous_domains = list(alexa_rank['SLD'].drop_duplicates())[:1000]
	return famous_domains

################################################################
def is_private(s):
    privacy_strings = ['REDACTED FOR PRIVACY',
                       'REDACTED FOR PRIVACY REDACTED FOR PRIVACY',
                       'REDACTED_FOR_PRIVACY, REDACTED_FOR_PRIVACY, REDACTED_FOR_PRIVACY',
                       'REDACTED_FOR_PRIVACY',
                       'Redacted for privacy',
                       'Redacted for GDPR privacy',
                      ]
    if s in privacy_strings:
        return 1
    return 0

def privacy_check_lst(items):
    for item in items:
        if isinstance(item, list):
            privacy_check_lst(item)
        elif isinstance(item, dict):
            privacy_check_dic(item)
        elif isinstance(item, str) and is_private(item):
            return 1
    return 0

def privacy_check_dic(dic):
    keys = dic.keys()
    for key in keys:
        if isinstance(dic[key], dict):
            if privacy_check_dic(dic[key]):
                return 1
        else:
            if isinstance(dic[key], list):
                items = dic[key]
            else:
                items = [dic[key]]
                
            if privacy_check_lst(items):
                return 1
    return 0

def privacy_check(var):
    if isinstance(var, dict):
        return privacy_check_dic(var)
    return 0

################################################################
def item_is_valid(item):
    if is_private(item):
        return 0
    if item is None:
        return 0
    return 1      
    
def get_field_lst(items, key, field):
    count = 0
    for item in items:
        if isinstance(item, dict):
            count += get_field_dic(item, field)
        else:
            if not field in key:
                return 0
            else:
                count += item_is_valid(item)
    return count

def get_field_dic(dic, field):
    count = 0
    keys = dic.keys()
    for key in keys:
        if isinstance(dic[key], dict):
            count += get_field_dic(dic[key], field)
        else:
            if isinstance(dic[key], list):
                items = dic[key]
            else:
                items = [dic[key]]
            
            count += get_field_lst(items, key, field)
    return count
                
def get_field(var, field):
    if isinstance(var, dict):
        return get_field_dic(var, field)
    return 0

################################################################

def get_connection(var):
    if var == 0:
        return 0
    return 1

def get_name(var):
    field = 'name'
    count = get_field(var, field)
    return count

def get_address(var):
    field = 'address'
    count = get_field(var, field)
    return count

def get_state(var):
    field = 'state'
    count = get_field(var, field)
    return count

def get_country(var):
    field = 'country'
    count = get_field(var, field)
    return count

def get_server(var):
    field = 'server'
    count = get_field(var, field)
    return count

def get_email(var):
    field = 'email'
    count = get_field(var, field)
    return count

def get_registrar(var):
    field = 'registrar'
    count = get_field(var, field)
    return count

def get_registrant(var):
    field = 'registrant'
    count = get_field(var, field)
    return count

def get_org(var):
    field = 'org'
    count = get_field(var, field)
    return count

#################################################################
def append(lst, new):
    if isinstance(new, list):
        ret = lst + new
    else:
        ret = lst + [new]    
    ret = filter(None.__ne__, ret)
    ret = list(ret)
    return ret

################################################################
def extract_year(date):
    if isinstance(date, datetime.datetime):
        return date.year
    
    
    if isinstance(date, str):
        year = re.sub("[^0-9]", "", date)
        if date[0] == '0':
            year = year[1:5]
        else:
            year = year[:4]
        
        year = int(year)
        if year < 1900 or year > 2021:
            return 0
        return(year)
    else:
        print(date, type(date))
        print("BIG ERROR")

################################################################  

def get_creation(dic):
    creations = []
    if dic == 0:
        return 0
    elif 'creation_date' in dic:
        creation = dic['creation_date']
        creations = append(creations, creation)
    elif 'nets' in dic:
        for net in dic['nets']:
            creation = net['created']
            creations = append(creations, creation)

    if len(creations) == 0:
        return 0
    
    creations = list(filter(('REDACTED FOR PRIVACY').__ne__, creations))   
    if len(creations) == 0:
        return -1
    
           
    creations = [extract_year(creation) for creation in creations]                
          
    return min(creations)

################################################################

def get_age(creation_year):
    if creation_year <= 0:
        return 0
    current_year = datetime.datetime.today().year
    age = current_year-creation_year
    return age

################################################################

def get_no_slds(s, famous_domains):
    count = 0
    words = s.split('.')
    for word in words:
        if word in famous_domains:
            count+=1
    return count

################################################################

def get_sld_dst(s, famous_domains):
    min_dst = np.inf
    for famous_domain in famous_domains:
        dst = enchant.utils.levenshtein(s, famous_domain)
        min_dst = min(min_dst, dst)
    return min_dst

################################################################	



def feature_gen_tp(df):
	famous_domains = get_famous_domains()

	df['Third Party'] = df['domain'].apply(get_cdt)

	df['connection']   = df['Third Party'].apply(get_connection)
	df['privacy']      = df['Third Party'].apply(privacy_check)
	df['name']         = df['Third Party'].apply(get_name)
	df['address']      = df['Third Party'].apply(get_address)
	df['state']        = df['Third Party'].apply(get_state)
	df['country']      = df['Third Party'].apply(get_country)
	df['email']        = df['Third Party'].apply(get_email)
	df['servers']      = df['Third Party'].apply(get_server)
	df['registrar']    = df['Third Party'].apply(get_registrar)
	df['registrant']   = df['Third Party'].apply(get_registrant)
	df['org']          = df['Third Party'].apply(get_org)
	df['creation']     = df['Third Party'].apply(get_creation)
	df['age']          = df['creation'].apply(get_age)
	df['SLDs in SUB']  = df['SUB'].apply(get_no_slds, famous_domains=famous_domains)
	df['SLD Distance'] = df['SLD'].apply(get_sld_dst, famous_domains=famous_domains)

	return df


################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################

################################################################

def get_len(s):
    return len(s)

################################################################

def get_pct(s):
    numbers = sum(c.isdigit() for c in s)
    lenght  = len(s)
    if numbers == 0:
        return 0
    return numbers/lenght

################################################################

def get_nan(s):
    numbers = sum(c.isdigit() for c in s)
    letters = sum(c.isalpha() for c in s)    
    others  = len(s) - numbers - letters
    return others

################################################################

def get_etp(s):
    if s == '':
        return 0
    
    pd_series = pd.Series(list(s))
    counts = pd_series.value_counts()
    return entropy(counts)

################################################################

def get_nos(s):
    word_list =s.split('.')
    return len(word_list)

################################################################

def get_val_1(s):
    total = len(s) 
    if total == 0:
        return 0     
    
    s = sorted(Counter(s), key=Counter(s).get, reverse=True)
    
    count = 0 
    for c in s:
        count += s.count(c)
        if count/total > 0.5:
            return count
    return count

################################################################

def get_val_2(s):
    total = len(s) 
    if total == 0:
        return 0    
    
    s = sorted(Counter(s), key=Counter(s).get, reverse=True)

    count = 0   
    for c in s[:5]:
        count += s.count(c)
    return count/total

################################################################

def get_val_3(s):
    total = len(s) 
    if total == 0:
        return ''     
    
    s = sorted(Counter(s), key=Counter(s).get, reverse=True)
    return s[0]

################################################################
################################################################


from itertools import groupby

def dig_seq_l(s):
    if len(s) == 0:
        return 0
    
    res = [''.join(j).strip() for k, j in groupby(s, str.isdigit)]
    res = [sub for sub in res if sub.isdigit()]
    
    if len(res) == 0:
        return 0
    
    res = max(res, key = len)
    return len(res)


################################################################

def chr_seq_l(s):
    if len(s) == 0:
        return 0
    
    res = [''.join(g) for _, g in groupby(s)]
    res = max(res, key = len)
    return len(res)

################################################################

def chr_seq_c(s):
    if len(s) == 0:
        return ''    
    
    res = [''.join(g) for _, g in groupby(s)]
    res = max(res, key = len)
    return res[0]

################################################################

def get_words():	
	words_websites = ['facebook',
	                  'fb',
	                  'instagram',
	                  'tiktok',
	                  'whatsapp',
	                  'ibm',
	                  'google',
	                  'amazon',
	                  'windows',
	                  'linux',
	                  'messsenger',
	                  'microsoft',
	                  'twitter',
	                  'outlook',
	                  'apple',
	                  'netflix',
	                  'flix',
	                  'film',                  
	                  'prime',
	                  'ebay',
	                  'bunker',
	                  'play',
	                  'social',
	                  'paypal',
	                  'pypl',
	                  'win',
	                 ]

	words_reliable = ['account',
	                  'password',
	                  'passwd',
	                  'senha',
	                  'good',
	                  'secure',
	                  'security',
	                  'certified',
	                  'save',
	                  'safe',
	                  'download',
	                  'down',
	                  'com',
	                  'login',
	                  'register',
	                  'erro',
	                  'id',
	                  'update',
	                  'submit',
	                  'oficial',
	                  'official',
	                  'home',
	                  'app',                  
	                  'web',
	                  'lock',
	                  'app',
	                  'cancel',
	                  'mobile',
	                  'copy',
	                  'warning'
	                  'warn',
	                  'verification',
	                  'verif',
	                  'recovery',
	                  'recover',
	                  'stat',
	                  'email',
	                  'reliable',
	                  'support',
	                  'doc',
	                  'notification',
	                  'notif',                  
	                  'confirm',
	                  'key',
	                  'software',
	                  'beta',
	                  'alpha',
	                  'alfa',
	                  'user',
	                  'admin',
	                  'try',
	                  'veri',
	                  'service',
	                  'import',
	                  'true',
	                  'null',
	                  'my',
	                  'your',
	                  'link',
	                  'online',
	                  'sign',
	                  'prof',
	                  'profile',
	                  'group',
	                 ]

	words_catchy = ['bank',
	                'money',
	                'cash',
	                'game',
	                'ship',
	                'market',
	                'pay',
	                'new',
	                'apply',
	                'deal',
	                'get',
	                'now',
	                'start',
	                'act',
	                'free',
	                'gift',
	                'card',
	                'credit',
	                'hot',
	                'drug',
	                'porn',
	                'ero',
	                'euro',
	                'dolar',    
	                'ofer',
	                'offer',
	                'work',
	                'food',
	                'book',
	                'now',
	                'tech',
	                'shop',
	                'diet',
	                'clinic',
	                'office',
	                'blog',
	                'intern',
	                'first',
	                'act',
	                'refund',
	                'photo',
	                'gif',
	                'net',
	                'cloud',
	                'limit',
	                'vk',
	               ]

	words_bad = ['malware',
	             'spam',
	             'attack',
	             'phishing',             
	            ]

	words_countries = ['usa', 'unitedstates', 'united', 'states', 'america',
	                   'brasil', 'brazil', 'bra', 'br',
	                   'germany', 'ger', 'germ',
	                   'britain', 'british', 'uk', 'kingdom'                   
	                   'china', 'chi',
	                   'india', 'ind',
	                   'spain', 'sp',
	                   'italy',
	                   'france',
	                   'turkey',
	                   'poland',
	                   'russia', 'russ', 'rus',
	                   'canada', 'can',
	                   'southkorea', 'sk', 'south','korea',
	                   'taiwan',
	                   'japan', 'jp',
	                   'mexico', 'mex',
	                   'argentina', 'arg',
	                   'australia', 'aus',
	                   'israel', 'isr',
	                  ]

	words_rubbish = ['ww',
	                 'kkk',
	                 'www',
	                 'xxx',
	                 'yyy',
	                 'zzz',    
	                ]

	target_words = words_websites + words_reliable + words_catchy + words_bad + words_countries + words_rubbish
	bad_words = [ 'britain','yyy','poland','linux','ibm','porn','british','russia','japan','taiwan','spam','attack','canada','game','euro','official','xxx','kkk','film','argentina','france','play','mexico','united','blog','social','israel','software','russ','good','chi','australia','work','diet','new','food','alpha','sk','true','isr']

	return bad_words, target_words

def have_words(s, words):
    bad_words = 0
    for word in words:
        if word in s:
            bad_words +=1
    return bad_words

def have_words_rplc(s, words):
    s = s.replace('0', 'o')
    s = s.replace('1', 'i')
    s = s.replace('3', 'e')
    s = s.replace('4', 'a')
    s = s.replace('5', 's')
    s = s.replace('6', 'g')
    s = s.replace('7', 't')
    s = s.replace('8', 'b')
    s = s.replace('8', 'b')    
    
    bad_words = 0
    for word in words:
        if word in s:
            bad_words +=1
    return bad_words


def feature_gen_lx(df):
	df['SSD_len'] = df['SSD'].apply(get_len)
	df['SUB_len'] = df['SUB'].apply(get_len)
	df['SLD_len'] = df['SLD'].apply(get_len)

	df['SSD_pct'] = df['SSD'].apply(get_pct)
	df['SUB_pct'] = df['SUB'].apply(get_pct)
	df['SLD_pct'] = df['SLD'].apply(get_pct)

	df['SSD_nan'] = df['SSD'].apply(get_nan)
	df['SUB_nan'] = df['SUB'].apply(get_nan)
	df['SLD_nan'] = df['SLD'].apply(get_nan)

	df['SSD_etp'] = df['SSD'].apply(get_etp)
	df['SUB_etp'] = df['SUB'].apply(get_etp)
	df['SLD_etp'] = df['SLD'].apply(get_etp)

	df['SUB_num'] = df['SUB'].apply(get_nos)


	df['SSD_val_1'] = df['SSD'].apply(get_val_1)
	df['SUB_val_1'] = df['SUB'].apply(get_val_1)
	df['SLD_val_1'] = df['SLD'].apply(get_val_1)

	df['SSD_val_2'] = df['SSD'].apply(get_val_2)
	df['SUB_val_2'] = df['SUB'].apply(get_val_2)
	df['SLD_val_2'] = df['SLD'].apply(get_val_2)

	df['SSD_val_3'] = df['SSD'].apply(get_val_3)
	df['SUB_val_3'] = df['SUB'].apply(get_val_3)
	df['SLD_val_3'] = df['SLD'].apply(get_val_3)

	df['SSD_dig_seq_l'] = df['SSD'].apply(dig_seq_l)
	df['SUB_dig_seq_l'] = df['SUB'].apply(dig_seq_l)
	df['SLD_dig_seq_l'] = df['SLD'].apply(dig_seq_l)

	df['SSD_chr_seq_l'] = df['SSD'].apply(chr_seq_l)
	df['SUB_chr_seq_l'] = df['SUB'].apply(chr_seq_l)
	df['SLD_chr_seq_l'] = df['SLD'].apply(chr_seq_l)

	df['SSD_chr_seq_c'] = df['SSD'].apply(chr_seq_c)
	df['SUB_chr_seq_c'] = df['SUB'].apply(chr_seq_c)
	df['SLD_chr_seq_c'] = df['SLD'].apply(chr_seq_c)


	bad_words, target_words = get_words()

	df['SSD_bad_words'] = df['SSD'].apply(have_words, words=bad_words)
	df['SUB_bad_words'] = df['SUB'].apply(have_words, words=bad_words)
	df['SLD_bad_words'] = df['SLD'].apply(have_words, words=bad_words)

	df['SSD_target_words'] = df['SSD'].apply(have_words, words=target_words)
	df['SUB_target_words'] = df['SUB'].apply(have_words, words=target_words)
	df['SLD_target_words'] = df['SLD'].apply(have_words, words=target_words)

	df['SSD_bad_words_rplc'] = df['SSD'].apply(have_words_rplc, words=bad_words)
	df['SUB_bad_words_rplc'] = df['SUB'].apply(have_words_rplc, words=bad_words)
	df['SLD_bad_words_rplc'] = df['SLD'].apply(have_words_rplc, words=bad_words)

	df['SSD_target_words_rplc'] = df['SSD'].apply(have_words_rplc, words=target_words)
	df['SUB_target_words_rplc'] = df['SUB'].apply(have_words_rplc, words=target_words)
	df['SLD_target_words_rplc'] = df['SLD'].apply(have_words_rplc, words=target_words)

	return df

def feature_gen(df):
	df = feature_gen_tp(df)
	df = feature_gen_lx(df)
	df = df.drop(columns=['domain','ip_format','SSD', 'SUB', 'SLD', 'Third Party', 'creation'])
	return df
