#analyze.pl
#Author : Saad Khan

#!/usr/bin/perl
use strict;
use warnings;

# Allow passing a log file path as an argument
my $log_file = $ARGV[0] // "../data/diagnostics_output/diagnostics.log";

# Check if file exists
unless (-e $log_file) {
    die "Log file not found: $log_file\n";
}

open(my $fh, '<', $log_file) or die "Could not open log file: $!";

my $success = 0;
my $fail = 0;

# Read each line of the log
while (my $line = <$fh>) {
    if ($line =~ /SUCCESS/) {
        $success++;
    } elsif ($line =~ /FAIL/) {
        $fail++;
    }
}

close($fh);

# Print summary
print "=== Diagnostics Analysis Report ===\n";
print "Log file: $log_file\n";
print "Successful pings: $success\n";
print "Failed pings: $fail\n";
print "-----------------------------------\n";