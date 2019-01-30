import Preprocessing.baseline_analysis as baseline

if __name__ == '__main__':
  baseline.do_analysis('initial')
  baseline.do_analysis('match')

  baseline.full_analysis()