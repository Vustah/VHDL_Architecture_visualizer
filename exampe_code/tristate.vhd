library ieee;
use ieee.std_logic_1164.all;

entity tristate_dr is
  port (
    d_in   : in std_logic_vector(7 downto 0);
    en     : in std_logic;
    d_out  : out std_logic_vector(7 downto 0);
    d2_out : out std_logic_vector(2 downto 0);
    rst    : in std_logic
  );
end tristate_dr;

architecture behavior of tristate_dr is
  signal local_signal                    : std_logic;
  signal local_signal_with_initial_value : std_logic := '1';

begin

  tristate_driver : process (d_in, en)
    variable local_variable_tristate : std_logic := '0';
  begin
    if rst = '1' then
      d_out                           <= "ZZZZZZZZ";
      local_signal_with_initial_value <= '0';
    else
      if en = '1' then
        d_out                           <= d_in;
        local_signal_with_initial_value <= '0';
      else
        -- array can be created simply by using vector
        d_out <= "ZZZZZZZZ";

      end if;
    end if;
  end process tristate_driver;

  p_rst : process (rst)
    procedure test(
      input_vector : inout std_logic_vector(1 downto 0);
    )is
    begin
      input_vector <= "11";
    end procedure;
  begin
    if rst = '1' then
      d2_out <= local_signal_with_initial_value;

    end if;
  end process;

end behavior;