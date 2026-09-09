# Prefer the IEEEtran class distributed with this repository over any
# system-installed copy. Keep the trailing colon so standard TeX packages
# remain discoverable.
$ENV{'TEXINPUTS'} = '../IEEE-conference-template-062824:'
  . ($ENV{'TEXINPUTS'} // '');
