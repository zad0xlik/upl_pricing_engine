#!/usr/local/bin/perl
use strict;
use warnings;
use LendingClub::API;
use Data::Dumper;
use JSON;

my $lcapi_object = new LendingClub::API( "73749336", "sOP6vjpfhhzBd0AaqoodrvvC9Qw=" );

my $listed_loans = Dumper( $lcapi_object->listed_loans() );

print $listed_loans;
