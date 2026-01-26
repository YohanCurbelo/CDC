# ==============================================================================
#                           Modules Imported                                
# ==============================================================================
# cocotb
import  cocotb
from    cocotb.triggers import Timer, RisingEdge
from    cocotb.clock    import Clock
from    random          import randint
from    math            import ceil

# ==============================================================================
#                       Generics and Constants                                
# ==============================================================================
# Clock Periods (ns)
SRC_CLK = 10        # 100 MHz
DEST_CLK = 5.55     # 180 MHz
CLK_RATIO_CEIL = ceil(SRC_CLK/DEST_CLK)

# Test Parameters
TOTAL_DATA_IN = 1000

# ==============================================================================
#                           Function Definitions                                
# ==============================================================================
def generate_data_test(dut):
    global data_test    
    data_test = []
    for i in range(TOTAL_DATA_IN):
        data_test.append(randint(0,2**int(dut.g_SIGNAL_WIDTH.value)-1))

def check_data():
    for i in range(TOTAL_DATA_IN*CLK_RATIO_CEIL):
        cocotb.log.info("Checking iteration %i" % i)  
        assert input_data[i] == output_data[i], "Input (%i) and output (%i) data mismatch" % (input_data[i], output_data[i])
    cocotb.log.info("Test successful!")  

async def read_data_in_with_dest_clk(dut):
    global input_data
    input_data = []
    await RisingEdge(dut.src_clk)                   # Await because first data is written after the first src_clk cycle
    await RisingEdge(dut.src_clk)                   # Await because src_in_bin is registered internally
    for i in range(TOTAL_DATA_IN*CLK_RATIO_CEIL):
        await RisingEdge(dut.dest_clk)
        input_data.append(src_in_bin_sr)

async def read_data_out(dut):
    global output_data
    output_data = []
    data_read = "X"    
    # wait until there is data available
    while data_read == "X":
        await RisingEdge(dut.dest_clk)
        data_read = str(dut.dest_out_bin.value)[0]
    output_data.append(int(dut.dest_out_bin.value))    
    for i in range(TOTAL_DATA_IN*CLK_RATIO_CEIL-1):
        await RisingEdge(dut.dest_clk)
        output_data.append(int(dut.dest_out_bin.value))

async def write_data_in(dut):    
    cocotb.start_soon(read_data_in_with_dest_clk(dut))
    global src_in_bin_sr
    src_in_bin_sr = 0
    await RisingEdge(dut.src_clk)
    for i in range(TOTAL_DATA_IN):
        dut.src_in_bin.value = data_test[i]
        await RisingEdge(dut.src_clk)
        src_in_bin_sr = data_test[i]
    await RisingEdge(dut.src_clk)
    dut.src_in_bin.value = 0
    await RisingEdge(dut.src_clk)
    src_in_bin_sr = 0

# ==============================================================================
#                           Tests Definitions                               
# ==============================================================================
@cocotb.test(stage = 1)
async def test_gray_cdc(dut):

    cocotb.log.info("Init Test")

    # Setting up clocks
    clk_src = Clock(dut.src_clk, SRC_CLK, units='ns')
    clk_dest = Clock(dut.dest_clk, DEST_CLK, units='ns')
    cocotb.start_soon(clk_src.start(start_high=False))
    cocotb.start_soon(clk_dest.start(start_high=False))

    # Generate data test
    generate_data_test(dut)

    # Write data
    in_data = cocotb.start_soon(write_data_in(dut))

    # Read data
    out_data = cocotb.start_soon(read_data_out(dut))

    # Waiting time
    await in_data
    await Timer(CLK_RATIO_CEIL*TOTAL_DATA_IN*SRC_CLK, units='ns')

    in_data.kill()
    out_data.kill()

    # Check data
    check_data()