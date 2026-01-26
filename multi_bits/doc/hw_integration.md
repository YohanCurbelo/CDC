# Entity: gray_cdc 
- **File**: gray_cdc.vhd

## Diagram
![Diagram](gray_cdc.svg "Diagram")

## Generics
| Generic name   | Type                  | Value | Description |
| -------------- | --------------------- | ----- | ----------- |
| g_SIGNAL_WIDTH | integer range 2 to 32 | 2     |             |

## Ports
| Port name    | Direction | Type                                        | Description |
| ------------ | --------- | ------------------------------------------- | ----------- |
| src_clk      | in        | std_logic                                   |             |
| src_in_bin   | in        | std_logic_vector(g_SIGNAL_WIDTH-1 downto 0) |             |
| dest_clk     | in        | std_logic                                   |             |
| dest_out_bin | out       | std_logic_vector(g_SIGNAL_WIDTH-1 downto 0) |             |

## Instantiations
- xpm_cdc_gray_inst: xpm_cdc_gray