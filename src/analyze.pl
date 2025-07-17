#analyze.pl
#Author: Saad Khan

#!/usr/bin/perl
use strict;
use warnings;

# Path to the diagnostics log
my $log_file = "../data/diagnostics_output/diagnostics.log";

# Try opening the log file
open(my $fh, '<', $log_file) or die "Could not open log file: $!";

my $success = 0;
my $fail = 0;

# Read the log line by line
while (my $line = <$fh>) {
    if ($line =~ /SUCCESS/) {
        $success++;
    } elsif ($line =~ /FAIL/) {
        $fail++;
    }
}

close($fh);

# Print the summary report
print "=== Diagnostics Analysis Report ===\n";
print "Successful pings: $success\n";
print "Failed pings: $fail\n";
print "-----------------------------------\n";