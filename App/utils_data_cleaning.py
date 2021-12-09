def get_domain(s):    
    s = s.replace('https://','')
    s = s.replace('http://','')
    s = s.split('/', 1)[0]
    if s[:4] == 'www.':
    	return s[4:]
    return s

def data_cleaning(df):
	df['domain'] = df['domain'].apply(get_domain)
	return df
    