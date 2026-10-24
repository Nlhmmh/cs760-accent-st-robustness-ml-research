# Use the official IEEE class supplied with the literature-review project.
# Preserve the trailing colon so normal TeX packages can still be found.
$ENV{'TEXINPUTS'} = '../../literature_review/IEEE-conference-template-062824:'
  . ($ENV{'TEXINPUTS'} // '');
$pdf_mode = 1;
$pdflatex = '/Library/TeX/texbin/pdflatex %O %S';