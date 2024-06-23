library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity main is -- 
port (
    clkExtPort : in std_logic;
    buttonPort : in std_logic;
    Tx : out std_logic);
end main;

architecture behavioral of main is 

component buttoninterface is
port(
    clk: in std_logic;
    buttonPort: in std_logic;
    buttonMpPort: out std_logic
  );
end component;

component clkgen is
port (clkExtPort: in std_logic;
        clkPort: out std_logic);
end component;

signal clk, rst, button, done, send_en, baud_tc : std_logic := '0';
signal Txsig : std_logic := '1';
signal Txarray, txreg : std_logic_vector(109 downto 0) := (others => '0');
signal baudcount, bitcount : integer := 0;

type state is (init,send);
signal cs, ns : state := init;

begin

U1 : clkgen
port map(
    clkExtPort => clkExtPort,
    clkPort => clk);

U2 : buttoninterface
port map(
    clk => clk,
    buttonPort => buttonPort,
    buttonMpPort => button);

Txarray <= "10110100001011001010101100101010110110001011011110100100000010111011101011011110101110010010110110001011001000";

process (clk)
begin
if rising_edge(clk) then
    cs <= ns;
end if;

end process;

process(button, done, cs)
begin
send_en <= '0';
rst <= '0';
ns <= cs;
case cs is 

when init =>
rst <= '1';
if button = '1' then
ns <= send;
end if;

when send =>
send_en <= '1';
if done = '1' then
ns <= init;
end if;

when others => ns <= init;

end case;
end process; 

baudcounter : process(clk)
begin

if rst = '1' then
  baudcount <= 0;
  baud_tc <= '0';
end if;

if rising_edge(clk) then
if send_en = '1' then
  baudcount <= baudcount+1; 
  if baudcount = 103 then
    baudcount <= 0;
  end if;       
end if;
end if;
if baudcount = 103 then
  baud_TC <= '1';
else
  baud_TC <= '0';
end if;      

end process baudcounter;

bitcounter : process(clk)
begin

if rst = '1' then
  bitcount <= 0;
  done <= '0';
  txreg <= txarray;
end if;

if rising_edge(clk) then
if baud_TC = '1' then
  txsig <= Txreg(0);
  txreg <= '1' & txreg(109 downto 1); 
  bitcount <= bitcount+1;    
  if bitcount = 109 then
    bitcount <= 0;
  end if;       
end if;
end if;
if bitcount = 109 and baudcount = 103 then
  done <= '1';
else
  done <= '0';
end if;   

end process bitcounter;

tx <= txsig;

        

end behavioral;



    