from DFA          import DFA
from DFABuilder   import DFABuilder
from DFAExtender  import DFAExtender
from pdf_from_dfa import pdf_from_dfa
from clean		  import clean_code_dir_keep_results


USE_DFA_BUILDER = True


def main():

	# construct dfa

	test_dfa = None

	if USE_DFA_BUILDER:

		orig_dfa = DFABuilder().mix(0,1,1,3).dfa()

	else:

		orig_dfa = DFA(
			['a','b','c','d','e'],
			[1,2,3,4,5],
			[
				((1,1),'a'),
				((1,2),'b'),
				((2,4),'c'),
				((5,1),'d'),
				((2,5),'e')
			],
			1,
			[4,5]
		)

		orig_dfa = DFA(
			['0', '1'],
			['AD', 'B', 'CE', 'G'],
			[
				(('AD','CE'),'1'),
				(('AD','G' ),'0'),
				
				(('B' ,'CE'),'0'),
				(('B' ,'CE'),'1'),
				
				(('CE','B' ),'0'),
				(('CE','AD'),'1'),
				
				(('G' ,'B' ),'0'),
				(('G' ,'CE'),'1'),
			],
			'AD',
			['CE']
		)


	# extend dfa

	task_dfa = DFAExtender(dfa = orig_dfa).duplicate(1).dfa()


	# generate graphical representation of original and extended dfa

	pdf_from_dfa(orig_dfa, "1")
	pdf_from_dfa(task_dfa, "2")


	# clean up directory

	clean_code_dir_keep_results()


if __name__ == "__main__":

	main()
