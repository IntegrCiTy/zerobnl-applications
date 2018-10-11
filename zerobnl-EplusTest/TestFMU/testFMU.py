import fmipp
import os.path
import math

work_dir = os.path.split( os.path.abspath( __file__ ) )[0] # define working directory
model_name = 'Exercise1D' # define FMU model name

path_to_fmu = os.path.join( work_dir, model_name + '.fmu' ) # path to FMU
uri_to_extracted_fmu = fmipp.extractFMU( path_to_fmu, work_dir ) # extract FMU

logging_on = False
time_diff_resolution = 1e-9
fmu = fmipp.FMUCoSimulationV1( uri_to_extracted_fmu, model_name, logging_on, time_diff_resolution )

print( 'successfully loaded the FMU' )

start_time = 0.
stop_time = 3600.*24. # 24 hours

instance_name = "eplus_fmu_test"
visible = False
interactive = False
status = fmu.instantiate( instance_name, start_time, visible, interactive )
assert status == fmipp.fmiOK

print( 'successfully instantiated the FMU' )

stop_time_defined = True
status = fmu.initialize( start_time, stop_time_defined, stop_time )
assert status == fmipp.fmiOK

print( 'successfully initialized the FMU' )

time = 0.
step_size = 3600 # 1 hour

print( 'start simulation loop' )

while ( ( time + step_size ) - stop_time < time_diff_resolution ):
  # Make co-simulation step.
  new_step = True
  status = fmu.doStep( time, step_size, new_step )
  assert status == fmipp.fmiOK

  # # Advance time.
  time += step_size

  fmu.setRealValue( 'Ts_second', 60 )
  assert fmu.getLastStatus() == fmipp.fmiOK

  temp_supply = fmu.getRealValue( 'Tr_second' )
  assert fmu.getLastStatus() == fmipp.fmiOK

  print( 'time = {}, Tr_secondary = {}'.format( time, temp_supply ) )
