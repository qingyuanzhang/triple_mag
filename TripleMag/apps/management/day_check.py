#coding=utf8
from TripleMag.apps.views import CallProc
def day_check():
    """
    每天执行everyday_check存储过程
    """
    proc_name = "everyday_check"
    call_proc = CallProc()
    call_proc.CallProcFuc_0(proc_name)
    
    
