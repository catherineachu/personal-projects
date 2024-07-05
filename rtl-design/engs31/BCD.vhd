"themed_title_bar": true,
--=============================================================================
--ENGS 31/ CoSc 56 22S
--Lab 3 Prelab BCD Counter VHDL Model
--B.L. Dobbins, E.W. Hansen, Professor Luke
--Your Name Here: Catherine Chu (2024)
--=============================================================================

--=============================================================================
--Library Declarations:
--=============================================================================
library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;

--=============================================================================
--Entity Declaration:
--=============================================================================
entity bcd_digit is
	port(clk_port		: in  std_logic;
    	 reset_port     : in  std_logic;         --1 to reset
    	 enable_port	: in  std_logic;         --1 to count, 0 to hold
		 y_port         : out std_logic_vector(3 downto 0);
         tc_port		: out std_logic );
end entity;

--=============================================================================
--Architecture Type:
--=============================================================================
architecture behavior of bcd_digit is
--=============================================================================
--Signal Declarations: 
--=============================================================================

--Your signals go here:
--unsigned means that it's a positive number
signal y_sig : unsigned(3 downto 0) := "0000";
signal tc_sig : std_logic := '0';

--=============================================================================
--Processes: 
--=============================================================================
begin

--+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
--BCD Digit Counter:
--+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
--Your synchronous component of the design goes here:

process(clk_port)
begin

    if rising_edge(clk_port) then
    	if reset_port = '1' or tc_sig = '1' then
        	y_sig <= "0000";
        elsif enable_port = '1' then
        	y_sig <= y_sig + 1;
		end if;
    end if;
    
end process;

--+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
--BCD Digit TC:
--+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
--Your asynchronous terminal count goes here:

process(y_sig)						
begin
	if y_sig = "1001" then
    	tc_sig <= '1';
    else
    	tc_sig <= '0';
    end if; 
	

end process;

y_port <= std_logic_vector(y_sig);
tc_port <= tc_sig;


end behavior;     

