# Load different backend so that matplotlib doesn't break inside a virtual env (https://github.com/pypa/virtualenv/issues/609)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 15})

initial_data = [5, 23, 137, 426, 849, 1498, 2241, 2589]
match_data = [839, 6507, 30339, 87100, 175041, 309945, 485545, 530464]
all_data = [844, 6530, 30476, 87526, 175890, 311443, 487786, 533053]

years = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']

if __name__ == '__main__':
  new_initial = [x / max(initial_data) for x in initial_data]
  new_match = [x / max(match_data) for x in match_data]

  fig = plt.figure()

  plt.xlabel('Year of publication', labelpad = 13)
  plt.ylabel('Number of documents\n (normalised)', labelpad = 10)
  
  plt.plot(years, new_initial, label = 'Big Data')
  plt.plot(years, new_match, linestyle = 'dashed', label = 'non-Big Data')

  plt.legend()

  plt.tight_layout(True)

  fig.savefig('plots/documents_per_year_normalised.pdf', bbox_inches = 'tight')