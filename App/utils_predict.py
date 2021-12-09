import numpy as np 

def most_common(lst):
    return max(set(lst), key=lst.count)

def get_preds(y_pred):
    y_pred = np.array(y_pred).T.tolist()
    y_pred = [most_common(y) for y in y_pred]
    return y_pred

def get_score(score, thr, pred):
	if pred == 0:
		return 1-score/thr
	return (score-thr)/(1-thr)


def get_scores(y_scores, preds, thrs = (0,0,0)):
	y_scores[0] = [get_score(score, thrs[0], preds[i]) for i, score in  enumerate(y_scores[0])]
	y_scores[1] = [get_score(score, thrs[1], preds[i]) for i, score in  enumerate(y_scores[1])]
	y_scores[2] = [get_score(score, thrs[2], preds[i]) for i, score in  enumerate(y_scores[2])]

	y_scores = np.array(y_scores).T.tolist()
	y_scores = [np.mean(y) for y in y_scores]
	return y_scores

def predict_df(df, clf_rf, clf_mlp, clf_knn):
	thr_rf = 0.435
	thr_mlp = 0.466
	thr_knn = 0.4


	X = df

	y_rf = clf_rf.predict_proba(X)[:, 1]
	y_mlp = clf_mlp.predict_proba(X.values)[:, 1]
	y_knn = clf_knn.predict_proba(X)[:, 1]

	y_scores = [y_rf, y_mlp, y_knn]

	y_rf  = [round(i - thr_rf + 0.5) for i in y_rf]
	y_mlp = [round(i - thr_mlp + 0.5) for i in y_mlp]
	y_knn = [round(i - thr_knn + 0.5) for i in y_knn]

	y_pred = [y_rf, y_mlp, y_knn]

	preds  = get_preds(y_pred)

	thresholds = (thr_rf, thr_mlp, thr_knn)
	scores = get_scores(y_scores, preds, thresholds)

	results = preds, scores
	results = np.array(results).T.tolist()
	return results

