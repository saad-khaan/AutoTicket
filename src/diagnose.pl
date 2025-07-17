#!/usr/bin/perl
# diagnose.pl
# Author: Saad Khan
# Purpose: Read tickets from SQLite, ping endpoints, write diagnostics.log

use strict;
use warnings;
use DBI;
use POSIX qw(strftime);
use File::Path qw(make_path);

# Paths
my $db_path   = "../tickets.db";
my $log_dir   = "../data/diagnostics_output";
my $log_file  = "$log_dir/diagnostics.log";

# Ensure log directory exists
if ( !-d $log_dir ) {
    make_path($log_dir) or die "Failed to create log directory: $!";
}

# Connect to SQLite
my $dbh = DBI->connect("dbi:SQLite:dbname=$db_path","","",{ RaiseError => 1, AutoCommit => 1 })
    or die "Could not connect to database: $DBI::errstr";

# Fetch tickets
my $sth = $dbh->prepare("SELECT id, endpoint FROM tickets");
$sth->execute();
my @tickets;
while (my @row = $sth->fetchrow_array) {
    push @tickets, \@row;
}
$sth->finish();
$dbh->disconnect();

# Open diagnostics log for writing
open(my $logfh, '>', $log_file) or die "Cannot write log file: $!";

foreach my $ticket (@tickets) {
    my ($id, $endpoint) = @$ticket;
    my $status = ping_host($endpoint) ? "SUCCESS" : "FAIL";
    my $timestamp = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime());
    print $logfh "$timestamp | Ticket #$id | $endpoint | $status\n";
    print "[INFO] Ticket #$id ($endpoint) => $status\n";
}

close($logfh);
print "[INFO] Diagnostics complete. Log saved to $log_file\n";

# Helper function to ping
sub ping_host {
    my $host = shift;
    my $param = ($^O eq 'MSWin32') ? '-n 1' : '-c 1';
    my $cmd = "ping $param $host >nul 2>&1";
    my $rc = system($cmd);
    return $rc == 0;
}