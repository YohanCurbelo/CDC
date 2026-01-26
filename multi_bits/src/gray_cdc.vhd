library ieee;
use     ieee.std_logic_1164.all;

library xpm;
use     xpm.vcomponents.all;


entity gray_cdc is
    generic (
        g_DEST_SYNC_FF  : integer range 2 to 10 := 4;
        g_SIGNAL_WIDTH  : integer range 2 to 32 := 2
    );
    port (
        -- inputs
        src_clk         : in  std_logic;
        src_in_bin      : in  std_logic_vector(g_SIGNAL_WIDTH-1 downto 0);
        dest_clk        : in  std_logic;
        -- output        
        dest_out_bin    : out std_logic_vector(g_SIGNAL_WIDTH-1 downto 0)
    );
end gray_cdc;

architecture rtl of gray_cdc is

begin

    -- xpm_cdc_gray: Synchronizer via Gray Encoding
    -- Xilinx Parameterized Macro, version 2019.2
    xpm_cdc_gray_inst : xpm_cdc_gray
        generic map (
            DEST_SYNC_FF          => g_DEST_SYNC_FF,    -- DECIMAL; range: 2-10
            INIT_SYNC_FF          => 0,                 -- DECIMAL; 0=disable simulation init values, 1=enable simulation init values
            REG_OUTPUT            => 0,                 -- DECIMAL; 0=disable registered output, 1=enable registered output
            SIM_ASSERT_CHK        => 0,                 -- DECIMAL; 0=disable simulation messages, 1=enable simulation messages
            SIM_LOSSLESS_GRAY_CHK => 0,                 -- DECIMAL; 0=disable lossless check, 1=enable lossless check
            WIDTH                 => g_SIGNAL_WIDTH     -- DECIMAL; range: 2-32
        )
        port map (
            dest_out_bin          => dest_out_bin,      -- WIDTH-bit output: Binary input bus (src_in_bin) synchronized to
                                                        -- destination clock domain. This output is combinatorial unless REG_OUTPUT
                                                        -- is set to 1.
            dest_clk              => dest_clk,          -- 1-bit input: Destination clock.
            src_clk               => src_clk,           -- 1-bit input: Source clock.
            src_in_bin            => src_in_bin         -- WIDTH-bit input: Binary input bus that will be synchronized to the destination clock domain.
        );
   
end rtl;