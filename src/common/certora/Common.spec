// Checks if method is related to the reachability rule
definition isReachabilityRelated(method f) returns bool = 
	f.selector == sig:reachabilitySuccess().selector || 
	f.selector == sig:reachabilityFail().selector;

// Checks that all methods have a none reverting path
rule reachability(method f) filtered { f -> isReachabilityRelated(f) }
{
	env e;
	calldataarg args;
	f(e,args);
	satisfy true;
}
