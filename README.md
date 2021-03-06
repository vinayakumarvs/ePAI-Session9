# Session 9 - Decorators
# EPAi Session9 Assignment

#### Objective of Assignment:

1. Write separate decorators that:

    a. allows a function to run only on odd seconds 

    b. log 

    c. authenticate

    d. timed (n times)

2. Provides privilege access (has 4 parameters, based on privileges (high, mid, low, no), gives access to all 4, 3, 2 or 1 params)

Write our htmlize code using inbuild singledispatch 



## Functions Defined:

* Function to run only at odd second: A simple decorator to make the function return the output only if the current time has seconds numeric as an odd digit.

    ```python
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
    ```

* Function to show log: A decorator to print the logs of a function, the start time of execution, end time, running time. Also, whether the function returns something, it's docs. The decorator adds these functionality for us.

```python
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
```

* Function to authenticate password: Decorator to implement simple authentication functionality and give that to any function of our choice. The user can make use of a closure to provide the current password. It has to match with the default user password provided beforehand.

```python
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
```

* time the function for 'n' times: A decorator factory, that takes in an integer, defining the number of iteration of which a function's runtime has to be calculated and average is calculated. It returns a decorator.

```python
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

```

* Privilege: Decorator that provides privilege access. A function can have four parameters and based on the privileges (high, mid, low, no), access is given to all 4, 3, 2 or 1 parameters.

```python
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
```

* singledispatch: Writing HTMLize code using singledispatch, available as a built-in decorator in functools module. Also the idea is to add functionality using monkey patching and not make every thing hard coded.


```python
def htmlize(input: 'input argument') -> str :
    '''
    function to htmlize the input based on the type of input.
    this is a default initializer.
    '''
    return escape(str(input))
```

Created a test functions to validate the functions.