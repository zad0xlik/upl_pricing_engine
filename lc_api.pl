#!/usr/local/bin/perl
use strict;
use warnings;
use LendingClub::API;
use Data::Dumper;
use JSON;
use DateTime;

my $lcapi_object = new LendingClub::API( "73749336", "sOP6vjpfhhzBd0AaqoodrvvC9Qw=" );
my $ref = $lcapi_object->listed_loans("TRUE");

my @array;
my $row = 0;
my $array_ref;

my $dt = DateTime->now( time_zone => 'America/New_York' );

my $load_date = $dt->ymd('/');
my $load_time = $dt->hms;

my $date = $ref->{'asOfDate'} //= '9999';
my @loans = $ref->{'loans'} //= '9999';

print Dumper($ref);

################

#my @result = formatChain();
#foreach (@result) {
#    print @{$_};
#    print "\n";scdiu
#}

#sub get_credentials {
#    my ($file) = @_;
#    open my $fh, "<", $file or die $!;
#
#    my $line = <$fh>;
#    chomp($line);
#    return ($line)
#
#};
#
#my ($dbInfo, $pguser, $pgpass) = split /~/, get_credentials("/home/zad0xlik/.qtrack_pg.conf");
#
#my $db = DBI->connect($dbInfo,
#    $pguser,
#    $pgpass,
#    {AutoCommit=>1,RaiseError=>1,PrintError=>0}
#) || die "Database connection not made: $DBI::errstr";
#
#my $sins = $db->prepare("INSERT INTO ". $table ." () VALUES()");

################

