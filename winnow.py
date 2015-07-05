import re
def preProcessDocument(s):
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

def rightWeightMin(l):
	curMin, minIndex, i = float('inf'), -1, 0
	while i < len(l):
		if l[i][0] <= curMin:
			curMin, minIndex = l[i][0], i
		i += 1
	return l[minIndex]

def winnow(kgrams, k, t):
	min = rightWeightMin
	fingerprints = []
	hashes = [(hash(kgrams[i]), i) for i in range(len(kgrams))]
	print(hashes)
	windowSize = t - k + 1
	# to guarantee matches for a t-sized string, 1 of the 
	# t - k + 1 hashes which will match must be selected
	# as a fingerprint.
	wStart, wEnd = 0, windowSize
	curMin = None
	while wEnd < len(hashes):
		window = hashes[wStart:wEnd]
		newMin = min(window)
		if curMin != newMin:
			fingerprints.append(newMin)
			curMin = newMin
		wStart, wEnd = wStart + 1, wEnd + 1
	return fingerprints
k, t = 5, 8


fingerprint = winnow(make_kgrams('adorunrunrunadorunrun', k), k, t)
