#!usr/bin/python3.5

# Here we show how to write our own generator
# The range(n) is by default non inclusive and does not onclude the ending no.
# We create our own range generator which will be inclusive


class inclusive_range:

	def __init__(self, *args):
		numargs = len(args)  	# no of arguments

		if(numargs < 1):		# if no args provided
			raise TypeError("inclusive_range expects atleast one argument")

		elif(numargs == 1):		# 1 arg means its the upper limit
			self.start = 0
			self.stop = args[0]
			self.step = 1

		elif(numargs == 2):		# the start and the end
			(self.start, self.stop) = args 
			self.step = 1

		elif(numargs == 3):		# start, end and step
			(self.start, self.stop, self.step) = args 

		else:
			raise TypeError("inclusive_range expects atmost 3 arguments")


	# the iter function makes teh generator iterable
	def __iter__(self):
		i = self.start
		while(i <= self.stop):
			yield i
			i = i + self.step


def main():
	try:
		ran = inclusive_range(4, 10, 2)
		for r in ran:
			print(r, end = ' ')
	except Exception as e:
		print(e)
	finally:
		print("\n")


if(__name__ == "__main__"): main() 