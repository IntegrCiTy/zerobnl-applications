import DYESOPT
from Core.setModelLabel import*
import os
import pywinauto
from pywinauto.application import Application
import time


TRNSYSmodel = model_plant


if DYESOPT.runMode == 'single':
    print(' ')
    app = Application(backend="uia").start(os.path.join(r'C:\DYESOPT\DYESOPT\DynSim&TEcalculations' , HESTech , TRNSYSmodel  ,'model',TRNSYSmodel+'.exe'))

    dlg_spec = app.AboutTRNEdit
    # wait till the window is really open
    actionable_dlg = dlg_spec.wait('visible')
    app.AboutTRNEdit.OK.click()
    time.sleep(1)
    pywinauto.mouse.click(button= 'left', coords=(1500, 500))
    time.sleep(1)
    pywinauto.keyboard.SendKeys('{F8}')
    time.sleep(3)
    pywinauto.mouse.click(button= 'left', coords=(500, 500))
    time.sleep(1)
    pywinauto.keyboard.SendKeys('{ENTER}')
    time.sleep(1)
    pywinauto.mouse.click(button= 'left', coords=(1500, 500))
    time.sleep(1)
    pywinauto.keyboard.SendKeys('%{F4}')
    time.sleep(1)
    pywinauto.keyboard.SendKeys('{RIGHT}')
    time.sleep(1)
    pywinauto.keyboard.SendKeys('{ENTER}')

    success=1


