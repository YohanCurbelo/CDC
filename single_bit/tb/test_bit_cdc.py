from    cocotb_test.simulator   import run
import  pytest
import  os
import  glob

dir = os.path.dirname(__file__)
src_vhdl = glob.glob("../src/*.vhd")
src_v = glob.glob("../tb/*.v")

@pytest.mark.parametrize(
        "parameters", [ {"g_DEST_SYNC_FF": "4", "g_SRC_INPUT_REG": "0"},
                        {"g_DEST_SYNC_FF": "10", "g_SRC_INPUT_REG": "0"},
                        {"g_DEST_SYNC_FF": "4", "g_SRC_INPUT_REG": "1"},
                        {"g_DEST_SYNC_FF": "10", "g_SRC_INPUT_REG": "1"}
                    ])
def test_bit_cdc_questa(parameters):
    run(
        verilog_sources=[os.path.join(dir, file) for file in src_v],    # verilog sources
        vhdl_sources=[os.path.join(dir, file) for file in src_vhdl],    # vhdl sources
        toplevel="bit_cdc",                                             # top level HDL
        module="bit_cdc_tb",                                            # name of cocotb test module
        toplevel_lang="vhdl",
        parameters=parameters,
        extra_env=parameters, 
        sim_args=["-t", "1ps", "bit_cdc.glbl"],
        force_compile=True
    )