library ieee;
use     ieee.std_logic_1164.all;

library xpm;
use     xpm.vcomponents.all;


entity bit_cdc is
   generic (
      g_DEST_SYNC_FF : integer range 2 to 10 := 4;
      g_SRC_INPUT_REG: integer range 0 to 1  := 1
   );
    port (
      -- inputs
      src_clk        : in  std_logic;
      src_in         : in  std_logic;
      dest_clk       : in  std_logic;
      -- output        
      dest_out       : out std_logic
    );
end bit_cdc;

architecture rtl of bit_cdc is

begin

   -- xpm_cdc_single: Single-bit Synchronizer
   -- Xilinx Parameterized Macro, version 2019.2
   xpm_cdc_single_inst: xpm_cdc_single
      generic map (
         DEST_SYNC_FF      => g_DEST_SYNC_FF,   -- DECIMAL; range: 2-10
         INIT_SYNC_FF      => 0,                -- DECIMAL; 0=disable simulation init values, 1=enable simulation init values
         SIM_ASSERT_CHK    => 0,                -- DECIMAL; 0=disable simulation messages, 1=enable simulation messages
         SRC_INPUT_REG     => g_SRC_INPUT_REG   -- DECIMAL; 0=do not register input, 1=register input
      )
      port map (
         dest_out          => dest_out,         -- 1-bit output: src_in synchronized to the destination clock domain. This output is registered.
         dest_clk          => dest_clk,         -- 1-bit input: Clock signal for the destination clock domain.
         src_clk           => src_clk,          -- 1-bit input: optional; required when SRC_INPUT_REG = 1
         src_in            => src_in            -- 1-bit input: Input signal to be synchronized to dest_clk domain.
      );

end rtl;