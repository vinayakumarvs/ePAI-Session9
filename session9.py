from time import perf_counter, localtime
from collections import defaultdict
from functools import wraps, singledispatch
from datetime import datetime, timezone
from decimal import Decimal
from html import escape


def odd_sec_run(time:datetime):
    """
    This is a decorator factory which takes a parameter
    # param:
        time: This variable contains the current time
    """
    def odd_second_runner(fn: 'input argument'):
        """
        This is a closure function
        # Param:
            fn : This function takes in function as a parameter
        """
        @wraps(fn)
        def inner(*args,**kwargs):
            """
            This function checks if the seconds is odd, then it will run the function
            else will return a message
            """
            run_dt = time
            print(str(run_dt) + " called " + str(fn.__name__))
            print(run_dt.second)
            if run_dt.second %2 != 0:
                value = fn(*args,**kwargs)
                return value
            else:
                return f"it is odd time {run_dt}"
        return inner
    return odd_second_runner


func_reg = defaultdict(lambda : 0)

def log_func(fn):
	'''
	Decorator which holds on log details whenever input function is executed.
	Args:
		fn: A User-Defined Function
	Returns a inner function(callable)
	'''
	
	count, total_time = 0, 0

	@wraps(fn)
	def inner(*args, **kwargs):
		nonlocal count
		nonlocal total_time

		func_time = datetime.now(timezone.utc)
		func_id = hex(id(fn.__name__))

		start_time = perf_counter()
		result = fn(*args, **kwargs)
		elapsed_time = perf_counter()-start_time

		func_reg[inner.__name__] = count
		count = count + 1
		total_time = total_time + elapsed_time


		print(f'Function Name: {fn.__name__} \n Function use {fn.__doc__} \n ID of function is {func_id} \n Executed at {func_time} \n Executed for about {count} times.\n Current Execution Time: {elapsed_time} seconds \n Total Execution Time: {total_time} seconds')
		return result
	return inner

def authenticate(user_password:str):
    """
    This function takes in user password and checks with the one 
    stored in the database and if it matches it executes the function 
    else raises error
    """
    def auth(fn):
        if user_password ==  'Bond@007':
            @wraps(fn)
            def inner(*args, **kwargs):
                return fn(*args, **kwargs)
            return inner
        else:
            raise ValueError("Provide correct password")
    return auth

def time_it(reps: int):
    """
    Decorator factory to take in an integer defining the number of
    iterations and return a decorator accordingly.
    """
    if type(reps) is not int:
        raise TypeError("Invalid type, accepts int")
    if reps < 1:
        raise ValueError("Ensure atleast 1 iteration.")
    def timed(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            total_elapsed = 0
            for i in range(reps):
                start = perf_counter()
                result = fn(*args, **kwargs)
                end = perf_counter()
                total_elapsed += (end - start)
            avg_run_time = total_elapsed / reps
            print('Avg Run time: {0:.6f}s ({1} reps)'.format(avg_run_time, reps))
            return result
        return inner
    return timed

def privilege(level:int):
    """
    This function takes in integer which defines the access level
    and then checks if the function belongs to that level, if it does
    then runs it else raises an error
    """
    levels = {1:('high','mid','low','no'),2:('mid','low','no'),3:('low','no'),4:('no')}
    def access_func(fn):
        func_list = levels.get(level)
        if fn.__name__ in func_list:
            @wraps(fn)
            def inner(*args,**kwargs):
                return fn(*args,**kwargs)
            return inner

        else:
            raise ValueError("No sufficient privilege")
    return access_func

@singledispatch
def htmlize(input: 'input argument') -> str :
    '''
    function to htmlize the input based on the type of input.
    this is a default initializer.
    '''
    return escape(str(input))

@htmlize.register(int)
def html_int(input: int) -> str:
    '''
    converts int in html formats
    '''
    return f'{input}(<i>{str(hex(input))}</i>)'

@htmlize.register(Decimal)
@htmlize.register(float)
def html_real(input: float) -> str:
    '''
    converts reals to html function
    '''
    return f'{round(input, 2)}'

@htmlize.register(str)
def html_str(input: str) -> str:
    '''
    fconvert string to html format
    '''
    return escape(input).replace('\n', '<br/>\n')

@htmlize.register(tuple)
@htmlize.register(list)
@htmlize.register(set)
@htmlize.register(frozenset)
def html_sequence(input) ->str:
    '''
    converts a sequence in html format
    '''
    items = (f'<li>{escape(str(item))}</li>' for item in input)
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'

@htmlize.register(dict)
def html_dict(input: dict) -> str:
    '''
    converts dictionary in html format
    '''
    items = (f'<li>{k}={v}</li>' for k, v in input.items())
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'