from Core.setModelLabel import*
from datetime import datetime
from datetime import date

# Display welcome header.
def dyesoptHeader(headerType):
    # Here the welcome header is set.
    # Determine DYESOPT version number----> OSAMA - How can we decide the version?
    now= date.today()
    version= now - date(2012,11,1)
    version = str(version)
    versNum = str('3.5.' + version[0:5])

    now=str(now)

    # Pad.
    print(' ')

    # Display main header section.
    print('   ++---------------------------------------------------++')
    print('   ++ DYESOPT - DYNAMIC ENERGY SYSTEM OPTIMISATION TOOL ++')
    print('   ++       Version:     '+ versNum + '    (' + now + ')      ++')

    if headerType == 'single':
        now= date.today()
        now=str(now.year)
        # Display header base section for single run.
        print('   ++---------------------------------------------------++')
        print('   ++      Copyright     KTH-EGI      (2008-' + now +')       ++')
        print('   ++---------------------------------------------------++')

    elif headerType == 'optimRun':

        # Display header base section for optimisation run.
        print('   ++ Copyright       KTH-EGI (2008-' + now.strftime('%Y')+')               ++')
        print('   ++---------------------------------------------------++')

    else:

        # Report error for unknown run type.
        print('dyesoptHeader: unrecognised run type')


    return
