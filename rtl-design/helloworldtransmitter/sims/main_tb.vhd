library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity main_tb is

end main_tb;

architecture testbench of main_tb is

component main is 
port (
    clkExtPort : in std_logic;
    buttonPort : in std_logic;
    Tx : out std_logic);
    
end component;

signal clkExtPort, buttonPort, Tx : std_logic := '0';


begin

U1 : main
port map (
    clkExtPort => clkExtPort,
    buttonPort => buttonPort,
    Tx => tx);
    
    
process
begin
clkExtPort <= '0';
wait for 5 ns;
clkExtPort <= '1';
wait for 5 ns;

end process;

process
begin
wait for 20 ns;
buttonPort <= '1';
wait for 20 ns;
buttonPort <= '0';
wait;

end process; 
end testbench;