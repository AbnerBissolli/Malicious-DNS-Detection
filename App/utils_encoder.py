from pickle import load
from sklearn.preprocessing import LabelEncoder
import pandas as pd

def idf_val(s, tfidf):
#     values = list(tfidf.idf_)
    feature_names = list(tfidf.get_feature_names_out())
        
    if s in feature_names:
        index = feature_names.index(s)
    else:
        index = feature_names.index('unknown_tld')
        
    return tfidf.idf_[index]

def encode(item, encoder):
    if item not in list(encoder.classes_):
        item = 'Unknown'
    lst = [item]
    lst = encoder.transform(lst)
    return lst[0]

def norm_df(df, vectorizer, enc_tld, enc_chr, scaler):
	# Encoding
	df['TLD_TD_IDF'] = df['TLD'].apply(idf_val, tfidf=vectorizer)
	df['TLD'] = df['TLD'].apply(encode, encoder=enc_tld)

	df['SSD_val_3'] = df['SSD_val_3'].apply(encode, encoder=enc_chr)
	df['SUB_val_3'] = df['SUB_val_3'].apply(encode, encoder=enc_chr)
	df['SLD_val_3'] = df['SLD_val_3'].apply(encode, encoder=enc_chr)

	df['SSD_chr_seq_c'] = df['SSD_chr_seq_c'].apply(encode, encoder=enc_chr)
	df['SUB_chr_seq_c'] = df['SUB_chr_seq_c'].apply(encode, encoder=enc_chr)
	df['SLD_chr_seq_c'] = df['SLD_chr_seq_c'].apply(encode, encoder=enc_chr)

	# Normalizing
	features = ['TLD', 'SSD_len', 'SUB_len', 'SLD_len', 'SSD_pct', 'SUB_pct', 'SLD_pct', 'SSD_nan', 'SUB_nan', 'SLD_nan', 'SSD_etp', 'SUB_etp', 'SLD_etp', 'SUB_num', 'SSD_val_1', 'SUB_val_1', 'SLD_val_1', 'SSD_val_2', 'SUB_val_2', 'SLD_val_2', 'SSD_val_3', 'SUB_val_3', 'SLD_val_3', 'SSD_dig_seq_l', 'SUB_dig_seq_l', 'SLD_dig_seq_l', 'SSD_chr_seq_l', 'SUB_chr_seq_l', 'SLD_chr_seq_l', 'SSD_chr_seq_c', 'SUB_chr_seq_c', 'SLD_chr_seq_c', 'SSD_bad_words', 'SUB_bad_words', 'SLD_bad_words', 'SSD_target_words', 'SUB_target_words', 'SLD_target_words', 'SSD_bad_words_rplc', 'SUB_bad_words_rplc', 'SLD_bad_words_rplc', 'SSD_target_words_rplc', 'SUB_target_words_rplc', 'SLD_target_words_rplc', 'connection', 'privacy', 'name', 'address', 'state', 'country', 'email', 'servers', 'registrar', 'registrant', 'org', 'age', 'SLDs in SUB', 'SLD Distance', 'TLD_TD_IDF']
	# df.columns = features
	df = df[features]

	df_norm = scaler.transform(df)
	df_norm = pd.DataFrame(df_norm, columns = features)


	return df_norm