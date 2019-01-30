import pickle
import numpy as np

# Load different backend so that matplotlib doesn't break inside a virtual env (https://github.com/pypa/virtualenv/issues/609)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 15})

def chunkify(item, n):
  return [item[i::n] for i in range(n)]

def bin_data(data):  
  bin_means = [np.mean(x) for x in chunkify(data, 250)]

  return bin_means

def plot_word_freqs(word_freqs):
  fig = plt.figure()

  initial_freqs = word_freqs['initial']
  match_freqs = word_freqs['match']

  initial_freqs = [x / max(initial_freqs) for x in initial_freqs]
  match_freqs = [x / max(match_freqs) for x in match_freqs]

  plt.bar(range(0, len(match_freqs)), match_freqs, alpha = 1.0, label = 'Big Data')
  plt.bar(range(0, len(initial_freqs)), initial_freqs, alpha = 1.0, label = 'non-Big Data')

  # Add labels
  plt.xlabel('Number of tokens', labelpad = 13)
  plt.ylabel('Number of documents\n (normalised)', labelpad = 10)

  plt.legend()
  
  plt.tight_layout(True)

  fig.savefig('plots/document_word_frequencies.pdf', bbox_inches = 'tight')

def get_word_freq_data():
  with open('../Metadata/word_counts.pickle', 'rb') as handle:
    return pickle.load(handle)

if __name__ == '__main__':
  word_freqs = get_word_freq_data()
  
  plot_word_freqs(word_freqs)