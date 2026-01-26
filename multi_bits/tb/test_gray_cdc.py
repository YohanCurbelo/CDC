from    cocotb_test.simulator   import run
import  pytest
import  os
import  glob

dir = os.path.dirname(__file__)
src_vhdl = glob.glob("../src/*.vhd")
src_v = glob.glob("../tb/*.v")

@pytest.mark.parametrize(
        "parameters", [ {"g_DEST_SYNC_FF": "4", "g_SIGNAL_WIDTH": "2"},            
                        {"g_DEST_SYNC_FF": "10", "g_SIGNAL_WIDTH": "4"}
                    ])
def test_gray_cdc_questa(parameters):
    run(
        vhdl_sources=[os.path.join(dir, file) for file in src_vhdl],    # vhdl sources
        verilog_sources=[os.path.join(dir, file) for file in src_v],    # verilog sources
        toplevel="gray_cdc",                                            # top level HDL
        module="gray_cdc_tb",                                           # name of cocotb test module
        parameters=parameters,
        extra_env=parameters, 
        sim_args=["-t", "1ps", "gray_cdc.glbl"],
        force_compile=True
    )