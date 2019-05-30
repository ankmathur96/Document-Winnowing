import re
def pre_process_document(s):
	pattern = '[,.!?;:\s\-\{\}\[\]]'
	s = re.sub(pattern, '', s)
	s = s.lower()
	return s

def make_kgrams(s, k):
	grams = []
	start, end = 0, k
	while start < len(s) - k + 1:
		grams.append(s[start:end])
		start += 1
		end += 1
	return grams

def right_weight_min(key=lambda x: x):
	def r_min(l):
		cur_min, min_index, i = float('inf'), -1, 0
		while i < len(l):
			if key(l[i]) <= cur_min:
				cur_min, min_index = key(l[i]), i
			i += 1
		return l[min_index]
	return r_min

def winnow(k_grams, k, t):
	min = right_weight_min(lambda x: x[0])
	fingerprints = []
	hashes = [(hash(k_grams[i]), i) for i in range(len(k_grams))]
	window_size = t - k + 1
	# to guarantee matches for a t-sized string, 1 of the 
	# t - k + 1 hashes which will match must be selected
	# as a fingerprint.
	w_start, w_end = 0, window_size
	cur_min = None
	while w_end < len(hashes):
		window = hashes[w_start:w_end]
		new_min = min(window)
		if cur_min != new_min:
			fingerprints.append(new_min)
			cur_min = new_min
		w_start, w_end = w_start + 1, w_end + 1
	return fingerprints

def output_fingerprint(fingerprints, kgrams):
	for i in fingerprints:
		print(repr(kgrams[i[1]]), i[0])
	print('---------------------------------')

def process_document(s, k, t):
	s = pre_process_document(s)
	k_grams = make_kgrams(s)
	fingerprints = winnow(k_grams, k, t)
	output_fingerprint(fingerprints, k_grams)
	match_set = set(fingerprints)

k, t = 5, 8
k_grams = make_kgrams('adorunrunrunadorunrun', k)
fingerprints = winnow(k_grams, k, t)
output_fingerprint(fingerprints, k_grams)

k_grams = make_kgrams('Didnt copy anyone. adorunrun. oh no, i did.', k)
fingerprints = winnow(k_grams, k, t) 
output_fingerprint(fingerprints, k_grams)

match_set = set(fingerprints)

#http://www.cse.buffalo.edu/~ss424/Presentations/UB-MOSS-Primer.pdf
#https://github.com/ucarion/winnow/blob/master/lib/winnow/matcher.rb