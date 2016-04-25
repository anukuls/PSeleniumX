import pytest

'''
    Executing Selenium Grid tests in distributed mode, with use of pytest-xdist.
    Need to define processes to be opened by popen.  Currently, 1 process per test on 
    each remote machine looks good.
'''
pytest_args = "--tx 1*popen --dist=each SeleniumGrid_Distributed_Driver.py -q --tb=line"
pytest.main(pytest_args)