#sub formatChain {
    foreach (@loans)
    {

        foreach (@{$_}) {
		
            push @{ $array_ref }, $load_date;
            push @{ $array_ref }, $load_time;
            push @{ $array_ref }, $date;
            push @{ $array_ref }, @{$_}{'dti'} //= '9999';
            push @{ $array_ref }, @{$_}{'isIncV'} //= '9999';
            push @{ $array_ref }, @{$_}{'mthsSinceRecentBc'} //= '9999';
            push @{ $array_ref }, @{$_}{'numTl120dpd2m'} //= '9999';
            push @{ $array_ref }, @{$_}{'moSinOldRevTlOp'} //= '9999';
            push @{ $array_ref }, @{$_}{'numTl30dpd'} //= '9999';
            push @{ $array_ref }, @{$_}{'numTl90gDpd24m'} //= '9999';
            push @{ $array_ref }, @{$_}{'numAcctsEver120Ppd'} //= '9999';
            push @{ $array_ref }, @{$_}{'reviewStatus'} //= '9999';
            push @{ $array_ref }, @{$_}{'bcOpenToBuy'} //= '9999';
            push @{ $array_ref }, @{$_}{'collections12MthsExMed'} //= '9999';
            push @{ $array_ref }, @{$_}{'expD'} //= '9999';
            push @{ $array_ref }, @{$_}{'creditPullD'} //= '9999';
            push @{ $array_ref }, @{$_}{'numOpRevTl'} //= '9999';
            push @{ $array_ref }, @{$_}{'inqLast6Mths'} //= '9999';
            push @{ $array_ref }, @{$_}{'fundedAmount'} //= '9999';
            push @{ $array_ref }, @{$_}{'ficoRangeLow'} //= '9999';
            push @{ $array_ref }, @{$_}{'homeOwnership'} //= '9999';
            push @{ $array_ref }, @{$_}{'empTitle'} //= '9999';
            push @{ $array_ref }, @{$_}{'totCollAmt'} //= '9999';
            push @{ $array_ref }, @{$_}{'totalRevHiLim'} //= '9999';
            push @{ $array_ref }, @{$_}{'moSinOldIlAcct'} //= '9999';
            push @{ $array_ref }, @{$_}{'isIncVJoint'} //= '9999';
            push @{ $array_ref }, @{$_}{'chargeoffWithin12Mths'} //= '9999';
            push @{ $array_ref }, @{$_}{'totCurBal'} //= '9999';
            push @{ $array_ref }, @{$_}{'mthsSinceRecentRevolDelinq'} //= '9999';
            push @{ $array_ref }, @{$_}{'totHiCredLim'} //= '9999';
            push @{ $array_ref }, @{$_}{'inqLast12m'} //= '9999';
            push @{ $array_ref }, @{$_}{'numActvBcTl'} //= '9999';
            push @{ $array_ref }, @{$_}{'desc'} //= '9999';
            push @{ $array_ref }, @{$_}{'openIl24m'} //= '9999';
            push @{ $array_ref }, @{$_}{'empLength'} //= '9999';
            push @{ $array_ref }, @{$_}{'allUtil'} //= '9999';
            push @{ $array_ref }, @{$_}{'openIl12m'} //= '9999';
            push @{ $array_ref }, @{$_}{'mortAcc'} //= '9999';
            push @{ $array_ref }, @{$_}{'numIlTl'} //= '9999';
            push @{ $array_ref }, @{$_}{'subGrade'} //= '9999';
            push @{ $array_ref }, @{$_}{'numTlOpPast12m'} //= '9999';
            push @{ $array_ref }, @{$_}{'pubRecBankruptcies'} //= '9999';
            push @{ $array_ref }, @{$_}{'bcUtil'} //= '9999';
            push @{ $array_ref }, @{$_}{'numBcTl'} //= '9999';
            push @{ $array_ref }, @{$_}{'totalCuTl'} //= '9999';
            push @{ $array_ref }, @{$_}{'openAcc'} //= '9999';
            push @{ $array_ref }, @{$_}{'memberId'} //= '9999';
            push @{ $array_ref }, @{$_}{'totalBalIl'} //= '9999';
            push @{ $array_ref }, @{$_}{'annualIncJoint'} //= '9999';
            push @{ $array_ref }, @{$_}{'iLUtil'} //= '9999';
            push @{ $array_ref }, @{$_}{'reviewStatusD'} //= '9999';
            push @{ $array_ref }, @{$_}{'addrState'} //= '9999';
            push @{ $array_ref }, @{$_}{'id'} //= '9999';
            push @{ $array_ref }, @{$_}{'expDefaultRate'} //= '9999';
            push @{ $array_ref }, @{$_}{'maxBalBc'} //= '9999';
            push @{ $array_ref }, @{$_}{'openAcc6m'} //= '9999';
            push @{ $array_ref }, @{$_}{'initialListStatus'} //= '9999';
            push @{ $array_ref }, @{$_}{'earliestCrLine'} //= '9999';
            push @{ $array_ref }, @{$_}{'numRevAccts'} //= '9999';
            push @{ $array_ref }, @{$_}{'totalBalExMort'} //= '9999';
            push @{ $array_ref }, @{$_}{'accOpenPast24Mths'} //= '9999';
            push @{ $array_ref }, @{$_}{'mthsSinceLastRecord'} //= '9999';
            push @{ $array_ref }, @{$_}{'pubRec'} //= '9999';
            push @{ $array_ref }, @{$_}{'delinq2Yrs'} //= '9999';
            push @{ $array_ref }, @{$_}{'acceptD'} //= '9999';
            push @{ $array_ref }, @{$_}{'totalIlHighCreditLimit'} //= '9999';
            push @{ $array_ref }, @{$_}{'pctTlNvrDlq'} //= '9999';
            push @{ $array_ref }, @{$_}{'percentBcGt75'} //= '9999';
            push @{ $array_ref }, @{$_}{'delinqAmnt'} //= '9999';
            push @{ $array_ref }, @{$_}{'revolUtil'} //= '9999';
            push @{ $array_ref }, @{$_}{'annualInc'} //= '9999';
            push @{ $array_ref }, @{$_}{'mthsSinceLastDelinq'} //= '9999';
            push @{ $array_ref }, @{$_}{'accNowDelinq'} //= '9999';
            push @{ $array_ref }, @{$_}{'numActvRevTl'} //= '9999';
            push @{ $array_ref }, @{$_}{'openRv12m'} //= '9999';
            push @{ $array_ref }, @{$_}{'installment'} //= '9999';
            push @{ $array_ref }, @{$_}{'grade'} //= '9999';
            push @{ $array_ref }, @{$_}{'addrZip'} //= '9999';
            push @{ $array_ref }, @{$_}{'loanAmount'} //= '9999';
            push @{ $array_ref }, @{$_}{'investorCount'} //= '9999';
            push @{ $array_ref }, @{$_}{'mthsSinceRcntIl'} //= '9999';
            push @{ $array_ref }, @{$_}{'mthsSinceRecentBcDlq'} //= '9999';
            push @{ $array_ref }, @{$_}{'applicationType'} //= '9999';
            push @{ $array_ref }, @{$_}{'numSats'} //= '9999';
            push @{ $array_ref }, @{$_}{'totalBcLimit'} //= '9999';
            push @{ $array_ref }, @{$_}{'numRevTlBalGt0'} //= '9999';
            push @{ $array_ref }, @{$_}{'openIl6m'} //= '9999';
            push @{ $array_ref }, @{$_}{'totalAcc'} //= '9999';
            push @{ $array_ref }, @{$_}{'term'} //= '9999';
            push @{ $array_ref }, @{$_}{'ilsExpD'} //= '9999';
            push @{ $array_ref }, @{$_}{'mthsSinceLastMajorDerog'} //= '9999';
            push @{ $array_ref }, @{$_}{'ficoRangeHigh'} //= '9999';
            push @{ $array_ref }, @{$_}{'avgCurBal'} //= '9999';
            push @{ $array_ref }, @{$_}{'moSinRcntTl'} //= '9999';
            push @{ $array_ref }, @{$_}{'listD'} //= '9999';
            push @{ $array_ref }, @{$_}{'openRv24m'} //= '9999';
            push @{ $array_ref }, @{$_}{'inqFi'} //= '9999';
            push @{ $array_ref }, @{$_}{'mthsSinceRecentInq'} //= '9999';
            push @{ $array_ref }, @{$_}{'dtiJoint'} //= '9999';
            push @{ $array_ref }, @{$_}{'revolBal'} //= '9999';
            push @{ $array_ref }, @{$_}{'numBcSats'} //= '9999';
            push @{ $array_ref }, @{$_}{'serviceFeeRate'} //= '9999';
            push @{ $array_ref }, @{$_}{'moSinRcntRevTlOp'} //= '9999';
            push @{ $array_ref }, @{$_}{'intRate'} //= '9999';
            push @{ $array_ref }, @{$_}{'taxLiens'} //= '9999';
            push @{ $array_ref }, @{$_}{'purpose'} //= '9999';

#            print join(';',@{ $array_ref }, "\n");

            push @{$array[$row]}, @{ $array_ref };
            $row++;

            @{ $array_ref } = ();

        }

    }

#    return @array;
#}


